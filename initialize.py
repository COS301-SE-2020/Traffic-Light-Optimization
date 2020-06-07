from influxdb_client import InfluxDBClient

#### database details
organisation = "cos301.alpha@gmail.com"
tk = "okx-Wk8zR33DYZxZP91T10ZTfUFmMz866DCKfE3Z8l5azgUT3QLIIdzk6rATGgCdAyuaAbWrReSi9KfchjW0kg=="
buck = "test Bucket"

#### database connection
client = InfluxDBClient(url = "https://eu-central-1-1.aws.cloud2.influxdata.com", token = tk, org = organisation)
