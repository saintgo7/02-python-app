#!/bin/bash
# DigitalOcean App Platform Deployment Script

set -e

PROJECT_NAME="$1"
ENVIRONMENT="${2:-staging}"

if [ -z "$PROJECT_NAME" ]; then
    echo "Usage: ./deploy-digitalocean.sh <project-name> [environment]"
    exit 1
fi

echo "🚀 Deploying $PROJECT_NAME to DigitalOcean App Platform..."

# Install doctl CLI
if ! command -v doctl &> /dev/null; then
    echo "📥 Installing doctl CLI..."
    cd ~
    wget https://github.com/digitalocean/doctl/releases/download/v1.98.4/doctl-1.98.4-linux-amd64.tar.gz
    tar xf ~/doctl-1.98.4-linux-amd64.tar.gz
    sudo mv ~/doctl /usr/local/bin
fi

# Authenticate
echo "🔐 Authenticating with DigitalOcean..."
doctl auth init --access-token $DIGITALOCEAN_TOKEN

# Create app.yaml
echo "📝 Creating app configuration..."
cat > app.yaml << EOF
name: $PROJECT_NAME
services:
- name: web
  github:
    repo: your-username/your-repo
    branch: $ENVIRONMENT
  build_command: pip install -r requirements.txt
  run_command: gunicorn main:app --workers 4
  environment_slug: python
  http_port: 8000
  min_instance_count: 1
  max_instance_count: 3
  instance_size_slug: basic-s
databases:
- name: postgresql
  engine: PG
  version: "15"
  production: true
- name: redis
  engine: REDIS
  version: "7"
  production: true
EOF

# Deploy
echo "🚀 Creating/updating app..."
doctl apps create --spec app.yaml || doctl apps update --spec app.yaml

echo "✅ Deployment complete!"
doctl apps list
