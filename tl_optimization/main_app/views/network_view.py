#from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.urls import reverse
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import InfluxDBClient
from numpy import random
import csv
import io
from django.http import HttpResponse

from ..forms import *
from ..models import *

# 1. Create views //////////////////////////////////////////////////////////////////////////////////////////////////
'''

'''
# Create your views here.

def upload(request):
    organisation_ = "cos301.alpha@gmail.com"
    token_ = "okx-Wk8zR33DYZxZP91T10ZTfUFmMz866DCKfE3Z8l5azgUT3QLIIdzk6rATGgCdAyuaAbWrReSi9KfchjW0kg=="
    bucket_ = "test Bucket"
    url_ = "https://eu-central-1-1.aws.cloud2.influxdata.com"

    client = InfluxDBClient(url=url_, token=token_, org=organisation_)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    if request.method == 'POST':
        uploaded_file = request.FILES['filename']
        if uploaded_file.name.endswith('.csv'):
            messages.error(request, 'Not a csv file')
            csv_data = uploaded_file.read().decode('UTF-8')
            io_data = io.StringIO(csv_data)

            next(io_data)
            status = ["red", "green", "orange"]
            tl_type = ["standard", "pedestrian", "turn"]
            car_capacity = [20, 25]
            for column in csv.reader(io_data, delimiter=',', quotechar="|"):
                random_index = random.randint(1)
                index = random.randint(2)
                num_cars = random.randint(20)
                json_body = [
                    {
                        "measurement": "traffic_lights",
                        "tags": {
                            "tl_id": column[0],
                            "tl_location": "Austin, Texas",
                            "tl_status": status[index],
                            "tl_type": tl_type[index],
                            "tl_name": column[8],
                            "tl_intersection": column[2],
                            "tl_operation_state": column[4],
                            "tl_operation_processed_time": column[5]
                        },
                        "fields": {
                            "car_capacity": car_capacity[random_index],
                            "num_lanes": 3,
                            "num_cars": num_cars
                        },
                        "time": None
                    }
                ]
                write_api.write(bucket=bucket_, org=organisation_, record=json_body)
    else:
        print("hello")
    return render(request, 'main_app/base.html')

def simulation(request):
    return render(request, 'main_app/simulation.html')

def index(request):
    return HttpResponse("Hello, world. You're at the main_app's index.")

def visualization(request):
    return render(request, 'main_app/view_simulation.html')


# 2. The Road Networks /////////////////////////////////////////////////////////////////////////////////////////////
'''
    Description: return all the networks in the database 
'''

def main_controller(request):
    
    if request.method == 'POST':
        network_form = NetworkForm(request.POST)
        if network_form.is_valid():
            # Saving the network and redirecting to the new network
            new_network = network_form.save()
            #URL = '/network/'+new_network.id+'/'
            return HttpResponseRedirect(reverse('road_network', args=(new_network.id,)))
    else:
        network_form = NetworkForm()

    if Network.objects.filter().exists():
        all_network_entries = Network.objects.filter()
    else:
        all_network_entries = []
    
    ui_data = {
        'network_list': all_network_entries ,
        'network_form': network_form
    }
    return render(request, 'main_app/all_networks.html', ui_data)

# 3. View relating to a network //////////////////////////////////////////////////////////////////////////////////////
''' 
    Description: 
        1. Return information about the specific network
        2. A template UI is called with the form parameters to add an intersection
'''
def road_network_controller(request, network_id):
    # 1. Data components ------------------------------------------------
    network_info = get_object_or_404( Network, pk=network_id )

    # 2. Handling Form ------------------------------------
    if request.method == 'POST':
        form_intersection = IntersectionForm(request.POST)
        if form_intersection.is_valid():
            new_intersection = form_intersection.save()
            new_intersection.network_id = network_info
            new_intersection.save()
            return HttpResponseRedirect(reverse('intersection', args=(network_id, new_intersection.id )))
    else:
        form_intersection = IntersectionForm()
        
    # 4. Preparing Data for User Intrerface ------------------------------
    if Intersection.objects.filter( network_id=network_id ).exists():
        intersection_entries_for_network = Intersection.objects.filter( network_id=network_id )
    else:
        intersection_entries_for_network = []
    
    # 4. Preparing Data for User Intrerface ------------------------------
    ui_data = {
        'network_info': network_info,
        'intersection_list': intersection_entries_for_network ,
        'intersection_form': form_intersection
    }
    return render(request, 'main_app/road_network.html', ui_data )

