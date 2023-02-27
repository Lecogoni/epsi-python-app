from django.db import models

# Create your models here.
class Region(models.Model):
    regionName = models.CharField(max_length=255)
    regionCode = models.IntegerField()
    regionVisited = models.BooleanField()

    def __str__(self):
        return "%s %s %s" % (self.regionName, self.regionCode, self.regionVisited)  