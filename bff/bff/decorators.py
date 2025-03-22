from django.http import JsonResponse

def login_required_bff(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "No autenticado"}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper