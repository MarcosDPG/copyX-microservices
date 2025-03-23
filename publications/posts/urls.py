from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TweetViewSet, RetweetViewSet
from .views import TweetViewSet, RetweetViewSet

router = DefaultRouter()
router.register(r'tweets', TweetViewSet)
router.register(r'retweets', RetweetViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('tweets/<uuid:pk>/retweet_count/', TweetViewSet.as_view({'get': 'retweet_count'}), name='retweet_count'),
]
