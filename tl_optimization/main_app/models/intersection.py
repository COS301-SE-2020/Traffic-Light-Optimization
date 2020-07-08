from django.db import models
from tl_optimization.main_app.Road_Network.road_network_contoller import Network
from tl_optimization.main_app.Road_Network.road import Road

class Intersection(models.Model):

    network = models.ForeignKey(
        Network, 
        blank=True, 
        null=True,
        on_delete=models.SET_NULL
    )

    name = models.CharField( max_length=200 )
    right_of_way = models.TextField( blank=True )
    configuration = models.TextField( blank=True )

    def __init__(self):
        super().__init__()
        self.roads_In = []
        self.roads_Out = []
        self.location_X = 0
        self.location_Y = 0
     
    def add_Road_In(self, road = None):
        if road == None :
            return False
        self.roads_In.append( road )

    def add_Road_Out(self, road = None):
        if road == None:
            return False
        self.roads_Out.append()

    def remove_Road_In(self, road = None):
        if road == None:
            return False
        
        if road not in self.roads_In:
            return False

        self.roads_In.remove( road )
        return True
    
    def remove_Road_out(self, road = None):
        if road == None:
            return False
        
        if road not in self.roads_Out:
            return False

        self.roads_Out.remove( road )
        return True

   
    def get_Roads_In(self):
        return self.add_Road_In

    def get_Roads_Out(self):
        return self.roads_Out
        
