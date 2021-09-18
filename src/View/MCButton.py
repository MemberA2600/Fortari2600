from tkinter import *

class MCButton:

    def __init__(self, loader, frame, image, w, function):

        self.__loader = loader
        self.__image = image

        self.__colors = self.__loader.colorPalettes
        self.__img = self.__loader.io.getImg(self.__image, None)


        self.__button = Button(
            frame, width=w,
            bg=self.__colors.getColor("window"),
            image = self.__img,
            command = function,
            state = DISABLED
        )

        self.__button.pack_propagate(False)
        self.__button.pack(side=RIGHT, anchor = E)

    def changeState(self, n):
        if n == True:
            self.__button.config(state = NORMAL)
        else:
            self.__button.config(state = DISABLED)
