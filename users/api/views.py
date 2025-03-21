from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
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
    user_name = request.data.get("user_name")
    password = request.data.get("password")

    try:
        user = User.objects.get(user_name=user_name)
    except User.DoesNotExist:
        return Response({"message": "Usuario o contraseña incorrectos"}, status=400)

    if check_password(password, user.password):
        return Response({"message": "Login exitoso"}, status=200)
    else:
        return Response({"message": "Usuario o contraseña incorrectos"}, status=400)
    
@api_view(['POST'])
def logout_view(request):
    #Cerrar sesion :3                                                    
    logout(request)
    return Response({"message": "Sesión cerrada exitosamente"}, status=status.HTTP_200_OK)

