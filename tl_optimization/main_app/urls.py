from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.upload, name='index'),
    path('simulation/', views.simulation, name='simulation'),
    path('home', views.home, name='home'),
]

urlpatterns += staticfiles_urlpatterns()