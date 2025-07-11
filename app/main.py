"""
Sinabro FastAPI 메인 애플리케이션
재외동포 시니어 간병 서비스 API
"""

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import logging
import time
from contextlib import asynccontextmanager

from config import settings
from database import init_db, check_db_connection, get_db_info, db_manager
from dependencies import verify_database_connection, log_request
from routers import access_code_router, channel_router, checklist_router

# 로깅 설정
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 생명주기 관리"""
    # 시작 시 실행
    logger.info("🚀 Sinabro API 서버 시작")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Demo mode: {settings.DEMO_MODE}")
    
    # 데이터베이스 연결 확인
    if check_db_connection():
        logger.info("✅ 데이터베이스 연결 성공")
    else:
        logger.error("❌ 데이터베이스 연결 실패")
    
    yield
    
    # 종료 시 실행
    logger.info("🛑 Sinabro API 서버 종료")


# FastAPI 애플리케이션 생성
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    **Sinabro** - 재외동포 시니어 간병 서비스 API
    
    해외에 거주하는 가족을 위한 AI 기반 시니어 케어 플랫폼입니다.
    
    ## 주요 기능
    * 📋 체크리스트 기반 간병 기록
    * 🤖 AI 자동 리포트 생성  
    * 🌐 다국어 실시간 번역
    * 💬 실시간 피드백 루프
    * 📸 사진 및 돌봄노트 관리
    
    ## 해커톤 데모용 접속 코드
    * 가디언: `GUARD001`, `GUARD002`, `GUARD003`
    * 케어기버: `CARE001`, `CARE002`, `CARE003`
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)


# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted Host 미들웨어 설정  
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.TRUSTED_HOSTS
)


# 요청 로깅 미들웨어
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    """요청/응답 로깅"""
    start_time = time.time()
    
    # 요청 로깅
    if settings.DEBUG:
        logger.info(f"📨 {request.method} {request.url}")
    
    # 요청 처리
    response = await call_next(request)
    
    # 응답 시간 계산
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # 응답 로깅
    if settings.DEBUG:
        logger.info(f"📤 {response.status_code} - {process_time:.4f}s")
    
    return response


# 전역 예외 핸들러
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """전역 예외 처리"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "서버 내부 오류가 발생했습니다",
            "detail": str(exc) if settings.DEBUG else "Internal server error",
            "type": "server_error"
        }
    )


# 기본 라우트들
@app.get("/", tags=["기본"])
async def root():
    """API 루트 엔드포인트"""
    return {
        "message": "🏠 Sinabro 재외동포 시니어 간병 서비스 API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health",
        "environment": settings.ENVIRONMENT,
        "demo_mode": settings.DEMO_MODE
    }


@app.get("/health", tags=["시스템"])
async def health_check():
    """시스템 헬스체크"""
    db_health = db_manager.health_check()
    
    system_status = {
        "status": "healthy" if db_health["status"] == "healthy" else "unhealthy",
        "timestamp": time.time(),
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "services": {
            "database": db_health,
            "api": {"status": "healthy"}
        }
    }
    
    if system_status["status"] == "unhealthy":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=system_status
        )
    
    return system_status


@app.get("/info", tags=["시스템"])
async def system_info(_: None = Depends(verify_database_connection)):
    """시스템 정보 조회"""
    db_info = get_db_info()
    table_counts = db_manager.get_table_count()
    
    return {
        "application": {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
            "debug": settings.DEBUG,
            "demo_mode": settings.DEMO_MODE
        },
        "database": db_info,
        "table_counts": table_counts,
        "demo_codes": {
            "guardian": [settings.DEMO_GUARDIAN_CODE, "GUARD002", "GUARD003"],
            "caregiver": [settings.DEMO_CAREGIVER_CODE, "CARE002", "CARE003"]
        } if settings.DEMO_MODE else None
    }


@app.get("/demo", tags=["데모"])  
async def demo_info():
    """해커톤 데모 정보"""
    if not settings.DEMO_MODE:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="데모 모드가 비활성화되어 있습니다"
        )
    
    return {
        "title": "🎭 Sinabro 해커톤 데모",
        "description": "재외동포 시니어 간병 서비스 시연용 API",
        "demo_scenario": {
            "step1": "CARE001 코드로 케어기버 로그인",
            "step2": "김영희님 체크리스트 작성 및 돌봄노트 기록",
            "step3": "AI 리포트 자동 생성 (150자 요약 + 가족 코멘트)",
            "step4": "GUARD001 코드로 가디언(아들) 로그인",
            "step5": "리포트 확인 및 피드백 작성",
            "step6": "실시간 피드백 루프 시연"
        },
        "access_codes": {
            "guardians": {
                "GUARD001": "김철수 (미국 뉴욕) - 김영희님 아들",
                "GUARD002": "이영희 (캐나다 토론토) - 이순자님 딸", 
                "GUARD003": "박민수 (일본 도쿄) - 박할아버지 아들"
            },
            "caregivers": {
                "CARE001": "최간병 (5년 경력) - 김영희님 담당",
                "CARE002": "정돌봄 (8년 경력) - 이순자님 담당",
                "CARE003": "한간호 (3년 경력) - 박할아버지 담당"
            }
        },
        "test_endpoints": [
            "GET /api/v1/access/{code} - 접속 코드로 사용자 정보 조회",
            "POST /api/v1/access/{code}/mark-used - 접속 코드 사용 표시",
            "GET /api/v1/channels/my - 내 채널 목록 조회",
            "GET /api/v1/channels/{id} - 채널 상세 정보",
            "GET /api/v1/checklists/templates - 체크리스트 템플릿 목록",
            "GET /api/v1/checklists/templates/{id} - 템플릿 상세 정보",
            "GET /api/v1/checklists/templates/category/{category} - 카테고리별 템플릿"
        ],
        "implemented_apis": {
            "total": 7,
            "status": "✅ 7단계 완료 - 기본 API 엔드포인트 구현됨",
            "next_step": "8단계 - Docker 실행 및 테스트"
        }
    }


# API 라우터 등록
app.include_router(access_code_router, tags=["접속 코드"])
app.include_router(channel_router, tags=["채널"])
app.include_router(checklist_router, tags=["체크리스트"])

# 향후 추가 예정 라우터들
# app.include_router(care_notes_router, prefix=f"{settings.API_PREFIX}/care-notes", tags=["돌봄노트"])  
# app.include_router(ai_reports_router, prefix=f"{settings.API_PREFIX}/ai-reports", tags=["AI 리포트"])
# app.include_router(feedback_router, prefix=f"{settings.API_PREFIX}/feedback", tags=["피드백"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "info"
    )
