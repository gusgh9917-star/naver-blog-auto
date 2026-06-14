@echo off
chcp 65001 > nul
echo ================================================
echo   네이버 블로그 자동화 - 초기 설정
echo ================================================
echo.

:: Python 확인
python --version > nul 2>&1
if errorlevel 1 (
    echo [오류] Python이 설치되지 않았습니다.
    echo https://www.python.org 에서 Python 3.10 이상을 설치해주세요.
    pause
    exit /b
)

echo [1/3] Python 확인 완료
echo.

:: 패키지 설치
echo [2/3] 필요한 패키지 설치 중... (수 분 소요될 수 있습니다)
pip install -r requirements.txt
if errorlevel 1 (
    echo [오류] 패키지 설치 실패
    pause
    exit /b
)
echo.

:: .env 파일 생성
if not exist ".env" (
    copy ".env.example" ".env" > nul
    echo [3/3] .env 설정 파일 생성 완료
    echo.
    echo ================================================
    echo  중요! .env 파일을 열어서 API 키를 입력해주세요:
    echo  C:\Users\gusgh\naver-blog-auto\.env
    echo ================================================
    notepad .env
) else (
    echo [3/3] .env 파일이 이미 존재합니다.
)

echo.
echo 설정 완료! run.bat 을 실행해서 프로그램을 시작하세요.
pause
