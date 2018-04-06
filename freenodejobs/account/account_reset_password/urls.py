from django.urls import path

from . import views

app_name = 'account_reset_password'

urlpatterns = (
    path('reset-password', views.view,
         name='view'),
    path('reset-password/<token>', views.reset,
         name='reset'),
)
