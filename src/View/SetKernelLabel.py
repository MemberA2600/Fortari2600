from tkinter import *

class SetKernelLabel:

    def __init__(self, loader, master, container, h, font):
        self.__loader = loader
        self.__master = master
        self.__container = container

        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs
        self.__fontManager = self.__loader.fontManager

        self.__frame = Frame(container.getTopLevel(), width=9999999, height = h)
        self.__frame.pack_propagate(False)
        self.__frame.pack(side=TOP, anchor=N, fill=X)
        self.__frame.config(bg=self.__loader.colorPalettes.getColor("window"))

        self.__label = Label(self.__frame, text = str(self.__dictionaries.getWordFromCurrentLanguage("kernelType")+" "), font=font)
        self.__label.pack(side=LEFT, anchor=W, fill=Y)

        self.optionValue = StringVar()
        self.optionValue.set("common")
        self.__option = OptionMenu(self.__frame, self.optionValue, tuple(self.__loader.virtualMemory.kernel_types))
        self.__option.config(font=font)
        self.__option.pack(side=LEFT, anchor=E, fill=BOTH)