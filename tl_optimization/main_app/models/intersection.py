# Headers ..................................................
from django.db import models
from django.urls import reverse
from datetime import datetime


# Import other necesary methods ............................
from .network import Network


from ..optimizer.intersection_optimizer import *
from ..optimizer.time_series_forecast import *


# 2. Models the behavior of a single intersection within a road network ................................................
class Intersection(models.Model):
    network_id = models.ForeignKey(
        Network, 
        blank=False,
        null=True,
        on_delete=models.SET_NULL
    )

    intersection_name = models.CharField( max_length=50, unique=True )
    right_of_way = models.TextField( blank=True )
    configuration = models.TextField( blank=True )

    def get_absolute_url(self):
        return reverse('home', args=(self.id,))
    
    def __str__(self):
        return self.intersection_name

    def optimizer(self):
        pass
