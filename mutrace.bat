@echo off
title mu-trace: Institutional Research Terminal
cd /d "%~dp0"
cls
py cli.py %*
if "%~1"=="" pause
