"""
Guardian (가디언) 모델
해외 거주 자녀를 나타내는 모델
"""

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from ..database import Base


class Guardian(Base):
    """가디언 (해외 거주 자녀) 모델"""
    
    __tablename__ = "guardians"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String(100), nullable=False, comment="가디언 이름")
    email = Column(String(255), comment="이메일 주소")
    phone_number = Column(String(20), comment="전화번호")
    country = Column(String(50), nullable=False, comment="거주 국가")
    city = Column(String(100), comment="거주 도시")
    language_preference = Column(String(10), default="ko", comment="선호 언어")
    timezone = Column(String(50), default="Asia/Seoul", comment="시간대")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="생성일시")
    
    # 관계 정의
    channels = relationship("Channel", back_populates="guardian", cascade="all, delete-orphan")
    guardian_feedback = relationship("GuardianFeedback", back_populates="guardian", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Guardian(name='{self.full_name}', country='{self.country}')>"
    
    def to_dict(self):
        """딕셔너리로 변환"""
        return {
            "id": str(self.id),
            "full_name": self.full_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "country": self.country,
            "city": self.city,
            "language_preference": self.language_preference,
            "timezone": self.timezone,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
