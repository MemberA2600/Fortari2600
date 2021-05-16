from tkinter import *
from threading import Thread

class LeftFrameEditor:

    def __init__(self, loader, frame, validity, view):
        self.__loader = loader
        self.__frame = frame

        self.stopThread = False
        self.__loader.stopThreads.append(self)

        self.stopThread = False
        self.__loader.stopThreads.append(self)

        self.__originalW = self.__frame.winfo_width()
        self.__originalH = self.__frame.winfo_height()
        self.__loader.frames["leftFrame"] = self

        from LeftFrameSetterFrame import LeftFrameSetterFrame
        self.__delimiterSetter = LeftFrameSetterFrame(self.__loader,
                                 self.__frame, "deliminatorSetter", self, 0.20, 20,
                                validity, view)


        t = Thread(target=self.sizing)
        t.daemon = True
        t.start()


    def sizing(self):
        from time import sleep
        while self.__loader.mainWindow.dead == False and self.stopThread==False:

            sleep(0.04)


    def getScales(self):
        return(
            self.__frame.winfo_width()/self.__originalW,
            self.__frame.winfo_height() / self.__originalH,
        )

    def getSizes(self):
        return(
            self.__frame.winfo_width(), self.__frame.winfo_height()
        )