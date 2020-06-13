try:
    from initialize import Initialize
    from readFile import ReadFile
    from write import Write
except Exception as e:
    print("there are some modules missing {}".format(e))

url = "https://eu-central-1-1.aws.cloud2.influxdata.com"
organisation = "cos301.alpha@gmail.com"
token = "okx-Wk8zR33DYZxZP91T10ZTfUFmMz866DCKfE3Z8l5azgUT3QLIIdzk6rATGgCdAyuaAbWrReSi9KfchjW0kg=="
bucket = "test Bucket"

path = r'data/traffic-signals-status-1.csv'

initialize = Initialize()
initialize.connectToDB(url, token, organisation)

readfile = ReadFile()
readfile.setPath(path)
readfile.readData()

write = Write()
write.setClient(initialize.getClient())
write.setData(readfile.getData())
write.writeToDB(bucket, organisation)

# on Windows cmd / visual studio code terminal
# install Visual C++ Build Tools 2015 
# pip install influxdb_client
# pip install pandas