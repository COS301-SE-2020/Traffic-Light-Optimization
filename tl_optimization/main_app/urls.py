from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.create, name='index'),
    path('data', views.upload, name='data'),
    path('simulation/', views.simulation, name='simulation'),
    path('home', views.home, name='home'),
]

urlpatterns += staticfiles_urlpatterns()