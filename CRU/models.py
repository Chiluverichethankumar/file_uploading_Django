# from django.db import models


# class CallRecording(models.Model):
#     filename = models.CharField(max_length=255)
#     uploaded_at = models.DateTimeField(auto_now_add=True)


from django.db import models

class CallRecording(models.Model):
    file = models.FileField(upload_to='recordings/')
    note = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField()

    def __str__(self):
        return str(self.file.name)
