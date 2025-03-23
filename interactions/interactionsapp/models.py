import uuid

from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class User(models.Model):
    user_id = models.UUIDField(primary_key=True)
    class Meta:
        managed = False  # Don't manage this model with migrations
        db_table = 'auth"."users'


class Like(models.Model):
    # Save the content type of the object being liked (Tweet or Comment)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # Save the ID of the object being liked (Tweet or Comment)
    object_id = models.UUIDField()
    # Create a generic foreign key to the object being liked, it means that the object being liked can be a Tweet or a Comment
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} liked {self.content_object}'

    class Meta:
        db_table = 'interaction"."likes'
        constraints = [
            UniqueConstraint(fields=['user', 'object_id'], name='PK_Like_User_Object')
        ]

class Tweet(models.Model):
    tweet_id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False)
    class Meta:
        managed = False  # Don't manage this model with migrations
        db_table = 'tweet"."tweet'

class Comment(models.Model):
    comment_id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, name='FK_Comment_User')
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, name='FK_Comment_Tweet')
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} commented {self.content} on {self.tweet}'

    class Meta:
        db_table = 'interaction"."comments'