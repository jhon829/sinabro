"""
AdminQuestion (관리자 질문) 모델
시스템에서 케어기버나 가디언에게 하는 질문을 관리하는 모델
"""

from sqlalchemy import Column, String, Boolean, DateTime, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from ..database import Base


class AdminQuestion(Base):
    """관리자 질문 모델"""
    
    __tablename__ = "admin_questions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_text = Column(String, nullable=False, comment="질문 내용")
    question_type = Column(
        String(30), 
        nullable=False, 
        comment="질문 유형 (daily/weekly/emergency/custom)"
    )
    target_audience = Column(
        String(20), 
        nullable=False, 
        comment="대상 사용자 (caregiver/guardian/both)"
    )
    is_active = Column(Boolean, default=True, comment="활성 상태")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="생성일시")
    
    # 제약조건
    __table_args__ = (
        CheckConstraint(
            "question_type IN ('daily', 'weekly', 'emergency', 'custom')", 
            name="check_question_type"
        ),
        CheckConstraint(
            "target_audience IN ('caregiver', 'guardian', 'both')", 
            name="check_target_audience"
        ),
    )
    
    # 관계 정의
    question_responses = relationship(
        "QuestionResponse", 
        back_populates="admin_question", 
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<AdminQuestion(type='{self.question_type}', audience='{self.target_audience}')>"
    
    @property
    def is_for_caregiver(self):
        """케어기버 대상 질문인지 확인"""
        return self.target_audience in ['caregiver', 'both']
    
    @property
    def is_for_guardian(self):
        """가디언 대상 질문인지 확인"""
        return self.target_audience in ['guardian', 'both']
    
    def to_dict(self):
        """딕셔너리로 변환"""
        return {
            "id": str(self.id),
            "question_text": self.question_text,
            "question_type": self.question_type,
            "target_audience": self.target_audience,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
