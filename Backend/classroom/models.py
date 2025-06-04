from django.db import models 
from field.models import Field 
from config import settings

class ClassRoom(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="ClassRoom Name" 
    )

    base = models.PositiveIntegerField(
        verbose_name="Base of student"
    )

    field = models.ForeignKey(
        Field,
        on_delete=models.CASCADE,
        verbose_name="Field"
    )

    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="classroom",
        limit_choices_to={"user_type": "student"},
        verbose_name="Student Users"
    )

    teachers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="teaching_classroom",
        limit_choices_to={"user_type": "teacher"},
        verbose_name="Teacher Users"
    )

    created_at = models.DateTimeField(
        auto_now_add=True 
    )

    updated_at = models.DateTimeField(
        auto_now_add=True 
    )

    def __str__(self):
        return f'{self.name}(base: {self.base})(field: {self.field.name})'