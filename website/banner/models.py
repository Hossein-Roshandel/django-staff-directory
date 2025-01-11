from django.db import models

# Create your models here.
class Banner(models.Model):
    image = models.ImageField(upload_to='banners/')  # Ensure MEDIA_URL and MEDIA_ROOT are set in settings.py
    index = models.PositiveIntegerField(unique=True)
    url_href = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['index']

    def __str__(self):
        return f"Banner {self.index}"

class SocialLink(models.Model):
    SOCIAL_CHOICES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('shopee', 'Shopee'),
        ('lazada', 'Lazada'),
    ]

    platform = models.CharField(max_length=50, choices=SOCIAL_CHOICES)
    url = models.URLField()

    def __str__(self):
        return f"{self.platform}: {self.url}"