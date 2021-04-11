
class DataReader:

    def __init__(self):
        pass

    def readDataFile(self, path):

        data = []

        try:
            file = open(path, "r", encoding="latin-1")
            data = file.readlines()
        except:
            file = open(path, "rb")
            str = file.read().decode("latin-1")
            data = str.split("\n")
        __dict = {}
        file.close()
        for line in data:
            line = line.replace("\r", "").replace("\n", "")
            if line != "":
                __dict[line.split("=")[0]] = line.split("=", 2)[1]
        return(__dict)

    def writeDataFile(self, path, keysValues):
        temp = []
        file = open(path, "w", encoding="latin-1")
        for key in keysValues.keys():
            temp.append(key+"="+keysValues[key]+"\r\n")
        file.writelines(temp)
        file.close()