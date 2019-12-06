
# Create your tests here.
from django.test import TestCase
from scalable.models import Root, Child, Mapping
from scalable.utils import MappingDict
# Create your tests here.

class shardTestCase(TestCase):
    def test_correct_shard_key(self):
        Root.objects.create(name='test')
        Root.objects.create(name='test1')
        print('######Gets:')
        test1 = Root.objects.get(name= 'test1')
    def test_mapping_table(self):
        print('mapping:')
        Mapping.objects.create(min_shard=0, max_shard=3, perm=0, target1='db1')
        Mapping.objects.create(min_shard=0, max_shard=3, perm=1, target1='db1')
        Mapping.objects.create(min_shard=4, max_shard=7, perm=0, target1='db2')
        Mapping.objects.create(min_shard=4, max_shard=7, perm=1, target1='db2')
        print('created mapping for shards from 0-3 read/write to db1')
        print('created mapping for shards from 4-7 read/write to db2')
        mapping_dict = MappingDict(Mapping.objects.all())
        print('Read db for shard 7: ', mapping_dict.get_read_db(7))
        print('Read db for shard 2: ', mapping_dict.get_read_db(2))
        print('Read db for shard 8 (does not exist): ', mapping_dict.get_read_db(8))
        print('Write db for shard 7: ', mapping_dict.get_write_db(7))
        print('Write db for shard 2: ', mapping_dict.get_write_db(2))
        print('Write db for shard 8 (does not exist): ', mapping_dict.get_write_db(8))
