import os
from copy import deepcopy

class Collector:
    from sys import path as systemPath


    def __init__(self, systemPath):

        for root, dir, files in os.walk("src/", topdown=False):
            systemPath.append(root)

        self.__systemPath = systemPath
        self.__backUp = deepcopy(systemPath)

    def getSelectedOnlyFromDir(self, dir, listOfModules):
        for root, dir, files in os.walk("pythonNotMadeByMe/"+dir+"/", topdown=False):
            for file in files:
                if (file in listOfModules) and (root not in self.__systemPath):
                    self.__systemPath.append(root)

    def restoreSystemPath(self):
        self.__systemPath = deepcopy(self.__backUp)

    def manuallyRegisterPackage(self, dir):
        for root, dir, files in os.walk("pythonNotMadeByMe/"+dir+"/", topdown=False):
            self.__systemPath.append(root)
