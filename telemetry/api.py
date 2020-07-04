from django_filters import rest_framework as filters
from rest_framework import mixins, viewsets
from rest_framework_csv.renderers import CSVRenderer

from telemetry.models import Message, Device
from telemetry.serializers import DeviceTelemetrySerializer, DeviceLatestTelemetryCVSSerializer


class DeviceTelemetryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    """
    Device Telemetry
        - Lists all messages sent to the backend for any device
        - Creates messages to be sent to the backend from the gateway's payload for various devices and their telemetry
    """
    queryset = Message.objects.all()
    serializer_class = DeviceTelemetrySerializer


class LatestTelemetryCVSViewSet( mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    LatestTelemetryCVS
        - returns the latest telemetry message CSV for a particular device or all devices
    """
    queryset = Device.objects.all()
    serializer_class = DeviceLatestTelemetryCVSSerializer
    renderer_classes = [CSVRenderer]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('identnr',)
