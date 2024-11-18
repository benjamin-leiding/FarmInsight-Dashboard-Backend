from django.urls import path

from farminsight_dashboard_backend.views import (
    UserprofileView,
    get_own_organizations,
    post_membership,
    MeasurementView,
    post_organization,
    post_fpf,
    get_fpf_data,
    get_sensor_data, get_organization
)




urlpatterns = [
    path('userprofiles',  UserprofileView.as_view(), name='get_userprofile'),
    path('userprofiles/<str:identifier>', UserprofileView.as_view(), name='userprofile_operations'),
    path('organizations/own', get_own_organizations, name='get_own_organizations'),
    path('organizations', post_organization, name='post_organization'),
    path('organizations/<str:organization_identifier>', get_organization, name='get_organization'),
    path('memberships', post_membership, name='post_membership'),
    path('fpfs', post_fpf, name='post_fpf'),
    path('fpfs/<str:fpf_id>/data', get_fpf_data, name='get_fpf_data'),
    path('sensors/<str:sensor_id>/measurements', get_sensor_data, name='get_sensor_data'),
    path('measurements/<str:sensor_id>', MeasurementView.as_view(), name='sensor-measurements')
]
