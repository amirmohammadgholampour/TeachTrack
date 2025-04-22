from rest_framework import serializers 
from field.models import Field

class FieldSerializer(serializers.ModelSerializer):
    model = Field
    fields = [
        "name",
        "created_at"
    ]