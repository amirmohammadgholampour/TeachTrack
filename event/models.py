from django.db import models
from user.models import User 

class Event(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Name of event"
    )

    description = models.TextField(
        verbose_name="Description"
    )

    image = models.ImageField(
        upload_to="event_images/",
        null=True,
        blank=True
    )

    date = models.DateField()
    time = models.TimeField()
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at"
    )

    def __str__(self):
        return self.name
    
class Registration(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE 
    )
    register_at = models.DateTimeField(
        auto_now_add=True
    )