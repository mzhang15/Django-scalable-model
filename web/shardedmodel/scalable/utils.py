from scalable.models import Mapping
from django.conf import settings
import importlib

class MappingDict:
    # TODO： you don't need to pass all mappings to this class; just use Mapping.objects.all() here
    def __init__(self, mappings):
        print(mappings)
        self.read_mappings = [m for m in mappings if m.perm == 1]
        self.write_mappings = [m for m in mappings if m.perm == 2]
    def get_read_db(self, logical):
        for m in self.read_mappings:
            if (logical >= m.min_shard and logical <= m.max_shard):
                return m.target1
        return None
    def get_mapping(self, logical):
        for m in self.read_mappings:
            if (logical >= m.min_shard and logical <= m.max_shard):
                return m
        return None
    def get_write_db(self, logical):
        for m in self.write_mappings:
            if (logical >= m.min_shard and logical <= m.max_shard):
                return m.target1
        return None

def migration(shard_mapping_id):
    split_db = Mapping.objects.get(id = 3)
    customized_models = importlib.import_module(settings.CUSTOMIZED_MODEL_MODULE)
    shardable_models = settings.SHARDABLE_MODELS.split(',')
    for model in shardable_models:
        model_to_migrate = getattr(customized_models, model)
        model_to_migrate.objects.using(split_db).all()
