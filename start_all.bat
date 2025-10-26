@echo off
chcp 65001 > nul
cd /d "%~dp0"
title SocialBoost Full System
echo Starting SocialBoost Full System (GUI + Scheduler)...

REM Activate virtual environment
echo Activating venv...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)

REM Start Scheduler in a separate background window
echo Launching Scheduler in background...
start "SocialBoost Scheduler" cmd /c "python Automatizare_Completa/scheduler.py"
REM Add a short pause to allow scheduler to start/crash
timeout /t 3 /nobreak > nul 

REM Run the GUI script in this window
echo Launching GUI...
python GUI/main_gui.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to launch GUI! Check logs/gui.log (if exists) or system.log.
    pause
    exit /b 1
)

echo GUI closed. Scheduler might still be running in background.
echo You can stop the scheduler using the GUI or Task Manager.
pause

