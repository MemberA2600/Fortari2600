from tkinter import *

class ChannelChangerButton:

    def __init__(self, loader, font, num, variable, w, frame):
        self.__loader = loader
        self.var = variable
        self.num = num

        self.__button = Button(frame, text=str(num), font=font,
                               width = w,
                               bg=self.__loader.colorPalettes.getColor("window"),
                               fg=self.__loader.colorPalettes.getColor("font"),
                               command = self.changeVar, state = DISABLED
                               )
        self.__button.pack_propagate(False)
        self.__button.pack(side=LEFT, fill=Y)

    def changeVar(self):
        self.var[0] = self.num

    def enable(self):
        self.__button.config(state=NORMAL)