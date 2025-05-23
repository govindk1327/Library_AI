from django.db import models
from django.contrib.auth.models import User

class PromptLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    prompt_text = models.TextField()
    response_text = models.TextField()
    user_query = models.CharField(max_length=255)
    book_isbns = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} | {self.user_query[:30]}"
