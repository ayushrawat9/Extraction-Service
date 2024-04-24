from django.db import models
from django.contrib.auth.models import User

class ExtractedText(models.Model):
    file_name = models.CharField(max_length=255)
    extracted_text = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

