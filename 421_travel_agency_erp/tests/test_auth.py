"""Authentication tests"""

import pytest
from app.models import UserRole


def test_register_user(client):
    """Test user registration"""
    response = client.post(
        "/auth/register",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "TestPassword123!",
            "full_name": "New User",
            "role": UserRole.CUSTOMER.value
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"


def test_register_duplicate_email(client, test_user):
    """Test registration with duplicate email"""
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "newusername",
            "password": "TestPassword123!",
            "full_name": "Another User",
            "role": UserRole.CUSTOMER.value
        }
    )

    assert response.status_code == 400


def test_login_success(client, test_user):
    """Test successful login"""
    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_email(client):
    """Test login with invalid email"""
    response = client.post(
        "/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "password"
        }
    )

    assert response.status_code == 401


def test_login_invalid_password(client, test_user):
    """Test login with invalid password"""
    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "WrongPassword123!"
        }
    )

    assert response.status_code == 401


def test_get_current_user(client, test_user):
    """Test getting current user info"""
    # First login
    login_response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
    )

    token = login_response.json()["access_token"]

    # Get current user
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
