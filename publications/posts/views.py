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
        try:
            tweet = Tweet.objects.get(tweet_id=pk)
            return Response({"retweet_count": tweet.retweet_count})
        except Tweet.DoesNotExist:
            return Response({"error": "Tweet not found"}, status=404)

    def perform_create(self, serializer):
        if not self.request.data.get("user_id"):
            serializer.save(user_id=uuid.UUID("00000000-0000-0000-0000-000000000000"))  # UUID por defecto
        else:
            serializer.save()

class RetweetViewSet(viewsets.ModelViewSet):
    queryset = Retweet.objects.all()
    serializer_class = RetweetSerializer

    def perform_create(self, serializer):
        retweet = serializer.save()
        tweet = get_object_or_404(Tweet, tweet_id=retweet.tweet.tweet_id)
        tweet.retweet_count += 1
        tweet.save()