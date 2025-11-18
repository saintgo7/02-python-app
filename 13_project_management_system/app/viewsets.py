from rest_framework import viewsets, status
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
