from rest_framework import serializers 
from event.models import Event, Registration

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "name",
            "description",
            "image",
            "date",
            "time",
            "status",
            "capacity",
            "created_at"
        ]

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = [
            "user",
            "event",
            "register_at"
        ]