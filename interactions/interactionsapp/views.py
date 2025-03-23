from http import HTTPStatus

from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from .models import Like, Comment, Tweet
from .serializers import LikeSerializer

def create_like(model, object_id, user_id):
    content_type = ContentType.objects.get_for_model(model)
    obj = model.objects.get(pk=object_id)
    like = Like.objects.create(
        user_id=user_id,
        content_type=content_type,
        object_id=obj.pk
    )
    return like

"""
Create a like for a Tweet or a Comment, if the user has already liked the object, return a 400 status code
Recieves a JSON object with the following format:
{
    "content_type": 1, // 1 for Comment, 2 for Tweet
    "object_id": comment_id or tweet_id,
    "user": user_id
}
"""
@api_view(['POST'])
def create_like_api(request):
    serializer = LikeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif Like.objects.filter(user=serializer.validated_data['user'], object_id=serializer.validated_data['object_id']).exists():
        return Response({'message': 'Ya le diste like a este objeto'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        create_like(Comment if serializer.validated_data['content_type'] == 1 else Tweet, serializer.validated_data['object_id'], serializer.validated_data['user'])
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
    except (Tweet.DoesNotExist, Comment.DoesNotExist):
        return JsonResponse({"message": "Objeto no encontrado"}, status=HTTPStatus.NOT_FOUND)

"""
Delete a like for a Tweet or a Comment if it exists, if the like does not exist, return a 404 status code
Recieves a user_id and an object_id as parameters in the URL
"""
@api_view(['DELETE'])
def delete_like(request, user_id, object_id):
    try:
        like = Like.objects.get(user=user_id, object_id=object_id)
    except Like.DoesNotExist:
        return Response({'message':'Like eliminado con éxito'},status=status.HTTP_404_NOT_FOUND)

    like.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
