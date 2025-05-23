from django.db import models

class Book(models.Model):
    id = models.AutoField(primary_key=True)  
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    publisher = models.CharField(max_length=255, blank=True)
    pub_date = models.DateField(null=True, blank=True)
    isbn13 = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.title} by {self.author}"
    
class BookSource(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='sources')
    source = models.CharField(max_length=100) 
    bestseller_rank = models.PositiveIntegerField(null=True, blank=True)
    detail_url = models.URLField(max_length=500, blank=True)
    inserted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source} - {self.book.title}"

class PromptLog(models.Model):
    prompt_text = models.TextField()
    response_text = models.TextField()
    user_query = models.CharField(max_length=255)
    book_isbns = models.TextField(blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prompt at {self.created_at}"


class LibraryConfig(models.Model):
    library_id = models.CharField(max_length=100, unique=True)
    enable_media = models.BooleanField(default=False)
    theme_class = models.CharField(max_length=50)
    naru_region_code = models.CharField(max_length=20)

    def __str__(self):
        return self.library_id
