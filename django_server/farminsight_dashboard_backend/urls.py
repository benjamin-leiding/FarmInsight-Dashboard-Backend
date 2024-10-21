from django.urls import path

from .views import userprofile


urlpatterns = [
    path('userprofiles', userprofile, name='userprofiles'),
]


