from scalable.models import Mapping

class MappingDict:
    # TODO： you don't need to pass all mappings to this class; just use Mapping.objects.all() here
    def __init__(self, mappings):
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
