from collections import OrderedDict

from rest_framework import serializers

from telemetry.models import Value, Device, Message


class ValueSerializer(serializers.ModelSerializer):
    """Value serializer"""
    class Meta:
        model = Value
        fields = [
            'value', 'tariff', 'subunit', 'dimension', 'storagenr'
        ]


class DeviceSerializer(serializers.ModelSerializer):
    """Device serializer for creating devices"""
    type = serializers.IntegerField()

    def create(self, validated_data):
        # return device if already exits with the same [identnr] else create it device in database
        # to avoid duplicate devices with the same id
        device, created = Device.objects.get_or_create(identnr=validated_data['identnr'])

        if created:
            device.device_type = validated_data['type']
            device.status = validated_data['status']
            device.version = validated_data['version']
            device.accessnr = validated_data['accessnr']
            device.manufacturer = validated_data['manufacturer']
            device.save()

        return device

    class Meta:
        model = Device
        fields = [
            'type', 'status', 'identnr', 'version', 'accessnr',
            'manufacturer'
        ]


class DeviceTelemetrySerializer(serializers.ModelSerializer):
    """Telemetry Serializer"""
    data = ValueSerializer(write_only=True, many=True)
    device = DeviceSerializer(write_only=True)

    def create(self, validated_data):
        device_data = validated_data['device']
        values_data = validated_data['data']

        # return device if already exits with the same [identnr] else create it device in database
        device, created = Device.objects.get_or_create(identnr=device_data['identnr'])

        # if created then update it other values from the default values
        if created:
            device.device_type = device_data['type']
            device.status = device_data['status']
            device.version = device_data['version']
            device.accessnr = device_data['accessnr']
            device.manufacturer = device_data['manufacturer']
            device.save()

        message = Message.objects.create(device=device)

        for value in values_data:
            Value.objects.create(message=message, **value)

        return message

    class Meta:
        model = Message
        fields = [
            'data', 'device'
        ]

    def to_representation(self, instance):
        representation = OrderedDict()

        values_data = []
        for value in instance.data.order_by('storagenr').iterator():
            value_serializer = ValueSerializer(instance=value)
            values_data.append(value_serializer.data)

        representation['data'] = values_data
        representation['device'] = {
            'type': instance.device.device_type,
            'status': instance.device.status,
            'identnr': instance.device.identnr,
            'version': instance.device.version,
            'accessnr': instance.device.accessnr,
            'manufacturer': instance.device.manufacturer
        }

        return representation


class DeviceLatestTelemetryCVSSerializer(serializers.ModelSerializer):
    date_and_time_of_message = serializers.CharField(label="Date and Time of Message", max_length=50)
    device_id = serializers.IntegerField(label="Device ID")
    device_manufacturer = serializers.IntegerField(label="Device Manufacturer")
    device_type = serializers.IntegerField(label="Device Type")
    device_version = serializers.IntegerField(label="Device Version")
    dimension_of_measurement = serializers.IntegerField(label="Dimension of Measurement")
    value_of_newest_measurement = serializers.IntegerField(label="Value of Newest Measurement")
    value_of_measurement_in_due_date = serializers.IntegerField(label="Value of Measurement In Due Date")
    date_of_due_date = serializers.CharField(label="Date of the Due Date", max_length=50)

    class Meta:
        model = Device
        fields = [
            'date_and_time_of_message', 'device_id', 'device_manufacturer', 'device_type', 'device_version',
            'dimension_of_measurement', 'value_of_newest_measurement', 'value_of_measurement_in_due_date',
            'date_of_due_date'
        ]

    def to_representation(self, instance):
        data = OrderedDict()
        msg, latest_val, date = instance.get_latest_device_message_and_date()
        due_val, due_date = instance.get_latest_message_due_date_and_due_date_measurement()
        data['date_and_time_of_message'] = date.strftime("%d %B, %Y %H:%M:%S")
        data['device_id'] = instance.identnr
        data['device_manufacturer'] = instance.manufacturer
        data['device_type'] = instance.device_type
        data['device_version'] = instance.version
        data['dimension_of_measurement'] = due_val.dimension
        data['value_of_newest_measurement'] = instance.get_latest_value()
        data['value_of_measurement_in_due_date'] = due_val
        data['date_of_due_date'] = due_date.strftime("%d %B, %Y")

        return data
