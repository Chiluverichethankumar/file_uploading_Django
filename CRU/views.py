from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import UploadGroup, UploadFile
from .serializers import (
    LoginSerializer, UserSerializer,
    UploadGroupSerializer, UploadGroupListSerializer
)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'username': user.username,
                    'email': user.email
                })
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        note = request.data.get('note', '').strip()
        files = request.FILES.getlist('file')  # optional

        if not note:
            return Response({'error': 'Note is required'}, status=status.HTTP_400_BAD_REQUEST)

        group = UploadGroup.objects.create(user=request.user, note=note)

        for f in files:
            UploadFile.objects.create(group=group, file=f)

        serializer = UploadGroupSerializer(group)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UploadListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UploadGroupListSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return UploadGroup.objects.all().order_by('-created_at')
        return UploadGroup.objects.filter(user=user).order_by('-created_at')


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Logout failed."}, status=status.HTTP_400_BAD_REQUEST)