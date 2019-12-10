from django.db import models
from .routers import logical_shard_of, logical_to_physical

class ShardManager(models.Manager):
    # TODO: pass in a dict **kwargs and check if name is given
    def get(self, pk):
        db = logical_to_physical(logical_shard_of(pk), 1)
        # print(db)
        queryset = super()._queryset_class(model=self.model, using=db, hints=self._hints)
        # specify which table to look (User.objects.using('db').get())
        queries = queryset.values()

        for query in queries:
            if query.get(queryset.model._meta.pk.name) == pk:
                print ("result: ", query)
                u = queryset.model.create(pk)
                print(u)
                return u
        

    # def get_queryset(self):
    #     print("get_queryset...")
    #     q = super().get_queryset()
    #     print("super queryest: ", q)
    #     queries = q.values()
    #     q._hints['shard_by'] = []
    #     #if current model is the root models
    #     if hasattr(q.model,'is_root'):
    #         print("iterate query...")
    #         print("queryset: ", queries)
    #         for query in queries:
    #             print(query.get(q.model._meta.pk.name))
    #             q._hints['shard_by'].append(query.get(q.model._meta.pk.name)) if query.get(q.model._meta.pk.name) != None else None
    #     elif hasattr(q.model, 'shard_key') :
    #         for query in queries:
    #             q._hints['shard_by'].append(query.get('shard_key')) if query.get('shard_key') != None else None
    #     return q

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