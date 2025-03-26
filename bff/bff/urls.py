"""
URL configuration for bff project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.welcome, name='welcome'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path("home/", views.home, name="home"),
    path("post/", views.post, name="post"),
    path("post/<str:post_id>", views.post_view, name="post_detail"),
    path("posts/", views.posts, name="posts"),
    path("posts/<str:user_id>", views.posts, name="posts_user_id"),
    path("comment/", views.comment_operations, name="comment"),
    path("comments/<str:post_id>", views.comment_operations, name="comments"),
    path("likes/<str:user_id>", views.likes, name="likes_user_id"),
    path("like/<str:object_id>", views.like_operations, name="like"),
    path("reposts/<str:user_id>", views.reposts, name="reposts_user_id"),
    path("repost/<str:content_id>", views.repost_operations, name="repost"),
    path("search/", views.search_view, name="search"),
    path("users/", views.users, name="users"),
    path("profile/", views.profile, name="profile_auth"),
    path("profile/<str:user_id>", views.profile, name="profile_user_id"),
    path("compose/post/", views.home, name="compose_post"),
    path("settings/", views.settings_view, name="settings"),
    path('settings/<str:option>/', views.settings_partial, name='settings_partial'),
    path('user/edit/username/', views.edit_username, name='edit_username'),
    path('user/edit/name/', views.edit_name, name='edit_name'),
    path('user/edit/birth_date/', views.edit_birth_date, name='edit_birth_date'),
    path('user/change_password/', views.change_password, name='change_password'),
    path('user/delete_account/', views.delete_account, name='delete_account'),
]

# Servir archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])