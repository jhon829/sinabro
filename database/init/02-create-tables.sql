-- ==========================================
-- Sinabro 데이터베이스 초기화 스크립트 2/3
-- 모든 테이블 생성 (13개 테이블)
-- ==========================================

-- 접속 코드 테이블
CREATE TABLE IF NOT EXISTS access_codes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(20) UNIQUE NOT NULL,
    user_type VARCHAR(20) NOT NULL CHECK (user_type IN ('guardian', 'caregiver')),
    user_id UUID NOT NULL,
    channel_id UUID,
    is_used BOOLEAN DEFAULT FALSE,
    expires_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() + INTERVAL '1 year'),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 가디언 테이블 (해외 거주 자녀)
CREATE TABLE IF NOT EXISTS guardians (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(255),
    phone_number VARCHAR(20),
    country VARCHAR(50) NOT NULL,
    city VARCHAR(100),
    language_preference VARCHAR(10) DEFAULT 'ko',
    timezone VARCHAR(50) DEFAULT 'Asia/Seoul',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 케어기버 테이블 (간병인)
CREATE TABLE IF NOT EXISTS caregivers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(255),
    phone_number VARCHAR(20),
    license_number VARCHAR(50),
    experience_years INTEGER DEFAULT 0,
    languages JSONB DEFAULT '[]'::jsonb,
    specialties JSONB DEFAULT '[]'::jsonb,
    profile_image_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 시니어 테이블 (돌봄 대상)
CREATE TABLE IF NOT EXISTS seniors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name VARCHAR(100) NOT NULL,
    birth_date DATE,
    gender VARCHAR(10) CHECK (gender IN ('male', 'female')),
    nationality VARCHAR(50),
    emergency_contact_name VARCHAR(100),
    emergency_contact_phone VARCHAR(20),
    
    -- 건강 정보
    medical_conditions JSONB DEFAULT '[]'::jsonb,
    allergies JSONB DEFAULT '[]'::jsonb,
    medications JSONB DEFAULT '[]'::jsonb,
    mobility_level VARCHAR(20) CHECK (mobility_level IN ('independent', 'assisted', 'wheelchair')),
    cognitive_level VARCHAR(20) CHECK (cognitive_level IN ('normal', 'mild_impairment', 'severe_impairment')),
    
    -- 문화적 선호사항
    preferred_language VARCHAR(10) DEFAULT 'ko',
    dietary_restrictions JSONB DEFAULT '[]'::jsonb,
    cultural_preferences JSONB DEFAULT '{}'::jsonb,
    
    -- 기타 정보
    profile_image_url TEXT,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 채널 테이블 (가디언-케어기버-시니어 연결)
CREATE TABLE IF NOT EXISTS channels (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    channel_name VARCHAR(100) NOT NULL,
    guardian_id UUID NOT NULL,
    caregiver_id UUID NOT NULL,
    senior_id UUID NOT NULL,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'completed')),
    start_date DATE NOT NULL DEFAULT CURRENT_DATE,
    end_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 체크리스트 템플릿 테이블
CREATE TABLE IF NOT EXISTS checklist_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    items JSONB NOT NULL DEFAULT '{"items": []}'::jsonb,
    is_default BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 일일 체크리스트 테이블
