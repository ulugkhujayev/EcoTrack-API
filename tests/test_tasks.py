from django.test import TestCase
from unittest.mock import patch
from core.tasks import fetch_openaq_data, fetch_openweathermap_data
from core.models import Location, EnvironmentalMetric, EnvironmentalData
from django.contrib.gis.geos import Point


class TasksTestCase(TestCase):
    def setUp(self):
        self.location = Location.objects.create(
            name="Test Location", coordinates=Point(1.0, 2.0)
        )

    @patch("core.tasks.requests.get")
    def test_fetch_openaq_data(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "results": [
                {"measurements": [{"parameter": "pm25", "value": 10, "unit": "µg/m³"}]}
            ]
        }

        fetch_openaq_data(self.location.id)

        self.assertEqual(EnvironmentalMetric.objects.count(), 1)
        self.assertEqual(EnvironmentalData.objects.count(), 1)

    @patch("core.tasks.requests.get")
    def test_fetch_openweathermap_data(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "main": {"temp": 25, "humidity": 60, "pressure": 1013}
        }

        fetch_openweathermap_data(self.location.id)

        self.assertEqual(EnvironmentalMetric.objects.count(), 3)
        self.assertEqual(EnvironmentalData.objects.count(), 3)
