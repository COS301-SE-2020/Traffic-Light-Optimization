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

def home(request):
    # Prepare the intersections list --------------------------------------
    intersection_list = Intersection.objects.get_queryset().order_by('id')
    paginator = Paginator(intersection_list, 5) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    intersection_form = IntersectionForm()

    # Prepare data for the simulation --------------------------------------

    # Prepare the optimizer ------------------------------------------------

    # Data passed to the User Interface ------------------------------------
    data_input = {
        #'current_intersection': intersection_id,
        'page_obj': page_obj ,
        'intersection_form': intersection_form
    }
    return render(request, 'main_app/home.html', data_input )

def intersection_View(request):
    return render(request, 'main_app/home.html')