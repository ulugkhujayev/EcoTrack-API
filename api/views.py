from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from core.models import Location, EnvironmentalMetric, EnvironmentalData
from .serializers import (
    LocationSerializer,
    EnvironmentalMetricSerializer,
    EnvironmentalDataSerializer,
)
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg
from rest_framework.decorators import action
from rest_framework.response import Response


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class EnvironmentalMetricViewSet(viewsets.ModelViewSet):
    queryset = EnvironmentalMetric.objects.all()
    serializer_class = EnvironmentalMetricSerializer


class EnvironmentalDataViewSet(viewsets.ModelViewSet):
    queryset = EnvironmentalData.objects.all()
    serializer_class = EnvironmentalDataSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["location", "metric", "source"]
    ordering_fields = ["timestamp"]

    @action(detail=False, methods=["get"])
    def current(self, request):
        lat = request.query_params.get("lat")
        lon = request.query_params.get("lon")
        if not lat or not lon:
            return Response(
                {"error": "Latitude and longitude are required."}, status=400
            )

        point = Point(float(lon), float(lat), srid=4326)
        locations = Location.objects.filter(coordinates__distance_lte=(point, D(km=10)))

        latest_data = (
            EnvironmentalData.objects.filter(
                location__in=locations,
                timestamp__gte=timezone.now() - timedelta(hours=1),
            )
            .order_by("location", "metric", "-timestamp")
            .distinct("location", "metric")
        )

        serializer = self.get_serializer(latest_data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def historical(self, request):
        location_id = request.query_params.get("location")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if not all([location_id, start_date, end_date]):
            return Response(
                {"error": "Location, start_date, and end_date are required."},
                status=400,
            )

        data = EnvironmentalData.objects.filter(
            location_id=location_id, timestamp__range=[start_date, end_date]
        ).order_by("timestamp")

        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def aggregated(self, request):
        location_id = request.query_params.get("location")
        metric_id = request.query_params.get("metric")
        aggregation = request.query_params.get("aggregation", "daily")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if not all([location_id, metric_id, start_date, end_date]):
            return Response(
                {"error": "Location, metric, start_date, and end_date are required."},
                status=400,
            )

        data = EnvironmentalData.objects.filter(
            location_id=location_id,
            metric_id=metric_id,
            timestamp__range=[start_date, end_date],
        )

        if aggregation == "daily":
            data = (
                data.annotate(date=TruncDate("timestamp"))
                .values("date")
                .annotate(avg_value=Avg("value"))
            )
        elif aggregation == "weekly":
            data = (
                data.annotate(week=TruncWeek("timestamp"))
                .values("week")
                .annotate(avg_value=Avg("value"))
            )
        elif aggregation == "monthly":
            data = (
                data.annotate(month=TruncMonth("timestamp"))
                .values("month")
                .annotate(avg_value=Avg("value"))
            )
        else:
            return Response({"error": "Invalid aggregation parameter."}, status=400)

        return Response(data)

    @action(detail=False, methods=["get"])
    def nearby(self, request):
        lat = request.query_params.get("lat")
        lon = request.query_params.get("lon")
        radius = request.query_params.get("radius", 10)  # Default radius of 10 km

        if not lat or not lon:
            return Response(
                {"error": "Latitude and longitude are required."}, status=400
            )

        point = Point(float(lon), float(lat), srid=4326)
        locations = Location.objects.filter(
            coordinates__distance_lte=(point, D(km=float(radius)))
        )

        latest_data = (
            EnvironmentalData.objects.filter(
                location__in=locations,
                timestamp__gte=timezone.now() - timedelta(hours=1),
            )
            .order_by("location", "metric", "-timestamp")
            .distinct("location", "metric")
        )

        serializer = self.get_serializer(latest_data, many=True)
        return Response(serializer.data)
