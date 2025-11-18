"""Structured logging configuration for production applications."""

import logging
import uuid
from logging.handlers import RotatingFileHandler
from pathlib import Path
import json
from datetime import datetime

_request_id = None

def get_request_id():
    """Get or create request ID for correlation tracking"""
    global _request_id
    if not _request_id:
        _request_id = str(uuid.uuid4())
    return _request_id

def set_request_id(request_id: str):
    """Set request ID for correlation tracking"""
    global _request_id
    _request_id = request_id

class JsonFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    def format(self, record):
        log_obj = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": get_request_id(),
        }
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_obj)

def setup_logging(app_name: str, log_level: str = "INFO", log_file: str = None):
    """Configure structured logging for the application"""
    logger = logging.getLogger(app_name)
    logger.setLevel(getattr(logging, log_level))
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(JsonFormatter())
    logger.addHandler(console_handler)
    if log_file:
        log_path = Path(log_file).parent
        log_path.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
        file_handler.setFormatter(JsonFormatter())
        logger.addHandler(file_handler)
    return logger
