from django.contrib import admin

from farminsight_dashboard_backend.models import Userprofile, Membership, Organization

# Register your models here.
admin.site.register(Userprofile)
admin.site.register(Membership)
admin.site.register(Organization)