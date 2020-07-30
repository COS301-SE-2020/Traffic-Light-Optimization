from django.db import models
from django.urls import reverse
# Create your models here.

# 1. Models an intersection into which different roads meet .....................
class Network(models.Model):
    network_name = models.CharField( max_length=50, unique=True )

    def get_absolute_url(self):
        return reverse('road_network', args=[self.id])
    
    def __str__(self):
        return self.network_name

# 2. Models the behavior of a single intersection within a road network .........
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
        return reverse('intersection', args=(self.network_id.id , self.id))
    
    def __str__(self):
        return self.intersection_name

# 3. Models a single traffic light within an intersection ......................
class TrafficLight(models.Model):
    intersection_id = models.ForeignKey(
        Intersection, 
        blank=False, 
        null=True,
        on_delete=models.SET_NULL
    )
    timing_red = models.IntegerField(default=0)
    timing_yellow = models.IntegerField(default=0)
    timing_green = models.IntegerField(default=0)

    def get_absolute_url(self):
        intersection = Intersection.objects.get(pk=self.intersection_id)
        return reverse('trafficlight', args=(intersection.network_id.id, self.intersection_id.id, self.id))
    
    def __str__(self):
        return self.timing_green


# 4. Models traffic artefacts whose movements should be optimized .................
class Artefact(models.Model):
    padestrians = models.IntegerField(default=0)
    cars = models.IntegerField(default=0)
    taxi = models.IntegerField(default=0)
    bus = models.IntegerField(default=0)


# 5. Models a single Road going in or out of an intersection ......................
class Road(models.Model):
    network_id = models.ForeignKey(
        Network, 
        blank=False, 
        null=True,
        on_delete=models.SET_NULL
    )

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

    road_name = models.CharField( max_length=50, unique=True)
    road_distance = models.IntegerField(default=0)
    average_speed = models.IntegerField(default=0)
    
    trafficlight_id =  models.ForeignKey(
        TrafficLight, 
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
    )

    def get_absolute_url(self):
        return reverse('road', args=[self.network_id.id,self.id])

    def __str__(self):
        return self.road_name

