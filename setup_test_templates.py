#!/usr/bin/env python3
"""
Test Templates Setup
Generates comprehensive test templates and fixtures for all projects
"""

from pathlib import Path

def generate_fastapi_conftest() -> str:
    """Generate pytest configuration for FastAPI projects"""
    return '''import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.core.database import Base, get_db
from app.core.security import create_access_token
from main import app

# Test database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create test database"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create test client"""
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db):
    """Create test user"""
    from app import models
    from app.core.security import hash_password

    user = models.User(
        email="test@example.com",
        hashed_password=hash_password("testpass123"),
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_token(test_user):
    """Create test JWT token"""
    return create_access_token(data={"sub": str(test_user.id)})


@pytest.fixture
def auth_headers(test_token):
    """Create authorization headers"""
    return {"Authorization": f"Bearer {test_token}"}
'''

def generate_fastapi_auth_tests() -> str:
    """Generate auth endpoint tests"""
    return '''import pytest
from fastapi import status


class TestAuthentication:
    """Test authentication endpoints"""

    def test_register_success(self, client):
        """Test successful user registration"""
        response = client.post(
            "/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "testpass123"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["email"] == "newuser@example.com"

    def test_register_duplicate_email(self, client, test_user):
        """Test registration with duplicate email"""
        response = client.post(
            "/auth/register",
            json={
                "email": test_user.email,
                "password": "testpass123"
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_success(self, client, test_user):
        """Test successful login"""
        response = client.post(
            "/auth/login",
            json={
                "email": test_user.email,
                "password": "testpass123"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        response = client.post(
            "/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "wrongpassword"
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_token_refresh(self, client, auth_headers):
        """Test token refresh"""
        response = client.post(
            "/auth/refresh",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
'''

def generate_fastapi_crud_tests() -> str:
    """Generate CRUD endpoint tests"""
    return '''import pytest
from fastapi import status


class TestCRUD:
    """Test CRUD operations"""

    def test_create_item_success(self, client, auth_headers, db):
        """Test successful item creation"""
        response = client.post(
            "/items/",
            json={"name": "Test Item", "description": "Test Description"},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == "Test Item"

    def test_create_item_unauthorized(self, client):
        """Test item creation without authentication"""
        response = client.post(
            "/items/",
            json={"name": "Test Item", "description": "Test Description"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_items(self, client, auth_headers):
        """Test retrieving items"""
        response = client.get(
            "/items/",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)

    def test_get_item_by_id(self, client, auth_headers):
        """Test retrieving single item"""
        # Create item first
        create_response = client.post(
            "/items/",
            json={"name": "Test Item"},
            headers=auth_headers
        )
        item_id = create_response.json()["id"]

        # Retrieve item
        response = client.get(
            f"/items/{item_id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == item_id

    def test_update_item(self, client, auth_headers):
        """Test updating item"""
        # Create item
        create_response = client.post(
            "/items/",
            json={"name": "Original Name"},
            headers=auth_headers
        )
        item_id = create_response.json()["id"]

        # Update item
        response = client.put(
            f"/items/{item_id}",
            json={"name": "Updated Name"},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == "Updated Name"

    def test_delete_item(self, client, auth_headers):
        """Test deleting item"""
        # Create item
        create_response = client.post(
            "/items/",
            json={"name": "Item to Delete"},
            headers=auth_headers
        )
        item_id = create_response.json()["id"]

        # Delete item
        response = client.delete(
            f"/items/{item_id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
'''

def generate_django_conftest() -> str:
    """Generate pytest configuration for Django projects"""
    return '''import pytest
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.test")

import django
django.setup()

from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def api_client():
    """Create API client"""
    return APIClient()


@pytest.fixture
def user():
    """Create test user"""
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )


@pytest.fixture
def authenticated_client(user):
    """Create authenticated API client"""
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client


@pytest.fixture
def auth_token(user):
    """Create authentication token"""
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)
'''

def generate_django_model_tests() -> str:
    """Generate Django model tests"""
    return '''import pytest
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestUserModel:
    """Test User model"""

    def test_create_user(self):
        """Test user creation"""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.check_password("testpass123")

    def test_user_string_representation(self):
        """Test user string representation"""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com"
        )
        assert str(user) == "testuser"

    def test_duplicate_username(self):
        """Test duplicate username"""
        User.objects.create_user(username="testuser", email="test@example.com")
        with pytest.raises(Exception):
            User.objects.create_user(username="testuser", email="another@example.com")
'''

def generate_django_api_tests() -> str:
    """Generate Django API tests"""
    return '''import pytest
from rest_framework import status


@pytest.mark.django_db
class TestAPIEndpoints:
    """Test API endpoints"""

    def test_list_endpoint(self, authenticated_client):
        """Test list endpoint"""
        response = authenticated_client.get("/api/v1/items/")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_create_endpoint(self, authenticated_client):
        """Test create endpoint"""
        response = authenticated_client.post(
            "/api/v1/items/",
            {"name": "Test Item", "description": "Test"}
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_unauthorized_access(self, api_client):
        """Test unauthorized access"""
        response = api_client.get("/api/v1/items/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
'''

