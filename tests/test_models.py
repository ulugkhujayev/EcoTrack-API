from django.test import TestCase
from django.contrib.gis.geos import Point
from core.models import Location, EnvironmentalMetric, EnvironmentalData
from django.utils import timezone


class LocationModelTest(TestCase):
    def test_location_creation(self):
        location = Location.objects.create(
            name="Test Location", coordinates=Point(1.0, 2.0)
        )
        self.assertEqual(str(location), "Test Location")
        self.assertEqual(location.coordinates.x, 1.0)
        self.assertEqual(location.coordinates.y, 2.0)


class EnvironmentalMetricModelTest(TestCase):
    def test_environmental_metric_creation(self):
        metric = EnvironmentalMetric.objects.create(name="Temperature", unit="°C")
        self.assertEqual(str(metric), "Temperature (°C)")


class EnvironmentalDataModelTest(TestCase):
    def setUp(self):
        self.location = Location.objects.create(
            name="Test Location", coordinates=Point(1.0, 2.0)
        )
        self.metric = EnvironmentalMetric.objects.create(name="Temperature", unit="°C")

    def test_environmental_data_creation(self):
        data = EnvironmentalData.objects.create(
            location=self.location,
            metric=self.metric,
            value=25.5,
            timestamp=timezone.now(),
            source="Test Source",
        )
        self.assertEqual(str(data), f"Temperature at Test Location - {data.timestamp}")
