"""Custom exceptions and error handling"""

from fastapi import HTTPException, status


class ApplicationError(Exception):
    """Base application error"""

    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        """Initialize error"""
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ValidationError(ApplicationError):
    """Validation error"""

    def __init__(self, message: str):
        """Initialize validation error"""
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class NotFoundError(ApplicationError):
    """Resource not found error"""

    def __init__(self, message: str = "Resource not found"):
        """Initialize not found error"""
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class UnauthorizedError(ApplicationError):
    """Unauthorized access error"""

    def __init__(self, message: str = "Unauthorized"):
        """Initialize unauthorized error"""
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)


class ForbiddenError(ApplicationError):
    """Forbidden access error"""

    def __init__(self, message: str = "Access denied"):
        """Initialize forbidden error"""
        super().__init__(message, status.HTTP_403_FORBIDDEN)


class ConflictError(ApplicationError):
    """Conflict error (e.g., duplicate entry)"""

    def __init__(self, message: str = "Conflict"):
        """Initialize conflict error"""
        super().__init__(message, status.HTTP_409_CONFLICT)


class BookingError(ApplicationError):
    """Booking-related error"""

    def __init__(self, message: str):
        """Initialize booking error"""
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class PaymentError(ApplicationError):
    """Payment-related error"""

    def __init__(self, message: str):
        """Initialize payment error"""
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class PackageError(ApplicationError):
    """Package-related error"""

    def __init__(self, message: str):
        """Initialize package error"""
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


def to_http_exception(error: ApplicationError) -> HTTPException:
    """Convert application error to HTTP exception"""
    return HTTPException(
        status_code=error.status_code,
        detail=error.message
    )
