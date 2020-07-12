from django.forms import ModelForm
from .models import *


class NetworkForm(ModelForm):
    class Meta:
        model = Network
        fields = [ 'network_name' ]


class IntersectionForm(ModelForm):
    class Meta:
        model = Intersection
        fields = ['intersection_name', 'right_of_way', 'configuration']


class TrafficlightForm(ModelForm):
    class Meta:
        model = TrafficLight
        fields = ['intersection', 'timing_red', 'timing_yellow', 'timing_green']


class RoadForm(ModelForm):
    class Meta:
        model = Road
        fields = ['intersection_in', 'intersection_out', 'road_name', 'road_distance', 'average_speed']


