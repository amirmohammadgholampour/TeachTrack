from django.db.models.signals import post_save 
from user.models import User 
from django.dispatch import receiver

@receiver(post_save, sender=User)
def save_admin_is_staff(instance, created, **kwargs):
    if created and instance.user_type == "admin":
        instance.is_staff = True 
        instance.save()