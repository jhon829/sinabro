@echo off
chcp 65001 > nul
title Sinabro Docker Manager

:MENU
cls
echo ==========================================
echo     🏠 Sinabro Docker 관리 도구
echo ==========================================
echo.
echo 🐳 Docker 서비스 관리:
echo   1. 전체 서비스 시작 (개발모드)
echo   2. 전체 서비스 시작 (프로덕션모드)
echo   3. 서비스 중지
echo   4. 서비스 재시작
echo.
echo 📊 상태 확인:
echo   5. 서비스 상태 확인
echo   6. 로그 확인
echo   7. 데이터베이스 접속 테스트
echo.
echo 🧹 관리 작업:
echo   8. 컨테이너 정리
echo   9. 볼륨 정리 (주의!)
echo   0. 종료
echo.
echo ==========================================

set /p choice=선택하세요 (0-9): 

if "%choice%"=="1" goto DEV_START
if "%choice%"=="2" goto PROD_START
if "%choice%"=="3" goto STOP
if "%choice%"=="4" goto RESTART
if "%choice%"=="5" goto STATUS
if "%choice%"=="6" goto LOGS
if "%choice%"=="7" goto DB_TEST
if "%choice%"=="8" goto CLEANUP
if "%choice%"=="9" goto VOLUME_CLEANUP
if "%choice%"=="0" goto EXIT

echo 잘못된 선택입니다.
timeout /t 2 > nul
goto MENU

:DEV_START
echo 🚀 개발모드로 서비스 시작 중...
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
echo.
echo ✅ 서비스가 시작되었습니다!
echo 📝 접속 정보:
echo   • API 문서: http://localhost:8000/docs
echo   • pgAdmin: http://localhost:5050
echo   • Redis Commander: http://localhost:8081
echo.
pause
goto MENU

:PROD_START
echo 🚀 프로덕션모드로 서비스 시작 중...
docker-compose up -d
echo.
echo ✅ 서비스가 시작되었습니다!
pause
goto MENU

:STOP
echo 🛑 서비스 중지 중...
docker-compose down
echo ✅ 모든 서비스가 중지되었습니다.
pause
goto MENU

:RESTART
echo 🔄 서비스 재시작 중...
docker-compose restart
echo ✅ 서비스가 재시작되었습니다.
pause
goto MENU

:STATUS
echo 📊 서비스 상태:
echo ==========================================
docker-compose ps
echo.
echo 📊 Docker 상태:
echo ==========================================
docker stats --no-stream
echo.
pause
goto MENU

:LOGS
echo 📋 실시간 로그 (Ctrl+C로 종료):
docker-compose logs -f
pause
goto MENU

:DB_TEST
echo 🔍 데이터베이스 연결 테스트 중...
docker-compose exec db psql -U sinabro_user -d sinabro_db -c "SELECT 'Database connection successful!' as status;"
if %errorlevel% equ 0 (
    echo ✅ 데이터베이스 연결 성공!
) else (
    echo ❌ 데이터베이스 연결 실패!
)
pause
goto MENU

:CLEANUP
echo 🧹 사용하지 않는 컨테이너 정리 중...
docker system prune -f
echo ✅ 정리 완료!
pause
goto MENU

:VOLUME_CLEANUP
echo ⚠️  WARNING: 모든 데이터가 삭제됩니다!
set /p confirm=정말 진행하시겠습니까? (y/N): 
if /i "%confirm%"=="y" (
    echo 🗑️ 볼륨 삭제 중...
    docker-compose down -v
    docker volume prune -f
    echo ✅ 모든 데이터가 삭제되었습니다.
) else (
    echo ❌ 취소되었습니다.
)
pause
goto MENU

:EXIT
echo 👋 Sinabro Docker Manager를 종료합니다.
exit /b 0
