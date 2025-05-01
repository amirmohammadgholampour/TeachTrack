from django.db import models

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