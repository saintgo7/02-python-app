"""Helper functions"""

from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any
from decimal import Decimal


def get_current_timestamp() -> datetime:
    """Get current timestamp in UTC"""
    return datetime.now(timezone.utc)


def add_days(date: datetime, days: int) -> datetime:
    """Add days to date"""
    return date + timedelta(days=days)


def days_until(date: datetime) -> int:
    """Get number of days until date"""
    delta = date - get_current_timestamp()
    return delta.days


def is_past(date: datetime) -> bool:
    """Check if date is in the past"""
    return date < get_current_timestamp()


def is_future(date: datetime) -> bool:
    """Check if date is in the future"""
    return date > get_current_timestamp()


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format amount as currency"""
    if currency == "USD":
        return f"${amount:,.2f}"
    elif currency == "EUR":
        return f"€{amount:,.2f}"
    elif currency == "GBP":
        return f"£{amount:,.2f}"
    else:
        return f"{amount:,.2f} {currency}"


def calculate_percentage(part: float, whole: float) -> float:
    """Calculate percentage"""
    if whole == 0:
        return 0.0

    return (part / whole) * 100


def round_price(price: float, decimals: int = 2) -> float:
    """Round price to specified decimals"""
    return round(price, decimals)


def paginate(total: int, skip: int, limit: int) -> Dict[str, Any]:
    """Calculate pagination info"""
    total_pages = (total + limit - 1) // limit  # Ceiling division
    current_page = (skip // limit) + 1

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "current_page": current_page,
        "total_pages": total_pages,
        "has_next": current_page < total_pages,
        "has_previous": current_page > 1
    }


def merge_dicts(dict1: dict, dict2: dict) -> dict:
    """Merge two dictionaries"""
    result = dict1.copy()
    result.update(dict2)
    return result


def filter_dict(data: dict, keys: list) -> dict:
    """Filter dictionary to include only specified keys"""
    return {k: v for k, v in data.items() if k in keys}


def exclude_dict(data: dict, keys: list) -> dict:
    """Filter dictionary to exclude specified keys"""
    return {k: v for k, v in data.items() if k not in keys}


def generate_reference_number(prefix: str = "REF") -> str:
    """Generate unique reference number"""
    timestamp = int(datetime.now(timezone.utc).timestamp() * 1000)
    return f"{prefix}-{timestamp}"


def get_status_badge(status: str) -> Dict[str, str]:
    """Get badge info for status"""
    status_map = {
        "pending": {"color": "warning", "label": "Pending"},
        "confirmed": {"color": "success", "label": "Confirmed"},
        "completed": {"color": "info", "label": "Completed"},
        "cancelled": {"color": "danger", "label": "Cancelled"},
        "paid": {"color": "success", "label": "Paid"},
        "unpaid": {"color": "danger", "label": "Unpaid"},
        "partial": {"color": "warning", "label": "Partial Payment"},
        "active": {"color": "success", "label": "Active"},
        "inactive": {"color": "secondary", "label": "Inactive"},
    }

    return status_map.get(status, {"color": "secondary", "label": status})
