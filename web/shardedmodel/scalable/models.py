from django.db import models

class Mapping(models.Model):
    min_shard = models.IntegerField()
    max_shard = models.IntegerField()
    perm = models.IntegerField()
    target1 = models.CharField(max_length=10)
    target2 = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return ("[%d, %d] %d %s %s" % (self.min_shard, self.max_shard, self.perm, self.target1, self.target2))

class ShardManager(models.Manager):
    def get_queryset(self):
        q = super().get_queryset()
        #if current model is the root models
        if hasattr(q.model,'is_root'):
            print(dir(q.query))
            #how to get the name of the query fields?
            #e.g. if input has pk, use as shard_key
            try:
                instance = q._hints['instance']
            except KeyError:
                print('no instance in hint')
        #if current model is not Root
            #if current model has a foreign field points to Root
                #if somehow the query points to an root instance

            #if not, go to not sharable db
        return q


class ShardModel(models.Model):
    objects = ShardManager()
    class Meta:
        abstract = True
    def save(self, *args, **kwargs):
        # set the root model
        if (hasattr(self,'shard_key') and isinstance(self._meta.get_field('shard_key'), models.ForeignKey)):
            self.shard_by = super().serializable_value('shard_key')
            super().save(*args, **kwargs)
        elif (hasattr(self,'is_root') and self.is_root):
            self.shard_by = super().serializable_value(self._meta.pk.name)
            super().save(*args, **kwargs)
        return

class Root(ShardModel):
    class Meta:
        app_label = 'app'
    is_root = models.BooleanField(default = True)
    name = models.CharField(max_length = 255,primary_key=True)

class Child(ShardModel):
    class Meta:
        app_label = 'app'
    name = models.CharField(max_length = 10, primary_key = True)
    shard_key = models.ForeignKey('Root', null=True,on_delete=models.CASCADE)
