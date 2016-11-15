from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from .models import Following, Post, Profile
from .models import FollowingForm, PostForm, MyUserCreationForm
from utils.hints import set_user_for_sharding
from routers import bucket_users_into_shards
from processor import processor

USE_RPC = False

# Anonymous views
#################
def index(request):
  if request.user.is_authenticated():
    return home(request)
  else:
    return anon_home(request)

def anon_home(request):
  return render(request, 'micro/public.html')

def stream(request, user_id):  
  # See if to present a 'follow' button
  form = None
  if request.user.is_authenticated() and request.user.id != int(user_id):
    try:
      following_query = Following.objects
      set_user_for_sharding(following_query, request.user.id)
      f = following_query.get(user_id=request.user.id, followee_id=user_id)
    except Following.DoesNotExist:
      form = FollowingForm
  user_query = Profile.objects
  set_user_for_sharding(user_query, user_id)
  user = user_query.get(pk=user_id)
  post_list = Post.objects.filter(user_id=user_id).order_by('-pub_date')
  set_user_for_sharding(post_list, user_id)
  paginator = Paginator(post_list, 10)
  page = request.GET.get('page')
  try:
    posts = paginator.page(page)
  except PageNotAnInteger:
    # If page is not an integer, deliver first page.
    posts = paginator.page(1) 
  except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
    posts = paginator.page(paginator.num_pages)
  context = {
    'posts' : posts,
    'stream_user' : user,
    'form' : form,
  }
  return render(request, 'micro/stream.html', context)

def register(request):
  if request.method == 'POST':
    form = MyUserCreationForm(request.POST)
    new_user = form.save(commit=True)
    # Create a mirror sharded User model.
    u = Profile(
        user_id=new_user.id, username=new_user.username, 
        first_name=new_user.first_name, last_name=new_user.last_name)
    u.save()
    # Log in that user.
    user = authenticate(username=new_user.username,
                        password=form.clean_password2())
    if user is not None:
      login(request, user)
    else:
      raise Exception
    return home(request)
  else:
    form = MyUserCreationForm
  return render(request, 'micro/register.html', {'form' : form})

# Authenticated views
#####################
@login_required
def home(request):
  '''List of recent posts by people I follow'''
  my_posts = Post.objects.filter(user_id=request.user.id).order_by('-pub_date')
  set_user_for_sharding(my_posts, request.user.id)
  if my_posts:
    my_post = my_posts[0]
  else:
    my_post = None
  following_list =  Following.objects.filter(user_id=request.user.id)
  set_user_for_sharding(following_list, request.user.id)
  follows = [o.followee_id for o in following_list]
  # We need to query every shard where there are users who this user follows
  # We break the users into shards, then for each shard we annotate it with
  # a hint for that shard, issue a query and at the end join all results.
  # Note that this is not very efficient if users are spread accorss many
  # shards. This is where Fan-out could help improve performance.
  shards_to_query = bucket_users_into_shards(follows)
  all_posts = []
  for shard, user_ids in shards_to_query.iteritems():   
    post_list = Post.objects.filter(
      user_id__in=user_ids).order_by('-pub_date')[0:10]
    set_user_for_sharding(post_list, shard)
    # The list comprehension actually invokes the db query in the QuerySet.
    all_posts = all_posts + [p for p in post_list]
  # TODO: Note that all_posts still needs to be sorted by time again, because
  # it is only ordered within each shard.
  context = {
    'post_list': all_posts,
    'my_post' : my_post,
    'post_form' : PostForm
  }
  return render(request, 'micro/home.html', context)

# Allows to post something and shows my most recent posts.
@login_required
def post(request):
  if request.method == 'POST':
    form = PostForm(request.POST)
    new_post = form.save(commit=False)
    new_post.user_id = request.user.id
    new_post.pub_date = timezone.now()
    # Make an RPC call to a backend service to process the post.
    if USE_RPC:
      new_post.text = processor.process_post(new_post.user_id, new_post.id, new_post.text)
    new_post.save()
    return home(request)
  else:
    form = PostForm
  return render(request, 'micro/post.html', {'form' : form})

@login_required
def follow(request):
  if request.method == 'POST':
    form = FollowingForm(request.POST)
    new_follow = form.save(commit=False)
    new_follow.user_id = request.user.id
    new_follow.follow_date = timezone.now()
    new_follow.save()
    return home(request)
  else:
    form = FollowingForm
  return render(request, 'micro/follow.html', {'form' : form})
