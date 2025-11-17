from django.core.cache import cache
from django.views.decorators.cache import cache_page
from functools import wraps
from typing import Callable


def cache_response(timeout: int = 300):
    """Cache decorator for views"""
    def decorator(view_func: Callable):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            cache_key = f"{view_func.__name__}:{request.user.id if request.user.is_authenticated else 'anon'}:{request.GET.urlencode()}"

            result = cache.get(cache_key)
            if result is not None:
                return result

            result = view_func(request, *args, **kwargs)
            cache.set(cache_key, result, timeout)

            return result

        return wrapper
    return decorator


def invalidate_user_cache(user_id: int):
    """Invalidate cache for specific user"""
    patterns = [
        f"*:{user_id}:*",
    ]
    cache.delete_many(patterns)


def invalidate_model_cache(model_name: str):
    """Invalidate cache for specific model"""
    cache.delete_many([f"{model_name}:*"])
