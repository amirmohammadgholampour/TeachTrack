from django.contrib import admin
from classroom.models import ClassRoom

@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'base',
        'field'
    ]
    search_fields = ['name']
    ordering = ['base', 'field']
    list_per_page = 10
    list_filter = ['field']