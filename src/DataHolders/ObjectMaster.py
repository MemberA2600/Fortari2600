import os
from Command  import Command
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
        self.loadKernelObjects()

    def loadKernelObjects(self):
        if "game" in self.objects.keys():
            del self.objects["game"]

        try:
           self.objRoot = "templates/objects_" + self.__loader.virtualMemory.kernel + "/"
        except:
           self.objRoot = "templates/objects_common/"

        for root, dirs, files in os.walk(self.objRoot + "Game"):
            for dir in dirs:
                if dir.endswith("ß"):
                    oList = [dir.replace("ß", "0"), dir.replace("ß", "1")]
                else:
                    oList = [dir]

                for item in oList:
                    path = self.__pathToListOfObj(root + "/" + item)
                    objRoot = self.objects
                    for objName in path:
                        if objName not in objRoot:
                            objRoot[objName] = {}
                        objRoot = objRoot[objName]

            for file in files:
                if "ß" in root:
                    rList = [root.replace("ß", "0"), root.replace("ß", "1")]
                else:
                    rList = [root]

                for item in rList:
                    path = self.__pathToListOfObj(item + "/" + file)
                    objRoot = self.objects

                    for objName in path:
                        if objName.startswith("_"): continue
                        if objName.endswith(".asm") == False and objName.endswith(".a26") == False:
                            objRoot = objRoot[objName]
                        else:
                            path = item + "/" + file

                            for word in ("player", "missile"):
                                for num in range(0, 2):
                                    check = word + str(num)
                                    if check in path:
                                       path = path.replace(check, check[:-1] + "ß")
                                       break

                            text = self.__loader.io.loadWholeText(path)
                            name = objName.split(".")[0]
                            f = open(path, "r")

                            firstLine = f.read().replace("\r", "").split("\n")[0]
                            f.close()

                            if firstLine[0] in ["*", "#"]:
                                listOfParams = firstLine.split("=")[1]
                                key = name + "(" + listOfParams + ")"
                            else:
                                key = name
                            objRoot[key] = text

        f = open(self.objRoot + "listOfColorChangers.txt", "r")
        lines = f.read().replace("\r", "").split("\n")
        f.close()

        for line in lines:
            if len(line) > 0:
                name = line.split("=")[0]
                params = line.split("=")[1].split(",")
                sysVar = params[0]
                parent = params[1]

                try:
                    path = "templates/objects_" + self.__loader.virtualMemory.kernel + "/colorChangers"
                except:
                    path = "templates/objects_common/colorChangers"

                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.endswith(".asm") or file.endswith(".a26"):
                            f = open(root + "/" + file)
                            text = f.read().replace("#SYSVAR#", sysVar)
                            f.close()

                            command = file.replace("#VARNAME#", name)[:-4]
                            self.objects[parent][command] = text

    def __changeCurrentBankPointer(self, bankNum):
        if type(bankNum) == int:
           bankNum = "bank" + str(int)

        self.objects["currentBank"] = self.objects[bankNum]

    def __pathToListOfObj(self, path):
        return path.replace("\\", "/").replace(self.objRoot + "Game/", "").split("/")

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

                          path = "templates/objects_screenItems/" + typ + "/"
                          for root, dirs, files in os.walk(path):
                              for file in files:
                                  if file.endswith(".asm") or file.endswith("a26"):
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

    def returnAllAboutTheObject(self, command):
        delimiter = "%"
        listOfValidDelimiters = self.__loader.config.getValueByKey("validObjDelimiters").split(" ")
        for symbol in listOfValidDelimiters:
            if symbol in command:
                delimiter = symbol
                break

        listOfObjects = command.split(delimiter)
        if listOfObjects[0] == "game": listOfObjects.pop(0)

        theObject = {}

        theObject["delimiter"] = delimiter
        level = 1
        try:
            pointer = self.objects
            for item in listOfObjects:
                pointer = pointer[item]
                level  += 1

        except Exception as e:
            pass

        if listOfObjects[0] == "currentBank":
           theObject["screen"] = True
        else:
           theObject["screen"] = False

        if level > len(listOfObjects): level = len(listOfObjects)
        theObject["level"] = level

        if theObject["level"] == 2 + theObject["screen"]:
           theObject["exist"] = True
        else:
           theObject["exist"] = False

        sysVar       = None
        found        = False

        if theObject["exist"] == True:
           path = os.getcwd() + "\\templates\\objects\\"
           if theObject["screen"] == True:
              path = os.getcwd() + "\\templates\\objects_screenItems\\"
           else:
              path += "game\\"

           path += "\\".join(listOfObjects) + ".asm"

           if os.path.exists(path):
              theObject["extension"] = "asm"
              found = True
           else:
              path = path[:-3] + "a26"
              if os.path.exists(path):
                  theObject["extension"] = "a26"
                  found = True
              else:
                  path  = None
                  theObject["extension"] = None

                  f = open("templates/objects_" + self.__loader.virtualMemory.kernel + "/listOfColorChangers.txt", "r")
                  lines = f.read().replace("\r", "").split("\n")
                  f.close()

                  commandComp = listOfObjects[-1]

                  for line in lines:
                      if len(line) > 0:
                          name = line.split("=")[0]
                          params = line.split("=")[1].split(",")
                          sysVar = params[0]
                          parent = params[1]

                          for mainPath in [
                              "templates/objects_" + self.__loader.virtualMemory.kernel + "/colorChangers",
                              "templates/objects_" + self.__loader.virtualMemory.kernel + "/game"
                          ]:
                              for root, dirs, files in os.walk(mainPath):
                                  for file in files:
                                      if file.endswith(".asm") or file.endswith(".a26"):
                                          f = open(root + "/" + file)
                                          text = f.read().replace("#SYSVAR#", sysVar)
                                          f.close()

                                          commandC = file.replace("#VARNAME#", name)[:-4]
                                          #print(commandC, commandComp)

                                          if commandC == commandComp:
                                             found                  = True
                                             path                   = root + "/" + file
                                             theObject["extension"] = path[-3:]
                                             break
                                  if found: break
                              if found: break
                      if found: break


           rNum  = None
           endIt = False

           #if found == False: print(command)
           thatWord = ["missile", "player"]
           for w in thatWord:
               if w in path:
                  for n in range(0, 2):
                      rWord = w + str(n)
                      if rWord in command:
                         rNum  = str(n)
                         theObject["replaceNum"] = rNum
                         path  = path.replace(rWord, w + "ß")
                         endIt = True
                         break
                  if endIt: break
               if endIt: break

           theObject["path"]     = path.replace("/", "\\")

           f = open(path, "r")
           theObject["template"] = f.read()
           f.close()

           if "::import" in theObject["template"]:
               linesAgain = theObject["template"].split("\n")
               for lNum in range(0, len(linesAgain)):
                   if linesAgain[lNum].startswith("::import"):
                      fileName = linesAgain[lNum].split("=")[1]
                      if "ß" in fileName: fileName = fileName.replace("ß", rNum)
                      f = open("\\".join(theObject["path"].split("\\")[:-1]) + "\\" + fileName, "r")
                      linesAgain[lNum] = f.read()
                      f.close()

               theObject["template"] = "\n".join(linesAgain)

           if sysVar != None:
              theObject["template"] = theObject["template"].replace("#SYSVAR#", sysVar)

           if rNum != None:
              theObject["template"] = theObject["template"].replace("ß", rNum)

           lines = theObject["template"].replace("\r", "").split("\n")
           try:
               pList = lines[0].split("=")[1].split(",")
           except:
               pList = []

           theObject["params"] = []
           validOnes = ["variable", "string", "stringConst", "number", "data"]

           #print(pList)
           paramNum = -1
           theObject["optionalParamNums"] = []

           for p in pList:
               paramNum += 1
               if p.startswith("{"):
                  p = p[1:-1]
                  theObject["optionalParamNums"].append(paramNum)

               them = p.split("|")
               ok = True
               for item in them:
                   if item not in validOnes:
                       ok = False
                       break
               if ok:
                   theObject["params"].append(p)
               else:
                   theObject["params"].append("variable")

           theObject["sysVars"] = []
           import re

           theObject["ioMethod"] = "read"
           for line in lines:
               if len(line) == 0:
                  continue

               if line[0] in ["*", "#", "!"]:
                  continue

               if theObject["extension"] == "asm":
                   if theObject["ioMethod"] != "write":
                      if len(re.findall(r'ST[AYX][\s\t]+#VAR', line)) > 0: theObject["ioMethod"] = "write"

                   line    = line.replace("\t", " ").split(";")[0].split(" ")
                   newLine = []
                   for item in line:
                       if item != "": newLine.append(item)

                   line = newLine
                   if len(line) > 1:
                      operand = line[1].split(",")[0]
                      var = self.__loader.virtualMemory.getVariableByName2(operand)
                      if var != False:
                         if var.system == True: theObject["sysVars"].append(operand)
               else:
                   theCommand = line.split("(")[0]
                   if theObject["ioMethod"] != "write":
                      for commandKey in self.__loader.syntaxList.keys():
                          if theCommand == commandKey or theCommand in self.__loader.syntaxList[commandKey].alias:
                             commandObj = self.__loader.syntaxList[commandKey]
                             if commandObj.does == "write": theObject["ioMethod"] = commandObj.does
                             break
                   try:
                      ppp     = line.split("(")[1].split(")")[0].split(",")
                      for pNum in range(0, len(ppp)):
                          ppp[pNum] = ppp[pNum].strip()
                          var = self.__loader.virtualMemory.getVariableByName2(ppp[pNum])
                          if var != False:
                             if var.system == True: theObject["sysVars"].append(ppp[pNum])

                   except Exception as e:
                      # print(str(e))
                      pass
           #print(theObject["sysVars"])
           theObject["paramsWithSettings"] = []

           for num in range(0, len(theObject["params"])):
               theObject["paramsWithSettings"].append({})
               last = theObject["paramsWithSettings"][-1]
               last["param"]    = theObject["params"][num]
               lineOfVar        = lines[num + 1].split("=")[1].split(",")
               last["replacer"] = lineOfVar[0]

               if pList[num].startswith("{"):
                   last["mustHave"] = False
               else:
                   last["mustHave"] = True

               if len(lineOfVar) > 1:
                  if last["param"] in ["data", "{data}"]:
                     last["folder"]    = lineOfVar[1]
                  else:
                     if len(lineOfVar) > 1:
                        last["converter"] = lineOfVar[1]

           nextIndex = len(theObject["params"]) + 1
           for index in range(nextIndex, len(lines)):
               if len(lines[index]) == 0: break
               if lines[index][0] not in ("*", "#"): break
               #print(lines[index].split("=")[0])
               try:
                   name = lines[index].split("=")[0].split(" ")[1]
                   theObject[name] = []
                   params = lines[index].split("=")[1].split(",")
                   theObject[name] = params
               except Exception as e:
                   continue

        else:
           return(theObject)

        #if "loadAndUse" in theObject.keys(): print(theObject["loadAndUse"])

        ##or key in theObject:
        #    print(key + ":", theObject[key])
        if "addManuallyToSysVars" in theObject.keys():
            for var in theObject["addManuallyToSysVars"]: theObject["sysVars"].append(var)
            del theObject["addManuallyToSysVars"]
        return theObject

    def createFakeCommandOnObjectProcess(self, command):
        object = self.returnAllAboutTheObject(command)

        if object["exist"]:
            name = command.split(object["delimiter"])[-1]
            data = []
            data.append("[]")
            data.append("[common]")
            data.append("command")
            data.append("None")
            if len(object["params"]) > 0:
               data.append("brackets")
            else:
               data.append("None")
            data.append("[]")
            data.append("[" + " ".join(object["params"]) + "]")
            data.append(object["ioMethod"])
            data.append("None")
            data.append("False")

            #print(Command(self.__loader, name, ",".join(data)).params)
            return Command(self.__loader, name, ",".join(data))
        else:
            return None

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

        delimiter = "%"
        listOfValidDelimiters = self.__loader.config.getValueByKey("validObjDelimiters").split(" ")
        for symbol in listOfValidDelimiters:
            if symbol in name:
               delimiter = symbol
               break

        name = name.split(delimiter)
        if name[0] == "game": name.pop(0)

        pointer = self.objects
        try:
            #if len(name) == 1: pointer = self.objects[name[0]]
            for word in name:
                if word in pointer.keys():
                   pointer = pointer[word]

            return(list(pointer.keys()))
        except:
            return []

    def returnObjListLike(self, lvl1Obj, lvl2Obj, lvl3Obj, lvlAskedFor):
        items = self.returnAllCombinations()
        returnThese = []

        for item in items:
            if (item[0][0].startswith(lvl1Obj) or lvl1Obj == "") and \
               (item[1][0].startswith(lvl2Obj) or lvl2Obj == "") and \
               (item[2][0].startswith(lvl3Obj) or lvl3Obj == ""):

               if lvlAskedFor >  1 and item[0][0] == "": continue
               if lvlAskedFor == 3 and item[1][0] == "": continue
               if item[lvlAskedFor-1][0] != "": returnThese.append(item[lvlAskedFor - 1])

        return returnThese

    def returnAllCombinations(self):
        items = []

        for lvl1 in self.objects.keys():
            if lvl1.startswith("bank"): continue

            found = False
            for lvl2 in self.objects[lvl1].keys():
                if "(" in lvl2:
                    lvl2 = lvl2.split("(")[0]
                    items.append([[lvl1, "object"], [lvl2, "process"], ["", ""]])
                    found = True

                else:
                    if type(self.objects[lvl1][lvl2]) == str:
                       items.append([[lvl1, "object"], [lvl2, "process"], ["", ""]])
                       found = True
                    else:
                       for lvl3 in self.objects[lvl1][lvl2].keys():
                           lvl3 = lvl3.split("(")[0]
                           items.append([[lvl1, "object"], [lvl2, "object"], [lvl3, "process"]])
                           found = True

            if found == False: items.append([[lvl1, "object"], ["", ""], ["", ""]])

        return items


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
           try:
               base = self.objects[data[0]]
           except:
               return []
        elif len(data) == 3:
           try:
               base = self.objects[data[0]][data[1]]
           except:
               return []
        else:
           return []

        for key in base.keys():
            if type(base[key]) != dict:
                if key.split("(")[0] == data[-1]:
                   return key.split("(")[1][:-1].split(",")

        return []

    def returnObjectOrProcess(self, name):
        if name == "game": return "object"

        for lvl1 in self.objects.keys():
            if name.upper() == lvl1.upper(): return "object"
            for lvl2 in self.objects[lvl1].keys():
                if name.upper() == lvl2.split("(")[0].upper() or name.upper() == lvl2.upper():
                   if type(self.objects[lvl1][lvl2]) == dict:
                      return "object"
                   else:
                      return "process"
                if type(self.objects[lvl1][lvl2]) == dict:
                   for lvl3 in self.objects[lvl1][lvl2].keys():
                       if lvl3.upper().split("(")[0] == name.upper() or name.upper() == lvl3.upper(): return "process"

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