# Compensation Analyzer - Quick Setup Guide

## Quick Start

1. **Setup Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Application**
   ```bash
   uvicorn main:app --reload
   ```

4. **Access API**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs

## Configuration

See `.env.example` for environment variables.

## Testing

```bash
pytest
```

## Docker

```bash
docker-compose up
```

## Production

See PRODUCTION_ENHANCEMENT_GUIDE.md for complete deployment instructions.
