"""
Access Code Service for Sinabro API
접속 코드 관련 비즈니스 로직
"""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, Dict, Any
from datetime import datetime
import logging

from ..models import AccessCode, Guardian, Caregiver, Channel, Senior
from .base import BaseService

logger = logging.getLogger(__name__)


class AccessCodeService(BaseService):
    """접속 코드 서비스"""
    
    def get_access_code_info(self, code: str) -> Dict[str, Any]:
        """
        접속 코드로 사용자 정보 조회
        
        Args:
            code: 접속 코드 (예: GUARD001, CARE001)
            
        Returns:
            Dict containing access code info, user info, and channel info
        """
        try:
            # 접속 코드 조회
            access_code = self.db.query(AccessCode).filter(
                AccessCode.code == code.upper()
            ).first()
            
            if not access_code:
                return self.create_error_response(
                    message="유효하지 않은 접속 코드입니다.",
                    error_code="INVALID_ACCESS_CODE"
                )
            
            # 만료 시간 확인
            if access_code.expires_at < datetime.now():
                return self.create_error_response(
                    message="만료된 접속 코드입니다.",
                    error_code="EXPIRED_ACCESS_CODE"
                )
            
            # 사용자 정보 조회
            user_info = None
            if access_code.user_type == "guardian":
                user = self.db.query(Guardian).filter(
                    Guardian.id == access_code.user_id
                ).first()
                if user:
                    user_info = user.to_dict()
            
            elif access_code.user_type == "caregiver":
                user = self.db.query(Caregiver).filter(
                    Caregiver.id == access_code.user_id
                ).first()
                if user:
                    user_info = user.to_dict()
            
            if not user_info:
                return self.create_error_response(
                    message="사용자 정보를 찾을 수 없습니다.",
                    error_code="USER_NOT_FOUND"
                )
            
            # 채널 정보 조회 (있는 경우)
            channel_info = None
            if access_code.channel_id:
                channel = self.db.query(Channel).options(
                    joinedload(Channel.guardian),
                    joinedload(Channel.caregiver),
                    joinedload(Channel.senior)
                ).filter(Channel.id == access_code.channel_id).first()
                
                if channel:
                    channel_info = {
                        "id": str(channel.id),
                        "channel_name": channel.channel_name,
                        "status": channel.status,
                        "start_date": channel.start_date.isoformat() if channel.start_date else None,
                        "senior_name": channel.senior.full_name if channel.senior else None
                    }
            
            # 응답 데이터 구성
            response_data = {
                "access_code": {
                    "code": access_code.code,
                    "user_type": access_code.user_type,
                    "is_used": access_code.is_used,
                    "expires_at": access_code.expires_at.isoformat()
                },
                "user_info": user_info,
                "channel_info": channel_info
            }
            
            return self.create_response(
                message="접속 코드 정보를 성공적으로 조회했습니다.",
                data=response_data
            )
            
        except SQLAlchemyError as e:
            return self.handle_db_error(e, "get access code info")
        except Exception as e:
            logger.error(f"Unexpected error in get_access_code_info: {str(e)}")
            return self.create_error_response(
                message="서버 오류가 발생했습니다.",
                error_code="INTERNAL_ERROR"
            )
    
    def mark_as_used(self, code: str) -> Dict[str, Any]:
        """
        접속 코드를 사용됨으로 표시
        
        Args:
            code: 접속 코드
            
        Returns:
            Success response
        """
        try:
            access_code = self.db.query(AccessCode).filter(
                AccessCode.code == code.upper()
            ).first()
            
            if not access_code:
                return self.create_error_response(
                    message="유효하지 않은 접속 코드입니다.",
                    error_code="INVALID_ACCESS_CODE"
                )
            
            access_code.is_used = True
            self.db.commit()
            
            return self.create_response(
                message="접속 코드가 사용됨으로 표시되었습니다."
            )
            
        except SQLAlchemyError as e:
            return self.handle_db_error(e, "mark access code as used")
        except Exception as e:
            logger.error(f"Unexpected error in mark_as_used: {str(e)}")
            return self.create_error_response(
                message="서버 오류가 발생했습니다.",
                error_code="INTERNAL_ERROR"
            )
