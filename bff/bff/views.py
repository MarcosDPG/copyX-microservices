from django.contrib import messages
from django.shortcuts import render, redirect
from .decorators import login_required_bff, redirect_if_authenticated_bff
from django.views.decorators.http import require_POST, require_GET
from django.http import JsonResponse
import requests
import json
from bff.settings import USERS_SERVICE_URL, PUBLICATIONS_SERVICE_URL, SECURE_COOKIE, DEBUG

CONTENT_DATA = {
        "user_id": "",
        "my_repost_id": "",
        "tweet_id": "",
        "id_like": "", #id del like                             ####
        "comment_id": "",
        "comments_count": "",
        "likes_count": "", #cantidad de likes que tiene el post o comentario    ####
        "retweet_count": "",
        "delta_created": "", #diferencia de tiempo desde que se creó el post    ####
        "content": "", #contenido del post o comentario         ####
        "name": "", #name de quien creo el post o comentario    ####
        "user_name": "", #user_name de quien creo el post
        "user_name_commenter": "", #user_name de quien comento  ####
        "user_name_reposter": "", #user_name de quien reposteó
    }

@redirect_if_authenticated_bff
def welcome(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, "index.html")

@redirect_if_authenticated_bff
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

@redirect_if_authenticated_bff
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

@require_GET
@login_required_bff
def logout(request):
    token = request.COOKIES.get("auth_token")

    try:
        # Enviar petición al microservicio con el token en la cabecera Authorization
        response = requests.post(
            f"{USERS_SERVICE_URL}/logout/",
            headers={"Authorization": f"Token {token}"}
        )

        if response.status_code == 200:
            response = redirect("welcome")
            response.delete_cookie("auth_token")
            response.delete_cookie("user_id")
            response.delete_cookie("user_name")
            response.delete_cookie("name")
            response.delete_cookie("email")
            response.delete_cookie("birth_date")
            return response

        return JsonResponse(response.json(), status=response.status_code)

    except requests.exceptions.RequestException:
        return JsonResponse({"error": "Error al cerrar sesión"}, status=400)

@login_required_bff
def home(request):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render(request, "partials/home.html")  # Carga solo la parte dinámica
    return render(request, "base.html", {"content_template": "partials/home.html", **obtener_usuario(request)})  # Carga la página completa

@require_POST
@login_required_bff
def post(request):
    data = {
        "user_id": request.COOKIES.get("user_id"),
        "content": request.POST.get("content"),
    }
    headers = {"Authorization": f"Bearer {request.COOKIES.get('auth_token')}"}

    try:
        response = requests.post(f"{PUBLICATIONS_SERVICE_URL}/posts/tweets/", json=data, headers=headers)
        if response.status_code == 201:
            return JsonResponse({"message": "Post creado exitosamente"}, status=201)
        else:
            return JsonResponse({"error": "Error al crear el post"}, status=400)
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": f"Error en la conexión con el microservicio: {str(e)}"}, status=500)

@login_required_bff
def post_view(request, post_id):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render(request, "partials/post_view.html", {"post": obtener_post_data(request, post_id)})
    #return JsonResponse(obtener_post_data(request, post_id))
    return render(request, "base.html", {"content_template": "partials/post_view.html", "post": obtener_post_data(request, post_id)})

