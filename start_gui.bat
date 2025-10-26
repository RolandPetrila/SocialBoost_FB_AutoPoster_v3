@echo off
chcp 65001 > nul
title SocialBoost GUI
echo Starting SocialBoost GUI...

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the GUI script
echo Launching GUI...
python GUI/main_gui.py

echo GUI closed.
pause

