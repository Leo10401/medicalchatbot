@echo off
echo ================================================
echo   Medical AI Chatbot - Starting Server
echo ================================================
echo.

REM Check if model files exist
if not exist "random_forest_model.pkl" (
    echo [WARNING] Model files not found!
    echo You need to train the model first.
    echo.
    echo Run: python trainmodel.py
    echo.
    pause
    exit /b
)

REM Check if API key is set
if "%OPENROUTER_API_KEY%"=="" (
    echo [WARNING] OpenRouter API Key not set!
    echo.
    echo Set your API key with:
    echo   set OPENROUTER_API_KEY=sk-or-v1-your-api-key-here
    echo.
    echo Or edit app.py and add your API key directly.
    echo.
    pause
)

echo Starting Flask server...
echo Open your browser to: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ================================================
echo.

python app.py

pause
