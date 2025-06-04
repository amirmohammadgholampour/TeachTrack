from django.contrib import admin
from score.models import Score 
from django.contrib import messages 

@admin.register(Score) 
class ScoreAdmin(admin.ModelAdmin):
    list_display = [
        'students',
        'lesson',
        'classroom',
        'score_value',
        'created_at'
    ]
    search_fields = ['students__username']
    ordering = ['score_value', 'lesson', 'classroom']
    list_per_page = 10
    list_filter = ['lesson', 'classroom']