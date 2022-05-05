from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from time import sleep

from ScreenSetterFrameBase import ScreenSetterFrameBase

class Picture64px:

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
        self.dead = [False]
        self.__lastData = None

        self.__setterBase = ScreenSetterFrameBase(loader, baseFrame, data, self.__name, changeName, self.dead)
        self.__addElements()

    def __addElements(self):
        self.__uniqueFrame = Frame(self.__baseFrame, width=self.__w,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h)

        self.__uniqueFrame.pack_propagate(False)
        self.__uniqueFrame.pack(side=TOP, anchor=N, fill=X)

        self.__listFrame = Frame(self.__uniqueFrame, width=self.__w,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h // 10 * 6)

        self.__listFrame.pack_propagate(False)
        self.__listFrame.pack(side=TOP, anchor=N, fill=X)

        folder = self.__loader.mainWindow.projectPath+"64px"

        self.__varList = []

        import os
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith(".asm"):
                   self.__varList.append(file[:-4])

        self.__varList.sort()
        self.__varListScrollBar = Scrollbar(self.__listFrame)
        self.__varListBox = Listbox(   self.__listFrame, width=100000,
                                        height=1000,
                                        yscrollcommand=self.__varListScrollBar.set,
                                        selectmode=BROWSE,
                                        exportselection = False,
                                        font = self.__smallFont,
                                        justify = LEFT
                                    )

        self.__varListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__varListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__varListBox.pack_propagate(False)

        self.__varListScrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__varListBox.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__varListScrollBar.config(command=self.__varListBox.yview)
        for var in self.__varList:
            self.__varListBox.insert(END, var)


        self.__setterBase.registerError("no64px")
        if len(self.__varList) == 0:
           self.__setterBase.changeErrorState("no64px", True)
           self.__varListBox.config(state = DISABLED)
        else:
            self.__varListBox.bind("<ButtonRelease-1>", self.clickedListBox)
            self.__tempSet = self.__varList[0]

            if self.__data[2] == "#":
                self.setIt(0)
            else:
                found = False
                for itemNum in range(0, len(self.__varList)):
                    if self.__varList[itemNum] == self.__data[2]:
                       found = True
                       self.setIt(itemNum)
                       break

                if found == False:
                   self.setIt(0)


    def clickedListBox(self, event):
        self.setIt(self.__varListBox.curselection()[0])

    def setIt(self, selected):
        if self.__lastData != self.__varList[selected]:
            self.__lastData = self.__varList[selected]
            self.__data[2]  = self.__varList[selected]
            num = 0
            for itemNum in range(0, len(self.__varList)):
                if self.__varList[itemNum] == self.__data[2]:
                    num = itemNum
                    break

            self.__varListBox.select_clear(0, END)
            self.__varListBox.select_set(num)
            self.__changeData(self.__data)
            h = self.getMaxHeight()
            print(h)

    def getMaxHeight(self):
        import os

        fileName1 = self.__loader.mainWindow.projectPath+"64px/"     +\
                    self.__varList[self.__varListBox.curselection()[0]] +\
                    ".a26"
        fileName2 = self.__loader.mainWindow.projectPath+"64px/"     +\
                    self.__varList[self.__varListBox.curselection()[0]] +\
                    ".asm"

        if os.path.exists(fileName1):
           f   = open(fileName1, "r")
           txt = f.read().replace("\r", "").split("\n")
           f.close()

           return(int(txt[0]))
        else:
           f = open(fileName2, "r")
           lines = f.read().replace("\r", "").split("\n")
           f.close()

           foundByte = False
           counter   = 0
           for line in lines:
               if "BYTE" in line.upper():
                   foundByte = True
                   counter  += 1
               else:
                   if foundByte == True:
                      break
           return counter