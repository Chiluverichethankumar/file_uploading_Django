from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    LoginView,
    UserDetailView,
    FileUploadView,
    UploadListView,
    LogoutView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('upload/', FileUploadView.as_view(), name='note/file-upload'),
    path('list_of_uploads/', UploadListView.as_view(), name='upload-list'),
    path('token/', obtain_auth_token, name='api_token_auth'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