CREATE TABLE IF NOT EXISTS daily_checklists (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    channel_id UUID NOT NULL,
    template_id UUID,
    checked_items JSONB NOT NULL DEFAULT '{"items": []}'::jsonb,
    additional_notes TEXT,
    completion_rate DECIMAL(5,2) DEFAULT 0.00,
    created_date DATE NOT NULL DEFAULT CURRENT_DATE,
    created_by UUID,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 돌봄노트 테이블
CREATE TABLE IF NOT EXISTS care_notes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    channel_id UUID NOT NULL,
    caregiver_id UUID NOT NULL,
    note_type VARCHAR(30) NOT NULL CHECK (note_type IN ('daily_summary', 'guardian_feedback', 'special_note')),
    content TEXT NOT NULL,
    related_date DATE NOT NULL DEFAULT CURRENT_DATE,
    tags JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 사진 테이블
CREATE TABLE IF NOT EXISTS photos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    channel_id UUID NOT NULL,
    caregiver_id UUID NOT NULL,
    file_url TEXT NOT NULL,
    file_name VARCHAR(255),
    description TEXT,
    photo_type VARCHAR(30) CHECK (photo_type IN ('activity', 'meal', 'medication', 'family_moment')),
    taken_date DATE NOT NULL DEFAULT CURRENT_DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 관리자 질문 테이블
CREATE TABLE IF NOT EXISTS admin_questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question_text TEXT NOT NULL,
    question_type VARCHAR(30) CHECK (question_type IN ('daily', 'weekly', 'emergency', 'custom')),
    target_audience VARCHAR(20) CHECK (target_audience IN ('caregiver', 'guardian', 'both')),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 질문 답변 테이블
CREATE TABLE IF NOT EXISTS question_responses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    channel_id UUID NOT NULL,
    question_id UUID NOT NULL,
    responder_id UUID NOT NULL,
    responder_type VARCHAR(20) NOT NULL CHECK (responder_type IN ('caregiver', 'guardian')),
    response_text TEXT NOT NULL,
    response_date DATE NOT NULL DEFAULT CURRENT_DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- AI 리포트 테이블
CREATE TABLE IF NOT EXISTS ai_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    channel_id UUID NOT NULL,
    report_date DATE NOT NULL DEFAULT CURRENT_DATE,
    
    -- 데이터 소스 참조
    checklist_ids UUID[] DEFAULT ARRAY[]::UUID[],
    care_note_ids UUID[] DEFAULT ARRAY[]::UUID[],
    photo_ids UUID[] DEFAULT ARRAY[]::UUID[],
    question_response_ids UUID[] DEFAULT ARRAY[]::UUID[],
    
    -- AI 생성 내용
    summary_text TEXT NOT NULL,
    family_comment TEXT NOT NULL,
    mood_analysis JSONB DEFAULT '{}'::jsonb,
    health_status JSONB DEFAULT '{}'::jsonb,
    recommendations JSONB DEFAULT '[]'::jsonb,
    
    -- 번역된 버전들
    translations JSONB DEFAULT '{}'::jsonb,
    
    -- 메타데이터
    generation_model VARCHAR(50) DEFAULT 'gpt-4',
    generation_time_ms INTEGER DEFAULT 0,
    confidence_score DECIMAL(3,2) DEFAULT 0.00,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 가디언 피드백 테이블
CREATE TABLE IF NOT EXISTS guardian_feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    channel_id UUID NOT NULL,
    guardian_id UUID NOT NULL,
    ai_report_id UUID,
    feedback_type VARCHAR(30) CHECK (feedback_type IN ('request', 'compliment', 'concern', 'question')),
    feedback_content TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'reviewed', 'resolved')),
    response_text TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==========================================
-- 외래키 제약조건 추가
-- ==========================================

-- 채널 관련 외래키
ALTER TABLE channels ADD CONSTRAINT fk_channels_guardian 
    FOREIGN KEY (guardian_id) REFERENCES guardians(id) ON DELETE CASCADE;
ALTER TABLE channels ADD CONSTRAINT fk_channels_caregiver 
    FOREIGN KEY (caregiver_id) REFERENCES caregivers(id) ON DELETE CASCADE;
ALTER TABLE channels ADD CONSTRAINT fk_channels_senior 
    FOREIGN KEY (senior_id) REFERENCES seniors(id) ON DELETE CASCADE;

-- 체크리스트 관련 외래키
ALTER TABLE daily_checklists ADD CONSTRAINT fk_checklists_channel 
    FOREIGN KEY (channel_id) REFERENCES channels(id) ON DELETE CASCADE;
ALTER TABLE daily_checklists ADD CONSTRAINT fk_checklists_template 
    FOREIGN KEY (template_id) REFERENCES checklist_templates(id);
ALTER TABLE daily_checklists ADD CONSTRAINT fk_checklists_creator 
    FOREIGN KEY (created_by) REFERENCES caregivers(id);

-- 돌봄노트 관련 외래키
ALTER TABLE care_notes ADD CONSTRAINT fk_notes_channel 
    FOREIGN KEY (channel_id) REFERENCES channels(id) ON DELETE CASCADE;
ALTER TABLE care_notes ADD CONSTRAINT fk_notes_caregiver 
    FOREIGN KEY (caregiver_id) REFERENCES caregivers(id);

-- 사진 관련 외래키
ALTER TABLE photos ADD CONSTRAINT fk_photos_channel 
    FOREIGN KEY (channel_id) REFERENCES channels(id) ON DELETE CASCADE;
ALTER TABLE photos ADD CONSTRAINT fk_photos_caregiver 
    FOREIGN KEY (caregiver_id) REFERENCES caregivers(id);

-- 질문 답변 관련 외래키
ALTER TABLE question_responses ADD CONSTRAINT fk_responses_channel 
    FOREIGN KEY (channel_id) REFERENCES channels(id) ON DELETE CASCADE;
ALTER TABLE question_responses ADD CONSTRAINT fk_responses_question 
    FOREIGN KEY (question_id) REFERENCES admin_questions(id);

