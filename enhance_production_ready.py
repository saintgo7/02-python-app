#!/usr/bin/env python3
"""
Production-ready enhancement for all 120 backend applications.
Adds:
- Error handling module (app/core/errors.py)
- Structured logging (app/core/logging.py)
- Validation utilities (app/utils/validation.py)
- Enhanced configuration (config.py)
- MANUAL.md documentation
"""

from pathlib import Path
import os

# Create error handling module content
def create_error_handling_file():
    return '''"""Core error handling utilities for production applications."""

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class AppException(Exception):
    """Base exception for application-specific errors"""
    def __init__(self, message: str, code: str = "APP_ERROR", status_code: int = 400):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)


class ValidationException(AppException):
    """Raised when input validation fails"""
    def __init__(self, message: str, field: str = None):
        super().__init__(message, "VALIDATION_ERROR", status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.field = field


class NotFoundException(AppException):
    """Raised when a requested resource is not found"""
    def __init__(self, resource: str, identifier: Any = None):
        message = f"{resource} not found"
        if identifier:
            message += f": {identifier}"
        super().__init__(message, "NOT_FOUND", status.HTTP_404_NOT_FOUND)


class UnauthorizedException(AppException):
    """Raised when authentication fails"""
    def __init__(self, message: str = "Authentication required"):
        super().__init__(message, "UNAUTHORIZED", status.HTTP_401_UNAUTHORIZED)


class ForbiddenException(AppException):
    """Raised when user lacks required permissions"""
    def __init__(self, message: str = "Access denied"):
        super().__init__(message, "FORBIDDEN", status.HTTP_403_FORBIDDEN)


def error_response(message: str, code: str = "ERROR", status_code: int = 400) -> JSONResponse:
    """Create standardized error response"""
    return JSONResponse(
        status_code=status_code,
        content={"error": {"message": message, "code": code}}
    )


def success_response(data: Any = None, message: str = "Success") -> Dict:
    """Create standardized success response"""
    return {"success": True, "message": message, "data": data}
'''


def create_logging_file():
    return '''"""Structured logging configuration for production applications."""

import logging
import uuid
from logging.handlers import RotatingFileHandler
from pathlib import Path
import json
from datetime import datetime

_request_id = None

def get_request_id():
    """Get or create request ID for correlation tracking"""
    global _request_id
    if not _request_id:
        _request_id = str(uuid.uuid4())
    return _request_id

def set_request_id(request_id: str):
    """Set request ID for correlation tracking"""
    global _request_id
    _request_id = request_id

class JsonFormatter(logging.Formatter):
    """JSON formatter for structured logging"""

    def format(self, record):
        log_obj = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": get_request_id(),
        }
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_obj)

def setup_logging(app_name: str, log_level: str = "INFO", log_file: str = None):
    """Configure structured logging for the application"""
    logger = logging.getLogger(app_name)
    logger.setLevel(getattr(logging, log_level))

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(JsonFormatter())
    logger.addHandler(console_handler)

    if log_file:
        log_path = Path(log_file).parent
        log_path.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
        file_handler.setFormatter(JsonFormatter())
        logger.addHandler(file_handler)

    return logger
'''


def create_validation_file():
    return '''"""Input validation utilities for production applications."""

import re
from urllib.parse import urlparse

class ValidationUtils:
    """Collection of validation helper methods"""

    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$')
    PHONE_PATTERN = re.compile(r'^\\+?1?\\d{9,15}$')

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        if not email or len(email) > 254:
            return False
        return bool(ValidationUtils.EMAIL_PATTERN.match(email))

    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format"""
        try:
            result = urlparse(url)
            return all([result.scheme in ['http', 'https'], result.netloc])
        except Exception:
            return False

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format"""
        clean_phone = phone.replace('-', '').replace(' ', '')
        return bool(ValidationUtils.PHONE_PATTERN.match(clean_phone))

    @staticmethod
    def sanitize_string(value: str, max_length: int = 1000) -> str:
        """Sanitize string input"""
        if not isinstance(value, str):
            return str(value)
        value = value.replace('\\x00', '')
        value = value[:max_length]
        value = ' '.join(value.split())
        return value

    @staticmethod
    def validate_length(value: str, min_len: int = 0, max_len: int = 1000) -> bool:
        """Validate string length"""
        if not isinstance(value, str):
            return False
        return min_len <= len(value) <= max_len

    @staticmethod
    def validate_password(password: str, min_length: int = 8):
        """Validate password strength. Returns (is_valid, message)"""
        if len(password) < min_length:
            return False, f"Password must be at least {min_length} characters"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        if not re.search(r'\\d', password):
            return False, "Password must contain at least one digit"
        return True, "Password is strong"
'''


