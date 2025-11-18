from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'propertys'

router = DefaultRouter()
router.register(r'propertys', PropertyViewSet, basename='property')
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'viewings', ViewingViewSet, basename='viewing')
router.register(r'offers', OfferViewSet, basename='offer')

urlpatterns = [
    path('', include(router.urls)),
]
