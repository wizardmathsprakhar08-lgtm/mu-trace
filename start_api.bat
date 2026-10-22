@echo off
cd /d "%~dp0"
echo Starting EquiTrace Enterprise REST API on http://localhost:8000 ...
py -m uvicorn api.app:app --port 8000 --reload
pause
