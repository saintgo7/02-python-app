#!/usr/bin/env python3
"""
Energy Efficiency Analyzer
Production-ready FastAPI application with comprehensive monitoring
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys
sys.path.insert(0, str(Path(__file__).parent))

from app.core.logging import setup_logging
from app.core.middleware import RequestLoggingMiddleware, SecurityHeadersMiddleware
from app.core.metrics import setup_metrics_endpoint

# Setup logging
logger = setup_logging(__name__)

# Create FastAPI application
app = FastAPI(
    title="Energy Efficiency Analyzer",
    version="1.0.0",
    description="Production-ready application with monitoring, error handling, and logging"
)

# Add security middleware
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestLoggingMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup Prometheus metrics
setup_metrics_endpoint(app, app_name="Energy Efficiency Analyzer", version="1.0.0", environment="production")

@app.get("/")
async def read_root():
    """Root endpoint with application info"""
    logger.info("Root endpoint accessed")
    return {
        "message": "Welcome to Energy Efficiency Analyzer",
        "version": "1.0.0",
        "docs": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json",
            "metrics": "/metrics"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "Energy Efficiency Analyzer"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
