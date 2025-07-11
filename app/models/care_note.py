"""
CareNote (돌봄노트) 모델
케어기버가 작성하는 상세한 돌봄 기록 모델
"""

from sqlalchemy import Column, String, Date, DateTime, Text, CheckConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from ..database import Base


class CareNote(Base):
    """돌봄노트 모델"""
    
    __tablename__ = "care_notes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    channel_id = Column(UUID(as_uuid=True), ForeignKey("channels.id", ondelete="CASCADE"), nullable=False, comment="채널 ID")
    caregiver_id = Column(UUID(as_uuid=True), ForeignKey("caregivers.id"), nullable=False, comment="케어기버 ID")
    note_type = Column(String(30), nullable=False, comment="노트 타입")
    content = Column(Text, nullable=False, comment="노트 내용")
    related_date = Column(Date, nullable=False, server_default=func.current_date(), comment="관련 날짜")
    tags = Column(JSONB, default=list, comment="태그들")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="생성일시")
    
    # 제약조건
    __table_args__ = (
        CheckConstraint("note_type IN ('daily_summary', 'guardian_feedback', 'special_note')", name="check_note_type"),
    )
    
    # 관계 정의
    channel = relationship("Channel", back_populates="care_notes")
    caregiver = relationship("Caregiver", back_populates="care_notes")
    
    def __repr__(self):
        return f"<CareNote(type='{self.note_type}', date='{self.related_date}')>"
    
    @property
    def word_count(self):
        """글자 수"""
        return len(self.content) if self.content else 0
    
    @property
    def is_recent(self):
        """최근 기록 여부 (7일 이내)"""
        from datetime import date, timedelta
        if not self.related_date:
            return False
        return (date.today() - self.related_date).days <= 7
    
    def add_tag(self, tag):
        """태그 추가"""
        if not self.tags:
            self.tags = []
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag):
        """태그 제거"""
        if self.tags and tag in self.tags:
            self.tags.remove(tag)
    
    def to_dict(self, include_relations=False):
        """딕셔너리로 변환"""
        result = {
            "id": str(self.id),
            "channel_id": str(self.channel_id),
            "caregiver_id": str(self.caregiver_id),
            "note_type": self.note_type,
            "content": self.content,
            "word_count": self.word_count,
            "related_date": self.related_date.isoformat() if self.related_date else None,
            "tags": self.tags if self.tags else [],
            "is_recent": self.is_recent,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
        
        if include_relations:
            result.update({
                "caregiver": self.caregiver.to_dict() if self.caregiver else None
            })
        
        return result
