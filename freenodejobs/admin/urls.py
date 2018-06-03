from django.urls import path, include

from . import views

app_name = 'admin'

urlpatterns = (
    path('', include('freenodejobs.admin.admin_users.urls',
         namespace='users')),

    path('admin', views.view,
         name='view'),
    path('admin/jobs/<slug:slug>/approve', views.approve,
         name='approve'),
    path('admin/jobs/<slug:slug>/reject', views.reject,
         name='reject'),
    path('admin/jobs/<slug:slug>/remove', views.remove,
         name='remove'),

    path('admin/<slug:state_slug>', views.view,
         name='view'),
)
