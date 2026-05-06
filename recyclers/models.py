from django.db import models
from accounts.models import User
from households.models import WastePickupRequest

class RecyclerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recycler_profile')
    is_approved = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    bio = models.TextField(blank=True, null=True)
    service_areas = models.TextField(help_text='Comma-separated areas', blank=True, null=True)
    vehicle_type = models.CharField(max_length=100, blank=True, null=True)
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.name} - {'Approved' if self.is_approved else 'Pending'}"
    
    def total_completed_pickups(self):
        return self.user.assigned_pickups.filter(status='completed').count()
    
    def total_pending_pickups(self):
        return self.user.assigned_pickups.filter(status='accepted').count()

class Review(models.Model):
    recycler = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    household = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    pickup_request = models.OneToOneField(WastePickupRequest, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.recycler.name} - {self.rating} stars"

class RecyclerNotification(models.Model):
    NOTIFICATION_TYPES = [
        ('new_request', 'New Pickup Request'),
        ('cancelled', 'Pickup Cancelled'),
        ('review_received', 'Review Received'),
        ('approval', 'Account Approved'),
    ]
    
    recycler = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    pickup_request = models.ForeignKey(WastePickupRequest, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.recycler.name} - {self.title}"
