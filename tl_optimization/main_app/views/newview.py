# Django requirements ..............
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.urls import reverse
from django.core.paginator import Paginator

# Views requirements .........
from ..forms import *
from ..models import *

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
    if Road.objects.filter(intersection_in=intersection_id).exists():
        road_entries_for_intersection_in = Road.objects.filter(intersection_in=intersection_id)
    else:
        road_entries_for_intersection_in = []

    if Road.objects.filter(intersection_out=intersection_id).exists():
        road_entries_for_intersection_out = Road.objects.filter(intersection_out=intersection_id)
    else:
        road_entries_for_intersection_out = []
    
    # Prepare the optimizer ------------------------------------------------

    # Data passed to the User Interface ------------------------------------
    data_input = {
        #'current_intersection': intersection_id,
        'page_obj': page_obj ,
        'intersection_info': intersection_info,
        'intersection_form': intersection_form ,
        'road_list_in': road_entries_for_intersection_in,
        'road_list_out': road_entries_for_intersection_out,
        'road_form': road_form
    }
    return render(request, 'main_app/view_home.html', data_input )

def intersection_View(request):
    return render(request, 'main_app/view_home.html')
# .....................................................................................................................
def create_intersection(request):
    if request.method == 'POST':
        #perform required operations
        pass
    return HttpResponseRedirect(reverse('home', args=(network_id, intersection_id ))) 

def delete_intersection(request):

    return HttpResponseRedirect(reverse('home', args=(network_id, intersection_id ))) 


# ...................................................................................................................
def add_road(request):
    if request.method == 'POST':
        #perform required operations
        pass
    return HttpResponseRedirect(reverse('home', args=(network_id, intersection_id ))) 

def update_road(request):
    if request.method == 'POST':
        #perform required operations
        pass
    return HttpResponseRedirect(reverse('home', args=(network_id, intersection_id ))) 

def delete_road(request, road_id):
    
    return HttpResponseRedirect(reverse('home', args=(network_id, intersection_id ))) 