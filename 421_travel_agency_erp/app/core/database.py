"""Database configuration and session management"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import get_settings
from typing import Generator

settings = get_settings()

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    poolclass=None,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=10,
    pool_recycle=settings.DATABASE_POOL_RECYCLE,
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db() -> Generator:
    """Get database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.commit()
        db.close()
