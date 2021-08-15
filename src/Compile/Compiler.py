import re
from Assembler import Assembler

class Compiler:

    def __init__(self, loader, kernel, mode, data):

        self.__loader = loader
        self.__kernel = kernel
        self.__mode = mode
        self.__data = data
        self.__openEmulator = False
        self.__io = self.__loader.io

        if self.__mode == "pfTest":
            self.pfTest()
        elif self.__mode == "spriteTest" or self.__mode == "tileSetTest":
            self.spriteTest()
        elif self.__mode == "kernelTest":
            self.kernelTest()

    def kernelTest(self):
        self.__openEmulator = True

        self.__mainCode = self.__data[0]
        self.__enterCode = self.__data[1]
        self.__overScanCode = self.__data[2]
        self.__kernelData = self.__data[3]

        self.__mainCode = self.__mainCode.replace("!!!TV!!!", "NTSC")
        self.__mainCode = self.__mainCode.replace("!!!ENTER_BANK2!!!", self.__enterCode)
        self.__mainCode = self.__mainCode.replace("!!!OVERSCAN_BANK2!!!", self.__overScanCode)
        self.__mainCode = self.__mainCode.replace("!!!KERNEL_DATA!!!", self.__kernelData)
        self.__mainCode = re.sub(r"!!![a-zA-Z0-9_]+!!!", "", self.__mainCode)


        self.doSave("temp/")
        assembler = Assembler(self.__loader, "temp/", True, "NTSC", False)

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

