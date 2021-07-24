
class Config:

    def __init__(self, dataReader):
        import os

        self.__dataReader = dataReader
        try:
            self.__config = dataReader.readDataFile("config/config.txt")
        except:
            self.__config = dataReader.readDataFile("config/configDefault.txt")

        self.__projects = dataReader.readDataFile("config/projectlist.txt")
        self.__checkIfProjectExists()

    def __checkIfProjectExists(self):
        import os

        toBeDeleted=[]
        for key in self.__projects.keys():
            if os.path.exists(self.__projects[key]) !=True:
                toBeDeleted.append(key)

        for key in toBeDeleted:
            self.__projects.pop(key)

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

    def addProjectPath(self, path):
        import os
        name = path.split("/")[-2]
        if path.startswith(os.getcwd().replace("\\", "/")):
            path = path.replace(os.getcwd().replace("\\", "/"), "")
            path=path[1:]
        path.replace("//", "/")
        self.addProject(name, path)

    def addProject(self, key, value):
        self.__projects[key] = value
        self.saveProjects()

    def saveProjects(self):
        self.__dataReader.writeDataFile("config/projectlist.txt", self.__projects)

    def getOSbits(self):
        import platform
        return platform.architecture()[0]