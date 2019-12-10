from .models import Mapping
from .utils import MappingDict
from django.conf import settings

READ_OP = 1
WRITE_OP = 2

def logical_shard_of(shard_key):
    print("shard_key", shard_key)
    print ("logical shard", hash(shard_key) % settings.NUM_LOGICAL_SHARDS)
    return hash(shard_key) % settings.NUM_LOGICAL_SHARDS

def logical_to_physical(logical, op_type):
    # TODO：MappingDict should not ask for all mappings
    mapping_dict = MappingDict(Mapping.objects.all())
    print("logical_to_physical: ", op_type)
    if op_type == READ_OP:
        target = mapping_dict.get_read_db(logical)
    elif op_type == WRITE_OP:
        target = mapping_dict.get_write_db(logical)
    print("target db", target)
    return target

class ShardRouter(object):
    def _database_of(self, shard_key, op_type):
        if shard_key is None or len(shard_key) == 0:
            return 'default'
        return logical_to_physical(logical_shard_of(shard_key[0]), op_type)

    def db_for_write(self, model, **hints):
        hints['op_type'] = WRITE_OP
        return self._db_for_read_write(model, **hints)

    def db_for_read(self, model, **hints):
        hints['op_type'] = READ_OP
        return self._db_for_read_write(model, **hints)

    def _db_for_read_write(self, model, **hints):
        if model._meta.app_label == 'auth':
            print("db_for_read: ", model._meta.app_label)
            return 'default'
        
        if model._meta.app_label == 'sessions':
            return 'default'

        db = None
        try:
            instance = hints['instance']
            print("instance", hints['instance'])
            print(instance.shard_by)
            db = self._database_of(instance.shard_by, hints['op_type'])
        except KeyError:
            try:
                db = self._database_of(hints['shard_by'], hints['op_type'])
            except KeyError:
                db = 'default'
        #if save() is called by django's own model, can't go through shard manager, thus instance won't have a shard_by field
        except AttributeError:
            db = 'default'
        return db

    def allow_relation(self, obj1, obj2, **hints):
        #allow_relations function is needed for app to run in gcp enviroment
        return True

    def allow_migrate(self, db, app_label, model=None, **hints):
        return True
