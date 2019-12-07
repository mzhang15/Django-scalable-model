from scalable.models import Mapping

class MappingDict:
    def __init__(self, mappings):
        self.read_mappings = [m for m in mappings if m.perm == 0]
        self.write_mappings = [m for m in mappings if m.perm == 1]
    def get_read_db(self, logical):
        for m in self.read_mappings:
            if (logical >= m.min_shard and logical <= m.max_shard):
                return m.target1
        return None
    def get_write_db(self, logical):
        for m in self.write_mappings:
            if (logical >= m.min_shard and logical <= m.max_shard):
                return m.target1
        return None
