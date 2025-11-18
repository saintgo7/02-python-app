# 📁 Project Structure Guide

Detailed guide to the organization and structure of all 80 applications.

## Quick Navigation

- [Root Structure](#root-structure)
- [FastAPI Projects (01-10)](#fastapi-projects-01-10)
- [Django Projects (11-20)](#django-projects-11-20)
- [PyTorch Projects (21-30)](#pytorch-projects-21-30)
- [TensorFlow Projects (31-40)](#tensorflow-projects-31-40)
- [Monetization Tools (41-60)](#monetization-tools-41-60)
- [Frontend Structure](#frontend-structure)
- [Infrastructure Structure](#infrastructure-structure)

---

## Root Structure

```
02-python-app/
│
├── 📂 .github/
│   └── workflows/           # 61 GitHub Actions CI/CD workflows
│       ├── fastapi-01.yml
│       ├── django-11.yml
│       ├── pytorch-21.yml
│       ├── tensorflow-31.yml
│       └── monetization-41.yml
│
├── 📂 01-10_fastapi_projects/
│   └── [FastAPI applications with full structure]
│
├── 📂 11-20_django_projects/
│   └── [Django applications with full structure]
│
├── 📂 21-30_pytorch_projects/
│   └── [PyTorch ML applications with full structure]
│
├── 📂 31-40_tensorflow_projects/
│   └── [TensorFlow ML applications with full structure]
│
├── 📂 41-60_monetization_tools/
│   └── [Production tools with full structure]
│
├── 📂 frontend/
│   ├── react-app/           # React frontend for FastAPI (01-10)
│   └── vue-app/             # Vue frontend for Django (11-20)
│
├── 📂 terraform/
│   ├── main.tf              # Main AWS infrastructure
│   ├── vpc.tf               # VPC and networking
│   ├── rds.tf               # PostgreSQL database
│   ├── redis.tf             # ElastiCache Redis
│   ├── outputs.tf           # Output values
│   ├── variables.tf         # Input variables
│   ├── modules/
│   │   ├── iam/             # IAM roles and policies
│   │   ├── elastic_beanstalk/  # Elastic Beanstalk config
│   │   └── alb/             # Application Load Balancer
│   ├── development.tfvars   # Development environment
│   ├── staging.tfvars       # Staging environment
│   └── production.tfvars    # Production environment
│
├── 📂 docs/
│   ├── index.html           # Documentation home page
│   ├── postman_collection.json  # Postman API collection
│   ├── guides/
│   │   ├── authentication.md    # Auth guide
│   │   ├── endpoints.md         # API endpoints
│   │   └── examples.md          # Code examples
│   └── architecture/
│       ├── backend.md
│       ├── frontend.md
│       └── devops.md
│
├── 📄 README.md             # Main project documentation
├── 📄 SETUP_GUIDE.md        # Setup instructions
├── 📄 PROJECT_STRUCTURE.md  # This file
├── 📄 DEPLOYMENT.md         # Deployment options
├── 📄 ARCHITECTURE.md       # Architecture details
│
└── 📄 LICENSE               # MIT License
```

---

## FastAPI Projects (01-10)

### Standard Structure for Each Project

```
01_task_management_saas/
│
├── 📂 app/
│   ├── __init__.py
│   │
│   ├── 📂 core/
│   │   ├── __init__.py
│   │   ├── config.py            # Configuration management
│   │   ├── database.py          # SQLAlchemy setup, session
│   │   ├── security.py          # JWT, password hashing
│   │   └── exceptions.py        # Custom exceptions
│   │
│   ├── 📂 models/
│   │   ├── __init__.py
│   │   ├── user.py              # User model
│   │   ├── task.py              # Task model
│   │   └── base.py              # Base model class
│   │
│   ├── 📂 schemas/
│   │   ├── __init__.py
│   │   ├── user.py              # User Pydantic schemas
│   │   ├── task.py              # Task Pydantic schemas
│   │   └── common.py            # Common schemas (pagination, etc.)
│   │
│   ├── 📂 routes/
│   │   ├── __init__.py
│   │   ├── auth.py              # Authentication endpoints
│   │   ├── tasks.py             # Task CRUD endpoints
│   │   └── advanced_crud.py     # Advanced filtering, search
│   │
│   ├── 📂 services/
│   │   ├── __init__.py
│   │   ├── user_service.py      # User business logic
│   │   ├── task_service.py      # Task business logic
│   │   └── email_service.py     # Email sending
│   │
│   ├── 📂 middleware/
│   │   ├── __init__.py
│   │   ├── logging.py           # Request logging
│   │   ├── error_handling.py    # Error middleware
│   │   └── rate_limiting.py     # Rate limiting
│   │
│   ├── cache.py                 # Redis caching utilities
│   ├── graphql_schema.py        # GraphQL schema
│   └── websocket.py             # WebSocket handlers
│
├── 📂 tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures
│   ├── test_auth.py             # Authentication tests
│   ├── test_crud.py             # CRUD operation tests
│   ├── test_models.py           # Model validation tests
│   ├── test_api.py              # API endpoint tests
│   ├── test_security.py         # Security tests
│   ├── test_websocket.py        # WebSocket tests
│   └── test_graphql.py          # GraphQL tests
│
├── 📂 scripts/
│   ├── init_db.py               # Database initialization
│   ├── create_user.py           # Create test user
│   └── generate_data.py         # Generate test data
│
├── main.py                      # FastAPI application entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Example environment variables
├── Dockerfile                   # Container configuration
├── docker-compose.yml           # Multi-service setup
├── pyproject.toml              # Project metadata
├── .gitignore                  # Git ignore rules
├── pytest.ini                  # Pytest configuration
├── .flake8                     # Flake8 linting config
├── mypy.ini                    # Type checking config
├── .github/workflows/ci-cd.yml # GitHub Actions workflow
│
└── README.md                   # Project-specific documentation
```

### Key Files Explanation

| File | Purpose |
|------|---------|
| `main.py` | FastAPI application setup, middleware, route inclusion |
| `app/core/database.py` | SQLAlchemy engine, SessionLocal, Base class |
| `app/core/security.py` | JWT token creation/validation, bcrypt hashing |
| `app/models/*.py` | SQLAlchemy ORM models |
| `app/schemas/*.py` | Pydantic request/response schemas |
| `app/routes/*.py` | API endpoint definitions |
| `app/services/*.py` | Business logic, separated from routes |
| `app/middleware/*.py` | Request/response middleware |
| `tests/conftest.py` | Pytest fixtures and configuration |
| `requirements.txt` | All pip dependencies |

---

## Django Projects (11-20)

### Standard Structure for Each Project

```
11_multi_tenant_crm/
│
├── 📂 project/
│   ├── __init__.py
│   ├── settings.py             # Django settings
│   ├── urls.py                 # URL routing
│   ├── asgi.py                 # ASGI application
│   ├── wsgi.py                 # WSGI application
│   └── middleware.py           # Custom middleware
│
├── 📂 app/
│   ├── __init__.py
│   │
│   ├── 📂 migrations/
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   └── 0002_*.py          # Auto-generated migrations
│   │
│   ├── 📂 models/
│   │   ├── __init__.py
│   │   ├── user.py             # User model
│   │   ├── account.py          # Account model
│   │   ├── contact.py          # Contact model
│   │   └── base.py             # Abstract base models
│   │
│   ├── 📂 serializers/
│   │   ├── __init__.py
│   │   ├── user.py             # User DRF serializers
│   │   ├── account.py          # Account serializers
│   │   └── common.py           # Common serializers
│   │
│   ├── 📂 views/
│   │   ├── __init__.py
│   │   ├── user.py             # User viewsets
│   │   ├── account.py          # Account viewsets
│   │   ├── advanced_views.py   # Advanced filtering, search
│   │   └── auth.py             # Authentication views
│   │
│   ├── 📂 viewsets/
│   │   ├── __init__.py
│   │   ├── user_viewset.py     # User CRUD viewset
│   │   └── account_viewset.py  # Account CRUD viewset
│   │
│   ├── 📂 managers/
│   │   ├── __init__.py
│   │   ├── user_manager.py     # Custom user manager
│   │   └── account_manager.py  # Custom account manager
│   │
│   ├── 📂 querysets/
│   │   ├── __init__.py
│   │   ├── user_queryset.py    # Custom user queryset
│   │   └── account_queryset.py # Custom account queryset
│   │
│   ├── 📂 services/
│   │   ├── __init__.py
│   │   ├── user_service.py     # User business logic
│   │   ├── account_service.py  # Account business logic
│   │   └── email_service.py    # Email service
│   │
│   ├── 📂 signals/
│   │   ├── __init__.py
│   │   └── handlers.py         # Signal handlers
│   │
│   ├── 📂 admin/
│   │   ├── __init__.py
│   │   ├── user_admin.py       # User admin configuration
│   │   └── account_admin.py    # Account admin configuration
│   │
│   ├── 📂 filters/
│   │   ├── __init__.py
│   │   ├── user_filter.py      # User filters
│   │   └── account_filter.py   # Account filters
│   │
│   ├── cache.py                # Caching utilities
│   ├── permissions.py          # Custom permissions
│   ├── pagination.py           # Custom pagination
│   ├── authentication.py       # Custom authentication
│   ├── exceptions.py           # Custom exceptions
│   └── urls.py                 # App URL routing
│
├── 📂 tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   ├── test_models.py          # Model tests
│   ├── test_serializers.py     # Serializer tests
│   ├── test_viewsets.py        # ViewSet tests
│   ├── test_permissions.py     # Permission tests
│   ├── test_signals.py         # Signal tests
│   └── test_api.py             # API endpoint tests
│
├── 📂 management/
│   ├── commands/
│   │   ├── init_data.py        # Initialize data command
│   │   └── create_admin.py     # Create admin command
│
├── 📂 scripts/
│   ├── create_user.py
│   └── generate_data.py
│
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── .env.example                # Example environment variables
├── Dockerfile                  # Container configuration
├── docker-compose.yml          # Multi-service setup
├── pytest.ini                  # Pytest configuration
├── .flake8                     # Flake8 configuration
├── mypy.ini                    # Type checking config
├── .github/workflows/ci-cd.yml # GitHub Actions workflow
│
└── README.md                   # Project-specific documentation
```

### Key Files Explanation

| File | Purpose |
|------|---------|
| `manage.py` | Django management command interface |
| `project/settings.py` | Django project configuration |
| `app/models/` | Database models definition |
| `app/views/` | View logic (can be function or class-based) |
| `app/serializers/` | DRF serializers for data validation/serialization |
| `app/viewsets/` | DRF ViewSets for API endpoints |
| `app/managers/` | Custom QuerySet managers |
| `app/signals/` | Django signal handlers |
| `app/admin/` | Django admin configuration |
| `migrations/` | Database migration files |

---

## PyTorch Projects (21-30)

### Standard Structure for Each Project

```
21_object_detection_api/
│
├── 📂 app/
│   ├── __init__.py
│   │
│   ├── 📂 core/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration
│   │   ├── database.py         # Database setup
│   │   └── security.py         # Authentication
│   │
│   ├── 📂 models/
│   │   ├── __init__.py
│   │   ├── user.py             # User model
│   │   └── prediction.py       # Prediction log model
│   │
│   ├── 📂 ml/
│   │   ├── __init__.py
│   │   ├── model_loader.py     # Load pre-trained model
│   │   ├── preprocessor.py     # Image preprocessing
│   │   ├── trainer.py          # Model training
│   │   ├── inference.py        # Model inference
│   │   ├── ensemble.py         # Model ensemble
│   │   ├── versioning.py       # Model versioning
│   │   ├── metrics.py          # Evaluation metrics
│   │   └── batch_processor.py  # Batch processing
│   │
│   ├── 📂 routes/
│   │   ├── __init__.py
│   │   ├── auth.py             # Authentication
│   │   └── predict.py          # Prediction endpoints
│   │
│   ├── 📂 schemas/
│   │   ├── __init__.py
│   │   └── prediction.py       # Pydantic schemas
│   │
│   ├── 📂 utils/
│   │   ├── __init__.py
│   │   ├── image.py            # Image utilities
│   │   ├── data.py             # Data utilities
│   │   └── visualization.py    # Visualization
│   │
│   └── cache.py                # Caching
│
├── 📂 models/
│   ├── pretrained_yolo.pt      # Pre-trained weights
│   ├── model_v1.pt             # Model version 1
│   └── model_v2.pt             # Model version 2
│
├── 📂 data/
│   ├── train/                  # Training dataset
│   ├── val/                    # Validation dataset
│   ├── test/                   # Test dataset
│   └── annotations.json        # Annotations
│
├── 📂 notebooks/
│   ├── training.ipynb          # Training notebook
│   ├── evaluation.ipynb        # Evaluation notebook
│   └── visualization.ipynb     # Visualization notebook
│
├── 📂 tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_inference.py       # Inference tests
│   ├── test_preprocessing.py   # Preprocessing tests
│   ├── test_training.py        # Training tests
│   ├── test_api.py             # API tests
│   └── test_batch_processor.py # Batch processing tests
│
├── main.py                     # FastAPI application
├── train.py                    # Training script
├── requirements.txt            # Dependencies
├── .env.example                # Example environment
├── Dockerfile                  # Container config
├── docker-compose.yml          # Multi-service setup
├── .github/workflows/ci-cd.yml # GitHub Actions
│
└── README.md                   # Project documentation
```

### Key ML-Specific Files

| File | Purpose |
|------|---------|
| `app/ml/model_loader.py` | Load PyTorch models |
| `app/ml/preprocessor.py` | Image preprocessing pipeline |
| `app/ml/trainer.py` | Training loop and utilities |
| `app/ml/inference.py` | Model inference code |
| `app/ml/ensemble.py` | Ensemble prediction methods |
| `app/ml/versioning.py` | Model version management |
| `app/ml/batch_processor.py` | Batch processing pipeline |
| `models/` | Stored model weights |
| `data/` | Training/validation data |
| `train.py` | Standalone training script |

---

## TensorFlow Projects (31-40)

### Standard Structure for Each Project

```
31_traffic_sign_detection/
│
├── 📂 app/
│   ├── __init__.py
│   │
│   ├── 📂 core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   │
│   ├── 📂 models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── prediction.py
│   │
│   ├── 📂 ml/
│   │   ├── __init__.py
│   │   ├── model_loader.py     # Load TensorFlow models
│   │   ├── preprocessor.py     # Image preprocessing
│   │   ├── trainer.py          # Training with Keras
│   │   ├── inference.py        # Model inference
│   │   ├── transfer_learning.py # Transfer learning
│   │   ├── ensemble.py         # Model ensemble
│   │   ├── versioning.py       # Model versioning
│   │   ├── metrics.py          # Evaluation metrics
│   │   ├── augmentation.py     # Data augmentation
│   │   └── batch_processor.py  # Batch processing
│   │
│   ├── 📂 routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── predict.py
│   │
│   ├── 📂 schemas/
│   │   ├── __init__.py
│   │   └── prediction.py
│   │
│   ├── 📂 utils/
│   │   ├── __init__.py
│   │   ├── image.py
│   │   ├── callbacks.py        # Custom callbacks
│   │   └── visualization.py
│   │
│   └── cache.py
│
├── 📂 models/
│   ├── saved_model/            # TensorFlow SavedModel format
│   │   ├── assets/
│   │   ├── saved_model.pb
│   │   └── variables/
│   ├── model_v1.h5            # HDF5 format
│   └── model_v2.h5
│
├── 📂 data/
│   ├── train/
│   ├── val/
│   ├── test/
│   └── classes.json
│
├── 📂 notebooks/
│   ├── training.ipynb
│   ├── transfer_learning.ipynb
│   ├── evaluation.ipynb
│   └── visualization.ipynb
│
├── 📂 tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_inference.py
│   ├── test_preprocessing.py
│   ├── test_training.py
│   ├── test_transfer_learning.py
│   ├── test_api.py
│   └── test_batch_processor.py
│
├── main.py
├── train.py
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── .github/workflows/ci-cd.yml
│
└── README.md
```

---

## Monetization Tools (41-60)

### Standard Structure for Each Project

```
41_stock_price_analyzer/
│
├── 📂 app/
│   ├── __init__.py
│   │
│   ├── 📂 core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   │
│   ├── 📂 models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── analysis.py         # Analysis results model
│   │   └── stock_data.py       # Stock data model
│   │
│   ├── 📂 routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── analysis.py         # Analysis endpoints
│   │
│   ├── 📂 schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── analysis.py
│   │
│   ├── 📂 services/
│   │   ├── __init__.py
│   │   ├── stock_service.py    # Stock data fetching
│   │   ├── analysis_service.py # Analysis logic
│   │   ├── prediction_service.py # Predictions
│   │   └── notification_service.py # Alerts
│   │
│   ├── 📂 tasks/
│   │   ├── __init__.py
│   │   └── scheduled_tasks.py  # Celery tasks
│   │
│   ├── 📂 utils/
│   │   ├── __init__.py
│   │   ├── data_fetcher.py     # Data fetching
│   │   ├── calculator.py       # Calculations
│   │   ├── formatter.py        # Response formatting
│   │   ├── parser.py           # Data parsing
│   │   └── external_api.py     # External API calls
│   │
│   ├── cache.py
│   ├── rate_limiter.py         # Rate limiting
│   └── exceptions.py
│
├── 📂 tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_services.py
│   ├── test_analysis.py
│   ├── test_prediction.py
│   ├── test_api.py
│   └── test_rate_limiting.py
│
├── 📂 scripts/
│   ├── fetch_initial_data.py
│   ├── backfill_data.py
│   └── generate_reports.py
│
├── main.py
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── .github/workflows/ci-cd.yml
│
└── README.md
```

---

## Frontend Structure

### React Frontend

```
frontend/react-app/
│
├── 📂 src/
│   ├── 📂 pages/
│   │   ├── LoginPage.tsx       # Login/Register page
│   │   ├── DashboardPage.tsx   # Dashboard
│   │   └── ItemsPage.tsx       # Items management
│   │
│   ├── 📂 components/
│   │   ├── Navbar.tsx          # Navigation bar
│   │   ├── Sidebar.tsx         # Sidebar menu
│   │   ├── FormInput.tsx       # Form input component
│   │   ├── LoadingSpinner.tsx  # Loading indicator
│   │   └── ErrorBoundary.tsx   # Error boundary
│   │
│   ├── 📂 stores/
│   │   ├── authStore.ts        # Zustand auth store
│   │   ├── uiStore.ts          # UI state store
│   │   └── apiStore.ts         # API state store
│   │
│   ├── 📂 api/
│   │   ├── client.ts           # Axios instance with JWT
│   │   ├── userApi.ts          # User API calls
│   │   ├── itemApi.ts          # Item API calls
│   │   └── authApi.ts          # Auth API calls
│   │
│   ├── 📂 types/
│   │   ├── api.ts              # API type definitions
│   │   ├── models.ts           # Data models
│   │   └── common.ts           # Common types
│   │
│   ├── 📂 hooks/
│   │   ├── useAuth.ts          # Auth hook
│   │   ├── useFetch.ts         # Data fetching hook
│   │   └── useForm.ts          # Form handling hook
│   │
│   ├── 📂 utils/
│   │   ├── validation.ts       # Form validation
│   │   ├── formatters.ts       # Data formatting
│   │   ├── storage.ts          # LocalStorage utilities
│   │   └── date.ts             # Date utilities
│   │
│   ├── 📂 styles/
│   │   ├── App.css
│   │   ├── pages.css
│   │   ├── components.css
│   │   └── variables.css
│   │
│   ├── App.tsx                 # Main app component
│   ├── App.css                 # App styles
│   ├── index.tsx               # Entry point
│   └── index.css               # Global styles
│
├── 📂 public/
│   ├── index.html              # HTML template
│   ├── favicon.ico
│   └── manifest.json           # PWA manifest
│
├── 📂 tests/
│   ├── App.test.tsx
│   ├── setupTests.ts
│   └── mocks/
│
├── .env.example                # Example environment
├── .env.local                  # Local environment (gitignored)
├── .env.production             # Production environment
├── package.json                # Dependencies
├── tsconfig.json               # TypeScript config
├── vite.config.ts              # Vite config
├── eslint.config.js            # ESLint config
├── .prettierrc                 # Prettier config
├── Dockerfile                  # Container config
├── docker-compose.yml          # Development setup
│
└── README.md                   # Frontend documentation
```

### Vue Frontend

```
frontend/vue-app/
│
├── 📂 src/
│   ├── 📂 pages/
│   │   ├── LoginPage.vue       # Login/Register
│   │   ├── DashboardPage.vue   # Dashboard
│   │   └── ItemsPage.vue       # Items management
│   │
│   ├── 📂 components/
│   │   ├── Navbar.vue
│   │   ├── Sidebar.vue
│   │   ├── FormInput.vue
│   │   ├── LoadingSpinner.vue
│   │   └── ErrorAlert.vue
│   │
│   ├── 📂 stores/
│   │   ├── auth.ts             # Pinia auth store
│   │   ├── ui.ts               # UI state store
│   │   └── api.ts              # API state store
│   │
│   ├── 📂 api/
│   │   ├── client.ts           # Axios instance
│   │   ├── userApi.ts
│   │   ├── itemApi.ts
│   │   └── authApi.ts
│   │
│   ├── 📂 types/
│   │   ├── api.ts
│   │   ├── models.ts
│   │   └── common.ts
│   │
│   ├── 📂 composables/
│   │   ├── useAuth.ts          # Auth composable
│   │   ├── useFetch.ts         # Data fetching
│   │   └── useForm.ts          # Form handling
│   │
│   ├── 📂 utils/
│   │   ├── validation.ts
│   │   ├── formatters.ts
│   │   ├── storage.ts
│   │   └── date.ts
│   │
│   ├── 📂 styles/
│   │   ├── main.css
│   │   ├── variables.css
│   │   └── components.css
│   │
│   ├── App.vue                 # Main component
│   ├── main.ts                 # Entry point
│   └── router.ts               # Vue Router config
│
├── 📂 public/
│   ├── index.html
│   ├── favicon.ico
│   └── manifest.json
│
├── 📂 tests/
│   ├── components/
│   └── stores/
│
├── .env.example
├── .env.local
├── .env.production
├── package.json
├── tsconfig.json
├── vite.config.ts
├── vitest.config.ts            # Vitest config
├── eslint.config.js
├── .prettierrc
├── Dockerfile
├── docker-compose.yml
│
└── README.md
```

---

## Infrastructure Structure

### Terraform Files

```
terraform/
│
├── 📄 main.tf
│   └── Contains:
│       - Terraform provider configuration
│       - Backend setup (S3 + DynamoDB)
│       - Provider version constraints
│
├── 📄 vpc.tf
│   └── Contains:
│       - VPC creation
│       - Subnet configuration (public/private)
│       - NAT Gateway
│       - Route tables
│       - Internet Gateway
│       - Security groups
│
├── 📄 rds.tf
│   └── Contains:
│       - RDS instance (PostgreSQL)
│       - DB subnet group
│       - KMS encryption key
│       - Enhanced monitoring
│       - Backup configuration
│       - Parameter group
│
├── 📄 redis.tf
│   └── Contains:
│       - ElastiCache cluster
│       - Redis security group
│       - Auth token configuration
│       - Encryption configuration
│       - Automatic failover
│
├── 📄 variables.tf
│   └── Contains:
│       - All input variables
│       - Variable descriptions
│       - Default values
│       - Variable types
│
├── 📄 outputs.tf
│   └── Contains:
│       - Output values for resources
│       - RDS endpoint
│       - Redis endpoint
│       - VPC ID
│       - Subnet IDs
│
├── 📂 modules/
│   │
│   ├── 📂 iam/
│   │   ├── main.tf            # IAM roles
│   │   └── variables.tf       # Input variables
│   │
│   ├── 📂 elastic_beanstalk/
│   │   ├── main.tf            # EB application
│   │   └── variables.tf
│   │
│   └── 📂 alb/
│       ├── main.tf            # Load balancer
│       └── variables.tf
│
├── 📄 development.tfvars
│   └── Contains:
│       - Small instance types
│       - Single AZ
│       - Minimal backup
│       - Lower costs
│
├── 📄 staging.tfvars
│   └── Contains:
│       - Medium instance types
│       - Multi-AZ configuration
│       - Standard backup
│
└── 📄 production.tfvars
    └── Contains:
        - Large instance types
        - Multi-AZ with failover
        - Enhanced backups
        - High availability
```

---

## Documentation Files

```
docs/
│
├── 📄 index.html               # Landing page
├── 📄 postman_collection.json  # Postman collection
│
├── 📂 guides/
│   ├── authentication.md       # JWT auth guide
│   ├── endpoints.md            # API endpoints list
│   ├── examples.md             # Code examples
│   └── webhooks.md             # Webhook guide
│
├── 📂 architecture/
│   ├── backend.md
│   ├── frontend.md
│   └── devops.md
│
└── 📂 deployment/
    ├── aws.md
    ├── heroku.md
    ├── docker.md
    └── kubernetes.md
```

---

## Common File Purposes

### Configuration Files

```
.env.example          # Template for environment variables
.env.local            # Local development (gitignored)
.env.production       # Production configuration (gitignored)
pyproject.toml        # Python project metadata
setup.py              # Package setup configuration
requirements.txt      # Python dependencies
package.json          # Node.js dependencies (frontend)
tsconfig.json         # TypeScript configuration
```

### Build & Container Files

```
Dockerfile            # Container image definition
docker-compose.yml    # Multi-container orchestration
.dockerignore         # Docker build ignore
```

### Version Control

```
.gitignore           # Git ignore rules
.gitattributes       # Git attributes
```

### Testing & Quality

```
pytest.ini           # Pytest configuration
.flake8              # Flake8 linting rules
mypy.ini             # Type checking configuration
.coveragerc          # Coverage report configuration
vitest.config.ts     # Vue test configuration (frontend)
```

### Code Style

```
.prettierrc           # Code formatting rules
.editorconfig         # Editor configuration
eslint.config.js     # ESLint rules (JavaScript/TypeScript)
pyproject.toml       # Black configuration
```

---

## File Navigation Tips

### Finding API Endpoints

1. **FastAPI**: Look in `app/routes/*.py`
2. **Django**: Look in `app/views/` or `app/viewsets/`
3. **Check for decorators**: `@app.get()`, `@app.post()`, `@api_view()`

### Finding Models

1. **FastAPI**: `app/models/`
2. **Django**: `app/models/`
3. **PyTorch/TensorFlow**: `app/ml/model_loader.py`

### Finding Tests

1. **All projects**: `tests/` directory
2. **Look for patterns**: `test_*.py` or `*_test.py`
3. **Fixtures**: `conftest.py`

### Finding Configuration

1. **Environment**: `.env.example` or `.env.local`
2. **App Config**: `app/core/config.py` (FastAPI) or `settings.py` (Django)
3. **Infrastructure**: `terraform/*.tf`

---

## Next Steps

1. **Choose a project**: Select from 01-60
2. **Explore its structure**: Follow the patterns above
3. **Read its README**: Each project has detailed docs
4. **Check main entry point**: `main.py` (FastAPI) or `manage.py` (Django)
5. **Look at tests**: Understand expected behavior
6. **Check API documentation**: Swagger/ReDoc

---

**Happy exploring! 🗺️**
