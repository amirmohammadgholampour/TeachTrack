from django.contrib import admin
from event.models import Event, Registration

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

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = [
        "user__username",
        "event__name",
        "register_at"
    ]
    search_fields = [
        "user__username",
        "event__name"
    ]
    ordering = ["user__username"]
    list_per_page = 10 