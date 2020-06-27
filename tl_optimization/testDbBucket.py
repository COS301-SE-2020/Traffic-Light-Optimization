from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "test Bucket"

client = InfluxDBClient(url="https://eu-central-1-1.aws.cloud2.influxdata.com", token="X4zOjxT5v6uu6d0QLJ4o9OlcYttkqFD7-AeGqQXfl5Mmg_lU_2jly9RdCtbHXz79IC6hQ3CfRV1aniB2yeCndA==", org="cos301.alpha@gmail.com")

## write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

## p = Point("my_measurement").tag("location", "Prague").field("temperature", 25.3)

## write_api.write(bucket=bucket, record=p)

## using Table structure
tables = query_api.query('from(bucket:"test Bucket") |> range(start: -1h)')

for table in tables:
    print(table)
    for row in table.records:
        print (row.values)

## using csv library
csv_result = query_api.query_csv('from(bucket:"test Bucket") |> range(start: -1h)')
val_count = 0
for row in csv_result:
    for cell in row:
        val_count += 1