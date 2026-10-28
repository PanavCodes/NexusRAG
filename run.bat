@echo off
setlocal enabledelayedexpansion
title NexusRAG Launcher
cd /d "%~dp0"

echo =====================================================================
echo                NexusRAG • Autonomous RAG Platform
echo            Google Gemini & OpenRouter AI Intelligence
echo =====================================================================
echo.

:: Check Virtual Environment
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found in .venv!
    echo Please run 'setup.bat' first to install all packages and dependencies.
    echo.
    pause
    exit /b 1
)

:: Set environment paths and API keys
set "PYTHONPATH=%~dp0"

if exist ".env" (
    for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
        set "line=%%A"
        if not "!line:~0,1!"=="#" (
            if not "%%B"=="" set "%%A=%%B"
        )
    )
)

:: Check API keys presence
if "%GEMINI_API_KEY%"=="" if "%OPENROUTER_API_KEY%"=="" (
    echo [INFO] No API keys detected in .env or environment.
    echo You can configure GEMINI_API_KEY or OPENROUTER_API_KEY in .env,
    echo or enter them interactively inside the NexusRAG UI Settings tab.
    echo.
)

echo [*] Activating environment...
call .venv\Scripts\activate.bat

echo [*] Starting NexusRAG server on http://localhost:8501 ...
echo [*] Opening default web browser...

:: Open web browser after a short delay
start "" http://localhost:8501

:: Launch Streamlit server
python -m streamlit run main.py --server.port 8501 --server.headless false

echo.
echo NexusRAG server has stopped.
pause

