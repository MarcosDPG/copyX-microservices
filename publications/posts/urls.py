from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TweetViewSet, RetweetViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'tweets', TweetViewSet)
router.register(r'retweets', RetweetViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
