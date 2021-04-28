from tkinter import *
from threading import Thread

class RightFrame:

    def __init__(self, loader, frame):
        self.__loader = loader
        self.__frame = frame

        self.__fontManager = loader.fontManager
        baseSize=18

        self.__fontNormalSize = ((self.__loader.screenSize[0]/1350) *
                            (self.__loader.screenSize[1]/1100) * baseSize
                           )

        self.__fontSmallSize = ((self.__loader.screenSize[0]/1350) *
                            (self.__loader.screenSize[1]/1100) * baseSize * 0.75
                           )

        self.__lastX = self.__loader.mainWindow.getScales()[0]
        self.__lastY = self.__loader.mainWindow.getScales()[1]

        self.setFonts()

        self.__labelVariables = Label(self.__frame, font=self.__fontNormal,
                                      text=self.__loader.dictionaries.getWordFromCurrentLanguage("variables"))

        self.__labelVariables.pack(side=TOP, anchor=NW)

        t = Thread(target=self.scaler)
        t.daemon = True
        t.start()

    def setFonts(self):
        self.__fontNormal = self.__loader.fontManager.getFont(
            round(self.__fontNormalSize * self.__lastX * self.__lastY),
            False, False, False)
        self.__fontSmall = self.__loader.fontManager.getFont(round(self.__fontSmallSize * self.__lastX * self.__lastY),
                                                             False, False, False)

    def scaler(self):
        from time import sleep
        while self.__loader.mainWindow.dead==False:
            if (self.__lastX!=self.__loader.mainWindow.getScales()[0] or
                self.__lastY != self.__loader.mainWindow.getScales()[1]
            ):
                self.__lastX = self.__loader.mainWindow.getScales()[0]
                self.__lastY = self.__loader.mainWindow.getScales()[1]
                self.setFonts()

                try:
                    self.__labelVariables.config(font=self.__fontNormal)
                except Exception as e:
                    self.__loader.logger.errorLog(e)

            sleep(0.04)
