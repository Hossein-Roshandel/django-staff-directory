from django.db import models
from django.contrib.postgres.fields import ArrayField  # For storing tags and images
from django.utils.timezone import now

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    brand = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)
    images = ArrayField(models.URLField(max_length=500), blank=True, default=list)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title