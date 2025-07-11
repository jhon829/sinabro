"""
ChecklistTemplate (체크리스트 템플릿) 모델
표준 체크리스트 템플릿을 관리하는 모델
"""

from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from ..database import Base


class ChecklistTemplate(Base):
    """체크리스트 템플릿 모델"""
    
    __tablename__ = "checklist_templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="템플릿 이름")
    category = Column(String(50), nullable=False, comment="카테고리")
    items = Column(JSONB, nullable=False, comment="체크리스트 항목들")
    is_default = Column(Boolean, default=True, comment="기본 템플릿 여부")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="생성일시")
    
    # 역참조 관계
    daily_checklists = relationship("DailyChecklist", back_populates="template")
    
    def __repr__(self):
        return f"<ChecklistTemplate(name='{self.name}', category='{self.category}')>"
    
    @property
    def item_count(self):
        """항목 개수"""
        if not self.items or not isinstance(self.items, dict):
            return 0
        return len(self.items.get("items", []))
    
    def get_required_items(self):
        """필수 항목 조회"""
        if not self.items or not isinstance(self.items, dict):
            return []
        return [item for item in self.items.get("items", []) if item.get("required", False)]
    
    def get_optional_items(self):
        """선택 항목 조회"""
        if not self.items or not isinstance(self.items, dict):
            return []
        return [item for item in self.items.get("items", []) if not item.get("required", False)]
    
    def to_dict(self):
        """딕셔너리로 변환"""
        return {
            "id": str(self.id),
            "name": self.name,
            "category": self.category,
            "items": self.items if self.items else {"items": []},
            "item_count": self.item_count,
            "required_items_count": len(self.get_required_items()),
            "optional_items_count": len(self.get_optional_items()),
            "is_default": self.is_default,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
