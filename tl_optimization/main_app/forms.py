from django.forms import ModelForm
from django import forms
from .models import *

from django.forms import ModelChoiceField

class customModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.intersection_name

class NetworkForm(ModelForm):
    class Meta:
        model = Network
        fields = [ 'network_name' ]
        widgets = {
            'network_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class IntersectionForm(ModelForm):
    class Meta:
        model = Intersection
        #fields = ['intersection_name', 'right_of_way', 'configuration']
        fields = ['intersection_name']
        widgets = {
            'intersection_name': forms.TextInput(attrs={'class': 'form-control'}),
            #'right_of_way': forms.Textarea(attrs={'class': 'form-control'}),
            #'configuration': forms.Textarea(attrs={'class': 'form-control'}),
        }


class TrafficlightForm(ModelForm):
    class Meta:
        model = TrafficLight
        fields = ['road_id', 'timing_red', 'timing_yellow', 'timing_green']

# Road Forms .............................................
class RoadForm(ModelForm):
    class Meta:
        model = Road
        fields = ['intersection_in', 'intersection_out', 'road_name', 'road_distance', 'average_speed']
        
        widgets = {
            #'intersection_in': forms.TextInput(attrs={'class': 'form-control'}),
            #'intersection_out': forms.TextInput(attrs={'class': 'form-control'}),
            'road_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'road_distance': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'average_speed': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
        }
        '''
        intersection_in = customModelChoiceField( 
            queryset=Intersection.objects.all() , 
            empty_label="" , 
            required=False,
            widget=forms.Select(attrs={'class':'form-control form-control-sm'})
        )
        intersection_out = customModelChoiceField( 
            queryset=Intersection.objects.all() , 
            empty_label="" ,  
            required=False,
            widget=forms.Select(attrs={'class':'form-control form-control-sm'})
        )
        '''



