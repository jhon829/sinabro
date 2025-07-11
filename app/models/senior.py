"""
Senior (시니어) 모델
돌봄 대상 어르신을 나타내는 모델
"""

from sqlalchemy import Column, String, Date, DateTime, Text, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from ..database import Base


class Senior(Base):
    """시니어 (돌봄 대상) 모델"""
    
    __tablename__ = "seniors"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String(100), nullable=False, comment="시니어 이름")
    birth_date = Column(Date, comment="생년월일")
    gender = Column(String(10), comment="성별")
    nationality = Column(String(50), comment="국적")
    emergency_contact_name = Column(String(100), comment="응급연락처 이름")
    emergency_contact_phone = Column(String(20), comment="응급연락처 전화번호")
    
    # 건강 정보
    medical_conditions = Column(JSONB, default=list, comment="기존 질병")
    allergies = Column(JSONB, default=list, comment="알레르기")
    medications = Column(JSONB, default=list, comment="복용 약물")
    mobility_level = Column(String(20), comment="거동 능력")
    cognitive_level = Column(String(20), comment="인지 능력")
    
    # 문화적 선호사항
    preferred_language = Column(String(10), default="ko", comment="선호 언어")
    dietary_restrictions = Column(JSONB, default=list, comment="식이 제한")
    cultural_preferences = Column(JSONB, default=dict, comment="문화적 선호사항")
    
    # 기타 정보
    profile_image_url = Column(Text, comment="프로필 사진 URL")
    notes = Column(Text, comment="특이사항")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="생성일시")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="수정일시")
    
    # 관계 정의
    channels = relationship("Channel", back_populates="senior", cascade="all, delete-orphan")
    
    # 제약조건
    __table_args__ = (
        CheckConstraint("gender IN ('male', 'female')", name="check_gender"),
        CheckConstraint("mobility_level IN ('independent', 'assisted', 'wheelchair')", name="check_mobility"),
        CheckConstraint("cognitive_level IN ('normal', 'mild_impairment', 'severe_impairment')", name="check_cognitive"),
    )
    
    def __repr__(self):
        return f"<Senior(name='{self.full_name}', age={self.age}세)>"
    
    @property
    def age(self):
        """나이 계산"""
        if not self.birth_date:
            return None
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
    
    def to_dict(self):
        """딕셔너리로 변환"""
        return {
            "id": str(self.id),
            "full_name": self.full_name,
            "birth_date": self.birth_date.isoformat() if self.birth_date else None,
            "age": self.age,
            "gender": self.gender,
            "nationality": self.nationality,
            "emergency_contact_name": self.emergency_contact_name,
            "emergency_contact_phone": self.emergency_contact_phone,
            "medical_conditions": self.medical_conditions if self.medical_conditions else [],
            "allergies": self.allergies if self.allergies else [],
            "medications": self.medications if self.medications else [],
            "mobility_level": self.mobility_level,
            "cognitive_level": self.cognitive_level,
            "preferred_language": self.preferred_language,
            "dietary_restrictions": self.dietary_restrictions if self.dietary_restrictions else [],
            "cultural_preferences": self.cultural_preferences if self.cultural_preferences else {},
            "profile_image_url": self.profile_image_url,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
