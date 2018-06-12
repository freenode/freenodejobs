from django.urls import path

from . import views

app_name = 'admin_users'

urlpatterns = (
    path('admin/users', views.view,
         name='view'),
    path('admin/users/<int:user_id>', views.edit,
         name='edit'),
)
