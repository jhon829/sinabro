"""
DailyChecklist (일일 체크리스트) 모델
실제 체크리스트 기록을 관리하는 모델
"""

from sqlalchemy import Column, String, Date, DateTime, Text, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from ..database import Base


class DailyChecklist(Base):
    """일일 체크리스트 모델"""
    
    __tablename__ = "daily_checklists"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    channel_id = Column(UUID(as_uuid=True), ForeignKey("channels.id", ondelete="CASCADE"), nullable=False, comment="채널 ID")
    template_id = Column(UUID(as_uuid=True), ForeignKey("checklist_templates.id"), comment="템플릿 ID")
    checked_items = Column(JSONB, nullable=False, comment="체크된 항목들")
    additional_notes = Column(Text, comment="추가 메모")
    completion_rate = Column(Numeric(5, 2), default=0.00, comment="완료율")
    created_date = Column(Date, nullable=False, server_default=func.current_date(), comment="기록 날짜")
    created_by = Column(UUID(as_uuid=True), ForeignKey("caregivers.id"), comment="작성자 ID")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="생성일시")
    
    # 관계 정의
    channel = relationship("Channel", back_populates="daily_checklists")
    template = relationship("ChecklistTemplate", back_populates="daily_checklists")
    creator = relationship("Caregiver", back_populates="daily_checklists")
    
    def __repr__(self):
        return f"<DailyChecklist(date='{self.created_date}', completion={self.completion_rate}%)>"
    
    def calculate_completion_rate(self):
        """완료율 계산"""
        if not self.checked_items or not isinstance(self.checked_items, dict):
            return 0.0
        
        items = self.checked_items.get("items", [])
        if not items:
            return 0.0
        
        checked_count = sum(1 for item in items if item.get("checked", False))
        total_count = len(items)
        
        return round((checked_count / total_count) * 100, 2) if total_count > 0 else 0.0
    
    def update_completion_rate(self):
        """완료율 업데이트"""
        self.completion_rate = self.calculate_completion_rate()
    
    def get_checked_items(self):
        """체크된 항목 조회"""
        if not self.checked_items or not isinstance(self.checked_items, dict):
            return []
        return [item for item in self.checked_items.get("items", []) if item.get("checked", False)]
    
    def get_unchecked_items(self):
        """체크되지 않은 항목 조회"""
        if not self.checked_items or not isinstance(self.checked_items, dict):
            return []
        return [item for item in self.checked_items.get("items", []) if not item.get("checked", False)]
    
    def to_dict(self, include_relations=False):
        """딕셔너리로 변환"""
        result = {
            "id": str(self.id),
            "channel_id": str(self.channel_id),
            "template_id": str(self.template_id) if self.template_id else None,
            "checked_items": self.checked_items if self.checked_items else {"items": []},
            "additional_notes": self.additional_notes,
            "completion_rate": float(self.completion_rate) if self.completion_rate else 0.0,
            "checked_count": len(self.get_checked_items()),
            "total_count": len(self.checked_items.get("items", [])) if self.checked_items else 0,
            "created_date": self.created_date.isoformat() if self.created_date else None,
            "created_by": str(self.created_by) if self.created_by else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
        
        if include_relations:
            result.update({
                "template": self.template.to_dict() if self.template else None,
                "creator": self.creator.to_dict() if self.creator else None
            })
        
        return result
