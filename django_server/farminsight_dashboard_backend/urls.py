from django.urls import path

from .views import get_userprofile, post_organization, post_fpf, get_own_memberships

urlpatterns = [
    path('userprofiles', get_userprofile, name='get_userprofile'),
    path('organizations', post_organization, name='post_organization'),
    path('fpfs', post_fpf, name='post_fpf'),
    path('memberships/own', get_own_memberships, name='get_own_memberships'),
]


