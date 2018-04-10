from django.conf import settings
from django.urls import path, include
from django.views.static import serve


urlpatterns = (
    path('', include('freenodejobs.account.urls',
         namespace='account')),
    path('', include('freenodejobs.admin.urls',
         namespace='admin')),
    path('', include('freenodejobs.dashboard.urls',
         namespace='dashboard')),
    path('', include('freenodejobs.profile.urls',
         namespace='profile')),
    path('', include('freenodejobs.registration.urls',
         namespace='registration')),
    path('', include('freenodejobs.static.urls',
         namespace='static')),
    path('', include('freenodejobs.jobs.urls',
         namespace='jobs')),

    path('storage/<path:path>', serve, {
        'show_indexes': settings.DEBUG,
        'document_root': settings.MEDIA_ROOT,
    }),
)
