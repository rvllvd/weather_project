from django.db import models

class SearchHistory(models.Model):
    city = models.CharField(max_length=100, unique=True)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.city} ({self.count})"
