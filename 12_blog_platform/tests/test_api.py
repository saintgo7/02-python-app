import pytest
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
