"""Validation utilities"""

import re
from datetime import datetime
from app.core.errors import ValidationError


class Validators:
    """Collection of validators"""

    @staticmethod
    def validate_email(email: str) -> str:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not re.match(pattern, email):
            raise ValidationError("Invalid email format")

        return email

    @staticmethod
    def validate_phone(phone: str) -> str:
        """Validate phone number format"""
        # Remove any non-digit characters except +
        cleaned = re.sub(r'[^\d+]', '', phone)

        if not cleaned or not 10 <= len(cleaned) <= 15:
            raise ValidationError("Invalid phone number format")

        return phone

    @staticmethod
    def validate_password(password: str) -> str:
        """Validate password strength"""
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters")

        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain lowercase letters")

        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain uppercase letters")

        if not re.search(r'\d', password):
            raise ValidationError("Password must contain numbers")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("Password must contain special characters")

        return password

    @staticmethod
    def validate_username(username: str) -> str:
        """Validate username format"""
        if not 3 <= len(username) <= 50:
            raise ValidationError("Username must be between 3 and 50 characters")

        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            raise ValidationError("Username can only contain letters, numbers, underscores, and hyphens")

        return username

    @staticmethod
    def validate_date_range(start_date: datetime, end_date: datetime) -> bool:
        """Validate date range"""
        if start_date >= end_date:
            raise ValidationError("Start date must be before end date")

        return True

    @staticmethod
    def validate_price(price: float) -> float:
        """Validate price"""
        if price <= 0:
            raise ValidationError("Price must be greater than 0")

        if price > 1000000:  # Maximum price limit
            raise ValidationError("Price exceeds maximum limit")

        return price

    @staticmethod
    def validate_rating(rating: int) -> int:
        """Validate rating"""
        if not 1 <= rating <= 5:
            raise ValidationError("Rating must be between 1 and 5")

        return rating

    @staticmethod
    def validate_participants(participants: int, max_participants: int) -> int:
        """Validate participant count"""
        if participants <= 0:
            raise ValidationError("Number of participants must be at least 1")

        if participants > max_participants:
            raise ValidationError(f"Number of participants cannot exceed {max_participants}")

        return participants

    @staticmethod
    def validate_string_length(value: str, min_length: int = 1, max_length: int = 255) -> str:
        """Validate string length"""
        if not min_length <= len(value) <= max_length:
            raise ValidationError(
                f"String length must be between {min_length} and {max_length} characters"
            )

        return value
