from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'tenants'

router = DefaultRouter()
router.register(r'tenants', TenantViewSet, basename='tenant')
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'deals', DealViewSet, basename='deal')
router.register(r'pipelines', PipelineViewSet, basename='pipeline')

urlpatterns = [
    path('', include(router.urls)),
]
