from datetime import datetime
from copy import deepcopy
import re

class FirstCompiler:

    def __init__(self, loader, editorBigFrame, text, addComments, mode, bank, section, startLine, fullText, allowSysVars):

        self.__loader         = loader
        self.__editorBigFrame = editorBigFrame
        self.__text           = text.replace("\t", " ").split("\n")
        self.__allowSys       = allowSysVars
        self.__testFirst      = True

        self.__fullText       = fullText.replace("\t", " ").split("\n")
        self.__noneList = ["", "None", None, []]
        self.__registers,     \
        self.__opcodes        = self.__loader.io.loadRegOpCodes()
        self.__replacers = {
            "#BANK#": bank,
            "#SECTION#": section,
            "#FULL#": bank + "_" + section
        }
        self.exiters    = self.__editorBigFrame.exiters
        self.stupidList = []
        self.__alreadyCollectedLabels = self.__loader.alreadyCollectedLabels

        for num1 in range(1, 5):
            for num2 in range(1, 7):
                self.stupidList.append(str(num1) + "_" + str(num2))

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
        self.bank1Data        = {}
        self.__branchers      = ["BCC", "BCS", "BEQ", "BNE", "BMI", "BPL", "BVC", "BVS"]
        self.__jumpers        = ["JMP", "JSR"]
        self.__exceptions     = []
        self.__labels         = []

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

        if self.__allowSys:
           self.__variablesOfBank["readOnly"]  = []
           self.__variablesOfBank["writable"]  = self.__variablesOfBank["all"]
           self.__variablesOfBank["nonSystem"] = self.__variablesOfBank["all"]


        self.numberRegexes    = {"dec": r'^\d{1,3}$',
                                 "bin": r'^[b|%][0-1]{1,8}$',
                                 "hex": r'^[$|z|h][0-9a-fA-F]{1,2}$'}

        self.__currentSection = section
        self.__virtualMemory  = self.__loader.virtualMemory
        self.__config         = self.__loader.config
        self.__dictionaries   = self.__loader.dictionaries
        self.__startLine      = startLine
        self.__constants      = self.__editorBigFrame.collectConstantsFromSections(self.__currentBank, self.__currentSection, True, None)

        self.__writable, self.__readOnly, self.__all, self.__nonSystem  = writable, readOnly, all, nonSystem

        self.__validMemoryAddresses = []

        for num in range(0, 255):
            origNum = num
            num = hex(num).replace("0x", "")
            if len(num) == 1: num = "0" + num

            if origNum > 127:
               self.__validMemoryAddresses.append("$" + num.upper())

            self.__validMemoryAddresses.append("$F0" + num.upper())

        linesFeteched = self.createFetchedLines(self.__text, False)

        self.__mode = mode

        self.__canBeFortariCommandAndASMOpCode = []
        for regNum in self.__opcodes:
            lineSettings = self.__opcodes[regNum]
            if lineSettings["opcode"].lower() in self.__loader.syntaxList.keys():
               if lineSettings["opcode"].lower() not in self.__canBeFortariCommandAndASMOpCode:
                  self.__canBeFortariCommandAndASMOpCode.append(lineSettings["opcode"].lower())
               continue

            for key in self.__loader.syntaxList.keys():
                foundOne = False
                if lineSettings["opcode"].lower() in self.__loader.syntaxList[key].alias:
                   if lineSettings["opcode"].lower() not in self.__canBeFortariCommandAndASMOpCode:
                      self.__canBeFortariCommandAndASMOpCode.append(lineSettings["opcode"].lower())
                   foundOne = True
                   break
                if foundOne: break


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


    def createFetchedLines(self, text, detect):
        linesFeteched = []

        for lineNum in range(0, len(text)):
            line = text[lineNum]

            if detect: line = self.deleteNotUsedUpParams(line)

            lineStruct = self.__editorBigFrame.getLineStructure(lineNum, text, True)

            #if lineStruct["command"][0] in self.__noneList:
            #   continue

            lineStruct["fullLine"]       = line
            lineStruct["labelsBefore"]   = []
            lineStruct["labelsAfter"]    = []
            lineStruct["commentsBefore"] = ""
            lineStruct["compiled"]       = ""
            lineStruct["compiledBefore"] = ""
            lineStruct["magicNumber"]    = -1

            if self.__addComments:
               lineStruct["commentsBefore"] = "***\t" + line[:self.__editorBigFrame.getFirstValidDelimiterPoz(line)]

            linesFeteched.append(lineStruct)
            lineStruct["unreachable"] = self.checkIfCodeUnreachable(linesFeteched, lineStruct["level"])
            if lineStruct["unreachable"] == True:
               lineStruct["command"][0]  = None
               lineStruct["param#1"][0]  = None
               lineStruct["param#2"][0]  = None
               lineStruct["param#3"][0]  = None

        return linesFeteched

    def compileBuild(self, linesFeteched, mode):
        for line in linesFeteched:
            self.__error = False

            if line["command"][0] not in self.__noneList and line["unreachable"] == False:
               #if "%" in line["command"][0]: print("SSSS")
               self.processLine(line, linesFeteched)

               #if "add" in line["command"][0]: print("xxx", line["compiled"], "xxx")
               line["compiled"].replace("##", "#")
               self.colorAnnotationAfter(line)

        textToReturn = ""
        currentLineNum = 0

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
                             if tLine[0] in ("*", "#"):
                                textToReturn += tLine + "\n"
                             else:
                                textToReturn += "\tasm(\"" + tLine + "\")\n"

            if line["comment"][0] not in self.__noneList:
                textToReturn = textToReturn[:-1] + "\t; " + line["comment"][0] + "\n"

        self.result = self.detectUnreachableCode(self.checkForNotNeededExtraLDA(textToReturn))
        #print("\n>>>>>>>>>>>>>>>>>\n", self.result, "\n<<<<<<<<<<<<<<<<<<<<<<<<\n")

    def colorAnnotationAfter(self, line):
        if "&COLOR" in line["compiled"]: return
        lines = line["compiled"].split("\n")

        hasColor = False
        for modeNum in range(0, 2):
            if hasColor == False and modeNum == 1: break

            for lineNum in range(0, len(lines)):
                theLine = lines[lineNum]
                if len(theLine) == 0: continue
                if theLine[0] in ["*", "#", "!"]: continue

                l = theLine.replace("\t", " ").split(" ")
                newLine = []
                for item in l:
                    if item != "": newLine.append(item)

                if len(newLine) > 1:
                    operand = newLine[1]
                    if modeNum == 0:
                       var = self.__loader.virtualMemory.getVariableByName2(operand)
                       if var != False:
                          if var.color == True:
                             hasColor = True
                             break
                    else:
                        if len(re.findall(r'#?[$%]?[0-9a-fA-F]+', operand)) > 0:
                           if ";" in lines[lineNum]:
                               adder = " &COLOR"
                           else:
                               adder = " ; &COLOR"
                           lines[lineNum] += adder

        line["compiled"] = "\n".join(lines)


    def LDATAYLDA(self, text):

        listOfWhat = ["\tLSR\n\tASL\n",
                      "\tASL\n\tLSR\n"]

        for what in listOfWhat:
            while what in text:
                text = text.replace(what, "")

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
                   if secondLine[0] in ["*", "#", "!"] or secondLine.isspace(): continue

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
        #print(self.__error)
        if self.__error: print("Errors Already Had:", self.errorList)

        import traceback

        self.__useThese = [line["lineNum"], linesFeteched]
        self.__thisLine = line
        self.__checked  = False
        self.__changeThese = {}
        annotation = ""
        hasBCD       = False
        hasColor     = False

        params = {}

        try:
            if line["command"][0] in self.__loader.syntaxList:
               command = self.__loader.syntaxList[line["command"][0]]
            else:
               command = self.__objectMaster.createFakeCommandOnObjectProcess(line["command"][0])

            if "fullLine" not in line:
                line["fullLine"] = self.__editorBigFrame.getFillLine(line)

            #print("faszom", line)
            params = self.getParamsWithTypesAndCheckSyntax(line)
            if len(params) > 0:
                thisIsTheResult = str(len(command.params) - 1)

                if command.flexSave == True:
                   if len(params) < len(command.params):
                      thisIsTheResult = "1"

                for name in params:
                    try:
                        var = self.__loader.virtualMemory.getVariableByName2(params[name][0])
                        if var != False:
                            if name[-1] == thisIsTheResult:
                                if var.color == True and hasColor == False:
                                    hasColor  = True
                                    #print(params[name][0])
                                    if annotation == "":
                                       annotation = "\t; &COLOR"
                                    else:
                                       annotation += " &COLOR"

                            #if var.bcd   == True:
                            #       hasBCD = True
                            #       if annotation == "":
                            #          annotation = "\t; &BCD"
                            #       else:
                            #          annotation += " &BCD"

                        if hasColor == True and hasBCD == True: break
                    except Exception as e:
                        print(str(e))
                        #pass
        except Exception as e:
            print("OMG!! " + line["fullLine"])
            print(traceback.format_exc(), line)
            #pass

        #print("faszom", params, line)
        #"print(self.__error, self.__text)

        if command.flexSave and "param#3" in params:
           if params["param#1"][0] == params["param#3"][0]:
              del params["param#3"]
              del line["param#3"]
              #del linesFeteched[line["lineNum"]]["param#3"]

        if len(params.keys()) > 0:
            allTheSame, hasBCD = self.paramsHaveBCDandBinaryAtTheSameTime(params)

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

            self.checkASMCode(txt, line, linesFeteched)

            if self.__error == False:
               line["compiled"] = txt
               #else:
               #   line["compiled"] = datas[0]

            for key in self.__changeThese.keys():
                line["compiled"] = line["compiled"].replace(key, self.__changeThese[key])

            self.__checked = True

        elif self.isCommandInLineThat(line, "sin"):
            txt  = ""
            var2 = self.__loader.virtualMemory.getVariableByName2(params["param#2"][0])
            var1 = self.__loader.virtualMemory.getVariableByName2(params["param#1"][0])
            self.__temps = self.collectUsedTemps()

            addToRoutines = True
            if var1 == False:
               self.addToErrorList(line["lineNum"],
                                   self.prepareError("compilerErrorVarNotFound",
                                                     params["param#1"][0],
                                                     "", "",
                                                     str(line["lineNum"] + self.__startLine)))

            value      = ""
            wasANumber = None
            if self.__error == False:
               itIsComplex = False
               if var2 != False:
                  itIsComplex = var2.bcd or var2.type != "byte"

               if itIsComplex == False:
                  value = params["param#2"][0]
                  if var2 == False:
                     if params["param#2"][1] == "constant":
                        value = "#" + str(self.__editorBigFrame.convertStringNumToNumber(self.getConstValue(params["param#2"][0]))%256)
                     else:
                        value = "#" + str(self.__editorBigFrame.convertStringNumToNumber(params["param#2"][0])%256)

                  txt = "\tLDX\t" + value + "\n"
               else:
                  txt = "\tLDA\t" + params["param#2"][0] + "\n" + self.convertAny2Any(var2, "TO", params, self.__temps) + "\n\tTAX\n"

            txt += "\tLDA\t#BANK#_Sine,x\n".replace("#BANK#", self.__currentBank)

            if value != "":
               if value[0] == "#":
                  num           = self.valOfNumber(value)
                  wasANumber    = num
                  txt           = self.__loader.io.loadCommandASM("sinTable").split("\n")[1:][num].replace('\tBYTE', "\tLDA") + "\n"
                  addToRoutines = False

            if "param#3" in params.keys():
                var3 = self.__loader.virtualMemory.getVariableByName2(params["param#1"][0])
                itIsComplex = False

                isIt0 = False
                if var3 != False:
                    itIsComplex = var3.bcd or var3.type != "byte"
                else:
                    num = params["param#3"][0]
                    if num in self.__constants:
                       num = self.__constants[num]

                    isIt0 = self.isIt(num, 0)

                if isIt0 == False:
                   txt += "\tTAY\n"

                   if itIsComplex == False:
                        value = params["param#3"][0]
                        if var3 == False:
                            if params["param#3"][1] == "constant":
                                value = "#" + str(self.__editorBigFrame.convertStringNumToNumber(
                                    self.getConstValue(params["param#3"][0])) % 256)
                            else:
                                value = "#" + str(
                                    self.__editorBigFrame.convertStringNumToNumber(params["param#3"][0]) % 256)

                        txt += "\tLDX\t" + value + "\n"
                   else:
                        txt += "\tLDA\t" + params["param#3"][0] + "\n" + self.convertAny2Any(var3, "TO", params,
                                                                                            self.__temps) + "\n\tTAX\n"

                   self.__magicNumber += 1
                   try:
                       theOne = self.__temps[0]
                       self.__temps.pop(0)
                   except:
                       self.addToErrorList(line["lineNum"],
                                           self.prepareError("compilerErrorStatementTemps", params["param#3"][0],
                                                             "", "",
                                                             str(line["lineNum"] + self.__startLine)))

                   if self.__error == False:
                      name = "sinFlatten"

                      if wasANumber != None:
                         if wasANumber > 127:
                            name += "_BiggerOnly"
                         else:
                            name += "_SmallerOnly"

                      txt += "\tTYA\n" + self.__loader.io.loadCommandASM(name)\
                             .replace("#BANK#", self.__currentBank).replace("#MAGIC#", str(self.__magicNumber)).replace("#TEMPVAR#", theOne)


            if addToRoutines: self.toRoutines["sinTable"] = self.__loader.io.loadCommandASM("sinTable").replace("#BANK#", self.__currentBank)

            txt += self.convertAny2Any(var1, "FROM", params, self.__temps) + "\n" + "\tSTA\t" + params["param#1"][0] + "\n"

            self.checkASMCode(txt, line, linesFeteched)
            if self.__error == False:
               line["compiled"] = txt

        elif self.isCommandInLineThat(line, "add"):
            #params = self.getParamsWithTypesAndCheckSyntax(line)
            #print(line)

            if params["param#1"][0] == params["param#2"][0]:

               subline = deepcopy(line)
               subline["command"] = "*"
               subline["param#2"] = ["2", "number"]
               subline["fullLine"] = "\t*(" + subline["param#1"][0] + ", 2"
               if "param#3" in subline["fullLine"]:
                   subline["fullLine"] += ", " + subline["param#3"][0]
               subline["fullLine"] += ")"

               self.processLine(subline, linesFeteched)
               line["compiled"] = subline["compiled"]
               self.checkASMCode(line["compiled"], line, linesFeteched)
               if self.__error == False:
                  self.__checked = True
               return

            if "param#3" not in params.keys():
                if params["param#2"][1] == "number":
                    if self.isIt(params["param#2"][0], 0):
                        return
                    elif self.isIt(params["param#2"][0], 1) and hasBCD == False:
                        addr = self.getAddress(params["param#1"][0])
                        var = self.__loader.virtualMemory.getVariableByName2(params["param#1"][0])

                        if len(addr) == 3 and var.type == "byte" and (var.iterable == True or params["param#1"][0] == "item"):
                            txt = "\tINC\t" + params["param#1"][0] + "\n"
                            txt = self.checkForNotNeededExtraLDA(txt)

                            self.checkASMCode(txt, line, linesFeteched)
                            if self.__error == False: line["compiled"] = txt
                            return

                params["param#3"] = params["param#1"]
                var = self.__loader.virtualMemory.getVariableByName2(params["param#1"][0])

            else:
                var = self.__loader.virtualMemory.getVariableByName2(params["param#3"][0])

                if params["param#1"][1] == "number" and params["param#2"][1] == "number":
                    theNum = int(self.__editorBigFrame.convertStringNumToNumber(params["param#1"][0])) + \
                             int(self.__editorBigFrame.convertStringNumToNumber(params["param#2"][0]))

                    theNum = theNum % 256

                    params["param#0"] = [str(theNum), "number"]
                    txt = self.saveAValue(params, "param#0", "param#3", line)
                    txt = self.checkForNotNeededExtraLDA(txt)

                    self.checkASMCode(txt, line, linesFeteched)
                    if self.__error == False: line["compiled"] = txt
                    return

                if params["param#2"][1] == "number":
                    if self.isIt(params["param#2"][0], 0):
                        txt = self.saveAValue(params, "param#1", "param#3", line)
                        txt = self.checkForNotNeededExtraLDA(txt)

                        self.checkASMCode(txt, line, linesFeteched)
                        if self.__error == False: line["compiled"] = txt
                        return

            changeText = self.prepareAdd(params, False)
            if self.__error == False: self.createASMTextFromLine(line, "add", params, changeText, annotation, linesFeteched)

        elif self.isCommandInLineThat(line, "sub"):
            #params = self.getParamsWithTypesAndCheckSyntax(line)
            #allTheSame, hasBCD = self.paramsHaveBCDandBinaryAtTheSameTime(params)
            if params["param#1"][0] == params["param#2"][0]:
               params["param#0"] = ["0", "number"]
               if "param#3" in params:
                   txt = self.saveAValue(params, "param#0", "param#3", line)
               else:
                   txt = self.saveAValue(params, "param#0", "param#1", line)
               self.checkASMCode(txt, line, linesFeteched)
               if self.__error == False: line["compiled"] = txt
               return

            if params["param#1"][1] == "number" and params["param#2"][1] == "number":
                var = self.__loader.virtualMemory.getVariableByName2(params["param#3"][0])

                theNum = int(self.__editorBigFrame.convertStringNumToNumber(params["param#1"][0])) - \
                         int(self.__editorBigFrame.convertStringNumToNumber(params["param#2"][0]))

                if theNum < 0:
                   theNum = 256 + theNum

                params["param#0"] = [str(theNum), "number"]
                txt = self.saveAValue(params, "param#0", "param#3", line)
                self.checkASMCode(txt, line, linesFeteched)
                if self.__error == False: line["compiled"] = txt
                return

            elif params["param#2"][1] == "number":
                if self.isIt(params["param#2"][0], 0):
                   if "param#3" in params.keys():
                       txt = self.saveAValue(params, "param#1", "param#3", line)
                       txt = self.checkForNotNeededExtraLDA(txt)

                       self.checkASMCode(txt, line, linesFeteched)
                       if self.__error == False: line["compiled"] = txt
                       return
                   else:
                      return
                elif self.isIt(params["param#2"][0], 1) and hasBCD == False:
                    addr = self.getAddress(params["param#1"][0])
                    var = self.__loader.virtualMemory.getVariableByName2(params["param#1"][0])

                    if len(addr) == 3 and var.type == "byte" and (var.iterable == True or params["param#1"][0] == "item"):
                        txt = "\tDEC\t" + params["param#1"][0] + "\n"
                        txt = self.checkForNotNeededExtraLDA(txt)

                        self.checkASMCode(txt, line, linesFeteched)
                        if self.__error == False: line["compiled"] = txt
                        return

            if "param3" not in params.keys():
                params["param#3"] = params["param#1"]

            var = self.__loader.virtualMemory.getVariableByName2(params["param#3"][0])
            if var == False:
                self.addToErrorList(line["lineNum"],
                                    self.prepareError("compilerErrorVarNotFound", params["param#3"][0],
                                                      "", "",
                                                      str(line["lineNum"] + self.__startLine)))
            changeText = self.prepareAdd(params, False)
            if self.__error == False: self.createASMTextFromLine(line, "sub", params, changeText, annotation, linesFeteched)

        elif self.isCommandInLineThat(line, "sqrt"):
            #params                  = self.getParamsWithTypesAndCheckSyntax(line)
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
                  template = template.replace("!!!to8bit!!!", self.convertAny2Any( var1, "TO", params, self.__temps))

               template = template.replace("#VAR02#", params["param#2"][0])
               template = template.replace("!!!from8bit!!!", self.convertAny2Any( var2, "FROM", params, self.__temps))
               template = template.replace("#TEMP#", theOne)
               self.checkASMCode(template, line, linesFeteched)
               if self.__error == False: line["compiled"] = template.replace("#BANK#", self.__currentBank).replace(
                   "#MAGIC#", str(self.__magicNumber))
               self.__magicNumber += 1

        elif self.isCommandInLineThat(line, "copy"):
            array1 = line["param#1"][0]
            if array1 not in self.__loader.virtualMemory.arrays.keys() or \
                    (self.__virtualMemory.getArrayValidity(array1) not in [self.__currentBank, "bank1", "global"]):
                self.addToErrorList(line["lineNum"],
                                    self.prepareError("compilerErrorArrayNotFound", array1,
                                                      "", "",
                                                      str(line["lineNum"] + self.__startLine)))

            array2 = line["param#2"][0]
            if array2 not in self.__loader.virtualMemory.arrays.keys() or \
                    (self.__virtualMemory.getArrayValidity(array2) not in [self.__currentBank, "bank1", "global"]):
                self.addToErrorList(line["lineNum"],
                                    self.prepareError("compilerErrorArrayNotFound", array2,
                                                      "", "",
                                                      str(line["lineNum"] + self.__startLine)))
            txt = ""
            if self.__error == False:
               lenght = min([len(self.__loader.virtualMemory.arrays[array1]),
                         len(self.__loader.virtualMemory.arrays[array2])])

               varKeys1 = list(self.__loader.virtualMemory.arrays[array1].keys())
               varKeys2 = list(self.__loader.virtualMemory.arrays[array2].keys())

               for num in range(0, lenght):
                   varName1 = varKeys1[num]
                   varName2 = varKeys2[num]

                   var1     = self.__loader.virtualMemory.arrays[array1][varName1]
                   var2     = self.__loader.virtualMemory.arrays[array2][varName2]

                   if var1 == False:
                      self.addToErrorList(line["lineNum"],
                                           self.prepareError("compilerErrorVarNotFound", varName1,
                                                             "", "",
                                                             str(line["lineNum"] + self.__startLine)))
                   if var2 == False:
                      self.addToErrorList(line["lineNum"],
                                           self.prepareError("compilerErrorVarNotFound", varName2,
                                                             "", "",
                                                             str(line["lineNum"] + self.__startLine)))
                   subline = deepcopy(line)
                   subline["command"][0] = "set"
                   subline["param#1"][0] = varName1
                   subline["param#2"][0] = varName2

                   subline["fullLine"] = "\tset(" + varName1 +"," + varName2 + ")"
                   subline["compiled"] = ""

                   self.processLine(subline, linesFeteched)
                   if self.__error: break

                   txt += subline["compiled"] + "\n"

            if self.__error == False:
               self.checkASMCode(txt, line, linesFeteched)

               if self.__error == False: line["compiled"] = txt

            return

        elif self.isCommandInLineThat(line, "randAll"):
            self.exceptionList(["random"], "add")
            txt = ""

            array = line["param#1"][0]
            if array not in self.__loader.virtualMemory.arrays.keys() or \
                    (self.__virtualMemory.getArrayValidity(array) not in [self.__currentBank, "bank1", "global"]):
                self.addToErrorList(line["lineNum"],
                                    self.prepareError("compilerErrorArrayNotFound", array,
                                                      "", "",
                                                      str(line["lineNum"] + self.__startLine)))

            counter = -1
            if self.__error == False:
               for varName in self.__loader.virtualMemory.arrays[array]:
                   counter += 1
                   var = self.__loader.virtualMemory.getVariableByName2(varName)
                   if var == False:
                      self.addToErrorList(line["lineNum"],
                                           self.prepareError("compilerErrorVarNotFound", params["param#2"][0],
                                                             "", "",
                                                             str(line["lineNum"] + self.__startLine)))
                   else:
                      subline = deepcopy(line)
                      subline["command"][0] = "rand"
                      subline["param#1"][0] = varName
                      subline["fullLine"] = "\trand(" + subline["param#1"][0]
                      for key in ["param#2", "param#3"]:
                          if key in subline.keys():
                              subline["fullLine"] += ", " + subline[key][0]
                      subline["fullLine"] += ")"
                      subline["compiled"]  = ""

                      self.processLine(subline, linesFeteched)
                      if self.__error:
                         break
                      else:
                         subTxt = subline["compiled"]
                         subTxt = subTxt.split("\n")
                         for lNum in range(0, len(subTxt)):
                             if "STA" in subTxt[lNum].upper() and "random" in subTxt[lNum]:
                                 subTxt.pop(lNum)
                                 break

                         txt += "\n".join(subTxt) + "\n"
                         if counter%2 == 0:
                            txt += "\tORA\tcounter\n\tSTA\trandom\n"
                         else:
                            txt += "\tLSR\n\tTAX\n\tORA\tcounter,x\n\tSTA\trandom\n"

               if self.__error == False:
                   self.checkASMCode(txt, line, linesFeteched)

            if self.__error == False: line["compiled"] = txt
            self.exceptionList(["random"], "delete")
            return

        elif self.isCommandInLineThat(line, "randXorCounter"):
            line["compiled"] = "\tLDA\trandom\t\n\tEOR\tcounter\n\tSTA\trandom\n"
            return

        elif self.isCommandInLineThat(line, "rand"):
            #params    = self.getParamsWithTypesAndCheckSyntax(line)
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

            replacers["!!!from8bit!!!"] = self.convertAny2Any( var, "FROM", params, self.__temps)
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
                  #replacers["!!!ADD!!!"] = "\tCLC\n\tADC\t#" + str(val).replace("#", "") + "\n"
                  adder = "#" + str(val).replace("#", "")
               else:
                   #allTheSame, hasBCD = self.paramsHaveBCDandBinaryAtTheSameTime(params)

                   if hasBCD and allTheSame == True:
                      replacers["!!!BCDon!!!"] = "\tSED"
                      replacers["!!!BCDoff!!!"] = "\tCLD"

                   if var.type == "byte" and (var.bcd == False or allTheSame == True):
                         #replacers["!!!ADD!!!"] = "\tCLC\n\tADC\t" + str(val) + "\n"
                         adder = str(val)

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
                            #replacers["!!!ADD!!!"]     = "\tCLC\n\tADC\t" + first + "\n"
                            adder = first
                            replacers["!!!CALCADD!!!"] = "\tLDA\t" + val + \
                                                         "\n" + self.convertAny2Any(var, "TO", params, self.__temps) +\
                                                         "\tSTA\t" + first + "\n"
               self.__magicNumber += 1
               label = "#BANK#_" + str(self.__magicNumber) + "_NotSmaller\n"
               replacers["!!!ADD!!!"] = "\tCMP\t" + adder + "\n\tBCS\t" + label + "\tLDA\t" + adder + "\n" + label

            if maxV != None:
                val = params[maxV][0]
                var = self.__loader.virtualMemory.getVariableByName2(val)
                if var == False:
                    replacers["!!!AND!!!"] = "\tAND\t#" + str(val).replace("#", "") + "\n"
                else:

                    #allTheSame, hasBCD = self.paramsHaveBCDandBinaryAtTheSameTime(params)

                    if hasBCD and allTheSame == True:
                        replacers["!!!BCDon!!!"] = "\tSED"
                        replacers["!!!BCDoff!!!"] = "\tCLD"

                    if var.type == "byte" and (var.bcd == False or allTheSame == True):
                        replacers["!!!AND!!!"] = "\tAND\t" + str(val) + "\n"
                    else:
                        try:
                            second = self.__temps[0]
                            self.__temps.pop(0)
                        except:
                            self.addToErrorList(line["lineNum"],
                                                self.prepareError("compilerErrorStatementTemps", params["param#1"][0],
                                                                  "", "",
                                                                  str(line["lineNum"] + self.__startLine)))
                        if self.__error == False:
                            replacers["!!!AND!!!"] = "\tAND\t" + second + "\n"
                            replacers["!!!CALCAND!!!"] = "\tLDA\t" + val + \
                                                         "\n" + self.convertAny2Any(var, "TO", params, self.__temps) + \
                                                         "\tSTA\t" + second + "\n"


            for key in replacers:
                template = template.replace(key, replacers[key])

            self.exceptionList(["random"], "add")
            self.checkASMCode(template, line, linesFeteched)
            self.exceptionList(["random"], "delete")

            if self.__error == False: line["compiled"] = template
            return

        elif self.isCommandInLineThat(line, "swap"):
            #params = self.getParamsWithTypesAndCheckSyntax(line)
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

            load1    = ""
            load2    = ""
            save1    = ""
            save2    = ""

            varName1 = params["param#1"][0]
            varName2 = params["param#2"][0]

            if var1.type == "byte" and (var1.bcd == False or allTheSame == True):
               load1     =  "\tLDY\t" + varName1 + "\n"
               save1     =  "\tSTA\t" + varName1 + "\n"
            else:
               load1     = "\tLDA\t" + varName1 + "\n" + self.convertAny2Any( var1, "TO", params, None) + "\tTAY\n"
               save1     = self.convertAny2Any( var1, "FROM", params, None) + "\tSTA\t" + varName1 + "\n"

            if var2.type == "byte" and (var2.bcd == False or allTheSame == True):
               load2     =  "\tLDA\t" + varName2 + "\n"
               save2     =  "\tSTY\t" + varName2 + "\n"
            else:
               load2     = "\tLDA\t" + varName2 + "\n" + self.convertAny2Any( var2, "TO", params, None)
               save2     = "\tTYA\n" + self.convertAny2Any( var2, "FROM", params, None) + "\tSTA\t" + varName2 + "\n"

            txt = load1 + load2 + save1 + save2

            self.checkASMCode(txt, line, linesFeteched)
            if self.__error == False: line["compiled"] = txt


        elif self.isCommandInLineThat(line, "pow"):
            #params = self.getParamsWithTypesAndCheckSyntax(line)

            #allTheSame, hasBCD = self.paramsHaveBCDandBinaryAtTheSameTime(params)
            self.__temps = self.collectUsedTemps()

            if params["param#1"][1] != "number" or params["param#2"][1] != "number":

                varPow2Param = False
                """
                if params["param#1"][1] == "number":
                   if self.isIt(params["param#1"][0], 2) and hasBCD == False:
                      varPow2Param = "param#2"
                """
                if   params["param#1"][1] == "number":
                     times = int(self.__editorBigFrame.convertStringNumToNumber(params["param#1"][0]))
                     if self.isPowerOfTwo(times) and times > 2:
                        times = self.howManyTimesThePowerOfTwo(times)
                        varPow2Param = "param#2"

                elif params["param#2"][1] == "number":
                     times = int(self.__editorBigFrame.convertStringNumToNumber(params["param#2"][0]))
                     if self.isPowerOfTwo(times) and times > 2:
                        times = self.howManyTimesThePowerOfTwo(times)
                        varPow2Param = "param#1"

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
                        template = template.replace("!!!to8bit!!!", self.convertAny2Any( var1, "TO", params, self.__temps))

                    else:
                        template = template.replace("#VAR01#", "#" + params[varPow2Param][0].replace("#", ""))

                    template = template.replace("!!!ASL!!!", times * "")

                    var2 = self.__loader.virtualMemory.getVariableByName(params["param#3"][0], self.__currentBank)
                    if var2 == False:
                       var2 = self.__loader.virtualMemory.getVariableByName(params["param#3"][0], "bank1")

                    if var2 == False:
                        self.addToErrorList(line["lineNum"],
                                            self.prepareError("compilerErrorVarNotFound", params["param#3"][0],
                                                              "", "",
                                                              str(line["lineNum"] + self.__startLine)))

                    template = template.replace("#VAR02#", params["param#3"][0])
                    template = template.raplace("!!!from8bit!!!" , self.convertAny2Any( var2, "FROM", params, self.__temps))

                    self.checkASMCode(template, line, linesFeteched)
                    if self.__error == False: line["compiled"] = template.replace("#BANK#", self.__currentBank).replace("#MAGIC#", str(self.__magicNumber))
                    self.__magicNumber += 1

                    return

                if params["param#2"][1] == "number":
                    if self.__editorBigFrame.convertStringNumToNumber(params["param#2"][0]) == 2:
                       subline = deepcopy(line)
                       subline["command"] = "*"
                       subline["param#2"] = subline["param#1"]
                       subline["fullLine"] = "\t*(" + subline["param#1"][0] + ", " + subline["param#1"][0]
                       if "param#3" in subline["fullLine"]:
                           subline["fullLine"] += ", " + subline["param#3"][0]
                       subline["fullLine"] += ")"

                       self.processLine(subline, linesFeteched)
                       line["compiled"] = subline["compiled"]
                       self.checkASMCode(line["compiled"] , line, linesFeteched)
                       if self.__error == False:
                          self.__checked = True
                       return

                    elif self.__editorBigFrame.convertStringNumToNumber(params["param#2"][0]) == 1:
                        params["param#0"] = params["param#1"]
                        if "param#3" not in params.keys():
                            return
                        else:
                            txt = self.saveAValue(params, "param#0", "param#3", line)

                        self.checkASMCode(txt, line, linesFeteched)
                        if self.__error == False: line["compiled"] = txt
                        return

                    elif self.__editorBigFrame.convertStringNumToNumber(params["param#2"][0]) == 0:
                        params["param#0"] = ["#1", "number"]
                        if "param#3" not in params.keys():
                            txt = self.saveAValue(params, "param#0", "param#1", line)
                        else:
                            txt = self.saveAValue(params, "param#0", "param#3", line)

                        self.checkASMCode(txt, line, linesFeteched)
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
                   self.checkASMCode(txt, line, linesFeteched)
                   if self.__error == False:
                      line["compiled"] = txt
                      self.__checked = True

            else:
                theNum = pow(self.__editorBigFrame.convertStringNumToNumber(params["param#1"][0]),
                             self.__editorBigFrame.convertStringNumToNumber(params["param#2"][0]))

                theNum = theNum%256
                params["param#0"] = ["#" + str(theNum), "number"]

                txt = self.saveAValue(params, "param#0", "param#3", line)
                self.checkASMCode(txt, line, linesFeteched)
                if self.__error == False: line["compiled"] = txt
                return

        elif self.isCommandInLineThat(line, "multi"):
            #params = self.getParamsWithTypesAndCheckSyntax(line)

            if params["param#1"][0] == params["param#2"][0] and params["param#1"][1] == "variable":
               template = self.__loader.io.loadCommandASM("multiS")
               var1 = self.__loader.virtualMemory.getVariableByName2(params["param#1"][0])

               if "param#3" not in params:
                  params["param#3"] = params["param#1"]

               var2 = self.__loader.virtualMemory.getVariableByName2(params["param#3"][0])

               if var1 == False:
                  self.addToErrorList(line["lineNum"],
                                       self.prepareError("compilerErrorStatementTemps", params["param#1"][0],
                                                         "", "",
                                                         str(line["lineNum"] + self.__startLine)))

               if var1 != var2 and var2 == False:
                  self.addToErrorList(line["lineNum"],
                                       self.prepareError("compilerErrorStatementTemps", params["param#3"][0],
                                                         "", "",
                                                         str(line["lineNum"] + self.__startLine)))

               changers = {}
               changers["#VAR01#"]   = params["param#1"][0]
               changers["#VARTEMP#"] = params["param#1"][0]
               changers["#VAR03#"]   = params["param#3"][0]
               if   var1.bcd == True and var2.bcd == True and var1.type == "byte" and var2.type == "byte":
                    changers["!!!BCDon!!!"]  = "\tSED\t"
                    changers["!!!BCDoff!!!"] = "\tCLD\t"

               else:
                    self.__temps = self.collectUsedTemps()
                    try:
                       first = self.__temps[0]
                       self.__temps.pop(0)
                    except:
                       self.addToErrorList(line["lineNum"],
                                           self.prepareError("compilerErrorStatementTemps", params["param#1"][0],
                                                             "", "",
                                                             str(line["lineNum"] + self.__startLine)))

                    if var2.bcd == True or var2.type != "byte":
                       changers["!!!from8bit!!!"] = self.convertAny2Any(params["param#3"][0], "FROM", params, self.__temps)

                    if var1.bcd == True or var1.type != "byte":
                       changers["!!!to8Bit1!!!"] = self.convertAny2Any(params["param#1"][0], "TO", params, self.__temps)
                       changers["#VARTEMP#"]     = first
                       changers["!!!staTEMP!!!"] = "\tSTA\t" + first + "\n"

               txt = template
               for item in changers:
                   txt = txt.replace(item, changers[item])

               self.checkASMCode(txt, line, linesFeteched)
               if self.__error == False:
                   line["compiled"] = txt
                   return

            if    params["param#1"][1] in ["number", "variable"] and params["param#2"][1] in ["number", "variable"]\
                  and params["param#1"][1] != params["param#2"][1]:

                  if params["param#1"][1] == "number":
                     numParam = "param#1"
                     varParam = "param#2"
                  else:
                     numParam = "param#2"
                     varParam = "param#1"

                  theNum = int(self.__editorBigFrame.convertStringNumToNumber(params[numParam][0]))
                  var = self.__loader.virtualMemory.getVariableByName2(params[varParam][0])
                  if "param#3" not in params:
                      if self.isIt(params[numParam][0], 1):
                          return

                      if var != False:
                          if self.isPowerOfTwo(theNum):
                             times   = self.howManyTimesThePowerOfTwo(theNum)
                             subLine = self.__editorBigFrame.getLineStructure(0, ["\tasl(" + str(times) + ", " + params[varParam][0] + " )"], False)
                             self.processLine(subLine, linesFeteched)
                             if "compiled" in subLine:
                                 line["compiled"] = subLine["compiled"]
                                 if line["compiled"] != "": return

                  if var != False:
                     if self.isPowerOfTwo(theNum):
                         times = self.howManyTimesThePowerOfTwo(theNum)
                         if times > 1:
                            template                  = self.__loader.io.loadCommandASM("pow2")
                            changer                   = {}
                            changer["#VAR01#"]        = params[varParam][0]
                            changer["#VAR02#"]        = params["param#3"][0]
                            changer["!!!to8bit!!!"]   = self.convertAny2Any(params[varParam][0] , "TO"  , params, None)
                            changer["!!!from8bit!!!"] = self.convertAny2Any(params["param#3"][0], "FROM", params, None)
                            changer["!!!ASL!!!"]      = "\tASL\n" * times

                            self.__magicNumber       += 1
                            changer["#MAGIC#"]        = str(self.__magicNumber)

                            for key in changer:
                                template = template.replace(key, changer[key])
                            self.checkASMCode(template, line, linesFeteched)
                            if self.__error == False:
                               line["compiled"] = template.replace("#BANK#", self.__currentBank)
                               return
                         elif times == 1:
                            txt = "\tLDA\t"   + params[varParam][0] + "\n" + self.convertAny2Any(params[varParam][0] , "TO"  , params, None) +\
                                  "\n\tASL\n" + self.convertAny2Any(params["param#3"][0], "FROM", params, None) + "\tSTA\t" + params["param#3"][0] + "\n"
                            self.checkASMCode(txt, line, linesFeteched)
                            if self.__error == False:
                               line["compiled"] = txt.replace("#BANK#", self.__currentBank)
                               return
                         else:
                             if   params[numParam][0] == "0":
                                  params["param#0"] = ["0", "number"]
                                  txt = self.saveAValue(params, "param#0", "param#3", line)
                                  self.checkASMCode(txt, line, linesFeteched)
                                  if self.__error == False:
                                     line["compiled"] = txt
                                     return
                             elif params[numParam][0] == "1":
                                  txt = self.saveAValue(params, "param#1", "param#3", line)
                                  self.checkASMCode(txt, line, linesFeteched)
                                  if self.__error == False:
                                     line["compiled"] = txt
                                     return


            if "param#3" not in params.keys():
                params["param#3"] = params["param#1"]

            if params["param#1"][1] == "number" and params["param#2"][1] == "number":
                theNum = int(self.__editorBigFrame.convertStringNumToNumber(params["param#1"][0])) * \
                         int(self.__editorBigFrame.convertStringNumToNumber(params["param#2"][0]))

                theNum = theNum % 256

                params["param#0"] = [str(theNum), "number"]
                txt = self.saveAValue(params, "param#0", "param#3", line)
                self.checkASMCode(txt, line, linesFeteched)
                if self.__error == False:
                    line["compiled"] = txt
                    return

            if params["param#1"][1] == "number":
               if self.isIt(params["param#1"][0], 1):
                  if "param#3" in params.keys():
                      txt = self.saveAValue(params, "param#2", "param#3", line)
                      self.checkASMCode(txt, line, linesFeteched)
                      if self.__error == False:
                          line["compiled"] = txt
                          return
                  else:
                      return

               elif self.isIt(params["param#1"][0], 0):
                    params["param#0"] = ["#0", "number"]
                    txt = self.saveAValue(params, "param#0", "param#3", line)
                    txt = self.checkForNotNeededExtraLDA(txt)

                    self.checkASMCode(txt, line, linesFeteched)
                    if self.__error == False:
                       line["compiled"] = txt
                       return

            if params["param#2"][1] == "number":
               if self.isIt(params["param#2"][0], 1):
                  if "param#3" in params.keys():
                      txt = self.saveAValue(params, "param#1", "param#3", line)
                      txt = self.checkForNotNeededExtraLDA(txt)

                      self.checkASMCode(txt, line, linesFeteched)
                      if self.__error == False:
                         line["compiled"] = txt
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

                    self.checkASMCode(txt, line, linesFeteched)
                    if self.__error == False:
                       line["compiled"] = txt
                       return

            changeText = self.prepareMulti(params)

            if self.__error == False: self.createASMTextFromLine(line, "multi", params, changeText, annotation, linesFeteched)

        elif self.isCommandInLineThat(line, "div") or self.isCommandInLineThat(line, "rem"):
            if self.isCommandInLineThat(line, "divide"):
               saveThisOne = "Y"
            else:
               saveThisOne = "A"

            if params["param#1"][0] == params["param#2"][0]:
               if saveThisOne == "Y":
                  params["param#0"] = ["0", "number"]
               else:
                  params["param#0"] = ["1", "number"]

               if "param#3" in params:
                   txt = self.saveAValue(params, "param#0", "param#3", line)
               else:
                   txt = self.saveAValue(params, "param#0", "param#1", line)
               self.checkASMCode(txt, line, linesFeteched)
               if self.__error == False:
                  line["compiled"] = txt
                  return

            #params  = self.getParamsWithTypesAndCheckSyntax(line)

            if (params["param#2"][1] == "number" and params["param#1"][1] == "variable" and "param#3" not in params):
                numParam = "param#2"
                varParam = "param#1"
                theNum = int(self.__editorBigFrame.convertStringNumToNumber(params[numParam][0]))

                var = self.__loader.virtualMemory.getVariableByName2(params[varParam][0])
                if var != False:
                    if self.isPowerOfTwo(theNum) and var.type == "byte":
                        times = self.howManyTimesThePowerOfTwo(theNum)
                        subLine = self.__editorBigFrame.getLineStructure(0, [
                            "\tlsr(" + str(times) + ", "+ params[varParam][0] +" )"],
                                                                         False)
                        self.processLine(subLine, linesFeteched)
                        line["compiled"] = subLine["compiled"]
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
                self.checkASMCode(txt, line, linesFeteched)
                if self.__error == False: line["compiled"] = txt
                return

            elif oneDiv == True:
                if saveThisOne == "Y":
                    if "param#3" not in params.keys():
                       return

                    txt = self.saveAValue(params, "param#1", "param#3", line)
                    txt = self.checkForNotNeededExtraLDA(txt)

                    self.checkASMCode(txt, line, linesFeteched)
                    if self.__error == False: line["compiled"] = txt
                    return
                else:
                    if "param#3" not in params.keys():
                        params["param#3"] = params["param#1"]

                    params["param#0"] = [0, "number"]
                    txt = self.saveAValue(params, "param#0", "param#3", line)
                    self.checkASMCode(txt, line, linesFeteched)
                    if self.__error == False: line["compiled"] = txt
                    self.__checked = True

            else:
                if "param#3" not in params.keys():
                   params["param#3"] = params["param#1"]

                changeText = self.prepareDiv(params, saveThisOne)
                if self.__error == False: self.createASMTextFromLine(line, "div", params, changeText, annotation, linesFeteched)


        elif self.isCommandInLineThat(line, "and") or\
             self.isCommandInLineThat(line, "or")  or\
             self.isCommandInLineThat(line, "xor"):
            if   self.isCommandInLineThat(line, "and"):
                 command = "and"
            elif self.isCommandInLineThat(line, "or"):
                 command = "or"
            else:
                 command = "xor"

            #params = self.getParamsWithTypesAndCheckSyntax(line)
            if "param#3" not in params.keys():

                if params["param#1"][0] == params["param#2"][0]:
                   if command == "xor":
                      params["param#0"] = ["#0", "number"]
                      txt = self.saveAValue(params, "param#0", "param#1", line)
                      txt = self.checkForNotNeededExtraLDA(txt)
                      self.checkASMCode(txt, line, linesFeteched)
                      if self.__error == False: line["compiled"] = txt
                      return

                   return

                var = self.__loader.virtualMemory.getVariableByName2(params["param#1"][0])

                if params["param#2"][1] == "number":
                    if command == "and":
                       if self.isIt(params["param#2"][0], 255):
                          return

                       if self.isIt(params["param#2"][0], 0):
                          params["param#0"] = ["#0", "number"]
                          txt = self.saveAValue(params, "param#0", "param#1", line)
                          txt = self.checkForNotNeededExtraLDA(txt)
                          self.checkASMCode(txt, line, linesFeteched)
                          if self.__error == False: line["compiled"] = txt
                          return
                    elif command == "or":
                        if self.isIt(params["param#2"][0], 0):
                            return

                        if self.isIt(params["param#2"][0], 255):
                            params["param#0"] = ["#255", "number"]
                            txt = self.saveAValue(params, "param#0", "param#1", line)
                            txt = self.checkForNotNeededExtraLDA(txt)
                            self.checkASMCode(txt, line, linesFeteched)
                            if self.__error == False: line["compiled"] = txt
                            return

                params["param#3"] = params["param#1"]
            else:
                if params["param#1"][0] == params["param#2"][0]:
                   if command == "xor":
                      params["param#0"] = ["#0", "number"]
                      txt = self.saveAValue(params, "param#0", "param#3", line)
                   else:
                      txt = self.saveAValue(params, "param#1", "param#3", line)
                   txt = self.checkForNotNeededExtraLDA(txt)
                   self.checkASMCode(txt, line, linesFeteched)
                   if self.__error == False: line["compiled"] = txt
                   return


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
                    self.checkASMCode(txt, line, linesFeteched)
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
                        self.checkASMCode(txt, line, linesFeteched)
                        if self.__error == False: line["compiled"] = txt
                        return

                    if param255 != None:
                        txt = self.saveAValue(params, param255, "param#3", line)
                        txt = self.checkForNotNeededExtraLDA(txt)
                        self.checkASMCode(txt, line, linesFeteched)
                        if self.__error == False: line["compiled"] = txt
                        return
                elif command == "or":
                    if param255 != None:
                        params["param#0"] = ["#255", "number"]
                        txt = self.saveAValue(params, "param#0", "param#3", line)
                        txt = self.checkForNotNeededExtraLDA(txt)
                        self.checkASMCode(txt, line, linesFeteched)
                        if self.__error == False: line["compiled"] = txt
                        return

                    if param0 != None:
                        txt = self.saveAValue(params, param0, "param#3", line)
                        txt = self.checkForNotNeededExtraLDA(txt)
                        self.checkASMCode(txt, line, linesFeteched)
                        if self.__error == False: line["compiled"] = txt
                        return

            changeText = self.prepareAdd(params, True)
            if self.__error == False: self.createASMTextFromLine(line, command, params, changeText, annotation, linesFeteched)

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

             if "param#2" not in params:
                 params["param#2"] = deepcopy(params["param#1"])
                 params["param#1"] = ["1", "number"]

             var1 = self.__loader.virtualMemory.getVariableByName2(params["param#1"][0])
             var2 = self.__loader.virtualMemory.getVariableByName2(params["param#2"][0])

             if var2.type == "bit": return

             if var2 == False:
                 self.addToErrorList(line["lineNum"],
                                     self.prepareError("compilerErrorVarNotFound", params["param#2"][0],
                                                       "", "",
                                                       str(line["lineNum"] + self.__startLine)))

             varName = params["param#2"][0]
             txt     = "\tLDA\t" + varName + "\n"
             if var1 == False and var2.type == "byte":
                shiftNum = self.__editorBigFrame.convertStringNumToNumber(params["param#1"][0])%8
                if shiftNum == 0: return

                _to   = ""
                if var2.bcd:
                   txt  += self.convertAny2Any(varName, "TO"  , params, None) + "\n"
                   _to   = self.convertAny2Any(varName, "FROM", params, None) + "\n"

                if shiftNum < 2 and var2.bcd == False and self.__loader.virtualMemory.isSara(params["param#1"][0]) == False:
                    txt = shiftNum * ("\t" + command + "\t" + varName + "\n")
                else:
                    txt += shiftNum * ("\t" + command + "\n") + _to + "\tSTA\t" + varName + "\n"

                txt = self.checkForNotNeededExtraLDA(txt)
                self.checkASMCode(txt, line, linesFeteched)
                if self.__error == False: line["compiled"] = txt
                return

             elif var1 != False and var2.type == "byte":
                self.__temps = self.collectUsedTemps()

                txt = self.__loader.io.loadCommandASM("shift").replace("#VAR01#", params["param#1"][0]) \
                                                              .replace("#VAR02#", params["param#2"][0]) \
                                                              .replace("!!!to8bit1!!!",  self.convertAny2Any(var1, "TO", params, self.__temps)) \
                                                              .replace("!!!to8bit2!!!",  self.convertAny2Any(var2, "TO", params, self.__temps)) \
                                                              .replace("!!!from8bit!!!", self.convertAny2Any(var2, "FROM", params, self.__temps)) \
                                                              .replace("#COMMAND#", command)
                self.__magicNumber += 1
                txt = self.checkForNotNeededExtraLDA(txt.replace("#MAGIC#", str(self.__magicNumber)))
                self.checkASMCode(txt, line, linesFeteched)
                if self.__error == False: line["compiled"] = txt
                return
             else:
                 if var1 == False:
                    shiftNum = self.__editorBigFrame.convertStringNumToNumber(params["param#1"][0]) % 8
                    if shiftNum == 0: return
                    shifting = "\tLDX\t#" + str(shiftNum) + "\n"
                 else:
                    if var1.type != "byte" or var1.bcd:
                       shifting = "\tLDA\t" + params["param#1"][0] + "\n" +\
                                  self.convertAny2Any(params["param#1"][0], "TO", params, None) +\
                                  "\tTAX\n"
                    else:
                       shifting = "\tLDX\t" + params["param#1"][0] + "\n"

                 changers = {}
                 changers["!!!NumOfShifting!!!"] = shifting
                 changers["!!!to8bit!!!"]    = self.convertAny2Any(params["param#2"][0], "TO"  , params, None)
                 changers["!!!from8bit!!!"]  = self.convertAny2Any(params["param#2"][0], "FROM", params, None)
                 changers["#VAR02#"]         = params["param#2"][0]

                 if command in ("ASL", "ROL"):
                    changers["#COMMAND#"] = "ASL"
                    direction             = "L"
                 else:
                    changers["#COMMAND#"] = "LSR"
                    direction             = "R"

                 changers["#MASK3#"] = "#%" + ("0" * (8 - len(var2.usedBits))) + ("1" * len(var2.usedBits))

                 self.__magicNumber += 1
                 changers["#MAGIC#"] = str(self.__magicNumber)

                 txt = self.__loader.io.loadCommandASM("shiftAdvanced")
                 if "RO" in command:
                     txt = txt.replace("!!!Sub!!!", self.__loader.io.loadCommandASM("shiftAdvancedSub"))

                     self.__temps = self.collectUsedTemps()
                     try:
                         first = self.__temps[0]
                         self.__temps.pop(0)
                     except:
                         self.addToErrorList(line["lineNum"],
                                             self.prepareError("compilerErrorStatementTemps", params["param#1"][0],
                                                               "", "",
                                                               str(line["lineNum"] + self.__startLine)))
                     if self.__error == False:
                        changers["#ORA#"]  = "\tORA\t" + first + "\n"
                        changers["#TEMP#"] = first

                        mask1 = "#%" + ("0" * (8 - len(var2.usedtBits))) + "1" + ("0" * (len(var2.usedtBits) - 1))
                        mask2 = "#%00000001"

                        if dimension == "L":
                           changers["#MASK1#"] = mask1
                           changers["#MASK2#"] = mask2
                        else:
                           changers["#MASK1#"] = mask2
                           changers["#MASK2#"] = mask1

                 for item in changers:
                     txt = txt.replace(item, changers[item])

                 line["compiled"] = txt

        elif self.isCommandInLineThat(line, "flip"):
            #params = self.getParamsWithTypesAndCheckSyntax(line)
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
                                        self.prepareError("compilerErrorVarNotFound", params["param#2"][0],
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
             #params = self.getParamsWithTypesAndCheckSyntax(line)

             subroutines   = self.__editorBigFrame.collectNamesByCommandFromSections("subroutine", self.__currentBank)
             bank1Routines = self.__editorBigFrame.collectNamesByCommandFromSections("subroutine", "bank1")
             self.removeTheOnesFromTheFirstThatIsInTheSecond(subroutines, bank1Routines)

             if params["param#1"][0] not in bank1Routines:
                 back = ""
                 template = self.__loader.io.loadCommandASM("call")
             else:
                 back = self.__currentBank + "_Call_" + str(self.__magicNumber) + "_Back"
                 self.__magicNumber += 1

                 template = self.__loader.io.loadCommandASM("callToBank1")

             template = template.replace("#LABEL#", self.__currentBank + "_SubRoutine_" + params["param#1"][0])\
                                .replace("#BANKNUM#", str(self.__currentBank)).replace("#BACK#", back)

             if params["param#1"][0] not in subroutines:
                self.addToErrorList(line["lineNum"], self.prepareError("compilerErrorSubroutine", params["param#1"][0],
                                                                        "", "",
                                                                        str(line["lineNum"] + self.__startLine)))

             if self.__error == False:
                save = ""
                if "param#2" in params:
                   if params["param#2"][0] not in self.__noneList:
                       var = self.__loader.virtualMemory.getVariableByName(params["param#2"][0], self.__currentBank)
                       if var == False:
                          var = self.__loader.virtualMemory.getVariableByName(params["param#2"][0], "bank1")

                       if var == False:
                          self.addToErrorList(line["lineNum"], self.prepareError("compilerErrorVarNotFound", params["param#2"][0],
                                                                                   "", "",
                                                                                   str(line["lineNum"] + self.__startLine)))
                       if self.__error == False:
                          self.__temps = self.collectUsedTemps()

                          try:
                               temp1 = self.__temps[0]
                               self.__temps.pop(0)

                               temp2 = self.__temps[0]
                               self.__temps.pop(0)

                          except:
                               self.addToErrorList(self.__thisLine["lineNum"],
                                                   self.prepareError("compilerErrorStatementTemps", params["param#1"][0],
                                                                     "", "",
                                                                     str(self.__thisLine["lineNum"] + self.__startLine)))
                          self.__temps = self.collectUsedTemps()
                          save += self.convertAny2Any(var, "FROM", params, self.__temps)
                          save += "\tSTA\t" + params["param#2"][0] + "\n"

                          template = template.replace("!!!SAVE!!!", save)
                line["compiled"] = template


        elif self.isCommandInLineThat(line, "callIf"):
            statement     = line["param#1"][0]
            portStateCode = self.__virtualMemory.returnCodeOfPortState(statement)

            if portStateCode == False:
                smallerCommands, temps = self.convertStatementToSmallerCodes("comprass",
                                                                             statement, line)
                smallerCommandLines = smallerCommands.split("\n")

                line["compiled"] = self.comprassThing(smallerCommandLines, line, linesFeteched)


                self.__magicNumber += 1
                label = self.__currentBank + "_" + str(self.__magicNumber) + "_CallIf_JumpOver"

                currentComprass = self.findCompass(statement)
                compassLine = self.fuseTempsAndLogical(temps[0], temps[1], currentComprass,
                                                             label)



                listOfThem = ["BEQ", "BNE", "BCC", "BCS"]
                for itemNum in range(0, len(listOfThem)):
                    item = listOfThem[itemNum]
                    if item in compassLine:
                        compassLine = compassLine.replace(item, listOfThem[itemNum^1])
                        break

                line["compiled"] += compassLine
                line["compiled"] = self.simplifyCompassShit(line["compiled"], temps)

                #print(line["compiled"].split("\n"))
            else:
                line["compiled"] = portStateCode
                self.__magicNumber += 1

                label   = self.__currentBank + "_" + str(self.__magicNumber) + "_CallIf_JumpOver"
                labelOk = self.__currentBank + "_" + str(self.__magicNumber) + "_CallIf_OK"

                line["compiled"] = line["compiled"].replace("#LABEL#", label).replace("#OKLABEL#" , labelOk)

            subline = deepcopy(line)
            subline["command"] = ["call", [0, 3]]
            subline["param#1"] = line["param#2"]
            subline["param#2"] = line["param#3"]
            subline["param#3"] = [None, [-1, -1]]

            subline["fullLine"] = "\tcall(" + subline["param#1"][0]
            if subline["param#2"][0] not in [None, "None", ""]:
                subline["fullLine"] += ", " + subline["param#2"][0] + ")"

            subline["fullLine"] += ")"
            subline["compiled"] = ""

            self.processLine(subline, linesFeteched)
            line["compiled"] += subline["compiled"]

            line["compiled"] += label + "\n"

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
               endLine["labelsBefore"].append(name + "End")
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
                                                 self.prepareError("compilerErrorVarNotFound", params["param#2"][0],
                                                                    "", "",
                                                                    str(line["lineNum"] + self.__startLine)))

                          else:
                              txt += "\tLDA\t" + varName + "\n"
                              txt += self.convertAny2Any(var, "TO", params, self.__temps)
                              txt += "\tSTA\titem\n\tJSR\t" + name + "JumpOver\n"

                              if isWriting:
                                 txt += "\tLDA\titem\n"
                                 txt += self.convertAny2Any(var, "FROM", params, self.__temps)
                                 txt += "\tSTA\t" + varName + "\n"

                      txt += "\tJMP\t" + name + "End\n" + name + "Loop" + "\n" + "\tRTS\n" + name + "JompOver\n"

                   self.changeIfYouCanSaveToItem(False)

               elif self.isCommandInLineThat(line, "do-until") or self.isCommandInLineThat(line, "do-while"):
                   opcode = ""
                   txt += name + "Loop" + "\n"

                   statement = line["param#1"][0]
                   portStateCode = self.__virtualMemory.returnCodeOfPortState(statement)

                   if portStateCode == False:
                       smallerCommands, temps = self.convertStatementToSmallerCodes("do-until",
                                                                                    statement, line)
                       smallerCommandLines = smallerCommands.split("\n")

                       #print(smallerCommandLines)

                       if self.__error == False:

                           txt = self.comprassThing(smallerCommandLines, line, linesFeteched)

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
                           txt  = self.simplifyCompassShit(txt, temps)
                   else:
                       txt = portStateCode

                       label   = name + "End"
                       labelOk = name + "OK"

                       txt = txt.replace("#LABEL#", label).replace("#OKLABEL#", labelOk)

                   line["compiled"] = txt

        elif self.isCommandInLineThat(line, "select"):
             line["magicNumber"] = str(self.__magicNumber)
             self.__magicNumber += 1

             name = self.__currentBank + "_" + line["magicNumber"] + "_Select_"

             #end = self.__editorBigFrame.findEnd(line, line["lineNum"], self.__text)
             end      = self.__editorBigFrame.findEnd(line, line["lineNum"], self.__text)
             #print(self.__text, end)

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
                endLine["labelsBefore"].append(name + "End")

                caseNum = -1

                for case in cases:
                    caseNum += 1
                    caseLine = linesFeteched[case["lineNum"]]
                    caseLine["labelsAfter"].append(name + "Case_" + str(caseNum))
                    caseLine["magicNumber"] = line["magicNumber"]

                if len(defaults) > 0:
                    defaultLine = linesFeteched[defaults[0]["lineNum"]]
                    defaultLine["labelsAfter"].append(name + "Default")
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
                       self.convertAny2Any(var, "TO", params, self.__temps)

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


                              try:
                                     txt = "\tTAX\n\tLDA\t" + cmp + "\n"+ \
                                           self.convertAny2Any(caseVar, "TO", params, self.__temps) +\
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

                            #print(statement)
                            portStateCode = self.__virtualMemory.returnCodeOfPortState(statement)

                            if portStateCode == False:
                                smallerCommands, temps = self.convertStatementToSmallerCodes("comprass",
                                                                                      statement, caseLine)
                                smallerCommandLines = smallerCommands.split("\n")

                                if self.__error == True: break

                                line["compiled"] = self.comprassThing(smallerCommandLines, line, linesFeteched)

                                currentComprass = self.findCompass(statement)
                                line["compiled"] += self.fuseTempsAndLogical(temps[0], temps[1], currentComprass, name + "Case_" + str(caseNum))
                                line["compiled"]  = self.simplifyCompassShit(line["compiled"], temps)
                            else:
                                line["compiled"] = portStateCode

                                label   = name + "Case_"   + str(caseNum)
                                labelOk = name + "CaseOK_" + str(caseNum)
                                line["compiled"] = line["compiled"].replace("#LABEL#", label).replace("#OKLABEL#", labelOk)


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

            #params  = self.getParamsWithTypesAndCheckSyntax(line)

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
            #params     = self.getParamsWithTypesAndCheckSyntax(line)
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
             #params = self.getParamsWithTypesAndCheckSyntax(line)
             line["labelsBefore"].append(self.__currentBank + "_SubRoutine_" + params["param#1"][0][1:-1] + "\n")

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

             if noRTS == False:
                 if self.__currentBank.lower() != "bank1":
                    line["compiled"] = "\tRTS\n"
                 else:
                    line["compiled"] += self.__loader.io.loadCommandASM("returnFromBank1")

        elif self.isCommandInLineThat(line, "set"):
            line["compiled"] = self.saveAValue(params, "param#2", "param#1", line)

        elif self.isCommandInLineThat(line, "init"):

            subLine = self.__editorBigFrame.getLineStructure(0, ["\tsetAll(" + params["param#1"][0] + ", 0)"], False)
            self.processLine(subLine, linesFeteched)
            line["compiled"] = subLine["compiled"]

        elif self.isCommandInLineThat(line, "setAll"):
            array = params["param#1"][0]

            if array not in self.__loader.virtualMemory.arrays.keys() or \
                    (self.__virtualMemory.getArrayValidity(array) not in [self.__currentBank, "bank1", "global"]):
                self.addToErrorList(line["lineNum"],
                                    self.prepareError("compilerErrorArrayNotFound", array,
                                                      "", "",
                                                      str(line["lineNum"] + self.__startLine)))
            groups   = {}

            val = self.__loader.virtualMemory.getVariableByName(params["param#2"][0],
                                                                self.__currentBank)

            if self.__error == False:
               txt = ""

               self.__temps = self.collectUsedTemps()
               buffer = self.__temps[0]
               self.__temps.pop(0)

               for varName in self.__virtualMemory.arrays[array]:
                   var = self.__loader.virtualMemory.getVariableByName2(varName)
                   bits = "".join(var.usedBits)

                   if var.bcd: bits = bits + "b"

                   if bits not in groups.keys(): groups[bits] = []
                   groups[bits].append(varName)

               for group in groups:
                   starter  = ""
                   firstVar = self.__loader.virtualMemory.getVariableByName2(groups[group][0])
                   if val == False:
                      starter = "\tLDA\t#%" + self.bibBinBin(params["param#2"][0], groups[group][0], firstVar.bcd, params, 2) + "\n"
                   else:
                      if val.bcd:
                         starter = "\tLDA\t" + params["param#2"][0] + "\n" + self.convertAny2Any(params["param#2"][0], "TO", params, self.__temps)
                         startingBit = min(firstVar.bits)
                         shifting = ""
                         if (8 - startingBit) < startingBit:
                             shifting = "\tROR\n" * (8 - startingBit)
                             forAND = ""
                             for num in range(7, -1, -1):
                                 if num in firstVar.bits:
                                     forAND += "1"
                                 else:
                                     forAND += "0"
                             shifting += "\tAND\t#%" + forAND + "\n"
                         else:
                             shifting = "\tASL\n" * startingBit

                         starter += shifting

                      else:
                         starter    = "\tLDA\t" + params["param#2"][0] + "\n"
                         minBitSrc  = min(val.usedBits)
                         minBitDest = min(firstVar.usedBits)

                         forAND = ""
                         if val.type != "byte":
                             for num in range(7, -1, -1):
                                 if num in val.bits:
                                     forAND += "1"
                                 else:
                                     forAND += "0"

                             forAND = "\tAND\t#%" + forAND + "\n"

                         shiftNum    = minBitDest - minBitSrc
                         if shiftNum > -1:
                            shiftNum = abs(shiftNum)
                            if shiftNum  < 5:
                               shiftWord = "ASL"
                            else:
                               shiftWord = "ROR"
                               shiftNum  = 8 - shiftNum
                         else:
                            shiftNum = abs(shiftNum)
                            if shiftNum  < 5:
                               shiftWord = "LSR"
                            else:
                               shiftWord = "ROL"
                               shiftNum  = 8 - shiftNum

                         shifting = forAND + ("\t" + (shiftWord + "\n") * shiftNum)
                         starter += shifting

                   if firstVar.type != "byte":
                      starter += "\tSTA\t" + buffer + "\n"
                   txt += starter

                   AND = ""
                   if firstVar.type != "byte":
                      bits = ""
                      for num in range(0, 8):
                          if num in (firstVar.usedBits):
                             bits = "0" + bits
                          else:
                             bits = "1" + bits
                      AND = "\tAND\t#%" + bits + "\n\tORA\t" + buffer + "\n"

                   for varName in groups[group]:
                       load = ""
                       if firstVar.type != "byte":
                          load = "\tLDA\t" + varName + "\n" + AND

                       txt += "\tSTA\t" + varName + "\n"

        elif self.isCommandInLineThat(line, "return"):
             #params = self.getParamsWithTypesAndCheckSyntax(line)
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
                   line["compiled"]  = "\tLDA\t" + params["param#1"][0] + "\n"
                   line["compiled"] += self.convertAny2Any(var, "TO", params, None)

             else:
                 line["compiled"] = "\tLDA\t#" + params["param#1"][0].replace("#", "") + "\n"

             if self.__currentBank > 1:
                line["compiled"] += "\tRTS\n"
             else:
                line["compiled"] += self.__loader.io.loadCommandASM("returnFromBank1")

        elif self.isCommandInLineThat(line, "screen"):
             #params = self.getParamsWithTypesAndCheckSyntax(line)
             line["labelsBefore"].append(self.__currentBank + "_Screen_" + params["param#1"][0][1:1] + "\n")
             #line["compiled"] = "\tLDX\titem\n\tTXS\n"

        elif self.isCommandInLineThat(line, "end-screen"):
            if self.__currentBank > 1:
               line["compiled"] = "\tTSX\n\tSTX\titem\n\tRTS\n"
            else:
               line["compiled"] += "\tTSX\n\tSTX\titem\n" + self.__loader.io.loadCommandASM("returnFromBank1")

        #elif self.isCommandInLineThat(line, "const"):
        #    line["compiled"] = ""
        elif self.isCommandInLineThat(line, "smallest") or self.isCommandInLineThat(line, "largest"):
            if self.isCommandInLineThat(line, "smallest"):
               mode = "SMALLEST"
            else:
               mode = "BIGGEST"

            self.__temps = self.collectUsedTemps()

            tempVar = params["param#1"][0]
            saveVar = self.__loader.virtualMemory.getVariableByName2(tempVar)
            if saveVar == False:
                self.addToErrorList(line["lineNum"],
                                    self.prepareError("compilerErrorVarNotFound",
                                                      saveVar,
                                                      "", "",
                                                      str(line["lineNum"] + self.__startLine)))

            if self.__error == False:
                isTempUsed = False
                if saveVar.type != "byte" or saveVar.bcd:
                    isTempUsed = True
                    try:
                        tempVar = self.__temps[0]
                        self.__temps.pop(0)
                    except:
                        self.addToErrorList(line["lineNum"],
                                            self.prepareError("compilerErrorStatementTemps", params["param#3"][0],
                                                              "", "",
                                                              str(line["lineNum"] + self.__startLine)))
                if self.__error == False:
                    array = params["param#2"][0]

                    if array not in self.__loader.virtualMemory.arrays.keys() or \
                            (self.__virtualMemory.getArrayValidity(array) not in [self.__currentBank, "bank1", "global"]):
                        self.addToErrorList(line["lineNum"],
                                            self.prepareError("compilerErrorArrayNotFound", array,
                                                              "", "",
                                                              str(line["lineNum"] + self.__startLine)))
                    if self.__error == False:
                        if mode == 'BIGGEST':
                           txt = "\tLDA\t#0\n\tSTA\t"   + tempVar + "\n"
                        else:
                           txt = "\tLDA\t#255\n\tSTA\t" + tempVar + "\n"

                        index = -1
                        for varName in self.__virtualMemory.arrays[array]:
                            index += 1
                            if self.__error: break

                            subTxt = "\tLDA\t" + varName + "\n"
                            var = self.__loader.virtualMemory.getVariableByName2(varName)
                            if var == False:
                                self.addToErrorList(line["lineNum"],
                                                    self.prepareError("compilerErrorVarNotFound",
                                                                      varName,
                                                                      "", "",
                                                                      str(line["lineNum"] + self.__startLine)))
                            subTxt += self.convertAny2Any(varName, "TO", params, self.__temps) + "\n"

                            if mode == "BIGGEST":
                               com  = "BCC"
                            else:
                               com  = "BCS"

                            subTxt += "\tCMP\t" + tempVar + "\n\t" + com + "\t#BANK#_#MAGIC#_DontSave_" + str(index) \
                                  + "\n\tSTA\t" + tempVar + "\n"         +   "#BANK#_#MAGIC#_DontSave_" + str(index) + "\n"

                            txt += subTxt

                    if self.__error == False:
                       if isTempUsed:
                          txt += "\tLDA\t" + tempVar + "\n" + self.convertAny2Any(saveVar, "FROM", params, self.__temps) + "\n\tSTA\t" + params["param#1"][0] + "\n"
                       line["compiled"] = txt


        elif self.isCommandInLineThat(line, "min") or self.isCommandInLineThat(line, "max"):
            self.__temps = self.collectUsedTemps()

            if self.isCommandInLineThat(line, "min"):
               mode = "MIN"
            else:
               mode = "MAX"

            source = params["param#1"][0]
            sourceVar = self.__loader.virtualMemory.getVariableByName2(source)

            compare = params["param#2"][0]
            compareVar = self.__loader.virtualMemory.getVariableByName2(compare)

            if "param#3" not in params:
                params["param#3"] = params["param#1"]

            dest        = params["param#3"][0]
            destVar     = self.__loader.virtualMemory.getVariableByName2(dest)

            self.__magicNumber += 1
            allTheSame, hasBCD = self.paramsHaveBCDandBinaryAtTheSameTime(params)

            if mode == "MIN":
               var1    = source
               var1Var = sourceVar

               temp    = compare
               tempVar = compareVar

               extra   = True
            else:
               var1    = compare
               var1Var = compareVar

               temp    = source
               tempVar = sourceVar

               extra   = False

            template = self.__loader.io.loadCommandASM("minmax")
            if extra:
               template = template.replace("!!!extraLDA!!!", "\tLDA\t#VARTEMP#\n")

            template = template.replace("#VAR01#", var1).replace("!!!to8bit!!!",
                                                                   self.convertAny2Any(var1Var, "TO", params,
                                                                                       self.__temps))
            template = template.replace("#VAR03#", dest).replace("!!!from8bit!!!",
                                                                   self.convertAny2Any(destVar, "FROM", params,
                                                                                       self.__temps))
            itWasDone = False
            if tempVar != False:
               if tempVar.type != "byte" or tempVar.bcd and allTheSame == False:
                   try:
                       first = self.__temps[0]
                       template = template.replace("#VARTEMP#", first)
                       self.__temps.pop(0)
                   except:
                       self.addToErrorList(self.__thisLine["lineNum"],
                                              self.prepareError("compilerErrorStatementTemps", params["param#2"][0],
                                                                "", "",
                                                                str(self.__thisLine["lineNum"] + self.__startLine)))


                   if self.__error == False:
                      template = template.replace("!!!convertCompare!!!", "\tLDA\t" + temp + "\n" +
                                                 self.convertAny2Any(tempVar, "TO", params,
                                                                     self.__temps)                  +
                                                 "\n\tSTA\t" + first + '\n'
                                                 )

            if itWasDone == False:
               template = template.replace("#VARTEMP#", temp)

            template = template.replace("#MAGIC#", str(self.__magicNumber)).replace("#BANK#", self.__currentBank)

            self.checkASMCode(template, line, linesFeteched)
            if self.__error == False:
               line["compiled"] = template

        elif self.isCommandInLineThat(line, "peek") or self.isCommandInLineThat(line, "poke"):
            if self.isCommandInLineThat(line, "peek"):
               mode = "peek"
            else:
               mode = "poke"

            register = self.__virtualMemory.registers[params["param#1"][0]]
            var      = self.__loader.virtualMemory.getVariableByName2(params["param#2"][0])

            self.__temps = self.collectUsedTemps()

            txt = ""

            if mode == "poke":
               to8Bit = ""
               if var != False:
                  to8Bit = self.convertAny2Any(params["param#2"][0], "TO", params, self.__temps)

               txt = "\tLDA\t" + params["param#2"][0] + "\n" + to8Bit + "\n\tSTA\t" + params["param#1"][0] + "\n"

            else:
                from8bit = ""
                if var != False:
                    from8bit = self.convertAny2Any(params["param#2"][0], "FROM", params, self.__temps)

                txt = "\tLDA\t" + params["param#1"][0] + "\n" + from8bit + "\n\tSTA\t" + params["param#2"][0] + "\n"

            self.checkASMCode(txt, line, linesFeteched)
            if self.__error == False:
                line["compiled"] = txt

        elif self.isCommandInLineThat(line, "bitOn") or self.isCommandInLineThat(line, "bitOff"):
            sourceTxt        = ""
            convertSecondTxt = ""
            changingBitsTxt  = ""
            destTxt          = ""
            makeThemSpace    = False

            self.__temps = self.collectUsedTemps()

            if self.isCommandInLineThat(line, "bitOn"):
               direction = "ON"
            else:
               direction = "OFF"

            source        = params["param#1"][0]
            sourceVar     = self.__loader.virtualMemory.getVariableByName2(source)
            if sourceVar != False:
               sourceTxt  = "\tLDA\t" + source + "\n" + self.convertAny2Any(sourceVar, "TO", params, self.__temps) + "\n"
            else:
               try:
                   number = self.__editorBigFrame.convertStringNumToNumber(source)%256
               except:
                   number = self.__editorBigFrame.convertStringNumToNumber(self.getConstValue(source))%256

               sourceTxt  = "\tLDA\t#" + str(number) + "\n"

            if "param#3" not in params.keys():
                params["param#3"] = params["param#1"]

            dest        = params["param#3"][0]
            destVar     = self.__loader.virtualMemory.getVariableByName2(dest)
            if destVar != False:
               destTxt  = self.convertAny2Any(destVar, "FROM", params, self.__temps) + "\n\tSTA\t" + dest + "\n"

            bitNum      = params["param#2"][0]
            bitNumVar   = self.__loader.virtualMemory.getVariableByName2(bitNum)

            if bitNumVar == False:
               try:
                   number = self.__editorBigFrame.convertStringNumToNumber(bitNum) % 8
               except:
                   number = self.__editorBigFrame.convertStringNumToNumber(self.getConstValue(bitNum))%8

               if source == dest:
                  sourceText       = ""
                  destText         = ""
                  convertSecondTxt = ""
                  vList            = {"ON": 1, "OFF": 0}

                  changingBitsTxt  = self.bitChanger(source, vList[direction], number + min(sourceVar.usedBits))
                  makeThemSpace    = True
               else:
                   if direction == "ON":
                       changingBitsTxt = "\tORA\t#%00000000\n"
                       changeIndex = len(changingBitsTxt) - number - 2
                       changingBitsTxt = changingBitsTxt[:changeIndex] + "1" + changingBitsTxt[changeIndex + 1:]

                   else:
                       changingBitsTxt = "\tAND\t#%11111111\n"
                       changeIndex = len(changingBitsTxt) - number - 2
                       changingBitsTxt = changingBitsTxt[:changeIndex] + "0" + changingBitsTxt[changeIndex + 1:]

            else:

                convertSecondTxt = "\tLDA\t" + bitNum + "\n" + self.convertAny2Any(bitNumVar, "TO", params, self.__temps) +\
                                   '\n\tAND\t#%00000111\n\tTAX\n'

                try:
                    first = self.__temps[0]
                    self.__temps.pop(0)
                except:
                    self.addToErrorList(self.__thisLine["lineNum"],
                                        self.prepareError("compilerErrorStatementTemps", params["param#2"][0],
                                                          "", "",
                                                          str(self.__thisLine["lineNum"] + self.__startLine)))

                if self.__error == False:
                   self.__magicNumber += 1

                   opcode = ["ORA", "AND"]
                   masks  = ["00000001", "11111110"]

                   if direction == 'ON':
                      num = 0
                   else:
                      num = 1

                   label               = "#BANK#_Shift_#MAGIC#"
                   exitLabel           = "#BANK#_Shift_#MAGIC#_End"

                   convertSecondTxt   += '\tLDA\t#%'+ masks[num] + '\n\tDEX\n\tBMI\t' + exitLabel + '\n' +\
                                         label + "\n\tASL\n\tDEX\n\tBPL\t" + label + "\n" + exitLabel + "\n\tSTA\t" + first + "\n"

                   changingBitsTxt     = '\t' + opcode[num] + "\t" + first + "\n"

            if self.__error == False:
               if makeThemSpace:
                  fullText = changingBitsTxt
               else:
                  fullText = convertSecondTxt + sourceTxt + changingBitsTxt + destTxt
               #print("#1\n", sourceTxt)
               #print("#2\n", changingBitsTxt)
               #print("#3\n", destTxt)

               fullText = fullText.replace("#BANK#", self.__currentBank).replace("#SECTION#", self.__currentSection).replace("#MAGIC#", str(self.__magicNumber))


               self.checkASMCode(fullText, line, linesFeteched)
               if self.__error == False:
                  line["compiled"] = fullText

            else:
                line["compiled"]   = ""

        elif line["command"][0].startswith("end") \
          or self.isCommandInLineThat(line, "exit") :
             pass

        elif self.isCommandInLineThat(line, "sum") or self.isCommandInLineThat(line, "avg"):
            varName = params["param#1"][0]
            arrName = params["param#2"][0]

            var = self.__loader.virtualMemory.getVariableByName2(varName)
            if var == False:
                self.addToErrorList(line["lineNum"],
                                    self.prepareError("compilerErrorVarNotFound",
                                                      varName,
                                                      "", "",
                                                      str(line["lineNum"] + self.__startLine)))

            if arrName not in self.__loader.virtualMemory.arrays.keys() or \
                             (self.__virtualMemory.getArrayValidity(arrName) not in [self.__currentBank, "bank1", "global"]):
                              self.addToErrorList(line["lineNum"],
                                                      self.prepareError("compilerErrorArrayNotFound", arrName,
                                                      "", "",
                                                      str(line["lineNum"] + self.__startLine)))

            if self.__error == False:
               self.__temps = self.collectUsedTemps()

               try:
                   tempVarName = self.__temps[0]
                   self.__temps.pop(0)
               except:
                   self.addToErrorList(self.__thisLine["lineNum"],
                                       self.prepareError("compilerErrorStatementTemps", params["param#1"][0],
                                                         "", "",
                                                         str(self.__thisLine["lineNum"] + self.__startLine)))
               first = True
               for inpVarname in self.__loader.virtualMemory.arrays[arrName]:
                   inputVar = self.__loader.virtualMemory.getVariableByName2(inpVarname)
                   if inputVar == False:
                       self.addToErrorList(line["lineNum"],
                                           self.prepareError("compilerErrorVarNotFound",
                                                             inpVarname,
                                                             "", "",
                                                             str(line["lineNum"] + self.__startLine)))
                       break

                   if first:
                      first = False
                      txt = "\tLDA\t" + inpVarname + "\n" + self.convertAny2Any(inputVar, "TO", params, self.__temps) + "\n"
                   else:
                      if inputVar.type == "byte" and inputVar.bcd == False:
                         txt += "\tCLC\n\tADC\t" + inpVarname + "\n"
                      else:
                         txt += "\tSTA\t" + tempVarName + "\n\tLDA\t" + inpVarname + "\n\t" + \
                                self.convertAny2Any(inputVar, "TO", params, self.__temps)   + \
                                "\n\tCLC\n\tADC\t" + tempVarName + "\n"

               if self.__error == False:
                  txt +=  self.convertAny2Any(var, "FROM", params, self.__temps) + "\n\tSTA\t" + varName + "\n"
                  if self.isCommandInLineThat(line, "avg"):
                     subLine          = " div(" + varName + "," + str(len(self.__loader.virtualMemory.arrays[arrName])) + ")"
                     subLineStructure = self.__editorBigFrame.getLineStructure(0, [subLine], False)

                     self.processLine(subLineStructure, linesFeteched)

                     if self.__error == False:
                        txt += subLineStructure["compiled"]

                  if self.__error == False:
                     self.checkASMCode(txt, line, linesFeteched)
                     if self.__error == False:
                        line["compiled"] = txt
                        return

        else:
            #This is where object related commands are handled.

            template, optionalText, objectThings = self.getObjTemplate(line, params)

            if objectThings["extension"] == "a26":
               template = template.split("\n")
               self.preBuildTemplate(template)
               template = self.convertASMlinesToASMCommands(template)

               #print("\n>>\n", "\n".join(template), "\n<<\n")

               result = FirstCompiler(self.__loader, self.__editorBigFrame, "\n".join(template), False,
                                   self.__mode, self.__currentBank, self.__currentSection, self.__startLine, "\n".join(self.__fullText), True).result

               #print("\n>>\n", "\n".join(template), "\n<<\n")

               result = self.reformatResult(result)
            else:
               result = template

            template = result + "\n" + optionalText + "\n"

            if "replaceNum" in objectThings.keys(): template = template.replace("ß", objectThings["replaceNum"])

            if "#MAGIC#" in template:
               self.__magicNumber += 1
               template = template.replace("#MAGIC#", str(self.__magicNumber))

            template = template.replace("#BANK#", self.__currentBank).replace("#SECTION#", self.__currentSection)
            if "#TEMPVAR#" in template:
                try:
                    tempVar = self.__temps[0]
                    self.__temps.pop(0)
                    template = template.replace("#TEMPVAR#", tempVar)
                except:
                    self.addToErrorList(line["lineNum"],
                                        self.prepareError("compilerErrorStatementTemps", params["param#1"][0],
                                                          "", "",
                                                          str(line["lineNum"] + self.__startLine)))

            if self.__error == False:
               self.exceptionList(objectThings["sysVars"], "add")
               self.checkASMCode(template, line, linesFeteched)
               self.exceptionList(objectThings["sysVars"], "delete")

               #print(objectThings["sysVars"])

               if self.__error == False:
                  line["compiled"] = template
                  #print("\n>>>>\n", template, "\n<<<<\n")
                  return

        if "compiled" in line: line["compiled"] = line["compiled"].replace("##", "#")
        else:
            line["compiled"] = ""

        if self.__error == False:
           line["compiled"] = line["compiled"].replace("#BANK#", self.__currentBank).replace("#SECTION#", self.__currentSection)

           if "#MAGIC#" in line["compiled"]:
              self.__magicNumber += 1
              line["compiled"] = line["compiled"].replace("#MAGIC#", str(self.__magicNumber))

           #print("#1", line["compiled"].split("\n")[-1])
           line["compiled"] = self.LDATAYLDA(self.detectUnreachableCode(self.checkForNotNeededExtraLDA(line["compiled"])))
           #print("#2", line["compiled"].split("\n")[-1])

           if line["compiled"] != "": self.checkASMCode(line["compiled"], line, linesFeteched)

           if line["lineNum"] > 0: self.checkIfCLDisFollowedBySED(linesFeteched, line["lineNum"])

        else:
            if "compiled" in line:
                print("ERROR -- ERROR -- ERROR")
                print(line["compiled"])
            line["compiled"] = ""

    def reformatResult(self, result):
        result = result.split("\n")
        newRes = []

        for line in result:
            if len(line) > 0:
               if   line.startswith("*** \t;"):
                    newRes.append(line.replace("*** \t;", "***"))
               elif "asm(" in line:
                    startPoz = -1
                    endPoz   = -1
                    for charNum in range(0, len(line)):
                        if line[charNum] == "(":
                           startPoz = charNum + 2
                           break

                    for charNum in range(len(line)-1, -1, -1):
                        if line[charNum] == ")":
                           endPoz = charNum - 1
                           break

                    newRes.append(line[startPoz:endPoz])
               else:
                    newRes.append(line)

        return "\n".join(newRes)

    def convertASMlinesToASMCommands(self, template):
        newTemplate = []
        for lineNum in range(0, len(template)):
            justAdd    = True

            if len(template[lineNum]) > 0:
                if template[lineNum][0] not in ("#", "*", "!"):
                   lineStruct = self.__editorBigFrame.getLineStructure(0, [template[lineNum]], False)

                   if lineStruct["command"][0] not in self.__noneList:
                      if  lineStruct["command"][0].lower() in self.__canBeFortariCommandAndASMOpCode:
                          for regNum in self.__opcodes.keys():
                              if lineStruct["command"][0].upper() == self.__opcodes[regNum]["opcode"]:

                                 #print("#1)", lineStruct["command"][0])
                                 if lineStruct["("] != -1 and lineStruct[")"] != -1 and len(lineStruct["commas"]) > 1:
                                    break

                                 opcode, value = self.getOpCodeAndOperandFromASMLine(template[lineNum])

                                 #print("#2)", lineStruct["command"][0])
                                 if opcode.upper() != self.__opcodes[regNum]["opcode"]: break

                                 if self.__opcodes[regNum]["format"] != None or value != "":
                                    if self.checkIfASMhasrightOperand(self.__opcodes[regNum], value) == False: continue

                                 #print("#3)", lineStruct["command"][0])

                                 justAdd = False
                                 break
                      else:
                          for regNum in self.__opcodes.keys():
                              if lineStruct["command"][0].upper() == self.__opcodes[regNum]["opcode"]:
                                 justAdd = False
                                 break

            if justAdd:
               newTemplate.append(template[lineNum])
            else:
               lines = template[lineNum].split("\n")
               for line in lines:
                   newTemplate.append(' asm("' + line + '")')
               #print("yyy", template[lineNum])

        #print("shit", "\n".join(newTemplate))
        return newTemplate



    def getObjTemplate(self, line, params):
        if params == None: params = self.getParamsWithTypesAndCheckSyntax(line)
        
        objectThings = self.__objectMaster.returnAllAboutTheObject(line["command"][0])
        template = objectThings["template"]

        self.__temps = self.collectUsedTemps()

        dataReplacers = {
            "playfields": ["##NAME##", "playfield"],
            "backgrounds": ["##NAME##", "background"],
            "sprites": ["##NAME##", "sprites"]
        }
        optionalCounter = -1

        template = objectThings["template"]
        optionalText = ""
        # print(params)

        for num in range(1, 20):
            num = str(num)
            if len(num) == 1: num = "0" + num
            tempString = "temp" + num

            templateLines = template.split("\n")
            for lineX in templateLines:
                if len(lineX) > 0:
                    if lineX[0] not in ("#", "*", "!"):
                        if tempString in template and tempString in self.__temps:
                            self.__temps.remove(tempString)

            for paramName in params.keys():
                if params[paramName][0] == tempString:
                    if tempString in self.__temps:
                        self.__temps.remove(tempString)

        # print(line["command"][0])
        for paramName in params.keys():
            data = ""
            ok = True
            saveIt = None
            convert = ""
            errType = None
            val = ""
            var = ""

            paramIndex = int(paramName[-1]) - 1
            pSettings = objectThings["paramsWithSettings"][paramIndex]
            validParams = pSettings["param"].split("|")

            optional = False
            if paramIndex in objectThings['optionalParamNums']: optional = True

            if params[paramName][1] not in validParams:
                ok = False
            # print(paramName, ok, params[paramName][1], validParams)
            errPrint = False

            if ok:
                if params[paramName][1] == "number":
                    try:
                        numVal = self.__editorBigFrame.convertStringNumToNumber(params[paramName][0])
                        if objectThings["extension"] == "asm":
                            saveIt = "#" + str(numVal)
                        else:
                            saveIt = str(numVal)
                    except:
                        ok = False
                        errType = "NotValidNumber"
                        # if errPrint: print("#1")

                elif params[paramName][1] == "stringConst":
                    ok = False
                    errType = "ConstNotFound"
                    for const in self.__constants:
                        if const == params[paramName][0]:
                            try:
                                numVal = self.__editorBigFrame.convertStringNumToNumber(self.getConstValue(const))
                                if objectThings["extension"] == "aam":
                                    saveIt = "#" + str(numVal)
                                else:
                                    saveIt = str(numVal)
                                break
                            except:
                                ok = False
                                errType = "ConstValNotValidNumber"
                                val = self.getConstValue(const)
                                # if errPrint: print("#2")

                elif params[paramName][1] == "string":
                    pass

                elif params[paramName][1] == "data":
                    path = self.__loader.mainWindow.projectPath + pSettings["folder"] + "/" + params[paramName][
                        0] + ".asm"
                    dataF = open(path, "r")
                    data = dataF.read()
                    dataF.close()
                    saveIt   = self.__currentBank + "_" + params[paramName][0] + "_" + dataReplacers[pSettings["folder"]][
                        1]

                    if "loadAndUse" in objectThings.keys():
                        if objectThings["loadAndUse"][0] == paramName:
                            template = self.useItThings(template, data, objectThings["loadAndUse"][1], objectThings)

                else:
                    var = self.__loader.virtualMemory.getVariableByName2(params[paramName][0])
                    if var == False:
                        self.addToErrorList(line["lineNum"],
                                            self.prepareError("compilerErrorVarNotFound",
                                                              params[paramName][0],
                                                              "", "",
                                                              str(line["lineNum"] + self.__startLine)))
                    if self.__error == False:
                        saveIt = params[paramName][0]
                        if var.type != "byte" or var.bcd:
                            direction = objectThings["direction"][0]
                            if "converter" in pSettings:
                                if "TO" in pSettings["converter"].upper(): direction = "TO"
                                if "FROM" in pSettings["converter"].upper(): direction = "FROM"

                            convert = self.convertAny2Any(params[paramName][0], direction, params, self.__temps)

                if errPrint: print(errType)
                if errType != None:
                    self.addToErrorList(line["lineNum"],
                                        self.prepareError("compilerError" + errType,
                                                          params[paramName][0],
                                                          val, var,
                                                          str(line["lineNum"] + self.__startLine)))
                # print("Error?")
                if self.__error == False:
                    # print("noError")
                    if "replacer" in pSettings:
                        replacer = pSettings["replacer"]
                        if params[paramName][1] != "data":
                           template = template.replace(replacer, saveIt)
                        else:
                           if objectThings["extension"] == "asm":
                              template = template.replace(replacer, saveIt)
                           else:
                              template = template.split("\n")
                              for lineNum in range(0, len(template)):
                                  lineS = self.__editorBigFrame.getLineStructure(0, [template[lineNum]], False)
                                  if self.isCommandInLineThat(lineS, "asm"):
                                     template[lineNum] = template[lineNum].replace(replacer, saveIt)
                                  else:
                                     template[lineNum] = template[lineNum].replace(replacer, params[paramName][0])
                              template = "\n".join(template)


                    if "converter" in pSettings:
                        converter = pSettings["converter"]

                        template = template.split("\n")
                        for templateLineNum in range(0, len(template)):
                            if template[templateLineNum] != "":
                                if template[templateLineNum][0] not in ("*", "#"):
                                    template[templateLineNum] = template[templateLineNum].replace(converter, convert)

                        template = "\n".join(template)

                        # template    = template.replace(converter, convert)

                    if "folder" in pSettings.keys():
                        dataR = dataReplacers[pSettings["folder"]][0]
                        name = self.__currentBank + "_" + params[paramName][0] + "_" + \
                               dataReplacers[pSettings["folder"]][1]
                        data = data.replace(dataR, name)
                        template = template.replace(dataR, name).replace(replacer, name)

                        self.bank1Data[name] = data

                    # print("optional" in objectThings.keys(), optional)
                    if "optional" in objectThings.keys() and optional:
                        optionalCounter += 1
                        optP = "/".join(objectThings["path"].split("\\")[:-1])

                        if len(objectThings["optional"]) >= optionalCounter + 1:
                            path = optP + "/" + objectThings["optional"][optionalCounter] + ".asm"
                            dataF = open(path, "r")
                            optD = dataF.read()
                            dataF.close()

                            if objectThings["extension"] == "asm":
                                template = template.replace("!!!Optional!!!", self.editOptionalTemplate(objectThings,
                                                                                                        optD, params[
                                                                                                            paramName],
                                                                                                        pSettings,
                                                                                                        optionalCounter,
                                                                                                        data))
                            else:
                                optionalText = self.editOptionalTemplate(objectThings,
                                                                         optD, params[paramName], pSettings,
                                                                         optionalCounter, data)

        if "loadAndUse" in objectThings.keys():
            #
            # This is only used on "Min" settings where the min requires no real data
            #

            if objectThings["loadAndUse"][0] == "param#0":
                dummy = "dummy1=256\n" * 10
                template = self.useItThings(template, dummy, objectThings["loadAndUse"][1], objectThings)
        else:
            if "#DELETE" in template:
                template = re.sub(r'###DELETE-FROM.+###FELETE-TO', "", template, flags=re.DOTALL)


        if "ifConstParams" in objectThings.keys():
            types = []
            for num in objectThings["ifConstParams"]:
                types.append(params["param#" + num][1])
            if "variable" not in types:
                if objectThings["ifConstFunc"][0][1:] == "etSubMenuTileData":
                    template = ""
                    values = []

                    for num in objectThings["ifConstParams"]:
                        pType = params["param#" + num][1]
                        pVal = params["param#" + num][0]

                        if pType == "constant":
                            pVal = str(self.__constants[pVal])
                        if "#" in pVal:
                            pVal = pVal.replace("#", "")

                        values.append(pVal)

                    tileVarNum = ""
                    if len(values) == 2:
                        tileVarNum = str(int(values[0]) + 1) + "_" + str(int(values[1]) + 1)
                    else:
                        n = int(values[0])

                        tileVarNum = self.stupidList[n]

                    theVarName = params["param#1"][0]
                    theVar = self.__loader.virtualMemory.getVariableByName2(theVarName)

                    if objectThings["ifConstFunc"][0][0] == "s":
                        to8Bit = ""
                        if theVar == False:
                            if theVarName in self.__constants: theVarName = str(self.__constants[theVarName])
                            theVarName = self.valOfNumber(theVarName) % 16
                            theVarName = "#" + str(theVarName)
                        else:
                            if theVar.type != "byte" or theVar.bcd:
                                to8Bit = self.convertAny2Any(theVar, "TO", params, self.__temps)

                        tileVarNum = "Tile" + tileVarNum
                        ander = ""
                        other = ""

                        if int(tileVarNum[-1]) % 2 == 0:
                            other = "\tASL\n" * 4
                            ander = "\tAND\t#$0F\n"
                            tileVarNum = tileVarNum[:-1] + str(int(tileVarNum[-1]) - 1)
                        else:
                            other = "\tAND\t#$0F\n"
                            ander = "\tAND\t#$F0\n"

                        template = "\tLDA\t" + theVarName + "\n" + to8Bit + "\n" + other + "\tSTA\t#TEMPVAR#\n" + \
                                   "\tLDA\t" + tileVarNum + "\n" + ander + "\tORA\t#TEMPVAR#\n" + "\tSTA\t" + tileVarNum + "\n"
                    else:
                        from8bit = ""
                        if theVar == False:
                            self.addToErrorList(line["lineNum"],
                                                self.prepareError("compilerErrorVarNotFound", params["param#1"][0],
                                                                  "", "",
                                                                  str(line["lineNum"] + self.__startLine)))
                        else:
                            tileVarNum = "Tile" + tileVarNum
                            ander = ""
                            other = ""

                            if theVar.type != "byte" or theVar.bcd:
                                from8bit = self.convertAny2Any(theVar, "FROM", params, self.__temps)

                            if int(tileVarNum[-1]) % 2 == 0:
                                other = "\tLSR\n" * 4
                                ander = "\tAND\t#$F0\n"
                                tileVarNum = tileVarNum[:-1] + str(int(tileVarNum[-1]) - 1)
                            else:
                                ander = "\tAND\t#$0F\n"

                            template = "\tLDA\t" + tileVarNum + "\n" + ander + other + from8bit + "\n" "\tSTA\t" + theVarName + "\n"

        if objectThings["extension"] == "a26":
            for paramNum in range(0, len(objectThings["paramsWithSettings"])):
                param = objectThings["paramsWithSettings"][paramNum]

                if param["mustHave"] == False and paramNum > len(params) - 1:
                    regex = r',[\t\s]{0,}' + param["replacer"]
                    template = re.sub(regex, "", template)
                    template = template.replace(param["replacer"], "")

            for tempNum in range(0, 20):
                if tempNum == 0:
                   tempText = "#TEMPVAR#"
                else:
                   tempText = "#TEMPVAR"+str(tempNum)+"#"

                if tempText in template:
                    try:
                        tempVarOther = self.__temps[0]
                        self.__temps.pop(0)
                        template = template.replace(tempText, tempVarOther)
                    except:
                        self.addToErrorList(line["lineNum"],
                                            self.prepareError("compilerErrorStatementTemps", params["param#1"][0],
                                                              "", "",
                                                              str(line["lineNum"] + self.__startLine)))
                else:
                    if tempNum > 0: break

        #print("\n###1\n", template, "\n###2\n")
        return template, optionalText, objectThings

    def preBuildTemplate(self, template):
        lineNum = -1
        while lineNum < len(template):
              lineNum += 1
              if lineNum >= len(template): break
              #print(lineNum, len(template))
              line  = template[lineNum]
              lineF = self.__editorBigFrame.getLineStructure(0, [line], False)
              if lineF["command"][0] not in self.__noneList:
                 obj = self.__objectMaster.returnAllAboutTheObject(lineF["command"][0])
                 if obj["exist"] == False or obj["extension"] == "asm": continue

                 linesToAdd, dummy, dummy2 = self.getObjTemplate(lineF, None)
                 linesToAdd = linesToAdd.split("\n")
                 #print(linesToAdd)
                 template.pop(lineNum)
                 for sublineNum in range(len(linesToAdd)-1, -1, -1):
                     template.insert(lineNum, linesToAdd[sublineNum])

                 lineNum -= 1

    def useItThings(self, template, data, usage, objectThings):
        if   usage == "setMinAndMaxofPF":
             firstLine = data.split("\n")[0]
             height = int(firstLine.split("=")[1])
             min = 26
             max = 26 + (height - 42)
             template = template.replace("!!!Max!!!", str(max)).replace("!!!Min!!!", str(min))

        elif usage == "setMinAndMaxofPlayer":
            firstLine = data.split("\n")[0]
            max = int(firstLine.split("=")[1])
            min = 1
            template = template.replace("!!!Max!!!", str(max)).replace("!!!Min!!!", str(min))

        elif usage == "setMinAndMaxofPlayerSpriteIndex":
            secondLine = data.split("\n")[1]
            max = int(secondLine.split("=")[1])
            min = 0
            template = template.replace("!!!Max!!!", str(max)).replace("!!!Min!!!", str(min))

        return template

    def deleteNotUsedUpParams(self, line):
        mustChange = False
        lineStruct = self.__editorBigFrame.getLineStructure(0, [line], False)

        for paramNum in range(1, 4):
            key = "param#" + str(paramNum)
            if lineStruct[key][0] not in self.__noneList:
                if lineStruct[key][0][0] == "#":
                    mustChange = True
                    lineStruct[key][0] = ""


        if mustChange == False: return line

        fakeLine = lineStruct["command"][0] + "("
        firstParam = True

        for paramNum in range(1, 4):
            key = "param#" + str(paramNum)
            if lineStruct[key][0] in self.__noneList:
               break

            if firstParam:
               fakeLine += lineStruct[key][0]
               firstParam = False
            else:
               fakeLine += "," + lineStruct[key][0]

        fakeLine += ")"
        #print("fos", fakeLine)

        return fakeLine

    def simplifyCompassShit(self, txt, temps):
        txt = txt.split("\n")

        #0. RemoveBlank
        newTxt = []
        for line in txt:
            if line.isspace() == False and line != "":
               newTxt.append(line)

        txt = newTxt

        #1. If the very first is just a simple load and save to a temp.
        opcode1, value1 = self.getOpCodeAndOperandFromASMLine(txt[0])
        opcode2, value2 = self.getOpCodeAndOperandFromASMLine(txt[1])

        #print(opcode1, opcode2, value1, value2, temps[0], temps[1])
        #print("#1", opcode1.upper() == "LDA", opcode1)
        #print("#2", opcode2.upper() == "STA", opcode2)
        #print("#3", value1 == temps[0], value1, temps[0])

        if opcode1.upper() == "LDA" and opcode2.upper() == "STA" and value2 == temps[0]:
           saveIt    = value1

           txt.pop(0)
           txt.pop(0)

           for lineNum in range(0, len(txt)):
               txt[lineNum] = txt[lineNum].replace(temps[0], saveIt)

        #2. Remove the STA / LDA before the CMP is the same, remove them!

        cmpLineNum = -1
        for lineNum in range(len(txt)-1, -1, -1):
            opcode, value = self.getOpCodeAndOperandFromASMLine(txt[lineNum])
            if opcode.upper() == "CMP":
                cmpLineNum = lineNum
                break

        opcode1, value1 = self.getOpCodeAndOperandFromASMLine(txt[cmpLineNum-2])
        opcode2, value2 = self.getOpCodeAndOperandFromASMLine(txt[cmpLineNum-1])

        #print("#1", txt[cmpLineNum-2])
        #print("#2", txt[cmpLineNum-1])

        if opcode1.upper() == "STA" and opcode2.upper() == "LDA" and value1 == value2:
           txt.pop(cmpLineNum-2)
           txt.pop(cmpLineNum-2)

        #print("\n".join(txt) + "\n")
        return "\n".join(txt) + "\n"


    def bitChanger(self, variable, value, oneBit):
        if type(variable) == str:
           name = variable
           variable = self.__loader.virtualMemory.getVariableByName2(variable)
        else:
           for address in self.__virtualMemory.memory.keys():
               for vName in self.__virtualMemory.memory[address].variables.keys():
                   if self.__virtualMemory.memory[address][vName] == variable:
                      name = vName
                      break

        if type(value) == str:
           try:
               value = self.valOfNumber(value)
           except:
               value = int(self.getConstValue(value))

        value = bin(value).replace("0b", "")

        if oneBit == None:
           bitLen      = len(variable.usedBits)
           largestBit  = max(variable.usedBits)
        else:
           bitLen      = 1
           largestBit  = oneBit

        leadingZeroes = "0" * (bitLen - len(value))

        _and        = self.generateAndOr("AND", leadingZeroes + value, largestBit, bitLen)
        _or         = self.generateAndOr("ORA", leadingZeroes + value, largestBit, bitLen)

        if "1" not in _and and _and != "": _or  = ""
        if "0" not in  _or and  _or != "": _and = ""

        if variable.register == False:
           return "\tLDA\t" + name + "\n" + _and + _or + "\tSTA\t" + name + "\n"
        else:
           return _or.replace("ORA", "LDA") + "\tSTA\t" + name + "\n"

    def generateAndOr(self, command, bitsToInsert, largestBit, bitLen):

        bbb = {"AND": "1", "ORA": "0"}
        #print("###", bitsToInsert)
        while bitLen < len(bitsToInsert):
           bitsToInsert = bitsToInsert[1:]

        if command.upper() == "AND":
            bitsToInsert = len(bitsToInsert) * "0"

        startingPoz = 7 - largestBit

       # print("###", largestBit, bitLen, startingPoz, bitsToInsert)

        bitsToInsert = (bbb[command.upper()] * startingPoz) + bitsToInsert
        bitsToInsert += bbb[command.upper()] * (8 - len(bitsToInsert))

        return "\t" + command + "\t#%" + bitsToInsert + "\n"

    def exceptionList(self, source, method):

        for item in source:
            if method == "add":
               self.__exceptions.append(item)
               if item in self.__readOnly:
                  self.__readOnly.remove(item)
            else:
               self.__exceptions.remove(item)
               if item not in self.__readOnly:
                  self.__readOnly.append(item)

    def editOptionalTemplate(self, objectThings, optionalText, paramData, paramSettings, counter, data):
        if   objectThings["optional"][counter] in ('_heightOfPF'):
             firstLine = data.split("\n")[0]
             height    = int(firstLine.split("=")[1])
             min = 26
             max = 26 + (height - 42)
             optionalText = optionalText.replace("!!!Max!!!", str(max)).replace("!!!Min!!!", str(min))
        elif objectThings["optional"][counter] in ('_heightOfPlayer'):
             firstLine = data.split("\n")[0]
             height = int(firstLine.split("=")[1])
             optionalText = optionalText.replace("!!!Max!!!", str(height))
        elif objectThings["optional"][counter] in ('_indexOfPlayer'):
             secondLine = data.split("\n")[1]
             height = int(secondLine.split("=")[1])
             optionalText = optionalText.replace("!!!Max!!!", str(height))

        return optionalText

    def checkIfCLDisFollowedBySED(self, linesFeteched, lineNum):
        lastvalidLine = -1

        for num in range(lineNum-1, -1, -1):
            if linesFeteched[num] != "":
               lastvalidLine = num
               break

        if lastvalidLine < 0: return

        currentLines = linesFeteched[lineNum]["compiled"].split("\n")
        beforeLines  = linesFeteched[lastvalidLine]["compiled"].split("\n")

        for lineNumX in range(0, len(currentLines)):
            line = currentLines[lineNumX].replace("\t", " ")
            if line == "" or line.isspace() or line[0] not in ["\t", " "]:
                continue

            opcode, value = self.getOpCodeAndOperandFromASMLine(line)
            if opcode.upper() in ("SBC", "ADC"): break
            if opcode.upper() == "SED":
               for subLineNum in range(len(beforeLines) - 1, -1, -1):
                   subLine = beforeLines[subLineNum]
                   if subLine == "" or subLine.isspace() or subLine[0] not in ["\t", " "]:
                      continue

                   sOpcode, Svalue = self.getOpCodeAndOperandFromASMLine(line)

                   if sOpcode.upper() in ("SBC", "ADC"): break
                   if sOpcode.upper() == "CLD":
                      currentLines.pop(lineNumX)
                      linesFeteched[lineNum]["compiled"] = "\n".join(currentLines)

                      beforeLines.pop(subLineNum)
                      linesFeteched[lastvalidLine]["compiled"] = "\n".join(subLineNum)

                      break

               break

    def comprassThing(self, smallerCommandLines, line, linesFeteched):
        txt = ""
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
                txt += subLineStructure["compiled"] + "\n"

        txt = txt.split("\n")

        while True:
            if   txt[-1] == "":
                 txt = txt[:-1]
                 continue
            #elif "STA" in txt[-1]:
            #     txt = txt[:-1]
            break

        return("\n".join(txt) + "\n")

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
            self.addToErrorList(line["lineNum"], self.prepareError("compilerErrorVarNotFound", params["param#2"][0],
                                                                   "", "",
                                                                   str(line["lineNum"] + self.__startLine)))
        if params["param#1"][1] == "variable":
            var1 = self.__loader.virtualMemory.getVariableByName2(params["param#1"][0])
            if var1 == False:
                self.addToErrorList(line["lineNum"], self.prepareError("compilerErrorVarNotFound", params["param#1"][0],
                                                                       "", "",
                                                                       str(line["lineNum"] + self.__startLine)))
            else:
                convert1 = self.convertAny2Any(var1, "TO", params, self.__temps)
                convert2 = self.convertAny2Any(var2, "FROM", params, self.__temps)

                if  convert1 == "" and convert2 == "":
                    txt = "\tLDY\t" + params["param#1"][0] + "\n"
                else:
                    txt = "\tLDA\t" + params["param#1"][0] + "\n" + convert1 + convert2 + "\tTAY\n"


        else:
            times = self.__editorBigFrame.convertStringNumToNumber(params["param#1"][0])

            if times < 3:
               conv1 = self.convertAny2Any(var2, "TO", params, self.__temps)
               conv2 = self.convertAny2Any(var2, "FROM", params, self.__temps)

               line["compiled"] = "\tLDA\t" + params["param#2"][0] + "\n" + conv1 +\
                                   times * ("\t" + command + "\n") + conv2 + "\tSTA\t" + params["param#2"][0] + "\n"
               return
            else:
               txt = "\tLDY\t#" + params["param#1"][0].replace("#", "") + "\n"

        magic = str(self.__magicNumber)
        self.__magicNumber += 1

        name = self.__currentBank + "_Shifting_" + magic + "_"

        conv1 = self.convertAny2Any(var2, "TO", params, self.__temps)
        conv2 = self.convertAny2Any(var2, "FROM", params, self.__temps)

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

        #for l in linesFetched:
        #    print(l["command"][0])

        #print(lineNum, len(linesFetched), linesFetched)

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
                   if paramNum in linesFetched[lNum]:
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
                    if paramNum in linesFetched[lNum]:
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

    def convertAny2Any(self, varName, direction, params, temps):
        txt = ""
        if type(varName) == str:
            var = self.__loader.virtualMemory.getVariableByName2(varName)
        else:
            var = varName
            for name in params:
                if self.__loader.virtualMemory.getVariableByName2(params[name][0]) == var:
                   varName = params[name][0]
                   break

        allTheSame, hasBCD = self.paramsHaveBCDandBinaryAtTheSameTime(params)

        if temps == None:
           temps = self.collectUsedTemps()

        temp1 = ""
        temp2 = ""

        if hasBCD:
            try:
                temp1 = temps[0]
                #temps.pop(0)

                temp2 = temps[1]
                #temps.pop(0)

            except:
                self.addToErrorList(self.__thisLine["lineNum"],
                                    self.prepareError("compilerErrorStatementTemps", params["param#1"][0],
                                                      "", "",
                                                      str(self.__thisLine["lineNum"] + self.__startLine)))
        if self.__error == True:
           return ""
        else:
           if direction.upper() == "TO":
              if var.type != "byte":
                 txt = self.__mainCompiler.convertAnyTo8Bits(var.usedBits)

              if var.bcd == True:
                 if "BCDtoBin_Table" not in self.toRoutines:
                     self.toRoutines["BCDtoBin_Table"] = self.__loader.io.loadSubModule("BCDtoBin_Table")

                 txt = self.__loader.io.loadSubModule("BCDtoBin_2") \
                     .replace("#TEMP1#", temp1).replace("#TEMP2#", temp2)
           else:
               if var.bcd == True:
                   txt += self.__loader.io.loadSubModule("bin2BCD_2") \
                       .replace("#TEMP1#", temp1).replace("#TEMP2#", temp2)

               if var.type != "byte":
                  txt += self.__mainCompiler.save8bitsToAny2(var.usedBits, varName, var.register)

           return txt

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

            allTheSame, hasBCD = self.paramsHaveBCDandBinaryAtTheSameTime(params)
            changeText = {}

            if sourceVar.type != "byte" or sourceVar.bcd == True:
               convert1 = self.convertAny2Any(sourceVar, "TO", params, None)

            if destVar.type != "byte" or destVar.bcd == True:
               convert2 = self.convertAny2Any(destVar, "FROM", params, None)

            line["compiled"] = "\tLDA\t" + params[varHolder][0] + "\n" +\
                               convert1 + shifting + convert2 + "\tSTA\t" + params["param#3"][0] + "\n"

    def prepareDiv(self, params, aaveThisOne):
        saveThisOne = "ST" + aaveThisOne
        changeText = {}

        var1 = self.__loader.virtualMemory.getVariableByName2(params["param#1"][0])
        var2 = self.__loader.virtualMemory.getVariableByName2(params["param#2"][0])
        if "param#3" in params:
            var3 = self.__loader.virtualMemory.getVariableByName2(params["param#3"][0])
        else:
            var3 = None

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


        allTheSame, hasBCD = self.paramsHaveBCDandBinaryAtTheSameTime(params)

        if hasBCD and allTheSame == True:
            changeText["!!!BCDon!!!"] = "\tSED"
            changeText["!!!BCDoff!!!"] = "\tCLD"

        if self.__error == False:
            if var1 != False:
                if var1 != "byte" or (var1.bcd == True and allTheSame == False):
                    changeText["!!!to8Bit1!!!"] = self.convertAny2Any(var1, "TO", params, self.__temps)

            else:
               if hasBCD == True and var1 != None: self.paramToDec(params, 1)

            changeText["#VARTEMP#"] = params["param#2"][0]
            if var2 != False:
                if var2 != "byte" or (var2.bcd == True and allTheSame == False):
                    changeText["!!!to8Bit2!!!"] = "\tLDA\t" + params["param#2"][0] + "\n" + \
                                                      self.convertAny2Any(var2, "TO", params, self.__temps)

                #if var2.type != "byte":
                    changeText["#VARTEMP#"]     = first
                    changeText["!!!staTEMP!!!"] = "\tSTA\t" + first + "\n"
                    changeText["!!!LDAVAR2!!!"] = "\tLDA\t" + params["param#2"][0] + "\n"

                else:
                    changeText["#VARTEMP#"] = params["param#2"][0]

            else:
                if hasBCD == True: self.paramToDec(params, 2)
                changeText["#VARTEMP#"] = params["param#2"][0]

        if var3 != False:
           changeText["!!!from8bit!!!"] = ""

           if var3 != "byte" or (var3.bcd == True and allTheSame == False):
              changeText["!!!from8bit!!!"] = self.convertAny2Any(var3, "FROM", params, self.__temps)

           else:
               if hasBCD == True and var3 != None: self.paramToDec(params, 3)

        if saveThisOne == "A":
           changeText["#SAVECOMMAND#"] = "STA"
        else:
           changeText["#SAVECOMMAND#"] = "STY"
           if "!!!from8bit!!!" in changeText.keys() and changeText["!!!from8bit!!!"] != "":
              changeText["!!!TAY!!!"]     = "\tTAY"
              changeText["!!!TYA!!!"]     = "\tTYA"

        return changeText

    def bibBinBin(self, num, var, hasBCD, params, paramNum):
        num = self.__editorBigFrame.convertStringNumToNumber(num) % 256

        if hasBCD: self.paramToDec(params, paramNum)

        binary = bin(self.__editorBigFrame.convertStringNumToNumber(num) % 256).replace("0b", "")
        binary = "0" * (8 - len(binary)) + binary

        if var.type != "byte":
            binary = binary[(8 - len(var.usedBits)):8]
            largest = max(var.usedBits)
            binary = "0" * (7 - largest) + binary
            binary = binary + (8 - len(binary)) * "0"

        return binary

    def saveAValue(self, params, paramName1, paramName2, line):
        txt = ""

        if params == None:
           params = {"param#1": [paramName1, None], "param#2": [paramName2, "variable"]}
           paramName1 = "param#1"
           paramName2 = "param#2"

           varTest = self.__loader.virtualMemory.getVariableByName(params[paramName1][0], self.__currentBank)

           if varTest == False:
               if params[paramName1][0] in self.__constants:
                  params[paramName1][1] = "constant"
               else:
                  params[paramName1][1] = "number"
           else:
               params[paramName1][1] = "variable"

        allTheSame, hasBCD = self.paramsHaveBCDandBinaryAtTheSameTime(params)
        #print(params)
        var2 = self.__loader.virtualMemory.getVariableByName(params[paramName2][0], self.__currentBank)
        if var2 == False:
            var2 = self.__loader.virtualMemory.getVariableByName(params[paramName2][0], "bank1")

        if var2 == False:
            self.addToErrorList(line["lineNum"],
                                self.prepareError("compilerErrorVarNotFound", params[paramName2][0],
                                                  "", "",
                                                  str(line["lineNum"] + self.__startLine)))

        if (hasBCD == False or allTheSame) and params[paramName1][1] in ["number", "stringConst"]:
           if hasBCD:
              try:
                  val = self.valOfNumber(params[paramName1][0])
              except:
                  val = int(self.getConstValue(params[paramName1][0]))

              val  = str(val)
              try:
                  num1 = bin(int(val[-2])).replace("0b", "")
                  num1 = (4 -len(num1)) * "0" + num1
              except:
                  num1 = "0000"

              num2 = bin(int(val[-1])).replace("0b", "")
              num2 = (4 - len(num2)) * "0" + num2

              val  = int("0b" + num1 + num2, 2)

           else:
              val  = params[paramName1][0]

           if var2.type == "byte":
              return "\tLDA\t#" + str(val) + "\n\tSTA\t" + params[paramName2][0] + "\n".replace("##", "#")

           txt = self.bitChanger(params[paramName2][0], val, None)
           return txt

        if self.__error == False:
            if params[paramName1][1] == "number":
               txt = "\tLDA\t#%" + self.bibBinBin(params[paramName1][0], var2, hasBCD, params, int(paramName1[-1])) \
                      + "\n\tSTA\t" + params[paramName2][0] + "\n"

            else:
                if hasBCD and allTheSame == True:
                   before = "\tSED\n"
                   after  = "\tCLD\n"
                else:
                   before = ""
                   after = ""

                var1 = self.__loader.virtualMemory.getVariableByName(params[paramName1][0], self.__currentBank)
                if var1 == False:
                    var1 = self.__loader.virtualMemory.getVariableByName(params[paramName1][0], "bank1")

                if var1 == False:
                    self.addToErrorList(line["lineNum"],
                                        self.prepareError("compilerErrorVarNotFound", params[paramName1][0],
                                                          "", "",
                                                          str(line["lineNum"] + self.__startLine)))

                if self.__error == False:
                   txt += "\tLDA\t" + params[paramName1][0] + "\n"
                   if (var1.bcd == True and allTheSame == False) or var1.type != "byte":
                       txt += self.convertAny2Any(var1, "TO", params, None)

                   if (var2.bcd == True and allTheSame == False) or var2.type != "byte":
                       txt += self.convertAny2Any(var2, "FROM", params, None)

                   txt += "\tSTA\t" + params[paramName2][0] + "\n"
                   txt = before + txt + after

        return txt

    def fuseTempsAndLogical(self, temp1, temp2, comprass, caseName):
        #print(temp1, temp2)

        comprassDict = self.__editorBigFrame.getComprassionDict()
        del comprassDict["all"]

        thatKey = None
        for key in comprassDict:
            if comprass in comprassDict[key]:
               thatKey = key

        allTheOnes = {
            "validNotEQ":           "\tLDA\t" + temp2 + "\n\tCMP\t" + temp1 + "\n\tBNE\t" + caseName + "\n",
            "validEQ":              "\tLDA\t" + temp2 + "\n\tCMP\t" + temp1 + "\n\tBEQ\t" + caseName + "\n",
            "validLargerThan":      "\tLDA\t" + temp2 + "\n\tCMP\t" + temp1 + "\n\tBCC\t" + caseName + "\n",
            "validSmallerThan":     "\tLDA\t" + temp1 + "\n\tCMP\t" + temp2 + "\n\tBCC\t" + caseName + "\n",
            "validLargerThanOrEQ":  "\tLDA\t" + temp1 + "\n\tCMP\t" + temp2 + "\n\tBCS\t" + caseName + "\n",
            "validSmallerThanOrEQ": "\tLDA\t" + temp2 + "\n\tCMP\t" + temp1 + "\n\tBCS\t" + caseName + "\n"
        }
        txt = allTheOnes[thatKey]

        #print("###", txt)

        return txt

    def isThereAnyLargerThan255(self, data):
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

    def valOfNumber(self, val):
        if val.startswith("#"): val = val[1:]

        if   val.startswith("%"):
             val = int(val.replace("%", "0b"), 2)
        elif val.startswith("$"):
             val = int(val.replace("$", "0x"), 16)
        else:
             val = int(val)

        return val

    def isIt(self, val, comp):
        val = self.valOfNumber(val)

        if val == comp: return True
        return False

    def createASMTextFromLine(self, line, command, params, changeText, annotation, linesFetched):
        template = self.__loader.io.loadCommandASM(command)

        for item in changeText:
            #print(item, item in template)
            template = template.replace(item, changeText[item])

        for num in range(1, 4):
            name    = "param#" + str(num)
            varName = "#VAR0" + str(num) + "#"

            if name not in params: continue
            if annotation != "" and params[name][1] == "number":
                template = template.replace(varName, params[name][0] + annotation)
            else:
                template = template.replace(varName, params[name][0])

        self.checkASMCode(template, line, linesFetched)
        if self.__error == False: line["compiled"] = template

    def prepareMulti(self, params):
        changeText = {}

        var1 = self.__loader.virtualMemory.getVariableByName2(params["param#1"][0])
        var2 = self.__loader.virtualMemory.getVariableByName2(params["param#2"][0])
        if "param#3" in params:
            var3 = self.__loader.virtualMemory.getVariableByName2(params["param#3"][0])
        else:
            var3 = None

        changeText["#MAGIC#"] = str(self.__magicNumber)
        changeText["#BANK#"]  = self.__currentBank
        changeText["#SECTION#"]  = self.__currentSection

        self.__magicNumber += 1

        self.__temps = self.collectUsedTemps()


        try:
            first = self.__temps[0]
            self.__temps.pop(0)

            second = self.__temps[0]
            self.__temps.pop(0)

        except:
            self.addToErrorList(self.__thisLine["lineNum"],
                                self.prepareError("compilerErrorStatementTemps", params["param#1"][0],
                                                  "", "",
                                                  str(self.__thisLine["lineNum"] + self.__startLine)))

        allTheSame, hasBCD = self.paramsHaveBCDandBinaryAtTheSameTime(params)

        if hasBCD == True and allTheSame == True:
           changeText["!!!BCDon!!!"] = "\tSED"
           changeText["!!!BCDoff!!!"] = "\tCLD"

        changeText["#VARTEMP#"] = params["param#1"][0]
        if self.__error == False:
            if var1 != False:

                if (var1.bcd == True and allTheSame == False) or var1.type != "byte":
                    changeText["!!!to8Bit1!!!"] = self.convertAny2Any(var1, "TO", params, self.__temps)

                    #if var1.type == "byte" or var1.bcd == True:
                    #    changeText["#VARTEMP#"] = params["param#1"][0]
                    #else:
                    changeText["#VARTEMP#"] = first
                    changeText["!!!staTEMP!!!"] = "\tSTA\t" + first + "\n"
                else:
                    changeText["#VARTEMP#"] = params["param#1"][0]

            else:
                if var1.bcd == True: self.paramToDec(params, 1)
                changeText["#VARTEMP#"] = params["param#1"][0]

            if var2 != False:
                if var2.type != "byte" or (var2.bcd == True and allTheSame == False):
                    changeText["!!!to8Bit2!!!"] = "\tLDA\t" + params["param#2"][0] + "\n" + \
                                                  self.convertAny2Any(var2, "TO", params, self.__temps) + "\tSTA\t" + second
            else:
                if hasBCD == True: self.paramToDec(params, 2)


            if var3 != False and var3 != None:
               if var3.type != "byte" or (var3.bcd == True and allTheSame == False):
                  changeText["!!!from8bit!!!"] = self.convertAny2Any(var3, "FROM", params, self.__temps)

            else:
               if hasBCD == True and var3 != None: self.paramToDec(params, 3)

        return changeText

    def preparePow(self, params, subLine, line):
        var1NotByte = False

        template = self.__loader.io.loadCommandASM("pow")

        self.__temps = self.collectUsedTemps()
        try:
            thisOne = self.__temps[0]
            self.__temps.pop(0)
            otherOne = self.__temps[0]
            self.__temps.pop(0)

        except:
            self.addToErrorList(line["lineNum"],
                                self.prepareError("compilerErrorStatementTemps", statement,
                                                  "", "", str(line["lineNum"] + self.__startLine)))

        allTheSame, hasBCD = self.paramsHaveBCDandBinaryAtTheSameTime(params)

        if hasBCD and allTheSame == True:
            template = template.replace("!!!BCDon!!!", "\tSED")
            template = template.replace("!!!BCDoff!!!", "\tCLD")

        if params["param#1"][1] == "variable":
            var1 = self.__loader.virtualMemory.getVariableByName2(subLine["param#1"][0])
            if var1 == False:
                self.addToErrorList(line["lineNum"],
                                    self.prepareError("compilerErrorVarNotFound", params["param#1"][0],
                                                      "", "",
                                                      str(line["lineNum"] + self.__startLine)))
            if var1.type != "byte": var1NotByte = True
        else:
            var1 = False
            if hasBCD: self.paramToDec(params, 1)

        if params["param#2"][1] == "variable":
            var2 = self.__loader.virtualMemory.getVariableByName2(subLine["param#2"][0])
            if var2 == False:
                self.addToErrorList(line["lineNum"], self.prepareError("compilerErrorVarNotFound", params["param#2"][0],
                                                                       "", "",
                                                                       str(line["lineNum"] + self.__startLine)))
        else:
            var2 = False
            if hasBCD: self.paramToDec(params, 2)

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

            replacer = ""
            if var2.type != "byte" or (var2.bcd == True and allTheSame == False):
                replacer = self.convertAny2Any(var2, "TO", params, self.__temps)

            template = template.replace("!!!DECR!!!", "\tDEX\n\tCMP\t#0\n\tBEQ\t#BANK#_Pow_#MAGIC#_End\n").replace(
                "!!!INCR!!!", "\tINX\n").replace("!!!to8Bit1!!!", replacer)

        if "param#3" in params.keys() or var1NotByte:
            if "param#3" in params.keys():
                var3 = self.__loader.virtualMemory.getVariableByName2(subLine["param#3"][0])
                if var3 == False:
                    self.addToErrorList(line["lineNum"],
                                        self.prepareError("compilerErrorVarNotFound", params["param#3"][0],
                                                          "", "",
                                                          str(line["lineNum"] + self.__startLine)))
            else:
                params["param#3"] = params["param#1"]
                var3              = var1

            if self.__error == False:

               subLine["param#1"][0] = thisOne
               subLine["param#2"][0] = otherOne
               subLine["param#3"][0] = thisOne
               #print(subLine)

               subLine["fullLine"] = subLine["fullLine"] = "*(" + subLine["param#1"][0] + ", " + subLine["param#2"][0] + ")"
               self.processLine(subLine, self.__useThese[1])

               txt1 = "\tLDA\t" + params["param#1"][0] + "\n"
               if var1 != False:
                   if var1.type != "byte" or (var1.bcd and allTheSame == False):
                      txt1 += self.convertAny2Any(var1, "TO", params, None)

               txt1 += "\tSTA\t" + thisOne + "\n"

               txt3 = "\tLDA\t" + thisOne + "\n"
               if var3 != False:
                  if var3.type != "byte" or (var3.bcd and allTheSame == False):
                     txt3 += self.convertAny2Any(var3, "FROM", params, None)

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


    def paramsHaveBCDandBinaryAtTheSameTime(self, params):
        binary = False
        bcd    = False

        for name in params:
            var = self.__loader.virtualMemory.getVariableByName2(params[name][0])
            if var != False:
               if var.bcd == True:
                  bcd    = True
               else:
                  binary = True

               if bcd == True and binary == True: return False, True

        return True, bcd

    def prepareAdd(self, params, ignoreBCDConvert):
        changeText = {}

        var1 = self.__loader.virtualMemory.getVariableByName2(params["param#1"][0])
        var2 = self.__loader.virtualMemory.getVariableByName2(params["param#2"][0])
        if "param#3" in params:
            var3 = self.__loader.virtualMemory.getVariableByName2(params["param#3"][0])
        else:
            var3 = None

        self.__temps = self.collectUsedTemps()

        try:
            first = self.__temps[0]
            self.__temps.pop(0)
        except:
            self.addToErrorList(self.__thisLine["lineNum"],
                                self.prepareError("compilerErrorStatementTemps", params["param#1"][0],
                                                  "", "",
                                                  str(self.__thisLine["lineNum"] + self.__startLine)))

        allTheSame, hasBCD = self.paramsHaveBCDandBinaryAtTheSameTime(params)

        if hasBCD and allTheSame == True:
           changeText["!!!BCDon!!!"] = "\tSED"
           changeText["!!!BCDoff!!!"] = "\tCLD"

        if self.__error == False:
            if var1 != False:
               if var1.type != "byte" or (var1.bcd == True and allTheSame == False):
                  changeText["!!!to8Bit1!!!"] = self.convertAny2Any(var1, "TO", params, self.__temps)
            else:
                if hasBCD == True and ignoreBCDConvert == False: self.paramToDec(params, 1)

            if var2 != False:
               if var2.type != "byte" or (var2.bcd and allTheSame == False):
                  changeText["#VAR02#"] = first
                  changeText["!!!to8Bit2!!!"] = "\tLDA\t" + params["param#2"][0] + "\n" + \
                                                self.convertAny2Any(var2, "TO", params, self.__temps) + "\tSTA\t" + first
            else:
                if hasBCD == True and ignoreBCDConvert == False: self.paramToDec(params, 2)

            if var3 != False and var3 != None:
               if var3.type != "byte" or (var3.bcd == True and allTheSame == False):
                  changeText["!!!from8bit!!!"] = self.convertAny2Any(var3, "FROM", params, None)
            else:
               if hasBCD == True and var3 != None and ignoreBCDConvert == False: self.paramToDec(params, 3)

        return changeText

    def paramToDec(self, params, num):
        val = str(self.valOfNumber(params["param#" + str(num)][0]))
        if len(val) == 1:
            val = "#$0" + val
        else:
            if len(val) > 2:
                self.addToErrorList(self.__useThese[0], self.prepareError("compilerErrorBCDOverFlow", "",
                                     "", params["param#" + str(num)][0],
                                    self.__useThese[0]))

            val = "#$"  + val[-2:]

        params["param#" + str(num)][0] = val

    def collectLabelsFromRoutines(self, labels):
        sources = [self.toRoutines, self.bank1Data, {"dummy":  "\n".join(self.__text)}]
        #sources = [self.toRoutines, self.bank1Data]

        for source in sources:
            for key in source.keys():
                b = self.__currentBank
                if source == self.bank1Data: b = "bank1"
                lines = source[key].replace("\r", "").split("\n")

                for line in lines:
                    if line == "" or line.isspace() or line[0] in ["\t", " "]:
                       continue

                    if line.replace("\t", " ")[0] != " " and "!!!" not in line:
                        if len(line) > 0:
                            if line[0] not in ("*", "#", "!") and "#BANK#" not in line:
                               labels.append(line)
                               labels.append(line.replace("#BANK#", b).replace("#SECTION#", key))

        subroutines = self.__editorBigFrame.collectNamesByCommandFromSections("subroutine", self.__currentBank)
        bank1Routines = self.__editorBigFrame.collectNamesByCommandFromSections("subroutine", "bank1")
        self.removeTheOnesFromTheFirstThatIsInTheSecond(subroutines, bank1Routines)

        sources = [subroutines, bank1Routines]

        for source in sources:
            for subName in subroutines:
                if source == bank1Routines:
                   b = "bank1"
                else:
                   b = self.__currentBank

                labels.append(
                    b + "_SubRoutine_" + subName
                )

        self.__labels = labels

    def removeTheOnesFromTheFirstThatIsInTheSecond(self, list1, list2):
        list1 = [item for item in list1 if item not in list2]

    def changeMagicAndOthersInLine(self, line):
        for pNum in range(1, 4):
            paramName = "param#" + str(pNum)
            if line[paramName][0] not in self.__noneList:
               line[paramName][0] = line[paramName][0].replace("#BANK#"   , self.__currentBank)   \
                                                      .replace("#SECTION#", self.__currentSection)\
                                                      .replace("#MAGIC#"  , str(self.__magicNumber))

    def checkASMCode(self, template, lineStructure, linesFetched):
        #if "add" in template: raise ValueError

        template = template.replace("#BANK#", self.__currentBank).replace("#SECTION#", self.__currentSection)
        lines = template.split("\n")
