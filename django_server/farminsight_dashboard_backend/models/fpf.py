import uuid
from django.db import models
from .organization import Organization


class FPF(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    isPublic = models.BooleanField(default=False)
    sensorServiceIp = models.GenericIPAddressField()
    cameraServiceIp = models.GenericIPAddressField()
    address = models.CharField(max_length=256)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
