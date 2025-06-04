from rest_framework import serializers 
from present_absent.models import (
    PresentAbsent,
    AttendanceApproval,
    AttendanceReview
)

class PresentAbsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PresentAbsent
        fields = [
            "user",
            "classroom",
            "status",
            "date"
        ]

class AttendanceApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceApproval
        fields = [
            "teacher",
            "student",
            "classroom",
            "status_requested",
            "date",
            "created_at"
        ]

class AttendanceReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceReview
        fields = [
            "attending_approval",
            "review_status",
            "reviewed_by",
            "reviewed_at"
        ]