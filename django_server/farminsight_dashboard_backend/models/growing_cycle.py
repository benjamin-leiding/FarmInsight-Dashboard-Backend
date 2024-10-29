import uuid
from django.db import models
from django.utils import timezone
from .fpf import FPF


class GrowingCycle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    startDate = models.DateTimeField(default=timezone.now)
    endDate = models.DateTimeField(default=timezone.now)
    plants = models.CharField(max_length=256)
    note = models.CharField(max_length=256)
    FPF = models.ForeignKey(FPF, on_delete=models.CASCADE)
