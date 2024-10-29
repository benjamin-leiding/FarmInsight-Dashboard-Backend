import uuid
from django.db import models


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