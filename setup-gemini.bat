@echo off
echo ===========================================
echo    RemotelyX Gemini AI Setup
echo ===========================================
echo.
echo This script will help you set up Gemini AI for intelligent job extraction.
echo.
echo 1. Get your Gemini API key from: https://makersuite.google.com/app/apikey
echo 2. Sign in to Google AI Studio
echo 3. Click "Create API Key"
echo 4. Copy the generated key
echo.
set /p GEMINI_KEY="Enter your Gemini API key: "
echo.
echo Setting up Gemini API key...
setx GEMINI_API_KEY "%GEMINI_KEY%"
echo.
echo ✅ Gemini API key has been set!
echo.
echo You can now restart your Docker containers to enable AI extraction:
echo   docker-compose down
echo   docker-compose up -d
echo.
pause
