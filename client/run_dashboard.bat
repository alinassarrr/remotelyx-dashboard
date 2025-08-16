@echo off
echo 🚀 Starting RemotelyX Dashboard...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not installed. Please install pip first.
    pause
    exit /b 1
)

echo 📦 Installing/updating dependencies...
pip install -r requirements.txt

REM Check if streamlit is installed
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo ❌ Streamlit is not installed. Installing now...
    pip install streamlit
)

echo ✅ Dependencies installed successfully!
echo 🌐 Starting dashboard...
echo 📱 Open your browser and go to: http://localhost:8501
echo ⏹️  Press Ctrl+C to stop the dashboard
echo.

REM Run the dashboard
streamlit run app.py

pause 