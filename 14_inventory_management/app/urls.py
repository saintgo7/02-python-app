from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'products'

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'warehouses', WarehouseViewSet, basename='warehouse')
router.register(r'stocks', StockViewSet, basename='stock')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
