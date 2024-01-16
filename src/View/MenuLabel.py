from threading import Thread
from tkinter import Label

class MenuLabel:

    def __init__(self, loader, frame, text, XPoz, fontmanager):
        self.__loader = loader

        self.__frame = frame
        self.__XPoz = XPoz
        self.__fontManager = fontmanager

        self.stopThread = False
        self.__loader.stopThreads.append(self)

        self.__label = Label(self.__frame, text = text)

        self.__font = None
        self.__lastScaleX = self.__loader.mainWindow.getScales()[0]
        self.__lastScaleY = self.__loader.mainWindow.getScales()[1]
        self.__label.config(bg=self.__loader.colorPalettes.getColor("window"))


        self.dead = False
        self.__placer()
        self.__setFont()

    def __placer(self):
        c = self.__loader.mainWindow.getConstant()
        try:

            x = (self.__loader.mainWindow.getConstant()*self.__XPoz*1.5)+ 5
            y = c*1.04+12

            self.__label.place(x=x, y = y)
        except Exception as e:
            print(str(e))

    def __setFont(self):
        self.__font = self.__fontManager.getFont("normal", False, False, False)
        self.__label.config(font=self.__font)

    def setText(self, string):
        self.__label.config(text=string)

    def changePlace(self, num):
        self.__XPoz = num
        self.__placer()

    def changeColor(self, color):
        self.__label.config(fg=color)