#        for line in lines:
 #           if "BNE" in line:
  #              print("faszom")
   #             raise ValueError

        labels = []
        self.collectLabelsFromRoutines(labels)

        self.__magicNumber += 1

        if self.isCommandInLineThat(lineStructure, "asm"):
           self.changeMagicAndOthersInLine(lineStructure)
           """
           if lineStructure["param#1"] not in self.__noneList:
              if lineStructure["param#1"][0][1:-1] not in [" ", "\t", "\n"] and " = " not in lineStructure["param#1"][0]:
                 print(lineStructure["param#1"][0][1:-1])
                 return
           """

        for line in linesFetched:
            for key in ["labelsBefore", "labelsAfter"]:
                if key in line:
                   for label in line[key]:
                       base = label.replace("\r", "")

                       labels.append(base)
                       labels.append(base.replace("#BANK#", self.__currentBank).replace("#SECTION#", self.__currentSection))

            if line["compiled"] != "":
               txt = line["compiled"]
            else:
               txt = template

            subLines = txt.replace("\r", "").split("\n")
            for subLine in subLines:
                if subLine.replace("\t", " ").startswith(" ") == False and "!!!" not in subLine:
                   if len(subLine) > 0:
                      if subLine[0] not in ("*", "#", "!") or "#BANK#" in subLine:
                         labels.append(subLine)
                         labels.append(subLine.replace("#BANK#", self.__currentBank).replace("#SECTION#", self.__currentSection))

            if self.isCommandInLineThat(line, "asm"):
               if line["param#1"][0] not in self.__noneList:
                  lineTxt = line["param#1"][0][1:-1]
                  if lineTxt not in self.__noneList:
                     if lineTxt[0] not in [" ", "\t", "\n"] and " = " not in lineTxt:
                        skip = False
                        if len(lineTxt) == 3:
                            for regNum in self.__opcodes:
                                lineSettings = self.__opcodes[regNum]
                                if lineSettings["opcode"].lower() == lineTxt.lower():
                                   skip = True
                                   break

                        if skip == False:
                           #print(lineTxt)
                           for charNum in range(0, len(lineTxt)):
                               if lineTxt[charNum] in [" ", "\t", "\n"]:
                                  labels.append(lineTxt[:charNum])
                                  labels.append(lineTxt[:charNum].replace("#BANK#", self.__currentBank).replace("#SECTION#", self.__currentSection))

                                  break
                               elif charNum == len(lineTxt) - 1:
                                  labels.append(lineTxt)
                                  labels.append(lineTxt.replace("#BANK#", self.__currentBank).replace("#SECTION#", self.__currentSection).replace("#MAGIC#", str(self.__magicNumber)))

                                  break

                     self.changeMagicAndOthersInLine(line)
                     #print(labels, template)

        for l in labels:
            if l not in self.__alreadyCollectedLabels:
               self.__alreadyCollectedLabels.append(l)

        labels = self.__alreadyCollectedLabels

        #if self.__testFirst:
           #self.__testFirst = False

           #for l in labels: print(l)

           #for line in linesFetched:
           #    if self.isCommandInLineThat(line, "asm"):
           #       print(line["param#1"], line["param#2"])

        for line in lines:
            full = line

            if line.replace("\t", " ").startswith(" ") == False: continue
            if line[0] in ["*", "#", "!"]: continue

            delimiterPoz = self.__editorBigFrame.getFirstValidDelimiterPoz(line)
            line = line[:delimiterPoz]
            #'$79': {'opcode': 'ADC', 'format': 'aaaa,y', 'bytes': 3},
            line = line.replace("\r", "").replace("\t", " ").split(" ")

            value   = ""

            newLine = []
            for item in line:
                if item != "": newLine.append(item)
            line    = newLine
            if line == []: continue

            if line[0].upper() in self.__branchers or line[0].upper() in self.__jumpers:
               if self.isCommandInLineThat(lineStructure, "asm"):
                   for replacer in self.__replacers.keys():
                       replaceIt = self.__replacers[replacer]

                       if replacer in line[1]: line[1] = line[1].replace(replacer, replaceIt)
                       for key in lineStructure.keys():
                           if type(lineStructure[key]) == list and lineStructure[key] != []:
                               if lineStructure[key][0] not in self.__noneList:
                                  #print(key, lineStructure[key][0])
                                  if type(lineStructure[key][0]) == str:
                                     lineStructure[key][0] = lineStructure[key][0].replace(replacer, replaceIt)
                                     self.__changeThese[replacer] = replaceIt

               if line[1] in labels                     or\
                  line[1] in self.__fullTextLabels      or\
                  line[1][0] == "*"                     or\
                  line[1] in self.__labelsOfMainKenrel:
                  continue
               """ 
               else:
                  if self.__testFirst:
                     for l in labels:
                         print(l)
                     self.__testFirst = False
                  print(">>", line[1])
               """

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

            if command.upper() == "BYTE":
               try:
                   t = self.valOfNumber(line[1])
                   continue
               except:
                   self.prepareErrorASM("compilerErrorASMByteInvalidParameter",
                                        "", line[1],
                                        lineStructure["lineNum"])
                   continue

            foundCommand = False

            if line[0] in labels                    or\
               line[0] in self.__fullTextLabels     or\
               line[0] in self.__labelsOfMainKenrel : continue

            #print(line,
            #      line in labels                     or\
            #      line in self.__fullTextLabels      or\
            #      line in self.__labelsOfMainKenrel  or line in self.__alreadyCollectedLabels)

            for item in self.__opcodes:
                lineSettings = self.__opcodes[item]

                if lineSettings["opcode"].upper() == command.upper():
                   if value in self.__noneList:
                       if lineSettings["bytes"] == 1:
                          foundCommand = True
                          break
                       else: continue

                   else:
                       if lineSettings["format"] == None: continue

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
                   #print("1", value)

                   if self.checkIfASMhasrightOperand(lineSettings, value) == False: continue

                   errorVal = 2

                   beforeComma = value.split(",")[0]

                   operandTyp  = self.getTypeOfOperand(beforeComma)
                   operandSize = self.sizeOfNumber(beforeComma, operandTyp)

                   numberValue = ""
                   numeric = beforeComma

                   if operandTyp in ("variable", "register"):
                      numeric = self.getAddress(self.removeAritmeticPart(beforeComma))

                   if beforeComma.startswith("#>") or beforeComma.startswith("#<"):
                       if operandTyp != "label":
                           if beforeComma[1] == ">":
                               beforeComma = self.__editorBigFrame.convertStringNumToNumber(numeric[1:3])
                           else:
                               beforeComma = self.__editorBigFrame.convertStringNumToNumber(numeric[3:5])

                   else:
                       #numeric     = self.removeAritmeticPart(beforeComma)
                       numberValue = self.__editorBigFrame.convertStringNumToNumber(numeric.replace("#", ""))

                   hexa    = ""
                   mode    = ""
                   special = ""
                   #print("2", beforeComma, operandTyp)

                   try:
                       opcodeDoes = self.opcodesIOsMoreOtherThanRead[command.upper()]
                   except:
                       opcodeDoes = "read"

                   if operandTyp == "variable" and "#" in beforeComma:
                      operandTyp  = "constant"
                      beforeComma =  numeric

                   if operandTyp == "variable":
                      beforeComma = self.removeAritmeticPart(beforeComma)

                   if operandTyp in ("address", "register"):

                      hexa = hex(numberValue).replace("0x", "")
                      if len(hexa) % 2 != 0: hexa = "0" + hexa
                      hexa = "$" + hexa.upper()

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
                          if int("0x" + hexa[1:], 16) > 29:
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

                   elif operandTyp in ("constant", "label"):
                        mode = "read"

                   if mode == "both" and (opcodeDoes == "read" or opcodeDoes == "write") and beforeComma not in self.__exceptions:
                      mode = opcodeDoes

                   if opcodeDoes != mode and beforeComma not in self.__exceptions:
                      if special == "":
                         #print(beforeComma)
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
               if self.__testFirst:
                  self.__testFirst = False
                  #print(labels, line in labels, type(line))

               self.addToErrorList(lineStructure["lineNum"], self.prepareErrorASM("compilerErrorASMOpCode",
                                                     command, value, lineStructure["lineNum"]))



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
        #print(value)
        labels = []
        self.collectLabelsFromRoutines(labels)

        for l in labels:
            if l not in self.__alreadyCollectedLabels:
               self.__alreadyCollectedLabels.append(l)

        labels = self.__alreadyCollectedLabels

        if lineSettings["format"].upper() == "#AA" and value[0:2] in ("#<", "#>"):
           if value[2:] in labels: return True

        if lineSettings["format"][0] == "#"    and\
           value.split(",")[0] not in labels   and\
           value[0] != "#":
           return False

        if lineSettings["format"][0] != "#"    and\
           value.split(",")[0] not in labels   and\
           value[0] == "#":
           return False

        beforeCommaValue    = value.split(",")[0]
        try:
            afterCommaValue = value.split(",")[1]
        except:
            afterCommaValue = ""

        beforeCommaValue     = self.removeAritmeticPart(beforeCommaValue)

        beforeCommaFormat    = lineSettings["format"].split(",")[0]
        try:
            afterCommaFormat = lineSettings["format"].split(",")[1]
        except:
            afterCommaFormat = ""

        #if value == "ScrollDirection":
        #print("1")
        if afterCommaFormat != afterCommaValue: return False
        beforeCommaFormat = beforeCommaFormat.upper()

        #print("2")
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

        #print("3")
        if "#" in beforeCommaValue and beforeCommaValue not in labels:
           allA = "#AA"
        else:
           allA = re.sub(r'[0-9a-fA-F]', "A", beforeCommaValue).replace("$", "")

        #print(value, beforeCommaFormat, allA)
        if beforeCommaFormat != allA: return False

        numOfBytesFormat = beforeCommaFormat.count("A") // 2
        if value.startswith("#"): numOfBytesFormat = 1

        #print(value, beforeCommaValue)
        #print(self.sizeOfNumber(value, ""), numOfBytesFormat)
        return self.sizeOfNumber(value, "") == numOfBytesFormat

    def getVarAddress(self, var):
        addr = self.__virtualMemory.getAddressOnVariableIsStored(var, "bank1")
        if addr == False:
           addr = self.__virtualMemory.getAddressOnVariableIsStored(var, self.__currentBank)
        return addr

    def sizeOfNumber(self, value, typ):
        value = self.removeAritmeticPart(value)
        value = value.split(",")[0]

        makeItHalf = 1

        if typ == "":
           typ =  self.getTypeOfOperand(value)

        if typ == "label":
           if ">" in value or "<" in value:
              return 2
           else:
              return 4

        if typ in ["variable", "register"]:

           value = self.getAddress(value)
           if value == False: return 0

        else:
            if value.startswith("#"):
               return 1

        #print(typ)
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

    def removeAritmeticPart(self, val):
        for aritmetic in ["+", "-"]:
            if aritmetic in val:
               parts = val.replace(" ", "").split(aritmetic)
               try:
                   t = int(parts[1])
                   val = parts[0]
               except:
                   pass

        return val

    def getTypeOfOperand(self, value):
        for key in self.numberRegexes:
            if len(re.findall(self.numberRegexes[key], value.replace("#", ""))) > 0:
               if "#" in value: return "constant"
               else:            return "address"

        value = self.removeAritmeticPart(value)

        if value.startswith("#"):  value = value[1:]
        if value[0] in [">", "<"]: value = value[1:]

        for key in self.__variablesOfBank:
            if value in self.__variablesOfBank[key]:
               return "variable"
        for key in self.__registers:
            if value.upper() in self.__registers[key]:
               return "register"

        if self.__labels == []:
           self.collectLabelsFromRoutines(self.__labels)

        for label in self.__labels:
            if value == label:
               return "label"

        return False

    def getParamsWithTypesAndCheckSyntax(self, line):
        params = {}

        #print(line)
        command = None
        for commandName in self.__loader.syntaxList.keys():
            if self.isCommandInLineThat(line, commandName):
               command = self.__loader.syntaxList[commandName]
               break

        if command == None:
           command = self.__objectMaster.createFakeCommandOnObjectProcess(line["command"][0])

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

               dummy, ioMethod = self.__editorBigFrame.returnParamsOfObjects(commandName)

               if command.flexSave == True and num == 1 and \
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
                   #print(ioMethod)
                   foundIt, paramTypeAndDimension = self.__editorBigFrame.checkIfParamIsOK(param, curParam,
                                                                                           ioMethod, None,
                                                                                           "dummy", mustHave, "param#"+str(num),
                                                                                           line, self.__text)

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
                          "array"      : "Array",
                          "register"   : "Register"
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
        #if listOfErrors != []: print(self.__text)

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
                      "sectionNotAllowed": {"#SECTIONS#": ", ".join(command.sectionsAllowed)},
                      "levelNotAllowed": {"#LEVEL#": str(command.levelAllowed)},
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
        #print(text)
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
        #print(text)
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
        #print(">>", line, command)
        if line["command"][0] == command or line["command"][0] in self.__loader.syntaxList[command].alias:
           return True
        return False

    def convertStatementToSmallerCodes(self, command, statement, line):
        #side1            = ""
        #side2            = ""
        statementData    = []
        #statementFetched = []
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

                           txt += self.convertToCommands(statement[0], line, temp1)
                           txt += self.convertToCommands(statement[1], line, temp2)

                           commands = txt
                           temps = [temp1, temp2]

        if self.__error == False:
           return commands, temps
        else:
           #print(self.errorList)
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

        params = self.getParamsWithTypesAndCheckSyntax(line)

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
            returnBack = " set(" + saveHere + ", " + finals[0] + ")\n"

            """
            isItNum = False
            try:
                teszt   = int(finals[0].replace("#", ""))
                isItNum = True
            except:
                pass

            #extra  = ""
            before = ""
            after  = ""

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
                else:
                    allTheSame, hasBCD = self.paramsHaveBCDandBinaryAtTheSameTime(params)

                    if hasBCD and allTheSame == True:
                       before = "asm(\"\tSED\n\")"
                       after  = "asm(\"\tCLD\n\")"

                    #if var.type != "byte" and (var.bcd and allTheSame == False):
                    #   extraLines = self.convertAny2Any(var, "TO", params, None)
                    #   for line in extraLines:
                    #       if line != "":
                    #          extra += "asm(\"" + line + "\")\n"

            if self.__error == False:
                returnBack += before                                +\
                              "asm(\"\tLDA\t" + finals[0] + "\")\n" +\
                              "asm(\"\tSTA\t" + saveHere  + "\")\n" +\
                              after
            """
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