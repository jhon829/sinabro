"""
AccessCode (접속 코드) 모델
해커톤용 접속 코드를 관리하는 모델
"""

from sqlalchemy import Column, String, DateTime, Boolean, CheckConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from ..database import Base


class AccessCode(Base):
    """접속 코드 모델"""
    
    __tablename__ = "access_codes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(20), unique=True, nullable=False, comment="접속 코드")
    user_type = Column(String(20), nullable=False, comment="사용자 타입")
    user_id = Column(UUID(as_uuid=True), nullable=False, comment="사용자 ID")
    channel_id = Column(UUID(as_uuid=True), ForeignKey("channels.id"), comment="연결된 채널 ID")
    is_used = Column(Boolean, default=False, comment="사용 여부")
    expires_at = Column(DateTime(timezone=True), comment="만료일시")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="생성일시")
    
    # 제약조건
    __table_args__ = (
        CheckConstraint("user_type IN ('guardian', 'caregiver')", name="check_user_type"),
    )
    
    # 관계 정의
    channel = relationship("Channel", back_populates="access_codes")
    
    def __repr__(self):
        return f"<AccessCode(code='{self.code}', type='{self.user_type}')>"
    
    @property
    def is_expired(self):
        """만료 여부 확인"""
        if not self.expires_at:
            return False
        from datetime import datetime
        return datetime.now(self.expires_at.tzinfo) > self.expires_at
    
    @property
    def is_valid(self):
        """유효성 검사"""
        return not self.is_expired
    
    def mark_as_used(self):
        """사용됨으로 표시"""
        self.is_used = True
    
    def to_dict(self):
        """딕셔너리로 변환"""
        return {
            "id": str(self.id),
            "code": self.code,
            "user_type": self.user_type,
            "user_id": str(self.user_id),
            "channel_id": str(self.channel_id) if self.channel_id else None,
            "is_used": self.is_used,
            "is_expired": self.is_expired,
            "is_valid": self.is_valid,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
