from django.urls import path

from . import views

app_name = 'registration'

urlpatterns = (
    path('register', views.view,
         name='view'),
    path('register/success', views.success,
         name='success'),
    path('register/validate/<token>', views.validate,
         name='validate'),
)
