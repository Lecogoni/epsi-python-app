from django.db import models
from datetime import date
from django.utils import timezone

# Create your models here.
class Region(models.Model):
    regionName = models.CharField(max_length=255)
    regionCode = models.IntegerField()


    def __str__(self):
        return "%s" % (self.regionName)  
    

class Weather(models.Model):
    name = models.CharField(max_length=255)
    codeInsee = models.IntegerField(unique=True, null=True)
    date = models.DateField(default=timezone.now) # models.DateField(default=date.today, blank=True)
    tmin = models.IntegerField(null=True)
    tmax = models.IntegerField(null=True)
    probarain = models.IntegerField(null=True)

    def __str__(self):
        return "%s %s " % (self.name, self.codeInsee)
    