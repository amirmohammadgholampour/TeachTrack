from rest_framework import serializers 
from present_absent.models import PresentAbsent 

class PresentAbsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PresentAbsent
        fields = [
            "user",
            "classroom",
            "status"
        ]