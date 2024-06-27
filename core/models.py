from django.contrib.gis.db import models
from django.db.models import JSONField


class Location(models.Model):
    name = models.CharField(max_length=255)
    coordinates = models.PointField()

    def __str__(self):
        return self.name


class EnvironmentalMetric(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.unit})"


class EnvironmentalData(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    metric = models.ForeignKey(EnvironmentalMetric, on_delete=models.CASCADE)
    value = models.FloatField()
    timestamp = models.DateTimeField()
    source = models.CharField(max_length=100)
    raw_data = JSONField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["location", "metric", "timestamp"]),
        ]

    def __str__(self):
        return f"{self.metric.name} at {self.location} - {self.timestamp}"
