from rest_framework import serializers
from .models import Like, Comment

class LikeSerializer(serializers.ModelSerializer):
    content_type = serializers.IntegerField()
    object_id = serializers.UUIDField()
    user = serializers.UUIDField()
    class Meta:
        model = Like
        fields = ['user', 'object_id', 'content_type']
        read_only_fields = ['id']

class CommentSerializer(serializers.ModelSerializer):
    content = serializers.CharField(max_length=300, required=True, min_length=3)
    user = serializers.UUIDField()
    tweet = serializers.UUIDField()
    comment_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Comment
        fields = ['comment_id', 'user', 'tweet', 'content']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = str(instance.user.user_id)
        representation['tweet'] = str(instance.tweet.tweet_id)
        return representation