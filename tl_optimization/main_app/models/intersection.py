# Headers ..................................................
from django.db import models
from django.urls import reverse
from datetime import datetime
from influxdb import InfluxDBClient
import pandas as pd

# Import other necesary methods ............................
from .network import Network


from ..optimizer.intersection_optimizer import *
from ..optimizer.time_series_forecast import *


# 2. Models the behavior of a single intersection within a road network ................................................
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
    forecast_model = models.FileField( upload_to='intersection/forecast_model/' )

    def get_absolute_url(self):
        return reverse('home', args=(self.id,))
    
    def __str__(self):
        return self.intersection_name

    def optimizer(self):
        tsf_services = Time_Series_Forecast()
        data = tsf_services.prepare_data()
        tsf_services.forecast_model()
        results = tsf_services.prediction()
        return data, results

    # Saving CSV Time Series data to InfluxDB
    def upload_historic_data(self, data):
        # Create database client 
        client = InfluxDBClient(host='localhost', port=8086)
        
        # Check if database for this intersection doesnt exist
        list = client.get_list_database()
        network = Network.object.get(pk=self.network_id)

        if {'name':self.intersection_name} not in list:
            client.create_database(network.network_name)
        
        # Connect database
        client.switch_database(network.network_name)

        # Open data in pandas 
        df = pd.read_csv(data, header=None)

        # Convert data to json format for storage
        headers = df[0]

        json_body = []
        for record in df[1:]:
            dict = {}
            for road,count in zip( headers[1:], record[1:]):
                pair = { road: count }
                dict.update(pair)

            json_record = {
                "measurement": "roadTraffic",
                "tags": {
                    "intersection_name": self.intersection_name,
                    "intersection_id": self.id
                },
                "time": record[0],
                "fields": dict
            }
            json_body.append( json_record )
        
        # Saving data to data base
        status = client.write_points(json_body)

        return status 

    # Retrieving time series data from database from database into pandas dataframe
    def get_historic_time_series_data(self):

        # Create database client 
        client = InfluxDBClient(host='localhost', port=8086)
        
        # Check if database for this intersection exist
        list = client.get_list_database()
        network = Network.object.get(pk=self.network_id)
        if {'name':self.intersection_name} not in list:
            return None

        # Connect database
        client.switch_database(network.network_name)

        # Query the time series database by default use hourly interval
        results = client.query('SELECT * FROM "roadTraffic" ')
        points = results.get_points(tags={"intersection_name":self.intersection_name})

        return points

    def train_model(self):
        tsf_services = Time_Series_Forecast()
        data = tsf_services.prepare_data()
        tsf_services.forecast_model()

    def forecast_traffic(self):
        results = tsf_services.prediction()
        return results
