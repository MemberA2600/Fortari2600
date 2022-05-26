import re
from Assembler import Assembler

class Block:

    def __init__(self):
        self.bytes = 0
        self.segments = []

    def addSegment(self, segment):
        if segment.bytes + self.bytes > 255:
           return False
        self.segments.append(segment)
        self.bytes+=segment.bytes
        return True

class Segment:

    def __init__(self, text):
        self.bytes = 0
        self.text  = text

        t = text.split("\n")
        for line in t:
            if "byte" in line.lower():
                self.bytes+=1

class Compiler:

    def __init__(self, loader, kernel, mode, data):

        if mode != "dummy":
            self.__loader = loader
            self.__kernel = kernel
            self.__mode = mode
            self.__data = data
            self.__executor = self.__loader.executor
            self.__openEmulator = False
            self.__io = self.__loader.io

            if self.__mode == "pfTest":
                self.pfTest()
            elif self.__mode == "spriteTest" or self.__mode == "tileSetTest":
                self.spriteTest()
            elif self.__mode == "kernelTest":
                self.kernelTest()
            elif self.__mode == 'music':
                self.generateMusicROM()
            elif self.__mode == 'getMusicBytes':
                self.getMusicBytesSizeOnly()
            elif self.__mode == 'test64px':
                self.test64PX()
            elif self.__mode == 'testWav':
                self.testWav()
            elif self.__mode == "getPFASM":
                self.getPFASM()
            elif self.__mode == "getSpriteASM":
                self.getSpriteASM()
            elif self.__mode == "getBigSpriteASM":
                self.getBigSpriteASM()
            elif self.__mode == "testBigSprite":
                self.testBigSprite()
            elif self.__mode == "menuASM":
                self.menuASM()
            elif self.__mode == "testMenu":
                self.testMenu()
            elif self.__mode == "testScreenElements":
                self.testScreenElements()

    def testScreenElements(self):
        self.__screenElements  = self.__data[0]
        self.__tv              = self.__data[1]
        self.__bank            = self.__data[2]

        self.__bankData = []
        # In this case, there is no top or bottom, all tested goes to top.
        self.__routines = {}
        self.__userData = {}

        self.__enterCode =  self.__io.loadTestElementPlain("enterTestCommon")
        self.__inits    = []

        testLine = self.__io.loadTestElementPlain("testLine")

        for item in self.__screenElements:
            item = item.split(" ")
            name = item[0]
            typ  = item[1]
            data = item[2:]

            fullName = self.__bank + "_" + name + "_" + typ
            if   typ == "ChangeFrameColor":
               self.__bankData.append(
                   self.generate_ChangeFrameColor(fullName, data)
               )
            elif typ == "EmptyLines":
                self.__bankData.append(
                    self.generate_EmptyLines(fullName, data)
                )
            elif typ == "Picture64px":
                fullName += "_" + data[0]
                those = self.generate_64px(fullName, data, data[0])
                self.__bankData.append(those[0])
                self.__userData[fullName] = those[1]
                self.__inits.append(those[2])
            elif typ == "Indicator":
                subtyp = item[2]
                fullName += "_" + subtyp
                data   = item[3:]
                if   subtyp == "FullBar":
                     those  = self.generate_FullBar(fullName, data, self.__bank)
                     self.__bankData.append(those[0])
                     self.__userData[fullName] = those[1]
                     self.__userData[self.__bank+"_Bar_Normal"] =\
                        self.__io.loadSubModule("BarPixels").replace("#BANK#", self.__bank)
                    #for item in those:
                    #    print(item)
                     self.__routines["FullBar"] = self.__io.loadSubModule("FullBar_Kernel").replace("#BANK#", self.__bank)

                elif subtyp == "HalfBarWithText":
                     those  = self.generate_HalfBarWithText(fullName, data, self.__bank)
                     self.__bankData.append(those[0])
                     self.__userData[fullName] = those[1]
                     self.__userData[self.__bank+"_Bar_Normal"] =\
                        self.__io.loadSubModule("BarPixels").replace("#BANK#", self.__bank)
                     self.__routines["HalfBarWithText"] = self.__io.loadSubModule("HalfBarWithText_Kernel").replace("#BANK#", self.__bank)
                     self.__userData[fullName + "_TextData"] = those[2]

        self.__bankData.insert(0, testLine)
        self.__bankData.append(testLine)

        self.__mainCode = self.__io.loadKernelElement(self.__kernel, "main_kernel")
        self.__mainCode = self.__mainCode.replace("!!!TV!!!", self.__tv)
        self.__mainCode = self.__mainCode.replace("!!!ENTER_BANK2!!!", self.__enterCode + "\n".join(self.__inits))
        self.__mainCode = self.__mainCode.replace("!!!SCREENTOP_BANK2!!!", "\n".join(self.__bankData))
        self.__mainCode = self.__mainCode.replace("!!!ROUTINES_BANK2!!!", "\n".join(self.__routines.values()))
        self.__mainCode = self.__mainCode.replace("!!!USER_DATA_BANK2!!!", self.__reAlignDataSection("\n".join(self.__userData.values())))

        self.__mainCode = re.sub(r"!!![a-zA-Z0-9_]+!!!", "", self.__mainCode)

        self.doSave("temp/")
        assembler = Assembler(self.__loader, "temp/", True, "NTSC", False)

    def generate_OnePicOneBar(self, name, data, bank):

        topLevelText           = "\n" + name + "\n"


        dataVarName            = data[0]
        dataVar                = self.__loader.virtualMemory.getVariableByName2(dataVarName)

        maxValue               = int(data[1])

        colorVarName           = data[2]
        colorVar               = self.__loader.virtualMemory.getVariableByName2(colorVarName)

        pattern                = self.generate_fadeOutPattern(2)
        patternIndex           = int(data[3])

        topLevelText +=        "\tLDA\t" + dataVarName + "\n"
        if dataVar.type        != "byte":
           topLevelText        += self.convertAnyTo8Bits(dataVar.bits)
        topLevelText        += "\tSTA\ttemp03\n"

        #topLevelText           +=  "\tLDA\t#" + str(32 // maxValue) + "\n\tSTA\ttemp04\n"

        topLevelText           += '\tLDA\t'
        if colorVar            == False:
           topLevelText        += "#" + colorVarName + "\n"
        else:
           topLevelText        += colorVarName + "\n"
           if colorVar.type    == "nibble":
              topLevelText     += self.moveVarToTheRight(colorVar.usedBits)
           topLevelText        += "\tAND\t#%11110000\n"

        topLevelText           += "\tSTA\ttemp05\n"

        topLevelText           += "\n\tLDA\t#"+data[1]+"\n\tCMP\ttemp03\n"       +\
                                  "\tBCS\t"+name+"_NO_STA\n\tSTA\ttemp03\n"      +\
                                  name+"_NO_STA\n"

        topLevelText            += "\tLDA\ttemp03\n"
        if   maxValue > 127:   topLevelText += "\tLSR\n" * 4
        elif maxValue > 63:    topLevelText += "\tLSR\n" * 3
        elif maxValue > 31:    topLevelText += "\tLSR\n" * 2
        elif maxValue > 15:    topLevelText += "\tLSR\n"
        elif maxValue > 7:     pass
        elif maxValue > 3:     topLevelText += "\tASL\n"
        elif maxValue > 1:     topLevelText += "\tASL\n" * 2
        else:                  topLevelText += "\tASL\n" * 3

        topLevelText            += "\tCMP\t#0\n\tBEQ\t" + name + "_NoAddOne\n\tCLC\n\tADC\t#1\n" + name + "_NoAddOne\n"
        topLevelText            += "\tSTA\ttemp03\n"

        xxx                     = self.generateBarColors(pattern[patternIndex], patternIndex, bank)
        patternData             = xxx[0]

        topLevelText           += "\tLDA\t#<" + xxx[1] +"\n\tSTA\ttemp06\n\tLDA\t#>" + xxx[1] +"\n\tSTA\ttemp07\n"
        # From here comes the special part
        # Start with temp10

        pictureName            = data[4].split("_(")[0]
        picType                = data[4].split("_(")[1][:-1]

        if picType == "Big":
            topLevelText           += "\tLDA\t#<" + pictureName + "_BigSprite_0" + "\n\tSTA\ttemp10\n"
            topLevelText           += "\tLDA\t#>" + pictureName + "_BigSprite_0" + "\n\tSTA\ttemp11\n"
            topLevelText           += "\tLDA\t#<" + pictureName + "_BigSprite_1" + "\n\tSTA\ttemp12\n"
            topLevelText           += "\tLDA\t#>" + pictureName + "_BigSprite_1" + "\n\tSTA\ttemp13\n"
            topLevelText           += "\tLDA\t#<" + pictureName + "_BigSpriteColor_0" + "\n\tSTA\ttemp14\n"
            topLevelText           += "\tLDA\t#>" + pictureName + "_BigSpriteColor_0" + "\n\tSTA\ttemp15\n"
            topLevelText           += "\tLDA\t#<" + pictureName + "_BigSpriteColor_1" + "\n\tSTA\ttemp16\n"
            topLevelText           += "\tLDA\t#>" + pictureName + "_BigSpriteColor_1" + "\n\tSTA\ttemp17\n"

        if data[5].startswith("%"):
           topLevelText += "\tLDA\t#" + data[5] + "\n\tSTA\ttemp18\n"
        else:
           topLevelText += "\tLDA\t"  + data[5] + "\n\tSTA\ttemp18\n"

        if picType == "Big":
            path = self.__loader.mainWindow.projectPath+"bigSprites/"+ pictureName +".asm"
        else:
            path = self.__loader.mainWindow.projectPath+"sprites/"+ pictureName +".asm"

        f = open(path, "r")
        picData = f.read().replace("##NAME##", pictureName)

        if picType == "Big":
            lines = picData.replace("\r","").split("\n")[0]
            for line in lines:
                if line.startswith("*") and "Mode=" in line:
                   #mode = line.split("Mode=")[1]
                   if "double" in line:
                       topLevelText += "\tLDA\ttemp04\n\tORA\t#%10000000\n\tSTA\ttemp04\n"

        # Jumpback!

        topLevelText           += "\tLDA\t#<" + name + "_Back" + "\n\tSTA\ttemp01\n" + \
                                  "\tLDA\t#>" + name + "_Back" + "\n\tSTA\ttemp02\n"
        topLevelText           += "\tJMP\t" + bank + "_OneBigPicOneBar_Kernel" + "\n"
        topLevelText           += name + "_Back" + "\n"

        return (topLevelText, patternData, picData)


    def generate_HalfBarWithText(self, name, data, bank):

        topLevelText           = "\n" + name + "\n"


        dataVarName            = data[0]
        dataVar                = self.__loader.virtualMemory.getVariableByName2(dataVarName)

        maxValue               = int(data[1])

        colorVarName           = data[2]
        colorVarName2          = data[4]
        print(data)

        colorVar               = self.__loader.virtualMemory.getVariableByName2(colorVarName)
        colorVar2              = self.__loader.virtualMemory.getVariableByName2(colorVarName2)

        pattern                = self.generate_fadeOutPattern(2)
        patternIndex           = int(data[3])

        topLevelText +=        "\tLDA\t" + dataVarName + "\n"
        if dataVar.type        != "byte":
           topLevelText        += self.convertAnyTo8Bits(dataVar.bits)
        topLevelText        += "\tSTA\ttemp03\n"


        #topLevelText           +=  "\tLDA\t#" + str(32 // maxValue) + "\n\tSTA\ttemp04\n"

        topLevelText           += '\tLDA\t'
        if colorVar            == False:
           topLevelText        += "#" + colorVarName + "\n\tSTA\ttemp04\n"

        else:
           topLevelText        += colorVarName + "\n"
           if colorVar.type    == "nibble":
              topLevelText     += self.moveVarToTheRight(colorVar.usedBits)
           topLevelText        += "\tAND\t#%11110000\n"
           topLevelText        += "\tSTA\ttemp04\n"

        topLevelText           += "\n\tLDA\t#"+data[1]+"\n\tCMP\ttemp03\n"       +\
                                  "\tBCS\t"+name+"_NO_STA\n\tSTA\ttemp03\n"      +\
                                  name+"_NO_STA\n"

        topLevelText            += "\tLDA\ttemp03\n"
        if   maxValue > 127:   topLevelText += "\tLSR\n" * 4
        elif maxValue > 63:    topLevelText += "\tLSR\n" * 3
        elif maxValue > 31:    topLevelText += "\tLSR\n" * 2
        elif maxValue > 15:    topLevelText += "\tLSR\n"
        elif maxValue > 7:     pass
        elif maxValue > 3:     topLevelText += "\tASL\n"
        elif maxValue > 1:     topLevelText += "\tASL\n" * 2
        else:                  topLevelText += "\tASL\n" * 3

        topLevelText            += "\tCMP\t#0\n\tBEQ\t" + name + "_NoAddOne\n\tCLC\n\tADC\t#1\n" + name + "_NoAddOne\n"
        topLevelText            += ("\tSTA\ttemp03\n" + self.__loader.io.loadSubModule("preSetHalfBar")
                                    .replace("#NAME#", name).replace("#BANK#", bank))

        xxx                     = self.generateBarColors(pattern[patternIndex], patternIndex, bank)
        patternData             = xxx[0]

        topLevelText           += "\tLDA\t#<" + xxx[1] +"\n\tSTA\ttemp06\n\tLDA\t#>" + xxx[1] +"\n\tSTA\ttemp07\n"
        topLevelText           += "\tLDA\t#<" + name + "_Back" + "\n\tSTA\ttemp01\n" + \
                                  "\tLDA\t#>" + name + "_Back" + "\n\tSTA\ttemp02\n"

        if colorVar2            == False:
           topLevelText        += "#" + colorVarName2 + "\n\tSTA\ttemp05\n"
        else:
           topLevelText        += colorVarName2 + "\n"
           if colorVar2.type    == "nibble":
              topLevelText     += self.moveVarToTheRight(colorVar2.usedBits)
           topLevelText        += "\tAND\t#%11110000\n"
           topLevelText        += "\tORA\t#%00000110\n"
           topLevelText        += "\tSTA\ttemp05\n"

        last = 6
        textData = "\n" + name + "_TextData\n" +\
                    self.generateAtariLetters(data[5], name, last)

        tempStart = 8
        for spriteCounter in range(0,last):
            topLevelText += "\tLDA\t#<" + name + "_TextData_Sprite_" + str(spriteCounter)+ "\n"
            t = str(tempStart + (2 * spriteCounter))
            if len(t) < 2: t = "0" + t
            topLevelText += "\tSTA\ttemp" + t + "\n"

            topLevelText += "\tLDA\t#>" + name + "_TextData_Sprite_" + str(spriteCounter)+ "\n"
            t = str(tempStart + (2 * spriteCounter) + 1)
            if len(t) < 2: t = "0" + t
            topLevelText += "\tSTA\ttemp" + t + "\n"

        topLevelText           += "\tJMP\t" + bank + "_HalfBarWithText_Kernel" + "\n"
        topLevelText           += name + "_Back" + "\n"

        return (topLevelText, patternData, textData)

    def generateAtariLetters(self, text, name, maX):
        lines = ["", "", "", "", "", "", "", ""]
        for letter in text:
            letterData = self.__loader.fontManager.getAtariChar(letter)
            for lineNum in range(0, len(letterData)):
                lines[lineNum] += letterData[lineNum]
            for lineNum in range(0, 8):
                lines[lineNum] += "0"
        for lineNum in range(0, 8):
            lines[lineNum] = lines[lineNum][:-1]

        spriteCounter = 0
        spriteData    = ""
        for indexStartX in range(0, len(lines[0]), 8):
            spriteData += name + "_TextData_Sprite_" + str(spriteCounter)+ "\n"

            for indexY in range(7, -1, -1):
                tempLine = "\tBYTE\t#%"
                for indexX in range(indexStartX, indexStartX + 8):
                    try:
                        tempLine += lines[indexY][indexX]
                    except:
                        tempLine += "0"

                tempLine += "\n"
                spriteData += tempLine
            spriteData    += "\n"
            spriteCounter += 1

        for num in range(spriteCounter, maX):
            spriteData += name + "_TextData_Sprite_" + str(num)+ "\n" +\
                          "\tBYTE\t#%00000000\n" + \
                          "\tBYTE\t#%00000000\n" + \
                          "\tBYTE\t#%00000000\n" + \
                          "\tBYTE\t#%00000000\n" + \
                          "\tBYTE\t#%00000000\n" + \
                          "\tBYTE\t#%00000000\n" + \
                          "\tBYTE\t#%00000000\n" + \
                          "\tBYTE\t#%00000000\n"
        return(spriteData)

    def generate_FullBar(self, name, data, bank):

        topLevelText           = "\n" + name + "\n"


        dataVarName            = data[0]
        dataVar                = self.__loader.virtualMemory.getVariableByName2(dataVarName)

        maxValue               = int(data[1])

        colorVarName           = data[2]
        colorVar               = self.__loader.virtualMemory.getVariableByName2(colorVarName)

        pattern                = self.generate_fadeOutPattern(2)
        patternIndex           = int(data[3])

        topLevelText +=        "\tLDA\t" + dataVarName + "\n"
        if dataVar.type        != "byte":
           topLevelText        += self.convertAnyTo8Bits(dataVar.bits)
        topLevelText        += "\tSTA\ttemp03\n"

        #topLevelText           +=  "\tLDA\t#" + str(32 // maxValue) + "\n\tSTA\ttemp04\n"

        topLevelText           += '\tLDA\t'
        if colorVar            == False:
           colors              =  colorVarName.split("|")
           topLevelText        += "#" + colors[0] + "\n\tSTA\ttemp05\n"
           topLevelText        += "\tLDA\t#" + colors[1] + "\n\tSTA\ttemp12\n"
           topLevelText        += "\tLDA\t#" + colors[2] + "\n\tSTA\ttemp13\n"

        else:
           topLevelText        += colorVarName + "\n"
           if colorVar.type    == "nibble":
              topLevelText     += self.moveVarToTheRight(colorVar.usedBits)
           topLevelText        += "\tAND\t#%11110000\n"

           topLevelText        += "\tSTA\ttemp05\n" +\
                                  "\tSTA\ttemp12\n" +\
                                  "\tSTA\ttemp13\n"

        topLevelText           += "\n\tLDA\t#"+data[1]+"\n\tCMP\ttemp03\n"       +\
                                  "\tBCS\t"+name+"_NO_STA\n\tSTA\ttemp03\n"      +\
                                  name+"_NO_STA\n"

        topLevelText            += "\tLDA\ttemp03\n"
        if   maxValue > 127:   topLevelText += "\tLSR\n" * 3
        elif maxValue > 63:    topLevelText += "\tLSR\n" * 2
        elif maxValue > 31:    topLevelText += "\tLSR\n"
        elif maxValue > 15:    pass
        elif maxValue > 7:     topLevelText += "\tASL\n"
        elif maxValue > 3:     topLevelText += "\tASL\n" * 2
        elif maxValue > 1:     topLevelText += "\tASL\n" * 3
        else:                  topLevelText += "\tASL\n" * 4

        topLevelText            += "\tCMP\t#0\n\tBEQ\t" + name + "_NoAddOne\n\tCLC\n\tADC\t#1\n" + name + "_NoAddOne\n"
        topLevelText            += "\tSTA\ttemp03\n"

        xxx                     = self.generateBarColors(pattern[patternIndex], patternIndex, bank)
        patternData             = xxx[0]

        topLevelText           += "\tLDA\t#<" + xxx[1] +"\n\tSTA\ttemp06\n\tLDA\t#>" + xxx[1] +"\n\tSTA\ttemp07\n"
        topLevelText           += "\tLDA\t#<" + name + "_Back" + "\n\tSTA\ttemp01\n" + \
                                  "\tLDA\t#>" + name + "_Back" + "\n\tSTA\ttemp02\n"
        topLevelText           += "\tJMP\t" + bank + "_FullBar_Kernel" + "\n"
        topLevelText           += name + "_Back" + "\n"

        return (topLevelText, patternData)

    def generateBarColors(self, pattern, index, bank):

        name = bank+"_Gradient_"+ str(len(pattern)) + "_" + str(index)
        text = name + "\n"

        for item in pattern:
            item = hex(item).replace("0x", "")
            while len(item) < 2:
                item = "0" + item

            text += "\tBYTE\t#$"+item+"\n"
        return(text, name)

    def moveVarToTheRight(self, bits):
        numForASL = 7 - max(bits)
        return numForASL * "\tASL\n"


    def getPixelStep(self, numOfPix, maxValue):
        return 256 // 32 // (256)

    def getClosestPowerOf2Minus1(self, v):
        from math import pow

        c = bin(v)[2:]
        goodOnes = []

        for num in range(1, 9):
            b = bin(int(pow(2, num))-1)[2:]
            while len(b) < 8: b = "0" + b
            goodOnes.append(b)

        while True:
            c = bin(v)[2:]
            while len(c) < 8: c = "0" + c
            if c in goodOnes: break
            v = v-1

        return(int("0b"+c, 2))

    def generate_fadeOutPattern(self, step):
        return  {
            1: [step * 4, step * 4, step * 3, step * 3, step * 2, step * 2, step * 1, step * 1],
            2: [step * 1, step * 1, step * 2, step * 2, step * 3, step * 3, step * 4, step * 4],
            3: [step * 1, step * 2, step * 3, step * 4, step * 4, step * 3, step * 2, step * 1],
            4: [step * 4, step * 3, step * 2, step * 1, step * 1, step * 2, step * 3, step * 4]
        }

    def generate_64px(self, name, data, fileName):
        text = "\n" + name
        height = data[1]
        varTypes = ["", ""]
        varNames = {
            "VAR01": "", "VAR02": ""
        }
        aliasNames = {}

        preSetCodes = []

        for num in range(0, 2):
            vName = "VAR0"+str(num+1)

            try:
                teszt = int(data[num+2])
                varTypes[num] = "constant"
                varNames[vName] = "#"+data[num+2]
            except:
                realName = data[num+2].split("::")[1]

                variable = self.__loader.virtualMemory.getVariableByName2(realName)
                varTypes[num] = variable.type
                if varTypes[num] == "byte":
                   varNames[vName] = realName
                else:
                   varNames[vName] = "temp0"+ str(num+3)
                   code =   "\tLDA\t" + realName + "\n"                 + \
                            self.convertAnyTo8Bits(variable.usedBits)   + \
                            "\tSTA\t" + varNames[num]                   + "\n"
                   preSetCodes.append(code)

        #print(varNames)
        if len(preSetCodes) > 0:
           text += "_PreSet\n"              + \
                  "\n".join(preSetCodes)    + "\n" + text

        text += "\n" + self.__loader.io.loadSubModule("64pxPicture") + "\n"
        topLevelCode = text.replace("pic64px", name)\
                           .replace("picHeight", name + "_picHeight")\
                           .replace("picIndex", name + "_picIndex")\
                           .replace("picDisplayHeight", name+"_picDisplayHeight")

        f = open(self.__loader.mainWindow.projectPath+"64px/"+fileName+".asm", "r")
        d = f.read()
        f.close()

        userData = d.replace("pic64px", name)

        enterCode = self.__loader.io.loadSubModule("64pxPictureEnter")
        ddd = enterCode.replace("\r", "").split("\n")
        for line in ddd:
            if "#VAR" in line:
                line = line.split("=")
                aliasNames[line[1].replace(" ","")] = line[0].replace(" ","")

        for item in varNames.keys():
            enterCode = enterCode.replace("#"+item+"#", varNames[item])
            if varNames[item].startswith("#"):
               enterCode = enterCode.replace("STA\t"+aliasNames["#"+item+"#"], "")


        enterCode = enterCode.replace("pic64px", name)\
                             .replace("picHeight", name + "_picHeight")\
                             .replace("picIndex", name + "_picIndex")\
                             .replace("picDisplayHeight", name+"_picDisplayHeight")\
                             .replace("FULLHEIGHT", height)

        return topLevelCode, userData, enterCode


    def generate_EmptyLines(self, name, data):
        from copy import deepcopy

        text = "\n" + name + "\n\tLDA\t"

        varType = None

        try:
            num = int(data[0])
            varType = "constant"
        except Exception as e:
            variable = self.__loader.virtualMemory.getVariableByName2(data[0])
            varType  = variable.type
            #varBits  = deepcopy(variable.usedBits)[::-1]
            varBits  = variable.usedBits

        if   varType == "constant":
           text += "#"+ data[0] +"\n"
        else:
           if self.isItSARA(data[0]):
                self.__loader.virtualMemory.getSARAReadAddressFromWriteAddress(data[0])

           text += data[0] + "\n" +\
                   self.convertAnyTo8Bits(varBits)
        text += "\tTAY\n"
        text += name + "_Loop\n"
        text += "\tCPY  #0\n\tBEQ\t" + name + "_LoopEnd\n\tDEY\n"
        text += "\tLDA\tframeColor\n"
        text += "\tSTA\tWSYNC\n"
        text += "\tSTA\tCOLUBK\n"
        text += "\tJMP\t" + name + "_Loop\n"
        text += name + "_LoopEnd\n"

        return text

    def convertAnyTo8Bits(self, bits):
        if len(bits) == 8: return ""

        txt = ""
        minNum = min(bits)
        maxNum = max(bits)

        numForROL = len(bits)+(7-maxNum)

        if minNum <= numForROL:
           counter = minNum
           shift   = "LSR"
        else:
           counter = numForROL
           shift   = "ROL"

        while counter > 0:
           txt     += "\t" + shift + "\n"
           counter -= 1

        num = "0" * (8-len(bits))
        while len(num) < 8:
            num += "1"

        txt += "\tAND\t#%"+num+"\n"
        return txt

    def isItSARA(self, num):
        if   len(num) != 5  : return False
        elif num[0]   != '$': return False

        try:
            teszt = int(num[1:])
            return True
        except:
            return False

    def generate_ChangeFrameColor(self, name, data):
        text = "\n" + name + "\n" + "\tLDA\t"

        if data[0][0] == "$":
           text += "#"

        if self.isItSARA(data[0]):
           self.__loader.virtualMemory.getSARAReadAddressFromWriteAddress(data[0])

        text+= data[0] +"\n"+"\tSTA\tframeColor\n"
        return(text)

    def preAlign(self, text):
        text = text.split("\n")
        tempText = "\n"
        blocks = []
        segments = {}
        blocks.append(Block())

        for line in text:
            if line == "":
                continue
            elif line[0].isalnum() == True or line.startswith("##NAME##"):
                if "byte" in tempText.lower():
                    seg = Segment(tempText)
                    tempText = "\n" + line + "\n"
                    segments[seg] = seg.bytes
                else:
                    tempText += "\n" + line + "\n"

            elif "byte" in line.lower():
               tempText += line + "\n"

        seg = Segment(tempText)
        segments[seg] = seg.bytes

        segmentKeys = sorted(segments, key = segments.get, reverse=True)
        for segment in segmentKeys:
            putIn = False
            for block in blocks:
                answer = block.addSegment(segment)
                if answer == True:
                   putIn = True
                   break
            if putIn == False:
               blocks.append(Block())
               blocks[-1].addSegment(segment)

        text = ""
        for block in blocks:
            for segment in block.segments:
                text += segment.text

        return text

    def __reAlignDataSection(self, text):
        if text == "": return ""

        text = self.preAlign(text)

        text = text.split("\n")

        temp = []
        for line in text:
            if line != "" and ("align" not in line.lower()):
                temp.append(line)

        byteCounter = 0

        last        = []
        for line in temp:

            if "byte" in line.lower():
                byteCounter += 1
                last[-1].append(line)
            else:
                last.append([])
                last[-1].append("\n"+line)

                if byteCounter > 256:
                   last[-2].insert(0, "\n\talign\t256\n")
                   bytes1 = 0
                   bytes2 = 0

                   for line in last[-2]:
                       if "byte" in line.lower():
                           bytes1 += 1

                   for line in last[-1]:
                       if "byte" in line.lower():
                           bytes2 += 1

                   byteCounter = bytes1 + bytes2

        last[0].insert(0, "\n\talign\t256\n")

        txt = ""
        for item in last:
            for subItem in item:
                txt += subItem + "\n"

        return txt

    def testMenu(self):
        from copy import deepcopy

        self.__lineData     = deepcopy(self.__data[0])
        self.__colorData    = deepcopy(self.__data[1])
        self.__lineNum      = self.__data[2]
        self.__segmentsText = self.__data[3]
        self.__segments     = self.__data[4]
        self.__tv           = self.__data[5]
        self.__name         = self.__data[6]
        self.__variables    = self.__data[7]
        self.__constants    = self.__data[8]

        converted      = self.getMenuASM()
        changer = self.__contructChanger(self.__variables, self.__constants)

        self.__enterCode =  self.__io.loadSubModule("menuEnter") + "\n" + \
                            self.__io.loadTestElementPlain("enterTestCommon")

        self.__topLevelCode = self.__io.loadSubModule("menuTopBottom")
        self.__overScanCode = self.__io.loadTestElementPlain("menuTestOverScan")

        for item in changer:
            self.__enterCode    = self.__enterCode.replace(item, changer[item])
            self.__topLevelCode = self.__topLevelCode.replace(item, changer[item])

        self.__enterCode = self.__enterCode.replace("##NAME##", self.__name).replace("##BANK##", "BANK2")
        self.__topLevelCode = self.__topLevelCode.replace("##NAME##", self.__name).replace("##BANK##", "BANK2")
        self.__overScanCode = self.__overScanCode.replace("##NAME##", self.__name).replace("##BANK##", "BANK2")

        converted = converted.replace("##NAME##", self.__name).replace("##BANK##", "BANK2")
        converted = self.__reAlignDataSection(converted)

        self.__mainCode = self.__io.loadKernelElement(self.__kernel, "main_kernel")
        self.__mainCode = self.__mainCode.replace("!!!TV!!!", self.__tv)
        self.__mainCode = self.__mainCode.replace("!!!ENTER_BANK2!!!", self.__enterCode)
        self.__mainCode = self.__mainCode.replace("!!!SCREENTOP_BANK2!!!", self.__topLevelCode)
        self.__mainCode = self.__mainCode.replace("!!!USER_DATA_BANK2!!!", converted)
        self.__mainCode = self.__mainCode.replace("!!!OVERSCAN_BANK2!!!", self.__overScanCode)

        self.__mainCode = re.sub(r"!!![a-zA-Z0-9_]+!!!", "", self.__mainCode)

        self.doSave("temp/")
        assembler = Assembler(self.__loader, "temp/", True, "NTSC", False)

    def menuASM(self):
        from copy import deepcopy

        self.__lineData     = deepcopy(self.__data[0])
        self.__colorData    = deepcopy(self.__data[1])
        self.__lineNum      = self.__data[2]
        self.__segmentsText = self.__data[3]
        self.__segments     = self.__data[4]
        self.__tv           = self.__data[5]
        self.__name         = self.__data[6]

        self.converted      = self.getMenuASM()
        self.converted      = self.__reAlignDataSection(self.converted)

    def getMenuASM(self):
        byteCounter = 0

        segmenttxt = "\n\talign\t256\n" + self.__name + "_segmentBorders\n"
        for item in self.__segments:
            segmenttxt +=  "\tBYTE\t#" + str(item[0]) + "\n" + \
                           "\tBYTE\t#" + str(item[1]) + "\n"

        segmenttxt += "\tBYTE\t#255\n" + \
                      "\n"


        self.__lineData = self.__lineData.split("\n")
        self.__lineData = self.__lineData[:(self.__segments[-1][1]+1)*8]
        for startNum in range(0, len(self.__lineData), 8):
            from copy import deepcopy

            temp = deepcopy(self.__lineData[startNum:startNum+8])
            for fuckNum in range(0,8):
                self.__lineData[startNum+fuckNum] = temp[7-fuckNum]

        spriteDatas = []
        startIndex = -8
        for num in range(0,6):

            startIndex += 8
            spriteDatas.append("\n"+self.__name+"__spriteData_" + str(num) + "\n")

            counter = 0
            nnn = 0
            for line in self.__lineData:
                if line != "":
                    if counter == 7:
                        spriteDatas[-1] += "\tBYTE\t#%" + line[startIndex:startIndex+8] + "\t; ("+str(nnn)+")\n"
                        counter = 0
                        nnn += 1
                    else:
                        spriteDatas[-1] += "\tBYTE\t#%" + line[startIndex:startIndex+8] + "\n"
                        counter += 1


            spriteDatas[-1] += "\n"

        colorDatas = []
        colorNames = ["UNSELECTED", "SELECTED_FG", "SELECTED_BG"]

        for num in range(0,3):
            colorDatas.append("\n" + self.__name +"_Color_"+colorNames[num]+"\n")
            for num2 in range(7, -1, -1) :
                colorDatas[-1] += "\tBYTE\t#"+self.__colorData[num][num2] +"\n"


        txt = segmenttxt
        byteCounter, overflow = self.setNewLineNum(byteCounter, txt)

        for item in spriteDatas:
            byteCounter, overflow = self.setNewLineNum(byteCounter, item)
            if overflow == True:
                txt += "\n\talign\t256\n"
            txt += item

        for item in colorDatas:
            byteCounter, overflow = self.setNewLineNum(byteCounter, item)
            if overflow == True:
                txt += "\n\talign\t256\n"
            txt += item

        return(txt)

        #for sprite in spriteDatas:
        #    print(sprite)


    def testLandScape(self):
        from copy import deepcopy

        self.__lineData = deepcopy(self.__data[0])
        self.__width = int(self.__data[1])
        self.__tv         = self.__data[2]
        self.__name       = self.__data[3]
        self.__monoMode   = self.__data[5]
        self.__removeBackGround = self.__data[6]

        variables  = self.__data[4]
        #constants  = [self.__width-40, self.__lineData[0]["colors"][1]]
        constants  = [self.__width+41]

        XXX = self.__convertLandScapeToFun()

        self.__convertedSpite = XXX[0]
        #pontertable = self.generateJumpTable(XXX[1])

        changer = self.__contructChanger(variables, constants)

