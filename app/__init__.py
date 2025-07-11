"""
Sinabro FastAPI 애플리케이션 패키지
재외동포 시니어 간병 서비스 API
"""

__version__ = "1.0.0"
__author__ = "Sinabro Development Team"
__description__ = "AI-powered senior care service for overseas Korean families"

# 패키지 레벨 imports
from .config import settings
from .database import get_db, db_manager, check_db_connection

__all__ = [
    "settings",
    "get_db", 
    "db_manager",
    "check_db_connection"
]
