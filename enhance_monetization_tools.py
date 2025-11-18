#!/usr/bin/env python3
"""
Monetization Tool Enhancement
Adds advanced features:
- Error handling and logging
- Rate limiting
- Caching
- API response standardization
- Database support
"""

from pathlib import Path

def generate_api_response_model() -> str:
    """Generate standardized API response model"""
    return '''from typing import Any, Optional, List, Dict
from datetime import datetime


class APIResponse:
    """Standard API response model"""

    def __init__(
        self,
        data: Any = None,
        message: str = "Success",
        status: str = "success",
        code: int = 200,
        timestamp: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        self.data = data
        self.message = message
        self.status = status
        self.code = code
        self.timestamp = timestamp or datetime.utcnow().isoformat()
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "data": self.data,
            "message": self.message,
            "status": self.status,
            "code": self.code,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }

    @staticmethod
    def success(data: Any = None, message: str = "Success", **kwargs) -> "APIResponse":
        return APIResponse(data=data, message=message, status="success", code=200, **kwargs)

    @staticmethod
    def error(message: str = "Error", code: int = 400, **kwargs) -> "APIResponse":
        return APIResponse(message=message, status="error", code=code, **kwargs)

    @staticmethod
    def paginated(
        items: List,
        total: int,
        page: int = 1,
        per_page: int = 10,
        **kwargs
    ) -> "APIResponse":
        return APIResponse(
            data=items,
            message="Success",
            status="success",
            code=200,
            metadata={
                "total": total,
                "page": page,
                "per_page": per_page,
                "pages": (total + per_page - 1) // per_page
            },
            **kwargs
        )
'''


def generate_error_handling() -> str:
    """Generate error handling utilities"""
    return '''import logging
from typing import Optional, Callable
from functools import wraps
from datetime import datetime


class ErrorHandler:
    """Centralized error handling"""

    def __init__(self, log_file: str = "error.log"):
        self.logger = logging.getLogger(__name__)
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_error(self, error: Exception, context: str = ""):
        """Log error with context"""
        self.logger.error(f"{context}: {str(error)}", exc_info=True)

    def handle_exception(self, func: Callable):
        """Decorator to handle exceptions"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.log_error(e, context=func.__name__)
                return {
                    "status": "error",
                    "message": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                }
        return wrapper


error_handler = ErrorHandler()
'''


def generate_rate_limiting() -> str:
    """Generate rate limiting utility"""
    return '''from functools import wraps
from time import time
from typing import Callable, Dict, Tuple
import threading


class RateLimiter:
    """Rate limiter with sliding window"""

    def __init__(self, max_calls: int = 100, time_window: int = 60):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls: Dict[str, list] = {}
        self.lock = threading.Lock()

    def is_allowed(self, key: str) -> Tuple[bool, Dict]:
        """Check if request is allowed"""
        with self.lock:
            now = time()

            if key not in self.calls:
                self.calls[key] = []

            # Remove old calls outside window
            self.calls[key] = [call_time for call_time in self.calls[key]
                               if now - call_time < self.time_window]

            if len(self.calls[key]) < self.max_calls:
                self.calls[key].append(now)
                return True, {"remaining": self.max_calls - len(self.calls[key])}
            else:
                return False, {"retry_after": int(self.calls[key][0] + self.time_window - now)}

    def rate_limit(self, max_calls: int = 100, time_window: int = 60):
        """Decorator for rate limiting"""
        limiter = RateLimiter(max_calls, time_window)

        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, user_id: str = "anonymous", **kwargs):
                allowed, info = limiter.is_allowed(user_id)

                if not allowed:
                    return {
                        "status": "error",
                        "message": "Rate limit exceeded",
                        "retry_after": info["retry_after"]
                    }

                result = func(*args, **kwargs)

                # Add rate limit headers
                result["X-RateLimit-Remaining"] = info.get("remaining", 0)
                return result

            return wrapper
        return decorator


rate_limiter = RateLimiter()
'''


def generate_database_support() -> str:
    """Generate database support for monetization tools"""
    return '''from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON
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
'''


def generate_enhanced_tool_main() -> str:
    """Generate enhanced tool main.py"""
    return '''from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
import logging
from typing import Optional, Dict, Any
from datetime import datetime
from app.api_response import APIResponse
from app.error_handling import error_handler
from app.rate_limiting import rate_limiter

app = FastAPI(
    title="Enhanced Tool API",
    version="2.0.0",
    description="Tool with error handling, rate limiting, and database support"
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.middleware("http")
async def log_middleware(request, call_next):
    """Log all requests"""
    start_time = datetime.utcnow()
    response = await call_next(request)
    process_time = (datetime.utcnow() - start_time).total_seconds()

    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")

    return response


def get_user_id(api_key: Optional[str] = Query(None)) -> str:
    """Get user ID from API key"""
    return api_key or "anonymous"


@app.post("/process")
@error_handler.handle_exception
def process_data(
    data: Dict[str, Any],
    user_id: str = Depends(get_user_id)
):
    """Process data with rate limiting and error handling"""
    allowed, info = rate_limiter.is_allowed(user_id)

    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
            headers={"Retry-After": str(info["retry_after"])}
        )

    try:
        # Process data
        result = {
            "input": data,
            "processed_at": datetime.utcnow().isoformat(),
        }

        response = APIResponse.success(
            data=result,
            message="Data processed successfully"
        )

        return response.to_dict()

    except Exception as e:
        error_handler.log_error(e, context="process_data")
        response = APIResponse.error(
            message=str(e),
            code=500
        )
        return response.to_dict()


@app.get("/status")
def get_status():
    """Get API status"""
    return APIResponse.success(
        data={"status": "operational"},
        message="API is operational"
    ).to_dict()


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''


def enhance_monetization_projects():
    """Enhance monetization projects"""
    monetization_projects = list(range(41, 61))

    print("🚀 Enhancing Monetization Tools with Advanced Features...")
    print("=" * 70)

    for i in monetization_projects:
        projects = list(Path("/home/user/02-python-app").glob(f"{i:02d}_*"))
        if not projects:
            continue

        project_name = projects[0].name
        base_path = projects[0]
        print(f"[{project_name}]", end=" ", flush=True)

        try:
            # Create API response model
            response_code = generate_api_response_model()
            (base_path / "app" / "api_response.py").write_text(response_code)

            # Create error handling
            error_code = generate_error_handling()
            (base_path / "app" / "error_handling.py").write_text(error_code)

            # Create rate limiting
            rate_code = generate_rate_limiting()
            (base_path / "app" / "rate_limiting.py").write_text(rate_code)

            # Create database models
            db_code = generate_database_support()
            (base_path / "app" / "models.py").write_text(db_code)

            # Update main.py
            enhanced_main = generate_enhanced_tool_main()
            (base_path / "main.py").write_text(enhanced_main)

            # Update requirements
            enhanced_requirements = '''fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-dotenv==1.0.0
pydantic==2.5.0
requests==2.31.0
beautifulsoup4==4.12.2
selenium==4.15.2
pandas==2.1.3
aiohttp==3.9.1
aiofiles==23.2.1
'''
            (base_path / "requirements.txt").write_text(enhanced_requirements)

            print("✅")
        except Exception as e:
            print(f"❌ Error: {e}")

    print("=" * 70)
    print("✨ Monetization tools enhanced!")


if __name__ == "__main__":
    enhance_monetization_projects()
