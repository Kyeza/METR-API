from django.test import TestCase

from telemetry.models import Device


class DeviceModelTest(TestCase):
    """Test Device Model"""

    def setUp(self) -> None:
        Device.objects.get_or_create(identnr=69656545)
        Device.objects.get_or_create(identnr=67756545)

    def test_device_creation(self):
        Device.objects.get_or_create(identnr=69653345)

        num_of_devices = Device.objects.count()

        self.assertEqual(num_of_devices, 3, msg=f'expected: {3} got: {num_of_devices}')
