from functools import wraps
from time import time
from typing import Callable, Dict, Tuple
import threading


class RateLimiter:
    """Rate limiter with sliding window"""

    def __init__(self, max_calls: int = 100, time_window: int = 60):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls: Dict[str, list] = {}
        self.lock = threading.Lock()

    def is_allowed(self, key: str) -> Tuple[bool, Dict]:
        """Check if request is allowed"""
        with self.lock:
            now = time()

            if key not in self.calls:
                self.calls[key] = []

            # Remove old calls outside window
            self.calls[key] = [call_time for call_time in self.calls[key]
                               if now - call_time < self.time_window]

            if len(self.calls[key]) < self.max_calls:
                self.calls[key].append(now)
                return True, {"remaining": self.max_calls - len(self.calls[key])}
            else:
                return False, {"retry_after": int(self.calls[key][0] + self.time_window - now)}

    def rate_limit(self, max_calls: int = 100, time_window: int = 60):
        """Decorator for rate limiting"""
        limiter = RateLimiter(max_calls, time_window)

        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, user_id: str = "anonymous", **kwargs):
                allowed, info = limiter.is_allowed(user_id)

                if not allowed:
                    return {
                        "status": "error",
                        "message": "Rate limit exceeded",
                        "retry_after": info["retry_after"]
                    }

                result = func(*args, **kwargs)

                # Add rate limit headers
                result["X-RateLimit-Remaining"] = info.get("remaining", 0)
                return result

            return wrapper
        return decorator


rate_limiter = RateLimiter()
