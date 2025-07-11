"""
Base service class for Sinabro API
기본 서비스 클래스
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List, Dict, Any
from uuid import UUID
import logging

logger = logging.getLogger(__name__)


class BaseService:
    """기본 서비스 클래스"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def handle_db_error(self, error: Exception, operation: str = "database operation"):
        """데이터베이스 에러 처리"""
        logger.error(f"Database error during {operation}: {str(error)}")
        if isinstance(error, SQLAlchemyError):
            self.db.rollback()
        raise error
    
    def create_response(self, success: bool = True, message: str = "OK", data: Any = None, error_code: str = None):
        """표준 응답 생성"""
        response = {
            "success": success,
            "message": message
        }
        
        if data is not None:
            response["data"] = data
            
        if error_code:
            response["error_code"] = error_code
            
        return response
    
    def create_error_response(self, message: str, error_code: str = None, details: Dict[str, Any] = None):
        """에러 응답 생성"""
        response = {
            "success": False,
            "message": message
        }
        
        if error_code:
            response["error_code"] = error_code
            
        if details:
            response["details"] = details
            
        return response
