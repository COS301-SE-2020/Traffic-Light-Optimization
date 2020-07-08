from django.db import models

# Create your models here.

# 1. Models an intersection into which different roads meet ................
class Network(models.Model):
    name = models.CharField( max_length=200 )

# 2. Models the behavior of a single intersection within a road network ....
class Intersection(models.Model):
    network = models.ForeignKey(
        Network, 
        blank=False, 
        null=True,
        on_delete=models.SET_NULL
    )
    name = models.CharField( max_length=200 )
    right_of_way = models.TextField( blank=True )
    configuration = models.TextField( blank=True )

# 3. Models a single traffic light within an intersection ...............
class TrafficLight(models.Model):
    intersection = models.ForeignKey(
        Intersection, 
        blank=False, 
        null=True,
        on_delete=models.SET_NULL
    )
    timing_red = models.IntegerField(default=0)
    timing_yellow = models.IntegerField(default=0)
    timing_green = models.IntegerField(default=0)


# 4. Models traffic artefacts whose movements should be optimized ........
class Artefact(models.Model):
    padestrians = models.IntegerField(default=0)
    cars = models.IntegerField(default=0)
    taxi = models.IntegerField(default=0)
    bus = models.IntegerField(default=0)


# 5. Models a single Road going in or out of an intersection .............
class Road(models.Model):

    intersection_in = models.ForeignKey(
        Intersection, 
        blank=True, 
        null=True,
        on_delete=models.SET_NULL,
        related_name='%(class)s_in'
    )

    intersection_out =  models.ForeignKey(
        Intersection, 
        blank=True, 
        null=True,
        on_delete=models.SET_NULL,
        related_name='%(class)s_out'
    )

    road_name = models.CharField(max_length=200)
    road_distance = models.IntegerField(default=0)
    average_speed = models.IntegerField(default=0)
    
    trafficlight =  models.ForeignKey(
        TrafficLight, 
        blank=False, 
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.name

