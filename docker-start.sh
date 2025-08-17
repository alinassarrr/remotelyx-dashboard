#!/bin/bash

# RemotelyX Docker Startup Script
echo "🚀 Starting RemotelyX Platform..."
echo "=================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Docker is installed and running
if ! command_exists docker; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if Docker Compose is available
if ! command_exists docker-compose && ! docker compose version >/dev/null 2>&1; then
    echo "❌ Docker Compose is not available. Please install Docker Compose."
    exit 1
fi

# Function to start services
start_services() {
    echo "🔄 Starting all services..."
    
    # Use docker compose if available, otherwise docker-compose
    if docker compose version >/dev/null 2>&1; then
        docker compose up -d
    else
        docker-compose up -d
    fi
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ All services started successfully!"
        echo ""
        echo "🌐 Access URLs:"
        echo "   - Frontend (Streamlit): http://localhost:8501"
        echo "   - Backend API: http://localhost:8000"
        echo "   - API Docs: http://localhost:8000/docs"
        echo "   - n8n Workflow: http://localhost:5679"
        echo "   - MongoDB: localhost:27017"
        echo "   - Redis: localhost:6379"
        echo "   - Ollama AI: http://localhost:11434"
        echo ""
        echo "🔐 Default Credentials:"
        echo "   - MongoDB: admin / password123"
        echo "   - n8n: hadihaidar1723@gmail.com / Treble23!"
        echo "   - App Demo: admin / admin123"
        echo ""
        echo "⏱️  Note: Services may take a few minutes to fully initialize"
        echo "📊 Check status with: docker-compose ps"
    else
        echo "❌ Failed to start services. Check the logs with: docker-compose logs"
        exit 1
    fi
}

# Function to stop services
stop_services() {
    echo "🛑 Stopping all services..."
    
    if docker compose version >/dev/null 2>&1; then
        docker compose down
    else
        docker-compose down
    fi
    
    echo "✅ All services stopped."
}

# Function to restart services
restart_services() {
    echo "🔄 Restarting all services..."
    stop_services
    start_services
}

# Function to show logs
show_logs() {
    if docker compose version >/dev/null 2>&1; then
        docker compose logs -f
    else
        docker-compose logs -f
    fi
}

# Function to show status
show_status() {
    echo "📊 Service Status:"
    echo "=================="
    
    if docker compose version >/dev/null 2>&1; then
        docker compose ps
    else
        docker-compose ps
    fi
}

# Function to setup Ollama models
setup_ollama() {
    echo "🤖 Setting up Ollama AI models..."
    echo "This may take several minutes..."
    
    # Wait for Ollama to be ready
    echo "⏳ Waiting for Ollama to start..."
    sleep 30
    
    # Pull the required model
    docker exec remotelyx_ollama ollama pull llama3.2
    
    if [ $? -eq 0 ]; then
        echo "✅ Ollama model setup complete!"
    else
        echo "⚠️  Ollama model setup failed. You can set it up manually later with:"
        echo "   docker exec remotelyx_ollama ollama pull llama3.2"
    fi
}

# Main script logic
case "${1:-start}" in
    "start")
        start_services
        ;;
    "stop")
        stop_services
        ;;
    "restart")
        restart_services
        ;;
    "logs")
        show_logs
        ;;
    "status")
        show_status
        ;;
    "setup-ollama")
        setup_ollama
        ;;
    "help"|*)
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  start       Start all services (default)"
        echo "  stop        Stop all services"
        echo "  restart     Restart all services"
        echo "  logs        Show service logs"
        echo "  status      Show service status"
        echo "  setup-ollama Setup Ollama AI models"
        echo "  help        Show this help"
        echo ""
        echo "Examples:"
        echo "  $0 start          # Start all services"
        echo "  $0 setup-ollama   # Setup AI models after first start"
        echo "  $0 logs           # View logs"
        ;;
esac
