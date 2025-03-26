from rest_framework import viewsets
from rest_framework.decorators import action
from .models import Tweet, Retweet
from rest_framework.response import Response
from .serializers import TweetSerializer, RetweetSerializer

class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    @action(detail=True, methods=["get"], url_path="tweets")
    def user_tweets(self, request, pk=None):
        tweets = Tweet.objects.filter(user_id=pk)
        serializer = self.get_serializer(tweets, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["post"])
    def get_by_ids(self, request):
        tweet_ids = request.data.get("ids", [])  # Obtener IDs desde el cuerpo JSON
        tweets = Tweet.objects.filter(tweet_id__in=tweet_ids)
        serializer = TweetSerializer(tweets, many=True)
        return Response(serializer.data)

class RetweetViewSet(viewsets.ModelViewSet):
    queryset = Retweet.objects.all()
    serializer_class = RetweetSerializer

    def perform_create(self, serializer):
        serializer.save()
    
    