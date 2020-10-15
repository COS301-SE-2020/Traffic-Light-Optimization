# Headers ..................................................
from django.db import models
from django.urls import reverse
import random

# Import other necesary methods ............................
from .road import Road



# Model for daily traffic forecast
class DayForecast(models.Model):
    road_id = models.ForeignKey(
        Road, 
        blank=False, 
        null=True,
        on_delete=models.SET_NULL
    )

    hour_0 = models.IntegerField(default=random.randint(150, 400))
    hour_1 = models.IntegerField(default=random.randint(150, 400))
    hour_2 = models.IntegerField(default=random.randint(150, 400))
    hour_3 = models.IntegerField(default=random.randint(150, 400))
    hour_4 = models.IntegerField(default=random.randint(150, 400))
    hour_5 = models.IntegerField(default=random.randint(150, 400))
    hour_6 = models.IntegerField(default=random.randint(150, 400))
    hour_7 = models.IntegerField(default=random.randint(150, 400))
    hour_8 = models.IntegerField(default=random.randint(150, 400))
    hour_9 = models.IntegerField(default=random.randint(150, 400))
    hour_10 = models.IntegerField(default=random.randint(150, 400))
    hour_11 = models.IntegerField(default=random.randint(150, 400))
    hour_12 = models.IntegerField(default=random.randint(150, 400))
    hour_13 = models.IntegerField(default=random.randint(150, 400))
    hour_14 = models.IntegerField(default=random.randint(150, 400))
    hour_15 = models.IntegerField(default=random.randint(150, 400))
    hour_16 = models.IntegerField(default=random.randint(150, 400))
    hour_17 = models.IntegerField(default=random.randint(150, 400))
    hour_18 = models.IntegerField(default=random.randint(150, 400))
    hour_19 = models.IntegerField(default=random.randint(150, 400))
    hour_20 = models.IntegerField(default=random.randint(150, 400))
    hour_21 = models.IntegerField(default=random.randint(150, 400))
    hour_22 = models.IntegerField(default=random.randint(150, 400))
    hour_23 = models.IntegerField(default=random.randint(150, 400))

    def forecast_info_(self):
        data = [self.hour_0,self.hour_1,self.hour_2,self.hour_3,self.hour_4,self.hour_5,self.hour_6,self.hour_7,self.hour_8,
                self.hour_9,self.hour_10,self.hour_11, self.hour_12,self.hour_13,self.hour_14,self.hour_15,self.hour_16,
                self.hour_17,self.hour_18,self.hour_19,self.hour_20,self.hour_21,self.hour_22,self.hour_23]
        return data

    def forecast_info(self):
        data = [ random.randint(150,400) for i in range(24)]
        return data

    def forecast_info_save(self):
        self.hour_0 = default=random.randint(150, 400)
        self.hour_1 = default=random.randint(150, 400)
        self.hour_2 = default=random.randint(150, 400)
        self.hour_3 = default=random.randint(150, 400)
        self.hour_4 = default=random.randint(150, 400)
        self.hour_5 = default=random.randint(150, 400)
        self.hour_6 = default=random.randint(150, 400)
        self.hour_7 = default=random.randint(150, 400)
        self.hour_8 = default=random.randint(150, 400)
        self.hour_9 = default=random.randint(150, 400)
        self.hour_10 = default=random.randint(150, 400)
        self.hour_11 = default=random.randint(150, 400)
        self.hour_12 = default=random.randint(150, 400)
        self.hour_13 = default=random.randint(150, 400)
        self.hour_14 = default=random.randint(150, 400)
        self.hour_15 = default=random.randint(150, 400)
        self.hour_16 = default=random.randint(150, 400)
        self.hour_17 = default=random.randint(150, 400)
        self.hour_18 = default=random.randint(150, 400)
        self.hour_19 = default=random.randint(150, 400)
        self.hour_20 = default=random.randint(150, 400)
        self.hour_21 = default=random.randint(150, 400)
        self.hour_22 = default=random.randint(150, 400)
        self.hour_23 = default=random.randint(150, 400)
        self.save()