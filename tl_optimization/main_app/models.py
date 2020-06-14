from django.db import models

# Create your models here.

# Models an intersection into which different roads meet
class Intersection(models.Model):
    name = models.CharField( max_length=200 )
    right_of_way = models.TextField( blank=True )
    configuration = models.TextField( blank=True )

# Models traffic artefacts whose movements should be optimized
class Artefact(models.Model):
    padestrians = models.IntegerField(default=0)
    cars = models.IntegerField(default=0)
    taxi = models.IntegerField(default=0)
    bus = models.IntegerField(default=0)

# Models a single Road going in or out of an intersection
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
    name = models.CharField(max_length=200)
    capacity = models.IntegerField(default=0)
    average_speed = models.IntegerField(default=0)
    
    traffic =  models.ForeignKey(
        Artefact, 
        blank=True, 
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.name

