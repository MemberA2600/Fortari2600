from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from time import sleep
import re

class SnowFlakes:
    def __init__(self, loader, baseFrame, data, changeData, w, h, currentBank, dead, blankAnimation):
        self.__loader = loader
        self.__baseFrame = baseFrame
        self.__data = data
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

        self.dead = dead

        itWasHash = False
        if "#" in self.__data:
            itWasHash = True

        self.__addElements()
        if itWasHash == True:
            self.__changeData(data)

    def killAll(self):
        for item in self.__uniqueFrame.pack_slaves():
            item.destroy()
        self.__uniqueFrame.destroy()
        self.__gradientFrame = None

    def __addElements(self):

        self.__uniqueFrame = Frame(self.__baseFrame, width=self.__w,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h)

        self.__uniqueFrame.pack_propagate(False)
        self.__uniqueFrame.pack(side=TOP, anchor=N, fill=X)

        self.__colorVars  = []
        self.__byteVars   = []
        self.__dataVars   = []
        self.__containers = []
        for address in self.__loader.virtualMemory.memory.keys():
            for variable in self.__loader.virtualMemory.memory[address].variables.keys():
                var = self.__loader.virtualMemory.memory[address].variables[variable]
                if ((var.validity == "global" or
                     var.validity == self.__currentBank) and
                        (var.system == False or
                         var.iterable == True or
                         var.linkable == True)
                ):
                    name = address + "::" + variable
                    self.__dataVars.append(name)
                    if (var.type == "byte" or var.type == "nibble"): self.__colorVars.append(name)
                    if  var.type == "byte": self.__byteVars.append(name)
                    if  var.type == "byte" and\
                        (var.system == False or
                         var.iterable == True ): self.__containers.append(name)

        numOf = 4
        self.__framesAndLabels = []
        self.__labels    = ["dataVar", "colorVar", "numOfLines", "gradient"]
        self.__listBoxes = []

        from HexEntry import HexEntry

        for num in range(0, numOf):
            f = Frame(self.__uniqueFrame, width=self.__w // numOf,
                                  bg=self.__loader.colorPalettes.getColor("window"),
                                  height=self.__h)

            f.pack_propagate(False)
            f.pack(side=LEFT, anchor=E, fill=Y)

            text = self.__dictionaries.getWordFromCurrentLanguage(self.__labels[num])
            if text.endswith(":") == False: text = text + ":"

            l = Label(f,          text=text,
                                  font=self.__smallFont, fg=self.__colors.getColor("font"),
                                  bg=self.__colors.getColor("window"), justify=CENTER
                                  )

            l.pack_propagate(False)
            l.pack(side=TOP, anchor=CENTER, fill=BOTH)

            self.__framesAndLabels.append([f, l])

            if num == 0:
                self.__listBoxes.append({})

                s = Scrollbar(f)
                l = Listbox(f, width=100000,
                                          height=1000,
                                          yscrollcommand=s.set,
                                          selectmode=BROWSE,
                                          exportselection=False,
                                          font=self.__smallFont,
                                          justify=LEFT
                                          )

                l.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
                l.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
                l.pack_propagate(False)

                s.pack(side=RIGHT, anchor=W, fill=Y)
                l.pack(side=LEFT, anchor=W, fill=BOTH)

                for item in self.__dataVars:
                    l.insert(END, item)

                self.__listBoxes[-1]["listBox"]     = l
                self.__listBoxes[-1]["selected"]    = ""
                self.__listBoxes[-1]["scrollBar"]   = s
                self.__listBoxes[-1]["dataList"]    = self.__dataVars

            elif num == 1:
                self.__listBoxes.append({})
                self.__constOrVar = IntVar()
                self.__constButton = Radiobutton(f, width=99999,
                                                 text=self.__dictionaries.getWordFromCurrentLanguage("constant"),
                                                 bg=self.__colors.getColor("window"),
                                                 fg=self.__colors.getColor("font"),
                                                 justify=LEFT, font=self.__smallFont,
                                                 variable=self.__constOrVar,
                                                 activebackground=self.__colors.getColor("highLight"),
                                                 value=1, command=self.__changeIfConstOrVar
                                                 )

                self.__constButton.pack_propagate(False)
                self.__constButton.pack(fill=X, side=TOP, anchor=N)

                text = self.__dictionaries.getWordFromCurrentLanguage("baseColor")
                if text.endswith(":") == False: text = text + ":"

                l1 = Label(f, text=text,
                          font=self.__smallFont, fg=self.__colors.getColor("font"),
                          bg=self.__colors.getColor("window"), justify=CENTER
                          )

                l1.pack_propagate(False)
                l1.pack(side=TOP, anchor=CENTER, fill=BOTH)

                self.__staticColors = ["$00", "$80"]
                self.__hexEntry = HexEntry(self.__loader, f, self.__colors, self.__colorDict,
                                           self.__normalFont, self.__staticColors, 0, None, self.__changeHex)

                text = self.__dictionaries.getWordFromCurrentLanguage("backColor")
                if text.endswith(":") == False: text = text + ":"

                l2 = Label(f, text=text,
                          font=self.__smallFont, fg=self.__colors.getColor("font"),
                          bg=self.__colors.getColor("window"), justify=CENTER
                          )

                l2.pack_propagate(False)
                l2.pack(side=TOP, anchor=CENTER, fill=BOTH)

                self.__hexEntry = HexEntry(self.__loader, f, self.__colors, self.__colorDict,
                                           self.__normalFont, self.__staticColors, 1, None, self.__changeHex)

                self.__varButton = Radiobutton(f, width=99999,
                                                 text=self.__dictionaries.getWordFromCurrentLanguage("variable"),
                                                 bg=self.__colors.getColor("window"),
                                                 fg=self.__colors.getColor("font"),
                                                 justify=LEFT, font=self.__smallFont,
                                                 variable=self.__constOrVar,
                                                 activebackground=self.__colors.getColor("highLight"),
                                                 value=2, command=self.__changeIfConstOrVar
                                                 )

                self.__varButton.pack_propagate(False)
                self.__varButton.pack(fill=X, side=TOP, anchor=N)

                s = Scrollbar(f)
                l = Listbox(f, width=100000,
                                          height=1000,
                                          yscrollcommand=s.set,
                                          selectmode=BROWSE,
                                          exportselection=False,
                                          font=self.__smallFont,
                                          justify=LEFT
                                          )

                l.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
                l.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
                l.pack_propagate(False)

                s.pack(side=RIGHT, anchor=W, fill=Y)
                l.pack(side=LEFT, anchor=W, fill=BOTH)

                for item in self.__colorVars:
                    l.insert(END, item)

                self.__listBoxes[-1]["listBox"]     = l
                self.__listBoxes[-1]["selected"]    = ""
                self.__listBoxes[-1]["scrollBar"]   = s
                self.__listBoxes[-1]["dataList"]    = self.__colorVars

                self.__framesAndLabels.append(l1)
                self.__framesAndLabels.append(l2)


            elif num == 2:
                self.__listBoxes.append({})

                self.__numOfLines = StringVar()
                self.__numOfLines = Entry(f,
                                          name="speed",
                                          bg=self.__colors.getColor("boxBackNormal"),
                                          fg=self.__colors.getColor("boxFontNormal"),
                                          width=9999, justify=CENTER,
                                          textvariable=self.__numOfLines,
                                          font=self.__normalFont
                                          )

                self.__numOfLines.pack_propagate(False)
                self.__numOfLines.pack(fill=X, side=TOP, anchor=N)

                self.__numOfLines.bind("<FocusOut>", self.__chamgeConst)
                self.__numOfLines.bind("<KeyRelease>", self.__chamgeConst)

                text = self.__dictionaries.getWordFromCurrentLanguage("container")
                if text.endswith(":") == False: text = text + ":"

                l3 = Label(f, text=text,
                           font=self.__smallFont, fg=self.__colors.getColor("font"),
                           bg=self.__colors.getColor("window"), justify=CENTER
                           )

                l3.pack_propagate(False)
                l3.pack(side=TOP, anchor=CENTER, fill=BOTH)

                s = Scrollbar(f)
                l = Listbox(f, width=100000,
                            height=1000,
                            yscrollcommand=s.set,
                            selectmode=BROWSE,
                            exportselection=False,
                            font=self.__smallFont,
                            justify=LEFT
                            )

                l.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
                l.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
                l.pack_propagate(False)

                s.pack(side=RIGHT, anchor=W, fill=Y)
                l.pack(side=LEFT, anchor=W, fill=BOTH)

                for item in self.__containers:
                    l.insert(END, item)

                self.__listBoxes[-1]["listBox"] = l
                self.__listBoxes[-1]["selected"] = ""
                self.__listBoxes[-1]["scrollBar"] = s
                self.__listBoxes[-1]["dataList"] = self.__containers
                self.__framesAndLabels.append(l3)

            elif num == 3:
                h = self.__h // 24
                w = self.__w // 8

                self.__hexEntries = {}
                self.__hexValues  = []
                for num2 in range(0, 32):
                    self.__hexValues.append("$00")

                for num2 in range(0, 16):
                    subF = Frame(f, width=self.__w,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height= h)

                    subF.pack_propagate(False)
                    subF.pack(side=TOP, anchor=N, fill=X)

                    subF1 = Frame(subF, width=w,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height= h)

                    subF1.pack_propagate(False)
                    subF1.pack(side=LEFT, anchor=E, fill=Y)

                    subF2 = Frame(subF, width=w,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height= h)

                    subF2.pack_propagate(False)
                    subF2.pack(side=LEFT, anchor=E, fill=Y)

                    self.__framesAndLabels.append(subF)
                    self.__framesAndLabels.append(subF1)
                    self.__framesAndLabels.append(subF1)

                    self.__hexEntries[num2]     = {}
                    self.__hexEntries[num2+16]  = {}

                    hexEntry1 = HexEntry(self.__loader, subF1, self.__colors, self.__colorDict,
                                        self.__normalFont, self.__hexValues, num2, None, self.__changeHex)

                    hexEntry2 = HexEntry(self.__loader, subF2, self.__colors, self.__colorDict,
                                        self.__normalFont, self.__hexValues, num2+15, None, self.__changeHex)

                self.__button = Button(
                        f, width=self.__w,
                        bg=self.__colors.getColor("window"),
                        fg=self.__colors.getColor("font"),
                        font=self.__normalFont,
                        command=self.__generatePattern,
                        text=self.__dictionaries.getWordFromCurrentLanguage("generateRandom")
                    )

                self.__button.pack_propagate(False)
                self.__button.pack(side=TOP, anchor=N)

        if self.__data[3] == "#":
           self.__listBoxes[0]["selected"] = self.__listBoxes[0]["dataList"][0].split("::")[1]

        selector = 0
        for itemNum in range(0, len(self.__listBoxes[0]["dataList"])):
            if self.__listBoxes[0]["selected"] == self.__listBoxes[0]["dataList"][itemNum].split("::")[1]:
                selector = itemNum
                break

        self.__listBoxes[0]["selected"] = self.__listBoxes[0]["dataList"][selector].split("::")[1]
        self.__data[3] = self.__listBoxes[0]["selected"]
        self.__listBoxes[0]["listBox"].select_set(selector)

    def __chamgeConst(self, event):
        pass

    def __changeHex(self, event):
        pass

    def __changeIfConstOrVar(self):
        pass

    def __generatePattern(self):
        numOfLines = int(self.__data[4])
        from datetime import datetime
        from random import randint

        time = datetime.now()
        importantNum = int(str(time).split(".")[-1]) % 2



    def isItBin(self, num):
        if num[0] != "%": return False

        try:
            teszt = int("0b" + num[1:], 2)
            return True
        except:
            return False

    def isItHex(self, num):
        if num[0] != "$": return False

        try:
            teszt = int("0x" + num[1:], 16)
            return True
        except:
            return False

    def isItNum(self, num):
        try:
            num = int(num)
            return True
        except:
            return False



