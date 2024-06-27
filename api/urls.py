from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LocationViewSet, EnvironmentalMetricViewSet, EnvironmentalDataViewSet

router = DefaultRouter()
router.register(r"locations", LocationViewSet)
router.register(r"metrics", EnvironmentalMetricViewSet)
router.register(r"data", EnvironmentalDataViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
