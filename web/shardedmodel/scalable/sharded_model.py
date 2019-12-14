from django.db import models
from .routers import logical_shard_of, logical_to_physical
from .models import Mapping
from django.conf import settings

READ_ONLY = 1
WRITE_ONLY = 2

class ShardManager(models.Manager):
    def get(self, **kwargs):
        shard_key = None
        try:
            if(self.model.is_root):
                shard_key = kwargs[self.model._meta.pk.name]
            else:
                shard_key = kwargs['shardkey']
            db = logical_to_physical(logical_shard_of(shard_key), 1)
        except KeyError:
            print('Get query must include the shard_key')
        print("get", db)
        queryset = super()._queryset_class(model=self.model, using=db, hints=self._hints)
        queries = queryset.values()

        for query in queries:
            if query.get(queryset.model._meta.pk.name) == shard_key:
                u = queryset.model.create(query)
                print(u)
                return u

def init_mapping():
    print("init mapping")
    if len(Mapping.objects.all()) == 0:

        # TODO: could check if the name of db starts with db
        num_of_db = len(settings.DATABASES) - 1
        if num_of_db == 0:
            print("not setting enought db")
            return

        db_list = list(settings.DATABASES.items())
        mapping = Mapping(min_shard=0, max_shard=settings.NUM_LOGICAL_SHARDS, perm=READ_ONLY, target1=db_list[1][1]['NAME'])
        mapping.save()
        mapping = Mapping(min_shard=0, max_shard=settings.NUM_LOGICAL_SHARDS, perm=WRITE_ONLY, target1=db_list[1][1]['NAME'])
        mapping.save()


class ShardModel(models.Model):
    objects = ShardManager()
    try:
        # this try block prevents the app from crashing during makemigraions
        init_mapping()
    except:
        print('In makemigrations step, cannot init_mapping yet')

    class Meta:
        abstract = True
        
    def save(self, *args, **kwargs):
        # set the root model
        if (hasattr(self,'shard_key') and isinstance(self._meta.get_field('shard_key'), models.ForeignKey)):
            print('save')
            self.shard_by = [super().serializable_value('shard_key')]
            super().save(*args, **kwargs)
            print(self.shard_by)
        elif (hasattr(self,'is_root') and self.is_root):
            self.shard_by = [super().serializable_value(self._meta.pk.name)]
            super().save(*args, **kwargs)
            print(self.shard_by)
        return
