"""
Sinabro 데이터베이스 모델
SQLAlchemy 모델 정의
"""

# 기본 사용자 모델
from .guardian import Guardian
from .caregiver import Caregiver  
from .senior import Senior

# 접속 및 채널 모델
from .access_code import AccessCode
from .channel import Channel

# 체크리스트 모델
from .checklist_template import ChecklistTemplate
from .daily_checklist import DailyChecklist

# 케어 관련 모델
from .care_note import CareNote
from .photo import Photo

# 질문 및 피드백 모델
from .admin_question import AdminQuestion
from .question_response import QuestionResponse
from .guardian_feedback import GuardianFeedback

# AI 관련 모델
from .ai_report import AIReport

__all__ = [
    # 기본 사용자 모델
    "Guardian",
    "Caregiver", 
    "Senior",
    
    # 접속 및 채널 모델
    "AccessCode",
    "Channel",
    
    # 체크리스트 모델
    "ChecklistTemplate",
    "DailyChecklist", 
    
    # 케어 관련 모델
    "CareNote",
    "Photo",
    
    # 질문 및 피드백 모델
    "AdminQuestion",
    "QuestionResponse",
    "GuardianFeedback",
    
    # AI 관련 모델
    "AIReport"
]
