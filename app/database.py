"""
Sinabro 데이터베이스 연결 관리
SQLAlchemy를 사용한 PostgreSQL 연결 설정
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import logging
from typing import Generator

from config import settings

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SQLAlchemy 엔진 생성
engine = create_engine(
    settings.database_url,
    # 연결 풀 설정
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    pool_pre_ping=True,
    # 개발환경에서 SQL 쿼리 로깅
    echo=settings.DEBUG,
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base 클래스 생성 (모든 모델의 기본 클래스)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    데이터베이스 세션 의존성
    FastAPI 의존성 주입에서 사용
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def init_db() -> None:
    """
    데이터베이스 초기화
    테이블 생성 (개발용)
    """
    try:
        # 모든 테이블 생성 (이미 SQL로 생성되어 있으므로 필요시에만)
        # Base.metadata.create_all(bind=engine)
        logger.info("Database initialization completed")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


def check_db_connection() -> bool:
    """
    데이터베이스 연결 상태 확인
    헬스체크에서 사용
    """
    try:
        db = SessionLocal()
        # 간단한 쿼리로 연결 테스트
        db.execute("SELECT 1")
        db.close()
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False


def get_db_info() -> dict:
    """
    데이터베이스 정보 반환
    관리자 API에서 사용
    """
    try:
        db = SessionLocal()
        result = db.execute("""
            SELECT 
                current_database() as database_name,
                current_user as current_user,
                version() as version,
                NOW() as current_time
        """).first()
        db.close()
        
        return {
            "database_name": result.database_name,
            "current_user": result.current_user,
            "version": result.version,
            "current_time": result.current_time,
            "status": "connected"
        }
    except Exception as e:
        logger.error(f"Failed to get database info: {e}")
        return {
            "status": "error",
            "error": str(e)
        }


class DatabaseManager:
    """데이터베이스 관리 클래스"""
    
    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal
    
    def create_session(self) -> Session:
        """새 세션 생성"""
        return self.SessionLocal()
    
    def health_check(self) -> dict:
        """헬스체크"""
        try:
            session = self.create_session()
            session.execute("SELECT 1")
            session.close()
            return {"status": "healthy", "database": "connected"}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
    
    def get_table_count(self) -> dict:
        """테이블별 레코드 수 조회"""
        try:
            session = self.create_session()
            tables = [
                "guardians", "caregivers", "seniors", "channels",
                "checklist_templates", "daily_checklists", "care_notes",
                "photos", "admin_questions", "question_responses",
                "ai_reports", "guardian_feedback", "access_codes"
            ]
            
            counts = {}
            for table in tables:
                result = session.execute(f"SELECT COUNT(*) FROM {table}").scalar()
                counts[table] = result
            
            session.close()
            return counts
        except Exception as e:
            logger.error(f"Failed to get table counts: {e}")
            return {"error": str(e)}


# 글로벌 데이터베이스 매니저 인스턴스
db_manager = DatabaseManager()
