from rest_framework import serializers
from .models import Tweet, Retweet, Comment

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = "__all__"

class RetweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retweet
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
