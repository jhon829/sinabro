"""
Photo (사진) 모델
케어기버가 업로드하는 사진을 관리하는 모델
"""

from sqlalchemy import Column, String, Date, DateTime, Text, CheckConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import os

from ..database import Base


class Photo(Base):
    """사진 모델"""
    
    __tablename__ = "photos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    channel_id = Column(UUID(as_uuid=True), ForeignKey("channels.id", ondelete="CASCADE"), nullable=False, comment="채널 ID")
    caregiver_id = Column(UUID(as_uuid=True), ForeignKey("caregivers.id"), nullable=False, comment="케어기버 ID")
    file_url = Column(Text, nullable=False, comment="파일 URL")
    file_name = Column(String(255), comment="원본 파일명")
    description = Column(Text, comment="사진 설명")
    photo_type = Column(String(30), comment="사진 타입")
    taken_date = Column(Date, nullable=False, server_default=func.current_date(), comment="촬영 날짜")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="생성일시")
    
    # 제약조건
    __table_args__ = (
        CheckConstraint("photo_type IN ('activity', 'meal', 'medication', 'family_moment')", name="check_photo_type"),
    )
    
    # 관계 정의
    channel = relationship("Channel", back_populates="photos")
    caregiver = relationship("Caregiver", back_populates="photos")
    
    def __repr__(self):
        return f"<Photo(type='{self.photo_type}', taken='{self.taken_date}')>"
    
    @property
    def file_extension(self):
        """파일 확장자"""
        if not self.file_name:
            return None
        return os.path.splitext(self.file_name)[1].lower()
    
    @property
    def is_image(self):
        """이미지 파일 여부"""
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        return self.file_extension in image_extensions
    
    @property
    def is_recent(self):
        """최근 촬영 여부 (7일 이내)"""
        from datetime import date, timedelta
        if not self.taken_date:
            return False
        return (date.today() - self.taken_date).days <= 7
    
    def get_display_name(self):
        """표시용 파일명"""
        if self.description:
            return self.description
        return self.file_name or f"사진_{self.taken_date}"
    
    def to_dict(self, include_relations=False):
        """딕셔너리로 변환"""
        result = {
            "id": str(self.id),
            "channel_id": str(self.channel_id),
            "caregiver_id": str(self.caregiver_id),
            "file_url": self.file_url,
            "file_name": self.file_name,
            "file_extension": self.file_extension,
            "description": self.description,
            "photo_type": self.photo_type,
            "display_name": self.get_display_name(),
            "is_image": self.is_image,
            "is_recent": self.is_recent,
            "taken_date": self.taken_date.isoformat() if self.taken_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
        
        if include_relations:
            result.update({
                "caregiver": self.caregiver.to_dict() if self.caregiver else None
            })
        
        return result
