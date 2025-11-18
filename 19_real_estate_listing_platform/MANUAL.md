# 19_real_estate_listing_platform - Complete Setup & Deployment Guide

## Overview

This is a production-ready FastAPI application with comprehensive error handling, structured logging, and containerization support.

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 13+ (or SQLite for development)
- Docker & Docker Compose (optional)

### Local Setup

1. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Run Application**
   ```bash
   uvicorn main:app --reload
   ```

Visit: `http://localhost:8000`
- Swagger Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Configuration

### Environment Variables

**Database**
```env
DATABASE_URL=sqlite:///./app.db
# Or PostgreSQL: postgresql://user:password@localhost/dbname
```

**Security**
```env
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Server**
```env
HOST=0.0.0.0
PORT=8000
DEBUG=false
ENVIRONMENT=production
LOG_LEVEL=INFO
```

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI Schema: `http://localhost:8000/openapi.json`

## Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=app --cov-report=html
```

## Docker Deployment

### Build & Run

```bash
# Build image
docker build -t 19_real_estate_listing_platform:latest .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL="sqlite:///./app.db" \
  -e SECRET_KEY="your-secret-key" \
  19_real_estate_listing_platform:latest

# Using Docker Compose
docker-compose up
```

## Production Deployment

### Systemd Service Setup

1. **Create Service File** (`/etc/systemd/system/19_real_estate_listing_platform.service`)
   ```ini
   [Unit]
   Description=19_real_estate_listing_platform
   After=network.target

   [Service]
   Type=notify
   User=www-data
   WorkingDirectory=/var/www/19_real_estate_listing_platform
   Environment="PATH=/var/www/19_real_estate_listing_platform/venv/bin"
   ExecStart=/var/www/19_real_estate_listing_platform/venv/bin/gunicorn main:app \
       --workers 4 \
       --worker-class uvicorn.workers.UvicornWorker \
       --bind 127.0.0.1:8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

2. **Enable & Start**
   ```bash
   sudo systemctl enable 19_real_estate_listing_platform
   sudo systemctl start 19_real_estate_listing_platform
   sudo systemctl status 19_real_estate_listing_platform
   ```

### Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Database Management

### Migrations (Alembic)

```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Monitoring & Logs

### Structured Logging

All requests are logged in JSON format with correlation IDs:

```json
{
    "timestamp": "2024-01-15T10:30:00.000000",
    "level": "INFO",
    "logger": "application",
    "message": "Request completed",
    "request_id": "550e8400-e29b-41d4-a716-446655440000",
    "duration_ms": 145.23
}
```

### Health Checks

```bash
curl http://localhost:8000/health
```

## Troubleshooting

### Port Already in Use
```bash
lsof -ti:8000 | xargs kill -9
# Or use different port
uvicorn main:app --port 8001
```

### Database Connection Error
- Verify DATABASE_URL in .env
- Check database credentials
- Ensure database service is running

### CORS Errors
Update CORS_ORIGINS in config.py with your frontend URL.

### Module Not Found
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Project Structure

```
19_real_estate_listing_platform/
├── main.py                 # Application entry point
├── config.py               # Configuration management
├── requirements.txt        # Dependencies
├── .env.example           # Environment template
├── Dockerfile             # Docker image
├── docker-compose.yml     # Docker composition
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── errors.py      # Error handling
│   │   ├── logging.py     # Structured logging
│   │   ├── middleware.py  # Custom middleware
│   │   └── database.py    # Database setup
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   ├── routes/            # API routes
│   ├── services/          # Business logic
│   └── utils/
│       └── validation.py  # Input validation
├── tests/
│   ├── __init__.py
│   ├── conftest.py        # Pytest configuration
│   └── test_*.py          # Test files
├── MANUAL.md              # This file
└── README.md              # Project overview
```

## Production Checklist

- [ ] Set DEBUG=false
- [ ] Generate strong SECRET_KEY
- [ ] Configure production database (PostgreSQL)
- [ ] Set ENVIRONMENT=production
- [ ] Update CORS_ORIGINS
- [ ] Enable HTTPS/SSL
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Review security headers

## Common Commands

```bash
# Development
uvicorn main:app --reload

# Production
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker

# Testing
pytest -v
pytest --cov=app

# Docker
docker build -t 19_real_estate_listing_platform:latest .
docker run -p 8000:8000 19_real_estate_listing_platform:latest
docker-compose up

# Database
alembic revision --autogenerate -m "message"
alembic upgrade head

# Git
git add .
git commit -m "message"
git push origin main
```

## Support

- FastAPI Docs: https://fastapi.tiangolo.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Pydantic: https://docs.pydantic.dev/

---
**Last Updated:** 2024-01-15
**Version:** 1.0.0
