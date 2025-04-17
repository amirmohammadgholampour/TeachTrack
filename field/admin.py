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