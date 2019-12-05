import bisect
import time
import hashlib
import random

from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured
from scalable import settings
from django.utils import timezone


def get_shard_index(key):
    _hash = hashlib.md5(key.encode()).hexdigest()
    return int(_hash, 16) % settings.MAX_SHARDS


def get_shard_index_from_uuid(uuid):
    return (uuid >> 10) & 0x1FFF


def get_shard(key):
    index = get_shard_index(key)
    return get_shard_from_index(index)


def get_shard_from_index(index):
    try:
        return django_settings.SHARDS[index]
    except KeyError:
        shard_indexes = list(django_settings.SHARDS.keys())
        pos = bisect.bisect(shard_indexes, index)
        if pos >= len(shard_indexes):
            pos = 0
        index = shard_indexes[pos:pos + 1][0]
        return django_settings.SHARDS[index]


def generate_uuid(shard_index):
    try:
        epoch = timezone.datetime.strptime(settings.EPOCH, '%Y-%m-%d')
        epoch = time.mktime(epoch.timetuple()) * 1000
    except ValueError:
        raise ImproperlyConfigured('EPOCH must be in Y-m-d format')
    local_id = random.randint(0, 1204)
    now = time.time() * 1000
    result = int(now - epoch) << 23
    result |= shard_index << 10
    result |= local_id % 1024
    return result
