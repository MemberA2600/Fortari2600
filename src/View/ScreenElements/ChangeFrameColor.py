from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from time import sleep

from ScreenSetterFrameBase import ScreenSetterFrameBase

class ChangeFrameColor:

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
        self.__fontSize = int(self.__screenSize[0]/1300 * self.__screenSize[1]/1050*14)
        self.__colors = self.__loader.colorPalettes
        self.__colorDict = self.__loader.colorDict

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize*0.65), False, False, False)
        self.__bigFont = self.__fontManager.getFont(int(self.__fontSize*1.15), False, False, False)
        self.__bigFont2 = self.__fontManager.getFont(int(self.__fontSize*1.5), False, False, False)

        self.__name         = StringVar()
        self.__name.set(self.__data[0])
        self.dead = [False]
        self.__lastData     = self.__data[2]

        self.__setterBase = ScreenSetterFrameBase(loader, baseFrame, data, self.__name, changeName, self.dead, itemNames)
        self.__addElements()

    def __addElements(self):
        self.__uniqueFrame = Frame( self.__baseFrame, width = self.__w,
                                    bg = self.__loader.colorPalettes.getColor("window"),
                                    height = self.__h)

        self.__uniqueFrame.pack_propagate(False)
        self.__uniqueFrame.pack(side=TOP, anchor=N, fill=X)

        self.__check = IntVar()
        self.__check.set(int(self.__data[3]))

        self.__checkBox = Checkbutton(self.__uniqueFrame, width=99999,
                                       text=self.__dictionaries.getWordFromCurrentLanguage("alterLastFrameColor"),
                                       bg=self.__colors.getColor("window"),
                                       fg=self.__colors.getColor("font"),
                                       justify=LEFT, font=self.__smallFont,
                                       variable=self.__check,
                                       activebackground=self.__colors.getColor("highLight"),
                                       command=self.__changeBox
                                       )

        self.__checkBox.pack_propagate(False)
        self.__checkBox.pack(fill=X, side=TOP, anchor=N)

        self.__constantVar  = StringVar()
        self.__variableVar  = StringVar()

        self.__option       = IntVar()

        self.__variableFrame = Frame(   self.__uniqueFrame, width = self.__w // 2,
                                    bg = self.__loader.colorPalettes.getColor("window"),
                                    height = self.__h)
        self.__variableFrame.pack_propagate(False)
        self.__variableFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__constantFrame = Frame(   self.__uniqueFrame, width = self.__w // 2,
                                    bg = self.__loader.colorPalettes.getColor("window"),
                                    height = self.__h)
        self.__constantFrame.pack_propagate(False)
        self.__constantFrame.pack(side=LEFT, anchor=E, fill=Y)

        import re

        if self.isItHex(self.__data[2]):
           self.__option.set(2)
           self.__variableVar.set("")
           self.__constantVar.set(self.__data[2])
        else:
           self.__option.set(1)
           self.__variableVar.set(self.__data[2])
           self.__constantVar.set("")

        self.__variableButton = Radiobutton( self.__variableFrame, width = 99999,
                                             text=self.__dictionaries.getWordFromCurrentLanguage("variable"),
                                             bg=self.__colors.getColor("window"),
                                             fg=self.__colors.getColor("font"),
                                             justify=LEFT, font=self.__normalFont,
                                             variable = self.__option,
                                             activebackground = self.__colors.getColor("highLight"),
                                             value = 1, command = self.XXX
        )

        self.__constantButton = Radiobutton( self.__constantFrame, width = 99999,
                                             text=self.__dictionaries.getWordFromCurrentLanguage("constant"),
                                             bg=self.__colors.getColor("window"),
                                             fg=self.__colors.getColor("font"),
                                             justify=LEFT, font=self.__normalFont,
                                             variable = self.__option,
                                             activebackground=self.__colors.getColor("highLight"),
                                             value = 2, command = self.XXX
        )

        self.__variableButton.pack_propagate(False)
        self.__variableButton.pack(side = TOP, anchor = N, fill = X)
        self.__constantButton.pack_propagate(False)
        self.__constantButton.pack(side = TOP, anchor = N, fill = X)

        self.__varList = []
        for address in self.__loader.virtualMemory.memory.keys():
            for variable in self.__loader.virtualMemory.memory[address].variables.keys():
                var = self.__loader.virtualMemory.memory[address].variables[variable]
                if (    var.type == "byte" and
                        (var.validity == "global" or
                        var.validity == self.__currentBank) and
                        (var.system == False or
                        var.iterable == True or
                        var.linkable == True)
                ):
                   self.__varList.append(address + "::" + variable)

        self.__varList.sort()

        self.__varListScrollBar = Scrollbar(self.__variableFrame)
        self.__varListBox = Listbox(   self.__variableFrame, width=100000,
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

        self.__varListBox.bind("<ButtonRelease-1>", self.clickedListBox)
        self.__varListBox.bind("<KeyRelease-Up>", self.clickedListBox)
        self.__varListBox.bind("<KeyRelease-Down>", self.clickedListBox)

        self.__tempSet = self.__varList[0].split("::")[1]
        if "::" in self.__data[2]: self.__tempSet = self.__data[2]

        from HexEntry import HexEntry
        self.__color = ["$00"]

        self.__constEntry = HexEntry(self.__loader, self.__constantFrame, self.__colors, self.__colorDict,
                                     self.__normalFont, self.__color, 0, None, self.__chamgeConst)

        if "::" not in self.__data[2]:
            self.__color[0] = self.__data[2]
            self.__constEntry.setValue(self.__data[2])

        self.setIt(None)

    def XXX(self):
        self.setIt(None)
        self.__changeData(self.__data)

    def setIt(self, data):
        if self.__option.get() == 1:
           self.__constEntry.changeState(DISABLED)
           self.__varListBox.config(state=NORMAL)

           if data == None:
               selector = 0
               for itemNum in range(0, len(self.__varList)):
                   if self.__varList[itemNum] == self.__tempSet:
                      selector = itemNum
                      break

               self.__varListBox.select_clear(0, END)
               self.__varListBox.select_set(selector)
               self.__data[2] = self.__varList[selector]
               self.__tempSet = self.__data[2]
               self.__changeData(self.__data)

           else:
               self.__tempSet = self.__varList[data]
               if self.__data[2] != self.__tempSet:
                    self.__data[2] = self.__tempSet
                    self.__changeData(self.__data)


        else:
            self.__varListBox.select_clear(0, END)
            self.__varListBox.config(state = DISABLED)
            self.__constEntry.changeState(NORMAL)

            if data == None:
               self.__constEntry.setValue(self.__color[0])
               self.__data[2] = self.__color[0]
               self.__changeData(self.__data)
            else:
               self.__color[0]  = self.__constEntry.getValue()
               if data != self.__data[2]:
                   self.__data[2]   = self.__color[0]
                   self.__changeData(self.__data)

    def clickedListBox(self, event):
        if self.__option.get() == 2:
           return
        self.setIt(self.__varListBox.curselection()[0])

    def __chamgeConst(self, event):
        if self.__option.get() == 1:
           return
        self.setIt(self.__constEntry.getValue())

    def isItHex(self, num):
        if num[0] != "$": return False

        try:
            teszt = int("0x"+num[1:], 16)
            return True
        except:
            return False

    def __changeBox(self):
        self.__data[3] = str(self.__check.get())
        self.__changeData(self.__data)