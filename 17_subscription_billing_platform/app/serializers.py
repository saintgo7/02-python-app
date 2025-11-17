from rest_framework import serializers
from .models import *


class PlanSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Plan
        fields = ['id', 'title', 'description', 'user', 'created_at', 'updated_at', 'is_active', 'metadata']
        read_only_fields = ['user', 'created_at', 'updated_at']


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'title', 'description', 'user', 'created_at', 'updated_at', 'is_active', 'metadata']
        read_only_fields = ['user', 'created_at', 'updated_at']


class InvoiceSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Invoice
        fields = ['id', 'title', 'description', 'user', 'created_at', 'updated_at', 'is_active', 'metadata']
        read_only_fields = ['user', 'created_at', 'updated_at']


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'title', 'description', 'user', 'created_at', 'updated_at', 'is_active', 'metadata']
        read_only_fields = ['user', 'created_at', 'updated_at']


