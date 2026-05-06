from django.contrib import admin
from .models import WasteCategory, EducationalContent

class WasteCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'created_at')
    search_fields = ('name',)

class EducationalContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'content_type', 'is_published', 'created_at')
    list_filter = ('content_type', 'is_published')
    search_fields = ('title', 'description')

admin.site.register(WasteCategory, WasteCategoryAdmin)
admin.site.register(EducationalContent, EducationalContentAdmin)
