from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from time import sleep

from ScreenSetterFrameBase import ScreenSetterFrameBase

class Indicator:

    def __init__(self, loader, baseFrame, data, changeName, changeData, w, h, currentBank):
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
        self.__lastSelected = None

        self.dead = [False]

        self.__setterBase = ScreenSetterFrameBase(loader, baseFrame, data, self.__name, changeName, self.dead)
        self.__addElements()

    def __addElements(self):
        self.__uniqueFrame = Frame(self.__baseFrame, width=self.__w,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h)

        self.__uniqueFrame.pack_propagate(False)
        self.__uniqueFrame.pack(side=TOP, anchor=N, fill=X)

        self.__indicators = []
        import os

        groot = os.getcwd() + "\src\View\ScreenElements\Indicators"
        #print(groot)
        for root, dirs, files in os.walk(groot):
            for file in files:
                if root == groot and "py" in file:
                    self.__indicators.append(file[:-3])
        #print(indicators)
        self.__indicators.sort()

        self.__label1 = Label(self.__uniqueFrame,
                                   text=self.__dictionaries.getWordFromCurrentLanguage("indicatorTyp")+":",
                                   font=self.__normalFont, fg=self.__colors.getColor("font"),
                                   bg=self.__colors.getColor("window"), justify=CENTER
                                   )

        self.__label1.pack_propagate(False)
        self.__label1.pack(side=TOP, anchor=CENTER, fill=X)

        self.__listFrame = Frame(self.__uniqueFrame, width=self.__w,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 height=round(self.__h // 10 * 2.5))

        self.__listFrame.pack_propagate(False)
        self.__listFrame.pack(side=TOP, anchor=N, fill=X)

        self.__indicatorListScrollBar = Scrollbar(self.__listFrame)
        self.__indicatorListBox = Listbox(self.__listFrame, width=100000,
                                    height=1000,
                                    yscrollcommand=self.__indicatorListScrollBar.set,
                                    selectmode=BROWSE,
                                    exportselection=False,
                                    font=self.__normalFont,
                                    justify=LEFT
                                    )

        self.__indicatorListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__indicatorListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__indicatorListBox.pack_propagate(False)

        self.__indicatorListScrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__indicatorListBox.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__indicatorListScrollBar.config(command=self.__indicatorListBox.yview)
        for var in self.__indicators:
            self.__indicatorListBox.insert(END, var)

        self.__indicatorListBox.select_clear(0, END)

        from FullBar             import FullBar
        from HalfBarWithText     import HalfBarWithText
        from TwoIconsTwoLines    import TwoIconsTwoLines
        from OneIconWithDigits   import OneIconWithDigits
        from SevenDigits         import SevenDigits
        from TwelveIconsOrDigits import TwelveIconsOrDigits

        self.screenSubs = {
            "FullBar"             : [FullBar,             ["#", "255", "$40|$30|$10", "1", "0"]],
            "HalfBarWithText"     : [HalfBarWithText,     ["#", "255", "$40", "1", "$06" ,"Health:", "0", "0"]],
            "TwoIconsTwoLines"    : [TwoIconsTwoLines,    ["#", "$40", "%00000000", "255", "#", "$80", "%00000000", "255", "1", "#", "#", "0", "0"]],
            "OneIconWithDigits"   : [OneIconWithDigits,   ["#", "$16", "%00000000", "2", "#", "#", "default", "1"]],
            "SevenDigits"         : [SevenDigits,         ["#", "#", "#", "#", "#", "#", "#", "7", "0", "1", "$16", "default"]],
            "TwelveIconsOrDigits" : [TwelveIconsOrDigits, ["#", "#", "$06", "#", "1", "1"]]
        }

        if self.__data[2]  == "#":
           self.__data[2]  = self.__indicators[0]
           self.__indicatorListBox.select_set(0)
           for num in range(0, len(self.screenSubs[self.__indicators[0]][1])):
               self.__data[3 + num] = self.screenSubs[self.__indicators[0]][1][num]
        else:
           for itemNum in range(0, len(self.__indicators)):
               if self.__indicators[itemNum] == self.__data[2]:
                  self.__indicatorListBox.select_set(itemNum)

        self.__lastSelected = self.__indicatorListBox.curselection()[0]

        self.__subFrame = self.screenSubs[self.__data[2]][0](
            self.__loader, self.__uniqueFrame, self.__data, self.__changeData,
            self.__w, self.__h - round(self.__h // 10 * 2.5), self.__currentBank, self.dead
        )

        self.__indicatorListBox.bind("<ButtonRelease-1>", self.__changedType)
        self.__indicatorListBox.bind("<KeyRelease-Up>", self.__changedType)
        self.__indicatorListBox.bind("<KeyRelease-Down>", self.__changedType)

    def __changedType(self, evenz):
        if self.__lastSelected != self.__indicatorListBox.curselection()[0]:
            self.__subFrame.killAll()
            self.__data[2] = self.__indicators[self.__indicatorListBox.curselection()[0]]
            for num in range(0, len(self.screenSubs[self.__indicators[self.__indicatorListBox.curselection()[0]]][1])):
                self.__data[3 + num] = self.screenSubs[self.__indicators[self.__indicatorListBox.curselection()[0]]][1][num]

            self.__lastSelected = self.__indicatorListBox.curselection()[0]

            self.__changeData(self.__data)

            self.__subFrame = self.screenSubs[self.__data[2]][0](
                self.__loader, self.__uniqueFrame, self.__data, self.__changeData,
                self.__w, self.__h - round(self.__h // 10 * 2.5), self.__currentBank, self.dead
            )