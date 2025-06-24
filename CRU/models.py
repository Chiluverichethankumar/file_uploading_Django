from django.db import models

class CallRecording(models.Model):
    file = models.FileField(upload_to='recordings/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)
    data_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.file.name
