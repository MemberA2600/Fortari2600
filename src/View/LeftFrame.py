from tkinter import *

class LeftFrame:

    def __init__(self, loader, frame):
        self.stopThread = False
        self.__loader.stopThreads.append(self)


    def getScales(self):
        return(
            self.__frame.winfo_width()/self.__originalW,
            self.__frame.winfo_height() / self.__originalH,
        )