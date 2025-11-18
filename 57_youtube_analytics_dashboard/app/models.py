from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class ToolResult(Base):
    """Model for storing tool results"""
    __tablename__ = "tool_results"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=True)
    tool_name = Column(String)
    input_data = Column(JSON)
    output_data = Column(JSON)
    processing_time = Column(Float)
    status = Column(String, default="success")
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ToolUsage(Base):
    """Model for tracking tool usage"""
    __tablename__ = "tool_usage"

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    tool_name = Column(String)
    calls_count = Column(Integer, default=0)
    last_called = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)


class ToolSubscription(Base):
    """Model for subscription management"""
    __tablename__ = "tool_subscriptions"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, unique=True)
    tier = Column(String, default="free")  # free, pro, enterprise
    api_key = Column(String, unique=True)
    monthly_limit = Column(Integer)
    used_calls = Column(Integer, default=0)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