-- AI 리포트 관련 외래키
ALTER TABLE ai_reports ADD CONSTRAINT fk_reports_channel 
    FOREIGN KEY (channel_id) REFERENCES channels(id) ON DELETE CASCADE;

-- 피드백 관련 외래키
ALTER TABLE guardian_feedback ADD CONSTRAINT fk_feedback_channel 
    FOREIGN KEY (channel_id) REFERENCES channels(id) ON DELETE CASCADE;
ALTER TABLE guardian_feedback ADD CONSTRAINT fk_feedback_guardian 
    FOREIGN KEY (guardian_id) REFERENCES guardians(id);
ALTER TABLE guardian_feedback ADD CONSTRAINT fk_feedback_report 
    FOREIGN KEY (ai_report_id) REFERENCES ai_reports(id);

-- ==========================================
-- 성능 최적화를 위한 인덱스 생성
-- ==========================================

-- 접속 코드 인덱스
CREATE INDEX IF NOT EXISTS idx_access_codes_code ON access_codes(code);
CREATE INDEX IF NOT EXISTS idx_access_codes_user ON access_codes(user_type, user_id);

-- 채널 관련 인덱스
CREATE INDEX IF NOT EXISTS idx_channels_guardian ON channels(guardian_id);
CREATE INDEX IF NOT EXISTS idx_channels_caregiver ON channels(caregiver_id);
CREATE INDEX IF NOT EXISTS idx_channels_senior ON channels(senior_id);
CREATE INDEX IF NOT EXISTS idx_channels_status ON channels(status);

-- 체크리스트 관련 인덱스
CREATE INDEX IF NOT EXISTS idx_checklists_channel_date ON daily_checklists(channel_id, created_date);
CREATE INDEX IF NOT EXISTS idx_checklists_template ON daily_checklists(template_id);

-- 돌봄노트 관련 인덱스
CREATE INDEX IF NOT EXISTS idx_notes_channel_date ON care_notes(channel_id, related_date);
CREATE INDEX IF NOT EXISTS idx_notes_caregiver ON care_notes(caregiver_id);

-- 사진 관련 인덱스
CREATE INDEX IF NOT EXISTS idx_photos_channel_date ON photos(channel_id, taken_date);
CREATE INDEX IF NOT EXISTS idx_photos_caregiver ON photos(caregiver_id);

-- AI 리포트 관련 인덱스
CREATE INDEX IF NOT EXISTS idx_reports_channel_date ON ai_reports(channel_id, report_date);

-- 피드백 관련 인덱스
CREATE INDEX IF NOT EXISTS idx_feedback_channel ON guardian_feedback(channel_id);
CREATE INDEX IF NOT EXISTS idx_feedback_guardian ON guardian_feedback(guardian_id);
CREATE INDEX IF NOT EXISTS idx_feedback_status ON guardian_feedback(status);

-- 유니크 제약조건 추가
CREATE UNIQUE INDEX IF NOT EXISTS unique_active_channel 
    ON channels(guardian_id, caregiver_id, senior_id) 
    WHERE status = 'active';

-- ==========================================
-- 완료 메시지
-- ==========================================

DO $$
BEGIN
    RAISE NOTICE '==========================================';
    RAISE NOTICE '✅ Sinabro 데이터베이스 테이블 생성 완료!';
    RAISE NOTICE '==========================================';
    RAISE NOTICE '📊 생성된 테이블 (13개):';
    RAISE NOTICE '  • access_codes: 접속 코드 관리';
    RAISE NOTICE '  • guardians: 가디언 (해외 자녀)';
    RAISE NOTICE '  • caregivers: 케어기버 (간병인)';
    RAISE NOTICE '  • seniors: 시니어 (돌봄 대상)';
    RAISE NOTICE '  • channels: 케어 채널';
    RAISE NOTICE '  • checklist_templates: 체크리스트 템플릿';
    RAISE NOTICE '  • daily_checklists: 일일 체크리스트';
    RAISE NOTICE '  • care_notes: 돌봄노트';
    RAISE NOTICE '  • photos: 사진 관리';
    RAISE NOTICE '  • admin_questions: 관리자 질문';
    RAISE NOTICE '  • question_responses: 질문 답변';
    RAISE NOTICE '  • ai_reports: AI 리포트';
    RAISE NOTICE '  • guardian_feedback: 가디언 피드백';
    RAISE NOTICE '==========================================';
    RAISE NOTICE '🔗 외래키: 37개 제약조건 설정됨';
    RAISE NOTICE '⚡ 인덱스: 17개 성능 최적화 인덱스 생성됨';
    RAISE NOTICE '==========================================';
END $$;
