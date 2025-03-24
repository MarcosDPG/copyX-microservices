#api/urls.py
from django.views.decorators.csrf import csrf_exempt
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('update/', views.update_user, name='update_user'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('logout/', views.logout_view, name='logout'),
    path('protected/', views.protected_view, name='protected'),
    path('validate_token/', views.validate_token, name='validate_token'),
    path('user/<uuid:user_id>/', views.get_user_by_id, name='get_user_by_id'),
]