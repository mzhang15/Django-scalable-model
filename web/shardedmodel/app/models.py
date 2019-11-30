from django.db import models

# Create your models here.
class ShardModel(models.Model):
    is_root = False
    class Meta:
        abstract = True
        base_manager_name = 'shardManager'

 # TODO: what if user specify the root model multiple times
    def save(self, *args, **kwargs):
        # if current model is the root model
        for att
        # if current model can be sharded

        # if current  mode cdbdban't be sharded
