from typing import Any, Optional, List, Dict
from datetime import datetime


class APIResponse:
    """Standard API response model"""

    def __init__(
        self,
        data: Any = None,
        message: str = "Success",
        status: str = "success",
        code: int = 200,
        timestamp: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        self.data = data
        self.message = message
        self.status = status
        self.code = code
        self.timestamp = timestamp or datetime.utcnow().isoformat()
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "data": self.data,
            "message": self.message,
            "status": self.status,
            "code": self.code,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }

    @staticmethod
    def success(data: Any = None, message: str = "Success", **kwargs) -> "APIResponse":
        return APIResponse(data=data, message=message, status="success", code=200, **kwargs)

    @staticmethod
    def error(message: str = "Error", code: int = 400, **kwargs) -> "APIResponse":
        return APIResponse(message=message, status="error", code=code, **kwargs)

    @staticmethod
    def paginated(
        items: List,
        total: int,
        page: int = 1,
        per_page: int = 10,
        **kwargs
    ) -> "APIResponse":
        return APIResponse(
            data=items,
            message="Success",
            status="success",
            code=200,
            metadata={
                "total": total,
                "page": page,
                "per_page": per_page,
                "pages": (total + per_page - 1) // per_page
            },
            **kwargs
        )
