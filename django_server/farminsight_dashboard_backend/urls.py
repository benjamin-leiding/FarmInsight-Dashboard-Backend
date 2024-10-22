from django.urls import path

from .views import get_userprofile, post_organization, post_fpf

urlpatterns = [
    path('userprofiles', get_userprofile, name='get_userprofile'),
    path('organizations', post_organization, name='post_organization'),
    path('fpfs', post_fpf, name='post_fpf'),
]


