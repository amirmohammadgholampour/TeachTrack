from django.contrib import admin
from django.contrib import messages
from user.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'username', 
        'email',
        'user_type',
        'first_name',
        'last_name',
        'phone_number',
        'national_code',
        'profile_image'
    ]
    list_filter = ['user_type']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'national_code']
    ordering = ['username']
    list_per_page = 10

    # Custom action to deactivate selected users
    @admin.action(description='Deactivate selected users')
    def deactivate_users(self, request, queryset):
        updated_count = queryset.update(is_active=False)
        self.message_user(
            request,
            f'{updated_count} user(s) were successfully deactivated.',
            messages.SUCCESS
        )

    actions = [deactivate_users]