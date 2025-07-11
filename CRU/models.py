from django.db import models
from django.contrib.auth.models import User

class UploadGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='upload_groups')
    note = models.TextField(blank=False)  # Mandatory
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.note}"

class UploadFile(models.Model):
    group = models.ForeignKey(UploadGroup, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='uploads/')
