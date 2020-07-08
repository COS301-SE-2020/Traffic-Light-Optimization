from django.db import models
from tl_optimization.main_app.Road_Network.traffic_light import TrafficLight 

class Road:

    def __init__(self, nextR = []):
        self.traffic_light = TrafficLight()
        self.next_Road = nextR
        
    def get_Next_Road(self):
        return self.nextRoad

    def add_Next_Road(self, nextR = None):
        if nextR == None:
            return
        self.nextRoad.append(nextR)
    
    def update_Next_Road(self, nextRs = []):
        self.nextRoad = nextRs