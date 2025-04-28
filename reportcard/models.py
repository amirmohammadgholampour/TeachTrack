from django.db import models
from config import settings 
from classroom.models import ClassRoom 
from score.models import Score 

class ReportCard(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={"user_type":"student"},
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

    DISCPLINARY_STATUS_CHOICES= [
        ("very_good", "Very good"),
        ("good", "Good"),
        ("normal", "Normal"),
        ("bad", "Bad"),
        ("very_bad", "Very bad")
    ]
    disciplinary_status = models.CharField(
        max_length=255,
        choices=DISCPLINARY_STATUS_CHOICES,
        verbose_name="Discplinary status"
    )

    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ReportCard for {self.user} - Grade: {self.grade}"
