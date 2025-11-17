# 🚀 Deployment Guide

Complete guide to deploy your applications to production across multiple platforms.

## Table of Contents

1. [Deployment Overview](#deployment-overview)
2. [Docker Deployment](#docker-deployment)
3. [AWS Deployment](#aws-deployment)
4. [Heroku Deployment](#heroku-deployment)
5. [DigitalOcean Deployment](#digitalocean-deployment)
6. [Kubernetes Deployment](#kubernetes-deployment)
7. [Environment Configuration](#environment-configuration)
8. [Monitoring & Logging](#monitoring--logging)
9. [Security Best Practices](#security-best-practices)
10. [Troubleshooting](#troubleshooting)

---

## Deployment Overview

### Platform Comparison

| Platform | Cost | Scalability | Ease | Best For |
|----------|------|-------------|------|----------|
| **Docker Compose** | Free | Low | ⭐⭐ | Local/Testing |
| **AWS** | ~$315/mo | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Enterprise |
| **Heroku** | ~$50/mo | ⭐⭐⭐ | ⭐⭐⭐⭐ | Startups |
| **DigitalOcean** | ~$25/mo | ⭐⭐⭐ | ⭐⭐⭐ | Small apps |
| **Kubernetes** | Variable | ⭐⭐⭐⭐⭐ | ⭐⭐ | Complex apps |

### Architecture Layers

```
┌─────────────────────────────────┐
│   Client Application            │
│  (Web Browser / Mobile App)     │
└──────────────┬──────────────────┘
               │
        ┌──────▼──────┐
        │  CDN/DNS    │
        │ (CloudFront)│
        └──────┬──────┘
               │
    ┌──────────▼────────────┐
    │  Load Balancer (ALB)  │
    └──────────┬────────────┘
               │
    ┌──────────▼──────────────────────┐
    │  Application Servers (Scaled)   │
    │  - Container 1                  │
    │  - Container 2                  │
    │  - Container 3 (Auto-scaling)   │
    └──────────┬──────────────────────┘
               │
    ┌──────────▼──────────────────────┐
    │  Data Layer (Persistence)       │
    │  - PostgreSQL (Primary DB)      │
    │  - Redis (Cache/Session)        │
    │  - S3 (Static Files)            │
    └─────────────────────────────────┘
```

---

## Docker Deployment

### Option 1: Docker Compose (Local Development)

Best for development and testing environments.

#### Prerequisites

- Docker installed
- Docker Compose installed

#### Steps

```bash
# 1. Navigate to project directory
cd 01_task_management_saas

# 2. Ensure docker-compose.yml exists
ls docker-compose.yml

# 3. Build images
docker-compose build

# 4. Start services
docker-compose up -d

# 5. Check status
docker-compose ps

# 6. View logs
docker-compose logs -f app

# 7. Access application
# API: http://localhost:8000
# Swagger: http://localhost:8000/docs

# 8. Stop services
docker-compose down

# 9. Clean up volumes
docker-compose down -v
```

#### docker-compose.yml Structure

```yaml
version: '3.8'

services:
  app:
    build: .
    container_name: python-app
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/appdb
      - REDIS_URL=redis://redis:6379
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
      - redis
    volumes:
      - .:/app
    command: python main.py

  db:
    image: postgres:15-alpine
    container_name: postgres-db
    environment:
      - POSTGRES_DB=appdb
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: redis-cache
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

### Option 2: Docker Swarm (Multi-Node)

For distributed deployments across multiple machines.

```bash
# 1. Initialize Docker Swarm
docker swarm init

# 2. Get join token
docker swarm join-token worker

# 3. Join other nodes (on each worker machine)
docker swarm join --token SWMTKN-... <manager-ip>:2377

# 4. Deploy stack
docker stack deploy -c docker-compose.yml myapp

# 5. Check services
docker service ls

# 6. Scale service
docker service scale myapp_app=3

# 7. Monitor
docker service ps myapp_app

# 8. Remove stack
docker stack rm myapp
```

---

## AWS Deployment

### Option 1: AWS Elastic Beanstalk (Recommended)

Managed platform for Python applications. Easiest AWS option.

#### Prerequisites

- AWS Account
- AWS CLI installed and configured
- Elastic Beanstalk CLI (EB CLI)

#### Setup Steps

```bash
# 1. Install EB CLI
pip install awsebcli

# 2. Navigate to project
cd 01_task_management_saas

# 3. Initialize Elastic Beanstalk
eb init -p python-3.11 python-app
# Follow prompts:
# - Select region (us-east-1 recommended)
# - CodeCommit: N
# - SSH: N

# 4. Create environment
eb create production-env
# This creates:
# - EC2 instance(s)
# - Load balancer
# - Auto scaling group
# - RDS database (optional)
# - ElastiCache (optional)

# 5. Check status
eb status

# 6. View logs
eb logs

# 7. Monitor
eb open  # Opens URL in browser

# 8. Deploy updates
# Modify code, then:
eb deploy

# 9. Scale up
eb scale 3  # 3 instances

# 10. Configure environment
eb setenv DATABASE_URL=postgresql://...

# 11. SSH to instance
eb ssh

# 12. Terminate
eb terminate production-env
```

#### .ebextensions Configuration

Create `.ebextensions/python.config`:

```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: main:app
    NumProcesses: 4
    NumThreads: 15
  aws:elasticbeanstalk:application:environment:
    PYTHONPATH: /var/app/current
    SECRET_KEY: your-secret-key

commands:
  01_migrate:
    command: "python -m app.core.database"
    leader_only: true
```

### Option 2: AWS EC2 (Manual Control)

For maximum control and flexibility.

```bash
# 1. Launch EC2 Instance
# - AMI: Amazon Linux 2
# - Instance Type: t3.medium (or larger)
# - Security Group: Allow ports 22, 80, 443
# - Key Pair: Create new or use existing

# 2. SSH into instance
ssh -i your-key.pem ec2-user@your-instance-ip

# 3. Install dependencies
sudo yum update -y
sudo yum install python311 python311-devel python311-pip -y
sudo yum install postgresql postgresql-devel -y
sudo yum install git -y

# 4. Clone repository
cd /home/ec2-user
git clone <repository-url>
cd 01_task_management_saas

# 5. Create Python virtual environment
python3.11 -m venv venv
source venv/bin/activate

# 6. Install Python dependencies
pip install -r requirements.txt
pip install gunicorn

# 7. Create environment file
nano .env.local
# Add your configuration

# 8. Install and start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql
createdb appdb
psql appdb < schema.sql

# 9. Run migrations
python -m app.core.database

# 10. Start application with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app

# 11. Setup systemd service
sudo nano /etc/systemd/system/python-app.service
```

Create `/etc/systemd/system/python-app.service`:

```ini
[Unit]
Description=Python Application
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/01_task_management_saas
Environment="PATH=/home/ec2-user/01_task_management_saas/venv/bin"
ExecStart=/home/ec2-user/01_task_management_saas/venv/bin/gunicorn \
    -w 4 \
    -b 0.0.0.0:8000 \
    main:app

[Install]
WantedBy=multi-user.target
```

```bash
# 12. Enable and start service
sudo systemctl enable python-app
sudo systemctl start python-app
sudo systemctl status python-app

# 13. Install nginx as reverse proxy
sudo yum install nginx -y
# Configure nginx...
sudo systemctl start nginx
sudo systemctl enable nginx
```

### Option 3: AWS with Terraform (Infrastructure as Code)

Using the included Terraform configuration.

```bash
# 1. Navigate to terraform directory
cd terraform

# 2. Initialize Terraform
terraform init

# 3. Choose environment
# Development: terraform plan -var-file=development.tfvars
# Staging: terraform plan -var-file=staging.tfvars
# Production: terraform plan -var-file=production.tfvars

terraform plan -var-file=production.tfvars

# 4. Review plan (carefully!)
# Make sure all resources look correct

# 5. Apply configuration
terraform apply -var-file=production.tfvars

# 6. Get outputs
terraform output

# 7. Access application
# Get the ALB DNS name from outputs
# Access: http://<alb-dns-name>

# 8. Destroy (when done)
terraform destroy -var-file=production.tfvars
```

#### Terraform Environment Files

**development.tfvars**:
```hcl
environment          = "development"
instance_type        = "t3.small"
min_instances        = 1
max_instances        = 2
multi_az            = false
backup_retention    = 7
rds_allocated_storage = 20
redis_node_type     = "cache.t3.micro"
```

**production.tfvars**:
```hcl
environment          = "production"
instance_type        = "t3.large"
min_instances        = 3
max_instances        = 6
multi_az            = true
backup_retention    = 30
rds_allocated_storage = 100
redis_node_type     = "cache.r7g.large"
```

---

## Heroku Deployment

### Prerequisites

- Heroku Account (free tier available)
- Heroku CLI installed
- Git installed

### Deployment Steps

```bash
# 1. Login to Heroku
heroku login

# 2. Create Heroku app
heroku create my-python-app
# Or use existing app:
# heroku git:remote -a my-python-app

# 3. Navigate to project
cd 01_task_management_saas

# 4. Create Procfile (if not exists)
cat > Procfile << 'EOF'
web: gunicorn -w 4 -b 0.0.0.0:$PORT main:app
EOF

# 5. Create runtime.txt (if not exists)
echo "python-3.11.6" > runtime.txt

# 6. Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=false
heroku config:set DATABASE_URL=postgresql://...

# 7. Add database add-on (optional)
heroku addons:create heroku-postgresql:standard-0

# 8. Add redis add-on (optional)
heroku addons:create heroku-redis:premium-0

# 9. Deploy
git push heroku main
# or for different branch:
# git push heroku feature-branch:main

# 10. Run migrations
heroku run python -m app.core.database

# 11. Check logs
heroku logs --tail

# 12. Monitor
heroku monitoring:dashboards open

# 13. Scale dynos
heroku ps:scale web=2

# 14. Access app
heroku open

# 15. Access console
heroku run bash
```

### Procfile Examples

**FastAPI**:
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT main:app
```

**Django**:
```
web: gunicorn project.wsgi --log-file -
release: python manage.py migrate
```

**With Workers**:
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT main:app
worker: celery -A app.celery worker
```

---

## DigitalOcean Deployment

### Option 1: DigitalOcean App Platform (Simplest)

```bash
# 1. Create app.yaml
cat > app.yaml << 'EOF'
name: python-app
services:
- name: web
  github:
    repo: your-username/your-repo
    branch: main
  build_command: pip install -r requirements.txt
  run_command: gunicorn -w 4 -b 0.0.0.0:$PORT main:app
  http_port: 8000
  envs:
  - key: SECRET_KEY
    value: ${SECRET_KEY}
  - key: DATABASE_URL
    value: ${DATABASE_URL}
databases:
- name: db
  engine: PG
  version: "15"
- name: cache
  engine: REDIS
  version: "7"
EOF

# 2. Deploy via CLI
doctl apps create --spec app.yaml

# 3. Or deploy via web console
# https://cloud.digitalocean.com/apps
```

### Option 2: DigitalOcean Droplet (VPS)

```bash
# 1. Create Droplet
# - Size: $5/month (Basic) to $40/month (Standard)
# - OS: Ubuntu 22.04
# - Region: Choose closest to you
# - SSH Key: Add your public key

# 2. SSH into droplet
ssh root@your-droplet-ip

# 3. Update system
apt update && apt upgrade -y

# 4. Install dependencies
apt install -y python3.11 python3.11-venv python3.11-dev
apt install -y postgresql postgresql-contrib
apt install -y redis-server
apt install -y nginx
apt install -y git

# 5. Clone repository
cd /var/www
git clone <repository-url>
cd 01_task_management_saas

# 6. Setup Python environment
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# 7. Setup PostgreSQL database
sudo -u postgres createdb appdb
sudo -u postgres createuser appuser
sudo -u postgres psql -c "ALTER USER appuser WITH PASSWORD 'password';"

# 8. Create .env file
cp .env.example .env.local
nano .env.local

# 9. Setup systemd service (same as AWS EC2)
# See AWS EC2 instructions above

# 10. Setup nginx reverse proxy
nano /etc/nginx/sites-available/python-app
```

Nginx configuration:

```nginx
upstream python_app {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://python_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/01_task_management_saas/static/;
    }
}
```

```bash
# 11. Enable site
ln -s /etc/nginx/sites-available/python-app /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx

# 12. Setup SSL with Let's Encrypt
apt install certbot python3-certbot-nginx -y
certbot --nginx -d your-domain.com
```

---

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (EKS, GKE, AKS, or local)
- kubectl installed
- Docker image built and pushed to registry

### Deployment Steps

```bash
# 1. Create Docker image
docker build -t your-registry/python-app:latest .
docker push your-registry/python-app:latest

# 2. Create namespace
kubectl create namespace production

# 3. Create secret for environment variables
kubectl create secret generic app-secrets \
  --from-literal=SECRET_KEY=your-secret-key \
  --from-literal=DATABASE_URL=postgresql://... \
  -n production

# 4. Create ConfigMap for configuration
kubectl create configmap app-config \
  --from-literal=LOG_LEVEL=INFO \
  --from-literal=WORKERS=4 \
  -n production

# 5. Create deployment
cat > k8s-deployment.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: python-app
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: python-app
  template:
    metadata:
      labels:
        app: python-app
    spec:
      containers:
      - name: app
        image: your-registry/python-app:latest
        ports:
        - containerPort: 8000
        env:
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: SECRET_KEY
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: DATABASE_URL
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: LOG_LEVEL
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
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
EOF

kubectl apply -f k8s-deployment.yaml

# 6. Create service
cat > k8s-service.yaml << 'EOF'
apiVersion: v1
kind: Service
metadata:
  name: python-app-service
  namespace: production
spec:
  type: LoadBalancer
  selector:
    app: python-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
EOF

kubectl apply -f k8s-service.yaml

# 7. Create ingress (for domain routing)
cat > k8s-ingress.yaml << 'EOF'
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: python-app-ingress
  namespace: production
spec:
  rules:
  - host: your-domain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: python-app-service
            port:
              number: 80
EOF

kubectl apply -f k8s-ingress.yaml

# 8. Monitor deployment
kubectl get pods -n production
kubectl logs -n production deployment/python-app
kubectl describe pod -n production <pod-name>

# 9. Scale deployment
kubectl scale deployment python-app --replicas=5 -n production

# 10. Update deployment
docker build -t your-registry/python-app:v1.1 .
docker push your-registry/python-app:v1.1
kubectl set image deployment/python-app \
  app=your-registry/python-app:v1.1 \
  -n production

# 11. View rollout status
kubectl rollout status deployment/python-app -n production

# 12. Rollback if needed
kubectl rollout undo deployment/python-app -n production
```

---

## Environment Configuration

### Environment Variables by Platform

**Docker Compose**:
```bash
# .env.local
DATABASE_URL=postgresql://user:password@db:5432/appdb
REDIS_URL=redis://redis:6379
SECRET_KEY=your-secret-key
DEBUG=false
```

**AWS Elastic Beanstalk**:
```bash
eb setenv \
  DATABASE_URL="postgresql://user:password@rds.amazonaws.com:5432/db" \
  REDIS_URL="redis://elasticache.amazonaws.com:6379" \
  SECRET_KEY="your-secret-key"
```

**Heroku**:
```bash
heroku config:set \
  DATABASE_URL="postgresql://..." \
  REDIS_URL="redis://..." \
  SECRET_KEY="your-secret-key"
```

**DigitalOcean App Platform**:
```yaml
envs:
  - key: DATABASE_URL
    value: ${DB_CONNECTION_STRING}
  - key: REDIS_URL
    value: ${REDIS_CONNECTION_STRING}
  - key: SECRET_KEY
    value: your-secret-key
```

---

## Monitoring & Logging

### Application Monitoring

```python
# Add to your FastAPI application
from fastapi import FastAPI
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": os.getenv("APP_ENV", "development")
    }

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    # Implement metrics collection
    return {}
```

### Logging

```bash
# Docker Compose
docker-compose logs -f app

# Heroku
heroku logs --tail

# AWS Elastic Beanstalk
eb logs

# Kubernetes
kubectl logs -n production deployment/python-app
kubectl logs -n production deployment/python-app --previous  # Previous instance

# DigitalOcean
# Access through web console
```

### Error Tracking

```python
# Add Sentry for error tracking
import sentry_sdk

sentry_sdk.init(
    dsn="https://your-sentry-dsn@sentry.io/project-id",
    traces_sample_rate=1.0,
    environment="production"
)
```

---

## Security Best Practices

### Pre-Deployment Checklist

- [ ] Change all default secrets
- [ ] Set `DEBUG=false` in production
- [ ] Use HTTPS (SSL/TLS)
- [ ] Configure CORS properly
- [ ] Set up firewall rules
- [ ] Enable database encryption
- [ ] Regular backups enabled
- [ ] Update dependencies
- [ ] Security headers configured
- [ ] Rate limiting enabled

### Environment Variables

```bash
# DO NOT commit these to git
SECRET_KEY=truly-random-secret-key-here-min-32-chars
DATABASE_URL=postgresql://user:password@host:5432/db
REDIS_URL=redis://host:6379/0
DEBUG=false
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### HTTPS Setup

```bash
# Let's Encrypt (Free)
sudo certbot certonly --standalone -d yourdomain.com

# AWS Certificate Manager
# Use with ALB/CloudFront

# Heroku (Automatic)
heroku certs:add <path-to-cert> <path-to-key>
```

### Database Security

```bash
# Strong password for database user
ALTER USER dbuser WITH PASSWORD 'very-strong-password-min-32-chars';

# Restrict network access
# - Allow only app servers
# - Use security groups / firewall rules

# Enable encryption at rest
# - RDS: Enable KMS encryption
# - PostgreSQL: pgcrypto extension

# Regular backups
# - Set retention period (7-30 days)
# - Test restore process
```

---

## Troubleshooting

### Common Issues

**Issue**: Application crashes on startup

```bash
# Check logs
docker-compose logs app
# or
heroku logs --tail

# Verify environment variables
docker-compose exec app env | grep DATABASE_URL

# Test database connection
psql $DATABASE_URL -c "SELECT 1"
```

**Issue**: 502 Bad Gateway

```bash
# Check if app is running
docker-compose ps

# Check app logs
docker-compose logs app

# Verify port is correct
netstat -tuln | grep 8000

# Check database connectivity
```

**Issue**: Database migration fails

```bash
# Run migrations manually
docker-compose exec app python -m app.core.database

# Check migration files
ls app/migrations/

# Reset database (development only)
docker-compose down -v
docker-compose up -d
```

**Issue**: Redis connection timeout

```bash
# Check Redis is running
redis-cli ping

# Check Redis configuration
redis-cli config get "*"

# Clear Redis cache
redis-cli FLUSHALL
```

---

## Deployment Checklist

Before deploying to production:

- [ ] All tests passing locally
- [ ] Code reviewed
- [ ] Security scan passed (bandit, safety)
- [ ] Database backups configured
- [ ] Monitoring set up
- [ ] Logging configured
- [ ] SSL certificate installed
- [ ] Environment variables set
- [ ] Load testing performed
- [ ] Disaster recovery plan documented
- [ ] Team trained on deployment process
- [ ] Rollback procedure tested

---

## Post-Deployment

### First 24 Hours

1. Monitor error rates
2. Check application logs
3. Verify database backups
4. Test all critical features
5. Monitor performance metrics

### Ongoing

1. Weekly security patches
2. Monthly backup testing
3. Quarterly disaster recovery drill
4. Regular performance optimization
5. Dependency updates

---

## Additional Resources

- [AWS Elastic Beanstalk Docs](https://docs.aws.amazon.com/elasticbeanstalk/)
- [Heroku Deployment Docs](https://devcenter.heroku.com/)
- [DigitalOcean Tutorials](https://docs.digitalocean.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

---

**Ready to deploy! 🚀**