#        self.__enterCode = self.__io.loadSubModule("scrollingTextEnter") +\
#                           "\n\n" +\
#                           self.__io.loadTestElementPlain("scrollingTextEnter") + "\n"

        self.__enterCode =  self.__io.loadSubModule("scrollingTextEnter") + "\n" + \
                            self.__io.loadTestElementPlain("enterTestCommon")

        #self.__overScanCode = self.__io.loadTestElementPlain("scrollingTextOverScan") + "\n"

        self.__topLevelCode = self.__io.loadSubModule("scrollingTextTopBottom").replace("###KERNEL_JUMP###",
                              self.__io.loadSubModule("kernelJump").replace(
                                  "##KERNEL_NAME##", "##BANK##_ScrollingText_Kernel_Begin"
                              ))
        #                      )).replace("###JUMPTABLE###", pontertable)
        self.__routineCode  = self.__io.loadSubModule("scrollingTextKernel") + self.__io.loadSubModule("inverted").replace("##BANK##", "BANK2")

        for item in changer:
            self.__enterCode    = self.__enterCode.replace(item, changer[item])
            # self.__overScanCode = self.__overScanCode.replace(item, changer[item])
            self.__topLevelCode = self.__topLevelCode.replace(item, changer[item])
            self.__routineCode  = self.__routineCode.replace(item, changer[item])

        if self.__monoMode == True:
            if self.__removeBackGround == True:
               self.__topLevelCode = self.__topLevelCode.replace("###NAME##_backGround", "frameColor")
            elif type(self.__removeBackGround) == str:
               self.__topLevelCode = self.__topLevelCode.replace("###NAME##_backGround", self.__removeBackGround)

        self.__enterCode = self.__enterCode.replace("##NAME##", self.__name).replace("##BANK##", "BANK2")
        self.__topLevelCode = self.__topLevelCode.replace("##NAME##", self.__name).replace("##BANK##", "BANK2")
        self.__routineCode = self.__routineCode.replace("##NAME##", self.__name).replace("##BANK##", "BANK2")
        self.__convertedSpite = self.__convertedSpite.replace("##NAME##", self.__name).replace("##BANK##", "BANK2")

        self.__mainCode = self.__io.loadKernelElement(self.__kernel, "main_kernel")
        self.__mainCode = self.__mainCode.replace("!!!TV!!!", self.__tv)
        self.__mainCode = self.__mainCode.replace("!!!ENTER_BANK2!!!", self.__enterCode)
        self.__mainCode = self.__mainCode.replace("!!!SCREENTOP_BANK2!!!", self.__topLevelCode)
        self.__mainCode = self.__mainCode.replace("!!!ROUTINES_BANK2!!!", self.__routineCode)
        self.__mainCode = self.__mainCode.replace("!!!USER_DATA_BANK2!!!", self.__convertedSpite)

        self.__mainCode = re.sub(r"!!![a-zA-Z0-9_]+!!!", "", self.__mainCode)

        self.doSave("temp/")
        assembler = Assembler(self.__loader, "temp/", True, "NTSC", False)


    def testWav(self):
        self.__kernelText = self.__loader.io.loadWholeText("templates/skeletons/common_main_kernel.asm")
        self.__pictureData = self.__loader.io.loadWholeText("templates/testCodes/pressFire.asm")
        self.__h = 83

        self.__init = (self.__loader.io.loadWholeText("templates/testCodes/64pxPictureEnter.asm").replace("FULLHEIGHT", str(self.__h))
                                                                                                 .replace("DSPHEIGHT", str(self.__h))
                                                                                                 .replace("DSPINDEX", "0"))
        self.__engine = self.__loader.io.loadWholeText("templates/skeletons/64pxPicture.asm")
        self.__overScan = (self.__loader.io.loadWholeText("templates/testCodes/testWavOverscan.asm"))
        self.__kernelText = (self.__kernelText.replace("!!!OVERSCAN_BANK2!!!", self.__overScan).replace("!!!ENTER_BANK2!!!", self.__init)
                            .replace("!!!SCREENTOP_BANK2!!!", self.__engine).replace("!!!USER_DATA_BANK2!!!", self.__pictureData)
                             .replace("!!!TV!!!", "NTSC")
                             )
        self.__kernelText = self.findAndDotALLReplace(self.__kernelText, r'###Start-Bank3.+###End-Bank3',
                                                          self.__data[0])

        self.__kernelText = self.__kernelText.replace("PlaySoundXX", self.__data[2]).replace("!!!TV!!!", "NTSC")

        self.__mainCode = re.sub(r"!!![a-zA-Z0-9_]+!!!", "", self.__kernelText)
        self.changePointerToZero(self.__data[1])
        self.doSave("temp/")
        assembler = Assembler(self.__loader, "temp/", True, "NTSC", False)


    def test64PX(self):
        self.__kernelText = self.__loader.io.loadWholeText("templates/skeletons/common_main_kernel.asm")
        self.__pictureData = self.__data[0]
        self.__h = self.__data[1]

        self.__init = (self.__loader.io.loadWholeText("templates/testCodes/64pxPictureEnter.asm").replace("FULLHEIGHT", str(self.__h))
                                                                                                 .replace("DSPHEIGHT", str(self.__h))
                                                                                                 .replace("DSPINDEX", "0")
                       )
        self.__engine = self.__loader.io.loadWholeText("templates/skeletons/64pxPicture.asm")

        self.__overScan = (self.__loader.io.loadWholeText("templates/testCodes/64pxPictureOverScan.asm").replace("FULLHEIGHT", str(self.__h))
                                                                                                 .replace("DSPHEIGHT", str(self.__h))
                                                                                                 .replace("DSPINDEX", "0"))


        self.__kernelText = (self.__kernelText.replace("!!!OVERSCAN_BANK2!!!", self.__overScan).replace("!!!ENTER_BANK2!!!", self.__init)
                            .replace("!!!SCREENTOP_BANK2!!!", self.__engine).replace("!!!USER_DATA_BANK2!!!", self.__pictureData)
                             .replace("!!!TV!!!", "NTSC")
                             )

        self.__mainCode = re.sub(r"!!![a-zA-Z0-9_]+!!!", "", self.__kernelText)
        self.doSave("temp/")
        assembler = Assembler(self.__loader, "temp/", True, "NTSC", False)

    def getMusicBytesSizeOnly(self):
        self.banks, self.bytes = self.generateSongBytes(self.__data[0], "NTSC")
        self.musicMode = self.__musicMode

    def generateMusicROM(self):
        import re

        self.__picturePath = self.__data[0]
        self.__pathToSave = self.__data[1]

        # valid: mono, stereo, double
        self.__musicMode = "stereo"

        self.__openEmulator = self.__data[2]

        self.__textBytes, self.__charNums = self.generateTextDataFromString(self.__data[3] + " - "+self.__data[4])
        self.__songData, bytes = self.generateSongBytes(self.__data[5], "NTSC")

        self.__banks = self.__data[6]
        self.__variables = self.__data[7]
        self.__colors = self.__data[8]
        self.__pictureData = self.__data[9]

        CoolSong = (self.__data[3] + " - "+self.__data[4]).replace(" ", "_")
        CoolSong = "".join(re.findall(r'[a-zA-Z_0-9\-]+[a-zA-Z_0-9]', CoolSong))

        #self.__init += "\n" + self.__loader.io.loadWholeText("templates/testCodes/musicEnterPlus.asm")

        self.__init = ("\n" + self.__loader.io.loadWholeText("templates/testCodes/musicTestEnter.asm")
                        .replace("FULLHEIGHT", str(self.__pictureData[0]))
                        .replace("DSPHEIGHT", str(self.__pictureData[1]))
                        .replace("DSPINDEX", str(self.__pictureData[2]))
                        .replace("TEST_TEXT_COLOR", str(self.__colors[0]))
                        .replace("TEST_BACK_COLOR", str(self.__colors[1]))
                        .replace("FRAME_COLOR", str(self.__colors[2]))
                        .replace("TEST_TEXT_END", str(len(self.__charNums)-12)))


        for num in range(0,12):

            strNum = str(num+1)
            if len(strNum) == 1:
                strNum = "0"+strNum

            try:
                self.__init = self.__init.replace("INITLETTER"+strNum, str(self.__charNums[num]))
            except:
                self.__init = self.__init.replace("INITLETTER"+strNum, "0")


        self.__music0 = self.createMusicEngine(0, CoolSong)
        if self.__musicMode != "mono":
            self.__music1 = self.createMusicEngine(1, CoolSong)
            self.__music0 = self.__music0.replace("!!!Song_Restart!!!",
                                                  self.__loader.io.loadWholeText("templates/skeletons/musicRestart.asm")
                                                  .replace("@@", "0") +
                                                  self.__loader.io.loadWholeText("templates/skeletons/musicRestart.asm")
                                                  .replace("@@", "1")
                                                  )

            self.__music1 = self.__music1.replace("!!!Song_Restart!!!",
                                                  self.__loader.io.loadWholeText("templates/skeletons/musicRestart.asm")
                                                  .replace("@@", "0") +
                                                  self.__loader.io.loadWholeText("templates/skeletons/musicRestart.asm")
                                                  .replace("@@", "1")
                                                  )

        else:
            self.__music1 = None
            self.__music0 = self.__music0.replace("!!!Song_Restart!!!",
                                                  self.__loader.io.loadWholeText("templates/skeletons/musicRestart.asm")
                                                  .replace("@@", "0"))


        if self.__musicMode == "mono":
            self.__music0 = self.__music0.replace("!!!JumpOrReturn!!!",
                                 self.__loader.io.loadWholeText("templates/skeletons/musicJumpBack.asm")
                                                  )
        elif self.__musicMode == "stereo":
            self.__music0 = self.__music0.replace("!!!JumpOrReturn!!!",
                                  self.__music1)
            self.__music0 = self.__music0.replace("!!!JumpOrReturn!!!",
                                  self.__loader.io.loadWholeText("templates/skeletons/musicJumpBack.asm"))
            self.__music1 = None

        elif self.__musicMode == "double":
            self.__music0 = self.__music0.replace("!!!JumpOrReturn!!!",
                                  self.__loader.io.loadWholeText("templates/skeletons/musicJumpNext.asm")
                                  .replace("BANKNEXT", str(self.__banks[1]))
                                  .replace("Cool_Song", CoolSong))
            self.__music1 = self.__music1.replace("!!!JumpOrReturn!!!",
                                  self.__loader.io.loadWholeText("templates/skeletons/musicJumpBack.asm"))

        if self.__musicMode == "mono":
            self.__init += "\n" + "CoolSong_Pointer0 = $e2\nCoolSong_Duration0 = $e4"
            self.__init += "\n" + "CoolSong_PointerBackUp0 = $e5"
            self.__init += "\n" + self.__loader.io.loadWholeText("templates/skeletons/musicInitMono.asm")

        else:
            self.__init += "\n\n" + "CoolSong_Pointer0 = $e2\nCoolSong_Duration0 = $e4\nCoolSong_Pointer1 = $e5\nCoolSong_Duration1 = $e7"
            self.__init += "\n" + "CoolSong_PointerBackUp0 = $e8" + "\n" + "CoolSong_PointerBackUp1 = $ea" + "\n"

            self.__init += "\n\n" + self.__loader.io.loadWholeText("templates/skeletons/musicInitStereo.asm")

        self.__init = self.__init.replace("CoolSong", CoolSong)




        self.__kernelText = self.__loader.io.loadWholeText("templates/skeletons/common_main_kernel.asm")
        self.__kernelText = self.__kernelText.replace("!!!ENTER_BANK2!!!", self.__init)

        self.__kernelText = self.__kernelText.replace("!!!OVERSCAN_BANK2!!!",
                                  (self.__loader.io.loadWholeText("templates/testCodes/musicTestOverScan.asm")
                                   + "\n" + self.__loader.io.loadWholeText("templates/skeletons/musicJumpStart.asm"))
                                  .replace("BANKBACK", "2")
                                  .replace("BANKNEXT", str(self.__banks[0]))
                                  )

        if self.__musicMode == "mono":
            #self.__kernelText = re.sub(r'###Start-Bank3.+###End-Bank3', self.__music0 + "\n\talign\t256\n"+self.__songData[0], self.__kernelText, re.DOTALL)
            self.__kernelText = self.findAndDotALLReplace(self.__kernelText, r'###Start-Bank3.+###End-Bank3',
                                                          self.__music0 + "\n" + self.__songData[0]
                                                          )

        elif self.__musicMode == "stereo":
            #self.__kernelText = re.sub(r'###Start-Bank3.+###End-Bank3', self.__music0 + "\n\talign\t256\n"+
            #                           self.__songData[0] + "\n" + self.__songData[1], self.__kernelText, re.DOTALL)

            self.__kernelText = self.findAndDotALLReplace(self.__kernelText, r'###Start-Bank3.+###End-Bank3',
                                                          self.__music0 + "\n"+self.__songData[0] + "\n" + self.__songData[1]
                                                          )
        elif self.__musicMode == "double":
            #self.__kernelText = re.sub(r'###Start-Bank3.+###End-Bank3', self.__music0 + "\n\talign\t256\n"+self.__songData[0], self.__kernelText, re.DOTALL)
            #self.__kernelText = re.sub(r'###Start-Bank4.+###End-Bank4', self.__music1 + "\n\talign\t256\n"+self.__songData[1], self.__kernelText, re.DOTALL)

            self.__kernelText = self.findAndDotALLReplace(self.__kernelText, r'###Start-Bank3.+###End-Bank3',
                                                          self.__music0 + "\n" + self.__songData[0]
                                                          )

            self.__kernelText = self.findAndDotALLReplace(self.__kernelText, r'###Start-Bank4.+###End-Bank4',
                                                          self.__music1 + "\n" + self.__songData[1]
                                                          )

        self.__bank2Data = self.__loader.io.loadWholeText("templates/skeletons/48pxTextFont.asm")

        if self.__picturePath == None:
            picName = "fortari"
            self.__bank2Data += self.__loader.io.loadWholeText("templates/testCodes/fortariLogo.asm").replace("pic64px", picName)
        else:
            picName = ".".join(self.__picturePath.split("/")[-1].split(".")[:-1])
            self.__bank2Data += self.__loader.io.loadWholeText(self.__picturePath).replace("pic64px", picName)

        self.__bank2Data+="\n"+self.__textBytes

        musicVisuals = self.__loader.io.loadWholeText("templates/skeletons/musicVisualizer.asm").replace("Music_Visuals", CoolSong+"_Visuals")
        if self.__variables[0] == None:
            musicVisuals = musicVisuals.replace("temp&1", "temp16")
        else:
            musicVisuals = musicVisuals.replace("temp&1", self.__variables[0])

        if self.__variables[1] == None:
            musicVisuals = musicVisuals.replace("temp&2", "temp17")
        else:
            musicVisuals = musicVisuals.replace("temp&2", self.__variables[1])

        if self.__variables[2] == None:
            musicVisuals = musicVisuals.replace("temp&3", "temp18")
        else:
            musicVisuals = musicVisuals.replace("temp&3", self.__variables[2])

        if self.__variables[3] == None:
            musicVisuals = musicVisuals.replace("temp&4", "temp19")
        else:
            musicVisuals = musicVisuals.replace("temp&4", self.__variables[3])

        musicVisuals = (musicVisuals.replace("#COLOR3#", self.__colors[3][1])
                                    .replace("#COLOR4#", self.__colors[4][1])
                                    .replace("#COLOR5#", self.__colors[5][1]))

        
        self.__screenTop = (self.__loader.io.loadWholeText("templates/skeletons/64pxPicture.asm")+"\n" +
                           self.__loader.io.loadWholeText("templates/skeletons/48pxTextDisplay.asm")+ "\n" +
                            musicVisuals + "\n")

        self.__screenTop = self.__screenTop.replace("pic64px", picName).replace("48pxText", CoolSong)

        self.__kernelText = (self.__kernelText.replace("!!!USER_DATA_BANK2!!!", self.__bank2Data)
                             .replace("!!!SCREENTOP_BANK2!!!", self.__screenTop)
                             )

        self.__kernelText = self.__kernelText.replace("!!!TV!!!", "NTSC").replace("BankXX", "Bank2")

        self.__mainCode = re.sub(r"!!![a-zA-Z0-9_]+!!!", "", self.__kernelText).replace("CoolSong", CoolSong)

        if self.__musicMode == "double":
            self.changePointerToZero(self.__banks[1])
        self.changePointerToZero(self.__banks[0])

        if self.__musicMode != "overflow":
            self.doSave(self.__pathToSave)
            if self.__pathToSave!="temp/":
                delete = True
            else:
                delete = False
            assembler = Assembler(self.__loader, self.__pathToSave, True, "NTSC", delete)
        else:
            self.__loader.fileDialogs.displayError("overflow", "overflowMessage", None, "Bank0: "+str(bytes[0])+"; Bank1: "+str(bytes[1]))

        #file = open("ffff.txt", "w")
        #file.write(self.__kernelText)
        #file.close()


    def changePointerToZero(self, bankNum):
        items = [
            "ScreenBottomBank@@", "EnterScreenBank@@", "VBlankEndBank@@"
        ]

        for item in items:
            item = item.replace("@@", str(bankNum))
            self.__mainCode = self.__mainCode.replace(item, "Zero")


    def findAndDotALLReplace(self, string, pattern, repl):

        stuff = re.findall(pattern, string, re.DOTALL)[0]
        return(string.replace(stuff, repl))



    def createMusicEngine(self, num, title):
        dividersAsl = {1:0, 2:1, 4:2, 8:3, 16:4, 32:5, 64:6, 128:7}

        __music = self.__loader.io.loadWholeText("templates/skeletons/musicEngine.asm")
        __music = __music.replace("@@", str(num))
        __music = __music.replace("CoolSong", title).replace("!!!ASL!!!", (dividersAsl[self.__largestDividers[num]]) * "\tASL\n")

        if self.__variables[num*2] == None:
            __music = __music.replace("temp&1", "temp"+str(16+(num*2)))
        else:
            __music = __music.replace("temp&1", self.__variables[num*2])

        if self.__variables[(num*2)+1] == None:
            __music = __music.replace("temp&2", "temp"+str(17+(num*2)))
        else:
            __music = __music.replace("temp&2", self.__variables[(num*2)+1])

        return(__music)

    def __getLargestDividerChannel(self, channelNum, tiaData, tv):
        from copy import deepcopy

        largest = 1
        #dividers = [2, 3, 4, 5, 7, 9, 11, 13, 16, 17, 19, 23, 25]
        dividers = [2, 4, 8, 16, 32, 64, 128]

        for divider in dividers:
            tempDur = 0
            setShit = True
            for note in tiaData[channelNum]:
                if tv == "PAL":
                    duration = int(note.duration/6*5)
                    tempDur +=note.duration-duration

                    if tempDur>1:
                        duration+=1
                        tempDur-=1

                else:
                    duration = note.duration

                if duration%divider!=0:
                    setShit = False
                    break

            if setShit == True:
                largest = divider
            else:
                break
        return(largest)

    def generateSongBytes(self, tiaData, tv):
        from TiaNote import TiaNote
        Channels = ["", ""]
        tempDur = 0
        bytes = [0,0]

        if len(tiaData) == 1:
            Channels.pop(1)
            self.__musicMode = "mono"
            if tiaData[0][-1].volume == 0 and tiaData[0][-1].duration > 6:
               tiaData[0][-1].duration = 6

            while tiaData[0][0].volume == 0:
                tiaData[0].pop(0)

        else:
            self.__musicMode = "stereo"
            if tiaData[0][-1].volume == 0 and tiaData[1][-1].volume == 0:
                if tiaData[0][-1].duration > tiaData[1][-1].duration:
                    if tiaData[1][-1].duration > 6:
                        maxi = 6
                    else:
                        maxi = tiaData[1][-1].duration
                else:
                    if tiaData[0][-1].duration > 6:
                        maxi = 6
                    else:
                        maxi = tiaData[0][-1].duration
                tiaData[0][-1].duration = maxi
                tiaData[1][-1].duration = maxi

        self.__largestDividers = [self.__getLargestDividerChannel(0, tiaData, tv)]
        if len(tiaData) == 2:
            self.__largestDividers.append(self.__getLargestDividerChannel(1, tiaData, tv))


        dataBytesNotes = [[], []]
        for num in range(0, len(tiaData)):
            for tiaNote in tiaData[num]:
                #if int(tiaNote.volume)<0 or int(tiaNote.channel)<0 or int(tiaNote.freq)<0 or int(tiaNote.duration)<0:
                #    print(tiaNote.volume, tiaNote.channel, tiaNote.freq, tiaNote.duration)

                noteText = ""
                firstByte = self.createBits(tiaNote.channel, 4) + self.createBits(tiaNote.volume, 4)

                if tv == 'PAL':
                    duration = int(tiaNote.duration/self.__largestDividers[num]/6*5)
                    tempDur +=tiaNote.duration-duration

                    if tempDur>1:
                        duration+=1
                        tempDur-=1

                else:
                    duration = tiaNote.duration/self.__largestDividers[num]

                if tiaNote.volume == 0:
                    Channels[num] += "\tBYTE\t#%00000000\n\tBYTE\t#%"+self.createBits(duration, 8)+"\n"
                    noteText+= "\tBYTE\t#%00000000\n\tBYTE\t#%"+self.createBits(duration, 8)+"\n"

                    bytes[num] +=2

                elif duration<8:
                    secondByte = self.createBits(duration, 3) + self.createBits(tiaNote.freq, 5)
                    Channels[num]+="\tBYTE\t#%"+firstByte+"\n\tBYTE\t#%"+secondByte+"\n"
                    noteText += "\tBYTE\t#%"+firstByte+"\n\tBYTE\t#%"+secondByte+"\n"

                    bytes[num] +=2
                else:
                    secondByte = self.createBits(tiaNote.freq, 8)
                    thirdByte = self.createBits(duration, 8)

                    Channels[num] += "\tBYTE\t#%" + firstByte + "\n\tBYTE\t#%" + secondByte + "\n"+"\n\tBYTE\t#%" + thirdByte + "\n"
                    noteText+= "\tBYTE\t#%" + firstByte + "\n\tBYTE\t#%" + secondByte + "\n"+"\n\tBYTE\t#%" + thirdByte + "\n"

                    bytes[num] += 3
                dataBytesNotes[num].append(noteText.replace("\n\n", "\n"))

        Channels[0] = re.sub("\n+", "\n", Channels[0])
        if self.__musicMode != "mono":
            Channels[1] = re.sub("\n+", "\n", Channels[1])

        Channels[0], bytes[0] = self.compress(Channels[0], "CoolSong", 0, dataBytesNotes[0], False)

        self.bytes = bytes

        if bytes[0] > bytes[0]>3600:
            self.__musicMode = "overflow"

        if self.__musicMode != "mono" and self.__musicMode != "overflow":
            Channels[1], bytes[1] = self.compress(Channels[1], "CoolSong", 1, dataBytesNotes[1], False)

            if (bytes[0] + bytes[1]) > 3500:
                self.__musicMode = "double"
                if (bytes[0]>3600) or (bytes[1]>3600):
                    self.__musicMode = "overflow"

            else:
                self.__musicMode = "stereo"

        return(Channels, bytes)




    def compress(self, data, sectonName, channelNum, dataArrayNotes, generateNotes):
        patterns = {}

        import time as TIME
        start_time = TIME.time()

        data = data.replace("\n\n", "\n")

        args = str(channelNum)+ " " + str(int(generateNotes)) + " " + sectonName
        dataToSend = {"00": data, "01": "---\n".join(dataArrayNotes)}

        dataPatterns = self.__executor.callFortran("Compress","GetPatterns", dataToSend, args, True, True)
        dataOccurences = self.__executor.callFortran("Compress","GetOccurences",
                                                     {"00": dataPatterns, "01": dataToSend["01"]},
                                                     args, True, True)

        dataSorted =  self.__executor.callFortran("Compress","SortWeights", dataOccurences, None, True, True)


        dataFinal = self.__executor.callFortran("Compress","Finalizing",
                                                     {"00": dataPatterns, "01": dataToSend["01"], "02": dataSorted},
                                                     args, True, True)

        savers = self.__executor.callFortran("Compress","SingleNoteOccurs", dataToSend["01"], None, True, True)

        if generateNotes == False:
            patternsWithKeys = {"00010000": ["", False],
                                "00100000": ["", False],
                                "00110000": ["", False],
                                "01000000": ["", False],
                                "01010000": ["", False],
                                "01100000": ["", False],
                                "01110000": ["", False],
                                "10000000": ["", False],
                                "10010000": ["", False],
                                "10100000": ["", False],
                                "10110000": ["", False],
                                "11000000": ["", False],
                                "11010000": ["", False]
            }


        keys = list(patternsWithKeys.keys())

        bigData = dataToSend["01"]

        usedOnes = ""

        for key in savers.keys():
            savers[key] = "---\n" + "\n".join(savers[key]).replace("\r","")+"---\n"
        saverNum = 1

        for num in range(0, 13):
            key = str(num+1)
            if len(key) == 1:
                key = "0" + key

            if key not in dataFinal:
                continue

            patternsWithKeys[keys[num]][0] = "---\n" + "\n".join(dataFinal[key])+"---\n"

            if (patternsWithKeys[keys[num]][0] in bigData) and patternsWithKeys[keys[num]][0] != "":
                patternsWithKeys[keys[num]][1] = True
            else:
                saverKey = str(saverNum)
                if (len(saverKey) == 1):
                    saverKey = "0" + saverKey

                if saverKey in savers:
                    if ((savers[saverKey] in bigData) and savers[saverKey] != ""):
                        patternsWithKeys[keys[num]][0] = savers[saverKey]

                        patternsWithKeys[keys[num]][1] = True
                        saverNum += 1

            if patternsWithKeys[keys[num]][1] == True:

                bigData = bigData.replace(patternsWithKeys[keys[num]][0],
                                          "---\n" + "\tBYTE\t#%" + keys[num] + "\t; This was changed!\n") + "---\n"
                usedOnes += sectonName + "_Channel" + str(channelNum) + "_" + keys[num] + "\n" + \
                            patternsWithKeys[keys[num]][0] + "\tBYTE\t#%11100000\n\n"

        #f = open("fasz"+str(channelNum)+".txt", "w")
        #f.write(nincs)
        #f.close()

        bigData += "\t"+"BYTE"+"\t"+"#%11110000\n"

        stringData = sectonName+"_Data"+ str(channelNum)+"_CompressedPointerTable\n\tBYTE\t#0\n\tBYTE\t#0\n"
        for name in patternsWithKeys.keys():
            if patternsWithKeys[name] != "":
                if patternsWithKeys[name][1] == True:
                    stringData+="\tBYTE\t#<"+sectonName+"_Channel"+str(channelNum)+"_"+name+"\n"
                    stringData+="\tBYTE\t#>"+sectonName+"_Channel"+str(channelNum)+"_"+name+"\n"
                else:
                    stringData+="\tBYTE\t#0\n"
                    stringData+="\tBYTE\t#0\n"


        stringData += "\n" + usedOnes +"\n" + sectonName+"_Data"+str(channelNum)+"\n"+bigData
        stringData = stringData.replace("---\n", "")

        numberOfBytes = 0
        for line in stringData.split("\n"):
            if "BYTE" in line:
                numberOfBytes+=1

        return(stringData, numberOfBytes)


    def createBits(self, num, l):
        source = num
        num = int(num)
        num = bin(num).replace("0b", "")
        while len(num)<l:
            num = "0"+num

        if ("b" in num) or ("-" in num):
            ff = []
            print(source, num, l)
            print(ff[0])
        return(num)

    def generateTextDataFromString(self, text):
        textToReturn = "\talign\t256\nCoolSong_ReallyNiceText\n"
        charNums = []

        while len(text)<12:
            text+=" "

        charset = {
            "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
            "A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15, "G": 16, "H": 17, "I": 18, "J": 19,
            "K": 20, "L": 21, "M": 22, "N": 23, "O": 24, "P": 25, "Q": 26, "R": 27, "S": 28, "T": 29,
            "U": 30, "V": 31, "W": 32, "X": 33, "Y": 34, "Z": 35,
            " ": 36, '\t': 36, '\n': 36,
            "<": 37, "(": 37, "[": 37, "{": 37,
            ">": 38, ")": 38, "]": 38, "}": 38,
            "+": 39, "-": 40, "=": 41, "*": 42, "¤": 42, "/": 43, "%": 44, "_": 45, ".": 46, "!": 47, "?": 48, ":": 49,
            ",": 46, ";": 49
        }

        for char in text.upper():
            if char in charset:
                textToReturn +="\tBYTE\t#"+str(charset[char]) + "\n"
                charNums.append(charset[char])
            else:
                textToReturn += "\tBYTE\t#36\n"
                charNums.append(36)


        textToReturn+= "\tBYTE\t#255\n"

        return(textToReturn, charNums)

    def kernelTest(self):
        self.__openEmulator = True

        self.__mainCode = self.__data[0]
        self.__enterCode = self.__data[1]
        self.__overScanCode = self.__data[2]
        self.__screenTopCode = self.__data[3]
        self.__kernelData = self.__data[4]


        self.__mainCode = self.__mainCode.replace("!!!TV!!!", "NTSC")
        self.__mainCode = self.__mainCode.replace("!!!ENTER_BANK2!!!", self.__enterCode)
        self.__mainCode = self.__mainCode.replace("!!!OVERSCAN_BANK2!!!", self.__overScanCode)
        self.__mainCode = self.__mainCode.replace("!!!SCREENTOP_BANK2!!!", self.__screenTopCode)
        self.__mainCode = self.__mainCode.replace("!!!KERNEL_DATA!!!", self.__kernelData)
        self.__mainCode = re.sub(r"!!![a-zA-Z0-9_]+!!!", "", self.__mainCode)

        self.doSave("temp/")
        assembler = Assembler(self.__loader, "temp/", True, "NTSC", False)

    def getPFASM(self):
        self.__pixelData = self.__data[0]
        self.__colorData = self.__data[1]
        self.__max = int(self.__data[2])
        self.__tv = self.__data[3]

        self.__mirrored = [0, 1, 1]
        self.__name = self.__data[4]

        self.convertedPlayfield =   self.convertPixelsToPlayfield(self.__name) +\
                                    self.addColors(self.__name)


    def pfTest(self):
        self.__openEmulator = True

        self.__mainCode = self.__io.loadKernelElement(self.__kernel, "main_kernel")
        self.__enterCode = self.__io.loadTestElement(self.__mode, self.__kernel, "enter")
        self.__overScanCode = self.__io.loadTestElement(self.__mode, self.__kernel, "overscan")

        self.__pixelData = self.__data[0]
        self.__colorData = self.__data[1]
        self.__max = int(self.__data[2])
        self.__tv = self.__data[3]

        if self.__kernel == "common":
            self.__mirrored = [0, 1, 1]

            min = 26
            max = 26 + (self.__max - 42)

            self.__overScanCode = self.__overScanCode.replace("!!!Max!!!", str(max))
            self.__enterCode = self.__enterCode.replace("!!!Min!!!", str(min))
            self.__overScanCode = self.__overScanCode.replace("!!!Min!!!", str(min))

        self.__convertedPlayfield = self.convertPixelsToPlayfield("TestPlayfield")
        if self.__kernel in ["common"]:
            self.__convertedPlayfield += self.addColors("TestPlayfield")

        self.__mainCode = self.__mainCode.replace("!!!TV!!!", self.__tv)
        self.__mainCode = self.__mainCode.replace("!!!ENTER_BANK2!!!", self.__enterCode)
        self.__mainCode = self.__mainCode.replace("!!!OVERSCAN_BANK2!!!", self.__overScanCode)
        self.__mainCode = self.__mainCode.replace("!!!KERNEL_DATA!!!", self.__convertedPlayfield)
        self.__mainCode = re.sub(r"!!![a-zA-Z0-9_]+!!!", "", self.__mainCode)

        self.doSave("temp/")
        assembler = Assembler(self.__loader, "temp/", True, self.__tv, False)

    def getSpriteASM(self):
        self.__spritePixels = self.__data[0]
        self.__spriteColors = self.__data[1]
        self.__height = int(self.__data[2])
        self.__frameNum = int(self.__data[3])
        self.__tv = self.__data[4]
        self.__name = self.__data[5]

        self.convertedSpite = self.convertPixelsToSpriteFrameLine(self.__name)

    def getBigSpriteASM(self):
        self.__spriteData = self.__data[0]
        self.__lineHeight = int(self.__data[1])
        self.__height     = int(self.__data[2])
        self.__spriteMode = self.__data[3]
        self.__frameNum   = int(self.__data[4])
        self.__tv         = self.__data[5]
        self.__name       = self.__data[6]

        self.convertedSpite = self.__convertDataToReallyBigSprite(self.__name)

    def testBigSprite(self):
        self.__spriteData = self.__data[0]
        self.__lineHeight = int(self.__data[1])
        self.__height     = int(self.__data[2])
        self.__spriteMode = self.__data[3]
        self.__frameNum   = int(self.__data[4])
        self.__tv         = self.__data[5]
        self.__name       = self.__data[6]
        self.__frameColor = self.__data[7]

        if self.__spriteMode == "simple":
           self.__mono = 1
        else:
           self.__mono = 0

        if self.__spriteMode == "double":
           self.__offset = 8
        else:
           self.__offset = 0

        variables = self.__data[8]
        constants = [self.__height, self.__lineHeight, self.__offset, self.__mono, self.__frameNum]

        try:
            teszt = int(self.__frameColor)
        except:
            self.__frameColor = 0


        self.__convertedSpite = self.__convertDataToReallyBigSprite(self.__name)

        changer = self.__contructChanger(variables, constants)

        self.__enterCode = self.__io.loadSubModule("bigSpriteEnter") +\
                           "\n\n" +\
                           self.__io.loadTestElementPlain("bigSpriteEnter") + "\n"

        self.__overScanCode = self.__io.loadTestElementPlain("bigSpriteOverScan") + "\n"

        self.__topLevelCode = self.__io.loadSubModule("bigSpriteTopBottom") + "\n" +\
                              self.__io.loadSubModule("kernelJump").replace(
                                  "##KERNEL_NAME##", "##BANK##_BigSprite_Kernel_Begin"
                              )
        self.__routineCode  = self.__io.loadSubModule("bigSpriteKernel")

        for item in changer:
            self.__enterCode    = self.__enterCode.replace(item, changer[item])
            self.__overScanCode = self.__overScanCode.replace(item, changer[item])
            self.__topLevelCode = self.__topLevelCode.replace(item, changer[item])
            self.__routineCode  = self.__routineCode.replace(item, changer[item])

        self.__enterCode        = self.__enterCode.replace("##NAME##", self.__name).replace("##BANK##", "BANK2").replace("FRAME_COLOR", str(self.__frameColor))
        self.__overScanCode     = self.__overScanCode.replace("##NAME##", self.__name).replace("##BANK##", "BANK2")
        self.__topLevelCode     = self.__topLevelCode.replace("##NAME##", self.__name).replace("##BANK##", "BANK2")
        self.__routineCode      = self.__routineCode.replace("##NAME##", self.__name).replace("##BANK##", "BANK2")
        self.__convertedSpite   = self.__convertedSpite.replace("##NAME##", self.__name).replace("##BANK##", "BANK2")

        self.__mainCode = self.__io.loadKernelElement(self.__kernel, "main_kernel")
        self.__mainCode = self.__mainCode.replace("!!!TV!!!", self.__tv)
        self.__mainCode = self.__mainCode.replace("!!!ENTER_BANK2!!!", self.__enterCode)
        self.__mainCode = self.__mainCode.replace("!!!OVERSCAN_BANK2!!!", self.__overScanCode)
        self.__mainCode = self.__mainCode.replace("!!!SCREENTOP_BANK2!!!", self.__topLevelCode)
        self.__mainCode = self.__mainCode.replace("!!!ROUTINES_BANK2!!!", self.__routineCode)
        self.__mainCode = self.__mainCode.replace("!!!USER_DATA_BANK2!!!", self.__convertedSpite)

        self.__mainCode = re.sub(r"!!![a-zA-Z0-9_]+!!!", "", self.__mainCode)

        self.doSave("temp/")
        assembler = Assembler(self.__loader, "temp/", True, self.__tv, False)

    def __contructChanger(self, variables, constants):
        d = {}

        for origN in range(1, len(variables)+1):
            num = str(origN)
            if len(num) == 1: num = "0" + num

            d["##VAR"+num+"##"] = str(variables[origN-1])

        for origN in range(1, len(constants)+1):
            num = str(origN)
            if len(num) == 1: num = "0" + num

            d["##CON" + num+"##"] = str(constants[origN-1])

        return d


    def __convertDataToReallyBigSprite(self, name):
        pixelData0      = "\n" + name + "_BigSprite_0"      + "\n"
        colorData0      = "\n" + name + "_BigSpriteColor_0" + "\n"
        backGroundData  = "\n" + name + "_BigSpriteBG"      + "\n"

        lineNum = 0
        isThereASinglePixelinP1 = False

        for spriteNum in range(0, self.__frameNum):
            line = self.__spriteData[spriteNum][0]
            bgLine = self.__spriteData[spriteNum][2]
            for Y in range(self.__height-1, -1, -1):
                pixels = line[Y]["pixels"]
                pixelLine = "\tbyte\t#%" + "".join(pixels[0:8])
                if spriteNum == 0:
                    colorLine = "\tbyte\t#" + line[Y]["color"] + "\n"
                    bgLineD = "\tbyte\t#" + bgLine[Y]["color"] + "\n"

                lineNum += 1
                if lineNum == self.__height:
                    pixelLine += "\t; (" + str(spriteNum) + ")" + "\n"
                    lineNum = 0
                else:
                    pixelLine += "\n"

                pixelData0 += pixelLine
                if spriteNum == 0:
                    colorData0     += colorLine
                    backGroundData += bgLineD

        pixelData1 = None
        colorData1 = None
        lineNum    = 0

        if self.__spriteMode != "simple":
            stuff = {
                "double":  [0,8,16],
                "overlay": [1,0,8]
            }

            pixelData1 = "\n" + name + "_BigSprite_1" + "\n"
            if self.__spriteMode == "overlay":
                colorData1 = "\n" + name + "_BigSpriteColor_1" + "\n"

            for spriteNum in range(0, self.__frameNum):
                line = self.__spriteData[spriteNum][stuff[self.__spriteMode][0]]
                for Y in range(self.__height-1, -1, -1):
                    pixels = line[Y]["pixels"]
                    if "1" in pixels: isThereASinglePixelinP1 = True

                    pixelLine = "\tbyte\t#%" + "".join(pixels[stuff[self.__spriteMode][1]:stuff[self.__spriteMode][2]])
                    if spriteNum == 0 and self.__spriteMode == "overlay":
                        colorLine = "\tbyte\t#" + line[Y]["color"] + "\n"

                    lineNum += 1
                    if lineNum == self.__height:
                        pixelLine += "\t; (" + str(spriteNum) + ")" + "\n"
                        lineNum = 0
                    else:
                        pixelLine += "\n"

                    pixelData1 += pixelLine
                    if self.__spriteMode == "overlay" and spriteNum == 0:
                        colorData1 += colorLine


        if isThereASinglePixelinP1 == False:
            pixelData1 = None
            colorData1 = None

        lineNum = 0

        if self.__spriteMode == "overlay":
           pixelData0 = pixelData0.replace("_BigSprite_0", "_BigSprite_1")
           colorData0 = colorData0.replace("_BigSpriteColor_0", "_BigSpriteColor_1")
           if isThereASinglePixelinP1 == True:
               pixelData1 = pixelData1.replace("_BigSprite_1", "_BigSprite_0")
               colorData1 = colorData1.replace("_BigSpriteColor_1", "_BigSpriteColor_0")

        text = "\talign\t256\n" + pixelData0 + "\n"
        lineNum = self.getBytesNum(text)

        if self.setNewLineNum(lineNum, colorData0)[1] == True:
           text += "\talign\t256\n"

        text += colorData0 + "\n"
        lineNum = self.setNewLineNum(lineNum, colorData0)[0]

        if isThereASinglePixelinP1 == True:
            if self.setNewLineNum(lineNum, pixelData1)[1] == True:
                text += "\talign\t256\n"

            text += pixelData1 + "\n"
            lineNum = self.setNewLineNum(lineNum, pixelData1)[0]

            if self.__spriteMode == "overlay":
                if self.setNewLineNum(lineNum, colorData1)[1] == True:
                    text += "\talign\t256\n"

                text += colorData1 + "\n"
                lineNum = self.setNewLineNum(lineNum, colorData1)[0]

        if self.setNewLineNum(lineNum, backGroundData)[1] == True:
            text += "\talign\t256\n"

        text += backGroundData + "\n"
        lineNum = self.setNewLineNum(lineNum, backGroundData)[0]

        emptyness = name + "_Empty"+"\n"+"\tBYTE\t#0\n"*self.__height

        if self.setNewLineNum(lineNum, emptyness)[1] == True:
            text += "\talign\t256\n"

        text += emptyness + "\n"
        lineNum = self.setNewLineNum(lineNum, emptyness)[0]

        text = self.checkIfMissing(name, text)


        return(text)

    def checkIfMissing(self, name, text):
        parts = [name + "_BigSprite_XXX\n",
                 name + "_BigSpriteColor_XXX" + "\n"]

        for item in parts:
            for num in range(0, 2):
                if item.replace("XXX", str(num)) not in text:
                   text = text.replace(
                       item.replace("XXX", str(1 - num)),
                       item.replace("XXX", str(num))+item.replace("XXX", str(1 - num))
                   )
        return(text)

    def setNewLineNum(self, orig, text):
        overflow = False
        new = self.getBytesNum(text)

        num = orig + new
        if num > 256:
           num = num - 256
           overflow = True

        #(orig, new, num, overflow)
        return(num, overflow)


    def getBytesNum(self, text):
        text = text.upper().split("\n")
        c = 0
        for line in text:
            if "BYTE" in line:
                c+=1
        return(c)




    def spriteTest(self):
        self.__openEmulator = True

        self.__mainCode = self.__io.loadKernelElement(self.__kernel, "main_kernel")

        p1Mode = self.__data[8]
        if p1Mode == 1:
            self.__enterCode = self.__io.loadTestElement(self.__mode, self.__kernel, "enterP1")
            self.__overScanCode = self.__io.loadTestElement(self.__mode, self.__kernel, "overscanP1")
        else:
            self.__enterCode = self.__io.loadTestElement(self.__mode, self.__kernel, "enter")
            self.__overScanCode = self.__io.loadTestElement(self.__mode, self.__kernel, "overscan")



        self.__spritePixels = self.__data[0]
        self.__spriteColors = self.__data[1]
        self.__height = int(self.__data[2])
        self.__frameNum = int(self.__data[3])
        self.__tv = self.__data[4]

        pfName = self.__data[5]
        bgName = self.__data[6]
        bgColor = self.__data[7]




        self.setPFandBGfromFiles(pfName, bgName, bgColor)

        if self.__kernel == "common":
            self.__mirrored = [0, 1, 1]


            min = 26
            max = 26 + (self.__max - 42)

            self.__overScanCode = self.__overScanCode.replace("!!!Max!!!", str(max))
            self.__enterCode = self.__enterCode.replace("!!!Min!!!", str(min))

            self.__overScanCode = self.__overScanCode.replace("!!!Min!!!", str(min))

            StartY = 26 - round(self.__height/2)
            self.__enterCode = self.__enterCode.replace("!!!StartY!!!", str(StartY))
            self.__enterCode = self.__enterCode.replace("!!!Height!!!", str(self.__height-1))
            self.__enterCode = self.__enterCode.replace("!!!MaxFrames!!!", str(self.__frameNum-1))


        self.__convertedPlayfield = self.convertPixelsToPlayfield("TestPlayfield")
        if self.__kernel in ["common"]:
            self.__convertedPlayfield += self.addColors("TestPlayfield")

        if self.__kernel == "common":
            self.__convertedSpite = self.convertPixelsToSpriteFrameLine("TestSprite")



        self.__mainCode = self.__mainCode.replace("!!!TV!!!", self.__tv)
        self.__mainCode = self.__mainCode.replace("!!!ENTER_BANK2!!!", self.__enterCode)
        self.__mainCode = self.__mainCode.replace("!!!OVERSCAN_BANK2!!!", self.__overScanCode)
        self.__mainCode = self.__mainCode.replace("!!!KERNEL_DATA!!!", (self.__convertedPlayfield+"\n\n"+self.__convertedSpite))
        self.__mainCode = re.sub(r"!!![a-zA-Z0-9_]+!!!", "", self.__mainCode)



        self.doSave("temp/")
        assembler = Assembler(self.__loader, "temp/", True, self.__tv, False)


    def convertPixelsToSpriteFrameLine(self, name):
        max = self.__height * self.__frameNum
        spriteNum = 0
        counter = 0

        spriteLines = []
        spriteColorLines = []
        tempLines = []

        for num in range(0, max):

            text = "\tbyte\t#%"+("".join(self.__spritePixels[spriteNum][num-(self.__height*spriteNum)]))

            tempLines.insert(0, text)

            if counter == self.__height-1:
                from copy import deepcopy

                tempLines[0]+="\t; ("+str(spriteNum)+")"
                spriteNum += 1

                #tempLines.insert(0, "\tbyte\t#%00000000"+"\t; ("+str(spriteNum)+")")


                counter = 0
                spriteLines.extend(deepcopy(tempLines))
                tempLines = []
            else:
                counter+=1

        for num in range(0, self.__height):
            spriteColorLines.insert(0, "\tbyte\t#"+self.__spriteColors[num])

        spriteData = "\talign\t256\n"+name+"_Sprite"+'\n'+("\n".join(spriteLines))+"\n"

        if len(spriteLines) + len(spriteColorLines)>256:
            spriteData+="\talign\t256"

        spriteData += "\n"+name+"_SpriteColor"+'\n'+("\n".join(spriteColorLines))+"\n"

        spriteData = self.__reAlignDataSection(spriteData)

        return spriteData


    def setPFandBGfromFiles(self, pfName, bgName, bgColor):
        from copy import deepcopy

        self.__pixelData = []
        self.__colorData = []

        self.__max = 42
        self.__pfData = None
        self.__bgData = None
        blank = self.__loader.dictionaries.getWordFromCurrentLanguage("blank")

        if pfName != blank:
            self.__pfData = open(self.__loader.mainWindow.projectPath+"playfields/"+pfName+".a26").read().replace("\r","").split("\n")[2:]
            self.__max = int(open(self.__loader.mainWindow.projectPath+"playfields/"+pfName+".a26").read().replace("\r","").split("\n")[1])
            if self.__max<42:
                self.__max = 42

        if bgName != blank:
            self.__bgData = open(self.__loader.mainWindow.projectPath+"backgrounds/"+bgName+".a26").read().replace("\r","").split("\n")[2].split(" ")
            thisMax = int(open(self.__loader.mainWindow.projectPath+"backgrounds/"+bgName+".a26").read().replace("\r","").split("\n")[1])
            if thisMax<self.__max:
                self.__max = thisMax

       # print(self.__max, len(self.__pfData), len(self.__bgData))
       # print(self.__pfData)
       # print(self.__bgData)

        emptyRow = []
        for num in range(0,40):
            emptyRow.append("0")

        for num in range(0, self.__max):
            if pfName != blank:
                row = self.__pfData[num].split(" ")
                self.__pixelData.append(deepcopy(row[:-1]))
                self.__colorData.append([row[-1]])
            else:
                self.__pixelData.append(deepcopy(emptyRow))
                self.__colorData.append([bgColor])

            if bgName == blank:
                self.__colorData[num].append(bgColor)
            else:
                self.__colorData[num].append(self.__bgData[num])



    def doSave(self, projectPath):
        import os

        if projectPath == "temp/":
            try:
                os.mkdir(projectPath+"bin/")
                os.mkdir(projectPath+"asm_log/")
            except:
                pass

        file = open(projectPath+"/source.asm", "w")
        file.write(self.__mainCode)
        file.close()




    def addColors(self, name):

        temp1 = []
        temp2 = []

        counter = 0
        while counter<self.__max:
            temp1.insert(0, "\tbyte\t#"+self.__colorData[counter][0]+"\n")
            temp2.insert(0, "\tbyte\t#"+self.__colorData[counter][1]+"\n")

            counter += 1

        return(name + "_FG\n"+"".join(temp1)+"\n"+name + "_BG\n"+"".join(temp2)+"\n")



    def convertPixelsToPlayfield(self, name):
        pfText = ""

        pf0 = []
        pf1 = []
        pf2 = []
        pf3 = []
        pf4 = []

        counter = 0
        while counter<self.__max:
            # pf1 and pf3 is reversed I guess.
            line = self.__pixelData[counter]

            pf0.insert(0, "\tbyte\t#%"+("".join(line[0:4]))[::-1]+"0000\n")
            pf1.insert(0, "\tbyte\t#%"+("".join(line[4:12]))+"\n")
            pf2.insert(0, "\tbyte\t#%"+("".join(line[12:20]))[::-1]+"\n")

            if self.__mirrored[2] == 0:
                pf3.insert(0, "\tbyte\t#%" + ("".join(line[20:28]))[::-1] + "\n")

            if self.__mirrored[1] == 0:
                pf4.insert(0, "\tbyte\t#%" + "".join(line[28:36]) + "\n")

            if self.__mirrored[0] == 0:
                pf0[0] = pf0[0][:-5] + ("".join(line[36:40])) + "\n"

            counter+=1

        pf0 = name+"_00\n"+"".join(pf0)
        pf1 = name+"_01\n"+"".join(pf1)
        pf2 = name+"_02\n"+"".join(pf2)

        if self.__mirrored[2] == 0:
            pf3 = name+"_03\n"+"".join(pf3)

        if self.__mirrored[1] == 0:
            pf4 = name+"_04\n"+"".join(pf4)


        pfText = pf0 + "\n" + pf1 + "\n"+pf2+"\n"
        if self.__mirrored[2] == 0:
            pfText += pf3 + "\n"

        if self.__mirrored[1] == 0:
            pfText += pf4 + "\n"

        return(pfText)


#if __name__ == "__main__":
#   c = Compiler(None, None, "dummy" ,None)
#   c.preAlign(open("F:\PyCharm\P\Fortari2600\projects\zerg\\bigSprites\Bird.asm", "r").read())
#   for num in range(1, 32):
#        print(num, "-",c.getClosestPowerOf2Minus1(num))
