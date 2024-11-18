from django.db.models import QuerySet, Q

from farminsight_dashboard_backend.exceptions import NotFoundException
from farminsight_dashboard_backend.models import Userprofile


def search_userprofiles(search_string) -> QuerySet[Userprofile]:
    return Userprofile.objects.filter(Q(name__contains=search_string) | Q(email__contains=search_string)).all()


def update_userprofile_name(userprofile_id, new_name):
    """
    Updates the name of the userprofile
    :param userprofile_id:
    :param new_name:
    :return:
    """
    try:
        user_profile = Userprofile.objects.get(id=userprofile_id)
        user_profile.name = new_name
        user_profile.save()
        return user_profile
    except Userprofile.DoesNotExist:
        raise NotFoundException(f'Userprofile {userprofile_id} not found.')
