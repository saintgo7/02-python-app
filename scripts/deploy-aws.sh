#!/bin/bash
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
