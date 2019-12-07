from .models import Mapping
from .utils import MappingDict
from django.conf import settings

def logical_shard_of(shard_key):
    print("shard_key", shard_key)
    print ("logical shard", hash(shard_key) % settings.NUM_LOGICAL_SHARDS)
    return hash(shard_key) % settings.NUM_LOGICAL_SHARDS

def logical_to_physical(logical):
    # TODO：MappingDict should not ask for all mappings
    mapping_dict = MappingDict(Mapping.objects.all())
    target = mapping_dict.get_read_db(logical)
    print("target db", target)
    return target

class ShardRouter(object):
    
    def _database_of(self, shard_key):
        if shard_key is None or len(shard_key) == 0:
            return 'default'
        return logical_to_physical(logical_shard_of(shard_key[0]))

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'auth':
            print(model._meta.app_label)
            return 'default'
        
        if model._meta.app_label == 'sessions':
            return 'default'

        # if model._meta.app_label == 'scalable':
        #     print('app label is scalable')
        #     return 'default'

        db = None
        try:
            instance = hints['instance']
            print("instance", hints['instance'])
            print(instance.shard_by)
            db = self._database_of(instance.shard_by)
        except KeyError:
            try:
                db = self._database_of(hints['shard_by'])
            except KeyError:
                db = 'default'
        #if save() is called by django's own model, can't go through shard manager, thus instance won't have a shard_by field
        except AttributeError:
            db = 'default'
        return db


    def allow_migrate(self, db, app_label, model=None, **hints):
        return True
