from rest_framework import serializers
from .models import Tweet, Retweet

class TweetSerializer(serializers.ModelSerializer):
    retweet_count = serializers.SerializerMethodField()
    content = serializers.CharField(max_length=300)
    user_id = serializers.UUIDField()
    tweet_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Tweet
        fields = ["content" , "user_id" , "tweet_id" , "retweet_count"]
        read_only_fields = ["retweet_count"]

    def get_retweet_count(self, obj):
        return Retweet.objects.filter(tweet=obj).count()

class RetweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retweet
        fields = "__all__"