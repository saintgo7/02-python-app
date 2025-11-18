import logging
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
