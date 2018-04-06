from django.conf import settings
from django.urls import path, include
from django.views.static import serve


urlpatterns = (
    path(r'', include('freenodejobs.account.urls',
         namespace='account')),
    path(r'', include('freenodejobs.admin.urls',
         namespace='admin')),
    path(r'', include('freenodejobs.dashboard.urls',
         namespace='dashboard')),
    path(r'', include('freenodejobs.profile.urls',
         namespace='profile')),
    path(r'', include('freenodejobs.registration.urls',
         namespace='registration')),
    path(r'', include('freenodejobs.static.urls',
         namespace='static')),
    path(r'', include('freenodejobs.jobs.urls',
         namespace='jobs')),

    path('storage/<path:path>', serve, {
        'show_indexes': settings.DEBUG,
        'document_root': settings.MEDIA_ROOT,
    }),
)
