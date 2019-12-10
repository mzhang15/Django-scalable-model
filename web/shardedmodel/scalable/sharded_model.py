from django.db import models
from .routers import logical_shard_of, logical_to_physical
from .models import Mapping
from django.conf import settings

READ_ONLY = 1
WRITE_ONLY = 2

class ShardManager(models.Manager):
    # TODO: pass in a dict **kwargs and check if name is given
    def get(self, pk):
        db = logical_to_physical(logical_shard_of(pk), 1)
        print(db)
        queryset = super()._queryset_class(model=self.model, using=db, hints=self._hints)
        # specify which table to look (User.objects.using('db').get())
        queries = queryset.values()

        for query in queries:
            if query.get(queryset.model._meta.pk.name) == pk:
                print ("result: ", query)
                u = queryset.model.create(pk)
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

        # step = int(settings.NUM_LOGICAL_SHARDS / num_of_db)
        # print("num of db", num_of_db)
        # print("step", step)

        # db_list_index = 1
        # for shard in range(0, 1024, step):
        #     db = db_list[db_list_index]
        #     db_list_index += 1
        #     # print("db", db)
        #     # print("db name", db[1]['NAME'])
        #     print(shard, shard + step - 1, db[1]['NAME'])
        #     mapping = Mapping(min_shard=shard, max_shard=shard + step - 1, perm=READ_ONLY, target1=db[1]['NAME'])
        #     mapping.save()
        #     mapping = Mapping(min_shard=shard, max_shard=shard + step - 1, perm=WRITE_ONLY, target1=db[1]['NAME'])
        #     mapping.save()


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