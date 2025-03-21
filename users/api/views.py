#api/views.py
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny]) 
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
@permission_classes([AllowAny]) 
def login_view(request):
    user_name = request.data.get("user_name")
    password = request.data.get("password")

    try:
        user = User.objects.get(user_name=user_name)
    except User.DoesNotExist:
        return Response({"message": "Usuario o contraseña incorrectos"}, status=400)

    if check_password(password, user.password):
        login(request, user)  # Asegura que se cree la sesión
        return Response({"message": "Login exitoso"}, status=200)
    else:
        return Response({"message": "Usuario o contraseña incorrectos"}, status=400)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    print("Usuario autenticado:", request.user)  # Depuración
    user = request.user
    serializer = UserSerializer(user)
    return Response({
        "message": "Estás autenticado",
        "user": serializer.data
    })
    
@api_view(['POST'])
def logout_view(request):
    #Cerrar sesion :3                                                    
    logout(request)
    return Response({"message": "Sesión cerrada exitosamente"}, status=status.HTTP_200_OK)

