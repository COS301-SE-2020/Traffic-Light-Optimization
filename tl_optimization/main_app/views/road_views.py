# Headers ................
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.urls import reverse
from django.core.paginator import Paginator


# Views requirements .........
from ..forms import *
from ..models import *

# Create Road .....................................................................................................................
def add_road(request, intersection_id):
    if request.method == 'POST':
        #perform required operations
        form_road = RoadForm(request.POST)
        
        position = request.POST.get('position')
        direction = request.POST.get('direction')
       
        if direction != None and form_road.is_valid():
            
            new_road = form_road.save()
            if direction == "in":
                new_road.intersection_in = get_object_or_404( Intersection, pk=intersection_id)
            else:
                new_road.intersection_out = get_object_or_404( Intersection, pk=intersection_id)
            if position != None :
                new_road.position = position
            new_road.save()
            return HttpResponseRedirect(reverse('home', args=(intersection_id, ))) 

    return HttpResponseRedirect(reverse('home', args=(intersection_id, ))) 

# Read Road ................................................................................................................
def read_road(request, intersection_id):

    if Road.objects.filter(intersection_in=intersection_id).exists():
        road_entries_for_intersection_in = Road.objects.filter(intersection_in=intersection_id)
    else:
        road_entries_for_intersection_in = []

    if Road.objects.filter(intersection_out=intersection_id).exists():
        road_entries_for_intersection_out = Road.objects.filter(intersection_out=intersection_id)
    else:
        road_entries_for_intersection_out = []
    
    info = {
        "roads_in": road_entries_for_intersection_in ,
        "roads_out": road_entries_for_intersection_out
    }
    return HttpResponse( info )


# Delete Road ...............................................................................................................
def update_delete_road(request, intersection_id, road_id):
    road = get_object_or_404( Road, pk=road_id)
    if request.method == 'POST':
        form_road = RoadForm(request.POST, instance=road)
        if form_road.is_valid():
            form_road.save()
            return HttpResponseRedirect(reverse('home', args=(intersection_id, )))
        # Write appropriate error message ...... 
        return HttpResponseRedirect(reverse('home', args=(intersection_id, )))
    road.delete()
    return HttpResponseRedirect(reverse('home', args=( intersection_id, ))) 