# 4. View relating to an intersection within a network ////////////////////////////////////////////////////////////////
def intersection_controller(request, network_id, intersection_id):
    # 1. Getting parents infomation ------------------------------------
    newtork_info = get_object_or_404( Network, pk=network_id )
    intersection_info = get_object_or_404( Intersection, pk=intersection_id)
    if Intersection.objects.filter( network_id=network_id ).exists():
        intersection_entries_for_network = Intersection.objects.filter( network_id=network_id )
    else:
        intersection_entries_for_network = []

    # 2. Handling forms for intersection -----------------------------
    if request.method == 'POST':
        form_road = RoadForm(request.POST)
        if form_road.is_valid():
            new_road = form_road.save()
            return HttpResponseRedirect(reverse('intersection', args=(network_id, intersection_id )))
        form_road.fields['intersection_in'] = customModelChoiceField( 
            intersection_entries_for_network , 
            empty_label="" , 
            required=False,
            widget=forms.Select(attrs={'class':'form-control'})
        )
        form_road.fields['intersection_out'] = customModelChoiceField( 
            intersection_entries_for_network , 
            empty_label="" ,
            required=False,
            widget=forms.Select(attrs={'class':'form-control'})
        )

    else:
    
        form_road = RoadForm()

        form_road.fields['intersection_in'] = customModelChoiceField( 
            intersection_entries_for_network , 
            empty_label="" , 
            required=False,
            widget=forms.Select(attrs={'class':'form-control'})
        )
        form_road.fields['intersection_out'] = customModelChoiceField( 
            intersection_entries_for_network , 
            empty_label="" , 
            required=False,
            widget=forms.Select(attrs={'class':'form-control'})
        )



    # 3. Getting information about this intersection i.e. checking the roads ------------------
    if Road.objects.filter(intersection_in=intersection_id).exists():
        road_entries_for_intersection_in = Road.objects.filter(intersection_in=intersection_id)
    else:
        road_entries_for_intersection_in = []

    if Road.objects.filter(intersection_out=intersection_id).exists():
        road_entries_for_intersection_out = Road.objects.filter(intersection_out=intersection_id)
    else:
        road_entries_for_intersection_out = []
    
    if TrafficLight.objects.filter( intersection_id=intersection_id ).exists():
        trafficlight_entries_for_intersection = TrafficLight.objects.filter( intersection_id=intersection_id )
    else:
        trafficlight_entries_for_intersection = []

    # 4. Preparing data to send to the User Interface -------------------
    ui_data = {
        'network_info': newtork_info ,
        'intersection_info': intersection_info ,
        'road_list_in': road_entries_for_intersection_in ,
        'road_list_out': road_entries_for_intersection_out ,
        'trafficlight_list': trafficlight_entries_for_intersection ,
        'road_form': form_road ,
        'len_road_list_in': len(road_entries_for_intersection_in) ,
        'len_road_list_out': len(road_entries_for_intersection_out) ,
        'max_roads': range( max( len(road_entries_for_intersection_in), len(road_entries_for_intersection_out)))
    }
    return render(request, 'main_app/intersection.html', ui_data)
    

# 4. View for Simulation of the traffic flow //////////////////////////////////////////////////////////////////////////


def road_controller(request, network_id):
    return render( request, 'main_app/roadview.html')

def trafficlight_controller( request, network_id, intersection_id ):
    return render( request, 'main_app/roadview.html')

# Network ------------------------------------------------------------------------------------------------
def update_network_controller(request, network_id):
    net_up = Network.objects.get(pk=network_id)
    if request.method == 'POST':
        form_road = RoadForm(request.POST)
        if form_road.is_valid():
            net_up.name = request.POST.get('name')
            net_up.save()
    else:
        return HttpResponseRedirect(reverse('road_network', args=(network_id, ))) 
    return HttpResponseRedirect(reverse('road_network', args=(network_id, ))) 

def delete_network_controller(request, network_id):
    net_del = Network.objects.get(pk=network_id)
    net_del.delete()
    return HttpResponseRedirect(reverse('all_network')) 
# Intersection -------------------------------------------------------------------------------------------------
def update_intersection_controller(request, network_id, intersection_id):
    return HttpResponseRedirect(reverse('intersection', args=(network_id, intersection_id ))) 

def delete_intersection_controller(request, network_id, intersection_id):
    inter_del = Intersection.objects.get(pk=intersection_id)
    inter_del.delete()
    return HttpResponseRedirect(reverse('road_network', args=(network_id, )))
# Road -------------------------------------------------------------------------------------------------
def update_road_controller(request, network_id, intersection_id, road_id):
    return HttpResponseRedirect(reverse('intersection', args=(network_id, intersection_id )))

def delete_road_controller(request, network_id, intersection_id, road_id):
    road_del = Intersection.objects.get(pk=road_id)
    road_del.delete()
    return HttpResponseRedirect(reverse('intersection', args=(network_id, intersection_id )))