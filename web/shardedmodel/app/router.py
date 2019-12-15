from django.db import models
from scalable.models import Root, Child

            #if shard_key is provided by the get_queryset
            #if not provided
class ShardRouter(object):
     def db_for_read(self, model, **hints):
         return None

     def db_for_write(self, model, **hints):

         return None
