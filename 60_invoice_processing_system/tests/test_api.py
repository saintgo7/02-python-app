import pytest
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
