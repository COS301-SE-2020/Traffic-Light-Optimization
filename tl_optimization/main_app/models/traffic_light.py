from django.db import models
class TafficLight:
    
    def __init__(self, timing = [0,0,0]):
        if len( timing ) == 0:
            timing = [0,0,0]
        self.red = timing[0]
        self.yellow = timing[1]
        self.green = timing[2]

    def get_Light_Timing(self):
        return self.red, self.yellow, self.green

    def set_Light_Timing(self, timing = []):
        if len( timing ) == 0:
            return 
        self.red = timing[0]
        self.yellow = timing[1]
        self.green = timing[2]