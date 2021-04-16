from tkinter import *

class SubMenuEntryWithButton:

    def __init__(self, master, loader, font):
        self.__loader = loader
        self.__var = StringVar()
        self.__font = font
        self.__master = master
        self.__entryFrame = Frame(master.getTopLevel(),
                                  width=master.getTopLevelDimensions()[0],
                                  height=self.__font.metrics('linespace'))
        self.__entryFrame.place()
        self.__entryFrame.pack(side=TOP, anchor=NW)
        self.__entryFrame.pack_propagate(False)

        self.__entry = Entry(self.__entryFrame,
                             width=999,
                             textvariable=self.__var,
                             font=self.__font)
        self.__entry.pack(side=LEFT, anchor=W)


    def enabled(self, bool):
        if bool == True:
            self.__entry.config(state = NORMAL)
        else:
            self.__entry.config(state = DISABLED)
            self.__var = ""

    def getText(self):
        return(self.__var.get())

    def setText(self,text):
        self.__var.set(text)

    def addButton(self, name, function):
        self.__img = self.__loader.getImg(name, self.__font.metrics('linespace')-5)
        self.__button = Button(self.__entryFrame, image=self.__img, command = function)
        self.__entry.config(width=self.__loader.fontManager.getCharacterLenghtFromPixels(
            self.__font,
            self.__master.getTopLevelDimensions()[0]-self.__loader.getConstant()
        ))
        self.__button.pack(fill=Y, side=RIGHT, anchor=E)