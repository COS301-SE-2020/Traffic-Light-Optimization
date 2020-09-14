# Headers ..................................................
from django.db import models
from django.urls import reverse

# Import other necesary methods ............................
from .network import Network
from .intersection import Intersection

# 5. Models a single Road going in or out of an intersection ......................................................
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

    road_name = models.CharField( max_length=50)
    road_distance = models.IntegerField(default=0)
    average_speed = models.IntegerField(default=0)
    num_lanes = models.IntegerField(default=1)

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

        info = {
            "id": self.id,
            "name": self.road_name ,
            "capacity": self.road_distance,
            "speed": self.average_speed,
            "position": self.position,
            "lanes": self.num_lanes,
        }
        return info