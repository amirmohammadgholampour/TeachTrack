from django.db.models.signals import post_save
from django.dispatch import receiver 
from user.models import User 
from gamification.models import StudentProfile

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.user_type == "student":
        StudentProfile.objects.get_or_create(students=instance)