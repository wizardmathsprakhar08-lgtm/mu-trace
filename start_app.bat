@echo off
cd /d "%~dp0"
echo Starting EquiTrace AI Dashboard...
py -m streamlit run app.py
pause
