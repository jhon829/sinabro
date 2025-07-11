"""
Channel related schemas for Sinabro API
채널 관련 스키마들
"""

from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List
from uuid import UUID

from .base import BaseResponse, PaginatedResponse
from .user import GuardianInfo, CaregiverInfo, SeniorInfo


class ChannelInfo(BaseModel):
    """채널 정보 스키마"""
    id: UUID = Field(description="채널 ID")
    channel_name: str = Field(description="채널 이름")
    guardian_id: UUID = Field(description="가디언 ID")
    caregiver_id: UUID = Field(description="케어기버 ID")
    senior_id: UUID = Field(description="시니어 ID")
    status: str = Field(description="채널 상태 (active/inactive/completed)")
    start_date: date = Field(description="케어 시작일")
    end_date: Optional[date] = Field(None, description="케어 종료일")
    created_at: datetime = Field(description="생성일시")
    updated_at: datetime = Field(description="수정일시")


class ChannelDetailInfo(ChannelInfo):
    """채널 상세 정보 스키마 (관계 포함)"""
    guardian: Optional[GuardianInfo] = Field(None, description="가디언 정보")
    caregiver: Optional[CaregiverInfo] = Field(None, description="케어기버 정보")
    senior: Optional[SeniorInfo] = Field(None, description="시니어 정보")


class ChannelResponse(BaseResponse):
    """단일 채널 응답 스키마"""
    data: ChannelDetailInfo = Field(description="채널 상세 정보")


class ChannelListResponse(PaginatedResponse):
    """채널 목록 응답 스키마"""
    data: List[ChannelInfo] = Field(description="채널 목록")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "채널 목록을 성공적으로 조회했습니다.",
                "pagination": {
                    "page": 1,
                    "size": 10,
                    "total": 3,
                    "total_pages": 1
                },
                "data": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440010",
                        "channel_name": "김영희님 케어채널",
                        "status": "active",
                        "start_date": "2024-01-15",
                        "created_at": "2024-01-15T09:00:00Z"
                    }
                ]
            }
        }


class MyChannelsResponse(BaseResponse):
    """내 채널 목록 응답 스키마"""
    data: List[ChannelDetailInfo] = Field(description="내 채널 목록 (상세 정보 포함)")
