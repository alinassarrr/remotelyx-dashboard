#!/bin/bash

# RemotelyX Database Management Script

echo "🗄️  RemotelyX Database Management"
echo "=================================="

# Check if we're in the server directory
if [ ! -f "manage.py" ]; then
    echo "❌ Please run this script from the server directory"
    echo "   cd server && ./db.sh"
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

# Function to show usage
show_usage() {
    echo ""
    echo "Usage: ./db.sh [command]"
    echo ""
    echo "Commands:"
    echo "  migrate    Run all pending migrations"
    echo "  seed       Run all pending seeds"
    echo "  setup      Run migrations + seeds (full setup)"
    echo "  status     Show migration and seed status"
    echo "  reset      Reset database (drop all collections)"
    echo "  help       Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./db.sh setup      # Full database setup"
    echo "  ./db.sh migrate    # Run migrations only"
    echo "  ./db.sh seed       # Run seeds only"
    echo "  ./db.sh status     # Check current status"
}

# Main logic
case "${1:-help}" in
    "migrate")
        echo "🔄 Running migrations..."
        poetry run python manage.py migrate
        ;;
    "seed")
        echo "🌱 Running seeds..."
        poetry run python manage.py seed
        ;;
    "setup")
        echo "🚀 Setting up database..."
        poetry run python manage.py setup
        ;;
    "status")
        echo "📊 Checking database status..."
        poetry run python manage.py status
        ;;
    "reset")
        echo "⚠️  Resetting database..."
        read -p "Are you sure you want to drop all collections? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            poetry run python manage.py reset
        else
            echo "Database reset cancelled."
        fi
        ;;
    "help"|*)
        show_usage
        ;;
esac 