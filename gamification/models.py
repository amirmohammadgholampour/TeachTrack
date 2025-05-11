from django.db import models 
from user.models import User
from django.db.models import Sum

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

    def recalculate_total_points(self):
        total = self.student_event.aggregate(total=Sum('event_type__point'))['total'] or 0
        self.total_point = total
        self.save()

    def __str__(self):
        return f'{self.students.username}(total points: {self.total_point}) (Level: {self.level})'
    
class EventType(models.Model):
    code = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Code of work"
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Name"
    )
    description = models.TextField(verbose_name="Description")
    point = models.IntegerField(verbose_name="Point")

    def __str__(self):
        return f'{self.name} (+{self.point}) (code: {self.code})'
    
class StudentEvent(models.Model):
    student_profile = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="student_event",
    )
    event_type = models.ForeignKey(
        EventType,
        on_delete=models.CASCADE,
        verbose_name="Event Type"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.student_profile.students.username}({self.event_type.name}) at {self.created_at}'