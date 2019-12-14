from django.db import models
from scalable.sharded_model import ShardModel
from django.db import models
# Create your models here.

class User(ShardModel):
    # class Meta:
    #     app_label = 'scalable'
    is_root = models.BooleanField(default = True)
    name = models.CharField(max_length = 255,primary_key=True)

    @classmethod
    def create(cls, kwargs):
        return cls(**kwargs)
