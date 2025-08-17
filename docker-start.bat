@echo off
REM RemotelyX Docker Startup Script for Windows

echo 🚀 Starting RemotelyX Platform...
echo ==================================

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

REM Start services
echo 🔄 Starting all services...
docker-compose up -d

if %errorlevel% equ 0 (
    echo.
    echo ✅ All services started successfully!
    echo.
    echo 🌐 Access URLs:
    echo    - Frontend (Streamlit): http://localhost:8501
    echo    - Backend API: http://localhost:8000
    echo    - API Docs: http://localhost:8000/docs
    echo    - n8n Workflow: http://localhost:5679
    echo    - MongoDB: localhost:27017
    echo    - Redis: localhost:6379
    echo    - Ollama AI: http://localhost:11434
    echo.
    echo 🔐 Default Credentials:
    echo    - MongoDB: admin / password123
    echo    - n8n: hadihaidar1723@gmail.com / Treble23!
    echo    - App Demo: admin / admin123
    echo.
    echo ⏱️  Note: Services may take a few minutes to fully initialize
    echo 📊 Check status with: docker-compose ps
    echo.
    echo 🤖 To setup AI models, run: docker exec remotelyx_ollama ollama pull llama3.2
) else (
    echo ❌ Failed to start services. Check the logs with: docker-compose logs
    pause
    exit /b 1
)

pause
