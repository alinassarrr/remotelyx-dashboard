#!/bin/bash

echo "🚀 Starting RemotelyX Dashboard with Login System..."
echo ""
echo "🔐 Login Page will open at: http://localhost:8501"
echo "👤 Demo Accounts Available:"
echo "   • admin / admin123 (Administrator)"
echo "   • racile / password123 (Manager)" 
echo "   • demo / secret123 (Demo User)"
echo "   • user / hello123 (Standard User)"
echo ""
echo "📱 Or click any demo account button for instant access!"
echo ""
echo "🛑 Press Ctrl+C to stop the application"
echo "=================================="

# Navigate to client directory if not already there
cd "$(dirname "$0")"

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Start the unified application (login + dashboard)
echo "🌐 Starting application..."
streamlit run app.py --server.port 8501 