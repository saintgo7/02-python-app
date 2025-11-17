from django.db.models import QuerySet, Q
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
