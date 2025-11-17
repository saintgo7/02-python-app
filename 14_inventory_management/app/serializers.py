from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'user', 'created_at', 'updated_at', 'is_active', 'metadata']
        read_only_fields = ['user', 'created_at', 'updated_at']


class WarehouseSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Warehouse
        fields = ['id', 'title', 'description', 'user', 'created_at', 'updated_at', 'is_active', 'metadata']
        read_only_fields = ['user', 'created_at', 'updated_at']


class StockSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Stock
        fields = ['id', 'title', 'description', 'user', 'created_at', 'updated_at', 'is_active', 'metadata']
        read_only_fields = ['user', 'created_at', 'updated_at']


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'title', 'description', 'user', 'created_at', 'updated_at', 'is_active', 'metadata']
        read_only_fields = ['user', 'created_at', 'updated_at']


