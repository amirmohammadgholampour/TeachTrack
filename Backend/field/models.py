from django.db import models 

class Field(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Name"
    )

    created_at = models.DateTimeField(
        auto_now_add=True 
    )

    def __str__(self):
        return self.name