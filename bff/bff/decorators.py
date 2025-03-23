from django.http import JsonResponse
from functools import wraps
import requests
from bff.settings import USERS_SERVICE_URL

def login_required_bff(view_func):
    """
    Decorador para requerir autenticación basada en token en las cookies.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_token = request.COOKIES.get("auth_token")

        if not auth_token:
            return JsonResponse({"error": "No autenticado"}, status=401)

        # Validar el token con el microservicio de autenticación
        try:
            headers = {"Content-Type": "application/json"}
            response = requests.post(f"{USERS_SERVICE_URL}/validate_token/", json={"token": auth_token}, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": f"Token inválido o expirado {str(e)}"}, status=401)

        return view_func(request, *args, **kwargs)

    return wrapper
