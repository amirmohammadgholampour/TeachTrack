from django.contrib import admin
from field.models import Field 
from django.contrib import messages

@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'created_at'
    ]
    search_fields = ['name']
    ordering = ['name']
    list_per_page = 10
    list_filter = ['created_at']

    # Custom action to deactivate selected fields
    @admin.action(description='Deactivate selected fields')
    def deactivate_fields(self, request, queryset):
        updated_count = queryset.update(is_active=False)
        self.message_user(
            request,
            f'{updated_count} field(s) were successfully deactivated.',
            messages.SUCCESS
        )
    actions = [deactivate_fields]