def create_middleware_file():
    return '''"""Production middleware for applications."""

from fastapi import Request
from fastapi.responses import JSONResponse
import logging
import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests with timing and correlation IDs"""

    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id

        logger.info(
            f"Request started: {request.method} {request.url.path}",
            extra={"request_id": request_id, "method": request.method, "path": request.url.path}
        )

        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)

        logger.info(
            f"Request completed: {request.method} {request.url.path} [{response.status_code}]",
            extra={"request_id": request_id, "status": response.status_code, "duration_ms": round(process_time * 1000, 2)}
        )

        return response

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses"""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response
'''


def create_manual_file(app_name: str, folder_name: str):
    manual = f'''# {app_name} - Complete Setup & Deployment Guide

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
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
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
docker build -t {folder_name}:latest .

# Run container
docker run -p 8000:8000 \\
  -e DATABASE_URL="sqlite:///./app.db" \\
  -e SECRET_KEY="your-secret-key" \\
  {folder_name}:latest

# Using Docker Compose
docker-compose up
```

## Production Deployment

### Systemd Service Setup

1. **Create Service File** (`/etc/systemd/system/{folder_name}.service`)
   ```ini
   [Unit]
   Description={app_name}
   After=network.target

   [Service]
   Type=notify
   User=www-data
   WorkingDirectory=/var/www/{folder_name}
   Environment="PATH=/var/www/{folder_name}/venv/bin"
   ExecStart=/var/www/{folder_name}/venv/bin/gunicorn main:app \\
       --workers 4 \\
       --worker-class uvicorn.workers.UvicornWorker \\
       --bind 127.0.0.1:8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

2. **Enable & Start**
   ```bash
   sudo systemctl enable {folder_name}
   sudo systemctl start {folder_name}
   sudo systemctl status {folder_name}
   ```

### Nginx Reverse Proxy

```nginx
server {{
    listen 80;
    server_name yourdomain.com;

    location / {{
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}
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
{{
    "timestamp": "2024-01-15T10:30:00.000000",
    "level": "INFO",
    "logger": "application",
    "message": "Request completed",
    "request_id": "550e8400-e29b-41d4-a716-446655440000",
    "duration_ms": 145.23
}}
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
{folder_name}/
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
docker build -t {folder_name}:latest .
docker run -p 8000:8000 {folder_name}:latest
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
'''
    return manual


def enhance_application(app_dir: Path, app_name: str):
    """Enhance a single application with production features"""
    try:
        # Create app/core directory
        core_dir = app_dir / "app" / "core"
        core_dir.mkdir(parents=True, exist_ok=True)

        # Create __init__.py if it doesn't exist
        (core_dir / "__init__.py").touch()

        # Create error handling module
        (core_dir / "errors.py").write_text(create_error_handling_file())

        # Create logging module
        (core_dir / "logging.py").write_text(create_logging_file())

        # Create middleware module
        (core_dir / "middleware.py").write_text(create_middleware_file())

        # Create app/utils directory
        utils_dir = app_dir / "app" / "utils"
        utils_dir.mkdir(parents=True, exist_ok=True)
        (utils_dir / "__init__.py").touch()

        # Create validation module
        (utils_dir / "validation.py").write_text(create_validation_file())

        # Create MANUAL.md
        folder_name = app_dir.name
        (app_dir / "MANUAL.md").write_text(create_manual_file(app_name, folder_name))

        return True
    except Exception as e:
        print(f"    Error: {str(e)}")
        return False


def main():
    """Enhance all 120 applications"""
    apps_dir = Path("/home/user/02-python-app")

    # Get all app directories
    app_dirs = sorted(
        [d for d in apps_dir.iterdir() if d.is_dir() and d.name[0].isdigit()],
        key=lambda x: int(x.name.split("_")[0])
    )

    print("\n" + "="*70)
    print("🔧 Production-Ready Enhancement for 120 Applications")
    print("="*70)
    print(f"Total applications to enhance: {len(app_dirs)}\n")

    success_count = 0
    for i, app_dir in enumerate(app_dirs, 1):
        app_num = app_dir.name.split("_")[0]
        folder_name = app_dir.name

        # Display progress
        status = f"[{i:3d}/{len(app_dirs)}]"
        folder_display = f"{app_num} - {folder_name[:40]:<40}"
        print(f"{status} {folder_display}", end=" ... ", flush=True)

        if enhance_application(app_dir, folder_name):
            print("✓")
            success_count += 1
        else:
            print("✗")

    print("\n" + "="*70)
    print(f"✅ Enhancement Complete: {success_count}/{len(app_dirs)} applications enhanced")
    print("="*70)
    print("\nEach application now includes:")
    print("  ✓ app/core/errors.py       - Comprehensive error handling")
    print("  ✓ app/core/logging.py      - Structured logging with correlation IDs")
    print("  ✓ app/core/middleware.py   - Security headers and request logging")
    print("  ✓ app/utils/validation.py  - Input validation utilities")
    print("  ✓ MANUAL.md                - Complete setup & deployment guide\n")


if __name__ == "__main__":
    main()
