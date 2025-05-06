from django.contrib import admin 
from present_absent.models import PresentAbsent

@admin.register(PresentAbsent)
class PresentAbsentAdmin(admin.ModelAdmin):
    list_display = [
        "user__username", 
        "classroom",
        "status"
    ]
    list_editable = ["status"]
    list_filter = [
        "status",
        "classroom__field__name",
        "classroom__base",
    ]
    list_per_page = 10
    ordering = ["status"]
    search_fields = [
        "user__username",
        "classroom__nmae"
    ]