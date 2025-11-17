"""
Production configuration management for the application.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    APP_NAME: str = "Invoice & Billing System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO" if not DEBUG else "DEBUG")

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    DATABASE_POOL_SIZE: int = int(os.getenv("DATABASE_POOL_SIZE", "5"))
    DATABASE_POOL_RECYCLE: int = int(os.getenv("DATABASE_POOL_RECYCLE", "3600"))

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production-12345")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8080"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]

    # API Keys (optional)
    API_KEY: Optional[str] = os.getenv("API_KEY")

    # Redis (optional)
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL")

    # AWS (optional)
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    AWS_ACCESS_KEY_ID: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")

    class Config:
        env_file = ".env"
        case_sensitive = True
        validate_assignment = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
