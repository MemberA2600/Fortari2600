from tkinter import *
from threading import Thread
from MainMenuLabel import MainMenuLabel
from FrameWithLabelAndEntry import FrameWithLabelAndEntry

class StatusFrame:

    def __init__(self, frame, loader):
        self.__container = frame
        self.__loader = loader

        self.__w = round(self.__container.winfo_width()/2)
        self.__h = self.__container.winfo_height()

        self.stopThread = False
        self.__loader.stopThreads.append(self)

        self.__lastScaleX = self.__loader.frames["MemorySetter"].getScales()[0]
        self.__lastScaleY = self.__loader.frames["MemorySetter"].getScales()[1]

        self.__thisFrame = Frame(self.__container, width=self.__w, height=self.__h)
        self.__thisFrame.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__thisFrame.pack_propagate(False)
        self.__thisFrame.pack(side=LEFT, anchor=NW)

        self.__loader.frames["StatusFrame"] = self
        self.__statusLabel = MainMenuLabel(self.__thisFrame, self.__loader, "freeMemory", 14, "MemorySetter")
        self.statusBasicRam = FrameWithLabelAndEntry(self.__thisFrame, loader, "basicRam", 10, 15, RIGHT)
        self.statusSaraRam = FrameWithLabelAndEntry(self.__thisFrame, loader, "saraRam", 10, 15, RIGHT)
        self.statusBasicRam.disable()
        self.statusSaraRam.disable()

        self.__selectedValidity = self.__loader.listBoxes["bankBox"].getSelectedName()

        if self.__selectedValidity != "bank1":
            self.statusBasicRamLocal = FrameWithLabelAndEntry(self.__thisFrame, loader, "basicRamLocal", 10, 15, RIGHT)
            self.statusSaraRamLocal = FrameWithLabelAndEntry(self.__thisFrame, loader, "saraRamLocal", 10, 15, RIGHT)
            self.statusBasicRamLocal.disable()
            self.statusSaraRamLocal.disable()

        self.calculateFreeRAM()

        self.__loader.frames["statusFrame"] = self

        t = Thread(target=self.resize)
        t.daemon=True
        t.start()

    def resize(self):
        from time import sleep
        while self.__loader.mainWindow.dead==False and self.__container!=None and self.stopThread==False:
            if (self.__lastScaleX != self.__loader.frames["MemorySetter"].getScales()[0] or
                    self.__lastScaleY != self.__loader.frames["MemorySetter"].getScales()[1]):
                self.__lastScaleX = self.__loader.frames["MemorySetter"].getScales()[0]
                self.__lastScaleY = self.__loader.frames["MemorySetter"].getScales()[1]

                if self.__thisFrame!=None:
                    try:
                        self.__thisFrame.config(width=self.__w * self.__lastScaleX,
                                     height=self.__h * self.__lastScaleY)
                    except Exception as e:
                        self.__loader.logger.errorLog(e)

            sleep(0.04)

    def calculateFreeRAM(self):
        basic = 0
        sara = 0
        basicLocal = 0
        saraLocal = 0
        for address in self.__loader.virtualMemory.memory.keys():
            if len(address) == 3:
                basic+=len(self.__loader.virtualMemory.memory[address].freeBits["global"])
                if self.__selectedValidity != "bank1":
                    basicLocal += len(self.__loader.virtualMemory.memory[address].freeBits[self.__selectedValidity])
            else:
                sara+=len(self.__loader.virtualMemory.memory[address].freeBits["global"])
                if self.__selectedValidity != "bank1":
                    saraLocal += len(self.__loader.virtualMemory.memory[address].freeBits[self.__selectedValidity])

        self.statusBasicRam.setEntry(self.calculate(basic))
        self.statusSaraRam.setEntry(self.calculate(sara))
        if self.__selectedValidity != "bank1":
            self.statusBasicRamLocal.setEntry(self.calculate(basicLocal))
            self.statusSaraRamLocal.setEntry(self.calculate(saraLocal))

    def calculate(self, number):
        bytes = number//8
        bits = number%8
        if bytes==1:
            text= "1 byte"
        else:
            text=str(bytes)+" bytes"

        if bits>0:
            if bits == 1:
                text+="; 1 bit"
            else:
                text+="; "+str(bits)+ " bits"

        return(text)
