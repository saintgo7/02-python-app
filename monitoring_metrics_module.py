#!/usr/bin/env python3
"""
Prometheus metrics module for application monitoring.
Collects and exposes metrics for Prometheus scraping.
"""

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request
from typing import Callable
import time
import logging

logger = logging.getLogger(__name__)

# Request metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency in seconds',
    ['method', 'endpoint'],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0)
)

http_request_size_bytes = Histogram(
    'http_request_size_bytes',
    'HTTP request size in bytes',
    ['method', 'endpoint']
)

http_response_size_bytes = Histogram(
    'http_response_size_bytes',
    'HTTP response size in bytes',
    ['method', 'endpoint']
)

# Error metrics
http_errors_total = Counter(
    'http_errors_total',
    'Total HTTP errors',
    ['method', 'endpoint', 'error_type']
)

# Database metrics
db_connection_pool_size = Gauge(
    'db_connection_pool_size',
    'Database connection pool size',
    ['database']
)

db_connections_active = Gauge(
    'db_connections_active',
    'Active database connections',
    ['database']
)

db_query_duration_seconds = Histogram(
    'db_query_duration_seconds',
    'Database query latency in seconds',
    ['operation'],
    buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 1.0)
)

db_query_errors_total = Counter(
    'db_query_errors_total',
    'Total database query errors',
    ['operation', 'error_type']
)

# Cache metrics
cache_hits_total = Counter(
    'cache_hits_total',
    'Total cache hits',
    ['cache_name']
)

cache_misses_total = Counter(
    'cache_misses_total',
    'Total cache misses',
    ['cache_name']
)

cache_duration_seconds = Histogram(
    'cache_duration_seconds',
    'Cache operation latency in seconds',
    ['cache_name', 'operation']
)

# Business metrics
active_users = Gauge(
    'active_users',
    'Number of active users'
)

requests_queued = Gauge(
    'requests_queued',
    'Number of queued requests'
)

# Application health
app_version = Gauge(
    'app_version_info',
    'Application version info',
    ['version', 'environment']
)

app_uptime_seconds = Gauge(
    'app_uptime_seconds',
    'Application uptime in seconds'
)

# Middleware for automatic metrics collection
class PrometheusMiddleware:
    """ASGI middleware to collect Prometheus metrics"""

    def __init__(self, app, app_name: str = "app", skip_paths: list = None):
        self.app = app
        self.app_name = app_name
        self.skip_paths = skip_paths or ["/metrics", "/health"]

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        path = scope["path"]
        if path in self.skip_paths:
            await self.app(scope, receive, send)
            return

        method = scope["method"]
        start_time = time.time()

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                status_code = message["status"]
                http_requests_total.labels(method=method, endpoint=path, status=status_code).inc()

            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        except Exception as exc:
            http_errors_total.labels(method=method, endpoint=path, error_type=type(exc).__name__).inc()
            raise
        finally:
            duration = time.time() - start_time
            http_request_duration_seconds.labels(method=method, endpoint=path).observe(duration)


class MetricsCollector:
    """Helper class for collecting application metrics"""

    @staticmethod
    def record_db_query(operation: str, duration: float, error: bool = False):
        """Record database query metrics"""
        db_query_duration_seconds.labels(operation=operation).observe(duration)
        if error:
            db_query_errors_total.labels(operation=operation, error_type='query_error').inc()

    @staticmethod
    def record_cache_hit(cache_name: str):
        """Record cache hit"""
        cache_hits_total.labels(cache_name=cache_name).inc()

    @staticmethod
    def record_cache_miss(cache_name: str):
        """Record cache miss"""
        cache_misses_total.labels(cache_name=cache_name).inc()

    @staticmethod
    def record_cache_operation(cache_name: str, operation: str, duration: float):
        """Record cache operation"""
        cache_duration_seconds.labels(cache_name=cache_name, operation=operation).observe(duration)

    @staticmethod
    def set_active_users(count: int):
        """Set number of active users"""
        active_users.set(count)

    @staticmethod
    def set_queued_requests(count: int):
        """Set number of queued requests"""
        requests_queued.set(count)

    @staticmethod
    def set_db_pool_size(database: str, size: int):
        """Set database connection pool size"""
        db_connection_pool_size.labels(database=database).set(size)

    @staticmethod
    def set_db_active_connections(database: str, count: int):
        """Set number of active database connections"""
        db_connections_active.labels(database=database).set(count)


def setup_metrics_endpoint(app, app_name: str = "app", version: str = "1.0.0", environment: str = "production"):
    """
    Setup metrics endpoint for the FastAPI application

    Usage:
        from app.core.metrics import setup_metrics_endpoint

        app = FastAPI()
        setup_metrics_endpoint(app, app_name="my-app", version="1.0.0", environment="production")
    """
    # Add middleware
    app.add_middleware(PrometheusMiddleware, app_name=app_name)

    # Metrics endpoint
    @app.get("/metrics")
    async def metrics():
        """Prometheus metrics endpoint"""
        app_version.labels(version=version, environment=environment).set(1)
        return generate_latest()

    # Add response header
    @app.middleware("http")
    async def add_metrics_header(request: Request, call_next):
        response = await call_next(request)
        response.headers["Content-Type"] = CONTENT_TYPE_LATEST
        return response

    logger.info(f"Prometheus metrics endpoint initialized for {app_name} v{version}")
