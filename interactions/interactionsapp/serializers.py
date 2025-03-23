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
    post = serializers.UUIDField()
    id = serializers.URLField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'content']