from django.urls import path

from . import views

app_name = 'jobs_add_edit'

urlpatterns = (
    path('dashboard/jobs/add', views.view,
         name='add'),
    path('dashboard/jobs/<slug:slug>/edit', views.view,
         name='edit'),
    path('dashboard/jobs/<slug:slug>/remove', views.remove,
         name='remove'),
    path('dashboard/jobs/<slug:slug>/submit-for-approval',
         views.submit_for_approval,
         name='submit-for-approval'),
)
