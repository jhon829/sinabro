"""
Sinabro 애플리케이션 설정 관리
환경 변수를 통한 설정 값 관리
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator, ConfigDict


class Settings(BaseSettings):
    """애플리케이션 설정 클래스"""
    
    # 앱 기본 설정
    APP_NAME: str = "Sinabro Care API"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # 서버 설정
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # 데이터베이스 설정
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    
    # Redis 설정
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # 보안 설정
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI 서비스 설정
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4"
    GOOGLE_TRANSLATE_API_KEY: Optional[str] = None
    GOOGLE_PROJECT_ID: Optional[str] = None
    
    # 파일 업로드 설정
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10485760  # 10MB
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "gif", "pdf"]
    
    # CORS 설정
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080", 
        "http://127.0.0.1:3000"
    ]
    TRUSTED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    
    # 해커톤 데모 설정
    DEMO_MODE: bool = True
    DEMO_GUARDIAN_CODE: str = "GUARD001"
    DEMO_CAREGIVER_CODE: str = "CARE001"
    
    @property
    def database_url(self) -> str:
        """데이터베이스 URL 생성"""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def redis_url(self) -> str:
        """Redis URL 생성"""
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        """CORS origins 문자열을 리스트로 변환"""
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    @validator("TRUSTED_HOSTS", pre=True)
    def assemble_trusted_hosts(cls, v):
        """Trusted hosts 문자열을 리스트로 변환"""
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    @validator("ALLOWED_EXTENSIONS", pre=True)
    def assemble_allowed_extensions(cls, v):
        """허용된 확장자 문자열을 리스트로 변환"""
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8", 
        case_sensitive=True
    )


# 글로벌 설정 인스턴스
settings = Settings()

# 개발/프로덕션 환경별 설정
def get_settings() -> Settings:
    """설정 객체 반환"""
    return settings

def is_development() -> bool:
    """개발 환경 여부 확인"""
    return settings.ENVIRONMENT == "development"

def is_production() -> bool:
    """프로덕션 환경 여부 확인"""
    return settings.ENVIRONMENT == "production"
