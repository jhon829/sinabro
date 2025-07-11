-- ==========================================
-- Sinabro 데이터베이스 초기화 스크립트 1/3
-- 데이터베이스 생성 및 확장 설치
-- ==========================================

-- UUID 확장 활성화 (필수)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 암호화 함수 확장 활성화 (필수)
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 텍스트 검색 확장 (검색 기능용)
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- 날짜/시간 함수 확장
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- 성공 메시지
DO $$
BEGIN
    RAISE NOTICE '==========================================';
    RAISE NOTICE '✅ Sinabro 데이터베이스 확장 설치 완료!';
    RAISE NOTICE '==========================================';
    RAISE NOTICE '📦 설치된 확장:';
    RAISE NOTICE '  • uuid-ossp: UUID 생성';
    RAISE NOTICE '  • pgcrypto: 암호화 함수';
    RAISE NOTICE '  • pg_trgm: 텍스트 검색';
    RAISE NOTICE '  • btree_gin: 인덱스 최적화';
    RAISE NOTICE '==========================================';
END $$;
