# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser
# from google.cloud import storage
# from django.conf import settings
# from .models import CallRecording
# from .serializers import CallRecordingSerializer

# class UploadCallRecording(APIView):
#     parser_classes = [MultiPartParser]

#     def post(self, request, format=None):
#         file = request.data['file']
#         storage_client = storage.Client()
#         bucket = storage_client.bucket(settings.GCP_BUCKET_NAME)
#         # 👇 Store under "recordings/" folder inside GCP bucket
#         blob_path = f"recordings/{file.name}"
#         blob = bucket.blob(blob_path)
#         # blob = bucket.blob(file.name)
#         blob.upload_from_file(file)
#         # Save metadata to DB
#         record = CallRecording.objects.create(filename=file.name)
#         serializer = CallRecordingSerializer(record)
#         return Response(serializer.data)




from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import CallRecording
from datetime import datetime

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        note = request.data.get('note', '')
        uploaded_at = request.data.get('uploaded_at')

        try:
            uploaded_at_dt = datetime.fromisoformat(uploaded_at.replace("Z", "+00:00"))
        except Exception as e:
            return Response({'error': f'Invalid date format: {str(e)}'}, status=400)

        if not file:
            return Response({'error': 'No file provided'}, status=400)

        CallRecording.objects.create(
            file=file,
            note=note,
            uploaded_at=uploaded_at_dt
        )

        return Response({'message': 'Upload successful'}, status=201)
