from tkinter import *

class RoboButton:

    def __init__(self, loader, name, motherFrame, w, h, values, entries, outFunc):
        self.__loader = loader

        self.__values = values
        self.__entries = entries

        self.__frame = Frame(motherFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                width = w,
                                height= h)
        self.__frame.pack_propagate(False)
        self.__frame.pack(side=LEFT, anchor=E, fill=Y)

        self.__img = self.__loader.io.getImg("robo_"+name, None)

        self.__button = Button(self.__frame, bg=self.__loader.colorPalettes.getColor("window"),
                                   name="openSound",
                                   image=self.__img, width=999999999, command=self.__setData)
        self.__button.pack_propagate(False)
        self.__button.pack(fill=BOTH)

        self.__outFunc = outFunc

    def __setData(self):
        for num in range(0, len(self.__entries)):
            self.__entries[num].var.set(str(self.__values[num]))

        self.__outFunc()