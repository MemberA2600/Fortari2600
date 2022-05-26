from tkinter import *
from threading import Thread
from copy import deepcopy
from time import sleep
import re

class NUSIZFrame:

    def __init__(self, loader, frame, changeData, h, data, dead, fontSize, dataNum, w, stretch):
        self.__loader        = loader
        self.__mainFrame     = frame
        self.__changeData    = changeData
        self.__h             = round(h * 0.9)
        self.__data          = data
        self.dead            = dead
        self.__dataNum       = dataNum
        self.__w             = w
        self.__stretchOnly   = stretch


        self.__nusizArrange = [
            "100000000",
            "101000000",
            "100010000",
            "101010000",
            "100000001",
            "110000000",
            "100010001",
            "111100000",
        ]

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

        self.__fontSize = fontSize
        self.__fonts = { "normal": self.__smallFont, "small": self.__miniFont}

        self.__canvas = Canvas(self.__mainFrame, bg = self.__colors.getColor("font"), bd=0,
                               width=9999999,
                               height=self.__h // 3)

        self.__canvas.pack_propagate(False)

        self.__entryFrame  = Frame(self.__mainFrame, width=999999,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h // 3)

        self.__entryFrame.pack_propagate(False)
        self.__entryFrame.pack(side=TOP, anchor=N, fill=X)

        self.__value = StringVar()
        self.__entry = Entry(self.__entryFrame,
                                   bg=self.__colors.getColor("boxBackNormal"),
                                   fg=self.__colors.getColor("boxFontNormal"),
                                   width=9999, justify=CENTER,
                                   textvariable=self.__value,
                                   font=self.__smallFont
                                   )

        self.__entry.pack_propagate(False)
        self.__entry.pack(fill=X, side=TOP, anchor=N)
        self.__canvas.pack(side=TOP, anchor=N, fill=X)

        print(self.__data)
        self.__value.set(str(int("0b" + self.__data[self.__dataNum][-3:], 2)))

        self.__setCanvas()
        self.__active = True
        self.__entry.bind("<KeyRelease>", self.__changed)
        self.__entry.bind("<FocusOut>", self.__changed)

    def __setCanvas(self):
        self.__canvas.clipboard_clear()
        self.__canvas.delete("all")

        data = self.__nusizArrange[int(self.__value.get())]
        for num in range(0, len(data)):
            if data[num] == "1":
                self.__canvas.create_rectangle((num)   * self.__w // 9, 0,
                                               (num+1) * self.__w // 9,
                                               self.__h // 3,
                                               outline="",
                                               fill=self.__colors.getColor("highLight")
                                               )

    def changeState(self, state):
        self.__entry.config(state = state)
        if state == NORMAL:
           self.__active = True
        else:
           self.__active = False

    def __changed(self, event):
        if self.__active == True:
            try:
                num = int(self.__value.get())
            except:
                self.__entry.config(bg = self.__colors.getColor("boxBackUnSaved"),
                                    fg=self.__colors.getColor("boxFontUnSaved")
                                    )
                return

            self.__entry.config(bg = self.__colors.getColor("boxBackNormal"),
                                fg=self.__colors.getColor("boxFontNormal")
                                    )

            if   num > 7: num = 7
            elif num < 0: num = 0

            if self.__stretchOnly == True:
               if   num == 6: num = 5
               elif num not in (0, 5, 7): num = 0

            d = bin(int(self.__value.get())).replace("0b", "")
            while len(d) < 3:
                d = "0" + d

            if d != self.__data[self.__dataNum][6:]:
                self.__value.set(str(num))

                self.__data[self.__dataNum] = self.__data[self.__dataNum][:6] + d
                self.__changeData(self.__data)
                self.__setCanvas()

    def getValue(self):
        return(self.__value.get())

    def setValue(self, val):
        self.__value.set(str(val))