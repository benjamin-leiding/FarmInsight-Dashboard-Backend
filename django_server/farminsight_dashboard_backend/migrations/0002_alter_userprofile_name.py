# Generated by Django 5.1.2 on 2024-10-24 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farminsight_dashboard_backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]