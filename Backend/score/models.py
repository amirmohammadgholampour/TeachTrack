from django.db import models 
from config import settings 
from lesson.models import Lesson 
from classroom.models import ClassRoom

class Score(models.Model):
    students = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"user_type":"student"},
        related_name="score_student"
    )

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="score_lesson"
    )

    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.CASCADE,
        related_name="score_classroom",
    )

    score_value = models.FloatField(
        max_length=20,
        verbose_name="Score"
    )

    created_at = models.DateTimeField(
        auto_now_add=True 
    )

    def __str__(self):
        return f"{self.students}({self.score_value})"