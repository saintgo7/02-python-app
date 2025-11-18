from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'events'

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'tickets', TicketViewSet, basename='ticket')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'attendees', AttendeeViewSet, basename='attendee')

urlpatterns = [
    path('', include(router.urls)),
]