@login_required_bff
def posts(request, user_id=None):
    try:
        response = requests.get(f"{PUBLICATIONS_SERVICE_URL}/posts/tweets/", params={"user_id": user_id} if user_id else {})
        response.raise_for_status()
        data_posts = response.json()
    except Exception as e:
        return JsonResponse({"error": f"Error en la conexión con el microservicio: {str}"})
    return render(request, "partials/posts_list.html", {"posts": obtener_posts_data(request,tweets=data_posts)})

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

    try:
        if user_id:
            user_id = str(user_id)
            headers = {"Authorization": f"Token {request.COOKIES.get('auth_token')}"}
            response = requests.get(f"{USERS_SERVICE_URL}/user/{user_id}/", headers=headers)
            response.raise_for_status()
            #response2 = requests.get(f"{PUBLICATIONS_SERVICE_URL}/tweets/count/{user_id}/")
            #response2.raise_for_status()
            #posts_count = response2.json()["posts_count"]
            view_data = response.json()
        else:
             #response2 = requests.get(f"{PUBLICATIONS_SERVICE_URL}/tweets/count/{request.COOKIES.get('user_id')}/")
            #response2.raise_for_status()
            #posts_count = response2.json()["posts_count"]
            view_data = {}

        #return JsonResponse(user_data) 
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return render(request, "partials/profile.html", {**obtener_usuario(request), "data": {"posts_count": 0, **view_data}})
        return render(request, "base.html", {"content_template": "partials/profile.html", **obtener_usuario(request), "data": {"posts_count": 0, **view_data}})
    except requests.exceptions.RequestException as e:
        return render(request, "base.html", {"content_template": "partials/profile.html", "error": f"Error en la conexión con el microservicio: {str(e)}"})

@login_required_bff
def settings_view(request):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render(request, "partials/settings.html")
    return render(request, "base.html", {"content_template": "partials/settings.html", **obtener_usuario(request)})

@login_required_bff
def settings_partial(request, option):
    if option == "account_options":
        return render(request, "partials/account_options.html", obtener_usuario(request))
    elif option == "preferences_options":
        return render(request, "partials/preferences_options.html", obtener_usuario(request))
    return None

@require_POST
@login_required_bff
def edit_username(request):
    data = {"user_name": request.POST.get("user_name", "").strip()}
    if not data["user_name"]:
        messages.error(request, "El nombre de usuario es obligatorio")
        return redirect("settings")
    return updateUserData(request, data)

@require_POST
@login_required_bff
def edit_name(request):
    data = {"name": request.POST.get("name", "").strip()}
    if not data["name"]:
        messages.error(request, "El nombre es obligatorio")
        return redirect("settings")
    return updateUserData(request, data)

@require_POST
@login_required_bff
def edit_birth_date(request):
    data = {
        "year": request.POST.get("year", "").strip(),
        "month": request.POST.get("month", "").strip(),
        "day": request.POST.get("day", "").strip(),
    }

    if not all(data.values()):
        messages.error(request, "Todos los campos de la fecha son obligatorios")
        return redirect("settings")

    birth_date = f"{data['year']}-{data['month']}-{data['day']}"
    return updateUserData(request, {"birth_date": birth_date})

@require_POST
@login_required_bff
def change_password(request):
    data = {
        "old_password": request.POST.get("old_password", "").strip(),
        "new_password1": request.POST.get("new_password1", "").strip(),
        "new_password2": request.POST.get("new_password2", "").strip(),
    }

    if not all(data.values()):
        messages.error(request, "Todos los campos son obligatorios")
        return redirect("settings")

    if data["new_password1"] != data["new_password2"]:
        messages.error(request, "Las contraseñas no coinciden")
        return redirect("settings")

    # Verificar la contraseña actual del usuario
    credentials = {
        "user_name": request.COOKIES.get("user_name"),
        "password": data["old_password"],
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(f"{USERS_SERVICE_URL}/login/", json=credentials, headers=headers)
        response.raise_for_status()

        if response.status_code == 200:
            return updateUserData(request, {"password": data["new_password1"]})

        messages.error(request, "Contraseña actual incorrecta")
    
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Error en la conexión con el microservicio: {str(e)}" if DEBUG else "Error al actualizar la contraseña")

    return redirect("settings")

def updateUserData(request, data={}): 
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {request.COOKIES.get('auth_token')}"
    }

    try:
        response = requests.patch(f"{USERS_SERVICE_URL}/update/", json=data, headers=headers)
        response.raise_for_status()
        res_data = response.json()

        if response.status_code == 200:
            messages.success(request, "Datos actualizados exitosamente")
            response_bff = redirect("settings")

            # Actualizar cookies con la nueva información del usuario
            response_bff.set_cookie("user_id", res_data["user"]["user_id"])
            response_bff.set_cookie("user_name", res_data["user"]["user_name"])
            response_bff.set_cookie("name", res_data["user"]["name"])
            response_bff.set_cookie("email", res_data["user"]["email"])
            response_bff.set_cookie("birth_date", res_data["user"]["birth_date"])

            return response_bff
    
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Error en la conexión con el microservicio: {str(e)}" if DEBUG else "Error al actualizar los datos")
        return redirect("settings")


