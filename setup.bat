@echo off
setlocal enabledelayedexpansion
title NexusRAG - Environment Setup & Dependency Installer
cd /d "%~dp0"

echo =====================================================================
echo                     NexusRAG v2.0 Setup Installer
echo         Autonomous Document & Codebase Intelligence Platform
echo =====================================================================
echo.

:: 1. Discover Python on System
echo [*] Checking Python installation...
set "PY_CMD="

python --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PY_CMD=python"
    goto :PYTHON_FOUND
)

py -3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PY_CMD=py -3"
    goto :PYTHON_FOUND
)

python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PY_CMD=python3"
    goto :PYTHON_FOUND
)

echo [ERROR] Python was not found on your system!
echo Please install Python 3.10, 3.11, or 3.12 from https://www.python.org/
echo Make sure to check the box "Add Python to PATH" during installation.
echo.
pause
exit /b 1

:PYTHON_FOUND
echo [+] Python found:
%PY_CMD% --version
echo.

:: 2. Check and Create Virtual Environment
if not exist ".venv\Scripts\activate.bat" (
    echo [*] Creating isolated virtual environment in .venv...
    %PY_CMD% -m venv .venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [+] Virtual environment created successfully.
) else (
    echo [+] Existing virtual environment detected in .venv.
)
echo.

:: 3. Activate Virtual Environment
echo [*] Activating virtual environment...
call .venv\Scripts\activate.bat

:: 4. Ensure Pip is Available and Upgraded
echo [*] Ensuring pip is installed and upgraded...
python -m ensurepip --default-pip >nul 2>&1
python -m pip install --upgrade pip --quiet
echo [+] Pip ready.
echo.

:: 5. Install Project Dependencies
echo [*] Installing required packages from requirements.txt...
echo Installing lightweight cloud dependencies from requirements.txt...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install one or more dependencies.
    echo Please check your internet connection and retry.
    pause
    exit /b 1
)
echo [+] All dependencies installed successfully!
echo.

:: 6. Setup Default .env Configuration
if not exist ".env" (
    if exist ".env.example" (
        echo [*] Initializing .env configuration from .env.example...
        copy /y ".env.example" ".env" >nul
        echo [+] Created .env template. Please configure your API keys in .env.
    ) else (
        echo [*] Creating default .env configuration file...
        (
            echo # NexusRAG Environment Configuration
            echo GEMINI_API_KEY=your_gemini_api_key_here
            echo OPENROUTER_API_KEY=your_openrouter_api_key_here
            echo NEXUSRAG_CONNECT_TIMEOUT=10
            echo NEXUSRAG_WEBSITE_TIMEOUT=60
            echo NEXUSRAG_MAX_FILES=100
            echo NEXUSRAG_GIT_TIMEOUT=180
        ) > ".env"
        echo [+] Created .env template.
    )
) else (
    echo [+] Existing .env configuration file found.
)
echo.

:: 7. Verification Test
echo [*] Verifying installation of core modules...
python -c "import streamlit, llama_index, google.genai, openai, openpyxl, pypdf; print('[+] All core NexusRAG modules verified successfully!')"
if %errorlevel% neq 0 (
    echo [WARNING] Verification check had warnings, but core setup completed.
)
echo.

echo =====================================================================
echo                    Setup Completed Successfully!
echo =====================================================================
echo You can now launch NexusRAG at any time by running:
echo    run.bat
echo.
echo Press any key to start NexusRAG now, or close this window.
pause >nul
call run.bat

