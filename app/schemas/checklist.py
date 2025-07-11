"""
Checklist template related schemas for Sinabro API
체크리스트 템플릿 관련 스키마들
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

from .base import BaseResponse, PaginatedResponse


class ChecklistItem(BaseModel):
    """체크리스트 아이템 스키마"""
    id: int = Field(description="아이템 ID")
    text: str = Field(description="아이템 텍스트")
    required: bool = Field(default=False, description="필수 항목 여부")
    type: str = Field(description="아이템 유형")


class ChecklistTemplateInfo(BaseModel):
    """체크리스트 템플릿 정보 스키마"""
    id: UUID = Field(description="템플릿 ID")
    name: str = Field(description="템플릿 이름")
    category: str = Field(description="카테고리")
    items: List[ChecklistItem] = Field(description="체크리스트 아이템 목록")
    is_active: bool = Field(default=True, description="활성 상태")
    created_at: datetime = Field(description="생성일시")


class ChecklistTemplateResponse(BaseResponse):
    """단일 체크리스트 템플릿 응답 스키마"""
    data: ChecklistTemplateInfo = Field(description="체크리스트 템플릿 정보")


class ChecklistTemplateListResponse(BaseResponse):
    """체크리스트 템플릿 목록 응답 스키마"""
    data: List[ChecklistTemplateInfo] = Field(description="체크리스트 템플릿 목록")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "체크리스트 템플릿 목록을 성공적으로 조회했습니다.",
                "data": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440100",
                        "name": "기본 건강관리 체크리스트",
                        "category": "health_management",
                        "items": [
                            {
                                "id": 1,
                                "text": "혈압 측정",
                                "required": True,
                                "type": "health"
                            },
                            {
                                "id": 2,
                                "text": "약물 복용 확인",
                                "required": True,
                                "type": "medication"
                            }
                        ],
                        "is_active": True,
                        "created_at": "2024-01-15T09:00:00Z"
                    }
                ]
            }
        }
