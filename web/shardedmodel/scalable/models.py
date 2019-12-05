from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

from django_autoshard import utils
from django_autoshard.managers import ShardedManager, UserManager


class ShardedModel(models.Model):
    id = models.BigIntegerField(primary_key=True)

    objects = ShardedManager()

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(ShardedModel, self).__init__(*args, **kwargs)
        try:
            key = getattr(self, self.SHARD_KEY)  # kwargs[self.SHARD_KEY]
        except AttributeError:
            raise RuntimeError('{} does not define a SHARD_KEY'.format(self.__repr__()))
        except KeyError:
            raise RuntimeError('{} does not have {} set'.format(self.__repr__(), self.SHARD_KEY))
        self.__shard = utils.get_shard(key)

    @property
    def shard(self):
        return self.__shard

    def save(self, *args, **kwargs):
        kwargs['using'] = self.shard.alias
        if self.pk is not None:
            return super(ShardedModel, self).save(*args, **kwargs)  # UPDATE
        self.id = utils.generate_uuid(self.shard.index)
        return super(ShardedModel, self).save(*args, **kwargs)  # Set the auto-id


class ShardRelatedModel(models.Model):
    class Meta:
        abstract = True

    @property
    def shard(self):
        for field in self._meta.fields:
            pass
ß