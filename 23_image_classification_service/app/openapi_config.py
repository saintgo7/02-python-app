from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from typing import Any


def custom_openapi(app: FastAPI) -> dict[str, Any]:
    """Generate custom OpenAPI schema with documentation"""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="API Documentation",
        version="1.0.0",
        description="Comprehensive API Documentation with Swagger UI",
        routes=app.routes,
    )

    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT Bearer token authentication"
        }
    }

    # Add tags
    openapi_schema["tags"] = [
        {
            "name": "Authentication",
            "description": "User authentication endpoints"
        },
        {
            "name": "Items",
            "description": "Item management endpoints"
        },
        {
            "name": "Search & Filter",
            "description": "Advanced search and filtering endpoints"
        },
        {
            "name": "Health",
            "description": "Health check endpoints"
        }
    ]

    # Add servers
    openapi_schema["servers"] = [
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://staging.example.com",
            "description": "Staging server"
        },
        {
            "url": "https://api.example.com",
            "description": "Production server"
        }
    ]

    # Add info with contact
    openapi_schema["info"]["contact"] = {
        "name": "API Support",
        "url": "https://example.com/support",
        "email": "support@example.com"
    }

    openapi_schema["info"]["license"] = {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


def setup_openapi_documentation(app: FastAPI, title: str, version: str = "1.0.0"):
    """Setup OpenAPI documentation for FastAPI application"""
    app.openapi = lambda: custom_openapi(app)

    # Configure Swagger UI
    app.swagger_ui_init_oauth = {
        "clientId": "your-client-id",
        "realm": "your-realm",
        "appName": title,
        "scopes": ["openid", "profile", "email"]
    }

    # Alternative ReDoc documentation
    app.redoc_url = "/redoc"
    app.swagger_url = "/docs"
    app.openapi_url = "/openapi.json"
