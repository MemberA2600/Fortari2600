from datetime import datetime

class FirstCompiler:

    def __init__(self, loader, editorBigFrame, text, addComments, mode, bank, section, startLine):

        self.__loader         = loader
        self.__editorBigFrame = editorBigFrame
        self.__text           = text.replace("\t", " ").split("\n")
        self.__magicNumber    = str(datetime.now()).replace("-", "").replace(".", "")
        self.__counter        = 0
        self.__addComments    = addComments
        self.__loadCommandASM = self.__loader.io.loadCommandASM
        self.errorList        = {}
        self.__currentBank    = bank

        self.__constants      = self.__editorBigFrame.collectConstantsFromSections(self.__currentBank)
        self.__currentSection = section
        self.__virtualMemory  = self.__loader.virtualMemory
        self.__config         = self.__loader.config
        self.__dictionaries   = self.__loader.dictionaries
        self.__startLine      = startLine

        self.__writable,\
        self.__readOnly,\
        self.__all,\
        self.__nonSystem      = self.__virtualMemory.returnVariablesForBank(self.__currentBank)

        linesFeteched = []
        self.__noneList = ["", "None", None, []]

        for lineNum in range(0, len(self.__text)):
            line = self.__text[lineNum]

            lineStruct = self.__editorBigFrame.getLineStructure(lineNum, self.__text, True)

            if lineStruct["command"][0] in self.__noneList: continue

            lineStruct["fullLine"]       = line
            lineStruct["labelsBefore"]   = []
            lineStruct["labelsAfter"]    = []
            lineStruct["commentsBefore"] = ""
            lineStruct["compiled"]       = ""

            if addComments:
               lineStruct["commentsBefore"] = "***\t" + line[:self.__editorBigFrame.getFirstValidDelimiterPoz(line)]

            linesFeteched.append(lineStruct)

        self.compileBuild(linesFeteched, mode)

    def compileBuild(self, linesFeteched, mode):

        for line in linesFeteched:
            self.__error = False
            if self.isCommandInLineThat(line, "asm"):
               datas = []
               for num in range(1, 3):
                   if line["param#" + str(num)][0] not in self.__noneList:
                      datas.append(line["param#" + str(num)][0][1:-1])

               line["compiled"] = "\t"+"\t".join(datas)
            elif self.isCommandInLineThat(line, "add"):
                params = self.getParamsWithTypesAndCheckSyntax(line)

                if params["param#1"][1] == "number":
                   if self.isItZero(params["param#1"][0]): continue

                if params["param#2"][1] == "number":
                   if self.isItZero(params["param#2"][0]): continue

                if "param#3" not in params.keys():
                   params["param#3"] = params["param#1"]

                if self.__error == False: self.createASMTextFromLine(line, "add", params)
                #print(params)

        textToReturn = ""
        for line in linesFeteched:
            for word in ["commentsBefore", "labelsBefore", "compiled", "labelsAfter"]:
                if line[word] not in self.__noneList:
                    if type(line[word]) == list:
                        line[word] = "\n".join(line[word])
                    if   mode == "forBuild":
                         textToReturn += line[word] + "\n"
                    elif mode == "forEditor":
                         textLines = line[word].split("\n")
                         for tLine in textLines:
                            if tLine in self.__noneList or tLine == "\n": continue
                            if tLine.startswith("*"):
                               textToReturn += tLine + "\n"
                            else:
                               textToReturn += "\tasm(\"" + tLine + "\")\n"

            if line["comment"][0] not in self.__noneList:
                textToReturn = textToReturn[:-1] + "\t; " + line["comment"][0] + "\n"

        self.result = textToReturn

    def isItZero(self, val):
        if val.startswith("#"): val = val[1:]

        if   val.startswith("%"):
             val = int(val.replace("%", "0b"), 2)
        elif val.startswith("$"):
             val = int(val.replace("$", "0x"), 16)
        else:
             val = int(val)

        if val == 0: return True
        return False

    def createASMTextFromLine(self, line, command, params):
        template = self.__loader.io.loadCommandASM(command)
        for num in range(1, 4):
            name    = "param#" + str(num)
            varName = "#VAR0" + str(num) + "#"
            template = template.replace(varName, params[name][0])

        """
        if line["comment"][0] not in self.__noneList:
           template = template.replace("#COMMENT#", line["comment"][0])
           line["comment"][0] = None

        """
        line["compiled"] = template

    def getParamsWithTypesAndCheckSyntax(self, line):
        params = {}

        command = None
        for commandName in self.__loader.syntaxList.keys():
            if self.isCommandInLineThat(line, commandName):
               command = self.__loader.syntaxList[commandName]
               break

        if command == None:
           self.addToErrorList(line["lineNum"], self.prepareError("compilerErrorCommand", "",
                                                 line["command"][0], "",
                                                 str(line["lineNum"] + self.__startLine)))
        for num in range(1, 4):
            curParam = line["param#"+str(num)][0]
            if curParam not in self.__noneList:
               #curParam = self.formatParam(curParam, line["command"][0], line["lineNum"])
               paramType = command.params[num-1]
               mustHave  = True
               if paramType.startswith("{"):
                  mustHave = False
                  paramType = paramType[1:-1]

               ioMethod = command.does

               if self.__loader.syntaxList[line["command"][0]].flexSave == True and num == 1 and \
                  line["param#3"][0] in self.__noneList:
                  paramType = "variable"
                  ioMethod  = "write"

               paramTypes = paramType.split("|")

               if self.__editorBigFrame.doesItWriteInParam(line, "param#"+str(num)) == False:
                   ioMethod = "read"

               foundIt               = False
               param                 = None
               paramTypeAndDimension = None
               for param in paramTypes:
                   foundIt, paramTypeAndDimension = self.__editorBigFrame.checkIfParamIsOK(param, curParam,
                                                                                           ioMethod, None,
                                                                                           "dummy", mustHave, "param#"+str(num),
                                                                                           line)
                   #print(curParam, param, foundIt)
                   if foundIt == True:
                      break

               if foundIt == False:
                  for param in paramTypes:
                      missinWords = {
                          "stringConst": "Const",
                          "variable"   : "Variable",
                          "number"     : "Number",
                          "string"     : "String",
                          "subroutine" : "Sub",
                          "array"      : "Array"
                      }

                      if param == "statement":
                         if line["command"][0] == "calc" or line["command"][0] in self.__loader.syntaxList["calc"].alias:
                            missing = "StatementCalc"
                        # elif here should be the speciel statement type for the screen text display!
                         else:
                            missing = "StatementComp"

                      else:
                          missing = missinWords[param]

                      self.addToErrorList(line["lineNum"],    self.prepareError("compilerErrorParam", "param#" + str(num),
                                                              line["param#" + str(num)][0], "",
                                                              str(line["lineNum"] + self.__startLine)) +
                                            " " + self.__dictionaries.getWordFromCurrentLanguage("compilerError" + missing))

               else:
                   if   paramTypeAndDimension[0] == "number":
                        curParam = "#" + curParam
                   elif paramTypeAndDimension[0] == "stringConst":
                        curParam = "#" + self.getConstValue(curParam)
                        paramTypeAndDimension[0] = "number"

                   params["param#" + str(num)] = [curParam, paramTypeAndDimension[0]]

        listOfErrors = self.__editorBigFrame.callLineTintingFromFirstCompiler(line["fullLine"], line["lineNum"], self.__text)
        errorNames = {"noEndFound": {"#COMMAND#": line["command"][0],
                                     "#END#": "end-" + line["command"][0].split("-")[0]},
                      "noStartFound": {"#COMMAND#": line["command"][0]},
                      "noSelectForCase": {"#COMMAND#": line["command"][0]},
                      "noEndForCase": {"#COMMAND#": line["command"][0]},
                      "noSelectForDefault": "noSelectForCase",
                      "noEndForDefault": "noEndForCase",
                      "noCaseForDefault": {"#COMMAND#": line["command"][0]},
                      "noDoForCommand": "noEndFound",
                      "noEndForDo": "noStartFound",
                      "missingOpeningBracket": {},
                      "missingClosingBracket": {},
                      "commandDoesNotNeedBrackets": {},
                      "sectionNotAllowed": {"#SECTIONS#": ", ".join(self.__loader.syntaxList[line["command"][0]].sectionsAllowed)},
                      "levelNotAllowed": {"#LEVEL#": str(self.__loader.syntaxList[line["command"][0]].levelAllowed)},
                      "paramNotNeeded": {},
                      "iteralError": {}
                      }

        for item in listOfErrors:
            if item[1] not in errorNames.keys():
                continue

            while type(errorNames[item[1]]) == str:
                item[1] = errorNames[item[1]]

            secondPart = self.__dictionaries.getWordFromCurrentLanguage(item[1])
            for key in errorNames[item[1]]:
                secondPart = secondPart.replace(key, errorNames[item[1]][key])

            self.addToErrorList(line["lineNum"], self.prepareError("compilerErrorCommand", "",
                                                                   line["command"][0], "",
                                                                   str(line["lineNum"] + self.__startLine))
                                + " " + secondPart)

        return(params)

    def getConstValue(self, key):
        if key in self.__constants.keys():
           return str(self.__constants[key]["value"])

        for that in self.__constants.keys():

            if key in self.__constants[that]["alias"]:
               return str(self.__constants[that]["value"])

    def addToErrorList(self, lineNum, text):
        if self.__currentBank not in self.errorList.keys():
           self.errorList[self.__currentBank] = {}

        if self.__currentSection not in self.errorList[self.__currentBank].keys():
           self.errorList[self.__currentBank][self.__currentSection] = {}

        if lineNum not in self.errorList[self.__currentBank][self.__currentSection].keys():
           self.errorList[self.__currentBank][self.__currentSection][lineNum] = []

        self.errorList[self.__currentBank][self.__currentSection][lineNum].append(text)

    def prepareError(self, text, param, val, var, lineNum):
        self.__error = True
        return self.__dictionaries.getWordFromCurrentLanguage(text)\
                    .replace("#VAL#", val).replace("#VAR#", var).replace("#BANK#", self.__currentBank)\
                    .replace("#SECTION#", self.__currentSection).replace("#LINENUM#", str(lineNum)).replace("#PARAM#", param).replace("  ", " ")



    def isCommandInLineThat(self, line, command):
        if line["command"][0] == command or command in self.__loader.syntaxList[command].alias:
           return True
        return False

