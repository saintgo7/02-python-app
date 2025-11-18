# drf-spectacular settings for OpenAPI schema generation

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
