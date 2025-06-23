# from django.urls import path
# from .views import UploadCallRecording

# urlpatterns = [
#     path('upload/', UploadCallRecording.as_view(), name='upload-recording'),
# ]

from django.urls import path
from .views import FileUploadView  # ✅ CORRECT NAME

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='upload-call-recording'),
]
