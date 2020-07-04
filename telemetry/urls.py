from django.urls import path, include
from rest_framework import routers

from telemetry.api import DeviceTelemetryViewSet, LatestTelemetryCVSViewSet

router = routers.DefaultRouter()
router.register('device_message', DeviceTelemetryViewSet)
router.register('telemetry_cvs', LatestTelemetryCVSViewSet)

app_name = 'telemetry'
urlpatterns = [
    path('api/', include(router.urls)),
]
