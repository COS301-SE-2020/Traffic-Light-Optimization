from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

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
    path('simulation/', views.simulate_intersection, name='simulation'),

    # Intersection controllers
    path('intersection/', views.create_intersection, name="create_intersection" ),
    path('intersection/<int:intersection_id>/', views.update_delete_intersection, name="update_delete_intersection" ),
    path('intersection/<int:intersection_id>/upload', views.upload_historic_data, name="upload_historic_data"),
    path('intersection/<int:intersection_id>/trafficlights', views.download_traffic_light_csv, name="download_traffic_light_csv"),
    path('intersection/<int:intersection_id>/forecast', views.download_forecast_results_csv, name="download_forecast_results_csv"),
    path('intersection/<int:intersection_id>/forecasttrafficlights', views.download_forecast_traffic_light_csv, name="download_forecast_traffic_light_csv"),
    

    # Intersection Simulation 
    # path('intersection/<int:intersection_id>/visualization', views.visualize_intersection, name="visualize_intersection"),
    path('intersection/visualization', views.visualize_intersection, name="visualize_intersection"),
    path('intersection/<int:intersection_id>/simulation', views.simulate_intersection, name="simulate_intersection"),
    path('intersection/simulation/<int:intersection_id>/', views.update_simulation_info, name="update_simulation" ),

    # Road controllers 
    path('road/<int:intersection_id>/', views.add_road, name="add_road" ),
    path('intersection/road/<int:intersection_id>/', views.update_delete_road, name="update_delete_road" ),
    path('intersection/traffic/<int:intersection_id>/', views.update_road_rate, name="update_road_rate" ),


    
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
