from django.db import models


class LibraryConfig(models.Model):
    library_id = models.CharField(max_length=100, unique=True)
    enable_media = models.BooleanField(default=False)
    theme_class = models.CharField(max_length=50, default="default-theme")
    naru_region_code = models.CharField(max_length=20)

    def __str__(self):
        return self.library_id
