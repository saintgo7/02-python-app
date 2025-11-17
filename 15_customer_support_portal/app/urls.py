from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'tickets'

router = DefaultRouter()
router.register(r'tickets', TicketViewSet, basename='ticket')
router.register(r'responses', ResponseViewSet, basename='response')
router.register(r'knowledgebases', KnowledgeBaseViewSet, basename='knowledgebase')
router.register(r'categorys', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]
