from django.shortcuts import redirect
from functools import wraps
import requests
from bff.settings import USERS_SERVICE_URL

def login_required_bff(view_func):
    """
    Decorador para requerir autenticación basada en token en las cookies.
    Si el token es inválido, elimina las cookies de sesión.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_token = request.COOKIES.get("auth_token")

        if not auth_token:
            return redirect("login")  # No hay token, redirige al login

        # Validar el token con el microservicio de autenticación
        try:
            headers = {"Content-Type": "application/json"}
            response = requests.post(f"{USERS_SERVICE_URL}/validate_token/", json={"token": auth_token}, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            # Si el token es inválido, eliminamos las cookies y redirigimos a login
            response = redirect("login")
            response.delete_cookie("auth_token")
            response.delete_cookie("user_id")
            response.delete_cookie("user_name")
            response.delete_cookie("name")
            response.delete_cookie("email")
            response.delete_cookie("birth_date")
            return response

        return view_func(request, *args, **kwargs)

    return wrapper

def redirect_if_authenticated_bff(view_func):
    """
    Decorador para redirigir a /home/ si el usuario ya está autenticado.
    Si el token es inválido, lo elimina de las cookies.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_token = request.COOKIES.get("auth_token")

        if auth_token:
            # Si hay un token, simplemente lo redirigimos a /home/
            return redirect("home")  

        return view_func(request, *args, **kwargs)

    return wrapper