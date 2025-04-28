from rest_framework import serializers 
from reportcard.models import ReportCard 
from score.models import Score 

class ReportCardSerializer(serializers.ModelSerializer):
    grade = serializers.SerializerMethodField()
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

    def get_grade(self, obj):
        scores = obj.scores.all()
        total_score = sum(score.score_value for score in scores)
        lesson_count = scores.values("lesson").distinct().count()

        if lesson_count == 0:
            return 0
        
        average = total_score / lesson_count
        return round(average, 2)