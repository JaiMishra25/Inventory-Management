# Multi-stage Dockerfile for Inventory Management Tool
# Stage 1: Build the React frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy package files
COPY frontend/package*.json ./

# Install frontend dependencies
RUN npm install --omit=dev

# Copy frontend source code
COPY frontend/ ./

# Build the frontend
RUN npm run build

# Stage 2: Python backend and serve frontend
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=8080

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY app/ ./app/

# Copy built frontend from stage 1
COPY --from=frontend-builder /app/frontend/build ./frontend/build

# Create a simple static file server for the frontend
RUN pip install aiofiles

# Expose the port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/ || exit 1

# Start the application
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"] 