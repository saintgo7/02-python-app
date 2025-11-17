from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'projects'

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'teammembers', TeamMemberViewSet, basename='teammember')
router.register(r'timelogs', TimeLogViewSet, basename='timelog')

urlpatterns = [
    path('', include(router.urls)),
]
