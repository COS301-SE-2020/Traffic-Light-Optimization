#from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.urls import reverse

from .forms import *
from .models import *

# 1. Create views //////////////////////////////////////////////////////////////////////////////////////////////////
'''

'''
def index(request):
    return HttpResponse("Hello, world. You're at the main_app's index.")

def home(request):
    return render(request, 'main_app/home.html')


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
def get_simulator(request):
    return render( request, 'main_app/roadnetwork.html')
