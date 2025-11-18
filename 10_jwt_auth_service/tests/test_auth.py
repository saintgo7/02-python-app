import pytest
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
