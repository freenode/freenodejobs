from django.urls import path, include

from . import views

app_name = 'account'

urlpatterns = (
    path(r'', include('freenodejobs.account.account_reset_password.urls',
         namespace='reset-password')),
    path(r'', include('freenodejobs.account.account_two_factor_auth.urls',
         namespace='two-factor-auth')),

    path('login', views.LoginView.as_view(),
         name='login'),
    path('logout', views.logout,
         name='logout'),
    path('account/password', views.PasswordChangeView.as_view(),
         name='password-change'),
)
