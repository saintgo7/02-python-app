"""Core error handling utilities for production applications."""

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class AppException(Exception):
    """Base exception for application-specific errors"""
    def __init__(self, message: str, code: str = "APP_ERROR", status_code: int = 400):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)


class ValidationException(AppException):
    """Raised when input validation fails"""
    def __init__(self, message: str, field: str = None):
        super().__init__(message, "VALIDATION_ERROR", status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.field = field


class NotFoundException(AppException):
    """Raised when a requested resource is not found"""
    def __init__(self, resource: str, identifier: Any = None):
        message = f"{resource} not found"
        if identifier:
            message += f": {identifier}"
        super().__init__(message, "NOT_FOUND", status.HTTP_404_NOT_FOUND)


class UnauthorizedException(AppException):
    """Raised when authentication fails"""
    def __init__(self, message: str = "Authentication required"):
        super().__init__(message, "UNAUTHORIZED", status.HTTP_401_UNAUTHORIZED)


class ForbiddenException(AppException):
    """Raised when user lacks required permissions"""
    def __init__(self, message: str = "Access denied"):
        super().__init__(message, "FORBIDDEN", status.HTTP_403_FORBIDDEN)


def error_response(message: str, code: str = "ERROR", status_code: int = 400) -> JSONResponse:
    """Create standardized error response"""
    return JSONResponse(
        status_code=status_code,
        content={"error": {"message": message, "code": code}}
    )


def success_response(data: Any = None, message: str = "Success") -> Dict:
    """Create standardized success response"""
    return {"success": True, "message": message, "data": data}
