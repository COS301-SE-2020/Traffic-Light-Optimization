from initialize import Initialize
from readFile import ReadFile
from write import Write

url = "https://eu-central-1-1.aws.cloud2.influxdata.com"
organisation = "cos301.alpha@gmail.com"
tk = "okx-Wk8zR33DYZxZP91T10ZTfUFmMz866DCKfE3Z8l5azgUT3QLIIdzk6rATGgCdAyuaAbWrReSi9KfchjW0kg=="
buck = "test Bucket"

path = r'data/traffic-signals-status-1.csv'

initialize = Initialize()
initialize.connectToDB(url, tk, organisation)

readfile = ReadFile()
readfile.setPath(path)
readfile.readData()

write = Write()
write.setClient(initialize.getClient())
write.setData(readfile.getData())
write.writeToDB(buck, organisation)