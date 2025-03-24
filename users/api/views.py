#api/views.py
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
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password 
from django.shortcuts import get_object_or_404

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
        # Obtener o crear el token del usuario
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "message": "Login exitoso",
            "token": token.key,
            "user": {
                "user_id": user.user_id,
                "user_name": user.user_name,
                "name": user.name,
                "email": user.email,
                "birth_date": user.birth_date
            }
        }, status=200)
    else:
        return Response({"message": "Usuario o contraseña incorrectos"}, status=400)
    
@api_view(['POST'])
@permission_classes([AllowAny])  
def validate_token(request):
    token_key = request.data.get("token")  # Recibir el token desde el cuerpo de la solicitud

    if not token_key:
        return Response({"message": "Token no proporcionado"}, status=400)

    try:
        token = Token.objects.get(key=token_key)  # Buscar el token en la base de datos
        user = token.user  # Obtener el usuario relacionado con el token

        return Response({
            "message": "Token válido",
            "user_id": user.user_id,
            "user_name": user.user_name,
            "name": user.name,
            "email": user.email,
            "birth_date": user.birth_date
        }, status=200)

    except Token.DoesNotExist:
        return Response({"message": "Token inválido"}, status=401)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_id(request, user_id):
    """
    Permite a un usuario autenticado ver la información pública de otro usuario.
    """
    user = get_object_or_404(User, user_id=user_id)  # Django ya lo trata como UUID
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response({
        "message": "Estás autenticado",
        "user": serializer.data
    })

@api_view(['PATCH'])  # PATCH permite actualizar solo algunos campos
@permission_classes([IsAuthenticated])  # Requiere autenticación
def update_user(request):
    """
    Permite a un usuario autenticado actualizar su perfil, incluyendo la contraseña.
    """
    user = request.user  # Usuario autenticado
    data = request.data  

    # Campos permitidos
    allowed_fields = ["user_name", "name", "email", "birth_date"]
    
    # Actualizar los campos permitidos
    for field in allowed_fields:
        if field in data:
            setattr(user, field, data[field])

    # Si se envía una nueva contraseña, se cifra antes de guardarla
    if "password" in data:
        user.set_password(data["password"])  

    user.save()  # Guardamos los cambios
    serializer = UserSerializer(user)  # Serializamos el usuario actualizado

    return Response({
        "message": "Usuario actualizado correctamente",
        "user": serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  # Solo usuarios autenticados pueden borrar su cuenta
def delete_account(request):
    """
    Permite a un usuario autenticado eliminar su cuenta solo si proporciona su contraseña actual.
    """
    user = request.user  # Obtiene el usuario autenticado
    data = request.data

    # Verificar que el usuario proporcionó la contraseña
    password = data.get("password")
    if not password:
        return Response({"message": "Debes proporcionar tu contraseña para eliminar la cuenta."}, status=status.HTTP_400_BAD_REQUEST)

    # Verificar si la contraseña es correcta
    if not check_password(password, user.password):
        return Response({"message": "Contraseña incorrecta."}, status=status.HTTP_401_UNAUTHORIZED)

    # Si la contraseña es correcta, eliminamos la cuenta
    user.delete()
    return Response({"message": "Cuenta eliminada exitosamente."}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def logout_view(request):
    # Verifica si el usuario tiene un token antes de intentar eliminarlo
    if hasattr(request.user, 'auth_token'):
        request.user.auth_token.delete()  # Elimina el token del usuario
        return Response({"message": "Sesión cerrada exitosamente"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Token no encontrado"}, status=status.HTTP_400_BAD_REQUEST)
    


