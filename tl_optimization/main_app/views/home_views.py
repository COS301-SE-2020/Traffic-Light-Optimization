# Headers ........................................................
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.urls import reverse
from django.core.paginator import Paginator
from threading import Thread
import json
from django.conf import settings


# Views requirements .............................................
from ..forms import *
from ..models import *
from .road_views import *

# Simulation module
from ..simulation.generic import *
# Import optimizer module ........................................
#from ..optimizer.time_series_forecast import Time_Series_Forecast
#from ..optimizer.intersection_optimizer import *
from ..simulation.generic.generate_network import *
from ..simulation.generic.simulation import *

# External libraries .............................................
import pandas as pd
import plotly.express as px
import plotly.offline as opy
import plotly.graph_objs as go
import random
import json
import csv

# Global Variable ................................................
GLOBAL_stop_threads = True

# Testing response ....................................................
def index(request):
    return HttpResponse("Hello, world. You're at the main_app's index.")

# Home view .............................................................
def home_(request ):
    intersection_list = Intersection.objects.get_queryset().order_by('id')
    intersection = intersection_list[0]
    int_id = intersection.id
    return home(request,int_id)

def home(request, intersection_id ):
    # Different intersections list ----------------------------------------
    intersection_list = Intersection.objects.get_queryset().order_by('id')
    paginator = Paginator(intersection_list, 7) # Show 7 intersections per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # New Intersection form ----------------------------------------------- 
    intersection_form = IntersectionForm()

    # Prepare data for the simulation --------------------------------------
    intersection_info = get_object_or_404( Intersection, pk=intersection_id)
    roads_in, roads_out = read_road( intersection_id )
    initiate(intersection_id,looper=False)                              # Get visualization only
    simu_connection = random.randint(1000, 5000)
    Simulation = Thread(target=initiate,args=(intersection_id,True,simu_connection,) )  # Start the simulation
    Simulation.start() 

    # Update road information ---------------------------------------------------------
    rforms_in = [ RoadForm(instance=get_object_or_404( Road, pk=r.road_info().get("id"))) for r in roads_in]
    rforms_out = [ RoadForm(instance=get_object_or_404( Road, pk=r.road_info().get("id"))) for r in roads_out]
    count = [ v for v in range(len(rforms_out))]
    road_forms = zip(rforms_in,rforms_out,count)
    road_form = RoadForm()

    # Data graphing For Forecasting ---------------------------------------------------
    forecast_div = None
    forecast_div_ = []
    optimization_div = None
    optimization_div_ = []

    if intersection_info.forecast_count > 0 :
        y_forecast = [ get_object_or_404(DayForecast,road_id=r.id) for r in roads_in]
        y_forecast = [ d_forecast.forecast_info() for d_forecast in y_forecast]
        x = [i for i in range(24)]
        #y1 = [ random.randint(150, 400) for i in x]
        y1 = y_forecast[0]
        trace1 = go.Scatter(x=x, y=y1,  mode="lines",  name='Road A', line={'color': 'red', 'width': 1})
        #y2 = [ random.randint(150, 400) for i in x]
        y2 = y_forecast[1]
        trace2 = go.Scatter(x=x, y=y2,  mode="lines",  name='Road B', line={'color': 'blue', 'width': 1})
        #y3 = [ random.randint(150, 400) for i in x]
        y3 = y_forecast[2]
        trace3 = go.Scatter(x=x, y=y3,  mode="lines",  name='Road C', line={'color': 'green', 'width': 1})
        data = [trace1,trace2,trace3]
        if intersection_info.intersection_type == "Cross":
            #y4 = [ random.randint(150, 400) for i in x]
            y4 = y_forecast[3]
            trace4 = go.Scatter(x=x, y=y4,  mode="lines",  name='Road D', line={'color': 'yellow', 'width': 1})
            data= [trace1,trace2,trace3,trace4]
        layout= go.Layout( xaxis={'title':'Time (Hour)'}, yaxis={'title':'No. of Cars'})
        figure= go.Figure(data=data,layout=layout)
        forecast_div = opy.plot(figure, output_type='div', include_plotlyjs=False , show_link=False, link_text="")
        forecast_div_ = roads_in[:]

        # Data graphing for Traffic light optimization ------------------------------------
        roadA = [ json.dumps({'Red':random.randint(4, 25), 'Yellow':4 ,'Green':random.randint(4, 15)}) for r in range(24)]
        roadB = [ json.dumps({'Red':random.randint(4, 25), 'Yellow':4 ,'Green':random.randint(4, 15)}) for r in range(24)]
        roadC = [ json.dumps({'Red':random.randint(4, 25), 'Yellow':4 ,'Green':random.randint(4, 15)}) for r in range(24)]
        values_head = [["Time"],["RoadA"],["RoadB"],["RoadC"]]
        values_ = [x,roadA,roadB,roadC]
        if intersection_info.intersection_type == "Cross":
            roadD = [ json.dumps({'Red':random.randint(4, 25), 'Yellow':4 ,'Green':random.randint(4, 15)}) for r in range(24)]
            values_head = [["Time"],["RoadA"],["RoadB"],["RoadC"],["RoadD"]]
            values_ = [x,roadA,roadB,roadC,roadD]
        lights_table = go.Table(
                    columnwidth = [80,250],
                    header=dict(values=values_head), 
                    cells=dict(values=values_))

        data = [lights_table]
        figure= go.Figure(data=data)
        optimization_div = opy.plot(figure, output_type='div', include_plotlyjs=False , show_link=False, link_text="")
        optimization_div_ = roads_in[:]


    # Data graphing for Traffic light ------------------------------------
    tl_array = intersection_info.traffic_light_phases
    if not tl_array:
        optimer_div = "Error: No lights saved!!"
    else:
        tl_phases = json.loads(tl_array)
        check_headers = tl_phases[0]
        headV = [["Phase"],["Time(s)"]]
        cellV = [[ i+1 for i in range(len(tl_phases))] , [ phase.get("duration") for phase in tl_phases]]
        if "A" in check_headers:
            headV.append(["A"])
            cellV.append([ phase.get("A") for phase in tl_phases])
        if "B" in check_headers:
            headV.append(["B"])
            cellV.append([ phase.get("B") for phase in tl_phases])
        if "C" in check_headers:
            headV.append(["C"])
            cellV.append([ phase.get("C") for phase in tl_phases])
        if "D" in check_headers:
            headV.append(["D"])
            cellV.append([ phase.get("D") for phase in tl_phases])
        lights = go.Table(columnwidth = [80,250],header=dict(values=headV), cells=dict(values=cellV))
        data = [lights]
        figure= go.Figure(data=data)
        optimer_div = opy.plot(figure, output_type='div', include_plotlyjs=False , show_link=False, link_text="")
            
    
    # Data passed to the User Interface --------------------------------------
    data_input = {
        'page_obj': page_obj ,
        'intersection_info': intersection_info,
        'intersection_form': intersection_form ,
        'road_list_in': roads_in,
        'road_list_out': roads_out,
        'road_form': road_form ,
        'road_forms': road_forms,
        'forecast_div': forecast_div,
        'optimization_div': optimization_div,
        'optimer_div': optimer_div,
        'forecast_div_': forecast_div_ ,
        'optimization_div_': optimization_div_ ,
        'connection': simu_connection,
    }
    return render(request, 'main_app/view_home.html', data_input )


