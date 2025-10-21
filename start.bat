@echo off
REM 中国股市数据分析平台 - 快速启动脚本
REM 
REM 使用方法：双击此文件即可启动应用
REM 或在命令行中运行: start.bat

echo ============================================================
echo   中国股市数据分析平台 - 快速启动
echo ============================================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 Python，请先安装 Python 3.8 或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/3] 检查依赖包...
python -c "import dash, dash_bootstrap_components, plotly, pandas" >nul 2>&1
if %errorlevel% neq 0 (
    echo [提示] 正在安装依赖包...
    python -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [错误] 依赖包安装失败
        pause
        exit /b 1
    )
)
echo [✓] 依赖包检查完成

echo.
echo [2/3] 检查数据文件...
if not exist "data\raw\sh_index.csv" (
    echo [错误] 缺少数据文件: data\raw\sh_index.csv
    pause
    exit /b 1
)
echo [✓] 数据文件检查完成

echo.
echo [3/3] 启动应用...
echo.

REM 启动应用
python main.py

pause
