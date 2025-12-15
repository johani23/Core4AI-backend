@echo off
title Core4.AI Backend Server
color 0E

echo ===============================================
echo 💎 Starting Core4.AI Backend Server
echo ===============================================

REM 🔹 Activate virtual environment
if exist venv (
    echo ⚙️  Activating virtual environment...
    call venv\Scripts\activate
) else (
    echo ❌ Virtual environment not found.
    echo 🪄 Creating new one...
    python -m venv venv
    call venv\Scripts\activate
)

REM 🔹 Ensure dependencies exist
echo.
echo 🔍 Checking dependencies...
python -m pip install --upgrade pip >nul
python -m pip install "uvicorn[standard]" fastapi sqlalchemy >nul

echo.
echo ===============================================
echo 🚀 Launching FastAPI server at http://127.0.0.1:8000 ...
echo ===============================================

python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

echo.
pause
