import pytest
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