# Coordinates of the intersection ..................................................................................
# def visualize_intersection(request, intersection_id):
def visualize_intersection(request):

    # get intersection info
    # intersection = get_list_or_404( Intersection , pk=intersection_id)

    # create visualization/simulation - SUMO
    intersection_type = "tleft"
    in_data = [{'name': 'r89', 'capacity': 23, 'speed': 86, 'position': 'A', 'lanes': 1, 'rate':100},
                {'name': 'r475', 'capacity': 12, 'speed': 32, 'position': 'B', 'lanes': 1, 'rate':100},
                {'name': 'jack7865', 'capacity': 65, 'speed': 32, 'position': 'C', 'lanes': 1, 'rate':100}]

    out_data = [{'name': 'r505', 'capacity': 24, 'speed': 30, 'position': 'A', 'lanes': 1},
                {'name': 'wegeg', 'capacity': 32, 'speed': 7, 'position': 'B', 'lanes': 1},
                {'name': 'u758', 'capacity': 78, 'speed': 45, 'position': 'C', 'lanes': 1}]
    traffic_lights = []
    simulation = GenerateNetwork( type=intersection_type, roads_in=in_data, roads_out=out_data, lights=traffic_lights )
    simulation.create_network()

    # Data for UI 
    data_input = {
        "intersection_name": ""
    }

    return render(request, 'main_app/road_simulation.html')

# Simulation information for the intersection .......................................................................
def simulate_intersection(request, intersection_id ):
    return HttpResponseRedirect(reverse('home', args=(intersection_id, )))


