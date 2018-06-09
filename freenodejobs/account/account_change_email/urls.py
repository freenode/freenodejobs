from django.urls import path

from . import views

app_name = 'account_change_email'

urlpatterns = (
    path('account/change-email', views.view,
         name='view'),
    path('account/change-email/validate/<token>', views.validate,
         name='validate'),
)
