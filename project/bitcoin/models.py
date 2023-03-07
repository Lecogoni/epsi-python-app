from django.db import models

# Create your models here.
class Currency(models.Model):
    
    currencyCode = models.CharField(max_length=10)
    currencyName = models.CharField(max_length=100,null=True)
    icon = models.CharField(max_length=255)
    status = models.BooleanField
    available_in_historical_data_from = models.DateField
    available_in_historical_data_till = models.DateField
    countryCode = models.CharField(max_length=30,null=True)
    countryName = models.CharField(max_length=50,null=True)
    currencyRates = models.JSONField(null=True)

    def __str__(self):
        return "%s %s %s %s %s %s %s %s %s" % (self.currencyCode, self.currencyName, self.icon, self.status, self.available_in_historical_data_from, self.available_in_historical_data_till, self.countryCode, self.countryName , self.currencyRates)