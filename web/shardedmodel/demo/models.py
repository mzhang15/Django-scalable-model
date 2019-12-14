from django.db import models
from scalable.sharded_model import ShardModel
from django.db import models
# Create your models here.

class User(ShardModel):
    is_root = models.BooleanField(default = True)
    name = models.CharField(max_length = 255,primary_key=True)

    @classmethod
    def create(cls, kwargs):
        return cls(**kwargs)

class Post(ShardModel):
    is_root = models.BooleanField(default = False)
    shard_key = models.ForeignKey('User', on_delete = models.CASCADE)
    content = models.CharField(max_length = 255)

    @classmethod
    def create(cls, kwargs):
        return cls(**kwargs)
