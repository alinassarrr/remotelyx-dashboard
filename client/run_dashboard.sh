#!/bin/bash

# RemotelyX Dashboard Launcher
echo "🚀 Starting RemotelyX Dashboard..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "📦 Installing dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo "✅ Virtual environment found"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if streamlit is available
if ! python -c "import streamlit" &> /dev/null; then
    echo "❌ Streamlit not found in virtual environment. Installing..."
    pip install -r requirements.txt
fi

echo "✅ Dependencies installed successfully!"
echo "🌐 Starting dashboard..."
echo "📱 Open your browser and go to: http://localhost:8501"
echo "⏹️  Press Ctrl+C to stop the dashboard"
echo ""

# Run the dashboard
streamlit run app.py 