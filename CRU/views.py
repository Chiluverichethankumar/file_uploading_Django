# CRU/views.py

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UploadedFileSerializer

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        # Keep this for debugging what DRF parses
        print("Request Data (parsed by DRF):", request.data)

        file_serializer = UploadedFileSerializer(data=request.data)
        print("hi ...............")

        # This is the crucial 'if' statement
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            # This print statement should ONLY be here, inside the else block
            print("Serializer Errors:", file_serializer.errors)
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)