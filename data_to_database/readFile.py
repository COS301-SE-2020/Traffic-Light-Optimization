try:
    import pandas as pd
except Exception as e:
    print("there are some modules missing {}".format(e))
class ReadFile:

    def setPath(self, path):
        self.path = path

    def readData(self):
        try:
            self.csvData = pd.read_csv(self.path)
        except Exception:
            self.path = "file path does not exist"

    def getData(self):
        return self.csvData