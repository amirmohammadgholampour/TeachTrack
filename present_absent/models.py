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
        ("present", "Present"),
        ("excused", "Excused")
    ]
    status = models.CharField(
        max_length=255,
        choices=STATUS_CHOICES,
        verbose_name="Status"
    )
    date = models.DateField()

    def __str__(self):
        return f"student: {self.user.username}({self.status})"
    
class AttendanceApproval(models.Model):
    teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={"user_type": "teacher"},
        verbose_name="Teacher User",
        related_name="attendance_approval_teacher"
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"user_type": "student"},
        verbose_name="Student User"
    )

    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.CASCADE,
        verbose_name="Class room"
    )

    STATUS_CHOICES = [
        ("absent", "Absent"),
        ("present", "Present"),
        ("excused", "Excused")
    ]
    status_requested = models.CharField(
        max_length=255,
        choices=STATUS_CHOICES,
        verbose_name="Requested Status"
    )

    date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.teacher.username} → {self.student.username} ({self.status_requested})"
    
class AttendanceReview(models.Model):
    attending_approval = models.OneToOneField(
        AttendanceApproval,
        on_delete=models.CASCADE,
        related_name="review",
        verbose_name="Attending Request"
    )

    REVIEW_CHOICES = [
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("pending", "Pending")
    ]
    review_status = models.CharField(
        max_length=20,
        choices=REVIEW_CHOICES,
        default="pending",
        verbose_name="Review Status"
    )

    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"user_type": "admin"},
        verbose_name="Reviewed by (Admin)"
    )

    reviewed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.attending_approval} → {self.review_status}"