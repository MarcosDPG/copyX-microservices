from django.db import models
import uuid

class Tweet(models.Model):
    tweet_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    content = models.TextField()
    user_id = models.UUIDField()
    retweet_count = models.IntegerField(default=0) 
    
    class Meta:
        db_table = 'tweet"."tweet'  # Coloca la tabla 'tweet' en el esquema 'tweet'

class Retweet(models.Model):
    retweet_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tweet"."retweet'  # Coloca la tabla 'retweet' en el esquema 'tweet'
