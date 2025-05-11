from django.db.models.signals import post_save 
from django.dispatch import receiver 
from score.models import Score 
from gamification.models import (
    StudentEvent,
    StudentProfile,
    EventType
)

@receiver(post_save, sender=Score)
def handle_score_event(instance, created, **kwargs):
    if created and instance.score_value == 20:
        try:
            profile = StudentProfile.objects.get(students=instance.students)

            event_type, _ = EventType.objects.get_or_create(
                code="score_20",
                defaults={
                    "name":"Excellent Score",
                    "description":"Student got a full score.",
                    "point":10
                }
            )

            StudentEvent.objects.create(
                student_profile=profile,
                event_type=event_type,
                note="Got full score in exam"
            )

            profile.recalculate_total_points()

        except StudentProfile.DoesNotExist:
            raise ValueError("Student Profile not found.")