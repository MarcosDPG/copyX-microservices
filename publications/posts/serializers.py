from rest_framework import serializers
from .models import Tweet, Retweet

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = "__all__"

class RetweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retweet
        fields = "__all__"