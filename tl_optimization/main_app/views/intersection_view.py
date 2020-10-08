# Django requirements ..............
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.urls import reverse
from django.core.paginator import Paginator
import json

# External libraries .................
import pandas as pd
from plotly.offline import plot
from plotly.graph_objs import Scatter
from plotly.graph_objs import Bar 
import plotly.express as px

# Import optimizer module ............
from ..optimizer.time_series_forecast import Time_Series_Forecast
#from ..optimizer.intersection_optimizer import *

# Views requirements .................
from ..forms import *
from ..models import *

from .road_views import *
from ..simulation.generic.generate_network import *
    
# Create Intersection ..............................................................................................
def create_intersection(request):
    if request.method == 'POST':
        #perform required operations
        form_intersection = IntersectionForm(request.POST)
        if form_intersection.is_valid():
            new_intersection = form_intersection.save()
            new_intersection.network_id = get_object_or_404( Network, pk=1)
            new_intersection.save()

            # Add default roads to this intersection
            dist, spd, lan = 40, 10, 1
            if new_intersection.intersection_type != "T-Up":
                r_in = Road.objects.create( 
                    intersection_in=new_intersection, road_name="inA",  position="A", road_distance=dist, average_speed=spd, num_lanes=lan ) 
                DayForecast.objects.create(road_id=r_in)
                Road.objects.create(
                    intersection_out=new_intersection, road_name="outA", position="A", road_distance=dist, average_speed=spd, num_lanes=lan )

            if new_intersection.intersection_type != "T-Right":   
                r_in = Road.objects.create( 
                    intersection_in=new_intersection , road_name="inB", position="B", road_distance=dist, average_speed=spd, num_lanes=lan )
                DayForecast.objects.create(road_id=r_in)
                Road.objects.create( 
                    intersection_out=new_intersection , road_name="outB", position="B", road_distance=dist, average_speed=spd, num_lanes=lan )
            
            if new_intersection.intersection_type != "T-Down":
                r_in = Road.objects.create( 
                    intersection_in=new_intersection, road_name="inC", position="C", road_distance=dist, average_speed=spd, num_lanes=lan )
                DayForecast.objects.create(road_id=r_in)
                Road.objects.create( 
                    intersection_out=new_intersection, road_name="outC", position="C", road_distance=dist, average_speed=spd, num_lanes=lan )

            if new_intersection.intersection_type != "T-Left":
                r_in = Road.objects.create( 
                    intersection_in=new_intersection, road_name="inD", position="D", road_distance=dist, average_speed=spd, num_lanes=lan )
                DayForecast.objects.create(road_id=r_in)
                Road.objects.create( 
                    intersection_out=new_intersection, road_name="outD", position="D", road_distance=dist, average_speed=spd, num_lanes=lan )

            # Create SUMO simulation files from default settings
            in_ , out_ = read_road( new_intersection.id )
            in_data = [ r.road_info() for r in in_ ]
            out_data = [ r.road_info() for r in out_ ]
            traffic_lights = []
            inter_object = get_object_or_404( Intersection, pk=new_intersection.id)
            simulation = GenerateNetwork( intersection_obj=inter_object, roads_in=in_data, roads_out=out_data, lights=traffic_lights )
            simulation.create_simulation_configurations()

            print("# Traffic Lights ----------------------------------------------------------------")
            tl_array = inter_object.traffic_light_phases
            print(tl_array)
            tl_phases = json.loads(tl_array)
            print(tl_phases)

            return HttpResponseRedirect(reverse('home', args=(new_intersection.id, ))) 
    return HttpResponseRedirect(reverse('home_'))


# Update OR Delete Intersection ...............................................................................................
def update_delete_intersection(request, intersection_id):
    intersection = get_object_or_404( Intersection, pk=intersection_id)
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('home', args=(intersection.id, ))) 
    
    intersection.delete()
    return HttpResponseRedirect(reverse('home_')) 


# Upload historic Data for forecasting future traffic ..............................................................
def upload_historic_data(request, intersection_id ):

    if request.method == 'POST':
        data_file = request.FILES.get('historic_data')
        if data_file is None:
            return HttpResponseRedirect(reverse('home', args=(intersection_id, ))) 
        # Open data in pandas 
        df = pd.read_csv(data_file)
        if not df.empty :
            flag = False
            intersection_info = get_object_or_404( Intersection, pk=intersection_id)
            for road in Road.objects.filter(intersection_in=intersection_id):
                if DayForecast.objects.filter(road_id=road).exists():
                    intersection_info.forecast_count += 1 
                    intersection_info.save()
                    flag = True
                    break
                else:
                    DayForecast.objects.create(road_id=road)
            if not flag:
                intersection_info.forecast_count += 1 
                intersection_info.save()

            # Get roads to validate data 
            roads_in, roads_out = read_road( intersection_id )
            # Validate headers
            print("Validate headers")
            if len(roads_in) > 1 :
                csv_road_names = list(df.columns)
                print(csv_road_names)
                count = 0
                for road in roads_in:
                    if road.position in csv_road_names:
                        count = count + 1
                print("......................................")
                if( len(roads_in) == count ):
                    print("Convert data to arrays")
                    # Convert data to arrays
                    #df = pd.read_csv(data_file)
                    traffic_list = []
                    for r in roads_in:
                        traffic_list.append( df[r.position].tolist() )
                    intersection = get_object_or_404( Intersection, pk=intersection_id)
                    print("......................................")
                    forecast_intersection(intersection.intersection_name, traffic_list )
                
                '''
                intersection.upload_historic_data( data_file )
                intersection.train_model()
                intersection.forecast_traffic()
                intersection.optimize_traffic_lights()'''
        # Error 

    return HttpResponseRedirect(reverse('home', args=(intersection_id, ))) 
   
# Forecast the uploaded data .......................................................................................
def forecast_intersection( name="", data=[]):
    print("forecast_intersection >>>>>>>>>>>>>>>>>>>>>>>>>>>")
    tsf_services = Time_Series_Forecast(intersection_name=name, data=data, n_steps_in=24, n_steps_out=24 )
    print("Time_Series_Forecast >>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    results = tsf_services.predict_traffic()
    print("tsf_services.predict_traffic() >>>>>>>>>>>>>>>>>>")
    #print(results)


# Calculate the time for each day ...................................................................................
def optimize_intersection( request , intersection_id):
    return HttpResponseRedirect(reverse('home', args=(intersection_id, )))

# update_simulation_info ...........................................................................................
def update_simulation_info( request , intersection_id):

    intersection = get_object_or_404( Intersection, pk=intersection_id)

    # Create the simulation files from updated Road settings
    in_data, out_data = read_road( intersection.id )
    in_data = [ r.road_info() for r in in_data ]
    out_data = [ r.road_info() for r in out_data ]
    traffic_lights = []
    simulation = GenerateNetwork( intersection_obj=intersection, roads_in=in_data, roads_out=out_data, lights=traffic_lights )
    simulation.create_simulation_configurations()
    #intersection.traffic_light_phases = json.dumps(traffic_lights_states)
    #intersection.save()

    return HttpResponseRedirect(reverse('home', args=( intersection_id, ))) 


# Get simulation extra information 
def get_simulation_infomation(request, intersection_id ):
    iteration = request.GET.get('iteration', None)
    data = simulation_info(intersection_id,iteration)
    return  JsonResponse(data)