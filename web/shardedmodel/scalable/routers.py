from .models import Mapping
from .utils import MappingDict

NUM_LOGICAL_SHARDS = 1024

def logical_shard_of(shard_key):
    return hash(shard_key) % NUM_LOGICAL_SHARDS

def logical_to_physical(logical):
    mapping_dict = MappingDict(Mapping.objects.all())
    target = mapping_dict.get_read_db(logical)
    return target

class ShardRouter(object):
    def _database_of(self, shard_key):
        if shard_key is None or len(shard_key) == 0:
            return 'default'
        return logical_to_physical(logical_shard_of(shard_key[0]))

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)

    def db_for_read(self, model, **hints):
        db = None
        try:
            instance = hints['instance']
            print("instance", hints['instance'])
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
