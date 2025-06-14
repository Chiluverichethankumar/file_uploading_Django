# app_name/serializers.py
from rest_framework import serializers
from .models import UploadedFile

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = '__all__' # Or specify individual fields like ['id', 'file', 'description', 'uploaded_at']

