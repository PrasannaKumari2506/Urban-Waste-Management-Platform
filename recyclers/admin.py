from django.contrib import admin
from .models import RecyclerProfile, Review

class RecyclerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_approved', 'is_available', 'created_at')
    list_filter = ('is_approved', 'is_available')
    search_fields = ('user__email', 'user__name')
    actions = ['approve_recyclers']
    
    def approve_recyclers(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} recycler(s) approved successfully.')
    approve_recyclers.short_description = 'Approve selected recyclers'

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('recycler', 'household', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('recycler__name', 'household__name')

admin.site.register(RecyclerProfile, RecyclerProfileAdmin)
admin.site.register(Review, ReviewAdmin)
