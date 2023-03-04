from django.contrib import admin
from .models import Region
from .models import Weather

# Register your models here.
admin.site.register(Region)
admin.site.register(Weather)