from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    #path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('network/', views.main_controller, name='all_networks'),
    path('network/<int:network_id>/', views.road_network_controller, name='road_network'),
    path('network/<int:network_id>/<int:intersection_id>/', views.intersection_controller, name='intersection'),
    path('network/<int:network_id>/<int:intersection_id>/<int:trafficlight_id>', views.trafficlight_controller, name='trafficlight'),

    path('network/<int:network_id>/<int:road_id>/', views.road_controller, name='road'),
    
    path('', views.upload, name='index'),
    path('simulation/', views.simulation, name='simulation'),
    
]

urlpatterns += staticfiles_urlpatterns()
