from threading import Thread
from tkinter import *

class SelectLabel:

    def __init__(self, loader, frame, text, fontmanager):
        self.__loader = loader

        self.__frame = frame
        self.__fontManager = fontmanager

        self.stopThread = False
        self.__loader.stopThreads.append(self)

        self.__contentHolder = self.__frame.getFrame()
        self.__label = Label(self.__contentHolder, text=text)

        self.__font = None
        self.__lastScaleX = self.__loader.mainWindow.getScales()[0]
        self.__lastScaleY = self.__loader.mainWindow.getScales()[1]
        self.__label.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__label.config(fg=self.__loader.colorPalettes.getColor("font"))

        #align = Thread(target=self.dinamicallyAlign)
        #align.daemon = True
        #align.start()
        self.__setFont()

        self.__label.pack(side=TOP, anchor=W)

    def __setFont(self):
        self.__font = self.__fontManager.getFont("normal", False, False, False)
        self.__label.config(font=self.__font)