from datetime import datetime

class FirstCompiler:

    def __init__(self, loader, editorBigFrame, text, addComments, mode, bank, section, startLine, fullText):

        self.__loader         = loader
        self.__editorBigFrame = editorBigFrame
        self.__text           = text.replace("\t", " ").split("\n")
        self.__fullText       = fullText.replace("\t", " ").split("\n")
        self.__noneList = ["", "None", None, []]
        self.__registers,     \
        self.__opcodes        = self.__loader.io.loadRegOpCodes()
        self.__replacers = {
            "#BANK#": bank,
            "#SECTION#": section,
            "#FULL#": bank + "_" + section
        }
        self.exiters = self.__editorBigFrame.exiters

        self.__fullTextLabels  = []
        for line in self.__fullText:
            if line == "": continue
            labelLineStructure = self.__editorBigFrame.getLineStructure(0, [line], False)
            if self.isCommandInLineThat(labelLineStructure, "asm"):
                asmCode = labelLineStructure["param#1"][0][1:-1]
                if labelLineStructure["param#2"][0] not in self.__noneList:
                   asmCode += " " + labelLineStructure["param#2"][0][1:-1]

                datas = asmCode.replace("\t", " ").split(" ")
                foundCode = False
                for part in datas:
                    if part != "":
                       for item in self.__opcodes:
                           lineSettings = self.__opcodes[item]
                           if lineSettings["opcode"].upper() == part.upper():
                               foundCode = True
                               break
                    break

                if foundCode: continue
                if "!!!" not in line and "=" not in line and asmCode[0] not in [" ", "\t", "*"] and\
                    (asmCode[0] != "#"               or
                     asmCode.startswith("#BANK#")    or
                     asmCode.startswith("#SECTION#") or
                     asmCode.startswith("#FULL#")):
                   for replacer in self.__replacers.keys():
                       if replacer in asmCode:
                          asmCode = asmCode.replace(replacer, self.__replacers[replacer])

                   self.__fullTextLabels.append(asmCode.replace("\n", "").replace("\t", "").replace(" ", "").replace("\r", ""))

        self.__magicNumber    = int(str(datetime.now()).replace("-", "").replace(".", "").replace(":", "").replace(" ", ""))
        self.__counter        = 0
        self.__addComments    = addComments
        self.__loadCommandASM = self.__loader.io.loadCommandASM
        self.errorList        = {}
        self.__currentBank    = bank
        self.__objectMaster   = self.__loader.virtualMemory.objectMaster
        self.toRoutines       = {}
        self.__branchers      = ["BCC", "BCS", "BEQ", "BNE", "BMI", "BPL", "BVC", "BVS"]
        self.__jumpers        = ["JMP", "JSR"]

        self.__labelsOfMainKenrel = []

        kernelText = self.__loader.io.loadKernelElement(self.__loader.virtualMemory.kernel, "main_kernel").split("\n")
        for line in kernelText:
            if line == "": continue
            if line[0] not in [" ", "\t", "*", "#"] and "=" not in line and "!!!" not in line:
               self.__labelsOfMainKenrel.append(line.replace("\t", "").replace(" ", "").replace("\r", ""))

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


        self.__writable, self.__readOnly, self.__all, self.__nonSystem  = writable, readOnly, all, nonSystem

        self.__validMemoryAddresses = []

        for num in range(0, 255):
            origNum = num
            num = hex(num).replace("0x", "")
            if len(num) == 1: num = "0" + num

            if origNum > 127:
               self.__validMemoryAddresses.append("$" + num.upper())

            self.__validMemoryAddresses.append("$F0" + num.upper())

        linesFeteched = []

        for lineNum in range(0, len(self.__text)):
            line = self.__text[lineNum]
            lineStruct = self.__editorBigFrame.getLineStructure(lineNum, self.__text, True)

            #if lineStruct["command"][0] in self.__noneList:
            #   continue

            lineStruct["fullLine"]       = line
            lineStruct["labelsBefore"]   = []
            lineStruct["labelsAfter"]    = []
            lineStruct["commentsBefore"] = ""
            lineStruct["compiled"]       = ""
            lineStruct["compiledBefore"] = ""
            lineStruct["magicNumber"]    = -1

            if addComments:
               lineStruct["commentsBefore"] = "***\t" + line[:self.__editorBigFrame.getFirstValidDelimiterPoz(line)]

            linesFeteched.append(lineStruct)
            lineStruct["unreachable"] = self.checkIfCodeUnreachable(linesFeteched, lineStruct["level"])
            if lineStruct["unreachable"] == True:
               lineStruct["command"][0]  = None
               lineStruct["param#1"][0]  = None
               lineStruct["param#2"][0]  = None
               lineStruct["param#3"][0]  = None


        """
        test = "\tLDA\ttemp01\n" + "\tLDA\ttemp01\n" + "\tSTA\ttemp02\n" + "\tLDA\ttemp01\n" + "\tLDA\ttemp01\n" + "\tSTA\ttemp03\n" + \
               "\tSTA\ttemp04\n" + "\tASL\n" + "\tLDA\ttemp01\n" + "\tSTA\ttemp05\n" + "\tLDA\ttemp04\n" + "\tLDA\ttemp01\n" + "\tSTA\ttemp06\n"

        print(self.checkForNotNeededExtraLDA(test))
        """

        """    
        text = "\tJMP\tFos\n\tLDA\t#0\nPacal\n\tSTA\ttemp01\nFos\n\tLDA\t#1\n"
        print(self.detectUnreachableCode(text))
        """

        #text = "\tLDA\t#3\n\tTAY\n\tLDA\ttemp01\n"
        #text = "\tLDA\ttemp02\n\tTAX\n\tLDA\ttemp01\n"
        #print(self.LDATAYLDA(text))

        self.compileBuild(linesFeteched, mode)

    def checkIfCodeUnreachable(self, linesFeteched, level):
        if len(linesFeteched) < 2: return False
        for lineNum in range(len(linesFeteched)-2, -1, -1):
            line = linesFeteched[lineNum]
            if line["level"] < level: return False
            if line["level"] > level: continue
            if line["command"][0] not in self.__noneList:
               for exitCommand in self.exiters:
                   if line["command"][0] == exitCommand or line["command"][0] in self.__loader.syntaxList[exitCommand].alias:
                      return True
        return False

        line = linesFeteched[-1]
        if line["command"][0] not in [None, "None", ""]:
            if self.__currentSection in ["subroutines", "screenroutines"] and line["level"] == 0 and \
               line["command"][0] != "subroutine"                         and line["command"][0] not in self.__loader.syntaxList["subroutine"].alias     and \
               line["command"][0] != "screen"                             and line["command"][0] not in self.__loader.syntaxList["screen"].alias         and \
               line["command"][0] != "end-subroutine"                     and line["command"][0] not in self.__loader.syntaxList["end-subroutine"].alias and \
               line["command"][0] != "end-screen"                         and line["command"][0] not in self.__loader.syntaxList["end-screen"].alias:

               return True

        return False

    def compileBuild(self, linesFeteched, mode):
        for line in linesFeteched:
            self.__error = False

            if line["command"][0] not in self.__noneList and line["unreachable"] == False:
               self.processLine(line, linesFeteched)

        textToReturn = ""
        for line in linesFeteched:
            for word in ["compiledBefore", "commentsBefore", "labelsBefore", "compiled", "labelsAfter"]:
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

        self.result = self.detectUnreachableCode(self.checkForNotNeededExtraLDA(textToReturn))

    def LDATAYLDA(self, text):
        lines = text.replace("\r", "").split("\n")

        for lineNum in range(2, len(lines)):
            line1 = lines[lineNum-2]
            line2 = lines[lineNum-1]
            line3 = lines[lineNum]

            if line1 == "" or line1.isspace() or line1[0] not in ["\t", " "] or \
               line2 == "" or line2.isspace() or line2[0] not in ["\t", " "] or \
               line3 == "" or line3.isspace() or line3[0] not in ["\t", " "]: continue

            opcode1, operand1 = self.getOpCodeAndOperandFromASMLine(line1)
            opcode2, operand2 = self.getOpCodeAndOperandFromASMLine(line2)
            opcode3, operand3 = self.getOpCodeAndOperandFromASMLine(line3)

            foundIt = False
            if (((opcode1.upper() == "LDA" and opcode2.upper() == "LDX")  or \
                (opcode1.upper() == "LDX" and opcode2.upper() == "LDA")) and \
                 operand1 == operand2)                                    or \
                (opcode1.upper() == "LDA" and opcode2.upper() == "TAX")      :
                 for item in self.__opcodes:
                    lineSettings = self.__opcodes[item]
                    if lineSettings["opcode"].upper() == "LAX":
                        if self.checkIfASMhasrightOperand(lineSettings, operand1) == True:
                            foundIt = True
                            break
                 if foundIt:
                    lines[lineNum - 2] = "\tLAX\t" + operand1
                    lines[lineNum - 1] = ""


            if foundIt == False:

                if opcode1[:2].upper() != "LD": continue
                if opcode3[:2].upper() != "LD": continue
                if opcode2[0].upper()  != "T"   or\
            "S" in opcode2                    : continue

                for letter1 in ["A", "Y", "X"]:
                    for letter2 in ["A", "Y", "X"]:
                        if letter1 == letter2: continue

                        compOp1 = "LD" + letter1
                        compOp2 = "T"  + letter1 + letter2

                        if opcode1 != compOp1 or opcode2 != compOp2 or opcode3 != compOp1: continue
                        newOpC = "LD" + letter2

                        foundIt = False
                        for item in self.__opcodes:
                            lineSettings = self.__opcodes[item]
                            if lineSettings["opcode"].upper() == newOpC:
                               if self.checkIfASMhasrightOperand(lineSettings, operand1) == True:
                                  foundIt = True
                                  break

                        if foundIt == False: continue
                        lines[lineNum-2] = "\t" + newOpC  + "\t" + operand1
                        lines[lineNum-1] = "\t" + opcode3 + "\t" + operand3
                        lines[lineNum]   =  ""
                        break

        return "\n".join(lines)

    def detectUnreachableCode(self, text):
        lines = text.replace("\r", "").split("\n")

        for lineNum in range(0, len(lines)):
            line = lines[lineNum]
            if line == "" or line.isspace() or line[0] not in ["\t", " "]:
                continue

            opcode, label = self.getOpCodeAndOperandFromASMLine(line)
            if opcode != "JMP":
               continue
            else:
               for secondLineNum in range(lineNum+1, len(lines)):
                   if secondLineNum >= len(lines): break
                   secondLine = lines[secondLineNum]

                   if secondLine.startswith(label): break
                   if len(secondLine) == 0: continue
                   if secondLine[0] in ["*", "#"] or secondLine.isspace(): continue

                   opcode2, filler = self.getOpCodeAndOperandFromASMLine(secondLine)

                   validOpCode = False
                   for item in self.__opcodes:
                       if opcode2.upper() == self.__opcodes[item]["opcode"]:
                          validOpCode = True
                          break

                   if validOpCode == False:
                      break

                   lines[secondLineNum] = ""

        return "\n".join(lines)

    def processLine(self, line, linesFeteched):
        self.__useThese = [line["lineNum"], linesFeteched]
        self.__thisLine = line
        self.__checked  = False
        self.__changeThese = {}

        if self.isCommandInLineThat(line, "asm"):
            datas = []
            for num in range(1, 3):
                if line["param#" + str(num)][0] not in self.__noneList:
                    datas.append(line["param#" + str(num)][0][1:-1])

            txt = "\t" + "\t".join(datas)

            """
            if line["param#2"][0] not in self.__noneList:
               line["param#1"][0] = "\"" + line["param#1"][0][1:-1] + " " + line["param#2"][0][1:-1] + "\""
               line["param#2"][0] = None
               line["fullLine"] = " asm(" + line["param#1"][0] + ")"
            """

            self.checkASMCode(txt, line)

            if self.__error == False:
               if line["level"] > -1:
                  line["compiled"] = txt
               else:
                  line["compiled"] = datas[0]

            for key in self.__changeThese.keys():
                line["compiled"] = line["compiled"].replace(key, self.__changeThese[key])

            self.__checked = True

        elif self.isCommandInLineThat(line, "add"):
            params = self.getParamsWithTypesAndCheckSyntax(line)

            if "param#3" not in params.keys():
                if params["param#2"][1] == "number":
                    if self.isIt(params["param#2"][0], 0):
                        return
                    elif self.isIt(params["param#2"][0], 1):
                        addr = self.getAddress(params["param#1"][0])
                        var = self.__loader.virtualMemory.getVariableByName2(params["param#1"][0])

                        if len(addr) == 3 and var.type == "byte" and (var.iterable == True or params["param#1"][0] == "item"):
                            txt = "\tINC\t" + params["param#1"][0] + "\n"
                            txt = self.checkForNotNeededExtraLDA(txt)

                            self.checkASMCode(txt, line)
                            if self.__error == False: line["compiled"] = txt
                            return

                params["param#3"] = params["param#1"]

            else:
                if params["param#1"][1] == "number" and params["param#2"][1] == "number":
                    theNum = int(self.__editorBigFrame.convertStringNumToNumber(params["param#1"][0])) + \
                             int(self.__editorBigFrame.convertStringNumToNumber(params["param#2"][0]))

                    theNum = theNum % 256

                    params["param#0"] = [str(theNum), "number"]
                    txt = self.saveAValue(params, "param#0", "param#3", line)
                    txt = self.checkForNotNeededExtraLDA(txt)

                    self.checkASMCode(txt, line)
                    if self.__error == False: line["compiled"] = txt
                    return

                if self.isIt(params["param#2"][0], 0):
                    txt = self.saveAValue(params, "param#1", "param#3", line)
                    txt = self.checkForNotNeededExtraLDA(txt)

                    self.checkASMCode(txt, line)
                    if self.__error == False: line["compiled"] = txt
                    return

            changeText = self.prepareAdd(params)

            if self.__error == False: self.createASMTextFromLine(line, "add", params, changeText)
            # print(params)

        elif self.isCommandInLineThat(line, "sub"):
            params = self.getParamsWithTypesAndCheckSyntax(line)

            if params["param#1"][1] == "number" and params["param#2"][1] == "number":
                theNum = int(self.__editorBigFrame.convertStringNumToNumber(params["param#1"][0])) - \
                         int(self.__editorBigFrame.convertStringNumToNumber(params["param#2"][0]))

                if theNum < 0:
                   theNum = 256 + theNum

                params["param#0"] = [str(theNum), "number"]
                txt = self.saveAValue(params, "param#0", "param#3", line)
                self.checkASMCode(txt, line)
                if self.__error == False: line["compiled"] = txt
                return

            elif params["param#2"][1] == "number":
                if self.isIt(params["param#2"][0], 0):
                   if "param#3" in params.keys():
                       txt = self.saveAValue(params, "param#1", "param#3", line)
                       txt = self.checkForNotNeededExtraLDA(txt)

                       self.checkASMCode(txt, line)
                       if self.__error == False: line["compiled"] = txt
                       return
                   else:
                      return
                elif self.isIt(params["param#2"][0], 1):
                    addr = self.getAddress(params["param#1"][0])
                    var = self.__loader.virtualMemory.getVariableByName2(params["param#1"][0])

                    if len(addr) == 3 and var.type == "byte" and (var.iterable == True or params["param#1"][0] == "item"):
                        txt = "\tDEC\t" + params["param#1"][0] + "\n"
                        txt = self.checkForNotNeededExtraLDA(txt)

                        self.checkASMCode(txt, line)
                        if self.__error == False: line["compiled"] = txt
                        return

                params["param#3"] = params["param#1"]

            changeText = self.prepareAdd(params)
            if self.__error == False: self.createASMTextFromLine(line, "sub", params, changeText)

        elif self.isCommandInLineThat(line, "sqrt"):
            params                  = self.getParamsWithTypesAndCheckSyntax(line)
            self.toRoutines["sqrt"] = self.__loader.io.loadCommandASM("sqrt_table").replace("#BANK#", self.__currentBank)
            template                = self.__loader.io.loadCommandASM("sqrt")
            self.__temps            = self.collectUsedTemps()

            try:
                theOne             =  self.__temps[0]
                self.__temps.pop(0)
            except:
                self.addToErrorList(line["lineNum"],
                                    self.prepareError("compilerErrorStatementTemps", params["param#1"][0],
                                                      "", "",
                                                      str(line["lineNum"] + self.__startLine)))

            if params["param#1"][1] == "variable":
                var1 = self.__loader.virtualMemory.getVariableByName(params["param#1"][0], self.__currentBank)
                if var1 == False:
                   var1 = self.__loader.virtualMemory.getVariableByName(params["param#1"][0], "bank1")

                if var1 == False:
                   self.addToErrorList(line["lineNum"],
                                       self.prepareError("compilerErrorVarNotFound", params["param#1"][0],
                                                          "", "",
                                                          str(line["lineNum"] + self.__startLine)))

            var2 = self.__loader.virtualMemory.getVariableByName(params["param#2"][0], self.__currentBank)
            if var2 == False:
               var2 = self.__loader.virtualMemory.getVariableByName(params["param#2"][0], "bank1")

            if var2 == False:
               self.addToErrorList(line["lineNum"],
                                   self.prepareError("compilerErrorVarNotFound", params["param#2"][0],
                                                      "", "",
                                                      str(line["lineNum"] + self.__startLine)))

            if self.__error == False:
               if params["param#1"][1] == "number":
                  template = template.replace("#VAR01#", "#" + params["param#1"][0].replace("#", ""))

               else:
                  template = template.replace("#VAR01#", params["param#1"][0])
                  if var1.type != "byte":
                      template = template.replace("!!!to8bit!!!", self.__mainCompiler.convertAnyTo8Bits(var1.usedBits))

               template = template.replace("#VAR02#", params["param#2"][0])
               if var2.type != "byte":
                   template = template.replace("!!!from8bit!!!",
                                               self.__mainCompiler.save8bitsToAny2(var2.usedBits),
                                                                                   params["param#2"][0])
               template = template.replace("#TEMP#", theOne)
               self.checkASMCode(template, line)
               if self.__error == False: line["compiled"] = template.replace("#BANK#", self.__currentBank).replace(
                   "#MAGIC#", str(self.__magicNumber))
               self.__magicNumber += 1

        elif self.isCommandInLineThat(line, "rand"):
            params    = self.getParamsWithTypesAndCheckSyntax(line)
            template  = self.__loader.io.loadCommandASM("rand")

            var = self.__loader.virtualMemory.getVariableByName(params["param#1"][0], self.__currentBank)
            if var == False:
               var = self.__loader.virtualMemory.getVariableByName(params["param#1"][0], "bank1")

            if var == False:
               self.addToErrorList(line["lineNum"],
                                   self.prepareError("compilerErrorVarNotFound", params["param#1"][0],
                                                     "", "",
                                                     str(line["lineNum"] + self.__startLine)))
            minV         = None
            maxV         = None
            replacers    = {}
            self.__temps = self.collectUsedTemps()

            if var.type != "byte":
               replacers["!!!from8bit!!!"] = self.__mainCompiler.save8bitsToAny2(var.usedBits, params["param#1"][0])
            replacers["#VAR01#"]           = params["param#1"][0]

            if   "param#3" in params.keys():
                 minV = "param#2"
                 maxV = "param#3"

            elif "param#2" in params.keys():
                 maxV = "param#2"

            if minV != None:
               val = params[minV][0]
               var = self.__loader.virtualMemory.getVariableByName2(val)
               if var == False:
                  replacers["!!!ADD!!!"] = "\tCLC\n\tADC\t#" + str(val).replace("#", "") + "\n"
               else:
                  if var.type == "byte":
                     replacers["!!!ADD!!!"] = "\tCLC\n\tADC\t" + str(val) + "\n"
                  else:
                     try:
                         first = self.__temps[0]
                         self.__temps.pop(0)
                     except:
                         self.addToErrorList(line["lineNum"],
                                             self.prepareError("compilerErrorStatementTemps", params["param#1"][0],
                                                               "", "",
                                                               str(line["lineNum"] + self.__startLine)))
                     if self.__error == False:
                        replacers["!!!ADD!!!"]     = "\tCLC\n\tADC\t" + first + "\n"
                        replacers["!!!CALCADD!!!"] = "\tLDA\t" + val + \
                                                     "\n" + self.__mainCompiler.convertAnyTo8Bits(var.usedBits) +\
                                                     "\tSTA\t" + first + "\n"

            if maxV != None:
                val = params[maxV][0]
                var = self.__loader.virtualMemory.getVariableByName2(val)
                if var == False:
                    replacers["!!!AND!!!"] = "\tCLC\n\tAND\t#" + str(val).replace("#", "") + "\n"
                else:
                    if var.type == "byte":
                        replacers["!!!AND!!!"] = "\tAND\t" + str(val) + "\n"
                    else:
                        try:
                            first = self.__temps[0]
                            self.__temps.pop(0)
                        except:
                            self.addToErrorList(line["lineNum"],
                                                self.prepareError("compilerErrorStatementTemps", params["param#1"][0],
                                                                  "", "",
                                                                  str(line["lineNum"] + self.__startLine)))
                        if self.__error == False:
                            replacers["!!!AND!!!"] = "\tAND\t" + first + "\n"
                            replacers["!!!CALCADD!!!"] = "\tLDA\t" + val + \
                                                         "\n" + self.__mainCompiler.convertAnyTo8Bits(var.usedBits) + \
                                                         "\tSTA\t" + first + "\n"


            for key in replacers:
                template = template.replace(key, replacers[key])

            self.__readOnly.remove("random")
            self.checkASMCode(template, line)
            self.__readOnly.append("random")
            if self.__error == False: line["compiled"] = template
            return

        elif self.isCommandInLineThat(line, "swap"):
            params = self.getParamsWithTypesAndCheckSyntax(line)
            var1 = self.__loader.virtualMemory.getVariableByName(params["param#1"][0], self.__currentBank)
            if var1 == False:
                var1 = self.__loader.virtualMemory.getVariableByName(params["param#1"][0], "bank1")

            if var1 == False:
                self.addToErrorList(line["lineNum"],
                                    self.prepareError("compilerErrorVarNotFound", params["param#1"][0],
                                                      "", "",
                                                      str(line["lineNum"] + self.__startLine)))

            var2 = self.__loader.virtualMemory.getVariableByName(params["param#2"][0], self.__currentBank)
            if var2 == False:
                var2 = self.__loader.virtualMemory.getVariableByName(params["param#2"][0], "bank1")

            if var2 == False:
                self.addToErrorList(line["lineNum"],
                                    self.prepareError("compilerErrorVarNotFound", params["param#1"][0],
                                                      "", "",
                                                      str(line["lineNum"] + self.__startLine)))

            load1    = ""
            load2    = ""
            save1    = ""
            save2    = ""

            varName1 = params["param#1"][0]
            varName2 = params["param#2"][0]

            if var1.type == "byte":
               load1     =  "\tLDY\t" + varName1 + "\n"
               save1     =  "\tSTA\t" + varName1 + "\n"
            else:
               load1     = "\tLDA\t" + varName1 + "\n" + self.__mainCompiler.convertAnyTo8Bits(var1.usedBits) + "\tTAY\n"
               save1     = self.__mainCompiler.save8bitsToAny2(var1.usedBits, varName1) + "\tSTA\t" + varName1 + "\n"

            if var2.type == "byte":
               load2     =  "\tLDA\t" + varName2 + "\n"
               save2     =  "\tSTY\t" + varName2 + "\n"
            else:
               load2     = "\tLDA\t" + varName1 + "\n" + self.__mainCompiler.convertAnyTo8Bits(var2.usedBits)
               save2     = "\tTYA\n" + self.__mainCompiler.save8bitsToAny2(var2.usedBits, varName1) + "\tSTA\t" + varName2 + "\n"

            txt = load1 + load2 + save1 + save2

            self.checkASMCode(txt, line)
            if self.__error == False: line["compiled"] = txt


        elif self.isCommandInLineThat(line, "pow"):
            from copy import deepcopy
            params = self.getParamsWithTypesAndCheckSyntax(line)

            if params["param#1"][1] != "number" or params["param#2"][1] != "number":

                varPow2Param = False
                if params["param#1"][1] == "number":
                   if self.isIt(params["param#1"][0], 2):
                      varPow2Param = "param#2"

                if varPow2Param != False:
                    template = self.__loader.io.loadCommandASM("pow2")
                    if params[varPow2Param][1] == "variable":
                        var1 = self.__loader.virtualMemory.getVariableByName(params[varPow2Param][0], self.__currentBank)
                        if var1 == False:
                           var1 = self.__loader.virtualMemory.getVariableByName(params[varPow2Param][0], "bank1")

                        if var1 == False:
                            self.addToErrorList(line["lineNum"],
                                                self.prepareError("compilerErrorVarNotFound", params["param#1"][0],
                                                                  "", "",
                                                                  str(line["lineNum"] + self.__startLine)))

                        template = template.replace("#VAR01#", params[varPow2Param][0])
                        if var1.type != "byte":
                           template = template.replace("!!!to8bit!!!", self.__mainCompiler.convertAnyTo8Bits(var1.usedBits))

                    else:
                        template = template.replace("#VAR01#", "#" + params[varPow2Param][0].replace("#", ""))


                    var2 = self.__loader.virtualMemory.getVariableByName(params["param#3"][0], self.__currentBank)
                    if var2 == False:
                       var2 = self.__loader.virtualMemory.getVariableByName(params["param#3"][0], "bank1")

                    if var2 == False:
                        self.addToErrorList(line["lineNum"],
                                            self.prepareError("compilerErrorVarNotFound", params["param#3"][0],
                                                              "", "",
                                                              str(line["lineNum"] + self.__startLine)))

                    template = template.replace("#VAR02#", params["param#3"][0])
                    if var2.type == "type":
                       template = template.raplace("!!!from8bit!!!" , self.__mainCompiler.save8bitsToAny2(var2.usedBits, params["param#2"][0]))

                    self.checkASMCode(template, line)
                    if self.__error == False: line["compiled"] = template.replace("#BANK#", self.__currentBank).replace("#MAGIC#", str(self.__magicNumber))
                    self.__magicNumber += 1

                    return

                if params["param#2"][1] == "number":
                    if self.__editorBigFrame.convertStringNumToNumber(params["param#2"][0]) == 2:
                       subline = self.createSubLineForPower(line, linesFeteched)
                       line["compiled"] = subline["compiled"]

                       self.checkASMCode(line["compiled"] , line)
                       if self.__error == False:
                          self.__checked = True
                       return

                    elif self.__editorBigFrame.convertStringNumToNumber(params["param#2"][0]) == 1:
                        params["param#0"] = params["param#1"]
                        if "param#3" not in params.keys():
                            return
                        else:
                            txt = self.saveAValue(params, "param#0", "param#3", line)

                        self.checkASMCode(txt, line)
                        if self.__error == False: line["compiled"] = txt
                        return

                    elif self.__editorBigFrame.convertStringNumToNumber(params["param#2"][0]) == 0:
                        params["param#0"] = ["#1", "number"]
                        if "param#3" not in params.keys():
                            txt = self.saveAValue(params, "param#0", "param#1", line)
                        else:
                            txt = self.saveAValue(params, "param#0", "param#3", line)

                        self.checkASMCode(txt, line)
                        if self.__error == False: line["compiled"] = txt
                        return

                subLine = self.createSubLineForPower(line, linesFeteched)
                if params["param#2"][1] == "variable":
                   var = self.__loader.virtualMemory.getVariableByName2(subLine["param#2"][0])
                   if var == False:
                      self.addToErrorList(line["lineNum"], self.prepareError("compilerErrorVarNotFound", params["param#2"][0],
                                                                              "", "",
                                                                              str(line["lineNum"] + self.__startLine)))
                if self.__error == False:
                   txt = self.preparePow(params, subLine, line)
                   self.checkASMCode(txt, line)
                   if self.__error == False:
                      line["compiled"] = txt
                      self.__checked = True

            else:
                theNum = pow(self.__editorBigFrame.convertStringNumToNumber(params["param#1"][0]),
                             self.__editorBigFrame.convertStringNumToNumber(params["param#2"][0]))

                theNum = theNum%256
                params["param#0"] = ["#" + str(theNum), "number"]

                txt = self.saveAValue(params, "param#0", "param#3", line)
                self.checkASMCode(txt, line)
                if self.__error == False: line["compiled"] = txt
                return


        elif self.isCommandInLineThat(line, "multi"):
            params = self.getParamsWithTypesAndCheckSyntax(line)

            if    (params["param#1"][1] == "number" and params["param#2"][1] == "variable"):
                  self.checkIfCanShiftBits(params, "param#2", "param#1", line, "ASL")
                  if line["compiled"] != "": return
            elif (params["param#2"][1] == "number" and params["param#1"][1] == "variable"):
                  self.checkIfCanShiftBits(params, "param#1", "param#2", line, "ASL")
                  if line["compiled"] != "": return

            if params["param#1"][1] == "number" and params["param#2"][1] == "number":
                theNum = int(self.__editorBigFrame.convertStringNumToNumber(params["param#1"][0])) * \
                         int(self.__editorBigFrame.convertStringNumToNumber(params["param#2"][0]))

                theNum = theNum % 256

                params["param#0"] = [str(theNum), "number"]
                txt = self.saveAValue(params, "param#0", "param#3", line)
                self.checkASMCode(txt, line)
                if self.__error == False: line["compiled"] = txt
                return


            if "param#3" not in params.keys():
               params["param#3"] = params["param#1"]

            if params["param#1"][1] == "number":
               if self.isIt(params["param#1"][0], 1):
                  if "param#3" in params.keys():
                      txt = self.saveAValue(params, "param#2", "param#3", line)
                      self.checkASMCode(txt, line)
                      if self.__error == False: line["compiled"] = txt
                      return
                  else:
                      return

               elif self.isIt(params["param#1"][0], 0):
                    params["param#0"] = ["#0", "number"]
                    txt = self.saveAValue(params, "param#0", "param#3", line)
                    txt = self.checkForNotNeededExtraLDA(txt)

                    self.checkASMCode(txt, line)
                    if self.__error == False: line["compiled"] = txt
                    return

            if params["param#2"][1] == "number":
               if self.isIt(params["param#2"][0], 1):
                  if "param#3" in params.keys():
                      txt = self.saveAValue(params, "param#1", "param#3", line)
                      txt = self.checkForNotNeededExtraLDA(txt)

                      self.checkASMCode(txt, line)
                      if self.__error == False: line["compiled"] = txt
                      return
                  else:
                      return

               elif self.isIt(params["param#2"][0], 0):
                    if params["param#3"][0] in self.__noneList:
                       saveParam = "param#1"
                    else:
                       saveParam = "param#3"

                    params["param#0"] = ["#0", "number"]
                    txt = self.saveAValue(params, "param#0", saveParam, line)
                    txt = self.checkForNotNeededExtraLDA(txt)

                    self.checkASMCode(txt, line)
                    if self.__error == False: line["compiled"] = txt
                    return

            changeText = self.prepareMulti(params)
            if self.__error == False: self.createASMTextFromLine(line, "multi", params, changeText)

        elif self.isCommandInLineThat(line, "div") or self.isCommandInLineThat(line, "rem"):
            if self.isCommandInLineThat(line, "divide"):
               saveThisOne = "Y"
            else:
               saveThisOne = "A"

            params  = self.getParamsWithTypesAndCheckSyntax(line)

            if (params["param#2"][1] == "number" and params["param#1"][1] == "variable"):
                self.checkIfCanShiftBits(params, "param#1", "param#2", line, "LSR")
                if line["compiled"] != "": return

            zeroDiv = False
            oneDiv  = False

            if params["param#2"][1] == "number":
               if self.isIt(params["param#2"][0], 0):
                  zeroDiv = True
               elif self.isIt(params["param#2"][0], 0):
                  oneDiv = True

            if zeroDiv == True:
                self.addToErrorList(line["lineNum"],
                                    self.prepareError("compilerErrorZeroDiv", "", "", "",
                                                      str(line["lineNum"] + self.__startLine)))

            elif params["param#1"][1] == "number" and params["param#2"][1] == "number":
                if saveThisOne == "Y":
                    theNum = int(self.__editorBigFrame.convertStringNumToNumber(params["param#1"][0])) // \
                             int(self.__editorBigFrame.convertStringNumToNumber(params["param#2"][0]))
                else:
                    theNum = int(self.__editorBigFrame.convertStringNumToNumber(params["param#1"][0])) % \
                             int(self.__editorBigFrame.convertStringNumToNumber(params["param#2"][0]))

                theNum = theNum % 256

                params["param#0"] = [str(theNum), "number"]
                txt = self.saveAValue(params, "param#0", "param#3", line)
                self.checkASMCode(txt, line)
                if self.__error == False: line["compiled"] = txt
                return

            elif oneDiv == True:
                if saveThisOne == "Y":
                    if "param#3" not in params.keys():
                       return

                    txt = self.saveAValue(params, "param#1", "param#3", line)
                    txt = self.checkForNotNeededExtraLDA(txt)

                    self.checkASMCode(txt, line)
                    if self.__error == False: line["compiled"] = txt
                    return
                else:
                    if "param#3" not in params.keys():
                        params["param#3"] = params["param#1"]

                    params["param#0"] = [0, "number"]
                    txt = self.saveAValue(params, "param#0", "param#3", line)
                    self.checkASMCode(txt, line)
                    if self.__error == False: line["compiled"] = txt
                    self.__checked = True

            else:
                if "param#3" not in params.keys():
                   params["param#3"] = params["param#1"]

                changeText = self.prepareDiv(params, saveThisOne)
                if self.__error == False: self.createASMTextFromLine(line, "div", params, changeText)


        elif self.isCommandInLineThat(line, "and") or\
             self.isCommandInLineThat(line, "or")  or\
             self.isCommandInLineThat(line, "xor"):
            if   self.isCommandInLineThat(line, "and"):
                 command = "and"
            elif self.isCommandInLineThat(line, "or"):
                 command = "or"
            else:
                 command = "xor"

            params = self.getParamsWithTypesAndCheckSyntax(line)
            if "param#3" not in params.keys():
                if params["param#2"][1] == "number":
                    if command == "and":
                       if self.isIt(params["param#2"][0], 255):
                          return

                       if self.isIt(params["param#2"][0], 0):
                          params["param#0"] = ["#0", "number"]
                          txt = self.saveAValue(params, "param#0", "param#1", line)
                          txt = self.checkForNotNeededExtraLDA(txt)
                          self.checkASMCode(txt, line)
                          if self.__error == False: line["compiled"] = txt
                          return
                    elif command == "or":
                        if self.isIt(params["param#2"][0], 0):
                            return

                        if self.isIt(params["param#2"][0], 255):
                            params["param#0"] = ["#255", "number"]
                            txt = self.saveAValue(params, "param#0", "param#1", line)
                            txt = self.checkForNotNeededExtraLDA(txt)
                            self.checkASMCode(txt, line)
                            if self.__error == False: line["compiled"] = txt
                            return

                params["param#3"] = params["param#1"]
            else:
                if params["param#1"][1] == "number" and params["param#2"][1] == "number":
                    if   command == "and":
                         theNum = int(self.__editorBigFrame.convertStringNumToNumber(params["param#1"][0])) &\
                                  int(self.__editorBigFrame.convertStringNumToNumber(params["param#2"][0]))
                    elif command == "or":
                          theNum = int(self.__editorBigFrame.convertStringNumToNumber(params["param#1"][0])) | \
                                   int(self.__editorBigFrame.convertStringNumToNumber(params["param#2"][0]))
                    else:
                          theNum = int(self.__editorBigFrame.convertStringNumToNumber(params["param#1"][0])) ^ \
                                   int(self.__editorBigFrame.convertStringNumToNumber(params["param#2"][0]))

                    params["param#0"] = [str(theNum), "number"]
                    txt = self.saveAValue(params, "param#0", "param#3", line)
                    txt = self.checkForNotNeededExtraLDA(txt)
                    self.checkASMCode(txt, line)
                    if self.__error == False: line["compiled"] = txt

                    return

                param0   = None
                param255 = None

                if params["param#1"][1] == "number":
                    if self.isIt(params["param#1"][0], 0):
                        param0    = "param#2"

                    if self.isIt(params["param#1"][0], 255):
                        param255 = "param#2"

                if params["param#2"][1] == "number":
                    if self.isIt(params["param#2"][0], 0):
                        param0    = "param#1"

                    if self.isIt(params["param#2"][0], 255):
                        param255 = "param#1"

                if command == "and":
                    if param0 != None:
                        params["param#0"] = ["#0", "number"]
                        txt = self.saveAValue(params, "param#0", "param#3", line)
                        txt = self.checkForNotNeededExtraLDA(txt)
                        self.checkASMCode(txt, line)
                        if self.__error == False: line["compiled"] = txt
                        return

                    if param255 != None:
                        txt = self.saveAValue(params, param255, "param#3", line)
                        txt = self.checkForNotNeededExtraLDA(txt)
                        self.checkASMCode(txt, line)
                        if self.__error == False: line["compiled"] = txt
                        return
                elif command == "or":
                    if param255 != None:
                        params["param#0"] = ["#255", "number"]
                        txt = self.saveAValue(params, "param#0", "param#3", line)
                        txt = self.checkForNotNeededExtraLDA(txt)
                        self.checkASMCode(txt, line)
                        if self.__error == False: line["compiled"] = txt
                        return

                    if param0 != None:
                        txt = self.saveAValue(params, param0, "param#3", line)
                        txt = self.checkForNotNeededExtraLDA(txt)
                        self.checkASMCode(txt, line)
                        if self.__error == False: line["compiled"] = txt
                        return

            changeText = self.prepareAdd(params)
            if self.__error == False: self.createASMTextFromLine(line, command, params, changeText)

        elif self.isCommandInLineThat(line, "rollL") or self.isCommandInLineThat(line, "rollR") or \
             self.isCommandInLineThat(line, "shiftL") or self.isCommandInLineThat(line, "shiftR"):
             if   self.isCommandInLineThat(line, "rollL"):
                  command = "ROL"
             elif self.isCommandInLineThat(line, "rollR"):
                  command = "ROR"
             elif self.isCommandInLineThat(line, "shiftL"):
                  command = "ASL"
             else:
                  command = "LSR"

             params = self.getParamsWithTypesAndCheckSyntax(line)

             if "param#2" not in params.keys():
                 params["param#2"] = ["2", "number"]
                 self.checkIfCanShiftBits(params, "param#1", "param#2", line, command)

             else:
                 from copy import deepcopy

                 shiftNum = -1
                 if params["param#1"][1] == "number":
                    shiftNum = self.__editorBigFrame.convertStringNumToNumber(params["param#1"][0])

                 if params["param#1"][1] == "variable" or shiftNum > 2:
                     self.shiftOnVars(params, line, command)

                 elif shiftNum == 0: return

                 else:
                     params["param#3"] = deepcopy(params["param#2"])
                     params["param#2"] = [str(2**shiftNum)]
                     params["param#1"] = params["param#3"]

                     self.checkIfCanShiftBits(params, "param#1", "param#2", line, command)

                 #if line["compiled"] != "": self.checkASMCode(line["compiled"], line)
                 #if self.__error == True: line["compiled"] = ""


        elif self.isCommandInLineThat(line, "flip"):
            params = self.getParamsWithTypesAndCheckSyntax(line)
            var1 = self.__loader.virtualMemory.getVariableByName(params["param#1"][0], self.__currentBank)
            if var1 == False:
                var1 = self.__loader.virtualMemory.getVariableByName(params["param#1"][0], "bank1")

            if var1 == False:
                self.addToErrorList(line["lineNum"], self.prepareError("compilerErrorVarNotFound", params["param#1"][0],
                                                                       "", "",
                                                                       str(line["lineNum"] + self.__startLine)))
            if "param#2" in params:
                var2 = self.__loader.virtualMemory.getVariableByName(params["param#1"][0], self.__currentBank)
                if var2 == False:
                    var2 = self.__loader.virtualMemory.getVariableByName(params["param#1"][0], "bank1")

                if var2 == False:
                    self.addToErrorList(line["lineNum"],
                                        self.prepareError("compilerErrorVarNotFound", params["param#1"][0],
                                                          "", "",
                                                          str(line["lineNum"] + self.__startLine)))

                subLineStructure = self.__editorBigFrame.getLineStructure(0,
                                                                          ["\txor(" + params["param#1"][0] + ", 255, " +
                                                                          params["param#2"][0] + ")"]
                                                                          , False)
            else:
                params["param#2"] = params["param#1"]
                subLineStructure = self.__editorBigFrame.getLineStructure(0,
                                                                          ["\txor("+ params["param#1"][0] + ", 255)"]
                                                                          , False )
            subLineStructure["fullLine"] = line["fullLine"]
            for key in line:
                if key not in subLineStructure.keys():
                   subLineStructure[key] = line[key]

            self.processLine(subLineStructure, linesFeteched)
            line["compiled"] = subLineStructure["compiled"]

        elif self.isCommandInLineThat(line, "calc"):
            smallerCommands, temps = self.convertStatementToSmallerCodes("calc", line["param#2"][0], line)

            if self.__error == False:
               smallerCommands     = self.isThereAnyLargerThan255(smallerCommands)
               smallerCommandLines = smallerCommands.split("\n")

               for subLine in smallerCommandLines:
                   if subLine == "": continue

                   subLineStructure = self.__editorBigFrame.getLineStructure(0, [subLine], False)
                   for key in line:
                       if key not in subLineStructure.keys():
                           subLineStructure[key] = line[key]

                   self.processLine(subLineStructure, linesFeteched)

                   if self.__error == False:
                      line["compiled"] += subLineStructure["compiled"] + "\n"

        elif self.isCommandInLineThat(line, "call"):
             params = self.getParamsWithTypesAndCheckSyntax(line)

             template = self.__loader.io.loadCommandASM("call")
             template = template.replace("#ADDRESS#", self.__currentBank + "_SubRoutine_" + params["param#1"][0])

             subroutines = self.__editorBigFrame.collectNamesByCommandFromSections("subroutine", self.__currentBank)

             if params["param#1"][0] not in subroutines:
                self.addToErrorList(line["lineNum"], self.prepareError("compilerErrorSubroutine", params["param#1"][0],
                                                                        "", "",
                                                                        str(line["lineNum"] + self.__startLine)))

             if self.__error == False:
                save = ""
                if params["param#2"][0] not in self.__noneList:
                   var = self.__loader.virtualMemory.getVariableByName(params["param#2"][0], self.__currentBank)
                   if var == False:
                      var = self.__loader.virtualMemory.getVariableByName(params["param#2"][0], "bank1")

                   if var == False:
                      self.addToErrorList(line["lineNum"], self.prepareError("compilerErrorVarNotFound", params["param#1"][0],
                                                                               "", "",
                                                                               str(line["lineNum"] + self.__startLine)))
                   if self.__error == False:
                      if var.type != "byte":
                         save += self.__mainCompiler.save8bitsToAny2(var.usedBits, params["param#2"][0])
                      save += "\tSTA\t" + params["param#2"][0] + "\n"

                      template = template.replace("!!!SAVE!!!", save)
                      line["compiled"] = template

        elif line["command"][0].split("-")[0] in ["do", "perform", "for", "foreach"]:
            command     = None
            commandName = None
            for c in self.__loader.syntaxList.keys():
                if line["command"][0] == c or line["command"][0] in self.__loader.syntaxList[c].alias:
                   command     = self.__loader.syntaxList[c]
                   commandName = c
                   break

            if command == None:
                self.addToErrorList(line["lineNum"], self.prepareError("compilerErrorCommand", "",
                                                                       line["command"][0], "",


                                                                       str(line["lineNum"] + self.__startLine)))

            txt = ""
            if self.__error == False:
               line["magicNumber"] = str(self.__magicNumber)
               self.__magicNumber += 1
               subName = commandName.split("-")
               for partNum in range(0, len(subName)):
                   subName[partNum] = subName[partNum][0].upper() + subName[partNum][1:]
               subName = "-".join(subName)

               name = self.__currentBank + "_" + line["magicNumber"] + "_" + subName + "_"

               txt = name + "Start" + "\n"
               end = self.__editorBigFrame.findEnd(line, line["lineNum"], self.__text)
               if  end == False:
                   self.addToErrorList(line["lineNum"],
                                       self.prepareError("compilerErrorNoEnd", "",
                                                          line["command"][0], "",
                                                          str(line["lineNum"] + self.__startLine)))

               endLine = linesFeteched[end[0]]
               endLine["labelsBefore"] = name + "End"
               if self.isCommandInLineThat(line, "do-frames") == False:
                  endLine["compiledBefore"] = "\tJMP\t" + name + "Loop\n"

               exits = self.__editorBigFrame.listAllCommandFromTo("exit", self.__text, line["level"] + 1,
                                                                  line["lineNum"], end[0] + 1)
               for item in exits:
                   exitLine = linesFeteched[item["lineNum"]]
                   exitLine["compiled"] = "\tJMP\t" + name + "End\n"

               cycles = self.__editorBigFrame.listAllCommandFromTo("cycle", self.__text, line["level"] + 1,
                                                                  line["lineNum"], end[0] + 1)
               for item in cycles:
                   cycleLine = linesFeteched[item["lineNum"]]
                   cycleLine["compiled"] = "\tJMP\t" + name + "Loop\n"

               self.__temps = self.collectUsedTemps()
               params = self.getParamsWithTypesAndCheckSyntax(line)

               if self.isCommandInLineThat(line, "do-times"):
                  if params["param#1"][0] == "variable":
                      if params["param#1"][1] == "variable":
                         var = self.__loader.virtualMemory.getVariableByName(params["param#1"][0],
                                                                             self.__currentBank)
                         if var == False:
                            var = self.__loader.virtualMemory.getVariableByName(params["param#1"][0], "bank1")
                         if var == False:
                            self.addToErrorList(line["lineNum"],
                                                  self.prepareError("compilerErrorVarNotFound",
                                                                    params["param#1"][0],
                                                                    "", "",
                                                                    str(line["lineNum"] + self.__startLine)))

                  if self.__error == False:
                     if params["param#1"][1] == "variable":
                        txt += "\tLDA\t"  + params["param#1"][0] + "\n"
                     else:
                        txt += "\tLDA\t#" + params["param#1"][0].replace("#", "") + "\n"

                     try:
                         first = self.__temps[0]
                         self.__temps.pop(0)
                     except:
                         self.addToErrorList(line["lineNum"],
                                             self.prepareError("compilerErrorStatementTemps", params["param#1"][0],
                                                               "", "",
                                                               str(line["lineNum"] + self.__startLine)))
                     if self.__error == False:
                         done = False
                         if params["param#1"][1] == "number":
                               if self.__editorBigFrame.convertStringNumToNumber(params["param#1"][0]) < 128:
                                   txt += "\tSTA\t" + first + "\n" + \
                                           name + "Loop" + "\n" + \
                                          "\tDEC\t" + first + "\n" + \
                                          "\tLDA\t" + first + "\n" + \
                                          "\tBMI\t" + name + "End\n"

                                   done = True

                         if done == False:
                             txt += "\tSTA\t" + first  + "\n"        +\
                                    "\tJMP\t" + name                 +\
                                    "JumpOver" + "\n"                +\
                                      name    + "Loop" + "\n"        +\
                                    "\tDEC\t" + first  + "\n"        +\
                                    "\tLDA\t" + first  + "\n"        +\
                                    "\tCMP\t" + "#0"   + "\n"        +\
                                    "\tBEQ\t" + name   + "End\n"     +\
                                    name      + "JumpOver\n"

               elif self.isCommandInLineThat(line, "do-frames"):
                  thatNum1 = str(self.__editorBigFrame.convertStringNumToNumber(params["param#1"][0]) - 1)

                  if "param#2" in params.keys():
                      thatNum2 = str(self.__editorBigFrame.convertStringNumToNumber(params["param#2"][0]) - 1)

                  if thatNum1 != "0":
                     txt += "\tLDA\tcounter\n\tAND\t#" + thatNum1 + "\n"
                     if "param#2" in params.keys():
                        txt += "\tCMP\t#" + thatNum2 + "\n"
                     else:
                        txt += "\tCMP\t#" + thatNum1 + "\n"
                     txt += "\tBNE\t" + name + "End" + "\n" + name + "Loop" + "\n"
                  else:
                     txt += name + "Loop" + "\n"

               elif self.isCommandInLineThat(line, "do"):
                   txt += name + "Loop" + "\n"

               elif self.isCommandInLineThat(line, "do-items"):
                   array = line["param#1"][0]
                   self.changeIfYouCanSaveToItem(True)

                   if array not in self.__loader.virtualMemory.arrays.keys() or\
                      (self.__virtualMemory.getArrayValidity(array) not in [self.__currentBank, "bank1", "global"]):

                      self.addToErrorList(line["lineNum"],
                                          self.prepareError("compilerErrorArrayNotFound", array,
                                                             "", "",
                                                             str(line["lineNum"] + self.__startLine)))

                   if self.__error == False:
                      isWriting = self.checkIfItIsWritingInItem(line["lineNum"], endLine["lineNum"], line["level"], self.__text)
                      for varName in self.__virtualMemory.arrays[array]:
                          var = self.__loader.virtualMemory.getVariableByName2(varName)
                          if var == False:
                             self.addToErrorList(line["lineNum"],
                                                 self.prepareError("compilerErrorVarNotFound", params["param#1"][0],
                                                                    "", "",
                                                                    str(line["lineNum"] + self.__startLine)))

                          else:
                              txt += "\tLDA\t" + varName + "\n"
                              if var.type != "byte":
                                 txt += self.__mainCompiler.convertAnyTo8Bits(var.usedBits)

                              txt += "\tSTA\titem\n\tJSR\t" + name + "JumpOver\n"

                              if isWriting:
                                 txt += "\tLDA\titem\n"
                                 if var.type != "byte":
                                    txt += self.__mainCompiler.save8bitsToAny2(var.usedBits, varName)
                                 txt += "\tSTA\t" + varName + "\n"

                      txt += "\tJMP\t" + name + "End\n" + name + "Loop" + "\n" + "\tRTS\n" + name + "JompOver\n"

                   self.changeIfYouCanSaveToItem(False)

               elif self.isCommandInLineThat(line, "do-until") or self.isCommandInLineThat(line, "do-while"):
                   opcode = ""
                   txt += name + "Loop" + "\n"

                   statement = line["param#1"][0]
                   smallerCommands, temps = self.convertStatementToSmallerCodes("do-until",
                                                                                statement, line)
                   smallerCommandLines = smallerCommands.split("\n")

                   #print(smallerCommandLines)

                   if self.__error == False:
                       for subLine in smallerCommandLines:
                           if subLine == "": continue

                           subLineStructure = self.__editorBigFrame.getLineStructure(0, [subLine],
                                                                                     False)
                           subLineStructure["fullLine"] = subLine
                           for key in line:
                               if key not in subLineStructure.keys():
                                   subLineStructure[key] = line[key]

                           self.processLine(subLineStructure, linesFeteched)
                           #print(self.__error, subLine)
                           if self.__error == False:
                               txt += subLineStructure["compiled"] + "\n"

                       currentComprass = self.findCompass(statement)
                       comprassLine = self.fuseTempsAndLogical(temps[0], temps[1], currentComprass,
                                                                    name + "End")

                       for opc in self.__branchers:
                           if opc in comprassLine:
                              opcode = opc
                              break

                       if commandName == "do-while":
                          for itemNum in range(0, len(self.__branchers)):
                              if opcode == self.__branchers[itemNum]:
                                 if itemNum % 2 == 0:
                                    itemNum += 1
                                 else:
                                    itemNum -= 1
                                 comprassLine = comprassLine.replace(opcode, self.__branchers[itemNum])
                                 break
                       txt += comprassLine

            line["compiled"] = txt

        elif self.isCommandInLineThat(line, "select"):
             line["magicNumber"] = str(self.__magicNumber)
             self.__magicNumber += 1

             name = self.__currentBank + "_" + line["magicNumber"] + "_Select_"

             #end = self.__editorBigFrame.findEnd(line, line["lineNum"], self.__text)
             end      = self.__editorBigFrame.findEnd(line, line["lineNum"], self.__text)

             cases    = []
             defaults = []

             if  end == False:
                 self.addToErrorList(line["lineNum"],
                                     self.prepareError("compilerErrorNoEnd", "",
                                                       line["command"][0], "",
                                                       str(line["lineNum"] + self.__startLine)))


             else:
                 cases    = self.__editorBigFrame.listAllCommandFromTo("case", self.__text, line["level"]+1,
                          line["lineNum"], end[0] + 1)

                 defaults = self.__editorBigFrame.listAllCommandFromTo("default", self.__text, line["level"]+1,
                          line["lineNum"], end[0] + 1)

                 if len(cases) == 0:
                    self.addToErrorList(line["lineNum"],
                                        self.prepareError("compilerErrorNoCases", "",
                                                           line["command"][0], "",
                                                           str(line["lineNum"] + self.__startLine)))

                 if len(defaults) > 1:
                    self.addToErrorList(line["lineNum"],
                                        self.prepareError("compilerErrorMoreDefault", "",
                                                           line["command"][0], "",
                                                           str(line["lineNum"] + self.__startLine)))

             if self.__error == False:
                endLine = linesFeteched[end[0]]
                endLine["labelsBefore"] = name + "End"

                caseNum = -1

                for case in cases:
                    caseNum += 1
                    caseLine = linesFeteched[case["lineNum"]]
                    caseLine["labelsAfter"] = name + "Case_" + str(caseNum)
                    caseLine["magicNumber"] = line["magicNumber"]

                if len(defaults) > 0:
                    defaultLine = linesFeteched[defaults[0]["lineNum"]]
                    defaultLine["labelsAfter"] = name + "Default"
                    defaultLine["magicNumber"] = line["magicNumber"]


                self.__temps = self.collectUsedTemps()
                params = self.getParamsWithTypesAndCheckSyntax(line)
                if params["param#1"][1] == "variable":

                   if line["param#1"][0] in self.__temps:
                      self.__temps.remove(line["param#1"][0])

                   for case in cases:
                       caseLine = linesFeteched[case["lineNum"]]
                       if caseLine["param#1"][0] in self.__temps:
                          self.__temps.remove(caseLine["param#1"][0])

                   txt = "\tLDA\t" +  params["param#1"][0] + "\n"
                   var = self.__loader.virtualMemory.getVariableByName(params["param#1"][0], self.__currentBank)
                   if var == False:
                      var = self.__loader.virtualMemory.getVariableByName(params["param#1"][0], 'bank1')

                   if var == False:
                      self.addToErrorList(line["lineNum"],
                                          self.prepareError("compilerErrorVarNotFound", params["param#1"][0],
                                                             "", "",
                                                             str(line["lineNum"] + self.__startLine)))
                   if self.__error == False:
                       if var.type != "byte":
                          txt += self.__mainCompiler.convertAnyTo8Bits(var.usedBits)

                       caseNum = -1
                       for case in cases:
                           caseNum += 1
                           caseLine = linesFeteched[case["lineNum"]]
                           subParams = self.getParamsWithTypesAndCheckSyntax(caseLine)

                           cmp = subParams["param#1"][0]

                           if subParams["param#1"][1] not in ["number", "stringConst", "variable"]:
                              self.addToErrorList(line["lineNum"],
                                                  self.prepareError("compilerErrorCaseNotNumber", subParams["param#1"][0],
                                                                    "", params["param#1"][0],
                                                                    str(caseLine["lineNum"] + self.__startLine)))
                           if self.__error: break
                           if subParams["param#1"][1] == "variable":
                              caseVar = self.__loader.virtualMemory.getVariableByName(subParams["param#1"][0], self.__currentBank)
                              if caseVar == False:
                                 caseVar = self.__loader.virtualMemory.getVariableByName(subParams["param#1"][0], "bank1")
                              if caseVar == False:
                                 self.addToErrorList(line["lineNum"],
                                                      self.prepareError("compilerErrorVarNotFound",
                                                                        subParams["param#1"][0],
                                                                        "", "",
                                                                        str(line["lineNum"] + self.__startLine)))

                              if caseVar.type != "byte":
                                 try:
                                     txt = "\tTAX\n\tLDA\t" + cmp + "\n"+ \
                                           self.__mainCompiler.convertAnyTo8Bits(subParams["param#1"][0]) +\
                                           "\tSTA\t" + self.__temps[0] + "\n"
                                     cmp = self.__temps[0]
                                     self.__temps.pop(0)
                                 except:
                                     self.addToErrorList(line["lineNum"],
                                                         self.prepareError("compilerErrorStatementTemps", subParams["param#1"][0],
                                                                           "", "",
                                                                           str(line["lineNum"] + self.__startLine)))
                           if self.__error == False:
                               txt += "\tCMP\t" + cmp + "\n" +\
                                      "\tBEQ\t" + name + "Case_" + str(caseNum) + "\n"

                       if len(defaults) > 0:
                          txt += "\tJMP\t" + name + "Default" + "\n"
                       else:
                          txt += "\tJMP\t" + name + "End" + "\n"

                       line["compiled"] = txt
                else:

                    if params["param#1"][1] == "stringConst":
                        if self.__editorBigFrame.convertStringNumToNumber(self.__constants[params["param#1"][0]]):
                           self.addToErrorList(line["lineNum"],
                                               self.prepareError("compilerErrorMustBe1", params["param#1"][0],
                                                                  "", self.__constants[params["param#1"][0]],
                                                                  str(line["lineNum"] + self.__startLine)))
                    elif params["param#1"][1] == "number":
                        if int(params["param#1"][0].replace("#", "")) != 1:
                           self.addToErrorList(line["lineNum"],
                                                self.prepareError("compilerErrorMustBe1", params["param#1"][0],
                                                                  "", self.__constants[params["param#1"][0]],
                                                                  str(line["lineNum"] + self.__startLine)))

                    if self.__error == False:
                        caseNum = -1
                        for case in cases:
                            caseNum += 1
                            caseLine = linesFeteched[case["lineNum"]]

                            statement = caseLine["param#1"][0]
                            smallerCommands, temps = self.convertStatementToSmallerCodes("comprass",
                                                                                  statement, caseLine)
                            smallerCommandLines = smallerCommands.split("\n")

                            if self.__error == True: break

                            for subLine in smallerCommandLines:
                                if subLine == "": continue

                                subLineStructure = self.__editorBigFrame.getLineStructure(0, [subLine],
                                                                                          False)
                                subLineStructure["fullLine"] = subLine
                                for key in line:
                                    if key not in subLineStructure.keys():
                                        subLineStructure[key] = line[key]

                                self.processLine(subLineStructure, linesFeteched)
                                if self.__error == False:
                                   line["compiled"] += subLineStructure["compiled"] + "\n"

                            currentComprass = self.findCompass(statement)
                            line["compiled"] += self.fuseTempsAndLogical(temps[0], temps[1], currentComprass, name + "Case_" + str(caseNum))

                        if len(defaults) > 0:
                            line["compiled"] += "\tJMP\t" + name + "Default" + "\n"
                        else:
                            line["compiled"] += "\tJMP\t" + name + "End" + "\n"


        elif self.isCommandInLineThat(line, "case") or self.isCommandInLineThat(line, "default"):
            allRelated = self.__editorBigFrame.foundAllRelatedForCaseDefault(line, line["lineNum"], self.__text, False)

            stuffs = []
            for item in allRelated["cases"]:
                stuffs.append(item["lineNum"])

            for item in allRelated["defaults"]:
                stuffs.append(item["lineNum"])

            """
            lastOne = True
            for item in stuffs:
                if item > line["lineNum"]:
                   lastOne = False
                   break
            """

            firstOne = True
            oneSmaller = -1
            empty      = False

            for item in stuffs:
                if item < line["lineNum"]:
                   firstOne = False
                   if item > oneSmaller:
                      oneSmaller = item

            if abs(line["lineNum"] - oneSmaller) == 1:
               empty = True

            if firstOne == False and empty == False:
               line["compiledBefore"] = "\tJMP\t" + self.__currentBank + "_" + str(line["magicNumber"]) + "_Select_End" + "\n"

        elif self.isCommandInLineThat(line, "incr") or self.isCommandInLineThat(line, "decr"):
            if self.isCommandInLineThat(line, "incr"):
               asmCommand = "INC"
               subLineCommand = "add"
               command = self.__loader.syntaxList["incr"]
            else:
               asmCommand = "DEC"
               subLineCommand = "sub"
               command = self.__loader.syntaxList["decr"]

            params  = self.getParamsWithTypesAndCheckSyntax(line)

            var = self.__loader.virtualMemory.getVariableByName(params["param#1"][0],
                                                                self.__currentBank)
            if var == False:
                var = self.__loader.virtualMemory.getVariableByName(params["param#1"][0], "bank1")
            if var == False:
                self.addToErrorList(line["lineNum"],
                                    self.prepareError("compilerErrorVarNotFound",
                                                      params["param#1"][0],
                                                      "", "",
                                                      str(line["lineNum"] + self.__startLine)))

            subLineStructure = self.__editorBigFrame.getLineStructure(0, ["\t" + subLineCommand + "(" + params["param#1"][0] + ", 1)"], False)
            subLineStructure["fullLine"] = line["fullLine"]
            for key in line:
                if key not in subLineStructure.keys():
                   subLineStructure[key] = line[key]

            self.processLine(subLineStructure, linesFeteched)
            line["compiled"] = subLineStructure["compiled"]

        elif self.isCommandInLineThat(line, "leave"):
            if self.__currentSection not in self.__loader.syntaxList[line["command"][0]].sectionsAllowed:
                secondPart = self.__dictionaries.getWordFromCurrentLanguage("sectionNotAllowed").replace("#SECTIONS#",
                             ", ".join(self.__loader.syntaxList[line["command"][0]].sectionsAllowed))

                self.addToErrorList(line["lineNum"], self.prepareError("compilerErrorCommand", "",
                                                                       line["command"][0], "",
                                                                       str(line["lineNum"] + self.__startLine))
                                                                       + " " + secondPart)

            if self.ifCommandInSections("goto") == False:
                self.addToErrorList(line["lineNum"], self.prepareError("compilerErrorBankMissingPairInSection",
                                                                       ", ".join(self.__loader.syntaxList["goto"].sectionsAllowed),
                                                                       line["command"][0], "goto",
                                                                       str(line["lineNum"] + self.__startLine))
                                                                       )

            line["compiled"] = "\tJMP\tLeaveScreenBank" + str(self.__currentBank[-1]) + "\n"

        elif self.isCommandInLineThat(line, "resetGame"):
            if self.__currentSection not in self.__loader.syntaxList[line["command"][0]].sectionsAllowed:
                secondPart = self.__dictionaries.getWordFromCurrentLanguage("sectionNotAllowed").replace("#SECTIONS#",
                             ", ".join(self.__loader.syntaxList[line["command"][0]].sectionsAllowed))

                self.addToErrorList(line["lineNum"], self.prepareError("compilerErrorCommand", "",
                                                                       line["command"][0], "",
                                                                       str(line["lineNum"] + self.__startLine))
                                                                       + " " + secondPart)

            if self.__error == False:
               # Have to rewrite these after reanaming the labels in the kernel!!
               if self.__currentBank == "bank8":
                  line["compiled"] = "\tJMP\tStart\n"
               else:
                  line["compiled"] = "\tJMP\tstart_bank"+ self.__currentBank[-1] +"\n"

        elif self.isCommandInLineThat(line, "resetScreen"):
            if self.__currentSection not in self.__loader.syntaxList[line["command"][0]].sectionsAllowed:
                secondPart = self.__dictionaries.getWordFromCurrentLanguage("sectionNotAllowed").replace("#SECTIONS#",
                             ", ".join(self.__loader.syntaxList[line["command"][0]].sectionsAllowed))

                self.addToErrorList(line["lineNum"], self.prepareError("compilerErrorCommand", "",
                                                                       line["command"][0], "",
                                                                       str(line["lineNum"] + self.__startLine))
                                                                       + " " + secondPart)

            if self.__error == False:
               # Have to rewrite these after reanaming the labels in the kernel!!
               line["compiled"] = "\tJMP\tEnterScreenBank"+ self.__currentBank[-1] +"\n"

        elif self.isCommandInLineThat(line, "goto"):
            params     = self.getParamsWithTypesAndCheckSyntax(line)
            bankToJump = params["param#1"][0].replace("#", "")

            if self.__currentSection not in self.__loader.syntaxList[line["command"][0]].sectionsAllowed:
                secondPart = self.__dictionaries.getWordFromCurrentLanguage("sectionNotAllowed").replace("#SECTIONS#",
                             ", ".join(self.__loader.syntaxList[line["command"][0]].sectionsAllowed))

                self.addToErrorList(line["lineNum"], self.prepareError("compilerErrorCommand", "",
                                                                       line["command"][0], "",
                                                                       str(line["lineNum"] + self.__startLine))
                                                                       + " " + secondPart)

            bankLocks  = self.__loader.virtualMemory.returnBankLocks()
            for lockBank in bankLocks.keys():
                if lockBank[-1] == bankToJump:
                    self.addToErrorList(line["lineNum"],
                                        self.prepareError("compilerErrorBankLocked",
                                                          bankToJump,
                                                          "", "",
                                                          str(line["lineNum"] + self.__startLine)))

                if int(bankToJump) > 8 or int(bankToJump) < 2:
                    self.addToErrorList(line["lineNum"],
                                        self.prepareError("compilerErrorBankOutOfRange",
                                                          bankToJump,
                                                          "", "",
                                                          str(line["lineNum"] + self.__startLine)))

            if self.ifCommandInSections("leave") == False:
                self.addToErrorList(line["lineNum"], self.prepareError("compilerErrorBankMissingPairInSection",
                                                                       ", ".join(self.__loader.syntaxList["leave"].sectionsAllowed),
                                                                       line["command"][0], "leave",
                                                                       str(line["lineNum"] + self.__startLine))
                                                                       )

            if self.__error == False:
               template = self.__loader.io.loadCommandASM("goto").replace("#NUM#", params["param#1"][0].replace("#", ""))
               line["compiled"] = template

        elif self.isCommandInLineThat(line, "subroutine"):
             params = self.getParamsWithTypesAndCheckSyntax(line)
             line["labelsBefore"] = self.__currentBank + "_SubRoutine_" + params["param#1"][0][1:-1] + "\n"

        elif self.isCommandInLineThat(line, "end-subroutine"):
             noRTS    = False
             breakOut = False
             if line["lineNum"] > 0:
                 cLineNum = -1
                 thatC = None
                 for lNum in range(line["lineNum"] - 1, -1, -1):
                     if linesFeteched[lNum]["command"][0] not in self.__noneList:
                         cLineNum = lNum
                         thatC = linesFeteched[lNum]["command"][0]
                         for exitCommand in self.exiters:
                             if thatC == exitCommand or thatC in self.__loader.syntaxList[exitCommand].alias:
                                noRTS = True
                                break
                         breakOut = True
                         if noRTS: break
                     if breakOut: break

             if noRTS == False: line["compiled"] = "\tRTS\n"

        elif self.isCommandInLineThat(line, "return"):
             params = self.getParamsWithTypesAndCheckSyntax(line)
             if params["param#1"][0] == "variable":
                var = self.__loader.virtualMemory.getVariableByName(params["param#1"][0],
                                                                     self.__currentBank)
                if var == False:
                   var = self.__loader.virtualMemory.getVariableByName(params["param#1"][0], "bank1")
                if var == False:
                   self.addToErrorList(line["lineNum"],
                                       self.prepareError("compilerErrorVarNotFound",
                                                          params["param#1"][0],
                                                          "", "",
                                                          str(line["lineNum"] + self.__startLine)))

                if self.__error == False:
                   line["compiled"] = "\tLDA\t" + params["param#1"][0] + "\n"
                   if var.type != "variable":
                      line["compiled"] += self.__mainCompiler.convertAnyTo8Bits(var.usedBits)

             else:
                 line["compiled"] = "\tLDA\t#" + params["param#1"][0].replace("#", "") + "\n"

             line["compiled"] += "\tRTS\n"

        elif self.isCommandInLineThat(line, "screen"):
             params = self.getParamsWithTypesAndCheckSyntax(line)
             line["labelsBefore"] = self.__currentBank + "_Screen_" + params["param#1"][0][1:1] + "\n"
             #line["compiled"] = "\tLDX\titem\n\tTXS\n"

        elif self.isCommandInLineThat(line, "end-screen"):
             line["compiled"] = "\tTSX\n\tSTX\titem\n\tRTS\n"

        line["compiled"] = self.LDATAYLDA(self.detectUnreachableCode(self.checkForNotNeededExtraLDA(line["compiled"])))
        if line["compiled"] != "": self.checkASMCode(line["compiled"], line)
        if self.__error == True: line["compiled"] = ""

    def ifCommandInSections(self, commandName):
        command = None

        for c in self.__loader.syntaxList.keys():
            if c == commandName or commandName in self.__loader.syntaxList[c].alias:
               command = self.__loader.syntaxList[c]
               break

        for sect in command.sectionsAllowed:
            if sect == self.__currentSection:
               lines = self.__fullText
            else:
               lines = self.__loader.virtualMemory.codes[self.__currentBank][sect].code.split("\n")

            for line in lines:
                lineStructure = self.__editorBigFrame.getLineStructure(0, [line], False)
                if lineStructure["command"][0] == commandName:
                   return True

        return False

    def createSubLineForPower(self, line, linesFeteched):
        from copy import deepcopy

        self.__temps = self.collectUsedTemps()
        try:
            thisOne = self.__temps[0]
            self.__temps.pop(0)

        except:
            self.addToErrorList(line["lineNum"],
                                self.prepareError("compilerErrorStatementTemps", statement,
                                                  "", "", str(line["lineNum"] + self.__startLine)))

        subLine = deepcopy(line)
        subLine["command"][0] = "*"
        subLine["param#2"][0] = thisOne

        subLine["fullLine"] = "*(" + subLine["param#1"][0] + ", " + subLine["param#1"][0]
        if subLine["param#3"][0] in self.__noneList:
            subLine["fullLine"] += ")"
        else:
            subLine["fullLine"] += ", " + subLine["param#3"][0] + ")"

        self.processLine(subLine, linesFeteched)
        return subLine

    def checkIfItIsWritingInItem(self, start, end, level, text):
        listOfCommands = self.__editorBigFrame.listAllCommandFromTo(None, text, None, start, end + 1)

        for thisLineStructure in listOfCommands:
            if "item" in [
                thisLineStructure["param#1"][0],
                thisLineStructure["param#2"][0],
                thisLineStructure["param#3"][0]]:
                c = thisLineStructure["command"][0]

                for key in self.__loader.syntaxList.keys():
                    if key == c or c in self.__loader.syntaxList[key].alias:
                        if self.__editorBigFrame.doesItWriteInParam(thisLineStructure, "param#" + \
                                                                    str([thisLineStructure["param#1"][0],
                                                                        thisLineStructure["param#2"][0],
                                                                        thisLineStructure["param#3"][0]].index("item")+1), "compiler"

                                                   ):
                            return True
        return False

    def checkForNotNeededExtraLDA(self, lineCompiled):
        lineLines = lineCompiled.split("\n")

        for letter in ["A", "Y", "X"]:
            opcode1 = "LD" + letter
            opcode2 = "ST" + letter

            if opcode1 not in lineCompiled: continue

            for currentLineNum in range(0, len(lineLines)):
                line = lineLines[currentLineNum].replace("\t", " ")
                if line == "" or line.isspace() or line[0] not in ["\t", " "]:
                   continue

                opC1, opR1 = self.getOpCodeAndOperandFromASMLine(line)

                if opC1 == opcode1:
                   for compareLineNum in range(currentLineNum - 1, -1, -1):
                       if compareLineNum < 0: break
                       compareLine = lineLines[compareLineNum]
                       if compareLine == "": continue

                       opC2, opR2 = self.getOpCodeAndOperandFromASMLine(compareLine)

                       if opC2[0:2] not in ("ST", "LD"):
                          break

                       if opR1 == opR2 and opC1[2] == opC2[2]:
                          lineLines[currentLineNum] = ""
                          break

                elif opC1 == opcode2:
                    for compareLineNum in range(currentLineNum - 1, -1, -1):
                        if compareLineNum < 0: break
                        compareLine = lineLines[compareLineNum].replace("\t", " ")
                        if compareLine == "" or line[0] not in ["\t", " "]: continue

                        opC2, opR2 = self.getOpCodeAndOperandFromASMLine(compareLine)

                        if opC2[0:2] not in ("ST", "LD"):
                            break

                        if opC2 == opcode1:
                           break

                        if opR1 == opR2 and opC1[2] == opC2[2]:
                            lineLines[currentLineNum] = ""
                            break
        returnB = ""
        for line in lineLines:
            if line != "": returnB += line + "\n"

        return returnB

    def getOpCodeAndOperandFromASMLine(self, line):
        asmStructure = self.__editorBigFrame.getLineStructure(0, [line], False)
        if self.isCommandInLineThat(asmStructure, "asm"):
           if asmStructure["param#2"][0] not in self.__noneList:
              asmLine = asmStructure["param#1"][0][1:-1] + " " + asmStructure["param#2"][0][1:-1]
           else:
              asmLine = asmStructure["param#1"][0][1:-1]
        else:
            asmLine = line.replace("\t", " ")

        asmLine = asmLine.split(" ")
        newLine = []

        for item in asmLine:
            if item != "":
               newLine.append(item)

        for nnn in range(0, 2-len(newLine)):
            newLine.append("")

        return newLine[0], newLine[1]

    def shiftOnVars(self, params, line, command):
        txt      = ""

        var2 = self.__loader.virtualMemory.getVariableByName2(params["param#2"][0])
        if var2 == False:
            self.addToErrorList(line["lineNum"], self.prepareError("compilerErrorVarNotFound", params["param#1"][0],
                                                                   "", "",
                                                                   str(line["lineNum"] + self.__startLine)))
        if params["param#1"][1] == "variable":
            var1 = self.__loader.virtualMemory.getVariableByName2(params["param#1"][0])
            if var1 == False:
                self.addToErrorList(line["lineNum"], self.prepareError("compilerErrorVarNotFound", params["param#1"][0],
                                                                       "", "",
                                                                       str(line["lineNum"] + self.__startLine)))
            else:
                if var1.type != "byte":
                    convert = self.__mainCompiler.convertAnyTo8Bits(var1.usedBits)
                    txt = "\tLDA\t" + params["param#1"][0] + "\n" + convert + "\tTAY\n"

                else:
                    txt = "\tLDY\t" + params["param#1"][0] + "\n"

        else:
            times = self.__editorBigFrame.convertStringNumToNumber(params["param#1"][0])

            if times < 3:
               conv1 = ""
               conv2 = ""

               if var2.type != "byte":
                   conv1 = self.__mainCompiler.convertAnyTo8Bits(var2.usedBits)
                   conv2 = self.__mainCompiler.save8bitsToAny2(var2.usedBits, params["param#2"][0])

               line["compiled"] = "\tLDA\t" + params["param#2"][0] + "\n" + conv1 +\
                                   times * ("\t" + command + "\n") + conv2 + "\tSTA\t" + params["param#2"][0] + "\n"
               return
            else:
               txt = "\tLDY\t#" + params["param#1"][0].replace("#", "") + "\n"

        conv1 = ""
        conv2 = ""

        magic = str(self.__magicNumber)
        self.__magicNumber += 1

        name = self.__currentBank + "_Shifting_" + magic + "_"

        if var2.type != "byte":
            conv1 = self.__mainCompiler.convertAnyTo8Bits(var2.usedBits)
            conv2 = self.__mainCompiler.save8bitsToAny2(var2.usedBits, params["param#2"][0])


        txt += "\tCPY\t#0\n\tBEQ\t" + name + "_End" + "\n"         +\
               "\tLDA\t" + params["param#2"][0] + "\n" + conv1     +\
               name + "Loop" + "\n\t" + command + "\n"             +\
               "\tDEY\n\tCPY\t#0\n\tBNE\t" + name + "Loop" + "\n"  +\
               name + "End" + "\n" + conv2 + "\tSTA\t" + params["param#2"][0] + "\n"

        line["compiled"] = txt

    def collectUsedTemps(self):
        lineNum      = self.__useThese[0]
        linesFetched = self.__useThese[1]

        startNum     = lineNum
        endNum       = lineNum
        usedTemps    = []
        currentLevel = linesFetched[lineNum]["level"]

        temps = []
        for num in range(1, 20):
            num = str(num)
            if len(num) == 1: num = "0" + num
            temps.append("temp" + num)

        for lNum in range(lineNum, -1, -1):
            if linesFetched[lNum]["level"] <= currentLevel:
               for paramNum in range(1,4):
                   paramNum = "param#" + str(paramNum)
                   if linesFetched[lNum][paramNum][0] in temps:
                      temps.remove(linesFetched[lNum][paramNum][0])

               for temp in temps:
                   if temp in linesFetched[lNum]["compiled"]:
                      temps.remove(temp)

            if linesFetched[lNum]["level"] == 0:
               startNum = linesFetched[lNum]["lineNum"]
               break

        for lNum in range(lineNum, len(linesFetched)):
            if linesFetched[lNum]["level"] <= currentLevel:
                for paramNum in range(1, 4):
                    paramNum = "param#" + str(paramNum)
                    if linesFetched[lNum][paramNum][0] in temps:
                        temps.remove(linesFetched[lNum][paramNum][0])

                for temp in temps:
                    if temp in linesFetched[lNum]["compiled"]:
                        temps.remove(temp)

            if linesFetched[lNum]["level"] == 0:
                endNum = linesFetched[lNum]["lineNum"]
                break

        #print(temps)
        return temps

    def checkIfCanShiftBits(self, params, varHolder, numberHolder, line, shiftDir):
        theNum = int(self.__editorBigFrame.convertStringNumToNumber(params[numberHolder][0]))
        if self.isPowerOfTwo(theNum) == False: return

        sourceVar = self.__loader.virtualMemory.getVariableByName2(params[varHolder][0])
        if sourceVar == False:
           self.addToErrorList(line["lineNum"], self.prepareError("compilerErrorVarNotFound", params[varHolder][0],
                                                                   "", "",
                                                                   str(line["lineNum"] + self.__startLine)))
        if "param#3" not in params.keys():
            destVar = sourceVar
            params["param#3"] = params["param#1"]
        else:
            destVar = self.__loader.virtualMemory.getVariableByName2(params["param#3"][0])
            if destVar == False:
               self.addToErrorList(line["lineNum"], self.prepareError("compilerErrorVarNotFound", params["param#3"][0],
                                                                       "", "",
                                                                       str(line["lineNum"] + self.__startLine)))

        times = self.howManyTimesThePowerOfTwo(theNum)
        if times > 2: self.shiftOnVars(params, line, shiftDir)
        else:
            if sourceVar == destVar and sourceVar.type == "byte":
               line["compiled"] = times * ("\t" + shiftDir + "\t" + params[varHolder][0] + "\n")
               return

            shifting = times * ("\t" + shiftDir + "\n")
            convert1 = ""
            convert2 = ""

            if sourceVar.type != "byte":
               convert1 = self.__mainCompiler.convertAnyTo8Bits(sourceVar.usedBits)

            if destVar.type != "byte":
               convert2 = self.__mainCompiler.save8bitsToAny2(destVar.usedBits, params["param#3"][0])

            line["compiled"] = "\tLDA\t" + params[varHolder][0] + "\n" +\
                               convert1 + shifting + convert2 + "\tSTA\t" + params["param#3"][0] + "\n"

    def prepareDiv(self, params, aaveThisOne):
        saveThisOne = "ST" + aaveThisOne
        changeText = {}

        var1 = self.__loader.virtualMemory.getVariableByName2(params["param#1"][0])
        var2 = self.__loader.virtualMemory.getVariableByName2(params["param#2"][0])
        var3 = self.__loader.virtualMemory.getVariableByName2(params["param#3"][0])

        changeText["#MAGIC#"] = str(self.__magicNumber)
        changeText["#BANK#"]  = self.__currentBank
        changeText["#SECTION#"]  = self.__currentSection

        self.__magicNumber += 1

        self.__temps = self.collectUsedTemps()

        try:
            first = self.__temps[0]
            self.__temps.pop(0)
        except:
            self.addToErrorList(self.__thisLine["lineNum"],
                                self.prepareError("compilerErrorStatementTemps", params["param#2"][0],
                                                  "", "",
                                                  str(self.__thisLine["lineNum"] + self.__startLine)))

        if self.__error == False:
            if var1 != False:
                if var1.type != "byte":
                    changeText["!!!to8Bit1!!!"] = self.__mainCompiler.convertAnyTo8Bits(var1.usedBits)

            if var2 != False:
                if var2.type != "byte":
                    changeText["!!!to8Bit2!!!"] = "\tLDA\t" + params["param#2"][0] + "\n" + \
                                                  self.__mainCompiler.convertAnyTo8Bits(var2.usedBits)
                    changeText["#VARTEMP#"]     = first
                    changeText["!!!staTEMP!!!"] = "\tSTA\t" + first + "\n"
                    changeText["!!!LDAVAR2!!!"] = "\tLDA\t" + params["param#2"][0] + "\n"

                else:
                    changeText["#VARTEMP#"] = params["param#2"][0]
        else:
            changeText["#VARTEMP#"] = params["param#2"][0]

        if var3 != False:
           if var3.type != "byte":
              changeText["!!!from8bit!!!"] = self.__mainCompiler.save8bitsToAny2(var3.usedBits, params["param#3"][0])

        if saveThisOne == "A":
           changeText["#SAVECOMMAND#"] = "STA"
        else:
           changeText["#SAVECOMMAND#"] = "STY"
           if "!!!from8bit!!!" in changeText.keys():
              changeText["!!!TAY!!!"]     = "\tTAY"
              changeText["!!!TYA!!!"]     = "\tTYA"


        return changeText



    def saveAValue(self, params, paramName1, paramName2, line):
        txt = ""
        itWas0 = False

        if params[paramName1][1] == "variable":
           var1 = self.__loader.virtualMemory.getVariableByName(params[paramName1][0], self.__currentBank)
           if var1 == False:
              var1 = self.__loader.virtualMemory.getVariableByName(params["param#1"][0], "bank1")

           if var1 == False:
              self.addToErrorList(line["lineNum"], self.prepareError("compilerErrorVarNotFound", params[paramName1][0],
                                                                     "", "",
                                                                    str(line["lineNum"] + self.__startLine)))

           txt += "\tLDA\t" + params[paramName1][0] + "\n"
           if var1.type != "byte": txt += self.__mainCompiler.convertAnyTo8Bits(var1.usedBits)
        else:
           txt += "\tLDA\t#" + params[paramName1][0].replace("#", "") + "\n"
           if self.isIt(params[paramName1][0], 0) or self.isIt(params[paramName1][0], 255): itWas0 = True

        var2 = self.__loader.virtualMemory.getVariableByName(params[paramName2][0], self.__currentBank)
        if var2 == False:
           var2 = self.__loader.virtualMemory.getVariableByName(params[paramName2][0], "bank1")

        if var2 == False:
           self.addToErrorList(line["lineNum"], self.prepareError("compilerErrorVarNotFound", params[paramName2][0],
                                                                     "", "",
                                                                    str(line["lineNum"] + self.__startLine)))
        if var2.type != "byte":
           if itWas0 == True:
              command = None
              if self.isIt(params[paramName1][0], 0):
                 command  = "AND"
                 forCOMM  = ""
                 for num in range(7, -1, -1):
                     if num in var2.usedBits:
                        forCOMM += "0"
                     else:
                        forCOMM += "1"
              else:
                  command = "ORA"
                  forCOMM = ""
                  for num in range(7, -1, -1):
                      if num in var2.usedBits:
                          forCOMM += "1"
                      else:
                          forCOMM += "0"

              return "\tLDA\t#" + params[paramName2][0] + "\n\t" + command + "\t#%" + forCOMM + "\n\tSTA\t" + params[paramName2][0] + "\n"
           else:
               saver = self.__mainCompiler.save8bitsToAny2(var2.usedBits, params[paramName2][0])

               if params[paramName1][1] == "number":
                  maxNumber = int("0b" + ("1" * len(var2.usedBits)), 2)
                  if maxNumber > self.__editorBigFrame.convertStringNumToNumber(params[paramName1][0]):
                     saver = saver.split("\n")
                     saver.pop(5)
                     saver = "\n".join(saver)
               txt += saver

        if itWas0:
           for opcode in ("ASL", "LSR", "ROL", "ROR"):
               txt = txt.replace("\t" + opcode + "\n", "")

        txt += "\tSTA\t" + params[paramName2][0] + "\n"
        return txt

    def fuseTempsAndLogical(self, temp1, temp2, comprass, caseName):
        comprassDict = self.__editorBigFrame.getComprassionDict()
        del comprassDict["all"]

        thatKey = None
        for key in comprassDict:
            if comprass in comprassDict[key]:
               thatKey = key

        allTheOnes = {
            "validNotEQ":           "\tLDA\t" + temp1 + "\n\tCMP\t" + temp2 + "\n\tBNE\t" + caseName + "\n",
            "validEQ":              "\tLDA\t" + temp1 + "\n\tCMP\t" + temp2 + "\n\tBEQ\t" + caseName + "\n",
            "validLargerThan":      "\tLDA\t" + temp2 + "\n\tCMP\t" + temp1 + "\n\tBCC\t" + caseName + "\n",
            "validSmallerThan":     "\tLDA\t" + temp1 + "\n\tCMP\t" + temp2 + "\n\tBCC\t" + caseName + "\n",
            "validLargerThanOrEQ":  "\tLDA\t" + temp1 + "\n\tCMP\t" + temp2 + "\n\tBCS\t" + caseName + "\n",
            "validSmallerThanOrEQ": "\tLDA\t" + temp2 + "\n\tCMP\t" + temp1 + "\n\tBCS\t" + caseName + "\n"
        }

        return allTheOnes[thatKey]

    def isThereAnyLargerThan255(self, data):
        import re

        numbers = re.findall(r'\d+', data)
        numberDict = {}
        numberList = []

        for num in numbers:
            numNum = int(num)
            if numNum > 255:
                numberDict[numNum] = str(numNum % 256)
                numberList.append(numNum)

        numberList.sort(reverse=True)
        for number in numberList:
            data = data.replace(str(number), numberDict[number])

        return (data)

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

    def prepareMulti(self, params):
        changeText = {}

        var1 = self.__loader.virtualMemory.getVariableByName2(params["param#1"][0])
        var2 = self.__loader.virtualMemory.getVariableByName2(params["param#2"][0])
        var3 = self.__loader.virtualMemory.getVariableByName2(params["param#3"][0])

        changeText["#MAGIC#"] = str(self.__magicNumber)
        changeText["#BANK#"]  = self.__currentBank
        changeText["#SECTION#"]  = self.__currentSection

        self.__magicNumber += 1

        self.__temps = self.collectUsedTemps()

        try:
            first = self.__temps[0]
            self.__temps.pop(0)
        except:
            self.addToErrorList(self.__thisLine["lineNum"],
                                self.prepareError("compilerErrorStatementTemps", params["param#1"][0],
                                                  "", "",
                                                  str(self.__thisLine["lineNum"] + self.__startLine)))
        if self.__error == False:
            if var1 != False:
                if var1.type != "byte":
                    changeText["!!!to8Bit1!!!"] = self.__mainCompiler.convertAnyTo8Bits(var1.usedBits)
                    changeText["#VARTEMP#"] = first
                    changeText["!!!staTEMP!!!"] = "\tSTA\t" + first + "\n"

                else:
                    changeText["#VARTEMP#"] = params["param#1"][0]
            else:
                changeText["#VARTEMP#"] = params["param#1"][0]

            if var2 != False:
                if var2.type != "byte":
                    changeText["!!!to8Bit2!!!"] = "\tLDA\t" + params["param#2"][0] + "\n" + \
                                                  self.__mainCompiler.convertAnyTo8Bits(var2.usedBits)
            if var3 != False:
               if var3.type != "byte":
                  changeText["!!!from8bit!!!"] = self.__mainCompiler.save8bitsToAny2(var3.usedBits, params["param#3"][0])

        return changeText

    def preparePow(self, params, subLine, line):
        var1NotByte = False

        if params["param#1"][1] == "variable":
            var1 = self.__loader.virtualMemory.getVariableByName2(subLine["param#1"][0])
            if var1 == False:
                self.addToErrorList(line["lineNum"],
                                    self.prepareError("compilerErrorVarNotFound", params["param#2"][0],
                                                      "", "",
                                                      str(line["lineNum"] + self.__startLine)))
            if var1.type != "byte": var1NotByte = True
        else:
            var1 = False

        if params["param#2"][1] == "variable":
            var2 = self.__loader.virtualMemory.getVariableByName2(subLine["param#2"][0])
            if var2 == False:
                self.addToErrorList(line["lineNum"], self.prepareError("compilerErrorVarNotFound", params["param#2"][0],
                                                                       "", "",
                                                                       str(line["lineNum"] + self.__startLine)))
        else:
            var2 = False

        template = self.__loader.io.loadCommandASM("pow")
        if params["param#2"][1] == "number":
            val = int(self.__editorBigFrame.convertStringNumToNumber(params["param#2"][0]))
            if val > 127:
                template = template.replace("#VAR#", "#" + str(val + 1)) \
                    .replace("!!!DECR!!!", "\tDEX\n\tCMP\t#0\n\tBEQ\t#BANK#_Pow_#MAGIC#_End\n")
            else:
                template = template.replace("#VAR#", "#" + str(val - 1)) \
                    .replace("!!!DECR!!!", "\tDEX\n\tBMI\t#BANK#_Pow_#MAGIC#_End\n")
        else:
            template = template.replace("#VAR#", params["param#2"][0])
            if var2.type != "byte":
                template = template.replace("!!!to8Bit1!!!", self.__mainCompiler.convertAnyTo8Bits(var.usedBits))

            template = template.replace("!!!DECR!!!", "\tDEX\n\tCMP\t#0\n\tBEQ\t#BANK#_Pow_#MAGIC#_End\n").replace(
                "!!!INCR!!!", "\tINX\n")

        if "param#3" in params.keys() or var1NotByte:
            if "param#3" in params.keys():
                var3 = self.__loader.virtualMemory.getVariableByName2(subLine["param#3"][0])
                if var3 == False:
                    self.addToErrorList(line["lineNum"],
                                        self.prepareError("compilerErrorVarNotFound", params["param#2"][0],
                                                          "", "",
                                                          str(line["lineNum"] + self.__startLine)))
            else:
                params["param#3"] = params["param#1"]
                var3              = var1

            self.__temps = self.collectUsedTemps()
            try:
                thisOne   = self.__temps[0]
                self.__temps.pop(0)
                otherOne  = self.__temps[0]
                self.__temps.pop(0)

            except:
                self.addToErrorList(line["lineNum"],
                                    self.prepareError("compilerErrorStatementTemps", statement,
                                                      "", "", str(line["lineNum"] + self.__startLine)))

            if self.__error == False:
               subLine["param#1"][0] = thisOne
               subLine["param#2"][0] = otherOne
               subLine["param#3"][0] = thisOne
               #print(subLine)

               subLine["fullLine"] = subLine["fullLine"] = "*(" + subLine["param#1"][0] + ", " + subLine["param#2"][0] + ")"
               self.processLine(subLine, self.__useThese[1])

               txt1 = "\tLDA\t" + params["param#1"][0] + "\n"
               if var1 != False:
                  if var1.type != "byte": txt1 += self.__mainCompiler.convertAnyTo8Bits(var1.usedBits)
               txt1 += "\tSTA\t" + thisOne + "\n"

               txt3 = "\tLDA\t" + thisOne + "\n"
               if var3 != False:
                  if var3.type != "byte": txt3 += self.__mainCompiler.save8bitsToAny2(var3.usedBits, params["param#3"][0])
               txt3 += "\tSTA\t" + params["param#3"][0] + "\n"

               template = template.replace("!!!TEMPVARLOAD!!!", txt1).replace("!!!TEMPVARSAVE!!!", txt3)\
                                  .replace("!!!SELF!!!", "\tSTA\t" + subLine["param#2"][0] + "\n")
        else:
            template = template.replace("!!!SELF!!!",
                                        "\tLDA\t" + subLine["param#1"][0] + "\n\tSTA\t" + subLine["param#2"][0] + "\n")


        if self.__error == False:
            template = template.replace("!!!Multi!!!", subLine["compiled"]) \
                .replace("#BANK#", self.__currentBank).replace("#MAGIC#", str(self.__magicNumber))
            self.__magicNumber += 1

            return template
        else:
            return ""

    def prepareAdd(self, params):
        changeText = {}

        var1 = self.__loader.virtualMemory.getVariableByName2(params["param#1"][0])
        var2 = self.__loader.virtualMemory.getVariableByName2(params["param#2"][0])
        var3 = self.__loader.virtualMemory.getVariableByName2(params["param#3"][0])

        self.__temps = self.collectUsedTemps()

        try:
            first = self.__temps[0]
            self.__temps.pop(0)
        except:
            self.addToErrorList(self.__thisLine["lineNum"],
                                self.prepareError("compilerErrorStatementTemps", params["param#1"][0],
                                                  "", "",
                                                  str(self.__thisLine["lineNum"] + self.__startLine)))

        if self.__error == False:
            if var1 != False:
               if var1.type != "byte":
                  changeText["!!!to8Bit1!!!"] = self.__mainCompiler.convertAnyTo8Bits(var1.usedBits)

            if var2 != False:
               if var2.type != "byte":
                  changeText["#VAR02#"] = first
                  changeText["!!!to8Bit2!!!"] = "\tLDA\t" + params["param#2"][0] + "\n" +\
                                                self.__mainCompiler.convertAnyTo8Bits(var2.usedBits) + "\tSTA\t" + first
            if var3 != False:
               if var3.type != "byte":
                  changeText["!!!from8bit!!!"] = self.__mainCompiler.save8bitsToAny2(var3.usedBits, params["param#3"][0])

        return changeText

    def collectLabelsFromRoutines(self, labels):
        for key in self.toRoutines.keys():
            lines = self.toRoutines[key].replace("\r", "").split("\n")
            for line in lines:
                if line == "" or line.isspace() or line[0] in ["\t", " "]:
                   continue

                if line.replace("\t", " ")[0] != " " and "!!!" not in line:
                    labels.append(line)
                    if self.__currentBank in line:
                       labels.append(line.replace(self.__currentBank, "#BANK#"))
                    else:
                       labels.append(line.replace("#BANK#", self.__currentBank))

    def checkASMCode(self, template, lineStructure):
        lines = template.split("\n")

        labels = []
        for line in lines:
            if line.replace("\t", " ").startswith(" ") == False and "!!!" not in line:
                labels.append(line.replace("\n", ""))

        self.collectLabelsFromRoutines(labels)

        for line in lines:
            full = line

            if line.replace("\t", " ").startswith(" ") == False: continue
            if line[0] in ["*", "#"]: continue

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

            #print(line[0].upper() in self.__branchers, line[0].upper() in self.__jumpers)

            if line[0].upper() in self.__branchers or line[0].upper() in self.__jumpers:

               if self.isCommandInLineThat(lineStructure, "asm"):
                   for replacer in self.__replacers.keys():
                       replaceIt = self.__replacers[replacer]

                       if replacer in line[1]: line[1] = line[1].replace(replacer, replaceIt)
                       for key in lineStructure.keys():
                           if type(lineStructure[key]) == list and lineStructure[key] != []:
                               if lineStructure[key][0] not in self.__noneList:
                                  lineStructure[key][0] = lineStructure[key][0].replace(replacer, replaceIt)
                                  self.__changeThese[replacer] = replaceIt
               """ 
               print(line, line[1] in labels,
                  "*" in line[1],
                  "#" in line[1],
                  line[1] in self.__fullTextLabels,
                  line[1] in self.__labelsOfMainKenrel)
               """

               if line[1] in labels                     or\
                  line[1] in self.__fullTextLabels      or\
                  line[1][0] == "*"                     or\
                  line[1] in self.__labelsOfMainKenrel:
                  continue

            if self.isCommandInLineThat(lineStructure, "asm"):
                for replacer in self.__replacers.keys():
                    replaceIt = self.__replacers[replacer]

                    if replacer in line[0]:
                        line[0] = line[0].replace(replacer, replaceIt)
                        for key in lineStructure.keys():
                            if type(lineStructure[key]) == list and lineStructure[key] != []:
                                if lineStructure[key][0] not in self.__noneList:
                                    lineStructure[key][0] = lineStructure[key][0].replace(replacer, replaceIt)
                                    self.__changeThese[replacer] = replaceIt

                if line[0] in labels or line[0] in self.__fullTextLabels:
                   lineStructure["level"] = -1

                   if self.__fullTextLabels.count(line[0]) > 1:
                      self.addToErrorList(lineStructure["lineNum"],
                                          self.prepareErrorASM("compilerErrorASMDuplicateLabel",
                                                                "", line[0],
                                                                lineStructure["lineNum"]))

                   if self.__labelsOfMainKenrel.count(line[0]) > 0:
                      self.addToErrorList(lineStructure["lineNum"],
                                          self.prepareErrorASM("compilerErrorASMDKernelLabel",
                                                                "", line[0],
                                                                lineStructure["lineNum"]))

                   if len(line[0]) < 8:
                      self.addToErrorList(lineStructure["lineNum"],
                                           self.prepareErrorASM("compilerErrorASMKernelLabelShort",
                                                                "", line[0],
                                                                lineStructure["lineNum"]))

                continue


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

                   if line[1].split(",")[0] in labels or \
                      line[1].split(",")[0] in self.__fullTextLabels or \
                      line[1].split(",")[0] in self.__labelsOfMainKenrel:

                      if "," not in line[1]:
                          if lineSettings["format"] == "aaaa":
                             foundCommand = True
                             break
                      else:
                          if "," in lineSettings["format"]:
                             splitFormat = lineSettings["format"].split(",")
                             splitValue  = value.split(",")
                             if splitValue[1] == splitFormat[1]:
                                foundCommand = True
                                break

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
                               if beforeComma != "item":
                                  mode = "read"
                               else:
                                  mode = "both"
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
        labels = []
        self.collectLabelsFromRoutines(labels)

        if lineSettings["format"][0] == "#"    and\
           value.split(",")[0] not in labels   and\
           value[0] != "#": return False

        if lineSettings["format"][0] != "#"    and\
           value.split(",")[0] not in labels   and\
           value[0] == "#": return False

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

        if beforeCommaValue in labels:
           thisIs = "aaaa," + afterCommaValue
           if lineSettings["format"] == thisIs: return True

        if "#" in beforeCommaValue and beforeCommaValue not in labels:
           allA = "#AA"
        else:
           allA = re.sub(r'[0-9a-fA-F]', "A", beforeCommaValue).replace("$", "")

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
               #print(command.params)
               paramType = command.params[num-1]
               mustHave  = True
               if paramType.startswith("{"):
                  mustHave = False
                  paramType = paramType[1:-1]

               if self.__loader.syntaxList[line["command"][0]].flexSave == True and num == 1 and \
                  line["param#" + str(len(command.params))][0] in self.__noneList:
                  paramType = "variable"
                  ioMethod  = "write"

               paramTypes = paramType.split("|")

               if self.__editorBigFrame.doesItWriteInParam(line, "param#"+str(num), "compiler") == False:
                  ioMethod = "read"

               foundIt               = False
               param                 = None
               paramTypeAndDimension = None
               for param in paramTypes:
                   foundIt, paramTypeAndDimension = self.__editorBigFrame.checkIfParamIsOK(param, curParam,
                                                                                           ioMethod, None,
                                                                                           "dummy", mustHave, "param#"+str(num),
                                                                                           line, self.__text)
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
                      "iteralError": {},
                      "infiniteLoop": {},
                      "mustBePowerOf2": {},
                      "mustBeSmaller": {},
                      "noSubRoutineForReturn": {"#COMMAND#": line["command"][0]},
                      "noEndSubRoutineForReturn": {"#COMMAND#": line["command"][0]},
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
        #raise ValueError

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
        if line["command"][0] == command or line["command"][0] in self.__loader.syntaxList[command].alias:
           return True
        return False

    def convertStatementToSmallerCodes(self, command, statement, line):
        side1            = ""
        side2            = ""
        statementData    = []
        statementFetched = []
        temps            = []
        commands         = ""

        self.__temps = self.collectUsedTemps()

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
               currentComprass = self.findCompass(statement)
               if currentComprass == False:
                  statement = str(expand(simplify(statement)))
               else:
                  statement = statement.split(currentComprass)
                  for num666 in range(0, len(statement)):
                      statement[num666] = str(expand(simplify(statement[num666])))
                  statement = currentComprass.join(statement)

               statementData = self.__editorBigFrame.getStatementStructure(statement, needComprassion, stringAllowed, 0,
                                                                           line)
               for item in statementData:
                   if item["word"] in ["(", ")"]:
                      self.addToErrorList(line["lineNum"],
                                          self.prepareError("compilerErrorStatementComplex", statement,
                                                             "", "", str(line["lineNum"] + self.__startLine)))
                      break

               if self.__error == False:
                  if command == "calc":
                     commands = self.convertToCommands(statement, line, None)
                  else:
                     # currentComprass = self.findCompass(statement)

                     if currentComprass == False:
                         self.addToErrorList(line["lineNum"],
                                             self.prepareError("compilerErrorComprassNotFound", statement,
                                                               "", "", str(line["lineNum"] + self.__startLine)))
                     if self.__error == False:
                        newT = []
                        for temp in self.__temps:
                             if temp not in statement:
                                 newT.append(temp)

                        self.__temps = newT
                        try:
                            temp1 = self.__temps[0]
                            self.__temps.pop(0)
                            temp2 = self.__temps[0]
                            self.__temps.pop(0)
                        except:
                            self.addToErrorList(line["lineNum"],
                                         self.prepareError("compilerErrorStatementTemps", statement,
                                                           "", "", str(line["lineNum"] + self.__startLine)))

                        if self.__error == False:
                           txt = ""
                           statement = statement.split(currentComprass)

                           #print(statement)
                           txt += self.convertToCommands(statement[0], line, temp1)
                           txt += self.convertToCommands(statement[1], line, temp2)

                           commands = txt
                           temps = [temp1, temp2]

        if self.__error == False:
           return commands, temps
        else:
           return False, temps

    def findCompass(self, statement):
        comprassDict = self.__editorBigFrame.getComprassionDict()["all"]
        fullDict     = {}

        largest = 0

        for item in comprassDict:
            if len(item) not in fullDict.keys():
               fullDict[len(item)] = []
               if len(item) > largest: largest = len(item)

            fullDict[len(item)].append(item)

        for num in range(largest, 0, -1):
            if num in fullDict.keys():
               for item in fullDict[num]:
                   if item in statement:
                      return item

        return False



    def convertToCommands(self, statement, line, saveHere):
        newT = []

        for temp in self.__temps:
            if temp not in statement:
               newT.append(temp)

        self.__temps = newT

        statement = statement.split(" ")

        preCalc = []
        finals  = []

        for num in range(0, len(statement)):
            item = statement[num]
            if item == "": continue

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

        if saveHere == None:
           saveHere   = line["param#1"][0]
        returnBack = "".join(preCalc)

        first = True
        if len(finals) >= 2:
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
        else:
            isItNum = False
            try:
                teszt   = int(finals[0].replace("#", ""))
                isItNum = True
            except:
                pass

            extra = ""
            if isItNum or finals[0][0] in ["%", "$"]:
               if finals[0][0] != "#":
                  finals[0]     = "#" + finals[0]
            else:
                var = self.__loader.virtualMemory.getVariableByName(finals[0], self.__currentBank)
                if var == False:
                   var = self.__loader.virtualMemory.getVariableByName(finals[0], "bank1")
                if var == False:
                   self.addToErrorList(line["lineNum"], self.prepareError("compilerErrorVarNotFound", finals[0],
                                                                           "", "",
                                                                           str(line["lineNum"] + self.__startLine)))
                if var.type != "byte":
                   extraLines = self.__mainCompiler.convertAnyTo8Bits(var.usedBits).split("\n")
                   for line in extraLines:
                       if line != "":
                          extra += "asm(\"" + line + "\")\n"

            if self.__error == False:
                returnBack += "asm(\"\tLDA\t" + finals[0] + "\")\n" +\
                              extra                                 +\
                              "asm(\"\tSTA\t" + saveHere  + "\")\n"

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

    def returnMaxParamNum(self, command):
        return len(self.__loader.syntaxList[command].params)

    def isPowerOfTwo(self, num):
        return num & (num - 1) == 0

    def howManyTimesThePowerOfTwo(self, num):
        count = 0
        while num > 1:
            num = num >> 1
            count += 1
        return count

    def changeIfYouCanSaveToItem(self, state):
        var = self.__loader.virtualMemory.getVariableByName2("item")
        var.iterable = state
        var.system   = 1 - state

        if state == True:
           self.__variablesOfBank["readOnly"].remove("item")
           self.__variablesOfBank["writable"].append("item")
        else:
            self.__variablesOfBank["readOnly"].append("item")
            self.__variablesOfBank["writable"].remove("item")

        #print(self.__variablesOfBank["writable"])