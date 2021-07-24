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
            self.__openEmulator = True

            self.__mainCode = self.__io.loadKernelElement(self.__kernel, "main_kernel")
            self.__enterCode = self.__io.loadTestElement(self.__mode, self.__kernel, "enter")
            self.__overScanCode = self.__io.loadTestElement(self.__mode, self.__kernel, "overscan")

            self.__pixelData = data[0]
            self.__colorData = data[1]
            self.__max = int(data[2])

            if self.__kernel == "common":
                self.__mirrored = [0,1,1]

            self.__convertedPlayfield = self.convertPixelsToPlayfield("TestPlayfield")
            if self.__kernel in ["common"]:
                self.__convertedPlayfield += self.addColors("TestPlayfield")

            self.__overScanCode.replace("!!!Max!!!", str(self.__max))
            self.__mainCode = self.__mainCode.replace("!!!ENTER_BANK2!!!", self.__enterCode)
            self.__mainCode = self.__mainCode.replace("!!!OVERSCAN_BANK2!!!", self.__overScanCode)
            self.__mainCode = self.__mainCode.replace("!!!KERNEL_DATA!!!", self.__convertedPlayfield)
            self.__mainCode = re.sub(r"!!![a-zA-Z0-9_]+!!!","", self.__mainCode)

            self.doSave("temp/")

    def doSave(self, projectPath):
        pass

    def addColors(self, name):

        temp1 = []
        temp2 = []

        counter = 0
        while counter<self.__max:
            temp1.insert(0, "\tbyte\t#"+self.__colorData[counter][0]+"\n")
            temp2.insert(0, "\tbyte\t#"+self.__colorData[counter][1]+"\n")

            counter += 1

        return(name + "__FG\n"+"".join(temp1)+"\n"+name + "__BG\n"+"".join(temp2)+"\n")



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

            pf0.insert(0, "\tbyte\t#%"+"".join(line[0:4])+"0000\n")
            pf1.insert(0, "\tbyte\t#%"+("".join(line[4:12]))[::-1]+"\n")
            pf2.insert(0, "\tbyte\t#%"+"".join(line[12:20])+"\n")

            if self.__mirrored[2] == 0:
                pf3.insert(0, "\tbyte\t#%" + ("".join(line[20:28]))[::-1] + "\n")

            if self.__mirrored[1] == 0:
                pf4.insert(0, "\tbyte\t#%" + "".join(line[28:36]) + "\n")

            if self.__mirrored[0] == 0:
                pf0[0] = pf0[0][:-5] + "".join(line[36:40]) + "\n"

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

