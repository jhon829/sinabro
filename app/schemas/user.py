"""
User-related schemas for Sinabro API
사용자(가디언, 케어기버, 시니어) 관련 스키마들
"""

from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from uuid import UUID

from .base import BaseResponse


class GuardianInfo(BaseModel):
    """가디언 정보 스키마"""
    id: UUID = Field(description="가디언 ID")
    full_name: str = Field(description="가디언 이름")
    email: Optional[str] = Field(None, description="이메일 주소")
    phone_number: Optional[str] = Field(None, description="전화번호")
    country: str = Field(description="거주 국가")
    city: Optional[str] = Field(None, description="거주 도시")
    language_preference: str = Field(default="ko", description="선호 언어")
    timezone: str = Field(default="Asia/Seoul", description="시간대")
    created_at: datetime = Field(description="가입일시")


class CaregiverInfo(BaseModel):
    """케어기버 정보 스키마"""
    id: UUID = Field(description="케어기버 ID")
    full_name: str = Field(description="케어기버 이름")
    email: Optional[str] = Field(None, description="이메일 주소")
    phone_number: Optional[str] = Field(None, description="전화번호")
    license_number: Optional[str] = Field(None, description="요양보호사 자격증 번호")
    experience_years: int = Field(default=0, description="경력 연수")
    languages: List[str] = Field(default_factory=list, description="구사 가능 언어")
    specialties: List[str] = Field(default_factory=list, description="전문 분야")
    profile_image_url: Optional[str] = Field(None, description="프로필 사진 URL")
    created_at: datetime = Field(description="가입일시")


class SeniorInfo(BaseModel):
    """시니어 정보 스키마"""
    id: UUID = Field(description="시니어 ID")
    full_name: str = Field(description="시니어 이름")
    birth_date: Optional[date] = Field(None, description="생년월일")
    age: Optional[int] = Field(None, description="나이")
    gender: Optional[str] = Field(None, description="성별")
    nationality: Optional[str] = Field(None, description="국적")
    emergency_contact_name: Optional[str] = Field(None, description="응급연락처 이름")
    emergency_contact_phone: Optional[str] = Field(None, description="응급연락처 전화번호")
    medical_conditions: List[str] = Field(default_factory=list, description="기존 질병")
    allergies: List[str] = Field(default_factory=list, description="알레르기")
    medications: List[str] = Field(default_factory=list, description="복용 약물")
    mobility_level: Optional[str] = Field(None, description="거동 능력")
    cognitive_level: Optional[str] = Field(None, description="인지 능력")
    preferred_language: str = Field(default="ko", description="선호 언어")
    dietary_restrictions: List[str] = Field(default_factory=list, description="식이 제한")
    cultural_preferences: Dict[str, Any] = Field(default_factory=dict, description="문화적 선호사항")
    profile_image_url: Optional[str] = Field(None, description="프로필 사진 URL")
    notes: Optional[str] = Field(None, description="특이사항")
    created_at: datetime = Field(description="생성일시")
    updated_at: datetime = Field(description="수정일시")


class UserResponse(BaseResponse):
    """사용자 정보 응답 스키마"""
    data: Dict[str, Any] = Field(description="사용자 데이터")
