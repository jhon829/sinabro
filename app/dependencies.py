"""
Sinabro FastAPI 공통 의존성
인증, 권한, 세션 관리 등
"""

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional, Union
import logging

from database import get_db, check_db_connection
from config import settings

logger = logging.getLogger(__name__)

# JWT 토큰 스키마 (향후 인증 구현용)
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
):
    """
    현재 사용자 정보 조회 (JWT 토큰 기반)
    해커톤에서는 비활성화, 추후 구현 예정
    """
    # 해커톤 모드에서는 인증 비활성화
    if settings.DEMO_MODE:
        return {"user_id": "demo_user", "user_type": "demo"}
    
    # 실제 JWT 토큰 검증 로직 (추후 구현)
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증이 필요합니다",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # TODO: JWT 토큰 검증 및 사용자 정보 조회
    return {"user_id": "authenticated_user"}


async def verify_database_connection():
    """데이터베이스 연결 상태 확인"""
    if not check_db_connection():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="데이터베이스 연결 실패"
        )
    return True


def get_access_code_from_request(request: Request) -> Optional[str]:
    """
    요청에서 접속 코드 추출
    헤더 또는 쿼리 파라미터에서 추출
    """
    # Authorization 헤더에서 추출
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Access "):
        return auth_header[7:]  # "Access " 제거
    
    # 쿼리 파라미터에서 추출
    return request.query_params.get("access_code")


class AccessCodeDependency:
    """접속 코드 의존성 클래스"""
    
    def __init__(self, required: bool = True):
        self.required = required
    
    async def __call__(
        self, 
        request: Request, 
        db: Session = Depends(get_db)
    ) -> Optional[dict]:
        """접속 코드 검증 및 사용자 정보 반환"""
        access_code = get_access_code_from_request(request)
        
        if not access_code and self.required:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="접속 코드가 필요합니다"
            )
        
        if not access_code:
            return None
        
        # 데이터베이스에서 접속 코드 검증
        try:
            result = db.execute("""
                SELECT 
                    ac.user_type,
                    ac.user_id,
                    ac.channel_id,
                    ac.is_used,
                    ac.expires_at
                FROM access_codes ac
                WHERE ac.code = :code AND ac.expires_at > NOW()
            """, {"code": access_code}).first()
            
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="유효하지 않은 접속 코드입니다"
                )
            
            return {
                "access_code": access_code,
                "user_type": result.user_type,
                "user_id": result.user_id,
                "channel_id": result.channel_id,
                "is_used": result.is_used
            }
        
        except Exception as e:
            logger.error(f"Access code verification failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="접속 코드 검증 중 오류가 발생했습니다"
            )


# 의존성 인스턴스들
require_access_code = AccessCodeDependency(required=True)
optional_access_code = AccessCodeDependency(required=False)


def get_pagination_params(
    page: int = 1,
    size: int = 10,
    max_size: int = 100
) -> dict:
    """페이징 파라미터 검증 및 반환"""
    if page < 1:
        page = 1
    if size < 1:
        size = 10
    if size > max_size:
        size = max_size
    
    offset = (page - 1) * size
    
    return {
        "page": page,
        "size": size,
        "offset": offset,
        "limit": size
    }


async def log_request(request: Request):
    """요청 로깅"""
    if settings.DEBUG:
        logger.info(f"{request.method} {request.url}")
        if request.headers.get("content-type") == "application/json":
            try:
                body = await request.body()
                if body:
                    logger.debug(f"Request body: {body.decode()[:200]}...")
            except Exception:
                pass
    return True


# 공통 의존성 조합
CommonDeps = Depends(verify_database_connection)
