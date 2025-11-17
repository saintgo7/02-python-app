from rest_framework import serializers
from .models import *


class TicketSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'title', 'description', 'user', 'created_at', 'updated_at', 'is_active', 'metadata']
        read_only_fields = ['user', 'created_at', 'updated_at']


class ResponseSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Response
        fields = ['id', 'title', 'description', 'user', 'created_at', 'updated_at', 'is_active', 'metadata']
        read_only_fields = ['user', 'created_at', 'updated_at']


class KnowledgeBaseSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = KnowledgeBase
        fields = ['id', 'title', 'description', 'user', 'created_at', 'updated_at', 'is_active', 'metadata']
        read_only_fields = ['user', 'created_at', 'updated_at']


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'user', 'created_at', 'updated_at', 'is_active', 'metadata']
        read_only_fields = ['user', 'created_at', 'updated_at']


