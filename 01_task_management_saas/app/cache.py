import redis
import json
from typing import Any, Optional, Callable
from functools import wraps
from config import settings
import hashlib
import inspect

class RedisCache:
    """Redis cache wrapper"""

    def __init__(self, redis_url: str = "redis://localhost:6379/0", ttl: int = 3600):
        self.redis_url = redis_url
        self.ttl = ttl
        try:
            self.client = redis.from_url(redis_url, decode_responses=True)
            self.client.ping()
            print("Redis connected successfully")
        except Exception as e:
            print(f"Redis connection failed: {e}")
            self.client = None

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.client:
            return None

        try:
            value = self.client.get(key)
            if value:
                return json.loads(value)
        except Exception as e:
            print(f"Cache get error: {e}")

        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache"""
        if not self.client:
            return False

        try:
            ttl = ttl or self.ttl
            self.client.setex(key, ttl, json.dumps(value))
            return True
        except Exception as e:
            print(f"Cache set error: {e}")

        return False

    def delete(self, key: str) -> bool:
        """Delete value from cache"""
        if not self.client:
            return False

        try:
            self.client.delete(key)
            return True
        except Exception as e:
            print(f"Cache delete error: {e}")

        return False

    def clear(self) -> bool:
        """Clear all cache"""
        if not self.client:
            return False

        try:
            self.client.flushdb()
            return True
        except Exception as e:
            print(f"Cache clear error: {e}")

        return False

    def generate_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate cache key"""
        key_parts = [prefix] + [str(arg) for arg in args]
        kwargs_str = json.dumps(kwargs, sort_keys=True)
        key_hash = hashlib.md5(kwargs_str.encode()).hexdigest()
        return ":".join(key_parts) + f":{key_hash}"


# Cache decorator
cache = RedisCache()


def cached(prefix: str, ttl: int = 3600):
    """Cache decorator for functions"""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = cache.generate_key(prefix, *args, **kwargs)

            # Try to get from cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value

            # Execute function
            result = func(*args, **kwargs)

            # Store in cache
            cache.set(cache_key, result, ttl)

            return result

        return wrapper
    return decorator


# Cache invalidation helper
def invalidate_cache(pattern: str = "*"):
    """Invalidate cache by pattern"""
    if not cache.client:
        return False

    try:
        keys = cache.client.keys(pattern)
        if keys:
            cache.client.delete(*keys)
        return True
    except Exception as e:
        print(f"Cache invalidation error: {e}")

    return False
