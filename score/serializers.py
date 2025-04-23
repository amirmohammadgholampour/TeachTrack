from rest_framework import serializers 
from score.models import Score 

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score 
        fields = [
            "students",
            "lesson",
            "classroom",
            "score_value",
            "created_at"
        ]