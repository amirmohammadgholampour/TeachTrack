from django.db.models.signals import post_save 
from django.dispatch import receiver 
from present_absent.models import PresentAbsent, AttendanceReview
from gamification.models import (
    EventType,
    StudentEvent,
    StudentProfile
)
from datetime import date

@receiver(post_save, sender=PresentAbsent)
def handle_attending_event(instance, created, **kwargs):
    if created and instance.status == "present":
        try:
            profile = StudentProfile.objects.get(students=instance.user)

            event_type, _ = EventType.objects.get_or_create(
                code="attend_on_time",
                defaults={
                    "name":"To be present",
                    "description":"Student attended in school.",
                    "point":5
                }
            )

            StudentEvent.objects.create(
                student_profile=profile,
                event_type=event_type,
                note="Attenting in school"
            )

            profile.recalculate_total_points()
            profile.calculate_level()

        except StudentProfile.DoesNotExist:
            raise ValueError("Student Profile not found.")


@receiver(post_save, sender=AttendanceReview)
def handle_review_decision(sender, instance, created, **kwargs):
    if instance.review_status == "pending":
        return 

    request = instance.attending_request
    student = request.student
    classroom = request.classroom
    status = request.status_requested
    attendance_date = request.date

    if PresentAbsent.objects.filter(user=student, classroom=classroom, date=attendance_date).exists():
        return 

    if instance.review_status == "approved":
        final_status = status
    elif instance.review_status == "rejected":
        if status == "absent":
            final_status = "present"
        elif status == "present":
            final_status = "absent"
        else:
            final_status = "present" 

    PresentAbsent.objects.create(
        user=student,
        classroom=classroom,
        status=final_status,
        date=attendance_date
    )