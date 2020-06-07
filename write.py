import initialize
from influxdb_client.client.write_api import SYNCHRONOUS
from numpy import random


write_api = initialize.client.write_api(write_options=SYNCHRONOUS)

# measurement #
# tl_name # tl_intersection # tl_state # lane_type # num_lanes # car_capacity

tl_name = ["burnett_1", "hilda_1"]
tl_intersection = "burnett-hilsa"
car_capacity = [20, 25]
num_lanes = 3
for x in range (20):
    random_index = random.randint(1)
    num_cars = random.randint(20)
    json_body = [
        {
            "measurement": "traffic_lights",
            "tags" : {
                "tl_name": tl_name[random_index],
                "tl_intersection": tl_intersection
            },
            "fields": {
                "car_capacity": car_capacity[random_index],
                "num_lanes": num_lanes,
                "num_cars" : num_cars
            },
            "time": None
        }
    ]

    write_api.write(bucket=initialize.buck, org=initialize.organisation, record=json_body)