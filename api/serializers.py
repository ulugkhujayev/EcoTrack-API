from rest_framework import serializers
from core.models import Location, EnvironmentalMetric, EnvironmentalData

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'coordinates']

class EnvironmentalMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnvironmentalMetric
        fields = ['id', 'name', 'unit']

class EnvironmentalDataSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    metric = EnvironmentalMetricSerializer()

    class Meta:
        model = EnvironmentalData
        fields = ['id', 'location', 'metric', 'value', 'timestamp', 'source']