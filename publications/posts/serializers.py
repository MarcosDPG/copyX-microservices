from rest_framework import serializers
from .models import Tweet, Retweet
from django.utils.timesince import timesince
from django.utils import timezone

class TweetSerializer(serializers.ModelSerializer):
    retweet_count = serializers.SerializerMethodField()
    content = serializers.CharField(max_length=300)
    user_id = serializers.UUIDField()
    tweet_id = serializers.UUIDField(read_only=True)
    delta_created = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = ["content" , "user_id" , "tweet_id" , "retweet_count", "delta_created"]
        read_only_fields = ["retweet_count" , "delta_created"]

    def get_retweet_count(self, obj):
        return Retweet.objects.filter(tweet_id=obj.tweet_id).count()

    def get_delta_created(self, obj):  
        delta = timezone.now() - obj.created_at  # ✅ Usar el campo del modelo
        days = delta.days
        seconds = delta.seconds
        hours = seconds // 3600
        minutes = seconds // 60

        if days > 0:
            return f"{days}D"
        elif hours > 0:
            return f"{hours}Hrs"
        elif minutes > 0:
            return f"{minutes}min"
        else:
            return f"{seconds}seg"

class RetweetSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField() 
    delta_created = serializers.SerializerMethodField()  
    class Meta:
        model = Retweet
        fields = ["retweet_id", "tweet_id", "user_id", "created_at" , "delta_created"]
    
    def get_delta_created(self, obj):  
        delta = timezone.now() - obj.created_at  # ✅ Usar el campo del modelo
        days = delta.days
        seconds = delta.seconds
        hours = seconds // 3600
        minutes = seconds // 60

        if days > 0:
            return f"{days}D"
        elif hours > 0:
            return f"{hours}Hrs"
        elif minutes > 0:
            return f"{minutes}min"
        else:
            return f"{seconds}seg"