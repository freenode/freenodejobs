from django.urls import path

from . import views

app_name = 'admin_users'

urlpatterns = (
    path('admin/users', views.view,
         name='view'),
    path('admin/users/<int:user_id>/set-admin', views.admin_toggle,
         {'enable': True}, name='set-admin'),
    path('admin/users/<int:user_id>/remove-admin', views.admin_toggle,
         {'enable': False}, name='remove-admin'),
)
