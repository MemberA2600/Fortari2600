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
        self.__objectMaster   = self.__loader.virtualMemory.objectMaster

        from Compiler import Compiler
        self.__mainCompiler   = Compiler(self.__loader, self.__loader.virtualMemory.kernel, "dummy", None)

        self.opcodesIOsMoreOtherThanRead = {
             "SAX": "write",
             "DCP": "both",
             "ISB": "both",
             "DEC": "both",
             "INC": "both",
             "STA": "write"
        }

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
               if self.__error == False: line["compiled"] = txt

            elif self.isCommandInLineThat(line, "add"):
                params = self.getParamsWithTypesAndCheckSyntax(line)

                if "param#3" not in params.keys():
                   if params["param#2"][1] == "number":
                      if   self.isIt(params["param#2"][0], 0): continue
                      elif self.isIt(params["param#2"][0], 1):
                           addr = self.getAddress(params["param#1"][0])
                           var  = self.__loader.virtualMemory.getVariableByName2(params["param#1"][0])

                           if len(addr) == 3 and var.type == "byte":
                              txt = "\tINC\t" + params["param#1"][0] + "\n"
                              self.checkASMCode(txt, line)
                              if self.__error == False: line["compiled"] = txt
                              continue

                   params["param#3"] = params["param#1"]

                else:
                    if params["param#1"][1] == "number" and params["param#2"][1] == "number":

                       keyParam = None
                       if   self.isIt(params["param#1"][0], 0):
                            keyParam = "param#2"
                       elif self.isIt(params["param#2"][0], 0):
                            keyParam = "param#1"

                       if keyParam != None:
                          txt = "\tLDA\t#" + params[keyParam][0].replace("#", "") + "\n"

                          var =  self.__loader.virtualMemory.getVariableByName2(params["param#3"][0])
                          if var.type != "byte":
                             txt += self.__mainCompiler.save8bitsToAny2(var.usedBits, params["param#3"][0])

                          txt += "\tSTA\t" + params["param#3"][0] + "\n"

                          self.checkASMCode(txt, line)
                          if self.__error == False: line["compiled"] = txt
                          continue

                changeText = self.prepareAdd(params)

                if self.__error == False: self.createASMTextFromLine(line, "add", params, changeText)
                #print(params)

            elif self.isCommandInLineThat(line, "and"):
                 params = self.getParamsWithTypesAndCheckSyntax(line)
                 if "param#3" not in params.keys():
                     if params["param#2"][1] == "number":
                        if self.isIt(params["param#2"][0], 255):
                           continue

                        if self.isIt(params["param#2"][0], 0):
                           txt = "\tLDA\t#0\n\tSTA\t" + params["param#1"][0] + "\n"
                           self.checkASMCode(txt, line)
                           if self.__error == False: line["compiled"] = txt
                           continue

                     params["param#3"] = params["param#1"]
                 else:

                     zeroParam = None
                     param255 = None

                     if params["param#1"][1] == "number":
                        if self.isIt(params["param#1"][0], 0):
                           zeroParam = True

                        if self.isIt(params["param#1"][0], 255):
                           param255 = "param#2"

                     if params["param#2"][1] == "number":
                        if self.isIt(params["param#2"][0], 0):
                           zeroParam = True

                        if self.isIt(params["param#2"][0], 255):
                           param255 = "param#1"

                     if zeroParam == True:
                        txt = "\tLDA\t#0\n\tSTA\t" + params["param#3"][0] + "\n"
                        self.checkASMCode(txt, line)
                        if self.__error == False: line["compiled"] = txt
                        continue

                     if param255 != None:
                        txt = "\tLDA\t#" + params[param255][0] + "\n\tSTA\t" + params["param#3"][0] + "\n"
                        self.checkASMCode(txt, line)
                        if self.__error == False: line["compiled"] = txt
                        continue

                 changeText = self.prepareAdd(params)
                 if self.__error == False: self.createASMTextFromLine(line, "and", params, changeText)

            elif self.isCommandInLineThat(line, "calc"):
                 self.convertStatementToSmallerCodes("calc", line["param#2"][0], line)


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
                            if tLine in self.__noneList or tLine == "\n" or "!!!" in tLine: continue
                            if tLine.startswith("*"):
                               textToReturn += tLine + "\n"
                            else:
                               textToReturn += "\tasm(\"" + tLine + "\")\n"

            if line["comment"][0] not in self.__noneList:
                textToReturn = textToReturn[:-1] + "\t; " + line["comment"][0] + "\n"

        self.result = textToReturn

    def isIt(self, val, comp):
        if val.startswith("#"): val = val[1:]

        if   val.startswith("%"):
             val = int(val.replace("%", "0b"), 2)
        elif val.startswith("$"):
             val = int(val.replace("$", "0x"), 16)
        else:
             val = int(val)

        if val == comp: return True
        return False

    def createASMTextFromLine(self, line, command, params, changeText):
        template = self.__loader.io.loadCommandASM(command)

        for item in changeText:
            #print(item, item in template)
            template = template.replace(item, changeText[item])

        for num in range(1, 4):
            name    = "param#" + str(num)
            varName = "#VAR0" + str(num) + "#"
            template = template.replace(varName, params[name][0])

        self.checkASMCode(template, line)
        if self.__error == False: line["compiled"] = template

    def prepareAdd(self, params):
        changeText = {}

        var1 = self.__loader.virtualMemory.getVariableByName2(params["param#1"][0])
        var2 = self.__loader.virtualMemory.getVariableByName2(params["param#2"][0])
        var3 = self.__loader.virtualMemory.getVariableByName2(params["param#3"][0])

        if var1 != False:
           if var1.type != "byte":
              changeText["!!!to8Bit1!!!"] = self.__mainCompiler.convertAnyTo8Bits(var1.usedBits)

        if var2 != False:
           if var2.type != "byte":
              changeText["#VAR02#"] = "temp01"
              changeText["!!!to8Bit2!!!"] = "\tLDA\t" + params["param#2"][0] + "\n" +\
                                            self.__mainCompiler.convertAnyTo8Bits(var2.usedBits) + "\tSTA\ttemp01"
        if var3 != False:
           if var3.type != "byte":
              changeText["!!!from8bit!!!"] = self.__mainCompiler.save8bitsToAny2(var3.usedBits, params["param#3"][0])

        return changeText


    def checkASMCode(self, template, lineStructure):
        lines = template.split("\n")

        for line in lines:
            delimiterPoz = self.__editorBigFrame.getFirstValidDelimiterPoz(line)
            line = line[:delimiterPoz]
            #'$79': {'opcode': 'ADC', 'format': 'aaaa,y', 'bytes': 3},
            line = line.replace("\r", "").replace("\t", " ").split(" ")
            command = ""
            value   = ""

            #if line == [""]: continue
            newLine = []
            for item in line:
                if item != "": newLine.append(item)
            line    = newLine
            if line == []: continue

            command = line[0]
            if len(line) > 1:
               value   = line[1]

            if command == "": continue
            errorVal   = 0

            foundCommand = False
            for item in self.__opcodes:
                lineSettings = self.__opcodes[item]
                if lineSettings["opcode"].upper() == command.upper():
                   if value in self.__noneList:
                       if lineSettings["bytes"] == 1:
                          foundCommand = True
                          break
                       else: continue

                   errorVal = 1
                   if self.checkIfASMhasrightOperand(lineSettings, value) == False: continue

                   errorVal = 2

                   beforeComma = value.split(",")[0]

                   operandTyp  = self.getTypeOfOperand(beforeComma)
                   operandSize = self.sizeOfNumber(beforeComma, operandTyp)

                   numberValue = ""
                   numeric = beforeComma

                   if operandTyp in ("variable", "register"):
                      numeric = self.getAddress(beforeComma)

                   if beforeComma.startswith("#>") or beforeComma.startswith("#<"):
                       if beforeComma[1] == ">":
                           beforeComma = self.__editorBigFrame.convertStringNumToNumber(numeric[1:3])
                       else:
                           beforeComma = self.__editorBigFrame.convertStringNumToNumber(numeric[3:5])
                   else:
                       numberValue = self.__editorBigFrame.convertStringNumToNumber(numeric.replace("#", ""))

                   hexa    = ""
                   mode    = ""
                   special = ""

                   try:
                       opcodeDoes = self.opcodesIOsMoreOtherThanRead[command.upper()]
                   except:
                       opcodeDoes = "read"

                   if operandTyp == "variable" and "#" in beforeComma:
                      operandTyp  = "constant"
                      beforeComma =  numeric

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
                               special = "RIOT"
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
                            special = "SARA"
                            if int(low) < 80:
                               mode = "write"
                            else:
                               mode = "read"
                      else:
                          special = "CPU"
                          if int(hexa[1:]) > 29:
                             mode = "read"
                          else:
                             mode = "write"

                   elif operandTyp == "variable":
                        if  len(self.getVarAddress(beforeComma)) > 3:
                            mode = self.changeSARAtoAddress(lineStructure, opcodeDoes, beforeComma)
                        else:
                            if beforeComma in self.__variablesOfBank["readOnly"]:
                               mode = "read"
                            else:
                               mode = "both"

                   elif operandTyp == "constant":
                        mode = "read"

                   if mode == "both" and (opcodeDoes == "read" or opcodeDoes == "write"):
                      mode = opcodeDoes

                   if opcodeDoes != mode:
                      if special == "":
                         eText = operandTyp[0].upper() + operandTyp[1:]
                      else:
                         eText = special

                      eText += opcodeDoes[0].upper() + opcodeDoes[1:]
                      self.addToErrorList(lineStructure["lineNum"],
                                          self.prepareErrorASM("compilerErrorASM"+eText,
                                                               command, value,
                                                               lineStructure["lineNum"]))
                   foundCommand = True
                   break

            if foundCommand == False:
               #print(line, errorVal)
               self.addToErrorList(lineStructure["lineNum"], self.prepareErrorASM("compilerErrorASMOpCode",
                                                     command, value, lineStructure["lineNum"]))

            """
            if foundCommand == True:
               try:
                   print(command, value, operandTyp, operandSize, item)
               except:
                   print(command, value)
            else:
               print(self.errorList)
            """

    def changeSARAtoAddress(self, line, IO, variable):
        address = self.getVarAddress(variable)
        low     = int(address[3:])

        if low  > 79:
           readAddress  = address
           writeAddress = self.__loader.virtualMemory.getSARAWriteAddressFromReadAddress(address)
        else:
           writeAddress = address
           readAddress  = self.__loader.virtualMemory.getSARAReadAddressFromWriteAddress(address)

        if IO == "read":
           line["compiled"] = line["compiled"].replace(variable, readAddress)
           return "read"
        else:
           line["compiled"] = line["compiled"].replace(variable, writeAddress)
           return "write"

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

        if "#" in beforeCommaValue:
           allA = "AA"
        else:
           allA = re.sub(r'[0-9a-fA-F]', "A", beforeCommaValue).replace("$", "")

        #print(beforeCommaFormat, allA)

        if beforeCommaFormat != allA: return False

        numOfBytesFormat = beforeCommaFormat.count("A") // 2
        if value.startswith("#"): numOfBytesFormat = 1

        return self.sizeOfNumber(value, "") == numOfBytesFormat

    def getVarAddress(self, var):
        addr = self.__virtualMemory.getAddressOnVariableIsStored(var, "bank1")
        if addr == False:
           addr = self.__virtualMemory.getAddressOnVariableIsStored(var, self.__currentBank)
        return addr

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

        for key in self.numberRegexes:
            if len(re.findall(self.numberRegexes[key], value.replace("#", ""))) > 0:
               if "#" in value: return "constant"
               else:            return "address"

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
        #raise ValueError

        return self.__dictionaries.getWordFromCurrentLanguage(text)\
                    .replace("#VAL#", val).replace("#VAR#", var).replace("#BANK#", self.__currentBank)\
                    .replace("#SECTION#", self.__currentSection).replace("#LINENUM#", str(lineNum)).replace("#PARAM#", param).replace("  ", " ")

    def prepareErrorASM(self, text, opcode, operand, lineNum):
        self.__error = True
        #raise ValueError

        return (self.__dictionaries.getWordFromCurrentLanguage("compilerErrorASM") + " " +\
               self.__dictionaries.getWordFromCurrentLanguage(text)).replace("#LINENUM#", str(lineNum))\
                                                                    .replace("#OPCODE#" , str(opcode))\
                                                                    .replace("#OPERAND#", str(operand))

    def isCommandInLineThat(self, line, command):
        if line["command"][0] == command or command in self.__loader.syntaxList[command].alias:
           return True
        return False

    def convertStatementToSmallerCodes(self, command, statement, line):
        side1            = ""
        side2            = ""
        statementData    = []
        statementFetched = []

        self.__temps = []
        for num in range(2, 20):
            num = str(num)
            if len(num) == 1: num = "0" + num

            self.__temps.append("temp" + num)

        needComprassion = True
        stringAllowed   = False
        statementTyp    = "comprass"

        if command == "calc":
           needComprassion = False
           statementTyp    = "calc"
        elif "%write" in command:
           needComprassion = False
           stringAllowed   = True
           statementTyp    = "write"

        statementData = self.__editorBigFrame.getStatementStructure(statement, needComprassion, stringAllowed, 0, line)

        foundError           = False
        for item in statementData:
            if item["type"] == "error":
               foundError = True
               break

        if foundError == True:
           self.addToErrorList(line["lineNum"],
                               self.prepareError("compilerErrorStatementError", statement,
                                                 "", "", str(line["lineNum"] + self.__startLine)))
        else:
            if statementTyp != "write":
               from sympy import simplify, expand
               statement = str(expand(simplify(statement)))

               statementData = self.__editorBigFrame.getStatementStructure(statement, needComprassion, stringAllowed, 0,
                                                                           line)
               for item in statementData:
                   if item["word"] in ["(", ")"]:
                      self.addToErrorList(line["lineNum"],
                                          self.prepareError("compilerErrorStatementComplex", statement,
                                                             "", "", str(line["lineNum"] + self.__startLine)))
                      break

               if self.__error == False:
                  commands = self.convertToCommands(statement, line)


        if self.__error == False:
           print(commands)


    def convertToCommands(self, statement, line):
        newT = []

        for temp in self.__temps:
            if temp not in statement:
               newT.append(temp)

        self.__temps = newT

        statement = statement.split(" ")

        print(statement)

        preCalc = []
        finals  = []

        import sympy
        for num in range(0, len(statement)):
            item = statement[num]

            if "*" in item or "/" in item or "%" in item:
               try:
                   temp = self.__temps[0]
                   preCalc.append( self.multiAndDivide(item, temp) )
                   finals.append(temp)
                   self.__temps.pop(0)
               except:
                   self.addToErrorList(line["lineNum"],
                                       self.prepareError("compilerErrorStatementTemps", statement,
                                                         "", "", str(line["lineNum"] + self.__startLine)))
                   return("")
            else:
               finals.append(item)

        saveHere   = line["param#1"]
        returnBack = "".join(preCalc)

        first = True
        for indexNum in range(2, len(finals), 2):
            if first == True:
               command  = finals[1]
               operand1 = finals[0]
               operand2 = finals[2]

               returnBack += "\t" + command + "(" + operand1 + ", " + operand2 + ", " + saveHere + ")\n"
               first       = False
            else:
                operand = finals[indexNum]
                command = finals[indexNum - 1]

                returnBack += "\t" + command + "(" + saveHere + ", " + operand + ")\n"

        return returnBack


    def multiAndDivide(self, data, temp):
        startIndex = 0
        endIndex   = -1

        returnBack = ""
        items      = []
        for charNum in range(0, len(data)):

            if charNum >= len(data) - 1:
               items.append(data[startIndex:])

            if data[charNum] in ["*", "/", "%"]:
               endIndex = charNum
               items.append(data[startIndex:endIndex])
               items.append(data[endIndex])

               startIndex = endIndex + 1
               endIndex   = -1

        first = True
        for indexNum in range(2, len(items), 2):
            if first == True:
               command  = items[1]
               operand1 = items[0]
               operand2 = items[2]

               returnBack += "\t" + command + "(" + operand1 + ", " + operand2 + ", " + temp + ")\n"
               first       = False
            else:
                operand = items[indexNum]
                command = items[indexNum - 1]

                returnBack += "\t" + command + "(" + temp + ", " + operand + ")\n"

        return returnBack
