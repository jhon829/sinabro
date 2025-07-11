"""
Base schemas for Sinabro API
공통으로 사용되는 기본 스키마들
"""

from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from uuid import UUID


class BaseResponse(BaseModel):
    """기본 응답 스키마"""
    success: bool = Field(default=True, description="요청 성공 여부")
    message: str = Field(default="OK", description="응답 메시지")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class ErrorResponse(BaseResponse):
    """에러 응답 스키마"""
    success: bool = Field(default=False)
    error_code: Optional[str] = Field(None, description="에러 코드")
    details: Optional[Dict[str, Any]] = Field(None, description="에러 상세 정보")


class PaginationInfo(BaseModel):
    """페이지네이션 정보"""
    page: int = Field(ge=1, description="현재 페이지")
    size: int = Field(ge=1, le=100, description="페이지 크기")
    total: int = Field(ge=0, description="전체 항목 수")
    total_pages: int = Field(ge=0, description="전체 페이지 수")


class PaginatedResponse(BaseResponse):
    """페이지네이션된 응답 스키마"""
    pagination: PaginationInfo = Field(description="페이지네이션 정보")
    data: List[Any] = Field(default_factory=list, description="데이터 목록")
