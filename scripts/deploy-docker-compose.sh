#!/bin/bash
# Docker Compose Deployment Script for Local/Server Deployment

set -e

PROJECT_NAME="${1:-.}"
ENVIRONMENT="${2:-development}"
PORT="${3:-8000}"

echo "🚀 Deploying $PROJECT_NAME using Docker Compose..."

# Check if docker-compose exists
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose not found. Please install Docker and Docker Compose."
    exit 1
fi

# Create .env file
echo "🔑 Creating environment file..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "📝 Please update .env with your configuration"
fi

# Build images
echo "📦 Building Docker images..."
docker-compose build

# Start services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 5

# Run migrations
echo "🔄 Running migrations..."
docker-compose exec -T web python manage.py migrate 2>/dev/null || true
docker-compose exec -T web python -m alembic upgrade head 2>/dev/null || true

# Create superuser (optional)
if [ "$ENVIRONMENT" = "development" ]; then
    echo "👤 Creating superuser..."
    docker-compose exec -T web python manage.py createsuperuser --noinput --email admin@example.com --username admin 2>/dev/null || true
fi

# Display status
echo "✅ Deployment complete!"
echo "📍 Application running on: http://localhost:$PORT"
docker-compose ps
