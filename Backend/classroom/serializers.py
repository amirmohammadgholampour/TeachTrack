from rest_framework import serializers 
from classroom.models import ClassRoom

class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom 
        fields = [
            "name",
            "base",
            "field",
            "students",
            "teachers"
        ]