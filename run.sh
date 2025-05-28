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
docker-compose build
docker-compose up
docker-compose logs -f | grep -v "GET /health"


# chmod +x run.sh
# ./run.sh