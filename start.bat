@echo off
REM China Stock Market Analysis Platform - Quick Start Script
REM
REM Usage: Double-click this file to start the application
REM Or run in the command line: start.bat

echo ============================================================
echo   China Stock Market Analysis Platform - Quick Start
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [Error] Python not found. Please install Python 3.8 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/3] Checking dependencies...
python -c "import dash, dash_bootstrap_components, plotly, pandas" >nul 2>&1
if %errorlevel% neq 0 (
    echo [Info] Installing dependencies...
    python -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [Error] Failed to install dependencies.
        pause
        exit /b 1
    )
)
echo [✓] Dependencies check complete.

echo.
echo [2/3] Checking data files...
if not exist "data\raw\sh_index.csv" (
    echo [Error] Missing data file: data\raw\sh_index.csv
    pause
    exit /b 1
)
echo [✓] Data files check complete.

echo.
echo [3/3] Starting application...
echo.

REM Start the application
python main.py

pause
