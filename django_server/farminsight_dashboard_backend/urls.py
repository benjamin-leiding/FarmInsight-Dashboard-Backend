from django.urls import path

from farminsight_dashboard_backend.views import (
    get_userprofile_by_search_string,
    get_own_organizations,
    post_membership,
    MeasurementView,
    get_userprofile,
    post_organization,
    post_fpf,
    get_fpf_data,
    get_sensor_data, get_organization
)


urlpatterns = [
    path('userprofiles', get_userprofile, name='get_userprofile'),
    path('userprofiles/<str:search_string>', get_userprofile_by_search_string, name='get_userprofile_by_search_string'),
    path('organizations', post_organization, name='post_organization'),
    path('organizations/<str:organization_identifier>', get_organization, name='get_organization'),
    path('memberships', post_membership, name='post_membership'),
    path('organizations/own', get_own_organizations, name='get_own_organizations'),
    path('fpfs', post_fpf, name='post_fpf'),
    path('fpfs/<str:fpf_id>/data', get_fpf_data, name='get_fpf_data'),
    path('sensors/<str:sensor_id>/measurements', get_sensor_data, name='get_sensor_data'),
    path('measurements/<str:sensor_id>', MeasurementView.as_view(), name='sensor-measurements')
]
