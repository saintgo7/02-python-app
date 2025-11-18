from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'posts'

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'categorys', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]
