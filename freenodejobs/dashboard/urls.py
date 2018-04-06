from django.urls import path

from . import views

app_name = 'superuser'

urlpatterns = (
    path('dashboard', views.view,
         name='view'),
)
