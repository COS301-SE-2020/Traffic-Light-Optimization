from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('networks', views.get_all_networks, name='all_networks'),
    path('networks/<int:network_id>/', views.get_network, name='road_network'),
    path('networks/<int:network_id>/<int:intersection_id>/', views.get_intersection, name='intersection')
]