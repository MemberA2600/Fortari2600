from tkinter import *
from threading import Thread

class LeftFrameSetterFrame:

    def __init__(self, loader, frame, title, father, height, baseSize, val, view):
        self.__loader = loader
        self.__frame = frame
        self.__father = father
        self.__baseSize = baseSize
        self.__height=height
        self.__bank=val
        self.__section=view

        self.stopThread = False
        self.__loader.stopThreads.append(self)

        self.__h = self.__frame.winfo_height()*height

        self.__originalW = self.__frame.winfo_width()
        self.__originalH = self.__frame.winfo_height()

        self.__thisFrame = Frame(self.__frame, height=round(self.__h))
        self.__thisFrame.config(bg=self.__loader.colorPalettes.getColor("window"))

        self.__thisFrame.pack_propagate(False)
        self.__thisFrame.pack(side=TOP, anchor=NW, fill=X)

        self.__title = Label(self.__thisFrame, text = self.__loader.dictionaries.getWordFromCurrentLanguage(title))
        self.setFont()
        self.__title.config(font=self.__font)
        self.__title.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__title.config(fg=self.__loader.colorPalettes.getColor("font"))
        self.__title.pack(side=LEFT, anchor=NW, fill=X)

        self.__lastX = self.__father.getScales()[0]
        self.__lastY = self.__father.getScales()[1]

        t = Thread(target=self.sizing)
        t.daemon = True
        t.start()

    def setFont(self):
        w = self.__father.getSizes()[0]/640
        h = self.__father.getSizes()[1]/320
        self.__fontSize = (self.__baseSize*w*h)
        self.__font = self.__loader.fontManager.getFont(round(self.__fontSize), False, False, False)

    def sizing(self):
        from time import sleep
        while self.__loader.mainWindow.dead==False and self.stopThread==False:
            if (self.__lastX != self.__father.getScales()[0] or
                self.__lastY != self.__father.getScales()[1]
            ):
                self.__lastX = self.__father.getScales()[0]
                self.__lastY = self.__father.getScales()[1]

                self.__h = self.__frame.winfo_height() * self.__height
                self.__thisFrame.config(height=round(self.__h))
                self.setFont()
                self.__title.config(font=self.__font)

            sleep(0.04)