#!/bin/bash

# Stop containers if running
echo "🧹 Cleaning up old containers..."
docker-compose down --volumes --remove-orphans

# Build everything
echo "🔨 Building Docker containers..."
docker-compose build

# Start all services
echo "🚀 Starting up the services..."
docker-compose up -d

# Show container status
docker-compose ps


# chmod +x run.sh
