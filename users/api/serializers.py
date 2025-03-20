# api/serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "user_name", "name", "email", "password", "birth_date"]
        extra_kwargs = {
            'password': {'write_only': True}  # Para que la contraseña no se devuelva en las respuestas
        }