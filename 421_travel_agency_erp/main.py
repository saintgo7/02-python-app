#!/usr/bin/env python3
"""
Travel Agency ERP System
Production-ready FastAPI application for travel agency management
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import engine, Base
from app.core.logging import setup_logging
from app.config import get_settings
from app.routes import auth, packages, bookings, payments, analytics

# Setup logging
logger = setup_logging(__name__)
settings = get_settings()

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title="Travel Agency ERP System",
    version="1.0.0",
    description="Comprehensive ERP system for travel agencies with booking, payment, and analytics",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Include routers
app.include_router(auth.router)
app.include_router(packages.router)
app.include_router(bookings.router)
app.include_router(payments.router)
app.include_router(analytics.router)


@app.get("/")
async def read_root():
    """Root endpoint with application info"""
    logger.info("Root endpoint accessed")
    return {
        "message": "Welcome to Travel Agency ERP System",
        "version": "1.0.0",
        "docs": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "Travel Agency ERP System",
        "environment": settings.ENVIRONMENT
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL.lower(),
        reload=settings.DEBUG
    )
