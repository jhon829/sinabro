# 🏠 Sinabro - 재외동포 시니어 간병 서비스

> **"시나브로"** - 모르는 사이에 조금씩, 천천히 발전하는 케어 서비스

## 📋 프로젝트 개요

재외동포 가족을 위한 AI 기반 시니어 케어 플랫폼입니다.
해외에 거주하는 자녀들이 국내 부모님의 건강과 안전을 원격으로 관리할 수 있도록 지원합니다.

## 🏗️ 기술 스택

- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15+
- **Cache**: Redis 7+
- **Container**: Docker & Docker Compose
- **AI**: OpenAI GPT-4, Google Translate API

## 🚀 빠른 시작

### 1. 프로젝트 클론
```bash
git clone <repository-url>
cd sinabro
```

### 2. 환경 변수 설정
```bash
cp .env.example .env
# .env 파일을 편집하여 필요한 값들을 설정하세요
```

### 3. Docker로 실행
```bash
# 전체 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 서비스 중지
docker-compose down
```

## 📁 프로젝트 구조

```
sinabro/
├── app/                        # FastAPI 애플리케이션
│   ├── main.py                # 메인 애플리케이션
│   ├── database.py            # 데이터베이스 연결
│   ├── models/                # SQLAlchemy 모델
│   ├── routers/               # API 라우터
│   ├── schemas/               # Pydantic 스키마
│   └── services/              # 비즈니스 로직
├── database/                   # 데이터베이스 설정
│   ├── init/                  # 초기화 SQL 스크립트
│   └── data/                  # PostgreSQL 데이터
├── tests/                     # 테스트 코드
├── docs/                      # 문서
├── docker-compose.yml         # Docker Compose 설정
├── Dockerfile                 # Docker 이미지 설정
├── requirements.txt           # Python 의존성
└── .env                       # 환경 변수
```

## 🎯 핵심 기능

### 1. 체크리스트 기반 간병 기록
- 간편한 체크박스 형태의 일일 케어 기록
- 가디언 맞춤형 요청사항 자동 반영
- 서류 작업 시간 50% 절감

### 2. AI 자동 리포팅
- 150자 이내 요약 리포트 자동 생성
- 다국어 실시간 번역 (한/영/중/일)
- 감정적 연결 강화 AI 코멘트

### 3. 실시간 피드백 루프
- 가디언 피드백 즉시 반영
- 개인화된 케어 서비스 제공
- 데이터 기반 서비스 품질 최적화

## 🔧 개발 환경 설정

### 필수 요구사항
- Docker Desktop
- Python 3.11+
- Git

### 로컬 개발
```bash
# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 개발 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📊 API 문서

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 테스트

```bash
# 단위 테스트 실행
pytest tests/

# 커버리지 포함 테스트
pytest --cov=app tests/

# 특정 테스트 실행
pytest tests/test_checklists.py
```

## 📈 모니터링

- **pgAdmin**: http://localhost:5050 (데이터베이스 관리)
- **API Health**: http://localhost:8000/health

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 👨‍💻 개발팀

- **Backend Developer**: [김동년]
- **Project Manager**: [PM명]

## 📞 연락처

프로젝트 문의: [qwert884@naver.com]
프로젝트 링크: [https://github.com/jhon829/sinabro]

---

**"시나브로, 조금씩 더 나은 케어를 향해"** 💝
