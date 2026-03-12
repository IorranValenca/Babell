@echo off
title Babell - Natural Language Terminal
color 0A
echo.
echo  ██████╗  █████╗ ██████╗ ███████╗██╗     ██╗     
echo  ██╔══██╗██╔══██╗██╔══██╗██╔════╝██║     ██║     
echo  ██████╔╝███████║██████╔╝█████╗  ██║     ██║     
echo  ██╔══██╗██╔══██║██╔══██╗██╔══╝  ██║     ██║     
echo  ██████╔╝██║  ██║██████╔╝███████╗███████╗███████╗
echo  ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝╚══════╝
echo.
echo  Natural Language Terminal
echo  ========================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo.
    echo Please install Python 3.7+ from:
    echo https://python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [INFO] Python found. Starting Babell...
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Run Babell with error handling
python main.py

REM Check if the program exited with an error
if errorlevel 1 (
    echo.
    echo [ERROR] Babell encountered an error.
    echo.
    echo Common solutions:
    echo 1. Make sure you're running this from the Babell folder
    echo 2. Check that all files are in the correct locations
    echo 3. Try running: python main.py
    echo.
    pause
) else (
    echo.
    echo [INFO] Babell closed successfully.
)

echo.
echo Press any key to exit...
pause >nul
