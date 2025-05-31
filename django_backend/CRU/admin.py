from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import UploadedFile # Import your UploadedFile model

# Register your model with the admin site
admin.site.register(UploadedFile)
