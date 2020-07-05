import uuid
from collections import Counter
from datetime import datetime

from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """abstract base model to be inherited by other application models"""

    class Meta:
        abstract = True

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.is_deleted = True
        self.save()


class Device(BaseModel):
    """Device model"""
    device_type = models.PositiveIntegerField(null=True, blank=True)
    status = models.PositiveIntegerField(default=0)
    identnr = models.PositiveIntegerField(db_index=True)
    version = models.PositiveIntegerField(default=0)
    accessnr = models.PositiveIntegerField(default=0)
    manufacturer = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['uuid', 'identnr']
        verbose_name = 'Device'
        verbose_name_plural = 'Devicies'

    def get_latest_device_message_and_date(self):
        """ get_latest_device_message_and_date
            - returns all messages related to a device
            - compares values of the messages' data who's dimensions are exactly "Time Point (time & date)"
              which are representing latest date of measurement

            :return tuple(message: message, value: int, date: datetime)
             message: latest message
             value: value for the latest measurement
             date: date for the latest measurement
        """

        if self.messages is not None and self.messages.count() > 0:
            msgs = list(self.messages.filter(data__dimension__exact='Time Point (time & date)')
                        .values('uuid', 'data__storagenr', 'data__value').all())
            latest_msg = max(msgs, key=lambda m: datetime.strptime(m['data__value'], "%Y-%m-%dT%H:%M:%S.000000"))
            message = Message.objects.get(uuid=latest_msg['uuid'])
            latest_value = message.data.filter(storagenr=latest_msg['data__storagenr'],
                                               dimension__exact=message.get_dimension()) \
                .values_list('value').first()[0]
            return message, latest_value, datetime.strptime(latest_msg['data__value'], "%Y-%m-%dT%H:%M:%S.000000")
        return None

    def get_latest_message_due_date_and_due_date_measurement(self):
        """ get_latest_message_due_date_and_due_date_measurement
            - return the latest message.
            - get all values related to the message whose dimensions are exactly "Time Point (date)".
            - get the due date by comparing it the date of the latest measurement and
              returning the earliest from it.

          :return tuple(due_value: int, due_date: datetime)
            value: value for measurement at due date
            date: date of the due date
        """

        n = None if self.get_latest_device_message_and_date() is None \
            else self.get_latest_device_message_and_date()
        if n is not None:
            message, latest_value, latest_date = n
            values = list(message.data.filter(dimension__exact='Time Point (date)').values('storagenr', 'value').all())
            due_data = max(values, key=lambda v: datetime.strptime(v['value'], "%Y-%m-%dT%H:%M:%S.000000"))
            due_value = message.data.filter(storagenr=due_data['storagenr'],
                                            dimension__exact=message.get_dimension()).values_list('value').first()[0]
            due_date = datetime.strptime(due_data['value'], "%Y-%m-%dT%H:%M:%S.000000")
            return due_value, due_date
        return n

    def __str__(self):
        return str(self.identnr)


class Message(BaseModel):
    """Message model
        This should receive the payload from the gateway contain device information and
        it's telemetry
    """
    # many messages are related one device
    device = models.ForeignKey("telemetry.Device", on_delete=models.CASCADE, related_name='messages')

    class Meta:
        ordering = ['uuid']
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def get_dimension(self):
        """get_dimension
            iterates through a messages data set and returns the dimensions that appears the most as the dimension
            to this device
            :return dimension: str
        """
        counter = Counter()
        for value in self.data.iterator():
            counter[value.dimension] += 1

        return max(counter)

    def __str__(self):
        return str(self.device)


class Value(BaseModel):
    """Value model"""
    # many values are related one message
    message = models.ForeignKey("telemetry.Message", on_delete=models.CASCADE, related_name='data')
    value = models.CharField(max_length=50)
    tariff = models.PositiveIntegerField()
    subunit = models.PositiveIntegerField()
    dimension = models.CharField(max_length=50, db_index=True)
    storagenr = models.PositiveIntegerField(db_index=True)

    class Meta:
        ordering = ['uuid']
        verbose_name = 'Value'
        verbose_name_plural = 'Values'

    def __str__(self):
        return str(self.value)
