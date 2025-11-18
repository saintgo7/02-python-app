"""
Prometheus metrics module for application monitoring.
Copy the full version from /monitoring_metrics_module.py
"""

from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time

# Metrics definitions
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency in seconds',
    ['method', 'endpoint']
)

http_errors_total = Counter(
    'http_errors_total',
    'Total HTTP errors',
    ['method', 'endpoint', 'error_type']
)

active_users = Gauge(
    'active_users',
    'Number of active users'
)

requests_queued = Gauge(
    'requests_queued',
    'Number of queued requests'
)

app_version = Gauge(
    'app_version_info',
    'Application version info',
    ['version', 'environment']
)

def setup_metrics_endpoint(app, app_name: str = "app", version: str = "1.0.0", environment: str = "production"):
    """Setup metrics endpoint for FastAPI application"""

    @app.get("/metrics")
    async def metrics():
        """Prometheus metrics endpoint"""
        app_version.labels(version=version, environment=environment).set(1)
        return generate_latest()
