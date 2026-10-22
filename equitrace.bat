@echo off
title EquiTrace AI - Terminal Runner
cd /d "%~dp0"
cls
py cli.py %*
if "%~1"=="" pause
