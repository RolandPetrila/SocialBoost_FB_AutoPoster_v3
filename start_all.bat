@echo off
cd /d "%~dp0"
chcp 65001 > nul
title SocialBoost Full System
echo Starting SocialBoost Full System (GUI + Scheduler)...

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start Scheduler in a separate background window
echo Launching Scheduler in background...
start "SocialBoost Scheduler" cmd /c "python Automatizare_Completa/scheduler.py"

REM Run the GUI script in this window
echo Launching GUI...
python GUI/main_gui.py

echo GUI closed. Scheduler might still be running in background.
echo You can stop the scheduler using the GUI or Task Manager.
pause

