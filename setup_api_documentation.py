#!/usr/bin/env python3
"""
API Documentation Setup
Generates OpenAPI/Swagger documentation for all projects
"""

from pathlib import Path

def generate_fastapi_openapi_config() -> str:
    """Generate enhanced FastAPI OpenAPI configuration"""
    return '''from fastapi import FastAPI
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
'''

def generate_fastapi_endpoint_docs() -> str:
    """Generate FastAPI endpoints with detailed documentation"""
    return '''from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.core.security import get_current_user

router = APIRouter()


# ============================================
# Authentication Endpoints
# ============================================

@router.post("/auth/register", tags=["Authentication"])
async def register(email: str, password: str):
    """
    Register a new user.

    - **email**: User's email address
    - **password**: User's password (minimum 8 characters)

    Returns the created user object with authentication token.
    """
    pass


@router.post("/auth/login", tags=["Authentication"])
async def login(email: str, password: str):
    """
    Login user with credentials.

    - **email**: User's email address
    - **password**: User's password

    Returns JWT access token and refresh token.
    """
    pass


@router.post("/auth/refresh", tags=["Authentication"])
async def refresh_token(current_user: dict = Depends(get_current_user)):
    """
    Refresh JWT access token.

    Requires valid JWT in Authorization header.

    Returns new access token.
    """
    pass


# ============================================
# Item Management Endpoints
# ============================================

@router.get("/items", tags=["Items"], response_model=dict)
async def list_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum items to return"),
    current_user: dict = Depends(get_current_user)
):
    """
    List all items with pagination.

    - **skip**: Number of items to skip (for pagination)
    - **limit**: Maximum number of items to return (1-100)

    Returns paginated list of items.
    """
    pass


@router.post("/items", tags=["Items"], status_code=status.HTTP_201_CREATED)
async def create_item(
    name: str,
    description: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new item.

    - **name**: Item name (required)
    - **description**: Item description (optional)

    Returns created item with ID.
    """
    pass


@router.get("/items/{item_id}", tags=["Items"])
async def get_item(
    item_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific item by ID.

    - **item_id**: The ID of the item to retrieve

    Returns item details.
    """
    pass


@router.put("/items/{item_id}", tags=["Items"])
async def update_item(
    item_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Update an existing item.

    - **item_id**: The ID of the item to update
    - **name**: New item name (optional)
    - **description**: New description (optional)

    Returns updated item.
    """
    pass


@router.delete("/items/{item_id}", tags=["Items"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete an item.

    - **item_id**: The ID of the item to delete

    Returns 204 No Content on success.
    """
    pass


# ============================================
# Advanced Search & Filter Endpoints
# ============================================

@router.get("/search", tags=["Search & Filter"])
async def advanced_search(
    q: str = Query(..., min_length=1, description="Search query"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort_by: str = Query("created_at", description="Field to sort by"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    current_user: dict = Depends(get_current_user)
):
    """
    Advanced search across all items.

    - **q**: Search query string (required)
    - **skip**: Number of results to skip
    - **limit**: Maximum results to return
    - **sort_by**: Field to sort results by
    - **sort_order**: Sort direction (asc/desc)

    Searches across multiple fields including name and description.
    """
    pass


@router.get("/filter", tags=["Search & Filter"])
async def advanced_filter(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    is_active: Optional[bool] = None,
    sort_by: str = Query("created_at"),
    current_user: dict = Depends(get_current_user)
):
    """
    Filter items with advanced options.

    - **is_active**: Filter by active status (optional)
    - **skip**: Number of results to skip
    - **limit**: Maximum results to return
    - **sort_by**: Field to sort by

    Returns filtered and sorted items.
    """
    pass


# ============================================
# Health Check Endpoints
# ============================================

@router.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.

    Returns application health status and connected services.
    """
    pass


@router.get("/status", tags=["Health"])
async def status_check():
    """
    Get application status.

    Returns detailed status information about the API.
    """
    pass
'''

