import uuid
from django.db import models
from django.utils import timezone


class Userprofile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    email = models.EmailField()
    systemRole = models.CharField(max_length=256)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = ["email"]

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email, "systemRole": self.systemRole}

class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    isPublic = models.BooleanField(default=False)

class Membership(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    membershipRole = models.CharField(max_length=256)
    createdAt = models.DateTimeField(default=timezone.now)
    userprofile = models.ForeignKey(Userprofile, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

class FPF(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    isPublic = models.BooleanField(default=False)
    sensorServiceIp = models.GenericIPAddressField()
    cameraServiceIp = models.GenericIPAddressField()
    address = models.CharField(max_length=256)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

class Sensor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    location = models.CharField(max_length=256)
    unit = models.CharField(max_length=256)
    modelNr = models.CharField(max_length=256)
    isActive = models.BooleanField(default=False)
    intervalSeconds = models.IntegerField()
    FPF = models.ForeignKey(FPF, on_delete=models.CASCADE)

class Camera(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    location = models.CharField(max_length=256)
    modelNr = models.CharField(max_length=256)
    resolution = models.CharField(max_length=256)
    isActive = models.BooleanField(default=False)
    intervalSeconds = models.IntegerField()
    FPF = models.ForeignKey(FPF, on_delete=models.CASCADE)

class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    measuredAt = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='images/')
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)

class GrowingCycle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    startDate = models.DateTimeField(default=timezone.now)
    endDate = models.DateTimeField(default=timezone.now)
    plants = models.CharField(max_length=256)
    note = models.CharField(max_length=256)
    FPF = models.ForeignKey(FPF, on_delete=models.CASCADE)
