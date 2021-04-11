
class Config:

    def __init__(self, dataReader):
        import os

        self.__dataReader = dataReader
        try:
            self.__config = dataReader.readDataFile("config/config.txt")
        except:
            self.__config = dataReader.readDataFile("config/configDefault.txt")

        self.__projects = dataReader.readDataFile("config/projectlist.txt")

    def getValueByKey(self, key):
        return(self.__config[key])

    def getKeys(self):
        return(self.__config.keys())

    def saveConfig(self):
        self.__dataReader.writeDataFile("config/config.txt", self.__config)

    def runAutoSetter(self):
        self.__autoSetter.run()

    def setKey(self, key, value):
        self.__config[key] = value

    def setAutoSetter(self, autoSetter, fileDialogs):
        from AutoSetter import AutoSetter
        self.__autoSetter = autoSetter
        if self.__config["autoSetter"] == "True":
            self.__autoSetter.run()

    def getProjects(self):
        return(self.__projects.keys())

    def getProjectPath(self, key):
        return(self.__projects[key])

    def addProject(self, key, value):
        self.__projects[key] = value

    def saveProjects(self):
        self.__dataReader.writeDataFile("config/projectlist.txt", self.__projects)