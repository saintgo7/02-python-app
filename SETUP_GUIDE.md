# 🚀 Complete Setup Guide

Comprehensive guide to set up and run any application in this ecosystem.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Individual Project Setup](#individual-project-setup)
4. [Docker Setup](#docker-setup)
5. [Frontend Setup](#frontend-setup)
6. [Development Tools](#development-tools)
7. [Database Setup](#database-setup)
8. [Environment Variables](#environment-variables)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

- **Operating System**: Linux, macOS, or Windows (with WSL2)
- **Python**: 3.11 or higher
- **Node.js**: 18 or higher (for frontend)
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: 20GB minimum

### Required Software

Install the following tools:

#### Python

```bash
# macOS (Homebrew)
brew install python@3.11

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv python3.11-dev

# Windows
# Download from https://www.python.org/downloads/

# Verify installation
python --version  # Should be 3.11+
```

#### Node.js

```bash
# macOS (Homebrew)
brew install node

# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Windows
# Download from https://nodejs.org/

# Verify installation
node --version   # Should be 18+
npm --version    # Should be 9+
```

#### Docker & Docker Compose

```bash
# macOS
brew install docker

# Ubuntu/Debian
sudo apt-get install docker.io docker-compose

# Windows
# Download Docker Desktop from https://www.docker.com/products/docker-desktop

# Verify installation
docker --version
docker-compose --version
```

#### Git

```bash
# macOS (Homebrew)
brew install git

# Ubuntu/Debian
sudo apt-get install git

# Windows
# Download from https://git-scm.com/

# Verify installation
git --version
```

#### PostgreSQL (Optional, for production)

```bash
# macOS (Homebrew)
brew install postgresql

# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# Windows
# Download from https://www.postgresql.org/download/windows/

# Verify installation
psql --version
```

#### Redis (Optional, for caching)

```bash
# macOS (Homebrew)
brew install redis

# Ubuntu/Debian
sudo apt-get install redis-server

# Windows (WSL2)
wsl --install
# Then run Ubuntu/Debian commands above

# Verify installation
redis-cli --version
```

---

## Quick Start

### For FastAPI Projects (01-10)

```bash
# Clone the repository
git clone <repository-url>
cd 02-python-app

# Navigate to project
cd 01_task_management_saas

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env.local

# Initialize database (if needed)
# python -m app.core.database

# Run the application
python main.py

# Open browser
# API: http://localhost:8000
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

### For Django Projects (11-20)

```bash
# Navigate to project
cd 11_multi_tenant_crm

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env.local

# Create database
python manage.py migrate

# Create superuser (optional)
# python manage.py createsuperuser

# Run the application
python manage.py runserver

# Open browser
# API: http://localhost:8000
# Admin: http://localhost:8000/admin
```

### For AI/ML Projects (21-40)

```bash
# Navigate to project
cd 21_object_detection_api

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies (might take longer due to ML libraries)
pip install -r requirements.txt

# Create environment file
cp .env.example .env.local

# Run the application
python main.py

# Open browser
# API: http://localhost:8000/docs
```

---

## Individual Project Setup

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd 02-python-app
```

### Step 2: Select Project

Choose any project from:
- **FastAPI**: 01-10
- **Django**: 11-20
- **PyTorch**: 21-30
- **TensorFlow**: 31-40
- **Monetization Tools**: 41-60

```bash
cd <project-name>
```

### Step 3: Create Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows

# Upgrade pip
pip install --upgrade pip
```

### Step 4: Install Dependencies

```bash
# Install from requirements.txt
pip install -r requirements.txt

# For development (includes testing tools)
pip install -r requirements.txt pytest pytest-cov black flake8 mypy
```

### Step 5: Configure Environment

```bash
# Copy example environment file
cp .env.example .env.local

# Edit with your settings
nano .env.local  # or use your preferred editor
```

### Step 6: Setup Database

#### For FastAPI/SQLAlchemy:

```bash
# The database is usually auto-initialized, but you can also:
python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

#### For Django:

```bash
# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### Step 7: Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py -v

# Run specific test
pytest tests/test_auth.py::test_login -v
```

### Step 8: Start Development Server

#### FastAPI:

```bash
python main.py
# or
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Django:

```bash
python manage.py runserver
# or for all interfaces
python manage.py runserver 0.0.0.0:8000
```

### Step 9: Access Application

- **API Endpoints**: http://localhost:8000
- **Swagger UI (FastAPI)**: http://localhost:8000/docs
- **ReDoc (FastAPI)**: http://localhost:8000/redoc
- **Admin Panel (Django)**: http://localhost:8000/admin

---

## Docker Setup

### Quick Start with Docker Compose

```bash
# Navigate to project
cd 01_task_management_saas

# Build and run containers
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

### Build Docker Image Manually

```bash
# Build image
docker build -t my-app:latest .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL="sqlite:///./test.db" \
  my-app:latest

# Or with environment file
docker run -p 8000:8000 \
  --env-file .env.local \
  my-app:latest
```

### Docker Compose with Multiple Services

```bash
# Create docker-compose.yml
cat > docker-compose.override.yml << 'EOF'
version: '3.8'

services:
  app:
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/appdb
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=appdb
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
EOF

# Start services
docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d

# Stop services
docker-compose down
```

### Docker Networking

```bash
# Check running containers
docker ps

# View container logs
docker logs <container-id>

# Execute command in container
docker exec -it <container-id> bash

# Access database in container
docker exec -it <container-name> psql -U user -d database
```

---

## Frontend Setup

### React Frontend (For FastAPI Projects)

```bash
# Navigate to frontend
cd frontend/react-app

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Edit configuration
nano .env.local

# Start development server
npm start

# Open browser
# http://localhost:3000
```

### Vue Frontend (For Django Projects)

```bash
# Navigate to frontend
cd frontend/vue-app

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Edit configuration
nano .env.local

# Start development server
npm run dev

# Open browser
# http://localhost:5173 (or as shown in terminal)
```

### Building for Production

#### React:

```bash
npm run build
# Output: build/ directory
```

#### Vue:

```bash
npm run build
# Output: dist/ directory
```

---

## Development Tools

### Code Formatting

```bash
# Format code with Black
black .

# Format specific file
black app/main.py
```

### Linting

```bash
# Check code style with Flake8
flake8 .

# Fix issues automatically (where possible)
autopep8 --in-place --aggressive -r .

# Check import ordering
isort --check-only .

# Fix import ordering
isort .
```

### Type Checking

```bash
# Check types with mypy
mypy .

# Check specific file
mypy app/main.py

# Strict mode
mypy --strict .
```

### Testing

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=app

# Generate coverage report
pytest --cov=app --cov-report=html
# Open htmlcov/index.html

# Run specific test
pytest tests/test_auth.py::test_login

# Run tests matching pattern
pytest -k "test_user"

# Stop at first failure
pytest -x

# Run last failed
pytest --lf

# Show print statements
pytest -s
```

### Security Scanning

```bash
# Check for common security issues
bandit -r app/

# Check dependencies for vulnerabilities
safety check

# Scan requirements.txt
safety check -r requirements.txt
```

### Database Migrations

#### FastAPI (Alembic):

```bash
# Create migration
alembic revision --autogenerate -m "Add new column"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# View migration history
alembic history
```

#### Django:

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration plan
python manage.py sqlmigrate app 0001

# Rollback migrations
python manage.py migrate app 0001
```

---

## Database Setup

### PostgreSQL (Production Database)

#### Installation

```bash
# macOS
brew install postgresql

# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# Windows
# Download installer from https://www.postgresql.org/download/windows/
```

#### Configuration

```bash
# Create database
createdb myapp

# Create user
createuser myappuser

# Set password
psql -c "ALTER USER myappuser WITH PASSWORD 'password';"

# Grant privileges
psql -c "GRANT ALL PRIVILEGES ON DATABASE myapp TO myappuser;"
```

#### Environment Configuration

```bash
# .env.local
DATABASE_URL=postgresql://myappuser:password@localhost:5432/myapp
```

### SQLite (Development Database)

SQLite is automatically created when you run the application.

```bash
# Create explicitly
sqlite3 app.db ".databases"

# Backup
cp app.db app.db.backup

# Reset (delete file and restart app)
rm app.db
# Restart application
```

### Redis (Caching)

#### Installation

```bash
# macOS
brew install redis

# Ubuntu/Debian
sudo apt-get install redis-server

# Start service
redis-server

# Or as daemon
redis-server --daemonize yes
```

#### Testing Connection

```bash
# Connect to Redis
redis-cli

# Test connection
ping
# Should return: PONG

# View keys
keys *

# Get value
get <key>

# Exit
exit
```

#### Docker Redis

```bash
docker run -d \
  --name redis \
  -p 6379:6379 \
  redis:7-alpine
```

---

## Environment Variables

### Common Environment Variables

```bash
# Application
APP_NAME="My App"
APP_ENV=development  # development, staging, production
DEBUG=true

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
# Or for SQLite
DATABASE_URL=sqlite:///./app.db

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]

# Email (if needed)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-password

# AWS (if using AWS)
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_REGION=us-east-1

# API Keys (if needed)
API_KEY=your-api-key
```

### Example .env.local

```bash
# Copy from .env.example
cp .env.example .env.local

# Edit with your values
EDITOR=nano .env.local
```

---

## Troubleshooting

### Python Issues

**Issue**: `command not found: python`

```bash
# Check Python path
which python3
which python

# Create alias if needed
alias python=python3
```

**Issue**: `ModuleNotFoundError: No module named 'app'`

```bash
# Make sure you're in the project root directory
cd /path/to/project

# Reinstall dependencies
pip install -r requirements.txt

# Check Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**Issue**: Virtual environment not activating

```bash
# Delete and recreate
rm -rf venv/
python -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
```

### Database Issues

**Issue**: `sqlite3.OperationalError: unable to open database file`

```bash
# Check directory permissions
ls -la

# Create data directory if needed
mkdir -p data

# Set correct permissions
chmod 755 data
```

**Issue**: `psycopg2.OperationalError: FATAL: Ident authentication failed`

```bash
# Check PostgreSQL is running
psql -U postgres

# Update DATABASE_URL
DATABASE_URL=postgresql://postgres:password@localhost:5432/dbname
```

**Issue**: `Redis connection refused`

```bash
# Check if Redis is running
redis-cli ping

# Start Redis
redis-server

# Or with Homebrew
brew services start redis
```

### Docker Issues

**Issue**: `Port 8000 is already in use`

```bash
# Find process using port
lsof -i :8000
# or for Windows
netstat -ano | findstr :8000

# Kill process
kill -9 <PID>
# or for Windows
taskkill /PID <PID> /F
```

**Issue**: `Cannot connect to Docker daemon`

```bash
# Start Docker daemon
# macOS: Start Docker Desktop app
# Linux: sudo systemctl start docker
# Windows: Start Docker Desktop app
```

**Issue**: `Failed to build docker image`

```bash
# Clear Docker cache
docker builder prune

# Build with no cache
docker build --no-cache -t myapp .
```

### Frontend Issues

**Issue**: `npm ERR! code EACCES: permission denied`

```bash
# Fix npm permissions
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH

# Or use nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm use 18
```

**Issue**: `Port 3000 is already in use`

```bash
# Use different port
PORT=3001 npm start
```

**Issue**: `CORS error when connecting to backend`

```bash
# Make sure backend CORS is configured
# Check .env.local has correct CORS_ORIGINS
CORS_ORIGINS=["http://localhost:3000"]

# Restart backend
```

### Dependency Issues

**Issue**: `pip install takes too long`

```bash
# Use a specific PyPI mirror
pip install -i https://pypi.tsinghua.edu.cn/simple -r requirements.txt

# Or upgrade pip
pip install --upgrade pip
```

**Issue**: `SSL certificate errors`

```bash
# Disable SSL verification (not recommended for production)
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Or fix SSL
# macOS: /Applications/Python\ 3.11/Install\ Certificates.command
```

**Issue**: Conflicting package versions

```bash
# Create fresh virtual environment
rm -rf venv/
python -m venv venv
source venv/bin/activate

# Reinstall with specific versions
pip install -r requirements.txt --force-reinstall
```

### Performance Issues

**Issue**: Slow application startup

```bash
# Profile startup
python -m cProfile -s cumulative main.py

# Check for large dependencies
pip show <package>

# Check import times
python -X importtime main.py 2>&1 | head -50
```

**Issue**: High memory usage

```bash
# Monitor memory
top  # macOS/Linux
# or
tasklist  # Windows

# Check for memory leaks
pip install memory-profiler
python -m memory_profiler main.py
```

---

## Getting Help

If you encounter issues:

1. **Check documentation**: See README.md in project directory
2. **Check logs**: Review error messages carefully
3. **Search issues**: Look for similar problems online
4. **Ask for help**: Create GitHub issue with:
   - Error message (full traceback)
   - Steps to reproduce
   - System information (OS, Python version, etc.)
   - What you've already tried

---

## Next Steps

After successful setup:

1. **Explore the codebase**: Understand the project structure
2. **Read the API documentation**: Visit `/docs` endpoint
3. **Run the tests**: Verify everything works
4. **Try the frontend**: If available, test the UI
5. **Customize**: Modify for your needs
6. **Deploy**: Follow deployment guides

---

**Happy coding! 🚀**
