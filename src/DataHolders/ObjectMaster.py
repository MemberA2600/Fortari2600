import os
from Command  import Command
from Compiler import Compiler
from copy import deepcopy

class ObjectMaster:

    def __init__(self, loader):
        self.__loader   = loader
        self.__compiler = Compiler(self.__loader, "common", "dummy", None)
        self.__listOfSourceTXTs = ["colorChangers", "simpleSetters", "movements"]
        self.__noGetter = ["movements"]

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

                            if firstLine[0] in ["*", "#"] and len(firstLine) > 1:
                                listOfParams = firstLine.split("=")[1]
                                key = name + "(" + listOfParams + ")"
                            else:
                                key = name
                            objRoot[key] = text

        f = open(self.objRoot + "get#VARNAME#.asm")
        getTemplate = f.read()
        f.close()

        for txtName in self.__listOfSourceTXTs:

            f = open(self.objRoot + "listOf" + txtName[0].upper() + txtName[1:] + ".txt", "r")
            lines = f.read().replace("\r", "").split("\n")
            f.close()

            for line in lines:
                if len(line) > 0:
                    name = line.split("=")[0]
                    params = line.split("=")[1].split(",")
                    sysVar = params[0].replace(" ", ",")
                    parent = params[1]

                    try:
                        path = "templates/objects_" + self.__loader.virtualMemory.kernel + "/"+ txtName
                    except:
                        path = "templates/objects_common/" + txtName

                    for root, dirs, files in os.walk(path):
                        for file in files:
                            if file.endswith(".asm") or file.endswith(".a26"):
                                f = open(root + "/" + file)
                                text = f.read().replace("#SYSVAR#", sysVar)
                                f.close()

                                command = file.replace("#VARNAME#", name)[:-4]
                                self.objects[parent][command] = text

                                getCommandName = "get" + name
                                if getCommandName in self.objects[parent]:
                                   continue

                                if txtName in self.__noGetter: continue

                                text = getTemplate.replace("#SYSVAR#", sysVar).replace("#PARENT#", parent)

                                #if "color" in txtName:
                                #    text = text.replace("#COLORANNOTATION#", "\t; &COLOR")
                                #else:
                                #    text = text.replace("#COLORANNOTATION#", "")
                                #print(txtName, file+"\n", text)
                                self.objects[parent][getCommandName] = text

        f = open(self.objRoot + "detectPointBasedCollisionOn#VARNAME#.a26")
        detectTemplate = f.read()
        f.close()

        f = open(self.objRoot + "detectPointBasedCollisionOnPlayfield.a26")
        detectPFTemplate = f.read()
        f.close()

        f = open(self.objRoot + "itemsOfDetection.txt")
        items = f.read().replace("\r", "").split("\n")
        f.close()

        itemList = []
        for itemLine in items:
            lineVar = itemLine.split("=")[0]
            itemList.append(lineVar)

        for item1 in items:
            for item2 in items:
                if item1 == item2:                       continue
                if "=" not in item1 or "=" not in item2: continue

                parent        = item1.split("=")[0]
                varName       = item2.split("=")[0]

                parentVars    = item1.split("=")[1].split(",")
                varNameVars   = item1.split("=")[1].split(",")

                nameOfcommand = "detectPointBasedCollisionOn" + varName[0].upper() + varName[1:]

                sysVars       = self.createSysVarsString(parentVars, varNameVars)

                text        = detectTemplate.replace("#SYSVAR#", sysVars)
                sysVarsList = sysVars.split(",")

                """ 
                for varNum in range(0, 4):
                    sysName = "#SYSVAR" + str(varNum + 1) + "#"
                    text    = text.replace(sysName, sysVarsList[varNum])
                """

                #itemList.remove(parent)
                #itemList.remove(varName)

                text = self.removeNotNeeded(itemList, text, parent, varName)
                self.objects[parent][nameOfcommand] = text

                if "detectPointBasedCollisionOnPlayfield" not in self.objects[parent].keys():
                    sysVars = self.createSysVarsString(parentVars, [])

                    text = detectPFTemplate.replace("#SYSVAR#", sysVars)
                    text = self.removeNotNeeded(itemList, text, parent, "")

                    sysVarsList = sysVars.split(",")

                    """
                    for varNum in range(0, 4):
                        sysName = "#SYSVAR" + str(varNum + 1) + "#"
                        text = text.replace(sysName, sysVarsList[varNum])
                    """

                    self.objects[parent]["detectPointBasedCollisionOnPlayfield"] = text

    def createSysVarsString(self, list1, list2):
        newList = []

        for item in list1:
            newList.append(item)

        for item in list2:
            newList.append(item)

        return ",".join(newList)

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

    def removeNotNeeded(self, itemsList, text, parent, colliding):
        import re

        tags = []
        for word in itemsList:
            openTag   = "###PARENT-"  + word[0].upper() + word[1:].lower()
            tags.append(openTag)

            openTag = "###COLLIDING-" + word[0].upper() + word[1:].lower()
            tags.append(openTag)

        openTag = "###PARENT-"    + parent[0].upper()    + parent[1:].lower()
        tags.remove(openTag)

        if colliding != "":
           openTag = "###COLLIDING-" + colliding[0].upper() + colliding[1:].lower()
           tags.remove(openTag)

        for word in tags:
            text = re.sub(rf'{word}.+{word+"-End"}', "", text, flags=re.DOTALL)

        return text

    def returnAllAboutTheObject(self, command):
        #print("#1")
        delimiter = "%"
        listOfValidDelimiters = self.__loader.config.getValueByKey("validObjDelimiters").split(" ")
        for symbol in listOfValidDelimiters:
            if symbol in command:
                delimiter = symbol
                break

        listOfObjects = command.split(delimiter)
        if listOfObjects[0] == "game": listOfObjects.pop(0)

        theObject = {}

        theObject["name"]      = command
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
        itemList     = []
        itemVars     = []

        if theObject["exist"] == True:
           path = os.getcwd() + "\\templates\\objects_common\\"
           if theObject["screen"] == True:
              path = os.getcwd() + "\\templates\\objects_screenItems\\"
           else:
              path += "game\\"

           path += "\\".join(listOfObjects) + ".asm"

           #print("!!!!!", path)

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

                  if listOfObjects[-1].startswith("detectPointBasedCollisionOn"):
                     if listOfObjects[-1].endswith("Playfield"):
                         parent     = listOfObjects[0]
                         varName    = "playfield"

                         f = open(self.objRoot + "itemsOfDetection.txt")
                         items = f.read().replace("\r", "").split("\n")
                         f.close()

                         for itemLine in items:
                             lineVar = itemLine.split("=")[0]
                             #if lineOfVar != parent:
                             itemList.append(lineVar)

                         itemVars = [parent, ""]

                         path = self.objRoot + "detectPointBasedCollisionOnPlayfield.a26"
                         found = True

                         parentVars = []

                         for line in items:
                             item     = line.split("=")[0]

                             if   item        == parent:
                                  parentVars  =  line.split("=")[1].split(",")
                                  break

                         theObject["extension"] = "a26"
                         sysVar    = self.createSysVarsString(parentVars, [])

                     else:
                         parent     = listOfObjects[0]
                         varName    = listOfObjects[-1].replace("detectPointBasedCollisionOn", "").lower()

                         f = open(self.objRoot + "itemsOfDetection.txt")
                         items = f.read().replace("\r", "").split("\n")
                         f.close()

                         for itemLine in items:
                             lineVar = itemLine.split("=")[0]
                             #if lineOfVar not in [parent, varName]:
                             itemList.append(lineVar)

                         path  = self.objRoot + "detectPointBasedCollisionOn#VARNAME#.a26"
                         found = True

                         itemVars = [parent, varName]

                         parentVars  = []
                         varNameVars = []

                         for line in items:
                             item     = line.split("=")[0]

                             if   item        == parent:
                                  parentVars  =  line.split("=")[1].split(",")
                             elif item        ==  varName:
                                  varNameVars =  line.split("=")[1].split(",")

                             if parentVars != [] and varNameVars != []: break

                         theObject["extension"] = "a26"
                         sysVar = self.createSysVarsString(parentVars, varNameVars)

                  else:
                      paths = []
                      for txtName in self.__listOfSourceTXTs:
                          #path.append("templates/objects_" + self.__loader.virtualMemory.kernel + "/listOf" + txtName + ".txt")

                          xxxPath = "templates/objects_" + self.__loader.virtualMemory.kernel + "/listOf"+txtName[0].upper() + txtName[1:]+".txt"
                          f = open(xxxPath, "r")
                          lines = f.read().replace("\r", "").split("\n")
                          f.close()

                          commandComp = listOfObjects[-1]
                          parentComp  = listOfObjects[0]

                          for line in lines:
                              if len(line) > 0:
                                  name = line.split("=")[0]
                                  params = line.split("=")[1].split(",")
                                  parent = params[1]

                                  if txtName == self.__listOfSourceTXTs[-1]:
                                      paths =[
                                          "templates/objects_" + self.__loader.virtualMemory.kernel + "/" + txtName,
                                          "templates/objects_" + self.__loader.virtualMemory.kernel + "/game",
                                          "templates/objects_" + self.__loader.virtualMemory.kernel
                                      ]
                                  else:
                                      paths = ["templates/objects_" + self.__loader.virtualMemory.kernel + "/" + txtName]

                                  for mainPath in paths:
                                      for root, dirs, files in os.walk(mainPath):
                                          for file in files:
                                              if file.endswith(".asm") or file.endswith(".a26"):
                                                  #f = open(root + "/" + file)
                                                  #text = f.read().replace("#SYSVAR#", sysVar).replace("#PARENT#", parent)
                                                  #f.close()
                                                  commandC = file.replace("#VARNAME#", name)[:-4]
                                                  #print(commandC, commandComp)

                                                  #print(mainPath)
                                                  #if commandC == commandComp: print(parent, parentComp)
                                                  if commandC == commandComp and parent == parentComp:
                                                     #print(commandC, parent, name)

                                                     #print(file, name, commandC)
                                                     if "#VARNAME#" in file and name not in commandC: continue
                                                     #print(parent, file, commandC, params[0], line, txtName, mainPath, xxxPath)
                                                     found                  = True
                                                     path                   = root + "/" + file
                                                     theObject["extension"] = path[-3:]
                                                     sysVar = params[0].replace(" ", ",")
                                                     #print(sysVar)

                                                     break
                                              if found: break
                                          if found: break
                                      if found: break
                              if found: break
                          if found: break

           rNum  = None
           endIt = False

           #if found == False: print(command)
           thatWord = ["missile", "player"]
           for w in thatWord:
               if path != None:
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

           #print(path)
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

           #print(sysVar)
           if sysVar != None:
              theObject["template"] = theObject["template"].replace("#SYSVAR#", sysVar)
              for sysNum in range(1, 20):
                  sysText = "#SYSVAR" + str(sysNum) + "#"
                  sysVars = sysVar.split(",")

                  if sysText in theObject["template"]:
                     theObject["template"] = theObject["template"].replace(sysText, sysVars[sysNum-1])
                  else:
                     break

           theObject["template"] = theObject["template"].replace("#PARENT#", listOfObjects[0])
           if itemList != []:
               theObject["template"] = self.removeNotNeeded(itemList, theObject["template"], itemVars[0], itemVars[1])

           if rNum != None:
              theObject["template"] = theObject["template"].replace("ß", rNum)

           lines = theObject["template"].replace("\r", "").split("\n")
           pList = []
           if "params" in lines[0].split("=")[0]:
               try:
                   pList = lines[0].split("=")[1].split(",")
               except:
                   pList = []


           theObject["params"] = []
           validOnes = ["variable", "string", "stringConst", "number", "data", "register"]

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
               #print(them)
               for item in them:
                   if item not in validOnes:
                       ok = False
                       break
               if ok:
                   theObject["params"].append(p)
               else:
                   theObject["params"].append("variable")

           #print(theObject["params"])

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
               #print(lines)
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
                     if len(lineOfVar) > 2:
                        last["restriction"] = lineOfVar[2]

           nextIndex = len(theObject["params"]) + 1
           for index in range(nextIndex, len(lines)):
               if len(lines[index]) == 0: break
               if lines[index][0] not in ("*", "#"): break
               #print(lines[index].split("="))
               try:
                   name = lines[index].split("=")[0].split(" ")[1]
                   theObject[name] = []
                   params = lines[index].split("=")[1].split(",")
                   theObject[name] = params
                   #print(name, theObject[name])
               except Exception as e:
                   #print(str(e), lines[index])
                   continue

        else:
           return(theObject)

        #if "loadAndUse" in theObject.keys(): print(theObject["loadAndUse"])

        #print(theObject["template"])

        if "addManuallyToSysVars" in theObject.keys():
            for var in theObject["addManuallyToSysVars"]: theObject["sysVars"].append(var)
            del theObject["addManuallyToSysVars"]

        #print(theObject["sysVars"])

        #for key in theObject:
        #    print(key + ":", theObject[key])

        #print("#2")
        return theObject

    def createFakeCommandOnObjectProcess(self, command):
        if type(command) == str:
           object = self.returnAllAboutTheObject(command)
        else:
           object = command

        if object["exist"]:
            try:
                name = command.split(object["delimiter"])[-1]
            except:
                name = object["name"]

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

            #print(object["optionalParamNums"])
            params = deepcopy(object["params"])
            for pNum in object["optionalParamNums"]:
                params[pNum] = "{" + params[pNum] + "}"

            data.append("[" + " ".join(params) + "]")
            data.append(object["ioMethod"])
            data.append("None")
            data.append("False")
            data.append("0")
            data.append("True")

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