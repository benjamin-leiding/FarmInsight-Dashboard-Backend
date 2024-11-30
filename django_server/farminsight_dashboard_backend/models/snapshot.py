import uuid

from django.db import models
from farminsight_dashboard_backend.models import Camera, FPF


class Snapshot(models.Model):
    camera = models.ForeignKey(Camera, related_name='snapshots', on_delete=models.DO_NOTHING)
    file_name = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)