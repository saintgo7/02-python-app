from django.db import models


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
