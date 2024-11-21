from django.urls import path

from farminsight_dashboard_backend.views import (
    UserprofileView,
    get_userprofile,
    get_own_organizations,
    MeasurementView,
    post_organization,
    get_fpf_data,
    get_sensor_data, get_organization
)
from farminsight_dashboard_backend.views.fpf_views import FpfView
from farminsight_dashboard_backend.views.membership_views import MembershipView
from farminsight_dashboard_backend.views.sensor_views import SensorView, get_fpf_sensor_types

urlpatterns = [
    path('userprofiles', get_userprofile, name='get_userprofile'),
    path('userprofiles/<str:identifier>', UserprofileView.as_view(), name='userprofile_operations'),
    path('organizations/own', get_own_organizations, name='get_own_organizations'),
    path('organizations', post_organization, name='post_organization'),
    path('fpfs', FpfView.as_view(), name='post_fpf'),
    path('fpfs/<str:fpf_id>', FpfView.as_view(), name='fpf_operations'),
    path('organizations/<str:organization_id>', get_organization, name='get_organization'),
    path('memberships', MembershipView.as_view(), name='post_membership'),
    path('memberships/<str:membership_id>', MembershipView.as_view(), name='membership_operations'),
    path('fpfs/<str:fpf_id>/data', get_fpf_data, name='get_fpf_data'),
    path('sensors/<str:sensor_id>/measurements', get_sensor_data, name='get_sensor_data'),
    path('sensors', SensorView.as_view(), name='post_sensor'),
    path('sensors/<str:sensor_id>', SensorView.as_view(), name='sensor_operations'),
    path('sensors/types/available/<str:fpf_id>', get_fpf_sensor_types, name='get_fpf_sensor_types'),
    path('measurements/<str:sensor_id>', MeasurementView.as_view(), name='sensor-measurements')
]
