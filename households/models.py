from django.db import models
from accounts.models import User
from core.models import WasteCategory

class WastePickupRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    household = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pickup_requests')
    recycler = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_pickups')
    waste_category = models.ForeignKey(WasteCategory, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    pickup_date = models.DateField()
    pickup_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.household.name} - {self.waste_category.name} - {self.status}"
