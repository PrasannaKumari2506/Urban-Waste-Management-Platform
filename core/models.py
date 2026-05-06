from django.db import models
from accounts.models import User

class WasteCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=7, default='#2C5530')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Waste Categories'
    
    def __str__(self):
        return self.name

class EducationalContent(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('article', 'Article'),
        ('video', 'Video'),
        ('guide', 'Guide'),
    ]
    
    title = models.CharField(max_length=255)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    description = models.TextField()
    content = models.TextField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    thumbnail = models.URLField(blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
