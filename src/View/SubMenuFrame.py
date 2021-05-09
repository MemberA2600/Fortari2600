from tkinter import *

class SubMenuFrame:
    def __init__(self, loader, master, container, w):
        self.__loader = loader
        self.__master = master
        self.__container = container
        self.__width = w
        self.__frame = Frame(self.__container, width=self.__width,
                             bg=self.__loader.colorPalettes.getColor("window"))

        self.__frame.pack_propagate(False)
        self.__frame.grid_propagate(False)
        self.__frame.pack(side=LEFT, anchor=W, fill=Y)

    def getFrame(self):
        return(self.__frame)

    def getFrameSize(self):
        return(self.__frame.winfo_width(), self.__frame.winfo_height())

    def getWindowSize(self):
        return(self.getFrameSize())

    def getScales(self):
        return(1,1)
