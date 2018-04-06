from django.urls import path

from . import views

app_name = 'account_two_factor_auth'

urlpatterns = (
    path(r'account/2fa', views.view,
         name='view'),
    path(r'account/2fa/enabled', views.enabled,
         name='enabled'),
    path(r'account/2fa/disable', views.disable,
         name='disable'),
    path(r'account/2fa/setup', views.SetupView.as_view(),
         name='setup'),
    path(r'account/2fa/qr-code', views.QRGeneratorView.as_view(),
         name='qr-code'),
)
