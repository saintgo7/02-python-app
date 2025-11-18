"""Travel package tests"""

import pytest
from app.models import UserRole


def test_list_packages(client, test_package):
    """Test listing packages"""
    response = client.get("/packages/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == "Test Package"


def test_get_package(client, test_package):
    """Test getting package details"""
    response = client.get(f"/packages/{test_package.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_package.id
    assert data["name"] == "Test Package"


def test_get_nonexistent_package(client):
    """Test getting nonexistent package"""
    response = client.get("/packages/99999")

    assert response.status_code == 404


def test_create_package_as_admin(client, test_admin):
    """Test package creation as admin"""
    # Login as admin
    login_response = client.post(
        "/auth/login",
        json={
            "email": "admin@example.com",
            "password": "AdminPassword123!"
        }
    )

    token = login_response.json()["access_token"]

    # Create package
    response = client.post(
        "/packages/",
        json={
            "name": "New Package",
            "description": "New Description",
            "destination": "New Destination",
            "duration_days": 5,
            "price_per_person": 500.0,
            "max_participants": 20,
            "included_services": "Hotel, Food"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Package"


def test_create_package_as_customer(client, test_user):
    """Test package creation as customer (should fail)"""
    # Login as customer
    login_response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
    )

    token = login_response.json()["access_token"]

    # Try to create package
    response = client.post(
        "/packages/",
        json={
            "name": "New Package",
            "description": "New Description",
            "destination": "New Destination",
            "duration_days": 5,
            "price_per_person": 500.0,
            "max_participants": 20
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403


def test_search_packages_by_destination(client, test_package):
    """Test searching packages by destination"""
    response = client.get(
        "/packages/",
        params={"destination": "Test Destination"}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["destination"] == "Test Destination"
