from rest_framework import serializers
from .models import Like

class LikeSerializer(serializers.ModelSerializer):
    content_type = serializers.IntegerField()
    object_id = serializers.UUIDField()
    user = serializers.UUIDField()
    class Meta:
        model = Like
        fields = ['id', 'user', 'object_id', 'content_type']
        read_only_fields = ['id']
