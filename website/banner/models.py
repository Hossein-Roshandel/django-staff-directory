from django.db import models

# Create your models here.
class Banner(models.Model):
    title = models.CharField(max_length=50, default='banner title')
    image = models.ImageField(upload_to='banners/')  
    index = models.PositiveIntegerField(unique=True)
    url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['index']

    def __str__(self):
        return f"Banner {self.index}"

class SocialLink(models.Model):
    SOCIAL_CHOICES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('linkedin-in', 'Linkedin'),
        ('x-twitter', 'X twitter'),
        ('tiktok', 'Tiktok'),
        ('shopee', 'Shopee'),
        ('lazada', 'Lazada'),
    ]

    index = models.PositiveIntegerField(unique=True, default=1)
    platform = models.CharField(max_length=50, choices=SOCIAL_CHOICES)
    url = models.URLField()
    is_shop = models.BooleanField(default=False)

class Journal(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class JournalImage(models.Model):
    journal = models.ForeignKey(Journal, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='journals/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"Image for {self.journal.title}"

    def __str__(self):
        return f"{self.platform}: {self.url}"