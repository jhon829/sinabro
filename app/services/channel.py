"""
Channel Service for Sinabro API
채널 관련 비즈니스 로직
"""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List, Dict, Any
from uuid import UUID
import logging

from ..models import Channel, Guardian, Caregiver, Senior
from .base import BaseService

logger = logging.getLogger(__name__)


class ChannelService(BaseService):
    """채널 서비스"""
    
    def get_my_channels(self, user_id: UUID, user_type: str) -> Dict[str, Any]:
        """
        사용자의 채널 목록 조회
        
        Args:
            user_id: 사용자 ID
            user_type: 사용자 유형 ('guardian' or 'caregiver')
            
        Returns:
            Dict containing user's channels with detailed info
        """
        try:
            # 사용자 유형에 따라 필터링
            query = self.db.query(Channel).options(
                joinedload(Channel.guardian),
                joinedload(Channel.caregiver),
                joinedload(Channel.senior)
            )
            
            if user_type == "guardian":
                channels = query.filter(Channel.guardian_id == user_id).all()
            elif user_type == "caregiver":
                channels = query.filter(Channel.caregiver_id == user_id).all()
            else:
                return self.create_error_response(
                    message="유효하지 않은 사용자 유형입니다.",
                    error_code="INVALID_USER_TYPE"
                )
            
            # 채널 정보를 딕셔너리로 변환
            channels_data = []
            for channel in channels:
                channel_data = {
                    "id": str(channel.id),
                    "channel_name": channel.channel_name,
                    "guardian_id": str(channel.guardian_id),
                    "caregiver_id": str(channel.caregiver_id),
                    "senior_id": str(channel.senior_id),
                    "status": channel.status,
                    "start_date": channel.start_date.isoformat() if channel.start_date else None,
                    "end_date": channel.end_date.isoformat() if channel.end_date else None,
                    "created_at": channel.created_at.isoformat() if channel.created_at else None,
                    "updated_at": channel.updated_at.isoformat() if channel.updated_at else None,
                    
                    # 관계 정보
                    "guardian": channel.guardian.to_dict() if channel.guardian else None,
                    "caregiver": channel.caregiver.to_dict() if channel.caregiver else None,
                    "senior": channel.senior.to_dict() if channel.senior else None
                }
                channels_data.append(channel_data)
            
            return self.create_response(
                message=f"{len(channels_data)}개의 채널을 성공적으로 조회했습니다.",
                data=channels_data
            )
            
        except SQLAlchemyError as e:
            return self.handle_db_error(e, "get my channels")
        except Exception as e:
            logger.error(f"Unexpected error in get_my_channels: {str(e)}")
            return self.create_error_response(
                message="서버 오류가 발생했습니다.",
                error_code="INTERNAL_ERROR"
            )
    
    def get_channel_by_id(self, channel_id: UUID) -> Dict[str, Any]:
        """
        채널 ID로 상세 정보 조회
        
        Args:
            channel_id: 채널 ID
            
        Returns:
            Dict containing channel detailed info
        """
        try:
            channel = self.db.query(Channel).options(
                joinedload(Channel.guardian),
                joinedload(Channel.caregiver),
                joinedload(Channel.senior)
            ).filter(Channel.id == channel_id).first()
            
            if not channel:
                return self.create_error_response(
                    message="채널을 찾을 수 없습니다.",
                    error_code="CHANNEL_NOT_FOUND"
                )
            
            channel_data = {
                "id": str(channel.id),
                "channel_name": channel.channel_name,
                "guardian_id": str(channel.guardian_id),
                "caregiver_id": str(channel.caregiver_id),
                "senior_id": str(channel.senior_id),
                "status": channel.status,
                "start_date": channel.start_date.isoformat() if channel.start_date else None,
                "end_date": channel.end_date.isoformat() if channel.end_date else None,
                "created_at": channel.created_at.isoformat() if channel.created_at else None,
                "updated_at": channel.updated_at.isoformat() if channel.updated_at else None,
                
                # 관계 정보
                "guardian": channel.guardian.to_dict() if channel.guardian else None,
                "caregiver": channel.caregiver.to_dict() if channel.caregiver else None,
                "senior": channel.senior.to_dict() if channel.senior else None
            }
            
            return self.create_response(
                message="채널 정보를 성공적으로 조회했습니다.",
                data=channel_data
            )
            
        except SQLAlchemyError as e:
            return self.handle_db_error(e, "get channel by id")
        except Exception as e:
            logger.error(f"Unexpected error in get_channel_by_id: {str(e)}")
            return self.create_error_response(
                message="서버 오류가 발생했습니다.",
                error_code="INTERNAL_ERROR"
            )
