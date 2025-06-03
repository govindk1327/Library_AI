from django.db import models
from django.contrib.auth.models import User

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="preferences")
    preferred_genres = models.JSONField(default=list, blank=True)  # list of strings
    # preferred_language = models.CharField(max_length=20, default="ko")
    prefers_ai_images = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preferences for {self.user.username}"