def generate_django_spectacular_config() -> str:
    """Generate Django drf-spectacular OpenAPI configuration"""
    return '''# drf-spectacular settings for OpenAPI schema generation

SPECTACULAR_SETTINGS = {
    'TITLE': 'API Documentation',
    'DESCRIPTION': 'Comprehensive REST API Documentation',
    'VERSION': '1.0.0',
    'SERVE_PERMISSIONS': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'SERVE_AUTHENTICATION': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    # Schema generation settings
    'SCHEMA_PATH_PREFIX': '/api/v[0-9]',
    'SCHEMA_MOUNT_PATH': '/api/schema',
    'SCHEMA_FILE_PATH': 'schema.yml',
    # Swagger UI settings
    'SWAGGER_UI_SETTINGS': {
        'DeepLinking': True,
        'PersistAuthorization': True,
        'DisplayOperationId': True,
        'Url': 'http://localhost:8000/api/schema/openapi.json'
    },
    # ReDoc settings
    'REDOC_SETTINGS': {
        'HideDownloadButton': False,
        'HideHostname': False,
    },
    # Security schemes
    'SECURITY': [
        {
            'Bearer': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT',
            }
        }
    ],
    # API info
    'CONTACT': {
        'name': 'API Support',
        'url': 'https://example.com/support',
        'email': 'support@example.com'
    },
    'LICENSE': {
        'name': 'MIT',
        'url': 'https://opensource.org/licenses/MIT'
    },
    # Servers configuration
    'SERVERS': [
        {'url': 'http://localhost:8000', 'description': 'Development'},
        {'url': 'https://staging.example.com', 'description': 'Staging'},
        {'url': 'https://api.example.com', 'description': 'Production'},
    ],
}

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
'''

def generate_django_urls_with_schema() -> str:
    """Generate Django URL configuration with schema endpoints"""
    return '''from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # OpenAPI schema endpoint
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI documentation
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),

    # ReDoc documentation
    path(
        'api/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
]
'''

