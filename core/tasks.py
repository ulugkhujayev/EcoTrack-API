from celery import shared_task
from django.conf import settings
import requests
from .models import Location, EnvironmentalMetric, EnvironmentalData
from django.utils import timezone
from .utils import normalize_data


@shared_task
def fetch_environmental_data():
    locations = Location.objects.all()

    for location in locations:
        fetch_openaq_data.delay(location.id)
        fetch_openweathermap_data.delay(location.id)


@shared_task
def fetch_openaq_data(location_id):
    location = Location.objects.get(id=location_id)
    url = f"https://api.openaq.org/v2/latest"
    params = {
        "coordinates": f"{location.coordinates.y},{location.coordinates.x}",
        "radius": 10000,
        "limit": 100,
        "api_key": settings.OPENAQ_API_KEY,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        for result in data["results"]:
            for measurement in result["measurements"]:
                metric, _ = EnvironmentalMetric.objects.get_or_create(
                    name=measurement["parameter"], unit=measurement["unit"]
                )
                normalized_data = normalize_data("openaq", measurement)
                EnvironmentalData.objects.create(
                    location=location,
                    metric=metric,
                    value=normalized_data["value"],
                    timestamp=timezone.now(),
                    source="OpenAQ",
                    raw_data=measurement,
                )


@shared_task
def fetch_openweathermap_data(location_id):
    location = Location.objects.get(id=location_id)
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": location.coordinates.y,
        "lon": location.coordinates.x,
        "appid": settings.OPENWEATHERMAP_API_KEY,
        "units": "metric",
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        metrics = {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
        }

        for name, value in metrics.items():
            metric, _ = EnvironmentalMetric.objects.get_or_create(
                name=name,
                unit=(
                    "°C"
                    if name == "temperature"
                    else "%" if name == "humidity" else "hPa"
                ),
            )
            normalized_data = normalize_data(
                "openweathermap", {"name": name, "value": value}
            )
            EnvironmentalData.objects.create(
                location=location,
                metric=metric,
                value=normalized_data["value"],
                timestamp=timezone.now(),
                source="OpenWeatherMap",
                raw_data=data,
            )
