# Headers ..................................................
from django.db import models
from django.urls import reverse


# 1. Models an intersection into which different roads meet ...........................................................
class Network(models.Model):
    network_name = models.CharField( max_length=50, unique=True )

    def get_absolute_url(self):
        return reverse('road_network', args=[self.id])
    
    def __str__(self):
        return self.network_name