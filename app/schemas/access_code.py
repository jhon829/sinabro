"""
Access code related schemas for Sinabro API
접속 코드 관련 스키마들
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Union
from uuid import UUID

from .base import BaseResponse
from .user import GuardianInfo, CaregiverInfo, SeniorInfo


class AccessCodeInfo(BaseModel):
    """접속 코드 정보 스키마"""
    id: UUID = Field(description="접속 코드 ID")
    code: str = Field(description="접속 코드")
    user_type: str = Field(description="사용자 유형 (guardian/caregiver)")
    user_id: UUID = Field(description="사용자 ID")
    channel_id: Optional[UUID] = Field(None, description="채널 ID")
    is_used: bool = Field(default=False, description="사용 여부")
    expires_at: datetime = Field(description="만료 시간")
    created_at: datetime = Field(description="생성일시")


class AccessCodeResponse(BaseResponse):
    """접속 코드 조회 응답 스키마"""
    data: dict = Field(description="접속 코드 및 사용자 정보")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "접속 코드 정보를 성공적으로 조회했습니다.",
                "data": {
                    "access_code": {
                        "code": "GUARD001",
                        "user_type": "guardian",
                        "is_used": False,
                        "expires_at": "2025-07-10T12:00:00Z"
                    },
                    "user_info": {
                        "id": "550e8400-e29b-41d4-a716-446655440001",
                        "full_name": "김철수",
                        "country": "미국",
                        "city": "뉴욕"
                    },
                    "channel_info": {
                        "id": "550e8400-e29b-41d4-a716-446655440010",
                        "channel_name": "김영희님 케어채널",
                        "status": "active"
                    }
                }
            }
        }
