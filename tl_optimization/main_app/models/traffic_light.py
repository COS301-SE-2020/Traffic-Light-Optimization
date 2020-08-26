# Headers ..................................................
from django.db import models
from django.urls import reverse
from datetime import datetime

# Import other necesary methods ............................
from .road import Road


# 3. Models a single traffic light within an intersection ...........................................................
class TrafficLight(models.Model):
    road_id = models.ForeignKey(
        Road, 
        blank=False, 
        null=True,
        on_delete=models.SET_NULL
    )
    date_time = models.DateTimeField(default=datetime.now, blank=True) 
    traffic_count = models.FloatField(default=0)

    timing_red = models.IntegerField(default=0)
    timing_yellow = models.IntegerField(default=0)
    timing_green = models.IntegerField(default=0)

    def get_absolute_url(self):
        road = Road.objects.get(pk=self.road_id)
        return reverse('trafficlight', args=(road.network_id.id, self.road_id.id, self.id))
    
    def __str__(self):
        return self.timing_green

    def light_info(self):
        light_info = {
            "red": self.timing_red,
            "orange": self.timing_yellow,
            "green": self.timing_green
        }
        return light_info