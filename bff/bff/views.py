from django.shortcuts import render, redirect
from .decorators import login_required_bff
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import requests
import json
from bff.settings import USERS_SERVICE_URL, SECURE_COOKIE

def welcome(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, "index.html")

def login(request):
    if request.method == "POST":
        data = {
            "user_name": request.POST.get("user_name", "").strip(),
            "password": request.POST.get("password", "").strip(),
        }

        if not data.get("user_name") or not data.get("password"):
            return JsonResponse({"error": "Usuario y contraseña son obligatorios"}, status=400)
        
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(f"{USERS_SERVICE_URL}/login/", json=data, headers=headers)
            response.raise_for_status()
            response_data = response.json()

            if response.status_code == 200:
                # Crear la respuesta JSON
                res = JsonResponse({"message": "Inicio de sesión exitoso"}, status=200)
                
                # Guardar datos en cookies seguras
                res.set_cookie("auth_token", response_data["token"], httponly=True, secure=SECURE_COOKIE, max_age=86400)
                res.set_cookie("user_id", response_data["user"]["user_id"], httponly=True, secure=SECURE_COOKIE, max_age=86400)
                res.set_cookie("user_name", response_data["user"]["user_name"], httponly=True, secure=SECURE_COOKIE, max_age=86400)
                res.set_cookie("name", response_data["user"]["name"], httponly=True, secure=SECURE_COOKIE, max_age=86400)
                res.set_cookie("email", response_data["user"]["email"], httponly=True, secure=SECURE_COOKIE, max_age=86400)
                res.set_cookie("birth_date", response_data["user"]["birth_date"], httponly=True, secure=SECURE_COOKIE, max_age=86400)

                return res

            return JsonResponse({"error": "Usuario o contraseña incorrectos"}, status=401)

        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": f"Error en la conexión con el microservicio: {str(e)}"}, status=400)

    return render(request, "login.html")

def signup(request):
    if request.method == "POST": 
        data = {
            "name": request.POST.get("name", "").strip(),
            "user_name": request.POST.get("user_name", "").strip(),
            "email": request.POST.get("email", "").strip(),
            "birth_date": request.POST.get("birth_date", "").strip(),
            "password": request.POST.get("password", "").strip(),
        }

        if not all(data.values()):
            return JsonResponse({"error": "Todos los campos son obligatorios"}, status=400)
        
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(f"{USERS_SERVICE_URL}/register/", 
                                     data=json.dumps(data),
                                     headers=headers)
            response.raise_for_status()
            if response.status_code == 201:
                return redirect("login")  # Redirigir al login después de registrarse
                
            return JsonResponse({"error": response.json()}, status=response.status_code)

        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": f"Error en la conexión con el microservicio: {str(e)}"}, status=400)

    return render(request, "register.html")

@require_POST
@login_required_bff
def logout(request):
    return redirect('welcome')

@login_required_bff
def home(request):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render(request, "partials/home.html")  # Carga solo la parte dinámica
    return render(request, "base.html", {"content_template": "partials/home.html"})  # Carga la página completa

@require_POST
@login_required_bff
def post(request):
    # Simulación de envío de datos al microservicio
    api_url = "http://microservicio/posts/"
    data = {
        "user_id": request.user.id,  # ID del usuario autenticado
        "content": request.POST.get("content"),
    }
    headers = {"Authorization": f"Bearer {request.user.auth_token}"}

    try:
        response = requests.post(api_url, json=data, headers=headers)
        if response.status_code == 201:
            return JsonResponse({"message": "Post creado exitosamente"}, status=201)
        else:
            return JsonResponse({"error": "Error al crear el post"}, status=400)
    except requests.exceptions.RequestException:
        return JsonResponse({"error": "Error en la conexión con el microservicio"}, status=500)

@login_required_bff
def post_view(request, post_id):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render(request, "partials/post_view.html", {"post": {}})
    return render(request, "base.html", {"content_template": "partials/post_view.html", "post": {}})

@login_required_bff
def posts(request, user_id=None):
    return render(request, "icons/spinner.html")

@login_required_bff
def comment_operations(request, post_id=None):
    if request.method == "POST":
        return JsonResponse({"message": "Comentario creado exitosamente"})
    elif request.method == "GET":
        return render(request, "icons/spinner.html")
    return JsonResponse({"error": "Método no permitido"}, status=405)

@login_required_bff
def likes(request, user_id):
    return render(request, "icons/spinner.html")

@login_required_bff
def like_operations(request, object_id):
    if request.method == "POST":
        return JsonResponse({"message": "Like creado exitosamente"})
    elif request.method == "DELETE":
        return JsonResponse({"message": "Like eliminado exitosamente"})
    return JsonResponse({"error": "Método no permitido"}, status=405)

@login_required_bff
def reposts(request, user_id):
    return render(request, "icons/spinner.html")

@login_required_bff
def repost_operations(request):
    if request.method == "POST":
        return JsonResponse({"message": "Repost creado exitosamente"})
    elif request.method == "DELETE":
        return JsonResponse({"message": "Repost eliminado exitosamente"})
    return JsonResponse({"error": "Método no permitido"}, status=405)

@login_required_bff
def search_view(request):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render(request, "partials/search.html")
    return render(request, "base.html", {"content_template": "partials/search.html"})

@login_required_bff
def users(request):
    return render(request, "icons/spinner.html")

@login_required_bff
def profile(request, user_id = None):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render(request, "partials/profile.html", {"user": {}})
    return render(request, "base.html", {"content_template": "partials/profile.html", "user": {}})

@login_required_bff
def settings_view(request):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render(request, "partials/settings.html")
    return render(request, "base.html", {"content_template": "partials/settings.html"})

@login_required_bff
def settings_partial(request, option):
    user_data = {
        "name": "name",#request.user.name,
        "user_name": "user_name",#request.user.user_name,
        "birth": "2004-03-02",#str(request.user.birth_date).split("-"), # año - mes - dia
    }
    if option == "account_options":
        return render(request, "partials/account_options.html", {**user_data})
    elif option == "preferences_options":
        return render(request, "partials/preferences_options.html", {**user_data})
    return None

@require_POST
@login_required_bff
def edit_username(request):
    return JsonResponse({"message": "Nombre de usuario actualizado exitosamente"})

@require_POST
@login_required_bff
def edit_password(request):
    return JsonResponse({"message": "Contraseña actualizada exitosamente"})

@require_POST
@login_required_bff
def edit_name(request):
    return JsonResponse({"message": "Nombre actualizado exitosamente"})

@require_POST
@login_required_bff
def edit_birth_date(request):
    return JsonResponse({"message": "Fecha de nacimiento actualizada exitosamente"})

@require_POST
@login_required_bff
def change_password(request):
    return JsonResponse({"message": "Contraseña actualizada exitosamente"})

@require_POST
@login_required_bff
def delete_account(request):
    return JsonResponse({"message": "Cuenta eliminada exitosamente"})

def obtener_usuario(request):
    user_data = {
        "user_id": request.COOKIES.get("user_id"),
        "user_name": request.COOKIES.get("user_name"),
        "name": request.COOKIES.get("name"),
        "email": request.COOKIES.get("email"),
        "birth_date": request.COOKIES.get("birth_date"),
    }
    
    if not user_data["user_id"]:
        return JsonResponse({"error": "No autenticado"}, status=401)

    return JsonResponse(user_data)