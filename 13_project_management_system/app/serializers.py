from rest_framework import serializers
from .models import *


class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'user', 'created_at', 'updated_at', 'is_active', 'metadata']
        read_only_fields = ['user', 'created_at', 'updated_at']


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'user', 'created_at', 'updated_at', 'is_active', 'metadata']
        read_only_fields = ['user', 'created_at', 'updated_at']


class TeamMemberSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TeamMember
        fields = ['id', 'title', 'description', 'user', 'created_at', 'updated_at', 'is_active', 'metadata']
        read_only_fields = ['user', 'created_at', 'updated_at']


class TimeLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TimeLog
        fields = ['id', 'title', 'description', 'user', 'created_at', 'updated_at', 'is_active', 'metadata']
        read_only_fields = ['user', 'created_at', 'updated_at']


