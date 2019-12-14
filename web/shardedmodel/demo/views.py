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
        # posts = Post.objects.get(shard_key=fk)
        # serializer = PostSerializer(posts, many=True)
        user = User(name='user1')
        post1 = Post(shard_key=user, content='fake post 1')
        post2 = Post(shard_key=user, content='fake post 2')
        posts = [post1, post2]
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        print("post post....")
        data = JSONParser().parse(request)
        print(data)
        serializer = PostSerializer(data=data)
        print(serializer)
        if serializer.is_valid():
            print("is valid...")
            user = User(name=data['shard_key'])
            post = Post(shard_key=user, content=data['content'])
            print(post)
            # post.save()
            # serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

# @csrf_exempt
# def post_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         # user = User.objects.get(pk=pk)
#         print("post detail: ", pk)
#         post = Post.objects.get(shard_key=pk)
#     except Post.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = PostSerializer(post)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = PostSerializer(post, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         post.delete()
#         return HttpResponse(status=204)