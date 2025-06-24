# # from rest_framework.views import APIView
# # from rest_framework.response import Response
# # from rest_framework.parsers import MultiPartParser
# # from google.cloud import storage
# # from django.conf import settings
# # from .models import CallRecording
# # from .serializers import CallRecordingSerializer

# # class UploadCallRecording(APIView):
# #     parser_classes = [MultiPartParser]

# #     def post(self, request, format=None):
# #         file = request.data['file']
# #         storage_client = storage.Client()
# #         bucket = storage_client.bucket(settings.GCP_BUCKET_NAME)
# #         # 👇 Store under "recordings/" folder inside GCP bucket
# #         blob_path = f"recordings/{file.name}"
# #         blob = bucket.blob(blob_path)
# #         # blob = bucket.blob(file.name)
# #         blob.upload_from_file(file)
# #         # Save metadata to DB
# #         record = CallRecording.objects.create(filename=file.name)
# #         serializer = CallRecordingSerializer(record)
# #         return Response(serializer.data)




# from rest_framework.views import APIView
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.response import Response
# from rest_framework import status
# from .models import CallRecording
# from datetime import datetime

# class FileUploadView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, *args, **kwargs):
#         file = request.FILES.get('file')
#         note = request.data.get('note', '')
#         uploaded_at = request.data.get('uploaded_at')

#         try:
#             uploaded_at_dt = datetime.fromisoformat(uploaded_at.replace("Z", "+00:00"))
#         except Exception as e:
#             return Response({'error': f'Invalid date format: {str(e)}'}, status=400)

#         if not file:
#             return Response({'error': 'No file provided'}, status=400)

#         CallRecording.objects.create(
#             file=file,
#             note=note,
#             uploaded_at=uploaded_at_dt
#         )

#         return Response({'message': 'Upload successful'}, status=201)


from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser) # Crucial for handling file uploads and form data

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file') # Ensure 'file' matches formData.append('file', ...)
        note = request.POST.get('note', '') # Ensure 'note' matches formData.append('note', ...)
        uploaded_at = request.POST.get('uploaded_at') # And 'uploaded_at'

        if not file_obj:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Process the file and note here
        # Example: save to disk, process with a model, etc.
        # You might want to use Django's FileSystemStorage or a dedicated library

        try:
            # Simple example: save file
            with open(f"/tmp/{file_obj.name}", "wb+") as destination:
                for chunk in file_obj.chunks():
                    destination.write(chunk)
            print(f"File '{file_obj.name}' uploaded successfully with note: '{note}' at {uploaded_at}")
            return Response({'message': 'File uploaded successfully', 'file_name': file_obj.name, 'note': note}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error saving file: {e}")
            return Response({'error': f'Failed to save file: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)