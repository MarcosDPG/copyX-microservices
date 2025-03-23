from django.urls import path
from . import views

urlpatterns = [
    path('likes', views.create_like_api, name='create_like'),
    path('likes/user/<uuid:user_id>/object/<uuid:object_id>', views.delete_like, name='delete_like'),
    path('comments', views.create_comment, name='create_comment'),
    path('comments/<uuid:id>', views.get_delete_comment, name='get_delete_comment'),
    # path('likes/post/<uuid:user_id>&<uuid:publication_id>/', views.post_like, name='post_like'),
    # path('likes/post/<uuid:user_id>&<uuid:publication_id>/count', views.post_like_count, name='post_like'),
    # path('comments/post/<uuid:id>', views.post_comment, name='post_comment'),
    # path('comments/postuuid:id>/count', views.post_comment_count, name='post_comment')
]