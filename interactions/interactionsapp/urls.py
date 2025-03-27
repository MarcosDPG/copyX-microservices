from django.urls import path
from . import views

urlpatterns = [
    path('likes', views.create_like_api, name='create_like'),
    path('likes/user/<uuid:user_id>/object/<uuid:object_id>', views.delete_like, name='delete_like'),
    path('likes/user/<uuid:user_id>/tweets', views.get_likes, name='get_likes'),
    path('comments', views.create_comment, name='create_comment'),
    path('comments/<uuid:id>', views.get_delete_comment, name='get_delete_comment'),
    path('comments/tweet/<uuid:id>', views.post_comment, name='post_comment'),
    path('tweets/stats', views.tweets_stats, name='tweets_stats'),
    path('tweets', views.posts_interactios, name='posts_interactios'),
]