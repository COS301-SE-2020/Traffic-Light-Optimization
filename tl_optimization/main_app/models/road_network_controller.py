from tl_optimization.main_app.Road_Network.intersection import Intersection
from django.shortcuts import get_object_or_404
from ..models import *

class Network(models.Model):
    
    network_name = models.CharField( max_length=200 )
    
    def create(self):
        #query database for the networks .....
        id_network = ""
        if id_network == "":
            return False
        #inter = Intersection( name )
        return True
        

    def get_Network(self, id_network="" ):
        # 1. Check for valid id ...........
        if id_network=="":
            return None

        # 2. Query the database ......................
        interDataValues = get_object_or_404( Intersection, id_network)
        
        # 3. Create diffent intersection objects 
        for intersec in interDataValues:
            new_intersection = Intersection( intersec.pk )
            self.intersections.append( new_intersection )
        return self.intersections



