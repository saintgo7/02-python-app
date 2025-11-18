from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'courses'

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'quizs', QuizViewSet, basename='quiz')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')

urlpatterns = [
    path('', include(router.urls)),
]
