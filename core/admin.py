from django.contrib import admin
from .models import Location, EnvironmentalMetric, EnvironmentalData

admin.site.register(Location)
admin.site.register(EnvironmentalMetric)
admin.site.register(EnvironmentalData)
