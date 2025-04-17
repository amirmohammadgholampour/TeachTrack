from django.contrib import admin
from django.contrib import messages
from event.models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'description',
        'image',
        'created_at'
    ]
    search_fields = ['name', 'description']
    ordering = ['name']
    list_per_page = 10
    list_filter = ['created_at']