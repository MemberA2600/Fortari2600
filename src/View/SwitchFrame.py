from tkinter import *
from MainMenuLabel import MainMenuLabel
from threading import Thread

class SwitchFrame:

    def __init__(self, container, loader):
        self.__loader = loader
        self.__container = container

        self.__w = self.__container.winfo_width()
        self.__h = round(self.__container.winfo_height()/10)

        self.__scaleLastX = self.__loader.mainWindow.getScales()[0]
        self.__scaleLastY = self.__loader.mainWindow.getScales()[1]

        self.__thisFrame = Frame(self.__container, width=self.__w, height=self.__h)
        self.__thisFrame.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__thisFrame.pack_propagate(False)
        self.__thisFrame.pack(side=TOP, anchor=E)


        self.__fastSwitch = MainMenuLabel(self.__thisFrame, self.__loader, "fastSwitching", 14)

        from BankSwitchButton import BankSwitchButton
        self.__bankSwitchButtons = []
        for num in range(1, 9):
            self.__bankSwitchButtons.append(BankSwitchButton(self.__loader,
                                                             self.__thisFrame, num))

        #for key in self.__loader.listBoxes.keys():
        #    print(key)


        t = Thread(target=self.resizer)
        t.daemon=True
        t.start()

    def resizer(self):
        from time import sleep
        while (self.__loader.mainWindow.dead==False and
            self.__container != None and self.__thisFrame!=None):

            if (self.__scaleLastX!=self.__loader.mainWindow.getScales()[0] or
                self.__scaleLastY != self.__loader.mainWindow.getScales()[1]):

                self.__scaleLastX = self.__loader.mainWindow.getScales()[0]
                self.__scaleLastY = self.__loader.mainWindow.getScales()[1]

                try:
                    self.__thisFrame.config(
                        width=self.__w * self.__scaleLastX,
                        height=self.__h * self.__scaleLastY,
                    )
                except Exception as e:
                    self.__loader.logger.errorLog(e)

            sleep(0.04)