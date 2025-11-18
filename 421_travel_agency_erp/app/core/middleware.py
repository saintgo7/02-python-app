"""Request/response middleware for Travel Agency ERP"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timezone
import logging
import uuid

logger = logging.getLogger(__name__)


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Add request ID to all requests"""

    async def dispatch(self, request: Request, call_next):
        """Add request ID header"""
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests and responses"""

    async def dispatch(self, request: Request, call_next):
        """Log request/response information"""
        request_id = getattr(request.state, "request_id", "unknown")

        # Log request
        logger.info(
            f"[{request_id}] {request.method} {request.url.path}",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        )

        try:
            response = await call_next(request)
            logger.info(
                f"[{request_id}] Status: {response.status_code}",
                extra={
                    "request_id": request_id,
                    "status_code": response.status_code
                }
            )
            return response
        except Exception as e:
            logger.error(
                f"[{request_id}] Error: {str(e)}",
                extra={
                    "request_id": request_id,
                    "error": str(e)
                },
                exc_info=True
            )
            raise


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to responses"""

    async def dispatch(self, request: Request, call_next):
        """Add security headers"""
        response = await call_next(request)

        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"

        return response


class CORSHeadersMiddleware(BaseHTTPMiddleware):
    """Handle CORS headers properly"""

    async def dispatch(self, request: Request, call_next):
        """Handle CORS"""
        if request.method == "OPTIONS":
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                headers={
                    "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
                    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type, Authorization"
                }
            )

        response = await call_next(request)
        return response
