from rest_framework import serializers 
from reportcard.models import ReportCard 

class ReportCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportCard 
        fields = [
            "user",
            "class_room",
            "scores",
            "disciplinary_status",
            "grade",
            "created_at"
        ]