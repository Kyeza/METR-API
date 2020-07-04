# Generated by Django 3.0.8 on 2020-07-04 06:59

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('telemetry', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
                'ordering': ['uuid'],
            },
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('value', models.CharField(max_length=50)),
                ('tariff', models.PositiveIntegerField()),
                ('subunit', models.PositiveIntegerField()),
                ('dimension', models.CharField(max_length=50)),
                ('storagenr', models.PositiveIntegerField(db_index=True)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data', to='telemetry.Message')),
            ],
            options={
                'verbose_name': 'Value',
                'verbose_name_plural': 'Values',
                'ordering': ['uuid'],
            },
        ),
        migrations.AlterModelOptions(
            name='device',
            options={'ordering': ['uuid', 'identnr'], 'verbose_name': 'Device', 'verbose_name_plural': 'Devicies'},
        ),
        migrations.AlterField(
            model_name='device',
            name='identnr',
            field=models.PositiveIntegerField(db_index=True, unique=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.DeleteModel(
            name='DeviceValue',
        ),
        migrations.AddField(
            model_name='message',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='telemetry.Device'),
        ),
    ]
