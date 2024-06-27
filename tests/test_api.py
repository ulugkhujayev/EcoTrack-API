from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.contrib.gis.geos import Point
from core.models import Location, EnvironmentalMetric, EnvironmentalData
from django.utils import timezone


class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)

        self.location = Location.objects.create(
            name="Test Location", coordinates=Point(1.0, 2.0)
        )
        self.metric = EnvironmentalMetric.objects.create(name="Temperature", unit="°C")
        self.data = EnvironmentalData.objects.create(
            location=self.location,
            metric=self.metric,
            value=25.5,
            timestamp=timezone.now(),
            source="Test Source",
        )

    def test_get_locations(self):
        response = self.client.get("/api/locations/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_metrics(self):
        response = self.client.get("/api/metrics/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_environmental_data(self):
        response = self.client.get("/api/data/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_current_data(self):
        response = self.client.get(f"/api/data/current/?lat=2.0&lon=1.0")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_historical_data(self):
        start_date = (timezone.now() - timezone.timedelta(days=1)).isoformat()
        end_date = timezone.now().isoformat()

        start_date = start_date.split(".")[0] + "Z"
        end_date = end_date.split(".")[0] + "Z"

        response = self.client.get(
            f"/api/data/historical/?location={self.location.id}&start_date={start_date}&end_date={end_date}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
