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
    print("1. Attempt to add single road")
    if request.method == 'POST':
        # perform required operations
        form_road = RoadForm(request.POST)
        
        position = request.POST.get('position')
        direction = request.POST.get('direction')
       
        if direction != None and form_road.is_valid():
            print( "Yes: direction != None and form_road.is_valid()" )
            new_road = form_road.save()
            if direction == "in":
                new_road.intersection_in = get_object_or_404( Intersection, pk=intersection_id)
            else:
                new_road.intersection_out = get_object_or_404( Intersection, pk=intersection_id)
            if position != None :
                new_road.position = position
            new_road.save()
            print( new_road )
            return HttpResponseRedirect(reverse('home', args=(intersection_id, ))) 

    return HttpResponseRedirect(reverse('home', args=(intersection_id, ))) 

# Read Road ................................................................................................................
def read_road( intersection_id):

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
    return info.get("roads_in"), info.get("roads_out")


# Update/Delete Road ...............................................................................................................
def update_delete_road(request, intersection_id):
    
    if request.method == 'POST':
        print("1. [post works]")
        print( request.POST )
        count = 0
        roads_in, roads_out = read_road( intersection_id )
        for r_in, r_out in zip( roads_in, roads_out ):
            print( count )
            if str(count) == str(request.POST.get("position")):
                #print(request.POST.get("num_lanes"))
                lanes = request.POST.getlist("num_lanes")
                distance = request.POST.getlist("road_distance")
                speed = request.POST.getlist("average_speed")

                r_in.num_lanes = lanes[0]
                r_in.road_distance = distance[0]
                r_in.average_speed = speed[0]
                r_in.save()
                r_out.num_lanes = lanes[1]
                r_out.road_distance = distance[0]
                r_out.average_speed = speed[1]
                r_out.save()
                break
            count += 1

        return HttpResponseRedirect(reverse('update_simulation', args=(intersection_id, )))

    # Write appropriate error message ...... 
    #return HttpResponseRedirect(reverse('home', args=(intersection_id, )))
    return HttpResponseRedirect(reverse('home', args=( intersection_id, ))) 

# Update the cars per minute rate ...............................................................................................
def update_road_rate(request, intersection_id):
    if request.method == 'POST':
        roads_in, roads_out = read_road( intersection_id )
        for road in roads_in:
            road.rate = request.POST.get(str(road.road_name))
            road.save()
        return HttpResponseRedirect(reverse('update_simulation', args=(intersection_id, )))
    return HttpResponseRedirect(reverse('home', args=( intersection_id, ))) 