@echo off
title Automated Literature Review Assistant
cd /d "%~dp0"

echo ================================================================
echo    AUTOMATED LITERATURE REVIEW ASSISTANT (LiteratureAI)
echo    Starting Agentic AI System & Launching Web UI...
echo ================================================================
echo.

:: Launch default browser after 2 seconds in background
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://127.0.0.1:7860"

:: Start Python App
python app.py

pause
