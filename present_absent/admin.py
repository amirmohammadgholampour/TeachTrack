from django.contrib import admin 
from present_absent.models import (
    PresentAbsent,
    AttendanceApproval,
    AttendanceReview
)

@admin.register(PresentAbsent)
class PresentAbsentAdmin(admin.ModelAdmin):
    list_display = [
        "user__username", 
        "classroom",
        "status",
        "date"
    ]
    list_editable = ["status"]
    list_filter = [
        "status",
        "classroom__field__name",
        "classroom__base",
        "date"
    ]
    list_per_page = 10
    ordering = ["status"]
    search_fields = [
        "user__username",
        "classroom__nmae"
    ]

@admin.register(AttendanceApproval)
class AttendanceApprovalAdmin(admin.ModelAdmin):
    list_display = [
        "teacher__username",
        "student__username",
        "classroom",
        "status_requested",
        "date"
    ]
    list_editable = ["status_requested"]
    list_filter = [
        "status_requested",
        "classroom",
        "classroom",
        "date"
    ]
    list_per_page = 10
    ordering = ["status_requested"]
    search_fields = [
        "teacher__username",
        "student__username",
        "classroom__nmae"
    ]

@admin.register(AttendanceReview)
class AttendanceReviewAdmin(admin.ModelAdmin):
    list_display = [
        "attending_approval",
        "review_status",
        "reviewed_by",
        "reviewed_at"
    ]
    list_editable = ["review_status"]
    list_filter = [
        "review_status",
        "reviewed_at"
    ]
    list_per_page = 10
    ordering = ["review_status"]
    search_fields = [
        "reviewed_by__username",
    ]