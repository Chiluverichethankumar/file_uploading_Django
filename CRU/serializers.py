from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UploadGroup, UploadFile

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class UploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFile
        fields = ['file']

class UploadGroupSerializer(serializers.ModelSerializer):
    files = UploadFileSerializer(many=True, read_only=True)

    class Meta:
        model = UploadGroup
        fields = ['id', 'note', 'files', 'created_at', 'user']
        read_only_fields = ['id', 'created_at', 'user']

class UploadGroupListSerializer(serializers.ModelSerializer):
    files = UploadFileSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UploadGroup
        fields = ['id', 'note', 'username', 'files', 'created_at']
