try:
    from influxdb_client.client.write_api import SYNCHRONOUS
    from numpy import random
except Exception as e:
    print("there are some modules missing {}".format(e))

class Write:
    
    def setClient(self, client):
        self.client = client

    def setData(self, csvData):
        self.csvData = csvData

    def setWriteMethod(self):
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def writeToDB(self, Bucket, Organisation):
        self.setWriteMethod()
        status = ["red", "green", "orange"]
        tl_type = ["standard", "pedestrian", "turn"]
        car_capacity = [20, 25]
        num_lanes = 3

        for x, row in self.csvData.iterrows():
            random_index = random.randint(1)
            index = random.randint(2)
            num_cars = random.randint(20)
            json_body = [
                {
                    "measurement": "traffic_lights",
                    "tags" : {
                        "tl_id": row[0],
                        "tl_location": "Austin, Texas",
                        "tl_status": status[index],
                        "tl_type": tl_type[index],
                        "tl_name": row[8],
                        "tl_intersection": row[2],
                        "tl_operation_state": row[4],
                        "tl_operation_processed_time": row[5]
                    },
                    "fields": {
                        "car_capacity": car_capacity[random_index],
                        "num_lanes": num_lanes,
                        "num_cars" : num_cars
                    },
                    "time": None
                }
            ]

            self.p = "correct"
            try:
                self.write_api.write(bucket = Bucket, org = Organisation, record = json_body)
            except Exception as e:
                self.p = e