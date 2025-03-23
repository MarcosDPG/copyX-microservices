from rest_framework import viewsets
from .models import Tweet, Retweet
from .serializers import TweetSerializer, RetweetSerializer

class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

class RetweetViewSet(viewsets.ModelViewSet):
    queryset = Retweet.objects.all()
    serializer_class = RetweetSerializer

    def perform_create(self, serializer):
        serializer.save()
