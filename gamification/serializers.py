from rest_framework import serializers
from gamification.models import StudentProfile, EventType, StudentEvent

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = [
            "students",
            "total_point",
            "level"
        ]

class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = [
            "code",
            "name",
            "description",
            "point"
        ]

class StudentEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentEvent
        fields = [
            "student_profile",
            "event_type",
            "created_at",
            "note"
        ]