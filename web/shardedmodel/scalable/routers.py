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
        if shard_key is None:
            return 'default'
        return logical_to_physical(logical_shard_of(shard_key[0]))

    def db_for_write(self, model, **hints):
        print("Writing to DB: ")
        return self.db_for_read(model, **hints)

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'auth':
            print(model._meta.app_label)
            return 'default'
        
        if model._meta.app_label == 'sessions':
            return 'default'

        db = None    
        try:
            instance = hints.get('instance', None)
            db = self._database_of(instance.shard_by)
        except KeyError:
            try:
                db = self._database_of(hints.get('shard_by'))
            except KeyError:
                print("No instance in hints and no shard_by")
                db = 'default'
        print("Returning", db)
        return db
        

    def allow_migrate(self, db, app_label, model=None, **hints):
        return True