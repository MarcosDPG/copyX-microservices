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
    
    @action(detail=False, methods=["get"], url_path="count")
    def get_tweets_count(self, request):
        user_id = request.query_params.get("user_id")
        if not user_id:
            return Response({"error": "user_id is required"}, status=400)
        count = Tweet.objects.filter(user_id=user_id).count()
        return Response({
            "user_id": user_id,
            "tweet_count": count,
            }, status=200)

class RetweetViewSet(viewsets.ModelViewSet):
    queryset = Retweet.objects.all()
    serializer_class = RetweetSerializer

    @action(detail=False, methods=["post"], url_path="interaction")
    def get_retweets_interaction(self, request):
        pk = request.data.get("user_id")
        tweet_ids = request.data.get("ids", [])
        if tweet_ids and pk:
            respuesta = {
                tweet_id: get_interactions(pk, tweet_id)
                for tweet_id in tweet_ids
            }
            return Response(respuesta)
        else:
            return Response({"error": "No se han enviado los datos necesarios"}, status=400)
        
    @action(detail=True, methods=["get"], url_path="retweets")
    def user_retweets(self, request, pk=None):
        retweets = Retweet.objects.filter(user=pk)
        serializer = self.get_serializer(retweets, many=True)
        return Response(serializer.data)
        
    def perform_create(self, serializer):
        serializer.save()
    

def get_interactions(user_id, post_id):
    def get_retweet_id(user_id, post_id):
        retweet = Retweet.objects.filter(user=user_id, tweet_id=post_id).first()
        return retweet.retweet_id if retweet else ""
    return {
        'retweet_id': get_retweet_id(user_id, post_id),
    }