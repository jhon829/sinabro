"""
Access Code API Router for Sinabro
접속 코드 관련 API 엔드포인트
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from services import AccessCodeService
from schemas import AccessCodeResponse, ErrorResponse

router = APIRouter(prefix="/api/v1/access", tags=["접속 코드"])


@router.get("/{code}", 
    response_model=AccessCodeResponse,
    summary="접속 코드로 사용자 정보 조회",
    description="접속 코드를 사용하여 해당 사용자의 정보와 연결된 채널 정보를 조회합니다.")
async def get_access_code_info(
    code: str,
    db: Session = Depends(get_db)
):
    """
    접속 코드로 사용자 정보 조회
    
    **사용 예시:**
    - `GUARD001` - 김철수 가디언 정보 조회
    - `CARE001` - 최간병 케어기버 정보 조회
    
    **응답 정보:**
    - 접속 코드 정보 (만료시간, 사용여부 등)
    - 사용자 정보 (가디언 또는 케어기버)
    - 연결된 채널 정보 (있는 경우)
    """
    try:
        # 접속 코드 서비스 인스턴스 생성
        access_code_service = AccessCodeService(db)
        
        # 접속 코드 정보 조회
        result = access_code_service.get_access_code_info(code)
        
        # 에러 응답 처리
        if not result.get("success", True):
            error_code = result.get("error_code")
            message = result.get("message", "알 수 없는 오류가 발생했습니다.")
            
            if error_code == "INVALID_ACCESS_CODE":
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=message
                )
            elif error_code == "EXPIRED_ACCESS_CODE":
                raise HTTPException(
                    status_code=status.HTTP_410_GONE,
                    detail=message
                )
            elif error_code == "USER_NOT_FOUND":
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=message
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=message
                )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="서버 내부 오류가 발생했습니다."
        )


@router.post("/{code}/mark-used",
    summary="접속 코드를 사용됨으로 표시",
    description="접속 코드를 사용됨으로 표시하여 중복 사용을 방지합니다.")
async def mark_access_code_as_used(
    code: str,
    db: Session = Depends(get_db)
):
    """
    접속 코드를 사용됨으로 표시
    
    **사용 시나리오:**
    - 사용자가 성공적으로 로그인한 후 호출
    - 접속 코드의 중복 사용 방지
    """
    try:
        # 접속 코드 서비스 인스턴스 생성
        access_code_service = AccessCodeService(db)
        
        # 접속 코드를 사용됨으로 표시
        result = access_code_service.mark_as_used(code)
        
        # 에러 응답 처리
        if not result.get("success", True):
            error_code = result.get("error_code")
            message = result.get("message", "알 수 없는 오류가 발생했습니다.")
            
            if error_code == "INVALID_ACCESS_CODE":
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=message
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=message
                )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="서버 내부 오류가 발생했습니다."
        )
