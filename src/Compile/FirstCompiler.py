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

        writable, readOnly, all, nonSystem = self.__loader.virtualMemory.returnVariablesForBank(self.__currentBank)
        self.__variablesOfBank = {
            "writable"  : writable,
            "readOnly"  : readOnly,
            "all"       : all,
            "nonSystem" : nonSystem
        }

        self.numberRegexes    = {"dec": r'^\d{1,3}$',
                                 "bin": r'^[b|%][0-1]{1,8}$',
                                 "hex": r'^[$|z|h][0-9a-fA-F]{1,2}$'}

        self.__constants      = self.__editorBigFrame.collectConstantsFromSections(self.__currentBank)
        self.__currentSection = section
        self.__virtualMemory  = self.__loader.virtualMemory
        self.__config         = self.__loader.config
        self.__dictionaries   = self.__loader.dictionaries
        self.__startLine      = startLine
        self.__registers,     \
        self.__opcodes        = self.__loader.io.loadRegOpCodes()

        self.__writable,\
        self.__readOnly,\
        self.__all,\
        self.__nonSystem      = self.__virtualMemory.returnVariablesForBank(self.__currentBank)

        self.__validMemoryAddresses = []

        for num in range(0, 255):
            origNum = num
            num = hex(num).replace("0x", "")
            if len(num) == 1: num = "0" + num

            if origNum > 127:
               self.__validMemoryAddresses.append("$" + num.upper())

            self.__validMemoryAddresses.append("$F0" + num.upper())

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

               txt = "\t"+"\t".join(datas)

               self.checkASMCode(txt, line)
               if self.__error: line["compiled"] = txt

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

        self.checkASMCode(template, line)
        if self.__error: line["compiled"] = template

    def checkASMCode(self, template, lineStructure):
        lines = template.split("\n")

        for line in lines:
            delimiterPoz = self.__editorBigFrame.getFirstValidDelimiterPoz(line)
            line = line[:delimiterPoz]
            #'$79': {'opcode': 'ADC', 'format': 'aaaa,y', 'bytes': 3},
            line = line.replace("\r", "").replace("\t", " ").split(" ")
            command = ""
            value   = ""

            for item in line:
                if item != "":
                   if command == "":
                      command = item
                   else:
                      value = item
                      break

            foundCommand = False
            for item in self.__opcodes:
                lineSettings = self.__opcodes[item]
                if lineSettings["opcode"].upper() == command.upper():
                   if value in self.__noneList:
                       if lineSettings["bytes"] == 1:
                          foundCommand = True
                          break
                       else: continue

                   if self.checkIfASMhasrightOperand(lineSettings, value) == False: continue

                   beforeComma = value.split(",")[0]

                   operandTyp  = self.getTypeOfOperand(beforeComma)
                   operandSize = self.sizeOfNumber(beforeComma, operandTyp)

                   numberValue = ""
                   numeric = value

                   if operandTyp in ("variable", "register"):
                      numeric = self.getAddress(value)

                   if value.startswith("#>") or value.startswith("#<"):
                       if value[1] == ">":
                           value = self.__editorBigFrame.convertStringNumToNumber(numeric[1:3])
                       else:
                           value = self.__editorBigFrame.convertStringNumToNumber(numeric[3:5])
                   else:
                       numberValue = self.__editorBigFrame.convertStringNumToNumber(numeric.replace("#", ""))

                   hexa = ""
                   mode = ""

                   if operandTyp in ("address", "register"):
                      hexa = hex(numberValue).replace("0x", "")
                      if len(hexa) % 2 != 0: hexa = "0" + hexa
                      hexa = "$" + hexa

                      if hexa not in self.__registers.keys() and hexa not in self.__validMemoryAddresses:
                         self.addToErrorList(lineStructure["lineNum"],
                                             self.prepareErrorASM("compilerErrorASMRegisterAddr",
                                                                   command, value,
                                                                   lineStructure["lineNum"]))
                      if operandSize == 2:
                         high = hexa[1:3]
                         low  = hexa[3:5]

                         if high != "F0":
                            if high == "02":
                               riot = {
                                   "80": "both",
                                   "81": "write",
                                   "82": "write",
                                   "83": "none",
                                   "84": "read",
                                   "94": "write",
                                   "95": "write",
                                   "96": "write",
                                   "97": "write"
                               }

                               mode = riot[low]
                            else:
                               mode = "read"
                         else:
                            if int(low) < 80:
                               mode = "write"
                            else:
                               mode = "read"
                      else:
                          if int(hexa[1:]) > 29:
                             mode = "read"
                          else:
                             mode = "write"

                   elif operandTyp == "variable":
                       pass


                   foundCommand = True
                   break

            if foundCommand == False:
                self.addToErrorList(lineStructure["lineNum"], self.prepareErrorASM("compilerErrorASMOpCode",
                                                     command, value, lineStructure["lineNum"]))

            if foundCommand == True:
               try:
                   print(command, value, operandTyp, operandSize, item)
               except:
                   print(command, value)
            else:
               print(self.errorList)

    def checkIfASMhasrightOperand(self, lineSettings, value):
        import re

        beforeCommaValue    = value.split(",")[0]
        try:
            afterCommaValue = value.split(",")[1]
        except:
            afterCommaValue = ""

        beforeCommaFormat    = lineSettings["format"].split(",")[0]
        try:
            afterCommaFormat = lineSettings["format"].split(",")[1]
        except:
            afterCommaFormat = ""

        if afterCommaFormat != afterCommaValue: return False
        beforeCommaFormat = beforeCommaFormat.upper()

        onlyBody = beforeCommaValue.replace("#", "").replace(">", "").replace("<", "")
        for reg in self.__registers:
            if self.__registers[reg] == onlyBody.upper():
               beforeCommaValue = beforeCommaValue.replace(onlyBody, "") + reg

        for var in self.__variablesOfBank["all"]:
            if var.upper() == onlyBody.upper():
               addr = self.__virtualMemory.getAddressOnVariableIsStored(var, "bank1")
               if addr == False:
                  addr = self.__virtualMemory.getAddressOnVariableIsStored(var, self.__currentBank)
               beforeCommaValue = beforeCommaValue.replace(onlyBody, "") + addr

        allA = re.sub(r'[0-9a-fA-F]', "A", beforeCommaValue).replace("$", "")

        if beforeCommaFormat != allA: return False

        numOfBytesFormat = beforeCommaFormat.count("A") // 2
        if value.startswith("#"): numOfBytesFormat = 1

        return self.sizeOfNumber(value, "") == numOfBytesFormat

    def sizeOfNumber(self, value, typ):
        makeItHalf = 1

        if typ == "":
           typ =  self.getTypeOfOperand(value)

        if typ in ["variable", "register"]:

           value = self.getAddress(value)
           if value == False: return 0

        else:
            if value.startswith("#"):
               return 1

        numberValue = self.__editorBigFrame.convertStringNumToNumber(value)
        if numberValue > 255:
           return 2 // makeItHalf
        else:
           return 1 // makeItHalf

    def getAddress(self, value):
        body = value.replace("#", "").replace(">", "").replace("<", "")

        address = self.__loader.virtualMemory.getAddressOnVariableIsStored(body, "bank1")
        if address == False:
            address = self.__loader.virtualMemory.getAddressOnVariableIsStored(body, self.__currentBank)

        if address == False:
            for reg in self.__registers:
                if body.upper() == self.__registers[reg].upper():
                    address = reg

        return address

    def getTypeOfOperand(self, value):
        import re

        numberFormat = None
        for key in self.numberRegexes:
            if len(re.findall(self.numberRegexes[key], value)) > 0:
               if "#" in value: return "constant"
               else:            return "address"

        if numberFormat == None:
           if value.startswith("#"): value = value[1:]

           for key in self.__variablesOfBank:
               if value in self.__variablesOfBank[key]:
                  return "variable"
           for key in self.__registers:
               if value.upper() in self.__registers[key]:
                  return "register"

        return False

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

    def prepareErrorASM(self, text, opcode, operand, lineNum):
        self.__error = True
        return (self.__dictionaries.getWordFromCurrentLanguage("compilerErrorASM") + " " +\
               self.__dictionaries.getWordFromCurrentLanguage(text)).replace("#LINENUM#", str(lineNum))\
                                                                    .replace("#OPCODE#" , str(opcode))\
                                                                    .replace("#OPERAND#", str(operand))

    def isCommandInLineThat(self, line, command):
        if line["command"][0] == command or command in self.__loader.syntaxList[command].alias:
           return True
        return False
