from django.conf import settings
from django.shortcuts import render

# rest framework
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# my import
from .serializers import TweetSerializer, TweetActionSerializer, TweetCreateSerializer
from .forms import TweetForm
from tweets.models import Tweet

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

"""
status = 201  # for created items after submitting
status = 403  # user is not authenticated
status = 404  # file does not exist
status = 401  # this is unauthorized meaning you aint the 
owner of what u are trying to delete
status = 500  # server error
"""


def home_view(request, *args, **kwargs):
    context = {}

    return render(request, 'tweet/tweet_home.html', context)


@api_view(['POST'])  # http method that the client has to send === POST
# @authentication_classes([SessionAuthentication]) #
@permission_classes([IsAuthenticated])  # user must be logged in
def tweet_create_view(request, *args, **kwargs):
    print(request.data)
    serializer = TweetCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        print(serializer.data)
        """ in here we are sending what we submitted in our form data in json 
        format response to our javascript with status 201  """
        return Response(serializer.data, status=201)
    return Response({}, status=400)


@api_view(['GET'])  # http method that the client has to get
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    username = request.GET.get('username')  # ?username=favour
    if username is not None:
        qs = qs.filter(user__username__iexact=username)

    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)  # filtering for the detail page id
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=200)


@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])  # user must be logged in
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)  # filtering for the detail page id
    if not qs.exists():
        return Response({'message': 'Tweet does not exist'}, status=404)
    qs = qs.filter(user=request.user)
    obj = qs.first()
    obj.delete()
    return Response({'message': 'Tweet removed'}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # user must be logged in
def tweet_action_view(request, tweet_id=None, *args, **kwargs):
    """
    id is required
    Action options are Likes ,Unlike and  retweet
    note we are sending data from the front end to this place
    """
    print(request.POST, request.data)
    serializer = TweetActionSerializer(data=request.data)  # we dont use request.post in here
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get('id')
        action = data.get('action')
        content = data.get('content')

        qs = Tweet.objects.filter(id=tweet_id)  # filtering for the detail page id
        if not qs.exists():
            return Response({'message': 'Tweet does not exist'}, status=404)
        obj = qs.first()
        if action == 'like':
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)

        elif action == 'unlike':
            obj.likes.remove(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)

        elif action == 'retweet':
            new_tweet = Tweet.objects.create(user=request.user,
                                             parent=obj, content=content)
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status=201)
        if request.user in obj.likes.all():
            obj.likes.remove(request.user)

    return Response({}, status=200)
