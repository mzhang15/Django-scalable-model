from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from demo.models import User, Post
from demo.serializers import UserSerializer, PostSerializer

@csrf_exempt
def user_list(request, db=0):
    """
    List all users under db, or create a new user.
    """
    if request.method == 'GET':
        users = User.objects.using(db).all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        print("post....")
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = User(name=data['name'])
            user.save()
            # serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def user_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        # user = User.objects.get(pk=pk)
        print("user detail: ", pk)
        user = User.objects.get(name=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=204)


@csrf_exempt
def post_list(request, fk):
    """
    List all posts for a user, or create a new post.
    """
    if request.method == 'GET':
        # TODO: need Shelly to debug post get method
        user = User(name=fk)
        posts = Post.objects.get(shard_key=user)
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        try:
            print("post post....")
            data = JSONParser().parse(request)
            print(data)
            user = User.objects.get(name=data['shard_key'])
            user.save()
            post = Post(shard_key=user, content=data['content'])
            post.save()
            return JsonResponse(data, status=201)
        except:
            return JsonResponse('Error when creating post', status=400)
