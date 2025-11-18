from rest_framework import serializers
from .models import *


class EventSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'user', 'created_at', 'updated_at', 'is_active', 'metadata']
        read_only_fields = ['user', 'created_at', 'updated_at']


class TicketSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'title', 'description', 'user', 'created_at', 'updated_at', 'is_active', 'metadata']
        read_only_fields = ['user', 'created_at', 'updated_at']


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'title', 'description', 'user', 'created_at', 'updated_at', 'is_active', 'metadata']
        read_only_fields = ['user', 'created_at', 'updated_at']


class AttendeeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Attendee
        fields = ['id', 'title', 'description', 'user', 'created_at', 'updated_at', 'is_active', 'metadata']
        read_only_fields = ['user', 'created_at', 'updated_at']


