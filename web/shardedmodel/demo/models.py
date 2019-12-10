from django.db import models
from scalable.manager import ShardModel
from django.db import models

class User(ShardModel):
    is_root = models.BooleanField(default = True)
    name = models.CharField(max_length = 255,primary_key=True)
    nid = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)


class Post(ShardModel):
    is_root = models.BooleanField(default = False)
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    text = models.CharField(max_length = 255,primary_key=True)