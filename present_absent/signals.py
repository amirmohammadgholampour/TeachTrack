from django.db.models.signals import post_save 
from django.dispatch import receiver 
from present_absent.models import PresentAbsent 
from gamification.models import (
    EventType,
    StudentEvent,
    StudentProfile
)

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

        except StudentProfile.DoesNotExist:
            raise ValueError("Student Profile not found.")