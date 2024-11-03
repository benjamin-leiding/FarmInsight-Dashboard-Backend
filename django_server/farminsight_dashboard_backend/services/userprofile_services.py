from django.db.models import QuerySet, Q
from farminsight_dashboard_backend.models import Userprofile


def search_userprofiles(search_string) -> QuerySet[Userprofile]:
    return Userprofile.objects.filter(Q(name__contains=search_string) | Q(email__contains=search_string)).all()
