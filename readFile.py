import pandas as pd

class ReadFile:

    def setPath(self, path):
        self.path = path

    def readData(self):
        self.csvData = pd.read_csv(self.path)
        #print(csvData.columns)

    def getData(self):
        return self.csvData