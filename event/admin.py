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

    # Custom action to deactivate selected events
    @admin.action(description='Deactivate selected events')
    def deactivate_events(self, request, queryset):
        updated_count = queryset.update(is_active=False)
        self.message_user(
            request,
            f'{updated_count} event(s) were successfully deactivated.',
            messages.SUCCESS
        )
    actions = [deactivate_events]