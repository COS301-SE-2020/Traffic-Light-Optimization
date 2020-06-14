try:
    from influxdb_client import InfluxDBClient
except Exception as e:
    print("there are some modules missing {}".format(e))
# on Windows
# install Visual C++ Build Tools 2015 
# pip install influxdb_client
# 

class Initialize:

    def connectToDB(self, u, t, o): # results will only be seen when writing
        self.client = InfluxDBClient(url = u, token = t, org = o)

    def getClient(self):
        return self.client
    # organisation = "cos301.alpha@gmail.com"
    # tk = "okx-Wk8zR33DYZxZP91T10ZTfUFmMz866DCKfE3Z8l5azgUT3QLIIdzk6rATGgCdAyuaAbWrReSi9KfchjW0kg=="
    # buck = "test Bucket"

    
   # client = InfluxDBClient(url = "https://eu-central-1-1.aws.cloud2.influxdata.com", token = tk, org = organisation)
