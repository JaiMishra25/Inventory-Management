#!/usr/bin/env python3
"""
Inventory Management Tool - Startup Script
This script starts the FastAPI application with proper configuration.
"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    print("Starting Inventory Management Tool...")
    print("API Documentation will be available at: http://localhost:8080/docs")
    print("Alternative documentation at: http://localhost:8080/redoc")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    ) 