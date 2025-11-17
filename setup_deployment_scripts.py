#!/usr/bin/env python3
"""
Deployment Scripts Setup
Creates deployment automation scripts for various platforms
"""

from pathlib import Path

def generate_deploy_aws_script() -> str:
    """Generate AWS deployment script"""
    return '''#!/bin/bash
# AWS Elastic Beanstalk Deployment Script

set -e

PROJECT_NAME="$1"
ENVIRONMENT="${2:-staging}"
REGION="${3:-us-east-1}"

if [ -z "$PROJECT_NAME" ]; then
    echo "Usage: ./deploy-aws.sh <project-name> [environment] [region]"
    exit 1
fi

echo "🚀 Deploying $PROJECT_NAME to AWS Elastic Beanstalk ($ENVIRONMENT)..."

# Build Docker image
echo "📦 Building Docker image..."
docker build -t $PROJECT_NAME:latest .

# Push to ECR
echo "📤 Pushing to ECR..."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $(aws sts get-caller-identity --query Account --output text).dkr.ecr.$REGION.amazonaws.com

aws ecr create-repository --repository-name $PROJECT_NAME --region $REGION 2>/dev/null || true

docker tag $PROJECT_NAME:latest $(aws sts get-caller-identity --query Account --output text).dkr.ecr.$REGION.amazonaws.com/$PROJECT_NAME:latest
docker push $(aws sts get-caller-identity --query Account --output text).dkr.ecr.$REGION.amazonaws.com/$PROJECT_NAME:latest

# Deploy to Elastic Beanstalk
echo "🚀 Deploying to Elastic Beanstalk..."
eb init -p "Docker running on 64bit Amazon Linux 2" $PROJECT_NAME-$ENVIRONMENT --region $REGION --keyname your-key-pair 2>/dev/null || true
eb create $PROJECT_NAME-$ENVIRONMENT --instance-type t3.micro --scale 1 --region $REGION 2>/dev/null || true
eb deploy $PROJECT_NAME-$ENVIRONMENT

# Run migrations (if applicable)
echo "🔄 Running migrations..."
eb ssh -e "python manage.py migrate" $PROJECT_NAME-$ENVIRONMENT 2>/dev/null || true

echo "✅ Deployment complete!"
echo "📍 Application URL: $(eb open --print-url $PROJECT_NAME-$ENVIRONMENT)"
'''

def generate_deploy_heroku_script() -> str:
    """Generate Heroku deployment script"""
    return '''#!/bin/bash
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
'''

def generate_deploy_digitalocean_script() -> str:
    """Generate DigitalOcean deployment script"""
    return '''#!/bin/bash
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
'''

def generate_deploy_docker_compose_script() -> str:
    """Generate Docker Compose deployment script"""
    return '''#!/bin/bash
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
'''

def generate_deploy_kubernetes_script() -> str:
    """Generate Kubernetes deployment script"""
    return '''#!/bin/bash
# Kubernetes Deployment Script

set -e

PROJECT_NAME="$1"
NAMESPACE="${2:-default}"
REPLICAS="${3:-3}"

if [ -z "$PROJECT_NAME" ]; then
    echo "Usage: ./deploy-kubernetes.sh <project-name> [namespace] [replicas]"
    exit 1
fi

echo "🚀 Deploying $PROJECT_NAME to Kubernetes..."

# Check kubectl
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl not found. Please install Kubernetes CLI."
    exit 1
fi

# Create namespace
echo "📦 Creating namespace..."
kubectl create namespace $NAMESPACE 2>/dev/null || true

# Create ConfigMap
echo "⚙️  Creating ConfigMap..."
kubectl create configmap $PROJECT_NAME-config --from-env-file=.env --namespace=$NAMESPACE -o yaml --dry-run=client | kubectl apply -f - 2>/dev/null || true

# Create deployment
echo "🚀 Creating Kubernetes deployment..."
cat << EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: $PROJECT_NAME
  namespace: $NAMESPACE
  labels:
    app: $PROJECT_NAME
spec:
  replicas: $REPLICAS
  selector:
    matchLabels:
      app: $PROJECT_NAME
  template:
    metadata:
      labels:
        app: $PROJECT_NAME
    spec:
      containers:
      - name: $PROJECT_NAME
        image: gcr.io/PROJECT_ID/$PROJECT_NAME:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: $PROJECT_NAME-config
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
EOF

# Create Service
echo "🌐 Creating Kubernetes service..."
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: $PROJECT_NAME-service
  namespace: $NAMESPACE
spec:
  selector:
    app: $PROJECT_NAME
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
EOF

# Create Ingress
echo "🔗 Creating Ingress..."
cat << EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: $PROJECT_NAME-ingress
  namespace: $NAMESPACE
spec:
  rules:
  - host: $PROJECT_NAME.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: $PROJECT_NAME-service
            port:
              number: 80
EOF

echo "✅ Kubernetes deployment complete!"
echo "📍 Service URL: $(kubectl get service $PROJECT_NAME-service -n $NAMESPACE -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')"
kubectl get all -n $NAMESPACE
'''

