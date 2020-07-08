#from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import *

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the main_app's index.")

def home(request):
    return render(request, 'main_app/home.html')


# The Road Networks
def get_all_networks(request):
    
    if request.method == 'POST':
        form = NetworkForm(request.POST)
        if form.is_valid():
           
            return HttpResponseRedirect('/thanks/')
    else:
        form = NetworkForm()

    return render(request, 'main_app/roadnetwork.html', {'form': form})

# Intersections in a network
def get_network(request):
    
    if request.method == 'POST':
        form = NetworkForm(request.POST)
        if form.is_valid():
           
            return HttpResponseRedirect('/thanks/')
    else:
        form = NetworkForm()

    return render(request, 'main_app/roadnetwork.html', {'form': form})

# Road to different intersections