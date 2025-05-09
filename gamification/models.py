from django.db import models 
from user.models import User

class StudentProfile(models.Model):
    students = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"user_type":"student"},
        verbose_name="Student"
    )

    total_point = models.IntegerField(
        default=0,
        verbose_name="Total points"
    )

    level = models.IntegerField(
        default=1,
        verbose_name="Level"
    )

    def __str__(self):
        return f'{self.students.username}(total points: {self.total_point}) (Level: {self.level})'