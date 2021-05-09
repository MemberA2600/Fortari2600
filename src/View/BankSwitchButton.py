from tkinter import *
from threading import Thread

class BankSwitchButton:

    def __init__(self, loader, frame, num):
        self.__loader = loader
        self.__frame = frame

        self.__num = num
        self.__button = Button(self.__frame, command=self.selectOnBoxes)

        self.stopThread = False
        self.__loader.stopThreads.append(self)

        if num == 1:
            self.__button.config(text="Global")
        else:
            self.__button.config(text="Bank"+str(num))


        self.__scaleLastX = self.__loader.mainWindow.getScales()[0]
        self.__scaleLastY = self.__loader.mainWindow.getScales()[1]

        self.getFont()

        self.__button.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__button.config(fg=self.__loader.colorPalettes.getColor("font"))
        self.__button.pack(side=LEFT, anchor=SE, fill=Y)

        self.__loader.destroyable.append(self.__button)

        t = Thread(target=self.resizer)
        t.daemon=True
        t.start()

    def selectOnBoxes(self):
        self.__loader.BFG9000.selectOnBoxes(self.__num)

    def getFont(self):
        if (self.__loader.mainWindow.dead==False and
            self.__frame != None and self.stopThread==False):
            self.__fontSize = ((self.__frame.winfo_height()/100)*20
                               )
            self.__font = self.__loader.fontManager.getFont(round(self.__fontSize), False, False, False)
            if self.__button!=None:
                try:
                    self.__button.config(font=self.__font)
                except Exception as e:
                    self.__loader.logger.errorLog(e)

    def resizer(self):
        from time import sleep
        while (self.__loader.mainWindow.dead==False and
            self.__frame != None and self.__button!=None and self.stopThread==False):

            if (self.__scaleLastX!=self.__loader.mainWindow.getScales()[0] or
                self.__scaleLastY != self.__loader.mainWindow.getScales()[1]):

                self.__scaleLastX = self.__loader.mainWindow.getScales()[0]
                self.__scaleLastY = self.__loader.mainWindow.getScales()[1]

                self.getFont()
            sleep(0.04)