"""
QuestionResponse (질문 답변) 모델
관리자 질문에 대한 케어기버나 가디언의 답변을 저장하는 모델
"""

from sqlalchemy import Column, String, Text, Date, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from ..database import Base


class QuestionResponse(Base):
    """질문 답변 모델"""
    
    __tablename__ = "question_responses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    channel_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("channels.id", ondelete="CASCADE"), 
        nullable=False, 
        comment="채널 ID"
    )
    question_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("admin_questions.id"), 
        nullable=False, 
        comment="질문 ID"
    )
    responder_id = Column(UUID(as_uuid=True), nullable=False, comment="응답자 ID")
    responder_type = Column(
        String(20), 
        nullable=False, 
        comment="응답자 유형 (caregiver/guardian)"
    )
    response_text = Column(Text, nullable=False, comment="답변 내용")
    response_date = Column(Date, nullable=False, server_default=func.current_date(), comment="답변 날짜")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="생성일시")
    
    # 제약조건
    __table_args__ = (
        CheckConstraint(
            "responder_type IN ('caregiver', 'guardian')", 
            name="check_responder_type"
        ),
    )
    
    # 관계 정의
    channel = relationship("Channel", back_populates="question_responses")
    admin_question = relationship("AdminQuestion", back_populates="question_responses")
    
    def __repr__(self):
        return f"<QuestionResponse(responder_type='{self.responder_type}', date='{self.response_date}')>"
    
    @property
    def is_caregiver_response(self):
        """케어기버의 답변인지 확인"""
        return self.responder_type == 'caregiver'
    
    @property
    def is_guardian_response(self):
        """가디언의 답변인지 확인"""
        return self.responder_type == 'guardian'
    
    def to_dict(self, include_relations=False):
        """딕셔너리로 변환"""
        result = {
            "id": str(self.id),
            "channel_id": str(self.channel_id),
            "question_id": str(self.question_id),
            "responder_id": str(self.responder_id),
            "responder_type": self.responder_type,
            "response_text": self.response_text,
            "response_date": self.response_date.isoformat() if self.response_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
        
        if include_relations:
            result.update({
                "admin_question": self.admin_question.to_dict() if self.admin_question else None
            })
        
        return result
