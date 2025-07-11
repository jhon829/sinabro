"""
Channel (채널) 모델
가디언-케어기버-시니어를 연결하는 케어 채널 모델
"""

from sqlalchemy import Column, String, Date, DateTime, CheckConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from ..database import Base


class Channel(Base):
    """케어 채널 모델"""
    
    __tablename__ = "channels"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    channel_name = Column(String(100), nullable=False, comment="채널 이름")
    guardian_id = Column(UUID(as_uuid=True), ForeignKey("guardians.id", ondelete="CASCADE"), nullable=False, comment="가디언 ID")
    caregiver_id = Column(UUID(as_uuid=True), ForeignKey("caregivers.id", ondelete="CASCADE"), nullable=False, comment="케어기버 ID")
    senior_id = Column(UUID(as_uuid=True), ForeignKey("seniors.id", ondelete="CASCADE"), nullable=False, comment="시니어 ID")
    status = Column(String(20), default="active", comment="채널 상태")
    start_date = Column(Date, nullable=False, server_default=func.current_date(), comment="케어 시작일")
    end_date = Column(Date, comment="케어 종료일")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="생성일시")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="수정일시")
    
    # 제약조건
    __table_args__ = (
        CheckConstraint("status IN ('active', 'inactive', 'completed')", name="check_channel_status"),
    )
    
    # 관계 정의
    guardian = relationship("Guardian", back_populates="channels")
    caregiver = relationship("Caregiver", back_populates="channels")
    senior = relationship("Senior", back_populates="channels")
    
    # 역참조 관계들
    daily_checklists = relationship("DailyChecklist", back_populates="channel", cascade="all, delete-orphan")
    care_notes = relationship("CareNote", back_populates="channel", cascade="all, delete-orphan")
    photos = relationship("Photo", back_populates="channel", cascade="all, delete-orphan")
    ai_reports = relationship("AIReport", back_populates="channel", cascade="all, delete-orphan")
    guardian_feedback = relationship("GuardianFeedback", back_populates="channel", cascade="all, delete-orphan")
    question_responses = relationship("QuestionResponse", back_populates="channel", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Channel(name='{self.channel_name}', status='{self.status}')>"
    
    @property
    def is_active(self):
        """활성 상태 여부"""
        return self.status == "active"
    
    def to_dict(self, include_relations=False):
        """딕셔너리로 변환"""
        result = {
            "id": str(self.id),
            "channel_name": self.channel_name,
            "guardian_id": str(self.guardian_id),
            "caregiver_id": str(self.caregiver_id),
            "senior_id": str(self.senior_id),
            "status": self.status,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_relations:
            result.update({
                "guardian": self.guardian.to_dict() if self.guardian else None,
                "caregiver": self.caregiver.to_dict() if self.caregiver else None,
                "senior": self.senior.to_dict() if self.senior else None
            })
        
        return result
