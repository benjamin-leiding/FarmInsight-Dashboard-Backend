from django.urls import path

from .views import get_userprofile, post_organization, post_fpf, get_own_organizations, MeasurementView, get_fpf_data, get_sensor_data


urlpatterns = [
    path('userprofiles', get_userprofile, name='get_userprofile'),
    path('organizations', post_organization, name='post_organization'),
    path('organizations/own', get_own_organizations, name='get_own_organizations'),
    path('fpfs', post_fpf, name='post_fpf'),
    path('fpfs/<str:fpf_id>/data', get_fpf_data, name='get_fpf_data'),
    path('sensors/<str:sensor_id>/measurements', get_sensor_data, name='get_sensor_data'),
    path('measurements/<str:sensor_id>', MeasurementView.as_view(), name='sensor-measurements')
]
