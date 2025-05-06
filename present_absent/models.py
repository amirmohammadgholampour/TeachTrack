from django.db import models 
from user.models import User 
from classroom.models import ClassRoom 

class PresentAbsent(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"user_type":"student"},
        verbose_name="Student Users"   
    )

    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.CASCADE,
        verbose_name="Class room"
    )

    STATUS_CHOICES = [
        ("absent", "Absent"),
        ("present", "Present")
    ]
    status = models.CharField(
        max_length=255,
        choices=STATUS_CHOICES,
        verbose_name="Status"
    )
    date = models.DateField()

    def __str__(self):
        return f"student: {self.user.username}({self.status})"