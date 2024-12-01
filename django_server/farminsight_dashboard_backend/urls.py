from django.conf.urls.static import static
from django.urls import path

from django_server import settings
from farminsight_dashboard_backend.views import (
    UserprofileView,
    get_userprofile,
    get_own_organizations,
    MeasurementView,
    post_organization,
    get_fpf_data,
    get_sensor_data,
    get_organization,
    post_growing_cycle,
    put_growing_cycle,
    MembershipView,
    SensorView,
    get_fpf_sensor_types,
    FpfView,
    post_fpf_api_key,
    post_camera,
    CameraView,
    get_camera_images
)

urlpatterns = [
    path('userprofiles', get_userprofile, name='get_userprofile'),
    path('userprofiles/<str:identifier>', UserprofileView.as_view(), name='userprofile_operations'),
    path('organizations/own', get_own_organizations, name='get_own_organizations'),
    path('organizations', post_organization, name='post_organization'),
    path('fpfs', FpfView.as_view(), name='post_fpf'),
    path('fpfs/<str:fpf_id>', FpfView.as_view(), name='fpf_operations'),
    path('fpfs/<str:fpf_id>/apiKey', post_fpf_api_key, name='post_fpf_api_key'),
    path('fpfs/<str:fpf_id>/data', get_fpf_data, name='get_fpf_data'),
    path('organizations/<str:organization_id>', get_organization, name='get_organization'),
    path('memberships', MembershipView.as_view(), name='post_membership'),
    path('memberships/<str:membership_id>', MembershipView.as_view(), name='membership_operations'),
    path('cameras/<str:camera_id>/images', get_camera_images, name='get_camera_snapshots'),
    path('sensors/<str:sensor_id>/measurements', get_sensor_data, name='get_sensor_data'),
    path('sensors', SensorView.as_view(), name='post_sensor'),
    path('sensors/<str:sensor_id>', SensorView.as_view(), name='sensor_operations'),
    path('sensors/types/available/<str:fpf_id>', get_fpf_sensor_types, name='get_fpf_sensor_types'),
    path('measurements/<str:sensor_id>', MeasurementView.as_view(), name='sensor-measurements'),
    path('growing-cycles', post_growing_cycle, name='post_growing_cycle'),
    path('growing-cycles/<str:growing_cycle_id>', put_growing_cycle, name='put_growing_cycle'),
    path('cameras', post_camera, name='post_camera'),
    path('cameras/<str:camera_id>', CameraView.as_view(), name='camera_operations'),
]



