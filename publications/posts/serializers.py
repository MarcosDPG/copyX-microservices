from rest_framework import serializers
from .models import Tweet, Retweet
from django.utils.timesince import timesince

class TweetSerializer(serializers.ModelSerializer):
    retweet_count = serializers.SerializerMethodField()
    content = serializers.CharField(max_length=300)
    user_id = serializers.UUIDField()
    tweet_id = serializers.UUIDField(read_only=True)
    time_since_creation = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = ["content" , "user_id" , "tweet_id" , "retweet_count", "time_since_creation"]
        read_only_fields = ["retweet_count"]

    def get_retweet_count(self, obj):
        return Retweet.objects.filter(tweet=obj).count()
    
    def get_time_since_creation(self, obj):
        return timesince(obj.created_at)

class RetweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retweet
        fields = "__all__"