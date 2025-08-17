@echo off
REM Setup ngrok for n8n RemotelyX Dashboard

echo 🌐 Setting up ngrok for n8n integration...
echo ===========================================

echo.
echo 📋 Instructions:
echo 1. Make sure ngrok is installed (https://ngrok.com/)
echo 2. Run: ngrok http 5679
echo 3. Copy your ngrok URL (e.g., https://abc123.ngrok.io)
echo 4. Update docker-compose.yml with your ngrok URL
echo 5. Restart n8n service
echo.

set /p NGROK_URL="Enter your ngrok URL (e.g., https://abc123.ngrok.io): "

if "%NGROK_URL%"=="" (
    echo ❌ No URL provided. Exiting...
    pause
    exit /b 1
)

echo.
echo 🔄 Updating docker-compose.yml with your ngrok URL...

REM Update the docker-compose.yml file
powershell -Command "(gc docker-compose.yml) -replace 'https://your-ngrok-subdomain.ngrok.io/', '%NGROK_URL%/' | Out-File -encoding ASCII docker-compose.yml"

echo ✅ Updated docker-compose.yml
echo.

echo 🔄 Restarting n8n service...
docker-compose restart n8n

echo.
echo ✅ Setup complete!
echo.
echo 🌐 Access URLs:
echo    - Local n8n: http://localhost:5679
echo    - Public n8n: %NGROK_URL%
echo    - Credentials: hadihaidar1723@gmail.com / Treble23!
echo.
echo 💡 Your webhooks will now work with: %NGROK_URL%/webhook/
echo.

pause
