"""
Checklist API Router for Sinabro
체크리스트 템플릿 관련 API 엔드포인트
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from database import get_db
from services import ChecklistService
from schemas import ChecklistTemplateListResponse, ChecklistTemplateResponse

router = APIRouter(prefix="/api/v1/checklists", tags=["체크리스트"])


@router.get("/templates",
    response_model=ChecklistTemplateListResponse,
    summary="체크리스트 템플릿 목록 조회",
    description="활성화된 체크리스트 템플릿 목록을 조회합니다. 카테고리별 필터링이 가능합니다.")
async def get_checklist_templates(
    category: Optional[str] = Query(None, description="카테고리 필터 (health_management, daily_care 등)"),
    is_active: bool = Query(True, description="활성 상태 필터"),
    db: Session = Depends(get_db)
):
    """
    체크리스트 템플릿 목록 조회
    
    **쿼리 파라미터:**
    - `category`: 카테고리 필터 (선택사항)
      - `health_management`: 건강관리
      - `daily_care`: 일상생활관리
      - 기타 카테고리들
    - `is_active`: 활성 상태 필터 (기본값: true)
    
    **사용 예시:**
    - 모든 템플릿: `/api/v1/checklists/templates`
    - 건강관리 템플릿: `/api/v1/checklists/templates?category=health_management`
    - 비활성 템플릿 포함: `/api/v1/checklists/templates?is_active=false`
    
    **응답 정보:**
    - 템플릿 기본 정보 (이름, 카테고리)
    - 체크리스트 아이템 목록
    - 각 아이템의 필수 여부 및 유형
    """
    try:
        # 체크리스트 서비스 인스턴스 생성
        checklist_service = ChecklistService(db)
        
        # 템플릿 목록 조회
        result = checklist_service.get_all_templates(category=category, is_active=is_active)
        
        # 에러 응답 처리
        if not result.get("success", True):
            message = result.get("message", "알 수 없는 오류가 발생했습니다.")
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


@router.get("/templates/{template_id}",
    response_model=ChecklistTemplateResponse,
    summary="체크리스트 템플릿 상세 조회",
    description="템플릿 ID로 특정 체크리스트 템플릿의 상세 정보를 조회합니다.")
async def get_checklist_template_by_id(
    template_id: UUID,
    db: Session = Depends(get_db)
):
    """
    체크리스트 템플릿 상세 조회
    
    **경로 파라미터:**
    - `template_id`: 조회할 템플릿의 UUID
    
    **사용 예시:**
    - `/api/v1/checklists/templates/550e8400-e29b-41d4-a716-446655440100`
    
    **응답 정보:**
    - 템플릿 전체 정보
    - 상세 체크리스트 아이템들
    - 각 아이템의 유형별 분류
    """
    try:
        # 체크리스트 서비스 인스턴스 생성
        checklist_service = ChecklistService(db)
        
        # 템플릿 상세 정보 조회
        result = checklist_service.get_template_by_id(template_id)
        
        # 에러 응답 처리
        if not result.get("success", True):
            error_code = result.get("error_code")
            message = result.get("message", "알 수 없는 오류가 발생했습니다.")
            
            if error_code == "TEMPLATE_NOT_FOUND":
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


@router.get("/templates/category/{category}",
    response_model=ChecklistTemplateListResponse,
    summary="카테고리별 체크리스트 템플릿 조회",
    description="특정 카테고리의 체크리스트 템플릿들을 조회합니다.")
async def get_templates_by_category(
    category: str,
    db: Session = Depends(get_db)
):
    """
    카테고리별 체크리스트 템플릿 조회
    
    **경로 파라미터:**
    - `category`: 카테고리명
      - `health_management`: 건강관리
      - `daily_care`: 일상생활관리
    
    **사용 예시:**
    - `/api/v1/checklists/templates/category/health_management`
    - `/api/v1/checklists/templates/category/daily_care`
    """
    try:
        # 체크리스트 서비스 인스턴스 생성
        checklist_service = ChecklistService(db)
        
        # 카테고리별 템플릿 조회
        result = checklist_service.get_templates_by_category(category)
        
        # 에러 응답 처리
        if not result.get("success", True):
            message = result.get("message", "알 수 없는 오류가 발생했습니다.")
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
