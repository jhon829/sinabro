"""
AIReport (AI 리포트) 모델
AI가 생성한 일일 케어 리포트를 저장하는 모델
"""

from sqlalchemy import Column, String, Text, Date, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.types import DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from ..database import Base


class AIReport(Base):
    """AI 리포트 모델"""
    
    __tablename__ = "ai_reports"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    channel_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("channels.id", ondelete="CASCADE"), 
        nullable=False, 
        comment="채널 ID"
    )
    report_date = Column(Date, nullable=False, server_default=func.current_date(), comment="리포트 날짜")
    
    # 데이터 소스 참조 (UUID 배열)
    checklist_ids = Column(ARRAY(UUID), default=[], comment="참조된 체크리스트 ID들")
    care_note_ids = Column(ARRAY(UUID), default=[], comment="참조된 돌봄노트 ID들")
    photo_ids = Column(ARRAY(UUID), default=[], comment="참조된 사진 ID들")
    question_response_ids = Column(ARRAY(UUID), default=[], comment="참조된 질문답변 ID들")
    
    # AI 생성 내용
    summary_text = Column(Text, nullable=False, comment="AI 생성 요약")
    family_comment = Column(Text, nullable=False, comment="가족을 위한 코멘트")
    mood_analysis = Column(JSONB, default={}, comment="기분 분석 결과")
    health_status = Column(JSONB, default={}, comment="건강 상태 평가")
    recommendations = Column(JSONB, default=[], comment="AI 추천사항")
    
    # 번역된 버전들
    translations = Column(JSONB, default={}, comment="다국어 번역 버전")
    
    # 메타데이터
    generation_model = Column(String(50), default="gpt-4", comment="생성에 사용된 AI 모델")
    generation_time_ms = Column(Integer, default=0, comment="생성 소요 시간 (밀리초)")
    confidence_score = Column(DECIMAL(3, 2), default=0.00, comment="AI 신뢰도 점수")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="생성일시")
    
    # 관계 정의
    channel = relationship("Channel", back_populates="ai_reports")
    guardian_feedback = relationship(
        "GuardianFeedback", 
        back_populates="ai_report", 
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<AIReport(date='{self.report_date}', model='{self.generation_model}')>"
    
    @property
    def has_high_confidence(self):
        """높은 신뢰도 점수인지 확인 (0.8 이상)"""
        return self.confidence_score and self.confidence_score >= 0.8
    
    @property
    def data_source_count(self):
        """참조된 데이터 소스의 총 개수"""
        return (
            len(self.checklist_ids or []) +
            len(self.care_note_ids or []) +
            len(self.photo_ids or []) +
            len(self.question_response_ids or [])
        )
    
    def to_dict(self, include_relations=False):
        """딕셔너리로 변환"""
        result = {
            "id": str(self.id),
            "channel_id": str(self.channel_id),
            "report_date": self.report_date.isoformat() if self.report_date else None,
            "checklist_ids": [str(uid) for uid in (self.checklist_ids or [])],
            "care_note_ids": [str(uid) for uid in (self.care_note_ids or [])],
            "photo_ids": [str(uid) for uid in (self.photo_ids or [])],
            "question_response_ids": [str(uid) for uid in (self.question_response_ids or [])],
            "summary_text": self.summary_text,
            "family_comment": self.family_comment,
            "mood_analysis": self.mood_analysis,
            "health_status": self.health_status,
            "recommendations": self.recommendations,
            "translations": self.translations,
            "generation_model": self.generation_model,
            "generation_time_ms": self.generation_time_ms,
            "confidence_score": float(self.confidence_score) if self.confidence_score else 0.0,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
        
        if include_relations:
            result.update({
                "data_source_count": self.data_source_count,
                "has_high_confidence": self.has_high_confidence
            })
        
        return result
