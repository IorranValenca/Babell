@echo off
title Babell
echo Starting Babell...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo Python found. Starting terminal...
echo.

REM Run the natural language terminal
python natural_language_terminal.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo Babell exited with an error.
    pause
)
