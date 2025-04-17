from django.contrib import admin
from lesson.models import Lesson
from django.contrib import messages

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'teachers',
        'created_at'
    ]
    search_fields = ['name']
    ordering = ['name', 'teachers']
    list_per_page = 10
    list_filter = ['teachers']