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
        elif self.__mode == 'music':
            self.generateMusicROM()
        elif self.__mode == 'getMusicBytes':
            self.getMusicBytesSizeOnly()

    def getMusicBytesSizeOnly(self):
        self.banks = len(self.generateSongBytes(self.__data[0], "NTSC"))

    def generateMusicROM(self):
        import re

        self.__picturePath = self.__data[0]
        self.__pathToSave = self.__data[1]

        # valid: mono, stereo, double
        self.__musicMode = "stereo"

        self.__openEmulator = self.__data[2]

        self.__textBytes, self.__charNums = self.generateTextDataFromString(self.__data[3] + " - "+self.__data[4])
        self.__songData = self.generateSongBytes(self.__data[5], "NTSC")

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
        else:
            self.__music1 = None

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

        else:
            self.__music0 = self.__music0.replace("!!!JumpOrReturn!!!",
                                  self.__loader.io.loadWholeText("templates/skeletons/musicJumpNext.asm")
                                  .replace("BANKNEXT", str(self.__banks[1]))
                                  .replace("Cool_Song", CoolSong))
            self.__music1 = self.__music1.replace("!!!JumpOrReturn!!!",
                                  self.__loader.io.loadWholeText("templates/skeletons/musicJumpBack.asm"))

        if self.__musicMode == "mono":
            self.__init += "\n" + "CoolSong_Pointer0 = $e2\nCoolSong_Duration0 = $e4"
            self.__init += "\n" + self.__loader.io.loadWholeText("templates/skeletons/musicInitMono.asm")

        else:
            self.__init += "\n\n" + "CoolSong_Pointer0 = $e2\nCoolSong_Duration0 = $e4\nCoolSong_Pointer1 = $e5\nCoolSong_Duration1 = $e7"

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
        else:
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



        self.doSave("temp/")
        assembler = Assembler(self.__loader, "temp/", True, "NTSC", False)

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
        __music = self.__loader.io.loadWholeText("templates/skeletons/musicEngine.asm")
        __music = __music.replace("@@", str(num))
        __music = __music.replace("CoolSong", title)

        if self.__variables[num*2] == None:
            __music = __music.replace("temp&1", "temp"+str(16+(num*2)))
        else:
            __music = __music.replace("temp&1", self.__variables[num*2])

        if self.__variables[(num*2)+1] == None:
            __music = __music.replace("temp&2", "temp"+str(17+(num*2)))
        else:
            __music = __music.replace("temp&2", self.__variables[(num*2)+1])

        return(__music)



    def generateSongBytes(self, tiaData, tv):
        from TiaNote import TiaNote
        Channels = ["CoolSong_Data0\n", "CoolSong_Data1\n"]
        tempDur = 0

        bytes = [0,0]

        if len(tiaData) == 1:
            Channels.pop(1)
            self.__musicMode = "mono"
        else:
            self.__musicMode = "stereo"

        for num in range(0, len(tiaData)):
            for tiaNote in tiaData[num]:
                firstByte = self.createBits(tiaNote.channel, 4) + self.createBits(tiaNote.volume, 4)

                if tv == 'PAL':
                    duration = int(tiaNote.duration/6*5)
                    tempDur +=tiaNote.duration-duration

                    if tempDur>1:
                        duration+=1
                        tempDur-=1

                else:
                    duration = tiaNote.duration

                if tiaNote.volume == 0:
                    Channels[num] += "\tBYTE\t#0\n\tBYTE\t#%"+self.createBits(duration, 8)+"\n"
                    bytes[num] +=2

                elif duration<8:
                    secondByte = self.createBits(duration, 3) + self.createBits(tiaNote.freq, 5)
                    Channels[num]+="\tBYTE\t#%"+firstByte+"\n\tBYTE\t#%"+secondByte+"\n"

                    bytes[num] +=2
                else:
                    secondByte = self.createBits(tiaNote.freq, 8)
                    thirdByte = self.createBits(duration, 8)

                    Channels[num] += "\tBYTE\t#%" + firstByte + "\n\tBYTE\t#%" + secondByte + "\n"+"\n\tBYTE\t#%" + thirdByte + "\n"
                    bytes[num] += 3


        #print(self.__musicMode)

        Channels[0] += "\tBYTE\t#240\n"
        bytes[0] += 1

        if self.__musicMode != "mono":
            bytes[1] += 1
            Channels[1] += "\tBYTE\t#240\n"

            if bytes[0]>3600 or bytes[1]>3600:
                self.__musicMode = "double"
            else:
                self.__musicMode = "stereo"

        return(Channels)

    def createBits(self, num, l):
        num = int(num)
        num = bin(num)[2:]
        while len(num)<l:
            num = "0"+num
        return(num)

    def generateTextDataFromString(self, text):
        textToReturn = "\talign\t256\nCoolSong_ReallyNiceText\n"
        charNums = []

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

