# Generated by Django 3.0.8 on 2020-07-05 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telemetry', '0006_auto_20200705_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='value',
            name='dimension',
            field=models.CharField(db_index=True, max_length=50),
        ),
    ]
