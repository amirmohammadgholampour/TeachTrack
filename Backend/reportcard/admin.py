from django.contrib import admin
from reportcard.models import ReportCard
from django.contrib import messages

@admin.register(ReportCard)
class ReportCardAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'class_room',
        'disciplinary_status',
        'grade',
        'created_at'
    ]
    search_fields = ['user__username']
    ordering = ['grade', 'class_room']
    list_per_page = 10
    list_filter = ['class_room']