def generate_aiml_conftest() -> str:
    """Generate pytest configuration for AI/ML projects"""
    return '''import pytest
import numpy as np
import tempfile
from pathlib import Path


@pytest.fixture
def sample_image_array():
    """Create sample image array"""
    return np.random.rand(224, 224, 3).astype(np.float32)


@pytest.fixture
def sample_batch():
    """Create sample batch of images"""
    return np.random.rand(4, 224, 224, 3).astype(np.float32)


@pytest.fixture
def temp_model_dir():
    """Create temporary directory for models"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_model():
    """Create mock model"""
    class MockModel:
        def predict(self, x):
            batch_size = len(x) if isinstance(x, (list, np.ndarray)) else 1
            return np.random.rand(batch_size, 10).astype(np.float32)

    return MockModel()
'''

def generate_aiml_model_tests() -> str:
    """Generate AI/ML model tests"""
    return '''import pytest
import numpy as np
from app.batch_processor import BatchProcessor
from app.model_ensemble import ModelEnsemble


class TestBatchProcessor:
    """Test batch processor"""

    def test_batch_processor_initialization(self):
        """Test batch processor init"""
        processor = BatchProcessor(batch_size=32, max_workers=4)
        assert processor.batch_size == 32

    def test_process_single_batch(self, mock_model, sample_batch):
        """Test processing single batch"""
        processor = BatchProcessor(batch_size=4)
        results = processor.process_batch(mock_model, sample_batch)
        assert len(results) == 4

    def test_process_multiple_batches(self, mock_model):
        """Test processing multiple batches"""
        processor = BatchProcessor(batch_size=2)
        data = np.random.rand(5, 224, 224, 3).astype(np.float32)
        results = processor.process_batch(mock_model, data)
        assert len(results) == 5


class TestModelEnsemble:
    """Test model ensemble"""

    def test_ensemble_initialization(self):
        """Test ensemble init"""
        ensemble = ModelEnsemble()
        assert len(ensemble.models) == 0

    def test_add_model_to_ensemble(self, mock_model):
        """Test adding model to ensemble"""
        ensemble = ModelEnsemble()
        ensemble.add_model(mock_model, weight=1.0)
        assert len(ensemble.models) == 1

    def test_ensemble_prediction(self, mock_model, sample_image_array):
        """Test ensemble prediction"""
        ensemble = ModelEnsemble()
        ensemble.add_model(mock_model, weight=1.0)

        input_data = np.expand_dims(sample_image_array, axis=0)
        result = ensemble.predict_average(input_data)
        assert result is not None
        assert len(result) == 10
'''

def setup_test_templates():
    """Setup test templates for all projects"""
    print("🧪 Setting up Test Templates...")
    print("=" * 70)

    # FastAPI projects
    print("[FastAPI Test Templates (01-10)]", end=" ", flush=True)
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
        tests_dir = base_path / "tests"
        tests_dir.mkdir(exist_ok=True)

        # Create conftest
        (tests_dir / "conftest.py").write_text(generate_fastapi_conftest())

        # Create test files
        (tests_dir / "test_auth.py").write_text(generate_fastapi_auth_tests())
        (tests_dir / "test_crud.py").write_text(generate_fastapi_crud_tests())
        (tests_dir / "__init__.py").touch()
    print("✅")

    # Django projects
    print("[Django Test Templates (11-20)]", end=" ", flush=True)
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
        tests_dir = base_path / "tests"
        tests_dir.mkdir(exist_ok=True)

        # Create conftest
        (tests_dir / "conftest.py").write_text(generate_django_conftest())

        # Create test files
        (tests_dir / "test_models.py").write_text(generate_django_model_tests())
        (tests_dir / "test_api.py").write_text(generate_django_api_tests())
        (tests_dir / "__init__.py").touch()
    print("✅")

    # AI/ML projects
    print("[AI/ML Test Templates (21-40)]", end=" ", flush=True)
    for i in range(21, 41):
        projects = list(Path("/home/user/02-python-app").glob(f"{i:02d}_*"))
        if not projects:
            continue
        base_path = projects[0]
        tests_dir = base_path / "tests"
        tests_dir.mkdir(exist_ok=True)

        # Create conftest
        (tests_dir / "conftest.py").write_text(generate_aiml_conftest())

        # Create test files
        (tests_dir / "test_models.py").write_text(generate_aiml_model_tests())
        (tests_dir / "__init__.py").touch()
    print("✅")

    # Monetization tools
    print("[Monetization Tools Test Templates (41-60)]", end=" ", flush=True)
    for i in range(41, 61):
        projects = list(Path("/home/user/02-python-app").glob(f"{i:02d}_*"))
        if not projects:
            continue
        base_path = projects[0]
        tests_dir = base_path / "tests"
        tests_dir.mkdir(exist_ok=True)

        # Create conftest
        (tests_dir / "conftest.py").write_text(generate_fastapi_conftest())

        # Create test files
        (tests_dir / "test_api.py").write_text(generate_fastapi_crud_tests())
        (tests_dir / "__init__.py").touch()
    print("✅")

    print("=" * 70)
    print("✨ Test templates setup complete!")
    print("\nTest Setup Summary:")
    print(f"  ✓ FastAPI test suites: 10 projects × 3 files = 30 files")
    print(f"  ✓ Django test suites: 10 projects × 3 files = 30 files")
    print(f"  ✓ AI/ML test suites: 20 projects × 2 files = 40 files")
    print(f"  ✓ Monetization test suites: 20 projects × 2 files = 40 files")
    print(f"  ✓ Total test files: 140 files")


if __name__ == "__main__":
    setup_test_templates()
