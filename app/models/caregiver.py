"""
Caregiver (케어기버) 모델
간병인을 나타내는 모델
"""

from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from ..database import Base


class Caregiver(Base):
    """케어기버 (간병인) 모델"""
    
    __tablename__ = "caregivers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String(100), nullable=False, comment="케어기버 이름")
    email = Column(String(255), comment="이메일 주소")
    phone_number = Column(String(20), comment="전화번호")
    license_number = Column(String(50), comment="요양보호사 자격증 번호")
    experience_years = Column(Integer, default=0, comment="경력 연수")
    languages = Column(JSONB, default=list, comment="구사 가능 언어")
    specialties = Column(JSONB, default=list, comment="전문 분야")
    profile_image_url = Column(Text, comment="프로필 사진 URL")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="생성일시")
    
    # 관계 정의
    channels = relationship("Channel", back_populates="caregiver", cascade="all, delete-orphan")
    care_notes = relationship("CareNote", back_populates="caregiver", cascade="all, delete-orphan")
    photos = relationship("Photo", back_populates="caregiver", cascade="all, delete-orphan")
    daily_checklists = relationship("DailyChecklist", back_populates="caregiver", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Caregiver(name='{self.full_name}', experience={self.experience_years}년)>"
    
    def to_dict(self):
        """딕셔너리로 변환"""
        return {
            "id": str(self.id),
            "full_name": self.full_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "license_number": self.license_number,
            "experience_years": self.experience_years,
            "languages": self.languages if self.languages else [],
            "specialties": self.specialties if self.specialties else [],
            "profile_image_url": self.profile_image_url,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    @property
    def experience_level(self):
        """경력 수준 반환"""
        if self.experience_years < 1:
            return "신입"
        elif self.experience_years < 3:
            return "초급"
        elif self.experience_years < 7:
            return "중급"
        else:
            return "고급"
