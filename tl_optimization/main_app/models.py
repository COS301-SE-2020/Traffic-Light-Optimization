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
        return reverse('home', args=(self.id,))
    
    def __str__(self):
        return self.intersection_name





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

    A, B, C, D = 'A', 'B','C','D'
    POSITION_CHOICE = [ (A,'A'), (B,'B'), (C,'C'), (D,'D'),]
    position = models.CharField(
        max_length=1,
        choices=POSITION_CHOICE,
        default=A,
    )


    def get_absolute_url(self):
        return reverse('road', args=[self.network_id.id,self.id])

    def __str__(self):
        return self.road_name

    def road_info(self):
        light_info = {}
        if TrafficLight.objects.filter(road_id=self.id).exists():
            light = TrafficLight.objects.filter(road_id=self.id)
            light_info = [ _.light_info() for _ in light ]
        else:
            light_info = {
                "red": 0,
                "orange": 0,
                "green": 0
            }

        info = {
            "name": road_name ,
            "capaicty": road_distance,
            "speed": average_speed,
            "traffic-light": light
        }
        return info

# 3. Models a single traffic light within an intersection ......................
class TrafficLight(models.Model):
    road_id = models.ForeignKey(
        Road, 
        blank=False, 
        null=True,
        on_delete=models.SET_NULL
    )
    date_time = models.DateTimeField() 
    traffic_info = models.IntegerField(default=0)

    timing_red = models.IntegerField(default=0)
    timing_yellow = models.IntegerField(default=0)
    timing_green = models.FloatField(default=0)

    def get_absolute_url(self):
        road = Road.objects.get(pk=self.road_id)
        return reverse('trafficlight', args=(road.network_id.id, self.road_id.id, self.id))
    
    def __str__(self):
        return self.timing_green

    def light_info(self):
        light_info = {
            "red": timing_red,
            "orange": timing_yellow,
            "green": timing_green
        }
        return light_info