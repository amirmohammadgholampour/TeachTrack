from django.db import models 
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_number = models.CharField(
        max_length=11, 
        unique=True, 
        verbose_name="Phone number"
    )

    national_code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="National code"
    )

    profile_image = models.ImageField(
        upload_to='profile_images'
    )

    USER_TYPE_CHOICES = [
        ("student", "Student"),
        ("teacher", "Teacher"),
        ("admin", "Manager")
    ]

    user_type = models.CharField(
        max_length=255,
        verbose_name="User type",
        choices=USER_TYPE_CHOICES
    )

    def __str__(self):
        return f'{self.username}({self.user_type})'