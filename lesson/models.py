from django.db import models 
from config import settings 

class Lesson(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Name of lesson"
    )

    teachers = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, 
        limit_choices_to={"user_type":"teacher"},
        related_name="teacher_lesson" 
    )

    def __str__(self):
        return f"{self.name}({self.teachers})"