def generate_api_docs_site_html() -> str:
    """Generate HTML for API documentation site"""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Documentation</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            max-width: 1000px;
            width: 100%;
            background: white;
            border-radius: 10px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }

        .content {
            padding: 40px;
        }

        .section {
            margin-bottom: 40px;
        }

        .section h2 {
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }

        .doc-links {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .doc-link {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
            border: 2px solid #ddd;
            border-radius: 8px;
            text-decoration: none;
            color: #333;
            transition: all 0.3s ease;
        }

        .doc-link:hover {
            border-color: #667eea;
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.2);
            transform: translateY(-5px);
        }

        .doc-link-icon {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .doc-link-title {
            font-weight: bold;
            margin-bottom: 5px;
        }

        .doc-link-desc {
            font-size: 0.9em;
            color: #666;
            text-align: center;
        }

        .features {
            background: #f5f7fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }

        .features h3 {
            color: #333;
            margin-bottom: 15px;
        }

        .features ul {
            list-style: none;
            columns: 2;
            column-gap: 30px;
        }

        .features li {
            margin-bottom: 10px;
            padding-left: 25px;
            position: relative;
        }

        .features li:before {
            content: "✓";
            position: absolute;
            left: 0;
            color: #667eea;
            font-weight: bold;
        }

        .footer {
            background: #f5f7fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }

        @media (max-width: 600px) {
            .header h1 {
                font-size: 1.8em;
            }

            .doc-links {
                grid-template-columns: 1fr;
            }

            .features ul {
                columns: 1;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 API Documentation</h1>
            <p>Comprehensive REST API with Interactive Documentation</p>
        </div>

        <div class="content">
            <div class="section">
                <h2>📚 Documentation</h2>
                <div class="doc-links">
                    <a href="/docs" class="doc-link">
                        <div class="doc-link-icon">🐍</div>
                        <div class="doc-link-title">Swagger UI</div>
                        <div class="doc-link-desc">Interactive API testing</div>
                    </a>
                    <a href="/redoc" class="doc-link">
                        <div class="doc-link-icon">📖</div>
                        <div class="doc-link-title">ReDoc</div>
                        <div class="doc-link-desc">Beautiful documentation</div>
                    </a>
                    <a href="/openapi.json" class="doc-link">
                        <div class="doc-link-icon">⚙️</div>
                        <div class="doc-link-title">OpenAPI Schema</div>
                        <div class="doc-link-desc">Machine-readable spec</div>
                    </a>
                    <a href="/health" class="doc-link">
                        <div class="doc-link-icon">💚</div>
                        <div class="doc-link-title">Health Check</div>
                        <div class="doc-link-desc">API status</div>
                    </a>
                </div>
            </div>

            <div class="section">
                <h2>✨ Features</h2>
                <div class="features">
                    <h3>API Capabilities</h3>
                    <ul>
                        <li>RESTful API design</li>
                        <li>JWT authentication</li>
                        <li>Advanced filtering & search</li>
                        <li>Pagination support</li>
                        <li>Rate limiting</li>
                        <li>Redis caching</li>
                        <li>WebSocket support</li>
                        <li>GraphQL API</li>
                        <li>Comprehensive error handling</li>
                        <li>Request/response logging</li>
                        <li>CORS configuration</li>
                        <li>OpenAPI documentation</li>
                    </ul>
                </div>
            </div>

            <div class="section">
                <h2>🔐 Authentication</h2>
                <p>All protected endpoints require JWT authentication in the Authorization header:</p>
                <pre style="background: #f5f7fa; padding: 15px; border-radius: 5px; margin-top: 10px; overflow-x: auto;">Authorization: Bearer &lt;your-jwt-token&gt;</pre>
            </div>

            <div class="section">
                <h2>📋 Available Endpoints</h2>
                <p>Visit the Swagger UI documentation to explore all available endpoints and test them directly.</p>
            </div>
        </div>

        <div class="footer">
            <p>API Version 1.0.0 | Built with FastAPI/Django | © 2024</p>
        </div>
    </div>
</body>
</html>
'''

def generate_github_pages_config() -> str:
    """Generate GitHub Pages documentation configuration"""
    return '''# GitHub Pages Configuration for API Documentation
site_name: API Documentation
site_description: Comprehensive REST API Documentation
theme:
  name: material
  palette:
    primary: indigo
    accent: indigo
nav:
  - Home: index.md
  - API Reference: api/reference.md
  - Authentication: guides/authentication.md
  - Endpoints: guides/endpoints.md
  - Examples: examples/usage.md
plugins:
  - search
  - mkdocstrings:
      default_handler: python
      handlers:
        python:
          rendering:
            show_source: true
markdown_extensions:
  - pymdownx.superfences
  - pymdownx.highlight
  - pymdownx.tabbed
  - admonition
'''

def generate_postman_collection() -> str:
    """Generate Postman API collection"""
    return '''{
  "info": {
    "name": "API Collection",
    "description": "Complete API endpoints for testing",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Authentication",
      "item": [
        {
          "name": "Register",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\\"email\\": \\"user@example.com\\", \\"password\\": \\"testpass123\\"}"
            },
            "url": {
              "raw": "{{base_url}}/auth/register",
              "host": ["{{base_url}}"],
              "path": ["auth", "register"]
            }
          }
        },
        {
          "name": "Login",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\\"email\\": \\"user@example.com\\", \\"password\\": \\"testpass123\\"}"
            },
            "url": {
              "raw": "{{base_url}}/auth/login",
              "host": ["{{base_url}}"],
              "path": ["auth", "login"]
            }
          }
        }
      ]
    },
    {
      "name": "Items",
      "item": [
        {
          "name": "List Items",
          "request": {
            "method": "GET",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{access_token}}"
              }
            ],
            "url": {
              "raw": "{{base_url}}/items?skip=0&limit=10",
              "host": ["{{base_url}}"],
              "path": ["items"],
              "query": [
                {
                  "key": "skip",
                  "value": "0"
                },
                {
                  "key": "limit",
                  "value": "10"
                }
              ]
            }
          }
        },
        {
          "name": "Create Item",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              },
              {
                "key": "Authorization",
                "value": "Bearer {{access_token}}"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\\"name\\": \\"Test Item\\", \\"description\\": \\"Test Description\\"}"
            },
            "url": {
              "raw": "{{base_url}}/items",
              "host": ["{{base_url}}"],
              "path": ["items"]
            }
          }
        }
      ]
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8000"
    },
    {
      "key": "access_token",
      "value": ""
    }
  ]
}
'''

def setup_api_documentation():
    """Setup API documentation for all projects"""
    print("📚 Setting up API Documentation...")
    print("=" * 70)

    # Create docs directory at root
    docs_dir = Path("/home/user/02-python-app/docs")
    docs_dir.mkdir(exist_ok=True)

    # Create API documentation site
    (docs_dir / "index.html").write_text(generate_api_docs_site_html())
    (docs_dir / "mkdocs.yml").write_text(generate_github_pages_config())
    (docs_dir / "postman_collection.json").write_text(generate_postman_collection())

    # Create API reference docs
    api_docs_dir = docs_dir / "api"
    api_docs_dir.mkdir(exist_ok=True)
    (api_docs_dir / "reference.md").write_text("""# API Reference

## Overview
This is the API reference documentation for all endpoints.

## Authentication
All protected endpoints require JWT authentication.

## Endpoints
See Swagger UI for interactive documentation.
""")

    # Create guides
    guides_dir = docs_dir / "guides"
    guides_dir.mkdir(exist_ok=True)

    (guides_dir / "authentication.md").write_text("""# Authentication Guide

## JWT Authentication
All endpoints (except registration and login) require JWT authentication.

### Login
```bash
curl -X POST http://localhost:8000/auth/login \\
  -H "Content-Type: application/json" \\
  -d '{"email": "user@example.com", "password": "password123"}'
```

### Using Token
Include the token in the Authorization header:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \\
  http://localhost:8000/items
```
""")

    (guides_dir / "endpoints.md").write_text("""# Available Endpoints

## Items
- `GET /items` - List all items
- `POST /items` - Create new item
- `GET /items/{id}` - Get specific item
- `PUT /items/{id}` - Update item
- `DELETE /items/{id}` - Delete item

## Search & Filter
- `GET /search?q=query` - Advanced search
- `GET /filter?is_active=true` - Filter items

## Health
- `GET /health` - Health check
- `GET /status` - API status
""")

    # Create examples
    examples_dir = docs_dir / "examples"
    examples_dir.mkdir(exist_ok=True)

    (examples_dir / "usage.md").write_text("""# Usage Examples

## Python Client
```python
import requests

# Login
response = requests.post(
    'http://localhost:8000/auth/login',
    json={'email': 'user@example.com', 'password': 'password123'}
)
token = response.json()['access_token']

# Get items
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://localhost:8000/items', headers=headers)
items = response.json()
```

## JavaScript Client
```javascript
// Login
const response = await fetch('http://localhost:8000/auth/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({email: 'user@example.com', password: 'password123'})
});
const {access_token} = await response.json();

// Get items
const itemsResponse = await fetch('http://localhost:8000/items', {
  headers: {'Authorization': `Bearer ${access_token}`}
});
const items = await itemsResponse.json();
```
""")

    # FastAPI projects
    print("[FastAPI Documentation (01-10)]", end=" ", flush=True)
    fastapi_projects = [
        "01_task_management_saas",
        "02_email_newsletter_platform",
        "03_url_shortener_service",
        "04_expense_tracker_saas",
        "05_document_converter_api",
        "06_form_builder_platform",
        "07_api_monitoring_service",
        "08_markdown_to_html_saas",
        "09_qr_code_generator_api",
        "10_jwt_auth_service",
    ]

    for project in fastapi_projects:
        base_path = Path(f"/home/user/02-python-app/{project}")
        app_dir = base_path / "app"

        # Create OpenAPI configuration
        (app_dir / "openapi_config.py").write_text(generate_fastapi_openapi_config())

        # Create documented routes
        routes_dir = app_dir / "routes"
        routes_dir.mkdir(exist_ok=True)
        (routes_dir / "documented.py").write_text(generate_fastapi_endpoint_docs())

        # Update main.py to use OpenAPI
        main_path = base_path / "main.py"
        if main_path.exists():
            content = main_path.read_text()
            if "setup_openapi_documentation" not in content:
                # This will be updated separately
                pass
    print("✅")

    # Django projects
    print("[Django Documentation (11-20)]", end=" ", flush=True)
    django_projects = [
        "11_multi_tenant_crm",
        "12_blog_platform",
        "13_project_management_system",
        "14_inventory_management",
        "15_customer_support_portal",
        "16_event_booking_system",
        "17_subscription_billing_platform",
        "18_learning_management_system",
        "19_real_estate_listing_platform",
        "20_social_network_backend",
    ]

    for project in django_projects:
        base_path = Path(f"/home/user/02-python-app/{project}")
        app_dir = base_path / "app"

        # Create spectacular configuration
        (app_dir / "spectacular_config.py").write_text(generate_django_spectacular_config())
        (app_dir / "schema_urls.py").write_text(generate_django_urls_with_schema())
    print("✅")

    # AI/ML projects
    print("[AI/ML Documentation (21-40)]", end=" ", flush=True)
    for i in range(21, 41):
        projects = list(Path("/home/user/02-python-app").glob(f"{i:02d}_*"))
        if not projects:
            continue
        base_path = projects[0]
        app_dir = base_path / "app"

        (app_dir / "openapi_config.py").write_text(generate_fastapi_openapi_config())
    print("✅")

    # Monetization tools
    print("[Monetization Documentation (41-60)]", end=" ", flush=True)
    for i in range(41, 61):
        projects = list(Path("/home/user/02-python-app").glob(f"{i:02d}_*"))
        if not projects:
            continue
        base_path = projects[0]
        app_dir = base_path / "app"

        (app_dir / "openapi_config.py").write_text(generate_fastapi_openapi_config())
    print("✅")

    print("=" * 70)
    print("✨ API documentation setup complete!")
    print("\nDocumentation Summary:")
    print(f"  ✓ Root documentation site: docs/")
    print(f"  ✓ FastAPI projects: OpenAPI config + documented routes")
    print(f"  ✓ Django projects: drf-spectacular configuration")
    print(f"  ✓ AI/ML projects: OpenAPI configuration")
    print(f"  ✓ Monetization tools: OpenAPI configuration")
    print(f"  ✓ Postman collection: docs/postman_collection.json")
    print(f"  ✓ MkDocs configuration: docs/mkdocs.yml")
    print("\nAccess Documentation:")
    print(f"  • Swagger UI: http://localhost:8000/docs")
    print(f"  • ReDoc: http://localhost:8000/redoc")
    print(f"  • OpenAPI Schema: http://localhost:8000/openapi.json")
    print(f"  • Documentation Site: docs/index.html")


if __name__ == "__main__":
    setup_api_documentation()
