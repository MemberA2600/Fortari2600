
class Config:

    def __init__(self, dataReader):
        import os

        self.__dataReader = dataReader
        try:
            self.__config = dataReader.readDataFile("config/config.txt")
        except:
            self.__config = dataReader.readDataFile("config/configDefault.txt")

    def getValueByKey(self, key):
        return(self.__config[key])

    def getKeys(self):
        return(self.__config.keys())

    def saveConfig(self):
        self.__dataReader.writeDataFile("config/config.txt", self.__config)