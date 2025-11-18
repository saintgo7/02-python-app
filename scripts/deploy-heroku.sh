#!/bin/bash
# Heroku Deployment Script

set -e

PROJECT_NAME="$1"
ENVIRONMENT="${2:-staging}"

if [ -z "$PROJECT_NAME" ]; then
    echo "Usage: ./deploy-heroku.sh <project-name> [environment]"
    exit 1
fi

HEROKU_APP="${PROJECT_NAME}-${ENVIRONMENT}"

echo "🚀 Deploying $PROJECT_NAME to Heroku ($HEROKU_APP)..."

# Login to Heroku
echo "🔐 Logging in to Heroku..."
heroku login

# Create app if it doesn't exist
echo "📝 Creating Heroku app..."
heroku create $HEROKU_APP 2>/dev/null || true

# Add buildpacks
echo "⚙️  Adding buildpacks..."
heroku buildpacks:add --index 1 heroku/python -a $HEROKU_APP
heroku buildpacks:add --index 2 heroku/nodejs -a $HEROKU_APP 2>/dev/null || true

# Set environment variables
echo "🔑 Setting environment variables..."
heroku config:set DEBUG=false -a $HEROKU_APP
heroku config:set ENVIRONMENT=$ENVIRONMENT -a $HEROKU_APP

# Add PostgreSQL addon
echo "🗄️  Adding PostgreSQL..."
heroku addons:create heroku-postgresql:hobby-dev -a $HEROKU_APP 2>/dev/null || true

# Add Redis addon
echo "🔴 Adding Redis..."
heroku addons:create heroku-redis:premium-0 -a $HEROKU_APP 2>/dev/null || true

# Deploy
echo "📦 Deploying to Heroku..."
git push heroku main:main || git push heroku develop:main

# Run migrations
echo "🔄 Running migrations..."
heroku run python manage.py migrate -a $HEROKU_APP 2>/dev/null || true

echo "✅ Deployment complete!"
echo "📍 Application URL: https://$HEROKU_APP.herokuapp.com"
heroku open -a $HEROKU_APP
