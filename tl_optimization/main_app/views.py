from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import InfluxDBClient
from numpy import random
import csv
import io
from django.http import HttpResponse
import datetime


# Create your views here.

def upload(request):
    organisation_ = "cos301.alpha@gmail.com"
    token_ = "okx-Wk8zR33DYZxZP91T10ZTfUFmMz866DCKfE3Z8l5azgUT3QLIIdzk6rATGgCdAyuaAbWrReSi9KfchjW0kg=="
    bucket_ = "test Bucket"
    url_ = "https://eu-central-1-1.aws.cloud2.influxdata.com"

    client = InfluxDBClient(url=url_, token=token_, org=organisation_)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    if request.method == 'POST':
        if request.POST['tl_form'] == 'add-traffic-light':
            json_body = [
                {
                    "measurement": "added_traffic_lights",
                    "tags": {
                        "tl_id": request.POST['tl_id'],
                        "tl_location": request.POST['tl_location'],
                        "tl_status": "red",
                        "tl_type": request.POST['tl_type'],
                        "tl_name": request.POST['tl_name'],
                        "tl_intersection": request.POST['tl_intersection'],
                        "tl_operation_state": datetime.datetime.fromtimestamp(1594688061).isoformat(),
                        "tl_operation_processed_time": datetime.datetime.fromtimestamp(1594688061).isoformat()
                    },
                    "fields": {
                        "car_capacity": None,
                        "num_lanes": request.POST['num_lanes'],
                        "num_cars": 0
                    },
                    "time": None
                }
            ]
            write_api.write(bucket=bucket_, org=organisation_, record=json_body)
            # print(json_body)
        elif request.POST['tl_form'] == 'add-historic-data':
            uploaded_file = request.FILES['filename']
            if uploaded_file.name.endswith('.csv'):
                messages.error(request, 'Not a csv file')
                csv_data = uploaded_file.read().decode('UTF-8')
                io_data = io.StringIO(csv_data)

                next(io_data)
                status = ["red", "green", "orange"]
                tl_type = ["standard", "pedestrian", "turn"]
                car_capacity = [20, 25]
                for column in csv.reader(io_data, delimiter=',', quotechar="|"):
                    random_index = random.randint(1)
                    index = random.randint(2)
                    num_cars = random.randint(20)
                    json_body = [
                        {
                            "measurement": "traffic_lights",
                            "tags": {
                                "tl_id": column[0],
                                "tl_location": "Austin, Texas",
                                "tl_status": status[index],
                                "tl_type": tl_type[index],
                                "tl_name": column[8],
                                "tl_intersection": column[2],
                                "tl_operation_state": column[4],
                                "tl_operation_processed_time": column[5]
                            },
                            "fields": {
                                "car_capacity": car_capacity[random_index],
                                "num_lanes": 3,
                                "num_cars": num_cars
                            },
                            "time": None
                        }
                    ]
                    # print(json_body)
                    write_api.write(bucket=bucket_, org=organisation_, record=json_body)
        else:
            print("Incorrect values entered")
    else:
        print("hello")
    return render(request, 'main_app/base.html')

def create(request):
    organisation_ = "cos301.alpha@gmail.com"
    token_ = "okx-Wk8zR33DYZxZP91T10ZTfUFmMz866DCKfE3Z8l5azgUT3QLIIdzk6rATGgCdAyuaAbWrReSi9KfchjW0kg=="
    bucket_ = "test Bucket"
    url_ = "https://eu-central-1-1.aws.cloud2.influxdata.com"


    client = InfluxDBClient(url=url_, token=token_, org=organisation_)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    if request.method == 'POST':
        # print(request.POST['tl_form'])
        if request.POST['tl_form'] == 'add_traffic_light':
            json_body = [
                {
                    "measurement": "added_traffic_lights",
                    "tags": {
                        "tl_id": request.POST['tl_id'],
                        "tl_location": request.POST['tl_location'],
                        "tl_status": "red",
                        "tl_type": request.POST['tl_type'],
                        "tl_name": request.POST['tl_name'],
                        "tl_intersection": request.POST['tl_intersection'],
                        "tl_operation_state": datetime.datetime.fromtimestamp(1594688061).isoformat(),
                        "tl_operation_processed_time": datetime.datetime.fromtimestamp(1594688061).isoformat()
                    },
                    "fields": {
                        "car_capacity": None,
                        "num_lanes": request.POST['num_lanes'],
                        "num_cars": 0
                    },
                    "time": None
                }
            ]
            print(json_body)
            # write_api.write(bucket=bucket_, org=organisation_, record=json_body)
            # uploaded_file = request.FILES['filename']
            # if uploaded_file.name.endswith('.csv'):
                # print("uploading content")
            #     messages.error(request, 'Not a csv file')
            #     csv_data = uploaded_file.read().decode('UTF-8')
            #     io_data = io.StringIO(csv_data)

            #     next(io_data)
            #     status = ["red", "green", "orange"]
            #     tl_type = ["standard", "pedestrian", "turn"]
            #     car_capacity = [20, 25]
            #     for column in csv.reader(io_data, delimiter=',', quotechar="|"):
            #         random_index = random.randint(1)
            #         index = random.randint(2)
            #         num_cars = random.randint(20)
            #         json_body = [
            #             {
            #                 "measurement": "traffic_lights",
            #                 "tags": {
            #                     "tl_id": column[0],
            #                     "tl_location": "Austin, Texas",
            #                     "tl_status": status[index],
            #                     "tl_type": tl_type[index],
            #                     "tl_name": column[8],
            #                     "tl_intersection": column[2],
            #                     "tl_operation_state": column[4],
            #                     "tl_operation_processed_time": column[5]
            #                 },
            #                 "fields": {
            #                     "car_capacity": car_capacity[random_index],
            #                     "num_lanes": 3,
            #                     "num_cars": num_cars
            #                 },
            #                 "time": None
            #             }
            #         ]
            #         write_api.write(bucket=bucket_, org=organisation_, record=json_body)
    else:
        print("sup")
    return render(request, 'main_app/base.html')

def simulation(request):
    return render(request, 'main_app/simulation.html')

def index(request):
    return HttpResponse("Hello, world. You're at the main_app's index.")

def home(request):
    return render(request, 'main_app/home.html')