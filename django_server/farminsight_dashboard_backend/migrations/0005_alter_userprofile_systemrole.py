# Generated by Django 5.1.2 on 2024-10-29 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farminsight_dashboard_backend', '0004_alter_fpf_cameraserviceip_alter_fpf_sensorserviceip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='systemRole',
            field=models.CharField(default='user', max_length=256),
        ),
    ]
