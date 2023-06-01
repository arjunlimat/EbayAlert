from django.db import models

# Create your models here.
class Alert(models.Model):
    search_phrase = models.CharField(max_length=255)
    email = models.EmailField()
    frequency = models.TextField()
    def __str__(self):
        return self.search_phrase
