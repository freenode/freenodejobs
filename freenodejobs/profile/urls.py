from django.urls import path

from . import views

app_name = 'profile'

urlpatterns = (
    path(r'profile', views.view,
         name='view'),
)
