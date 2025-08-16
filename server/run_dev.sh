#!/bin/bash

# RemotelyX Server Development Startup Script

echo "🚀 Starting RemotelyX Server Development..."

# Check if we're in the server directory
if [ ! -f "main.py" ]; then
    echo "❌ Please run this script from the server directory"
    echo "   cd server && ./run_dev.sh"
    exit 1
fi

# Check if Poetry is available
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry is not installed. Please install Poetry first."
    exit 1
fi

# Check if MongoDB is running
if ! curl -s http://localhost:27017 > /dev/null 2>&1; then
    echo "⚠️  MongoDB doesn't seem to be running on localhost:27017"
    echo "💡 You can start MongoDB with: docker run -d -p 27017:27017 --name mongo mongo:latest"
fi

# Install dependencies if needed
echo "📦 Installing dependencies..."
poetry install

# Start the development server
echo "🔥 Starting FastAPI server with auto-reload..."
echo "📚 API Documentation will be available at:"
echo "   - Swagger UI: http://localhost:8000/docs"
echo "   - ReDoc: http://localhost:8000/redoc"
echo "🌐 API Base URL: http://localhost:8000/api/v1"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload 