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
               lineStruct["commentsBefore"] = "*\t" + line[:self.__editorBigFrame.getFirstValidDelimiterPoz(line)]

            linesFeteched.append(lineStruct)

        if   mode == "forEditor":
             self.compileBuild(linesFeteched)
        elif mode == "forBuild":
             self.compileBuild(linesFeteched)

    def compileBuild(self, linesFeteched):

        for line in linesFeteched:
            if self.isCommandInLineThat(line, "asm"):
               datas = []
               for num in range(1, 3):
                   if line["param#" + str(num)][0] not in self.__noneList:
                      datas.append(line["param#" + str(num)][0][1:-1])

               line["compiled"] = "\t"+"\t".join(datas)
            elif self.isCommandInLineThat(line, "add"):
                params = self.getParamsWithTypes(line)

        textToReturn = ""
        for line in linesFeteched:
            for word in ["commentsBefore", "labelsBefore", "compiled", "labelsAfter"]:
                if line[word] not in self.__noneList:
                   if type(line[word]) == list:
                      line[word] = "\n".join(line[word])
                   textToReturn += line[word] + "\n"

            if line["comment"][0] not in self.__noneList:
               textToReturn = textToReturn[:-1] + "\t; " +  line["comment"][0] + "\n"

        self.result = textToReturn

    def getParamsWithTypes(self, line):
        params = []
        for num in range(1, 4):
            curParam = line["param#"+str(num)][0]
            if curParam not in self.__noneList:
               curParam = self.formatParam(curParam, line["command"][0], line["lineNum"])
               if curParam == None:
                  continue

    def formatParam(self, paramText, command, lineNum):
        import re

        returnMe = {"param": paramText, "type": "variable"}

        numberRegexes = {"dec": r'^\d{1,3}$',
                         "bin": r'^[b|%][0-1]{1,8}$',
                         "hex": r'^[$|z|h][0-9a-f]{1,2}$'
                         }
        for key in numberRegexes:
            if len(re.findall(numberRegexes[key], paramText)) > 0:
               returnMe["param"] = "#" + returnMe["param"]
               returnMe["type"]  = "number"
               return returnMe

        if paramText in self.__constants.keys():
           for key in numberRegexes:
               if len(re.findall(numberRegexes[key], self.__constants[paramText])) > 0:
                  returnMe["param"] = "#" + self.__constants[paramText]
                  returnMe["type"]  = "number"
                  return returnMe


           self.addToErrorList(self.prepareError("compileErrorConstant",
                               self.__constants[paramText], paramText,
                               str(lineNum + self.__startLine))
                               )

           return(None)

        vars        = self.__all
        commandData = self.__loader.syntaxList[command]

        if command.does == "write":
           if paramText == "item":
                pass
           else:
                vars = self.__writable

    def addToErrorList(self, text):
        if self.__currentBank not in self.errorList.keys():
           self.errorList[self.__currentBank] = {}

        if self.__currentSection not in self.errorList[self.__currentBank].keys():
           self.errorList[self.__currentBank][self.__currentSection] = []

        self.errorList[self.__currentBank][self.__currentSection].append(text)

    def prepareError(self, text, val, var, lineNum):
        return self.__dictionaries.getWordFromCurrentLanguage(text)\
                    .replace("#VAL#", val, "#VAR#", var,
                             "#BANK", self.__currentBank, "#SECTION#", self.__currentSection,
                             "#LINENUM#", str(lineNum)
                             )


    def isCommandInLineThat(self, line, command):
        if line["command"][0] == command or command in self.__loader.syntaxList[command].alias:
           return True
        return False

