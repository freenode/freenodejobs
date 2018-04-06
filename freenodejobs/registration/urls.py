from django.urls import path

from . import views

app_name = 'registration'

urlpatterns = (
    path(r'register', views.view,
         name='view'),
)
