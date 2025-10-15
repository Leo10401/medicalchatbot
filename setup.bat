@echo off
echo ================================================
echo   Medical AI Chatbot - Complete Setup
echo ================================================
echo.

echo Step 1: Installing required packages...
echo ================================================
pip install -r requirements.txt
echo.

echo Step 2: Training the disease prediction model...
echo ================================================
python trainmodel.py
echo.

if errorlevel 1 (
    echo [ERROR] Model training failed!
    pause
    exit /b
)

echo.
echo ================================================
echo   Setup Complete!
echo ================================================
echo.
echo Next steps:
echo 1. Set your OpenRouter API key:
echo    set OPENROUTER_API_KEY=sk-or-v1-your-api-key-here
echo.
echo 2. Run the chatbot:
echo    python app.py
echo.
echo Or simply run: run_chatbot.bat
echo ================================================
echo.

pause
