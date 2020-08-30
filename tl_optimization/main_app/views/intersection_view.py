# Django requirements ..............
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.urls import reverse
from django.core.paginator import Paginator

# External libraries .................
import pandas as pd
from plotly.offline import plot
from plotly.graph_objs import Scatter
from plotly.graph_objs import Bar 
import plotly.express as px

# Import optimizer module ............
from ..optimizer.time_series_forecast import Time_Series_Forecast
from ..optimizer.intersection_optimizer import *

# Views requirements .................
from ..forms import *
from ..models import *


    
# Create Intersection ..............................................................................................
def create_intersection(request):
    if request.method == 'POST':
        #perform required operations
        form_intersection = IntersectionForm(request.POST)
        if form_intersection.is_valid():
            new_intersection = form_intersection.save()
            new_intersection.network_id = get_object_or_404( Network, pk=1)
            new_intersection.save()
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
        data_file = request.FILES['historic_data']
        # Open data in pandas 
        df = pd.read_csv(data_file, header=None)
        headers = df[0]

        # Get roads to validate data 
        roads = read_road( intersection_id )
        roads_in = roads.roads_in
        # Validate headers
        if len(roads_in) > 1 :
            csv_road_names = headers[1:]
            count = 0
            for road in roads_in:
                if road.road_name in csv_road_names:
                    count = count + 1
            if( len(roads_in) == count ):
                intersection = get_object_or_404( Intersection, pk=intersection_id)
                intersection.upload_historic_data( data_file )
                intersection.train_model()
                intersection.forecast_traffic()
                intersection.optimize_traffic_lights()
        # Error 

    return HttpResponseRedirect(reverse('home', args=(intersection_id, ))) 
   
# Forecast the uploaded data .......................................................................................
def forecast_intersection( date):
    tsf_services = Time_Series_Forecast()
    data = tsf_services.prepare_data()
    tsf_services.forecast_model()
    results = tsf_services.prediction()
    return data , results


# Calculate the time for each day ...................................................................................
def optimize_intersection( request , intersection_id):
    return HttpResponseRedirect(reverse('home', args=(intersection_id, )))



    