# Generated by Django 3.0.8 on 2020-07-04 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telemetry', '0004_auto_20200704_0749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='accessnr',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='device',
            name='manufacturer',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='device',
            name='status',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='device',
            name='version',
            field=models.PositiveIntegerField(default=0),
        ),
    ]