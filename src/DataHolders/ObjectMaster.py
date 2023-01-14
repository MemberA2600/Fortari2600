import os
from threading import Thread
from copy import deepcopy
from Compiler import Compiler

class ObjectMaster:

    def __init__(self, loader):
        self.__loader   = loader
        self.__compiler = Compiler(self.__loader, "common", "dummy", None)

        self.objects = {}
        for num in range(2, 9):
            bankNum = "bank"+str(num)
            self.objects[bankNum] = {}

        self.objects["currentBank"] = self.objects["bank2"]

        for root, dirs, files in os.walk("templates/objects/Game"):
            for dir in dirs:
                path = self.__pathToListOfObj(root + "/" + dir)
                objRoot = self.objects
                for objName in path:
                    if objName not in objRoot:
                       objRoot[objName] = {}
                    objRoot = objRoot[objName]

            for file in files:
                path = self.__pathToListOfObj(root + "/" + file)
                objRoot = self.objects

                for objName in path:
                    if objName.endswith(".asm") == False:
                       objRoot = objRoot[objName]
                    else:
                       text = self.__loader.io.loadWholeText(root + "/" + file)
                       name = objName.split(".")[0]
                       f = open((root + "/" + file), "r")
                       firstLine = f.read().replace("\r", "").split("\n")[0]
                       f.close()

                       listOfParams = firstLine.split("=")[1]
                       key = name + "(" + listOfParams + ")"
                       objRoot[key] = text

                """
                objRoot = self.objects
                for objName in path:
                    if objName not in objRoot:
                       if objName.endswith(".asm"):
                           text = self.__loader.io.loadWholeText(root + "/" + file)
                           name = objName.split(".")[0]
                           f = open((root + "/" + file), "r")
                           firstLine = f.read().replace("\r", "").split("\n")[0]
                           f.close()

                           listOfParams=firstLine.split("=")[1]
                           key = name + "(" + listOfParams + ")"

                           objRoot[key] = text
                       else:
                           objRoot[objName] = {}
                           objRoot = objRoot[objName]
                """
        # print(self.objects)

    def __changeCurrentBankPointer(self, bankNum):
        if type(bankNum) == int:
           bankNum = "bank" + str(int)

        self.objects["currentBank"] = self.objects[bankNum]

    def __pathToListOfObj(self, path):
        return path.replace("\\", "/").replace("templates/objects/Game/", "").split("/")

    def generateScreenObjects(self):
        codes = self.__loader.virtualMemory.codes

        for num in range(2, 9):
            bankKey = "bank"+str(num)
            self.objects[bankKey] = {}

            for key in codes[bankKey].key():
                if key in ["screen_top", "screen_bottom"]:
                   codeLines = self.objects[bankKey][key]
                   for line in codeLines:
                       if line.startswith("*") == False and line.startswith("#") == False:
                          data = line.split("=")[1].split(" ")
                          name = data[0]
                          typ  = data[1]

                          path = "templates/objects/screenItems/" + typ + "/"
                          for root, dirs, files in os.walk(path):
                              for file in files:
                                  if file.endswith(".asm"):
                                      f = open((root + "/" + file), "r")
                                      txtToSave = self.__loader.io.loadWholeText(root + "/" + file)
                                      f.close()

                                      firstLine  = txtToSave.replace("\r", "").split("\n")[0]
                                      secondLine = txtToSave.replace("\r", "").split("\n")[1]
                                      listOfReplacePositions=secondLine.split("=")[1]

                                      counter = 0
                                      exit    = False
                                      for replaceNum in listOfReplacePositions:
                                          color = False
                                          if "C" in replaceNum:
                                              color = True
                                              replaceNum = replaceNum.replace("C", "")

                                          replaceNum = int(replaceNum)
                                          counter   += 1
                                          varRep    = None
                                          if counter < 10:
                                             varRep  = "VAR0" + str(counter)
                                          else:
                                             varRep  = "VAR"  + str(counter)

                                          varName = data[replaceNum]
                                          var     = self.__loader.virtualMemory.getVariableByName2(varName)
                                          if var  == False:
                                             exit = True
                                             break

                                          replaceText = ""
                                          if var.type != "byte":
                                             if color:
                                                replaceText = self.__compiler.moveVarToTheRight(var.usedBits, True)
                                             else:
                                                replaceText = self.__compiler.convertAnyTo8Bits(var.usedBits)

                                          txtToSave = txtToSave.replace("!!!" + varRep + "_CHANGE!!!", replaceText)\
                                                               .replace(varRep, data[replaceNum])

                                      if exit: continue

                                      listOfParams = firstLine.split("=")[1]
                                      procedure = name + "(" + listOfParams + ")"
                                      
                                      self.objects[bankKey][name][procedure] = txtToSave

        self.objects["currentBank"] = self.objects[self.__loader.bigFrame.getCurrentBank()]

    def returnNextLevelOrProcesses(self, fullLine):
        delimiter = "%"
        listOfValidDelimiters = self.__loader.config.getValueByKey("validObjDelimiters").split(" ")
        for symbol in listOfValidDelimiters:
            if symbol in fullLine:
               delimiter = symbol
               break

        data = fullLine.split(delimiter)
        if data[0] == "game":
           data.pop(0)

        objLevl = None
        try:
            objLevl = self.objects[data[0]]
        except:
            return False

        try:
            for obj in data[1:-1]:
                objLevl = objLevl[obj]
        except:
            return False

        if type(objLevl[data[-1]]) == dict:
           return(objLevl[data[-1].keys()])
        else:
            return False

    def returnNextLevel(self, name):
        if name == "game": return list(self.objects.keys())

        for lvl1 in self.objects.keys():
            if name.upper() == lvl1.upper(): return list(self.objects[lvl1].keys())
            for lvl2 in self.objects[lvl1].keys():
                if name.upper() == lvl2.upper():
                   if type(self.objects[lvl1][lvl2]) == dict:
                      return list(self.objects[lvl1][lvl2].keys())

        return([])

    def returnParamsForProcess(self, line):
        if line == None: return []

        delimiter = "%"
        listOfValidDelimiters = self.__loader.config.getValueByKey("validObjDelimiters").split(" ")
        for symbol in listOfValidDelimiters:
            if symbol in line:
               delimiter = symbol
               break

        data = line.split(delimiter)
        if data[0] == "game":
           data.pop(0)

        while "" in data:
            data.remove("")

        word = None
        base = None

        if   len(data) == 2:
           base = self.objects[data[0]]
        elif len(data) == 3:
           base = self.objects[data[0]][data[1]]
        else:
           return []

        for key in base.keys():
            if type(base[key]) != dict:
                if key.split("(")[0] == data[-1]:
                   return key.split("(")[1][:-1].split(",")

        return []

    def returnOcjectOrProcess(self, name):
        if name == "game": return "object"

        for lvl1 in self.objects.keys():
            if name.upper() == lvl1.upper(): return "object"
            for lvl2 in self.objects[lvl1].keys():
                if name.upper() == lvl2.split("(")[0].upper():
                   if type(self.objects[lvl1][lvl2]) == dict:
                      return "object"
                   else:
                      return "process"
                if type(self.objects[lvl1][lvl2]) == dict:
                   for lvl3 in self.objects[lvl1][lvl2].keys():
                       if self.objects[lvl1][lvl2][lvl3].split("(")[0].upper() == name.upper(): return "process"

    def getObjectsAndProcessesValidForGlobalAndBank(self):
        # It assumes there are up to 3 levels

        objectList  = []
        processList = []

        ignored = []

        for keyNum in range(2, 9):
            bankNum = "bank" + str(keyNum)
            ignored.append(bankNum)

        for lvl1Key in self.objects.keys():
            if lvl1Key in ignored: continue

            objectList.append(lvl1Key)

            for lvl2Key in self.objects[lvl1Key]:

                objectList.append(lvl2Key)

                if type(self.objects[lvl1Key][lvl2Key]) == {}:
                    for lvl3Key in self.objects[lvl1Key][lvl2Key]:
                        processList.append(lvl3Key.split("(")[0])
                else:
                   processList.append(lvl2Key.split("(")[0])

        return objectList, processList

    def getStartingObjects(self):
        objectList  = []
        ignored = []
        for keyNum in range(2, 9):
            bankNum = "bank" + str(keyNum)
            ignored.append(bankNum)

        for lvl1Key in self.objects.keys():
            if lvl1Key in ignored: continue
            objectList.append(lvl1Key)

        return objectList