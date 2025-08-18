#!/usr/bin/env python3
"""
Startup script for RemotelyX Backend Server
"""
import uvicorn
import os
from app.core.config import settings

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.getenv("PORT", 8000))
    
    # Get host from environment or use default
    host = os.getenv("HOST", "0.0.0.0")
    
    # Get reload flag from environment
    reload = os.getenv("RELOAD", "false").lower() == "true"
    
    print(f"Starting RemotelyX Backend Server...")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Reload: {reload}")
    print(f"MongoDB: {settings.MONGODB_URL}")
    print(f"Database: {settings.MONGODB_DB}")
    print(f"API Docs: http://{host}:{port}/docs")
    print(f"Health Check: http://{host}:{port}/health")
    
    # Start the server
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    ) 