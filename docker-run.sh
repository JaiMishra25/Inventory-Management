#!/bin/bash

# Docker deployment script for Inventory Management Tool

set -e

echo "🚀 Starting Inventory Management Tool Backend with Docker..."

# Default port
PORT=${PORT:-8080}

echo "📦 Building Docker image..."
docker build -t inventory-management .

echo "🔧 Starting backend container on port $PORT..."
docker run -d \
  --name inventory-management-app \
  -p $PORT:8080 \
  -e PORT=8080 \
  -v inventory_data:/app/inventory.db \
  --restart unless-stopped \
  inventory-management

echo "✅ Backend started successfully!"
echo "🔧 Backend API at: http://localhost:$PORT"
echo "📚 API Documentation at: http://localhost:$PORT/docs"
echo "⚠️  Note: This is backend only. For frontend, use local development mode."
echo ""
echo "📋 Useful commands:"
echo "  - View logs: docker logs inventory-management-app"
echo "  - Stop app: docker stop inventory-management-app"
echo "  - Remove app: docker rm inventory-management-app"
echo "  - Remove image: docker rmi inventory-management" 