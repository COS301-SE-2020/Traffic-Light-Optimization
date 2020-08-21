# Headers ..................................................
from django.db import models
from django.urls import reverse
from datetime import datetime

# Import other necesary methods ............................
from .network import Network
from .intersection import Intersection
from .traffic_light import TrafficLight

# 4. Models traffic artefacts whose movements should be optimized .................................................
class Artefact(models.Model):
    padestrians = models.IntegerField(default=0)
    cars = models.IntegerField(default=0)
    taxi = models.IntegerField(default=0)
    bus = models.IntegerField(default=0)