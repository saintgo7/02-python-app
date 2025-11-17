# Document Management System

## Description

Enterprise document storage with full-text search, versioning, and access control

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL / SQLite
- **Cache**: Redis
- **Authentication**: JWT
- **Testing**: Pytest

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env.local

# Run application
python main.py

# Access API
# Swagger: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

## Features

- JWT Authentication
- SQLAlchemy ORM
- Redis Caching
- Comprehensive API Documentation
- Docker Support
- Full Test Coverage

## Project Structure

```
Document Management System/
├── main.py
├── app/
│   ├── models/
│   ├── schemas/
│   ├── routes/
│   └── services/
├── tests/
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## API Documentation

Swagger UI available at: http://localhost:8000/docs
ReDoc available at: http://localhost:8000/redoc

## Testing

```bash
pytest
pytest --cov=app
```

## License

MIT
