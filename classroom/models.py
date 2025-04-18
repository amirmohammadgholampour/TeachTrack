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

    students = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="classroom",
        on_delete=models.CASCADE,
        limit_choices_to={"user_type": "student"}
    )

    teachers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="teaching_classroom",
        limit_choices_to={"user_type": "teacher"}
    )

    def __str__(self):
        return f'{self.name}(base: {self.base})(field: {self.field__name})'