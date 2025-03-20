from django.db import models
import uuid

class Tweet(models.Model):
    tweet_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    content = models.TextField()
    user_id = models.UUIDField()
    comments_count = models.IntegerField(default=0)
    retweet_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)

class Retweet(models.Model):
    retweet_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
