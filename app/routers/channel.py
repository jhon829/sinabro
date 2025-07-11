"""
Channel API Router for Sinabro
채널 관련 API 엔드포인트
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from database import get_db
from services import ChannelService
from schemas import MyChannelsResponse, ChannelResponse

router = APIRouter(prefix="/api/v1/channels", tags=["채널"])


@router.get("/my",
    response_model=MyChannelsResponse,
    summary="내 채널 목록 조회",
    description="사용자의 채널 목록을 조회합니다. 가디언 또는 케어기버별로 필터링됩니다.")
async def get_my_channels(
    user_id: UUID = Query(..., description="사용자 ID"),
    user_type: str = Query(..., description="사용자 유형 (guardian 또는 caregiver)"),
    db: Session = Depends(get_db)
):
    """
    내 채널 목록 조회
    
    **쿼리 파라미터:**
    - `user_id`: 사용자의 UUID
    - `user_type`: 'guardian' 또는 'caregiver'
    
    **사용 예시:**
    - 가디언: `/api/v1/channels/my?user_id=550e8400-e29b-41d4-a716-446655440001&user_type=guardian`
    - 케어기버: `/api/v1/channels/my?user_id=550e8400-e29b-41d4-a716-446655440004&user_type=caregiver`
    
    **응답 정보:**
    - 채널 기본 정보
    - 연결된 가디언, 케어기버, 시니어 정보
    - 채널 상태 및 기간
    """
    try:
        # 사용자 유형 검증
        if user_type not in ["guardian", "caregiver"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user_type은 'guardian' 또는 'caregiver'여야 합니다."
            )
        
        # 채널 서비스 인스턴스 생성
        channel_service = ChannelService(db)
        
        # 내 채널 목록 조회
        result = channel_service.get_my_channels(user_id, user_type)
        
        # 에러 응답 처리
        if not result.get("success", True):
            error_code = result.get("error_code")
            message = result.get("message", "알 수 없는 오류가 발생했습니다.")
            
            if error_code == "INVALID_USER_TYPE":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=message
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=message
                )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="서버 내부 오류가 발생했습니다."
        )


@router.get("/{channel_id}",
    response_model=ChannelResponse,
    summary="채널 상세 정보 조회",
    description="채널 ID로 특정 채널의 상세 정보를 조회합니다.")
async def get_channel_by_id(
    channel_id: UUID,
    db: Session = Depends(get_db)
):
    """
    채널 상세 정보 조회
    
    **경로 파라미터:**
    - `channel_id`: 조회할 채널의 UUID
    
    **사용 예시:**
    - `/api/v1/channels/550e8400-e29b-41d4-a716-446655440010`
    
    **응답 정보:**
    - 채널 전체 정보
    - 가디언, 케어기버, 시니어 상세 정보
    - 채널 상태 및 운영 기간
    """
    try:
        # 채널 서비스 인스턴스 생성
        channel_service = ChannelService(db)
        
        # 채널 상세 정보 조회
        result = channel_service.get_channel_by_id(channel_id)
        
        # 에러 응답 처리
        if not result.get("success", True):
            error_code = result.get("error_code")
            message = result.get("message", "알 수 없는 오류가 발생했습니다.")
            
            if error_code == "CHANNEL_NOT_FOUND":
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=message
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=message
                )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="서버 내부 오류가 발생했습니다."
        )
