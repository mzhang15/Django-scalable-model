from django.db import models
        
class Mapping(models.Model):
    min_shard = models.IntegerField()
    max_shard = models.IntegerField()
    perm = models.IntegerField()
    target1 = models.CharField(max_length=10)
    target2 = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return ("[%d, %d] %d %s %s" % (self.min_shard, self.max_shard, self.perm, self.target1, self.target2)) 