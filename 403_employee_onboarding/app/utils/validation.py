"""Input validation utilities for production applications."""

import re
from urllib.parse import urlparse

class ValidationUtils:
    """Collection of validation helper methods"""
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    PHONE_PATTERN = re.compile(r'^\+?1?\d{9,15}$')

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        if not email or len(email) > 254:
            return False
        return bool(ValidationUtils.EMAIL_PATTERN.match(email))

    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format"""
        try:
            result = urlparse(url)
            return all([result.scheme in ['http', 'https'], result.netloc])
        except Exception:
            return False

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format"""
        clean_phone = phone.replace('-', '').replace(' ', '')
        return bool(ValidationUtils.PHONE_PATTERN.match(clean_phone))

    @staticmethod
    def sanitize_string(value: str, max_length: int = 1000) -> str:
        """Sanitize string input"""
        if not isinstance(value, str):
            return str(value)
        value = value.replace('\x00', '')
        value = value[:max_length]
        value = ' '.join(value.split())
        return value

    @staticmethod
    def validate_length(value: str, min_len: int = 0, max_len: int = 1000) -> bool:
        """Validate string length"""
        if not isinstance(value, str):
            return False
        return min_len <= len(value) <= max_len

    @staticmethod
    def validate_password(password: str, min_length: int = 8):
        """Validate password strength"""
        if len(password) < min_length:
            return False, f"Password must be at least {min_length} characters"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        if not re.search(r'\d', password):
            return False, "Password must contain at least one digit"
        return True, "Password is strong"
