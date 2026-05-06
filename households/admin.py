from django.contrib import admin
from .models import WastePickupRequest

class WastePickupRequestAdmin(admin.ModelAdmin):
    list_display = ('household', 'waste_category', 'pickup_date', 'status', 'recycler', 'created_at')
    list_filter = ('status', 'waste_category', 'pickup_date')
    search_fields = ('household__email', 'household__name', 'recycler__email')
    
admin.site.register(WastePickupRequest, WastePickupRequestAdmin)
