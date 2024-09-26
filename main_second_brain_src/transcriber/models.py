# transcriber/models.py
from django.db import models


class Transcription(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    video_url = models.URLField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    transcript = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transcription for {self.video_url} - {self.status}"
