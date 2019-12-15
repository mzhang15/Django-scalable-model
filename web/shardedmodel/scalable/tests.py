
# Create your tests here.
from django.test import TestCase
from scalable.models import Root, Child, Mapping
from scalable.utils import MappingDict
from django.db import models
# Create your tests here.

class ShardTestCase(TestCase):
    def test_correct_shard_key(self):
        Root.objects.create(name='test')
        Root.objects.create(name='test1')
        test1 = Root.objects.get(name= 'test1')
