@echo off
chcp 65001 > nul
title [동탄트램 24h AI 시스템] 통합 실행기
cd /d "C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG"

echo ========================================================
echo   [동탄트램 엔지니어링 RAG & 24h AI 텔레그램 비서 시스템]
echo ========================================================
echo.
echo 1. RAG 웹 코어 서버 (Port 8080) 기동 중...
python "C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\Rag구축\restart_rag_server.py"

echo.
echo 2. 동탄트램 24시간 텔레그램 AI 봇 (@DongtanTram_AI_bot) 기동 중...
python "C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\Rag구축\start_telegram_bot.py"

echo.
echo 3. 외부 웹 브라우저 접속용 터널 (Cloudflare) 기동...
python start_tunnel.py

echo.
echo ========================================================
echo   모든 시스템이 성공적으로 가동되었습니다!
echo   - 텔레그램 봇: @DongtanTram_AI_bot (24시간 무중단)
echo   - 로컬 웹서버: http://localhost:8080
echo   이 창을 닫아도 백그라운드에서 계속 동작합니다.
echo ========================================================
pause
