from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TweetViewSet, RetweetViewSet

router = DefaultRouter()
router.register(r'tweets', TweetViewSet)
router.register(r'retweets', RetweetViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
