@echo off
chcp 65001 > nul
echo 🚀 Sinabro 빠른 시작!
echo ==========================================

echo 📋 1. 환경 변수 확인 중...
if not exist .env (
    echo ❌ .env 파일이 없습니다!
    echo 📝 .env.example을 복사해서 .env 파일을 만들어주세요.
    pause
    exit /b 1
)
echo ✅ .env 파일 확인됨

echo.
echo 📋 2. Docker 상태 확인 중...
docker info > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker가 실행되지 않았습니다!
    echo 🔧 Docker Desktop을 시작해주세요.
    pause
    exit /b 1
)
echo ✅ Docker 정상 실행 중

echo.
echo 📋 3. 서비스 시작 중...
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

echo.
echo 📋 4. 서비스 상태 확인 중...
timeout /t 5 > nul
docker-compose ps

echo.
echo 🎉 Sinabro 서비스가 시작되었습니다!
echo ==========================================
echo.
echo 🌐 접속 정보:
echo   • API 서버: http://localhost:8000
echo   • API 문서: http://localhost:8000/docs
echo   • pgAdmin: http://localhost:5050
echo   • Redis Commander: http://localhost:8081
echo.
echo 📝 로그인 정보:
echo   • pgAdmin: admin@sinabro.com / admin123
echo.
echo 🔧 관리 명령어:
echo   • 상태 확인: docker-compose ps
echo   • 로그 확인: docker-compose logs -f
echo   • 서비스 중지: docker-compose down
echo.
echo ==========================================

pause
