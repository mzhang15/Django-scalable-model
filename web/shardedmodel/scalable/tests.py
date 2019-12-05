from django.test import TestCase
from scalable import utils

class utilTests(TestCase):
    def setUp(self):
        pass

    def test_generate_uuid(self):
        print()
        print('Generating uuid with index 1')
        print('*** Generated uuid:', utils.generate_uuid(1))
        print()
        
    def test_get_shard_id_uuid(self):
        print('Retreving shard index from uuid created with 1')
        uuid = utils.generate_uuid(1)
        print('*** Retreved index:', utils.get_shard_index_from_uuid(uuid))
        print()

    # def test_get_shard_from_index(self):
    #     print('Getting shard with index 1')
    #     print('Shard info:', utils.get_shard_from_index(1))
