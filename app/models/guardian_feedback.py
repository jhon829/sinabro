"""
GuardianFeedback (가디언 피드백) 모델
가디언이 AI 리포트나 케어 서비스에 대해 제공하는 피드백을 저장하는 모델
"""

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from ..database import Base


class GuardianFeedback(Base):
    """가디언 피드백 모델"""
    
    __tablename__ = "guardian_feedback"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    channel_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("channels.id", ondelete="CASCADE"), 
        nullable=False, 
        comment="채널 ID"
    )
    guardian_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("guardians.id"), 
        nullable=False, 
        comment="가디언 ID"
    )
    ai_report_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("ai_reports.id"), 
        nullable=True, 
        comment="관련 AI 리포트 ID"
    )
    feedback_type = Column(
        String(30), 
        nullable=False, 
        comment="피드백 유형 (request/compliment/concern/question)"
    )
    feedback_content = Column(Text, nullable=False, comment="피드백 내용")
    status = Column(
        String(20), 
        default="pending", 
        comment="처리 상태 (pending/reviewed/resolved)"
    )
    response_text = Column(Text, nullable=True, comment="관리자 응답")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="생성일시")
    
    # 제약조건
    __table_args__ = (
        CheckConstraint(
            "feedback_type IN ('request', 'compliment', 'concern', 'question')", 
            name="check_feedback_type"
        ),
        CheckConstraint(
            "status IN ('pending', 'reviewed', 'resolved')", 
            name="check_feedback_status"
        ),
    )
    
    # 관계 정의
    channel = relationship("Channel", back_populates="guardian_feedback")
    guardian = relationship("Guardian", back_populates="guardian_feedback")
    ai_report = relationship("AIReport", back_populates="guardian_feedback")
    
    def __repr__(self):
        return f"<GuardianFeedback(type='{self.feedback_type}', status='{self.status}')>"
    
    @property
    def is_pending(self):
        """대기 중인 피드백인지 확인"""
        return self.status == "pending"
    
    @property
    def is_resolved(self):
        """해결된 피드백인지 확인"""
        return self.status == "resolved"
    
    @property
    def has_response(self):
        """관리자 응답이 있는지 확인"""
        return self.response_text is not None and len(self.response_text.strip()) > 0
    
    def to_dict(self, include_relations=False):
        """딕셔너리로 변환"""
        result = {
            "id": str(self.id),
            "channel_id": str(self.channel_id),
            "guardian_id": str(self.guardian_id),
            "ai_report_id": str(self.ai_report_id) if self.ai_report_id else None,
            "feedback_type": self.feedback_type,
            "feedback_content": self.feedback_content,
            "status": self.status,
            "response_text": self.response_text,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
        
        if include_relations:
            result.update({
                "guardian": self.guardian.to_dict() if self.guardian else None,
                "ai_report": self.ai_report.to_dict() if self.ai_report else None,
                "is_pending": self.is_pending,
                "is_resolved": self.is_resolved,
                "has_response": self.has_response
            })
        
        return result
