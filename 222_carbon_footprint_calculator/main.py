#!/usr/bin/env python3
"""
Carbon Footprint Calculator
Production-ready FastAPI application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging import setup_logging
from app.core.middleware import RequestLoggingMiddleware, SecurityHeadersMiddleware
import logging

logger = setup_logging(__name__)

app = FastAPI(
    title="Carbon Footprint Calculator",
    version="1.0.0",
    description="Production-ready application with comprehensive error handling and logging"
)

# Add middleware
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/")
async def read_root():
    """Root endpoint"""
    return {"message": "Welcome to Carbon Footprint Calculator", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
