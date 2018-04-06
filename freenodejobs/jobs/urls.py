from django.urls import path, re_path, include

from . import views
from .enums import JobTypeEnum

app_name = 'jobs'

urlpatterns = [
    path(r'', include('freenodejobs.jobs.jobs_add_edit.urls',
         namespace='add-edit')),

    path(r'all-jobs', views.view,
         name='view'),
    path(r'full-time-jobs', views.view,
         {'job_type': JobTypeEnum.FULL_TIME}, name='full-time'),
    path(r'part-time-jobs', views.view,
         {'job_type': JobTypeEnum.PART_TIME}, name='part-time'),
    path(r'contract-jobs', views.view,
         {'job_type': JobTypeEnum.CONTRACT}, name='contract'),

    re_path(r'^job/(?P<prefix>[-a-zA-Z0-9_]+)-(?P<slug>[a-z]{8})$', views.job,
         name='view'),
    re_path(r'^job/(?P<slug>[a-z]{8})$', views.job,
         name='view'),
]
