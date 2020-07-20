from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('network/', views.main_controller, name='all_networks'),
    path('network/<int:network_id>/', views.road_network_controller, name='road_network'),
    path('network/<int:network_id>/<int:intersection_id>/', views.intersection_controller, name='intersection')
]