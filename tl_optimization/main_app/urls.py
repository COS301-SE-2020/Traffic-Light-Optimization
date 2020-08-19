from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    #path('', views.index, name='index'),
    path('home/', views.home_, name='home_'),
    path('home/<int:intersection_id>/', views.home, name='home'),

    # Old - paths for old view
    path('roadvisual/', views.visualization, name='visualization'),
    path('network/', views.main_controller, name='all_networks'),
    path('network/<int:network_id>/', views.road_network_controller, name='road_network'),
    path('network/<int:network_id>/<int:intersection_id>/', views.intersection_controller, name='intersection'),
    path('network/<int:network_id>/<int:intersection_id>/<int:trafficlight_id>', views.trafficlight_controller, name='trafficlight'),

    path('network/<int:network_id>/<int:road_id>/', views.road_controller, name='road'),
    
    path('', views.upload, name='index'),
    path('simulation/', views.simulation, name='simulation'),

    # New - CRUD Operations
    path('intersection/', views.create_intersection, name="create_intersection" ),
    path('intersection/<int:intersection_id>/', views.delete_intersection, name="delete_intersection" ),

    path('road/<int:intersection_id>/', views.add_road, name="add_road" ),
    path('road/<int:road_id>/', views.delete_road, name="delete_road" ),
    
]

urlpatterns += staticfiles_urlpatterns()
