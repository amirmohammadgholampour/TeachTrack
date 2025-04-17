from django.db import models
from config import settings 
from classroom.models import ClassRoom 
from score.models import Score 

class ReportCard(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='report_cards'
    )

    class_room = models.ForeignKey(
        ClassRoom,
        on_delete=models.CASCADE,
        related_name='report_cards'
    )

    scores = models.ManyToManyField(
        Score,
        related_name='report_cards'
    )

    disciplinary_status = models.CharField(max_length=255)
    grade = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ReportCard for {self.user} - Grade: {self.grade}"
