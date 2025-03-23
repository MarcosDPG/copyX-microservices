from django.db import models
import uuid

class User(models.Model):
    user_id = models.UUIDField(primary_key=True)
    class Meta:
        managed = False
        db_table = 'auth"."users'

class Tweet(models.Model):
    tweet_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tweets")
    
    class Meta:
        db_table = 'tweet"."tweet'  # Coloca la tabla 'tweet' en el esquema 'tweet'

class Retweet(models.Model):
    retweet_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="retweets")

    class Meta:
        db_table = 'tweet"."retweet'  # Coloca la tabla 'retweet' en el esquema 'tweet'
