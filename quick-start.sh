#!/bin/bash

# RemotelyX Dashboard Quick Start Script
# This script sets up the development environment quickly

set -e

echo "🚀 RemotelyX Dashboard Quick Start"
echo "=================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create .env file if it doesn't exist
if [ ! -f "server/.env" ]; then
    echo "📝 Creating environment file..."
    cp server/.env.example server/.env
    echo "✅ Created server/.env file"
    echo "💡 You may want to edit server/.env with your configuration"
fi

# Start Docker services
echo "🐳 Starting Docker services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo "✅ Services are running!"
    echo ""
    echo "🎉 Setup Complete!"
    echo "=================="
    echo ""
    echo "🔗 Access your application:"
    echo "   • Backend API: http://localhost:8000"
    echo "   • API Docs: http://localhost:8000/docs"
    echo "   • MongoDB: localhost:27017"
    echo "   • Redis: localhost:6379"
    echo ""
    echo "📚 Next steps:"
    echo "   1. Set up the frontend (see README.md)"
    echo "   2. Test the API endpoints"
    echo "   3. Check logs: docker-compose logs -f"
    echo ""
    echo "🛑 To stop services: docker-compose down"
else
    echo "❌ Some services failed to start. Check logs:"
    docker-compose logs
    exit 1
fi
