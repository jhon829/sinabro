"""
Sinabro API Schemas
Pydantic 스키마 정의
"""

# 기본 스키마
from .base import (
    BaseResponse,
    ErrorResponse,
    PaginationInfo,
    PaginatedResponse
)

# 사용자 관련 스키마
from .user import (
    GuardianInfo,
    CaregiverInfo,
    SeniorInfo,
    UserResponse
)

# 접속 코드 관련 스키마
from .access_code import (
    AccessCodeInfo,
    AccessCodeResponse
)

# 채널 관련 스키마
from .channel import (
    ChannelInfo,
    ChannelDetailInfo,
    ChannelResponse,
    ChannelListResponse,
    MyChannelsResponse
)

# 체크리스트 관련 스키마
from .checklist import (
    ChecklistItem,
    ChecklistTemplateInfo,
    ChecklistTemplateResponse,
    ChecklistTemplateListResponse
)

__all__ = [
    # 기본 스키마
    "BaseResponse",
    "ErrorResponse", 
    "PaginationInfo",
    "PaginatedResponse",
    
    # 사용자 관련 스키마
    "GuardianInfo",
    "CaregiverInfo",
    "SeniorInfo",
    "UserResponse",
    
    # 접속 코드 관련 스키마
    "AccessCodeInfo",
    "AccessCodeResponse",
    
    # 채널 관련 스키마
    "ChannelInfo",
    "ChannelDetailInfo",
    "ChannelResponse",
    "ChannelListResponse",
    "MyChannelsResponse",
    
    # 체크리스트 관련 스키마
    "ChecklistItem",
    "ChecklistTemplateInfo",
    "ChecklistTemplateResponse",
    "ChecklistTemplateListResponse"
]
