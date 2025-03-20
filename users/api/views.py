from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from .models import User
from .serializers import UserSerializer

# Create your views here.

@api_view(['POST'])
def register(request):
    """
    Registra un nuevo usuario.
    """
    data = request.data
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": "Usuario registrado exitosamente"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
    """
    Inicia sesión con un usuario existente.
    """
    user_name = request.data.get('user_name')
    password = request.data.get('password')

    user = authenticate(request, user_name=user_name, password=password)
    if user is not None:
        login(request, user)
        return Response({"message": "Inicio de sesión exitoso"}, status=status.HTTP_200_OK)
    return Response({"message": "Usuario o contraseña incorrectos"}, status=status.HTTP_400_BAD_REQUEST)


