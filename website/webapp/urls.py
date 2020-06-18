from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.upload, name='index'),
    path('simulation/', views.simulation, name='simulation'),
]

urlpatterns += staticfiles_urlpatterns()