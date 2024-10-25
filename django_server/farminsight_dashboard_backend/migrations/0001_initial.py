# Generated by Django 5.1.2 on 2024-10-19 16:09

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FPF',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('isPublic', models.BooleanField(default=False)),
                ('sensorServiceIp', models.CharField(max_length=256)),
                ('cameraServiceIp', models.CharField(max_length=256)),
                ('address', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('isPublic', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Userprofile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('email', models.EmailField(max_length=254)),
                ('systemRole', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('location', models.CharField(max_length=256)),
                ('modelNr', models.CharField(max_length=256)),
                ('resolution', models.CharField(max_length=256)),
                ('isActive', models.BooleanField(default=False)),
                ('intervalSeconds', models.IntegerField()),
                ('FPF', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farminsight_dashboard_backend.fpf')),
            ],
        ),
        migrations.CreateModel(
            name='GrowingCycle',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('startDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('endDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('plants', models.CharField(max_length=256)),
                ('note', models.CharField(max_length=256)),
                ('FPF', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farminsight_dashboard_backend.fpf')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('measuredAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.ImageField(upload_to='images/')),
                ('camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farminsight_dashboard_backend.camera')),
            ],
        ),
        migrations.AddField(
            model_name='fpf',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farminsight_dashboard_backend.organization'),
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('location', models.CharField(max_length=256)),
                ('unit', models.CharField(max_length=256)),
                ('modelNr', models.CharField(max_length=256)),
                ('isActive', models.BooleanField(default=False)),
                ('intervalSeconds', models.IntegerField()),
                ('FPF', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farminsight_dashboard_backend.fpf')),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('membershipRole', models.CharField(max_length=256)),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farminsight_dashboard_backend.organization')),
                ('userprofile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farminsight_dashboard_backend.userprofile')),
            ],
        ),
    ]
