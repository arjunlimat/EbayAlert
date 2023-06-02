from django.db import models
from django.utils import timezone

# Create your models here.
class Alert(models.Model):
    search_phrase = models.CharField(max_length=255)
    email = models.EmailField()
    frequency = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.search_phrase

class Price(models.Model):
    item = models.CharField(max_length=255)
    email_id = models.EmailField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    frequency = models.CharField(max_length=20)

    def __str__(self):
        return self.item