from django.test import TestCase
from scalable.models import Root, Child
# Create your tests here.

class shardTestCase(TestCase):
    def test_correct_shard_key(self):
        Root.objects.create(name='test')
        test = Root.objects.get(name= 'test')
        Child.objects.create(name='ha', shard_key = test)
        Child.objects.get(name= 'ha')
