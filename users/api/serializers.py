# api/serializers.py
from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "user_name", "name", "email", "password", "birth_date"]
        extra_kwargs = {
            'password': {'write_only': True}  # Para que la contraseña no se devuelva en las respuestas
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # Hashear la contraseña
        return super().create(validated_data)