def generate_deployment_github_action() -> str:
    """Generate deployment GitHub Action workflow"""
    return '''name: Deploy to Production

on:
  push:
    branches: [main]
  workflow_dispatch:

env:
  PROJECT_NAME: ${{ github.event.repository.name }}

jobs:
  deploy-aws:
    runs-on: ubuntu-latest
    if: contains(github.repository, 'aws')
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Deploy to Elastic Beanstalk
        run: |
          chmod +x ./scripts/deploy-aws.sh
          ./scripts/deploy-aws.sh ${{ env.PROJECT_NAME }} production us-east-1

  deploy-heroku:
    runs-on: ubuntu-latest
    if: contains(github.repository, 'heroku')
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Deploy to Heroku
        uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
          heroku_app_name: ${{ env.PROJECT_NAME }}-production
          heroku_email: ${{ secrets.HEROKU_EMAIL }}
          region: us

  deploy-kubernetes:
    runs-on: ubuntu-latest
    if: contains(github.repository, 'k8s')
    steps:
      - uses: actions/checkout@v4

      - name: Set up kubectl
        uses: azure/setup-kubectl@v3
        with:
          version: 'latest'

      - name: Configure kubectl
        run: |
          mkdir -p $HOME/.kube
          echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > $HOME/.kube/config

      - name: Deploy to Kubernetes
        run: |
          chmod +x ./scripts/deploy-kubernetes.sh
          ./scripts/deploy-kubernetes.sh ${{ env.PROJECT_NAME }} production 3

  notify:
    needs: [deploy-aws, deploy-heroku, deploy-kubernetes]
    runs-on: ubuntu-latest
    if: always()
    steps:
      - name: Notify deployment status
        run: |
          echo "Deployment Status: ${{ job.status }}"
          # Add Slack notification
          # Add email notification
          # Add other notifications as needed
'''

def setup_deployment_scripts():
    """Setup deployment scripts for all projects"""
    print("🚀 Setting up Deployment Scripts...")
    print("=" * 70)

    # Root scripts directory
    scripts_dir = Path("/home/user/02-python-app/scripts")
    scripts_dir.mkdir(exist_ok=True)

    # Create deployment scripts
    (scripts_dir / "deploy-aws.sh").write_text(generate_deploy_aws_script())
    (scripts_dir / "deploy-heroku.sh").write_text(generate_deploy_heroku_script())
    (scripts_dir / "deploy-digitalocean.sh").write_text(generate_deploy_digitalocean_script())
    (scripts_dir / "deploy-docker-compose.sh").write_text(generate_deploy_docker_compose_script())
    (scripts_dir / "deploy-kubernetes.sh").write_text(generate_deploy_kubernetes_script())

    # Make scripts executable
    import os
    import stat
    for script in scripts_dir.glob("*.sh"):
        os.chmod(script, os.stat(script).st_mode | stat.S_IEXEC)

    print("[Deployment Scripts (Root)]", end=" ", flush=True)

    # Add deployment workflow to root
    workflows_dir = Path("/home/user/02-python-app/.github/workflows")
    workflows_dir.mkdir(parents=True, exist_ok=True)
    (workflows_dir / "deploy.yml").write_text(generate_deployment_github_action())

    print("✅")

    print("=" * 70)
    print("✨ Deployment scripts setup complete!")
    print("\nDeployment Scripts Created:")
    print("  ✓ scripts/deploy-aws.sh - AWS Elastic Beanstalk")
    print("  ✓ scripts/deploy-heroku.sh - Heroku Platform")
    print("  ✓ scripts/deploy-digitalocean.sh - DigitalOcean Apps")
    print("  ✓ scripts/deploy-docker-compose.sh - Docker Compose")
    print("  ✓ scripts/deploy-kubernetes.sh - Kubernetes")
    print("  ✓ .github/workflows/deploy.yml - GitHub Actions deployment")


if __name__ == "__main__":
    setup_deployment_scripts()
