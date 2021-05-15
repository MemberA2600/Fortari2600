from tkinter import *
from MainMenuLabel import MainMenuLabel
from threading import Thread

class SwitchFrame:

    def __init__(self, container, loader):
        self.__loader = loader
        self.__container = container

        self.__w = self.__container.winfo_width()
        self.__h = round(self.__container.winfo_height()/10)

        self.stopThread = False
        self.__loader.stopThreads.append(self)


        self.__scaleLastX = self.__loader.frames["MemorySetter"].getScales()[0]
        self.__scaleLastY = self.__loader.frames["MemorySetter"].getScales()[1]

        self.__thisFrame = Frame(self.__container, width=self.__w, height=self.__h)
        self.__thisFrame.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__thisFrame.pack_propagate(False)
        #self.__thisFrame.place(x=5, y=5+self.__loader.frames["MemorySetter"].title.getH())
        self.__thisFrame.pack(side=TOP, fill=X, anchor=NE)

        self.__fastSwitch = MainMenuLabel(self.__thisFrame, self.__loader, "fastSwitching", 20, "MemorySetter")

        from BankSwitchButton import BankSwitchButton
        self.__bankSwitchButtons = []
        for num in range(1, 9):
            self.__bankSwitchButtons.append(BankSwitchButton(self.__loader,
                                                             self.__thisFrame, num))

        #for key in self.__loader.listBoxes.keys():
        #    print(key)

        self.__loader.frames["SwitchFrame"] = self

        t = Thread(target=self.resizer)
        t.daemon=True
        t.start()

    def getH(self):
        return(self.__thisFrame.winfo_height())

    def resizer(self):
        from time import sleep
        while (self.__loader.mainWindow.dead==False and
            self.__container != None and self.__thisFrame!=None
            and self.stopThread==False
        ):

            if (self.__scaleLastX!=self.__loader.frames["MemorySetter"].getScales()[0] or
                self.__scaleLastY != self.__loader.frames["MemorySetter"].getScales()[1]):

                self.__scaleLastX = self.__loader.frames["MemorySetter"].getScales()[0]
                self.__scaleLastY = self.__loader.frames["MemorySetter"].getScales()[1]

                try:
                    self.__thisFrame.config(
                        width=self.__w * self.__scaleLastX,
                        height=self.__h * self.__scaleLastY,
                    )
                except Exception as e:
                    self.__loader.logger.errorLog(e)
            #self.__thisFrame.place(x=5, y=5 + self.__loader.frames["MemorySetter"].title.getH())
            sleep(0.04)