#!/bin/bash

# RemotelyX Backend Server Startup Script

echo "🚀 Starting RemotelyX Backend Server..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if MongoDB is running
echo "🗄️ Checking MongoDB connection..."
if ! python3 -c "
import motor.motor_asyncio
import asyncio
async def check_mongo():
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
        await client.admin.command('ping')
        print('✅ MongoDB is running')
        client.close()
    except Exception as e:
        print('❌ MongoDB connection failed:', e)
        exit(1)
asyncio.run(check_mongo())
"; then
    echo "❌ MongoDB is not running. Please start MongoDB first."
    echo "   On Ubuntu/Debian: sudo systemctl start mongod"
    echo "   On macOS: brew services start mongodb-community"
    echo "   On Windows: net start MongoDB"
    exit 1
fi

# Start the server
echo "🌟 Starting server..."
echo "📖 API Documentation will be available at: http://localhost:8000/docs"
echo "🔍 Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 start_server.py 