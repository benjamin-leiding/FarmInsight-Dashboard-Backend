import uuid
from farminsight_dashboard_backend.utils import ListableEnum

from django.db import models
from django.contrib.auth.models import AbstractUser

class SystemRole(ListableEnum):
    SystemAdmin = 'sysAdmin'
    User = 'user'


class Userprofile(AbstractUser):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    #email = models.EmailField()
    systemRole = models.CharField(max_length=256, default=SystemRole.User.value)
'''
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = ["email"]

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True
'''