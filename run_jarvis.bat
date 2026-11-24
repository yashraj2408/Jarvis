@echo off
title J.A.R.V.I.S. Launcher - Stark Industries
color 0B
cls
echo =====================================================================
echo           ⚡ J.A.R.V.I.S. - STARK INDUSTRIES OS LAUNCHER ⚡
echo =====================================================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

if not exist ".venv" (
    echo [INFO] Creating Python virtual environment (.venv)...
    python -m venv .venv
)

echo [INFO] Activating virtual environment...
call .venv\Scripts\activate.bat

echo [INFO] Installing / verifying required libraries...
python -m pip install --upgrade pip >nul 2>nul
pip install -r requirements.txt

echo.
echo =====================================================================
echo [SUCCESS] J.A.R.V.I.S. is ready! Launching web interface...
echo =====================================================================
echo.

python -m streamlit run streamlit_app.py

pause
