from http import HTTPStatus

from django.utils import timezone
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from .models import Like, Comment, Tweet
from .serializers import LikeSerializer, CommentSerializer

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

"""
Create a comment for a Tweet, if the user has already commented the object, return a 400 status code
Recieves a JSON object with the following format:
{
    "content": "comment content",
    "user": user_id,
    "tweet": tweet_id
}
"""
@api_view(['POST'])
def create_comment(request):
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        comment = Comment.objects.create(
            user_id=serializer.validated_data['user'],
            tweet_id=serializer.validated_data['tweet'],
            content=serializer.validated_data['content']
        )
        serializer.validated_data['id'] = comment.comment_id
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
Delete a comment for a Tweet if it exists, if the comment does not exist, return a 404 status code. Recieves a comment_id as a parameter in the URL
Get a comment for a Tweet if it exists, if the comment does not exist, return a 404 status code. Recieves a comment_id as a parameter in the URL and returns a JSON object with the comment data
like this:
{
    "comment_id": "comment_id",
    "user": "user_id",
    "tweet": "tweet_id",
    "content": "comment content"
}
"""
@api_view(['DELETE','GET'])
def get_delete_comment(request, id):
    if request.method == 'DELETE':
        try:
            comment = Comment.objects.get(comment_id=id)
        except Comment.DoesNotExist:
            return Response({'message':f'Comentario con id {id} no existe'},status=status.HTTP_404_NOT_FOUND)

        comment.delete()
        return Response({"message":"El comantario fue eliminado con éxito"},status=status.HTTP_204_NO_CONTENT)
    else:
        try:
            comment = Comment.objects.get(comment_id=id)
        except Comment.DoesNotExist:
            return Response({'message':f'Comentario con id {id} no existe'},status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

"""
Return the delta time between the current time and the time the object was created in the following format:
- If the object was created more than a day ago, return the number of days
- If the object was created more than an hour ago, return the number of hours
- If the object was created more than a minute ago, return the number of minutes
- If the object was created less than a minute ago, return the number of seconds
Recieves a datetime object as a parameter
"""
def get_delta_created(fecha):
    delta = timezone.now() - fecha
    days = delta.days
    seconds = delta.seconds
    hours = seconds // 3600
    minutes = seconds // 60

    if days > 0:
        return f"{days}D"
    elif hours > 0:
        return f"{hours}Hrs"
    elif minutes > 0:
        return f"{minutes}min"
    else:
        return f"{seconds}seg"

"""
Return all the comments for a Tweet, if there are no comments, return a 404 status code. Recieves a tweet_id as a parameter in the URL and returns a JSON object with the comments data like this:
{
    "comment_id": "comment_id",
    "user": "user_id",
    "tweet": "tweet_id",
    "content": "comment content",
    "likes_count": 0,
    "delta_created": "Hace un instante"
}
"""
@api_view(['GET'])
def post_comment(request, id):
    comments = Comment.objects.filter(tweet_id=id)

    if not comments.exists():
        return Response({'message':f'No hay comentarios para el tweet con id {id}'},status=status.HTTP_404_NOT_FOUND)

    # Add the delta_created and likes_count fields to the comments
    for comment in comments:
        comment.delta_created = get_delta_created(comment.created_at)
        comment.likes_count = Like.objects.filter(content_type=ContentType.objects.get_for_model(Comment), object_id=comment.comment_id).count()

    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)