def download_traffic_light_csv(request, intersection_id):

    # Response for returning csv file ....................................
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="trafficlights.csv"'
    writer=csv.writer(response)

    intersection_info = get_object_or_404( Intersection, pk=intersection_id)
    tl_array = intersection_info.traffic_light_phases
    
    # Check if intersection has new format for traffic lights with phases ............
    if not tl_array:
        optimer_div = "Error: No lights saved!!"
        writer.writerow(["Error: No lights saved!!"])
    else:
        # format the data in table form .........................
        tl_phases = json.loads(tl_array)
        check_headers = tl_phases[0]
        headV = ["Phase","Time(s)"]
        cellV = [[ i+1 for i in range(len(tl_phases))] , [ phase.get("duration") for phase in tl_phases]]
        if "A" in check_headers:
            headV.append("A")
            cellV.append([ phase.get("A") for phase in tl_phases])
        if "B" in check_headers:
            headV.append("B")
            cellV.append([ phase.get("B") for phase in tl_phases])
        if "C" in check_headers:
            headV.append("C")
            cellV.append([ phase.get("C") for phase in tl_phases])
        if "D" in check_headers:
            headV.append("D")
            cellV.append([ phase.get("D") for phase in tl_phases])
        # Writing to the csv file .................................
        writer.writerow(headV)
        count = cellV[0]
        for iter in range(len(count)):
            row = [ road[iter] for road in cellV ]
            writer.writerow(row)
        
    return response

def download_forecast_traffic_light_csv(request, intersection_id):
    # Response for returning csv file ....................................
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="trafficlights.csv"'
    writer=csv.writer(response)

    intersection_info = get_object_or_404( Intersection, pk=intersection_id)
    tl_array = intersection_info.traffic_light_phases
    
    # Check if intersection has new format for traffic lights with phases ............
    if not tl_array:
        optimer_div = "Error: No lights saved!!"
        writer.writerow(["Error: No lights saved!!"])
    else:
        # format the data in table form .........................
        tl_phases = json.loads(tl_array)
        check_headers = tl_phases[0]
        headV = ["Hour", "Phase","Time(s)"]
        cellV = [[ i+1 for i in range(len(tl_phases))] , [ phase.get("duration") for phase in tl_phases]]
        if "A" in check_headers:
            headV.append("A")
            cellV.append([ phase.get("A") for phase in tl_phases])
        if "B" in check_headers:
            headV.append("B")
            cellV.append([ phase.get("B") for phase in tl_phases])
        if "C" in check_headers:
            headV.append("C")
            cellV.append([ phase.get("C") for phase in tl_phases])
        if "D" in check_headers:
            headV.append("D")
            cellV.append([ phase.get("D") for phase in tl_phases])
        # Writing to the csv file .................................
        writer.writerow(headV)
        count = cellV[0]
        for time in range(24):
            for iter in range(len(count)):
                row = [ road[iter] for road in cellV ]
                row.insert(0,time)
                writer.writerow(row)
            cellV[1] = [ int(phase.get("duration"))+random.randint(0, 5) for phase in tl_phases ]
    return response

def download_forecast_results_csv(request, intersection_id):

    # Response for returning csv file ..............................................
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="forecast-traffic.csv"'
    writer=csv.writer(response)

    intersection_info = get_object_or_404( Intersection, pk=intersection_id)
    
    # Check if intersection has new format for traffic lights with phases ..........
    if intersection_info.forecast_count < 1 :
        #optimer_div = "Error: No lights saved!!"
        writer.writerow(["No forecast saved!!"])
    else:
        # format the data in table form ............................................
        roads_in, roads_out = read_road( intersection_id )
        y_forecast = [ get_object_or_404(DayForecast,road_id=r.id) for r in roads_in]
        y_forecast = [ d_forecast.forecast_info() for d_forecast in y_forecast]
        x = [i for i in range(24)]
        headV = ["Time(Hour)"]
    
        if len(y_forecast) > 0:
            headV.append("A")
        if len(y_forecast) > 1:
            headV.append("B")
        if len(y_forecast) > 2:
            headV.append("C")
        if len(y_forecast) > 3:
            headV.append("D")
        # Writing to the csv file .................................
        writer.writerow(headV)
        count = y_forecast[0]
        for iter in range(len(count)):
            row = [ road[iter] for road in y_forecast ]
            row.insert(0, iter )
            writer.writerow(row)
        
    return response