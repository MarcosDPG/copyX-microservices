from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
import uuid
from .models import Tweet, Retweet
from .serializers import TweetSerializer, RetweetSerializer

class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    @action(detail=True, methods=["get"])
    def retweet_count(self, request, pk=None):
        tweet = get_object_or_404(Tweet, tweet_id=pk)
        count = tweet.retweets.count()  # Contar los retweets relacionados
        return Response({"retweet_count": count})

    def perform_create(self, serializer):
        user_id = self.request.data.get("user_id", "00000000-0000-0000-0000-000000000000")
        serializer.save(user_id=uuid.UUID(user_id))

class RetweetViewSet(viewsets.ModelViewSet):
    queryset = Retweet.objects.all()
    serializer_class = RetweetSerializer

    def perform_create(self, serializer):
        serializer.save()
