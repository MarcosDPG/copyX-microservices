from django.shortcuts import render
from rest_framework import viewsets
from .models import Tweet, Retweet, Comment
from .serializers import TweetSerializer, RetweetSerializer, CommentSerializer

class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

class RetweetViewSet(viewsets.ModelViewSet):
    queryset = Retweet.objects.all()
    serializer_class = RetweetSerializer

