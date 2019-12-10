from django.db import models
from django.conf import settings

READ_ONLY = 1
WRITE_ONLY = 2

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