@require_POST
@login_required_bff
def delete_account(request):
    data = {
        "password": request.POST.get("password", "").strip()
    }

    if not data["password"]:
        messages.error(request, "No es posible eliminar la cuenta sin verificar que seas tu")
        return redirect("settings")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {request.COOKIES.get('auth_token')}"
    }

    try:
        response = requests.delete(f"{USERS_SERVICE_URL}/delete_account/", json=data, headers=headers)
        response.raise_for_status()

        if response.status_code == 200:
            response_bff = redirect("welcome")
            response_bff.delete_cookie("auth_token")
            response_bff.delete_cookie("user_id")
            response_bff.delete_cookie("user_name")
            response_bff.delete_cookie("name")
            response_bff.delete_cookie("email")
            response_bff.delete_cookie("birth_date")
            return response_bff

    except requests.exceptions.RequestException as e:
        messages.error(request, f"Error en la conexión con el microservicio: {str(e)}" if DEBUG else "Error al eliminar la cuenta")
    
    return redirect("settings")

def obtener_usuario(request):
    user_data = {
        "user_id": request.COOKIES.get("user_id"),
        "user_name": request.COOKIES.get("user_name"),
        "name": request.COOKIES.get("name"),
        "email": request.COOKIES.get("email"),
        "birth_date": request.COOKIES.get("birth_date"),
        "birth": request.COOKIES.get("birth_date","--").split("-"),
    }
    
    if not user_data["user_id"]:
        return {"error": "No autenticado"}

    return user_data

def obtener_post_data(request, post_id):
    try:
        return obtener_posts_data(request, [post_id])[0]
    except Exception as e:
        return {"error": f"Error al obtener los datos del post: {str(e)}" if DEBUG else "Error al obtener los datos del post"}

def obtener_posts_data(request, post_ids=None, tweets=None):
    posts = [] 
    headers = {"Authorization": f"Token {request.COOKIES.get('auth_token')}"}

    if not tweets and post_ids:
        try:
            response = requests.post(f"{PUBLICATIONS_SERVICE_URL}/tweets/get_by_ids/", json={"ids": post_ids}, headers=headers)
            response.raise_for_status()
            tweets = response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error en la conexión con el microservicio PUBLICATIONS: {str(e)}" if DEBUG else "Error al obtener los datos de los posts")
    elif not tweets:
        raise RuntimeError(f"No hay datos necesarios para procesar")

    user_ids = list({tweet["user_id"] for tweet in tweets})  # Conjunto → Lista para eliminar duplicados

    try:
        response_users = requests.post(f"{USERS_SERVICE_URL}/users/", json={"ids": user_ids}, headers=headers)
        response_users.raise_for_status()
        users_data = response_users.json()
    except requests.exceptions.RequestException as e:
        users_data = {}
        #raise RuntimeError(f"Error en la conexión con el microservicio USERS: {str(e)}" if DEBUG else "Error al obtener los datos de los usuarios")

    for tweet in tweets:
        tweet_data = CONTENT_DATA.copy()
        tweet_data.update(tweet)

        user_info = users_data.get(tweet["user_id"], {})  # Obtener datos del usuario o vacío si no está
        tweet_data["name"] = user_info.get("name", "Desconocido")
        tweet_data["user_name"] = user_info.get("user_name", "Desconocido")

        posts.append(tweet_data)

    return posts
