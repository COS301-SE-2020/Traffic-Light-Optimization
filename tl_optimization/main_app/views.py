#from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import *
from .models import *

# 1. Create views ...........................................................................................
'''

'''
def index(request):
    return HttpResponse("Hello, world. You're at the main_app's index.")

def home(request):
    return render(request, 'main_app/home.html')


# 2. The Road Networks ........................................................................................
'''
    Description: return all the networks in the database 
'''

def get_all_networks(request):
    
    if request.method == 'POST':
        network_form = NetworkForm(request.POST)
        if network_form.is_valid():
            # Create a network form 
            return HttpResponseRedirect('/thanks/')
    else:
        network_form = NetworkForm()

    all_network_entries = Network.object.all()
    ui_data = {
        'network_entries': all_network_entries ,
        'network_form': network_form
    }
    return render(request, 'main_app/roadnetwork.html', ui_data)

# 3. View relating to a network ..................................................................................
''' 
    Description: 
        1. Return information about the specific network
        2. A template UI is called with the form parameters to add an intersection
'''
def get_network(request, network_id):
    
    if request.method == 'POST':
        form_intersection = IntersectionForm(request.POST)
        if form_intersection.is_valid():
           
            return HttpResponseRedirect('/thanks/')
    else:
        # 1. Form elements ..............
        form_intersection = IntersectionForm()
        
        
    # 2. Data components ............
    intersection_entries_for_network = Intersection.objects.get(fk=network_id)
    ui_data = {
        'network_entries': intersection_entries_for_network ,
        'network_form': form
    }
    return render(request, 'main_app/road_network.html', {'form': form, })

# 4. View relating to an intersection within a network .................................................................
def get_intersection(request, intersection_id):
    if request.method == 'POST':
        form = NetworkForm(request.POST)
        if form.is_valid():
            
            return HttpResponseRedirect('/thanks/')
    else:
        form_trafficlight = TrafficlightForm()
        form_road = RoadForm()

    road_entries_for_intersection = Road.object.all(intersection_in=intersection_id)
    ui_data = {
        'network_entries': road_entries_for_intersection ,
        'network_form': form
    }
    return render(request, 'main_app/intersection.html', ui_data)
    

# 4. View for Simulation of the traffic flow ..............................................................................
def get_simulator(request):
    return render( request, 'main_app/roadnetwork.html')
