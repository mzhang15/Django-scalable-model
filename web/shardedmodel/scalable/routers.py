from scalable import models
from scalable import utils
from django.conf import settings
from .models import Mapping

def logical_shard_of(shard_key):
    return shard_keys % NUM_LOGICAL_SHARDS

def logical_to_physical(logical):
    mapping_dict = MappingDict(Mapping.objects.all())
    target = mapping_dict.get_read_db(logical)
    return target

class ShardRouter(object):
    def _database_of(self, shard_key):
        return logical_to_physical(logical_shard_of(shard_key))

    def _db_for_write(self, model, **hints):
        print("Writing to DB: ")
        return self._db_for_read(model, **hints)

    def _db_for_read(self, model, **hints):
        if model._meta.app_label != 'scalable':
            print('default')
            return 'default'
        try:
            shard_keys = hints['instance'].shard_by
        except:
            try:
                shard_keys = hints['shard_by']
            except:
                print('default')
                return 'default'
        print(_database_of(shard_keys[0]['name'])) 
        return _database_of(shard_keys[0]['name'])
