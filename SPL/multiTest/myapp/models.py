# myapp/models.py
from django.db import models
from datetime import datetime

class UploadedFile(models.Model):
    filename = models.CharField(max_length=100)
    filepath = models.CharField(upload_to='uploads/')
    upload_time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.filename
