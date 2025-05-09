from django.contrib import admin 
from gamification.models import EventType, StudentEvent, StudentProfile

@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
	list_display = [
		"code",
		"name",
		"description",
		"point",
    ]
	list_filter = [
        "code",
        "name",
    ]
	list_per_page = 10
	list_editable = [
        "description",
        "point",
    ]
	search_fields = [
        "code",
        "name",
    ]
	
@admin.register(StudentEvent)
class StudentEventAdmin(admin.ModelAdmin):
    list_display = [
        "student_profile",
        "event_type",
        "created_at",
        "note",
    ]
    list_filter = [
        "student_profile",
        "event_type",
    ]
    list_per_page = 10
    list_editable = [
        "note",
    ]
    search_fields = [
        "student_profile__students__username",
        "event_type__name",
    ]

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = [
        "students",
        "total_point",
        "level",
    ]
    list_filter = [
        "students",
        "total_point",
        "level",
    ]
    list_per_page = 10
    list_editable = [
        "total_point",
        "level",
    ]
    search_fields = [
        "students__username",
    ]
    ordering = [
        "students",
    ]