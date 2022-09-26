from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from time import sleep

from ScreenSetterFrameBase import ScreenSetterFrameBase

class Reseter:

    def __init__(self, loader, baseFrame, data, changeName, changeData, w, h, currentBank, blankAnimation, topLevelWindow, itemNames):
        self.__loader = loader
        self.__baseFrame = baseFrame
        self.__data = data.split(" ")
        self.__w = w
        self.__h = h
        self.__currentBank = currentBank

        self.__changeData = changeData

        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs
        self.__fontManager = self.__loader.fontManager
        self.__fontSize = int(self.__screenSize[0] / 1300 * self.__screenSize[1] / 1050 * 14)
        self.__colors = self.__loader.colorPalettes
        self.__colorDict = self.__loader.colorDict

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize * 0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize * 0.65), False, False, False)
        self.__bigFont = self.__fontManager.getFont(int(self.__fontSize * 1.15), False, False, False)
        self.__bigFont2 = self.__fontManager.getFont(int(self.__fontSize * 1.5), False, False, False)

        self.__name = StringVar()
        self.__name.set(self.__data[0])
        self.dead = [False]
        self.__entered = None
        self.__lastData = self.__data[2]

        self.__setterBase = ScreenSetterFrameBase(loader, baseFrame, data, self.__name, changeName, self.dead,
                                                  itemNames)
        self.__addElements()

    def __addElements(self):
        self.__uniqueFrame = Frame(self.__baseFrame, width=self.__w,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h)

        self.__uniqueFrame.pack_propagate(False)
        self.__uniqueFrame.pack(side=TOP, anchor=N, fill=X)

        self.__init = Label(self.__uniqueFrame,
                      text=self.__dictionaries.getWordFromCurrentLanguage("initialize"),
                      font=self.__bigFont2, fg=self.__colors.getColor("font"),
                      bg=self.__colors.getColor("window"), justify=CENTER
                      )

        self.__init.pack_propagate(False)
        self.__init.pack(side=TOP, anchor=CENTER, fill=X)

        self.__frame1 = Frame(self.__uniqueFrame, width=self.__w // 2,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h)

        self.__frame1.pack_propagate(False)
        self.__frame1.pack(side=LEFT, anchor=E, fill=Y)

        self.__frame2 = Frame(self.__uniqueFrame, width=self.__w // 2,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h)

        self.__frame2.pack_propagate(False)
        self.__frame2.pack(side=LEFT, anchor=E, fill=Y)

        self.__label1 = Label(self.__frame1,
                      text=self.__dictionaries.getWordFromCurrentLanguage("frameColor"),
                      font=self.__bigFont, fg=self.__colors.getColor("font"),
                      bg=self.__colors.getColor("window"), justify=CENTER
                      )

        self.__label1.pack_propagate(False)
        self.__label1.pack(side=TOP, anchor=CENTER, fill=X)

        self.__label2 = Label(self.__frame2,
                      text=self.__dictionaries.getWordFromCurrentLanguage("zero") + ":",
                      font=self.__bigFont, fg=self.__colors.getColor("font"),
                      bg=self.__colors.getColor("window"), justify=CENTER
                      )

        self.__label2.pack_propagate(False)
        self.__label2.pack(side=TOP, anchor=CENTER, fill=X)

        toZero              = ["GRP0", "GRP1", "ENAM0", "ENAM1", "ENABL", "PF0", "PF1", "PF2", "HMCLR"]
        toFrameColor        = ["COLUPF", "COLUBK", "COLUP0", "COLUP1"]

        self.__checkBoxes   = {}

        counter = 1

        for item in toZero:
            counter += 1
            value = int(self.__data[counter])

            self.__checkBoxes[item] = {}

            d = IntVar()
            d.set(value)

            c = Checkbutton(self.__frame1,
                                         text = self.__dictionaries.getWordFromCurrentLanguage(item),
                                         name = item.lower(),
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__normalFont,
                                         variable=d,
                                         activebackground=self.__colors.getColor("highLight"),
                                         command=self.__checkPressed
                                         )

            c.pack_propagate(False)
            c.pack(fill=X, side=TOP, anchor=CENTER)

            c.bind("<Enter>", self.__enter)

            self.__checkBoxes[item]["value"]    = d
            self.__checkBoxes[item]["box"]      = c

        for item in toFrameColor:
            counter += 1
            value = int(self.__data[counter])

            self.__checkBoxes[item] = {}

            d = IntVar()
            d.set(value)

            c = Checkbutton(self.__frame2,
                            text=self.__dictionaries.getWordFromCurrentLanguage(item),
                            name=item.lower(),
                            bg=self.__colors.getColor("window"),
                            fg=self.__colors.getColor("font"),
                            justify=LEFT, font=self.__normalFont,
                            variable=d,
                            activebackground=self.__colors.getColor("highLight"),
                            command=self.__checkPressed
                            )

            c.pack_propagate(False)
            c.pack(fill=X, side=TOP, anchor=CENTER)

            c.bind("<Enter>", self.__enter)

            self.__checkBoxes[item]["value"] = d
            self.__checkBoxes[item]["box"] = c

    def __checkPressed(self):
        index = ["GRP0", "GRP1", "ENAM0", "ENAM1", "ENABL", "PF0", "PF1", "PF2",
                 "HMCLR", "COLUPF", "COLUBK", "COLUP0", "COLUP1"].index(self.__entered) + 2

        self.__data[index] = str(self.__checkBoxes[self.__entered]["value"].get())
        self.__changeData(self.__data)

    def __enter(self, event):
        self.__entered = str(event.widget).split(".")[-1].upper()
