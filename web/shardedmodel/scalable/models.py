from django.db import models
from django.conf import settings

class Mapping(models.Model):
    min_shard = models.IntegerField()
    max_shard = models.IntegerField()
    perm = models.IntegerField()
    target1 = models.CharField(max_length=10)
    target2 = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return ("[%d, %d] %d %s %s" % (self.min_shard, self.max_shard, self.perm, self.target1, self.target2))

    def migrate(self, mapping, target):
        pass

def init_mapping():
    print("init mapping")
    if len(Mapping.objects.all()) == 0:
        num_of_db = len(settings.DATABASES) - 1
        db_list = list(settings.DATABASES.items())
        step = int(settings.NUM_LOGICAL_SHARDS / num_of_db)
        read_perm = 1
        write_perm = 2
        print("num of db", num_of_db)
        print("step", step)

        db_list_index = 1
        for shard in range(0, 1024, step):
            db = db_list[db_list_index]
            db_list_index += 1
            # print("db", db)
            # print("db name", db[1]['NAME'])
            print(shard, shard + step - 1, db[1]['NAME'])
            mapping = Mapping(min_shard=shard, max_shard=shard + step - 1, perm=read_perm, target1=db[1]['NAME'])
            mapping.save()
            mapping = Mapping(min_shard=shard, max_shard=shard + step - 1, perm=write_perm, target1=db[1]['NAME'])
            mapping.save()

class ShardManager(models.Manager):
    def get_queryset(self):
        q = super().get_queryset()
        queries = q.values()
        q._hints['shard_by'] = []
        #if current model is the root models
        if hasattr(q.model,'is_root'):
            for query in queries:
                q._hints['shard_by'].append(query.get(q.model._meta.pk.name)) if query.get(q.model._meta.pk.name) != None else None
        elif hasattr(q.model, 'shard_key') :
            for query in queries:
                q._hints['shard_by'].append(query.get('shard_key')) if query.get('shard_key') != None else None
        return q

class ShardModel(models.Model):
    objects = ShardManager()
    init_mapping()

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
