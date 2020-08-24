# Django requirements ..............
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.urls import reverse
from django.core.paginator import Paginator
import pandas as pd

# Import optimizer module
from ..optimizer.time_series_forecast import Time_Series_Forecast
from ..optimizer.intersection_optimizer import *

# Views requirements .........
from ..forms import *
from ..models import *
from .road_views import *

def index(request):
    return HttpResponse("Hello, world. You're at the main_app's index.")

def home_(request ):
    return home(request,1)

def home(request, intersection_id ):
    # Prepare the intersections list --------------------------------------
    intersection_list = Intersection.objects.get_queryset().order_by('id')
    paginator = Paginator(intersection_list, 7) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    intersection_form = IntersectionForm()
    road_form = RoadForm()
    # Prepare data for the simulation --------------------------------------
    intersection_info = get_object_or_404( Intersection, pk=intersection_id)
    road_list = read_road( request, intersection_id )
    
    # Prepare the optimizer ------------------------------------------------
    ''''
    
    data , results = forecast_intersection()
    forecast = {
        'data': data,
        'results': results,
    }
    optimizer = {
        'data': [
            {"road_name": "r111" , "capacity": 45 , "rate": 0.6 , "out": "A" ,"direction": "left"} ,
            {"road_name": "r111" , "capacity": 45 , "rate": 0.2 , "out": "B" ,"direction": "right"} ,
            {"road_name": "r201" , "capacity": 45 , "rate": 0.3 , "out": "A" ,"direction": "left"} ,
            {"road_name": "r201" , "capacity": 45 , "rate": 0.3 , "out": "B" ,"direction": "right"}
        ],
        'results': traffic_light_optimizer(),
    }

    '''

    # Data passed to the User Interface ------------------------------------
    data_input = {
        #'current_intersection': intersection_id,
        'page_obj': page_obj ,
        'intersection_info': intersection_info,
        'intersection_form': intersection_form ,
        'road_list_in': road_entries_for_intersection_in,
        'road_list_out': road_entries_for_intersection_out,
        'road_form': road_form ,
        # optimizer information
        'forecast': forecast ,
        'optimizer': optimizer
    }
    return render(request, 'main_app/view_home.html', data_input )

    
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
    return home_(request )


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
        roads = read_road( request, intersection_id )
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
                optimize_traffic_lights()
        # Error 

    return HttpResponseRedirect(reverse('home', args=(intersection_id, ))) 
   
# Forecast the uploaded data .......................................................................................
def forecast_intersection( ):
    tsf_services = Time_Series_Forecast()
    data = tsf_services.prepare_data()
    tsf_services.forecast_model()
    results = tsf_services.prediction()
    return data , results


# Calculate the time for each day ...................................................................................
def optimize_intersection( request , intersection_id):
    return HttpResponseRedirect(reverse('home', args=(intersection_id, ))) 

# Coordinates of the intersection ..................................................................................
def visualize_intersection(request, intersection_id):
    return HttpResponseRedirect(reverse('home', args=(intersection_id, )))

# Simulation information for the intersection .......................................................................
def simulate_intersection(request, intersection_id ):
    return HttpResponseRedirect(reverse('home', args=(intersection_id, )))
    

    