from rest_framework import serializers 
from user.models import User 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "national_code",
            "profile_image",
            "user_type"
        ]