@echo off
echo === DRL Management System CLI - Windows Setup ===
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found

REM Install groq package
echo 📦 Installing groq package...
pip install groq
if %errorlevel% neq 0 (
    echo ❌ Failed to install groq package
    echo Please run: pip install groq
    pause
    exit /b 1
)

echo ✅ Groq package installed successfully
echo.
echo 🚀 Setup complete! Here's how to get started on Windows:
echo.
echo 1. Set up your Groq API key:
echo    python drl_management_cli.py config set-api-key
echo.
echo 2. Start interactive mode:
echo    python drl_management_cli.py --interactive
echo.
echo 3. Or scan a repository directly:
echo    python drl_management_cli.py scan C:\path\to\your\project
echo.
echo 4. Get help anytime:
echo    python drl_management_cli.py --help
echo.

REM Ask if user wants to set up API key now
set /p setup_api="Would you like to set up your Groq API key now? (y/n): "
if /i "%setup_api%"=="y" (
    echo.
    echo Please get your API key from: https://console.groq.com/
    python drl_management_cli.py config set-api-key
)

echo.
echo 🎉 You're ready to use the DRL Management System CLI on Windows!
pause
