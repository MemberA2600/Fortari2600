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
        #print(self.objects)

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




