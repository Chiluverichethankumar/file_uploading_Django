# # # from rest_framework.views import APIView
# # # from rest_framework.response import Response
# # # from rest_framework.parsers import MultiPartParser
# # # from google.cloud import storage
# # # from django.conf import settings
# # # from .models import CallRecording
# # # from .serializers import CallRecordingSerializer

# # # class UploadCallRecording(APIView):
# # #     parser_classes = [MultiPartParser]

# # #     def post(self, request, format=None):
# # #         file = request.data['file']
# # #         storage_client = storage.Client()
# # #         bucket = storage_client.bucket(settings.GCP_BUCKET_NAME)
# # #         # 👇 Store under "recordings/" folder inside GCP bucket
# # #         blob_path = f"recordings/{file.name}"
# # #         blob = bucket.blob(blob_path)
# # #         # blob = bucket.blob(file.name)
# # #         blob.upload_from_file(file)
# # #         # Save metadata to DB
# # #         record = CallRecording.objects.create(filename=file.name)
# # #         serializer = CallRecordingSerializer(record)
# # #         return Response(serializer.data)




# # from rest_framework.views import APIView
# # from rest_framework.parsers import MultiPartParser, FormParser
# # from rest_framework.response import Response
# # from rest_framework import status
# # from .models import CallRecording
# # from datetime import datetime

# # class FileUploadView(APIView):
# #     parser_classes = (MultiPartParser, FormParser)

# #     def post(self, request, *args, **kwargs):
# #         file = request.FILES.get('file')
# #         note = request.data.get('note', '')
# #         uploaded_at = request.data.get('uploaded_at')

# #         try:
# #             uploaded_at_dt = datetime.fromisoformat(uploaded_at.replace("Z", "+00:00"))
# #         except Exception as e:
# #             return Response({'error': f'Invalid date format: {str(e)}'}, status=400)

# #         if not file:
# #             return Response({'error': 'No file provided'}, status=400)

# #         CallRecording.objects.create(
# #             file=file,
# #             note=note,
# #             uploaded_at=uploaded_at_dt
# #         )

# #         return Response({'message': 'Upload successful'}, status=201)


# from rest_framework.views import APIView
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.response import Response
# from rest_framework import status

# class FileUploadView(APIView):
#     parser_classes = (MultiPartParser, FormParser) # Crucial for handling file uploads and form data

#     def post(self, request, *args, **kwargs):
#         file_obj = request.FILES.get('file') # Ensure 'file' matches formData.append('file', ...)
#         note = request.POST.get('note', '') # Ensure 'note' matches formData.append('note', ...)
#         uploaded_at = request.POST.get('uploaded_at') # And 'uploaded_at'

#         if not file_obj:
#             return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

#         # Process the file and note here
#         # Example: save to disk, process with a model, etc.
#         # You might want to use Django's FileSystemStorage or a dedicated library

#         try:
#             # Simple example: save file
#             with open(f"/tmp/{file_obj.name}", "wb+") as destination:
#                 for chunk in file_obj.chunks():
#                     destination.write(chunk)
#             print(f"File '{file_obj.name}' uploaded successfully with note: '{note}' at {uploaded_at}")
#             return Response({'message': 'File uploaded successfully', 'file_name': file_obj.name, 'note': note}, status=status.HTTP_200_OK)
#         except Exception as e:
#             print(f"Error saving file: {e}")
#             return Response({'error': f'Failed to save file: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# from rest_framework.views import APIView
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.response import Response
# from rest_framework import status

# class FileUploadView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, *args, **kwargs):
#         file_obj = request.FILES.get('file')
#         note = request.POST.get('note', '')
#         uploaded_at = request.POST.get('uploaded_at')
#         data_time = request.POST.get('data_time')  # optional, if passed from frontend

#         if not file_obj:
#             return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             # Just save the file to /tmp (not saving to database)
#             with open(f"/tmp/{file_obj.name}", "wb+") as destination:
#                 for chunk in file_obj.chunks():
#                     destination.write(chunk)

#             print(f"File '{file_obj.name}' uploaded with note: '{note}' and data_time: {data_time}")
#             return Response({
#                 'message': 'File uploaded successfully',
#                 'file_name': file_obj.name,
#                 'note': note,
#                 'data_time': data_time
#             }, status=status.HTTP_200_OK)

#         except Exception as e:
#             print(f"Error saving file: {e}")
#             return Response({'error': f'Failed to save file: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# CRU/views.py
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import CallRecording
from .serializers import CallRecordingSerializer
from datetime import datetime

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_obj    = request.FILES.get('file')
        note        = request.data.get('note', '')
        uploaded_at = request.data.get('uploaded_at')
        data_time   = request.data.get('data_time')

        if not file_obj:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        # parse incoming timestamps or fall back to now()
        try:
            uploaded_dt = datetime.fromisoformat(uploaded_at)
        except Exception:
            uploaded_dt = timezone.now()

        try:
            data_dt = datetime.fromisoformat(data_time) if data_time else timezone.now()
        except Exception:
            data_dt = timezone.now()

        # Create & save the model — Django will store the file under MEDIA_ROOT/recordings/
        recording = CallRecording.objects.create(
            file        = file_obj,
            note        = note,
            uploaded_at = uploaded_dt,
            data_time   = data_dt
        )

        # If you prefer using your serializer:
        # serializer = CallRecordingSerializer(recording)
        # return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({
            'message':     'File uploaded and saved!',
            'id':          recording.id,
            'file_url':    recording.file.url,
            'note':        recording.note,
            'uploaded_at': recording.uploaded_at,
            'data_time':   recording.data_time
        }, status=status.HTTP_201_CREATED)
