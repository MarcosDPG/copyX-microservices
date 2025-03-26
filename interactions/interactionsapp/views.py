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
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif Like.objects.filter(user=serializer.validated_data['user'], object_id=serializer.validated_data['object_id']).exists():
        return JsonResponse({'message': 'Ya le diste like a este objeto'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        create_like(Comment if serializer.validated_data['content_type'] == 1 else Tweet, serializer.validated_data['object_id'], serializer.validated_data['user'])
        return JsonResponse(serializer.validated_data, status=status.HTTP_201_CREATED)
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
        return JsonResponse({'message':'Like eliminado con éxito'},status=status.HTTP_404_NOT_FOUND)

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
        return JsonResponse(serializer.validated_data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            return JsonResponse({'message':f'Comentario con id {id} no existe'},status=status.HTTP_404_NOT_FOUND)

        comment.delete()
        Like.objects.filter(content_type=ContentType.objects.get_for_model(Comment), object_id=id).delete()
        return JsonResponse({"message":"El comantario fue eliminado con éxito"},status=status.HTTP_204_NO_CONTENT)
    else:
        try:
            comment = Comment.objects.get(comment_id=id)
        except Comment.DoesNotExist:
            return JsonResponse({'message':f'Comentario con id {id} no existe'},status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(comment)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

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
    comments = Comment.objects.filter(tweet_id=id).order_by('-created_at')

    if not comments.exists():
        return JsonResponse({'message':f'No hay comentarios para el tweet con id {id}'},status=status.HTTP_404_NOT_FOUND)

    # Add the delta_created and likes_count fields to the comments
    for comment in comments:
        comment.delta_created = get_delta_created(comment.created_at)
        comment.likes_count = Like.objects.filter(content_type=ContentType.objects.get_for_model(Comment), object_id=comment.comment_id).count()

    serializer = CommentSerializer(comments, many=True)
    return JsonResponse(serializer.data)

"""
Return all the tweets that a user has liked, if the user has not liked any tweets, return a 404 status code.
Recieves a user_id as a parameter in the URL and returns a JSON object with the tweets ids like this:
{
    "tweets_ids": ["tweet_id1", "tweet_id2", ...]
}
"""
@api_view(['GET'])
def get_likes(request, user_id):
    try:
        likes = Like.objects.filter(user_id=user_id, content_type=ContentType.objects.get_for_model(Tweet))
        tweets_ids = [like.object_id for like in likes]
        if not tweets_ids:
            return JsonResponse({'message':'El usuario no ha dado likes a tweets'},status=status.HTTP_404_NOT_FOUND)
        return JsonResponse({'tweets_ids':tweets_ids})
    except Tweet.DoesNotExist:
        return JsonResponse({'message':'Tweet no encontrado'},status=status.HTTP_404_NOT_FOUND)

"""
Return the number of likes and comments for a list of tweets. Recieves a JSON object with the following format:
{
    "tweet_ids": ["tweet_id1", "tweet_id2", ...]
}
Returns a JSON object with the following format:
{
    "tweet_id1": {
        "likes_count": 0,
        "comments_count": 0
    },
    "tweet_id2": {
        "likes_count": 0,
        "comments_count": 0
    },
    ...
}
"""
@api_view(['POST'])
def tweets_stats(request):
    tweet_ids = request.data.get('tweet_ids', [])
    if not tweet_ids:
        return JsonResponse({'message':'No se han proporcionado tweets_ids'},status=status.HTTP_400_BAD_REQUEST)

    stats = {
        tweet_id: {
            'likes_count': Like.objects.filter(object_id=tweet_id).count(),
            'comments_count': Comment.objects.filter(tweet_id=tweet_id).count(),
        }
        for tweet_id in tweet_ids
    }

    return JsonResponse(stats)

"""
Return the interactions (like_id and comment_id) for a user and a specific post. Recieves a JSON object with the following format:
{
    "ids": ["post_id1", "post_id2", ...],
    "user_id": user_id,
    "content_type": content_type / 1 for Comment, 2 for Tweet
}
Returns a JSON object with the following format:
{
    "post_id1": {
        "like_id": "like_id",
        "comment_id": "comment_id"
    },
    "post_id2": {
        "like_id": "like_id",
        "comment_id": "comment_id"
    },
    ...
}
"""
@api_view(['POST'])
def posts_interactios(request):
    # Validar los datos de entrada
    post_ids = request.data.get('ids', [])
    if not post_ids:
        return JsonResponse({'message': 'No se han proporcionado post_ids'}, status=status.HTTP_400_BAD_REQUEST)

    user_id = request.data.get('user_id', None)
    if not user_id:
        return JsonResponse({'message': 'No se ha proporcionado user_id'}, status=status.HTTP_400_BAD_REQUEST)

    content_type = request.data.get('content_type', None)
    if not content_type:
        return JsonResponse({'message': 'No se ha proporcionado content_type'}, status=status.HTTP_400_BAD_REQUEST)

    # Obtener el ContentType correspondiente
    content_type_model = Comment if content_type == 1 else Tweet
    content_type_instance = ContentType.objects.get_for_model(content_type_model)

    # Construir la respuesta
    respuesta = {
        post_id: get_interactions(user_id, post_id, content_type_instance)
        for post_id in post_ids
    }

    return JsonResponse({'message': respuesta})

"""
Obtiene las interacciones (like_id y comment_id) para un usuario y un post específico.
"""
def get_interactions(user_id, post_id, content_type):
    return {
        'like_id': get_like_id(user_id, post_id, content_type),
        'comment_id': get_comment_id(user_id, post_id)
    }

"""
Obtiene el ID del like si existe, o una cadena vacía si no.
"""
def get_like_id(user_id, post_id, content_type):
    like = Like.objects.filter(user_id=user_id, object_id=post_id, content_type=content_type).first()
    return like.id if like else ""

"""
Obtiene el ID del comentario si existe, o una cadena vacía si no.
"""
def get_comment_id(user_id, post_id):
    comment = Comment.objects.filter(user_id=user_id, tweet_id=post_id).first()
    return comment.comment_id if comment else ""