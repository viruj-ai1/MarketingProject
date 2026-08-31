@echo off
REM Always use the project's venv Python to run the app
cd /d "%~dp0"
.\venv\Scripts\python.exe app.py

