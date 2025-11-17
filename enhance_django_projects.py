#!/usr/bin/env python3
"""
Django Project Enhancement
Adds advanced features to Django projects:
- Advanced filtering, searching, sorting, pagination
- Redis caching
- Custom model methods and querysets
"""

from pathlib import Path

def generate_django_advanced_queryset() -> str:
    """Generate advanced Django QuerySet with search, filter, sort"""
    return '''from django.db.models import QuerySet, Q
from django.core.paginator import Paginator
from typing import List, Optional, Dict, Any


class AdvancedQuerySet(QuerySet):
    """Advanced QuerySet with filtering, searching, sorting"""

    def search(self, search_fields: List[str], query: str) -> 'AdvancedQuerySet':
        """Search across multiple fields"""
        if not query:
            return self

        q_objects = Q()
        for field in search_fields:
            q_objects |= Q(**{f"{field}__icontains": query})

        return self.filter(q_objects)

    def advanced_filter(self, **kwargs) -> 'AdvancedQuerySet':
        """Advanced filtering with support for range queries"""
        filters = {}
        for key, value in kwargs.items():
            if value is not None:
                filters[key] = value

        return self.filter(**filters)

    def sorted_by(self, sort_field: str = "-created_at", sort_order: str = "desc") -> 'AdvancedQuerySet':
        """Sort by field with direction"""
        if sort_order.lower() == "desc":
            return self.order_by(f"-{sort_field}")
        else:
            return self.order_by(sort_field)

    def paginate(self, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """Paginate results"""
        paginator = Paginator(self, per_page)
        page_obj = paginator.get_page(page)

        return {
            "total": paginator.count,
            "pages": paginator.num_pages,
            "page": page,
            "per_page": per_page,
            "items": list(page_obj),
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous()
        }

    def with_counts(self) -> QuerySet:
        """Add related counts"""
        from django.db.models import Count
        return self.annotate(total_count=Count("id"))
'''


def generate_django_model_manager() -> str:
    """Generate Django Model Manager with advanced methods"""
    return '''from django.db import models


class AdvancedManager(models.Manager):
    """Manager with advanced query methods"""

    def get_queryset(self):
        return AdvancedQuerySet(self.model, using=self._db)

    def search(self, search_fields, query):
        return self.get_queryset().search(search_fields, query)

    def advanced_filter(self, **kwargs):
        return self.get_queryset().advanced_filter(**kwargs)

    def sorted_by(self, sort_field="-created_at", sort_order="desc"):
        return self.get_queryset().sorted_by(sort_field, sort_order)

    def get_paginated(self, page=1, per_page=10):
        return self.get_queryset().paginate(page, per_page)
'''


def generate_django_filter_viewset() -> str:
    """Generate Django filter ViewSet"""
    return '''from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q


class AdvancedViewSet(viewsets.ModelViewSet):
    """Advanced ViewSet with filtering, searching, sorting"""

    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["created_at", "updated_at", "name"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().filter(user=user)

        # Advanced search
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        # Status filtering
        status = self.request.query_params.get("status")
        if status:
            queryset = queryset.filter(status=status)

        # Date range filtering
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)

        return queryset

    @action(detail=False, methods=["get"])
    def stats(self, request):
        """Get statistics"""
        queryset = self.get_queryset()
        stats = {
            "total": queryset.count(),
            "active": queryset.filter(is_active=True).count(),
            "inactive": queryset.filter(is_active=False).count(),
        }
        return Response(stats)

    @action(detail=False, methods=["get"])
    def export(self, request):
        """Export data"""
        import csv
        from django.http import HttpResponse

        queryset = self.get_queryset()
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=export.csv"

        writer = csv.writer(response)
        writer.writerow(["ID", "Name", "Description", "Created", "Updated"])

        for item in queryset:
            writer.writerow([item.id, item.name, item.description, item.created_at, item.updated_at])

        return response
'''


def generate_django_redis_cache() -> str:
    """Generate Django Redis caching"""
    return '''from django.core.cache import cache
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
'''


def generate_django_signals() -> str:
    """Generate Django signals for cache invalidation"""
    return '''from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache


@receiver(post_save)
def invalidate_cache_on_save(sender, instance, created, **kwargs):
    """Invalidate cache when model is saved"""
    model_name = sender.__name__
    cache.delete_many([f"{model_name}:*"])

    if hasattr(instance, "user_id"):
        cache.delete_many([f"*:{instance.user_id}:*"])


@receiver(post_delete)
def invalidate_cache_on_delete(sender, instance, **kwargs):
    """Invalidate cache when model is deleted"""
    model_name = sender.__name__
    cache.delete_many([f"{model_name}:*"])

    if hasattr(instance, "user_id"):
        cache.delete_many([f"*:{instance.user_id}:*"])
'''


def generate_django_enhanced_settings() -> str:
    """Generate enhanced Django settings snippet"""
    return '''# Cache Configuration
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PARSER_KWARGS": {"encoding": "utf8"},
            "CONNECTION_POOL_KWARGS": {"max_connections": 50},
        },
        "KEY_PREFIX": "django_cache",
        "TIMEOUT": 300,
    }
}

# Enable query optimization
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda r: DEBUG,
}

# REST Framework settings
REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

# Database connection pooling
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "CONN_MAX_AGE": 600,
        "CONN_HEALTH_CHECKS": True,
        "OPTIONS": {
            "connect_timeout": 10,
        }
    }
}
'''


def enhance_django_projects():
    """Enhance Django projects"""
    django_projects = [
        "11_multi_tenant_crm",
        "12_blog_platform",
        "13_project_management_system",
        "14_inventory_management",
        "15_customer_support_portal",
        "16_event_booking_system",
        "17_subscription_billing_platform",
        "18_learning_management_system",
        "19_real_estate_listing_platform",
        "20_social_network_backend",
    ]

    print("🚀 Enhancing Django Projects with Advanced Features...")
    print("=" * 70)

    for project in django_projects:
        base_path = Path(f"/home/user/02-python-app/{project}")
        print(f"[{project}]", end=" ", flush=True)

        try:
            # Create advanced queryset
            queryset_code = generate_django_advanced_queryset()
            (base_path / "app" / "querysets.py").write_text(queryset_code)

            # Create manager
            manager_code = generate_django_model_manager()
            (base_path / "app" / "managers.py").write_text(manager_code)

            # Create filter viewset
            filter_code = generate_django_filter_viewset()
            (base_path / "app" / "viewsets.py").write_text(filter_code)

            # Create cache utilities
            cache_code = generate_django_redis_cache()
            (base_path / "app" / "cache.py").write_text(cache_code)

            # Create signals
            signals_code = generate_django_signals()
            (base_path / "app" / "signals.py").write_text(signals_code)

            # Create settings snippet
            settings_code = generate_django_enhanced_settings()
            (base_path / "app" / "settings_enhanced.py").write_text(settings_code)

            # Update requirements.txt
            enhanced_requirements = '''Django==4.2.8
djangorestframework==3.14.0
django-cors-headers==4.3.1
django-environ==0.21.0
psycopg2-binary==2.9.9
celery==5.3.4
redis==5.0.1
pytest-django==4.7.0
python-decouple==3.8

# Enhanced features
django-redis==5.4.0
django-filter==23.5
django-rest-framework-simplejwt==5.3.2
djangorestframework-simplejwt==5.3.2
'''
            (base_path / "requirements.txt").write_text(enhanced_requirements)

            print("✅")
        except Exception as e:
            print(f"❌ Error: {e}")

    print("=" * 70)
    print("✨ Django projects enhanced!")


if __name__ == "__main__":
    enhance_django_projects()
