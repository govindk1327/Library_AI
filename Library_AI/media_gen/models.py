from django.db import models
from books.models import Book

class MediaAsset(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="media_assets")
    media_type = models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')])
    media_url = models.URLField(max_length=500)
    summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
