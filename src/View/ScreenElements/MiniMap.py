from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from time import sleep

from ScreenSetterFrameBase import ScreenSetterFrameBase

class MiniMap:

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
        self.dead           = [False]

        self.__loadVariables()
        self.__loadPictures()

        itWasHash = False
        if "#" in self.__data :
            itWasHash = True

        self.__setterBase = ScreenSetterFrameBase(loader, baseFrame, data, self.__name, changeName, self.dead, itemNames)
        self.__addElements()

        if itWasHash == True:
            self.__changeData(self.__data)


    def __loadVariables(self):
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


    def __loadPictures(self):
        self.__listOfPictures = {}

        import os

        for root, dirs, files in os.walk(self.__loader.mainWindow.projectPath + "minimaps/"):
            for file in files:
                if file.endswith(".asm"):
                    self.__listOfPictures[file.replace(".asm", "")] = {}

                    f = open(root + "/" + file.replace(".asm", ".a26"))
                    lines = f.read().replace("\r", "").split("\n")
                    f.close()

                    self.__listOfPictures[file.replace(".asm", "")]["matrix"]     = lines[1].split(" ")
                    self.__listOfPictures[file.replace(".asm", "")]["stepY"]      = lines[2]
                    self.__listOfPictures[file.replace(".asm", "")]["colors"]     = lines[3].split(" ")
                    self.__listOfPictures[file.replace(".asm", "")]["colors"].pop(2)

    def __addElements(self):
        self.__uniqueFrame = Frame(self.__baseFrame, width=self.__w,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h)

        self.__uniqueFrame.pack_propagate(False)
        self.__uniqueFrame.pack(side=TOP, anchor=N, fill=X)

        maxFrames = 6

        self.__framesAndLabels = []
        self.__listBoxes = []
        self.__hexEntries = []
        self.__hexColors = ["$40", "$02", "$0e"]
        self.__buttons = []
        self.__buttonVars = []

        from HexEntry import HexEntry
        labels      = ["minimap", "dataVar",  "dataVar",  "COLUPF", "COLUBK", "ballColor"]
        functions   = [self.__changeIfConstOrVar1, self.__changeIfConstOrVar2, self.__changeIfConstOrVar3]

        for num in range(0, maxFrames):
            f = Frame(self.__uniqueFrame, width=self.__w // maxFrames,
                      bg=self.__loader.colorPalettes.getColor("window"),
                      height=self.__h)

            f.pack_propagate(False)
            f.pack(side=LEFT, anchor=E, fill=Y)

            text = self.__dictionaries.getWordFromCurrentLanguage(labels[num])
            if text.endswith(":") == False: text = text + ":"

            l1 = Label(f, text=text,
                       font=self.__smallFont, fg=self.__colors.getColor("font"),
                       bg=self.__colors.getColor("window"), justify=CENTER
                       )

            l1.pack_propagate(False)
            l1.pack(side=TOP, anchor=CENTER, fill=X)

            self.__framesAndLabels.append(f)
            self.__framesAndLabels.append(l1)

            if num == 0:

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
                s.config(command=l.yview)

                self.__listBoxes.append({})
                self.__listBoxes[-1]["listBox"]     = l
                self.__listBoxes[-1]["scrollBar"]   = s
                self.__listBoxes[-1]["dataList"]    = list(self.__listOfPictures.keys())
                self.__listBoxes[-1]["selected"]    = ""

                for item in self.__listBoxes[-1]["dataList"]:
                    self.__listBoxes[-1]["listBox"].insert(END, item)

                l.bind("<ButtonRelease-1>", self.__changeSelected)
                l.bind("<KeyRelease-Up>", self.__changeSelected)
                l.bind("<KeyRelease-Down>", self.__changeSelected)

            elif num in range(1, 3):
                f1 = Frame(f, width=self.__w // maxFrames,
                          bg=self.__loader.colorPalettes.getColor("window"),
                          height=self.__h // 2.5)

                f1.pack_propagate(False)
                f1.pack(side=TOP, anchor=N, fill=X)

                l2 = Label(f, text=text,
                           font=self.__smallFont, fg=self.__colors.getColor("font"),
                           bg=self.__colors.getColor("window"), justify=CENTER
                           )

                l2.pack_propagate(False)
                l2.pack(side=TOP, anchor=CENTER, fill=X)

                f2 = Frame(f, width=self.__w // maxFrames,
                          bg=self.__loader.colorPalettes.getColor("window"),
                          height=self.__h // 2.5)

                f2.pack_propagate(False)
                f2.pack(side=TOP, anchor=N, fill=X)

                self.__framesAndLabels.append(f1)
                self.__framesAndLabels.append(f2)
                self.__framesAndLabels.append(l2)

                s1 = Scrollbar(f1)
                l1 = Listbox(f1, width=100000,
                            height=1000,
                            yscrollcommand=s1.set,
                            selectmode=BROWSE,
                            exportselection=False,
                            font=self.__smallFont,
                            justify=LEFT
                            )

                l1.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
                l1.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
                l1.pack_propagate(False)

                s1.pack(side=RIGHT, anchor=W, fill=Y)
                l1.pack(side=LEFT, anchor=W, fill=BOTH)
                s1.config(command=l1.yview)

                s2 = Scrollbar(f2)
                l2 = Listbox(f2, width=100000,
                            height=1000,
                            yscrollcommand=s2.set,
                            selectmode=BROWSE,
                            exportselection=False,
                            font=self.__smallFont,
                            justify=LEFT
                            )

                l2.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
                l2.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
                l2.pack_propagate(False)

                s2.pack(side=RIGHT, anchor=W, fill=Y)
                l2.pack(side=LEFT, anchor=W, fill=BOTH)
                s2.config(command=l2.yview)

                self.__listBoxes.append({})
                self.__listBoxes[-1]["listBox"]     = l1
                self.__listBoxes[-1]["scrollBar"]   = s1
                self.__listBoxes[-1]["selected"]    = ""
                self.__listBoxes[-1]["dataList"]    = None

                self.__listBoxes.append({})
                self.__listBoxes[-1]["listBox"]     = l2
                self.__listBoxes[-1]["scrollBar"]   = s2
                self.__listBoxes[-1]["selected"]    = ""
                self.__listBoxes[-1]["dataList"]    = None

                l1.bind("<ButtonRelease-1>", self.__changeSelected)
                l1.bind("<KeyRelease-Up>", self.__changeSelected)
                l1.bind("<KeyRelease-Down>", self.__changeSelected)

                l2.bind("<ButtonRelease-1>", self.__changeSelected)
                l2.bind("<KeyRelease-Up>", self.__changeSelected)
                l2.bind("<KeyRelease-Down>", self.__changeSelected)

                # These listboxes are set later since we don't know the selected minimap source.

            elif num > 2:
                self.__hexEntries.append({})

                __constOrVar = IntVar()
                __constButton = Radiobutton(f, width=99999,
                                                 text=self.__dictionaries.getWordFromCurrentLanguage("constant"),
                                                 bg=self.__colors.getColor("window"),
                                                 fg=self.__colors.getColor("font"),
                                                 justify=LEFT, font=self.__smallFont,
                                                 variable=__constOrVar,
                                                 activebackground=self.__loader.colorPalettes.getColor("highLight"),
                                                 activeforeground=self.__loader.colorPalettes.getColor("font"),
                                                 value=1, command=functions[num-3]
                                                 )

                __constButton.pack_propagate(False)
                __constButton.pack(fill=X, side=TOP, anchor=N)

                __hexEntry = HexEntry(self.__loader, f, self.__colors, self.__colorDict,
                             self.__normalFont, self.__hexColors, num-3, None, self.__changeHex)

                self.__hexEntries[-1]["object"]  = __hexEntry
                self.__hexEntries[-1]["entry"]   = __hexEntry.getEntry()
                self.__hexEntries[-1]["value"]   = __hexEntry.getValue()
                self.__hexEntries[-1]["state"]   = NORMAL

                __varButton = Radiobutton(f, width=99999,
                                                 text=self.__dictionaries.getWordFromCurrentLanguage("variable"),
                                                 bg=self.__colors.getColor("window"),
                                                 fg=self.__colors.getColor("font"),
                                                 justify=LEFT, font=self.__smallFont,
                                                 variable=__constOrVar,
                                                 activebackground=self.__loader.colorPalettes.getColor("highLight"),
                                                 activeforeground=self.__loader.colorPalettes.getColor("font"),
                                                 value=2, command=functions[num-3]
                                                 )

                __varButton.pack_propagate(False)
                __varButton.pack(fill=X, side=TOP, anchor=N)
                self.__buttons.append(__constButton)
                self.__buttons.append(__varButton)

                self.__listBoxes.append({})

                s1 = Scrollbar(f)
                l1 = Listbox(f, width=100000,
                             height=1000,
                             yscrollcommand=s1.set,
                             selectmode=BROWSE,
                             exportselection=False,
                             font=self.__smallFont,
                             justify=LEFT
                             )

                l1.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
                l1.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
                l1.pack_propagate(False)

                s1.pack(side=RIGHT, anchor=W, fill=Y)
                l1.pack(side=LEFT, anchor=W, fill=BOTH)
                s1.config(command=l1.yview)

                self.__buttonVars.append(__constOrVar)

                self.__listBoxes[-1]["listBox"]     = l1
                self.__listBoxes[-1]["scrollBar"]   = s1
                self.__listBoxes[-1]["selected"]    = ""
                self.__listBoxes[-1]["dataList"]    = self.__colorVars

                l1.bind("<ButtonRelease-1>", self.__changeSelected)
                l1.bind("<KeyRelease-Up>", self.__changeSelected)
                l1.bind("<KeyRelease-Down>", self.__changeSelected)

                for item in self.__listBoxes[-1]["dataList"]:
                    self.__listBoxes[-1]["listBox"].insert(END, item)

        minimap     = self.__data[2]
        xPoz        = self.__data[3]
        yPoz        = self.__data[4]
        ballX       = self.__data[5]
        ballY       = self.__data[6]
        colors      = self.__data[7:10]


        # xPoz shouldn't reach the matrix X!
        # yPoz shouldn't reach the matirx Y!
        # ballX is always between 0-30, so it's a bytewar
        # ballY shoudln't reach stepY!

        if self.__data[2] == "#": self.__data[2] = self.__listBoxes[0]["dataList"][0]

        selector = 0
        for itemNum in range(0, len(self.__listBoxes[0]["dataList"])):
            if minimap == self.__listBoxes[0]["dataList"][itemNum]:
               selector = itemNum
               break

        self.__listBoxes[0]["listBox"].select_set(selector)
        self.__listBoxes[0]["listBox"].yview(selector)

        matrixX = int(self.__listOfPictures[self.__listBoxes[0]["dataList"][selector]]["matrix"][0])
        matrixY = int(self.__listOfPictures[self.__listBoxes[0]["dataList"][selector]]["matrix"][1])
        stepY   = int(self.__listOfPictures[self.__listBoxes[0]["dataList"][selector]]["stepY"])

        self.__generateListBoxes([matrixX, matrixY, 30, stepY])

        for num in range(0, 3):
            if colors[num] == "#":
                colors[num] = self.__hexColors[num]
                self.__data[7 + num] = colors[num]

            if self.isItHex(colors[num]) == True:
               self.__hexEntries[num]["object"].changeState(NORMAL)
               self.__hexEntries[num]["state"] = NORMAL
               self.__hexEntries[num]["object"].setValue(colors[num])
               self.__hexEntries[num]["value"] = colors[num]
               self.__hexColors[num] = colors[num]

               self.__listBoxes[num + 5]["listBox"].config(state = DISABLED)
               self.__buttonVars[num].set(1)
            else:
               self.__hexEntries[num]["object"].changeState(DISABLED)
               self.__hexEntries[num]["state"] = DISABLED

               self.__listBoxes[num + 5]["listBox"].config(state=NORMAL)
               selector = 0
               for itemNum in range(0, len(self.__listBoxes[num + 5]["dataList"])):
                   if self.__listBoxes[num + 5]["dataList"][itemNum].split("::")[1] == colors[num]:
                      selector = itemNum
                      break

               self.__listBoxes[num + 5]["selected"] = self.__listBoxes[num + 5]["dataList"][selector].split("::")[1]
               self.__data[num + 7]                  = self.__listBoxes[num + 5]["selected"]
               self.__buttonVars[num].set(2)
               self.__listBoxes[num + 5]["listBox"].select_set(selector)
               self.__listBoxes[num + 5]["listBox"].yview(selector)

    def __generateListBoxes(self, limits):
        for num in range(0, 4):
            limitNum = bin(limits[num]).replace("0b", "")
            bits     = len(limitNum)

            self.__listBoxes[num + 1]["listBox"].select_clear(0, END)
            self.__listBoxes[num + 1]["listBox"].delete(0, END)
            self.__listBoxes[num + 1]["dataList"] = []

            for var in self.__dataVars:
                theVar = self.__loader.virtualMemory.getVariableByName2(var.split("::")[1])
                if len(theVar.usedBits) >= bits:
                   self.__listBoxes[num + 1]["dataList"].append(var)
                   self.__listBoxes[num + 1]["listBox"].insert(END, var)

            if self.__data[3+num] == "#":
               self.__listBoxes[num + 1]["selected"] = self.__listBoxes[num + 1]["dataList"][0].split("::")[1]
               self.__data[3 + num]                  = self.__listBoxes[num + 1]["selected"]

            selector = 0
            for itemNum in range(0, len(self.__listBoxes[num + 1]["dataList"])):
                if self.__listBoxes[num + 1]["dataList"][itemNum].split("::")[1] == self.__data[3 + num]:
                   selector = itemNum
                   break

            self.__listBoxes[num + 1]["selected"] = self.__listBoxes[num + 1]["dataList"][selector].split("::")[1]
            self.__data[3 + num] = self.__listBoxes[num + 1]["selected"]
            self.__listBoxes[num + 1]["listBox"].select_set(selector)
            self.__listBoxes[num + 1]["listBox"].yview(selector)

            self.__changeData(self.__data)

    def __changeSelected(self, event):
        listNum = 0
        for itemNum in range(0, len(self.__listBoxes)):
            if event.widget == self.__listBoxes[itemNum]["listBox"]:
               listNum = itemNum
               break

        if listNum in range(5,8):
           if self.__listBoxes[listNum]["state"] == DISABLED: return

        magicData = ""

        try:
            magicData = self.__listBoxes[listNum]["dataList"][
                        self.__listBoxes[listNum]["listBox"].curselection()[0]].split("::")[1]
        except:
            magicData = self.__listBoxes[listNum]["dataList"][
                        self.__listBoxes[listNum]["listBox"].curselection()[0]]


        if self.__listBoxes[listNum]["selected"] != magicData:
           self.__listBoxes[listNum]["selected"]  = magicData
           self.__data[listNum + 2] = self.__listBoxes[listNum]["selected"]

           if listNum == 0:
               matrixX = int(self.__listOfPictures[self.__listBoxes[0]["dataList"][self.__listBoxes[0]["listBox"].curselection()[0]]]["matrix"][0])
               matrixY = int(self.__listOfPictures[self.__listBoxes[0]["dataList"][self.__listBoxes[0]["listBox"].curselection()[0]]]["matrix"][1])
               stepY   = int(self.__listOfPictures[self.__listBoxes[0]["dataList"][self.__listBoxes[0]["listBox"].curselection()[0]]]["stepY"])

               self.__generateListBoxes([matrixX, matrixY, 30, stepY])

           self.__changeData(self.__data)

    def __changeHex(self, event):
        hexNum = 0
        for num in range(0, 3):
            if self.__hexEntries[num]["entry"] == event.widget:
               hexNum = num
               break

        if self.__hexEntries[hexNum]["state"] == DISABLED: return

        val = self.__hexEntries[hexNum]["object"].getValue()
        if self.isItHex(val):
           self.__hexEntries[-1]["value"] = self.__hexEntries[-1]["object"].getValue()
           self.__data[hexNum + 7] = val
           self.__changeData(self.__data)

    def __changeIfConstOrVar1(self):
        self.__changeIfConstOrVar(0)

    def __changeIfConstOrVar2(self):
        self.__changeIfConstOrVar(1)

    def __changeIfConstOrVar3(self):
        self.__changeIfConstOrVar(2)

    def __changeIfConstOrVar(self, num):

        forceSelect = None

        if self.__buttonVars[num].get() == 1:
           self.__listBoxes[num + 5]["state"] = DISABLED
           self.__hexEntries[num]["state"]    = NORMAL

           self.__data[num + 7] = self.__hexEntries[num]["object"].getValue()

        else:
            self.__listBoxes[num + 5]["state"] = NORMAL
            self.__hexEntries[num]["state"]    = DISABLED

            try:
                self.__data[num + 7] = self.__listBoxes[num + 5]["dataList"][
                                       self.__listBoxes[num + 5]["listBox"].curselection()[0]
                ]

            except Exception as e:
                # print(str(e))
                selector = 0
                if self.__listBoxes[num + 5]["selected"] == "" or self.__listBoxes[num + 5]["selected"] == None:
                   self.__listBoxes[num + 5]["selected"] = self.__listBoxes[num + 5]["dataList"][0].split("::")[1]

                for itemNum in range(0, len(self.__listBoxes[num + 5]["dataList"])):
                    if self.__listBoxes[num + 5]["dataList"][itemNum].split("::")[1] == self.__listBoxes[num + 5]["selected"]:
                        selector = itemNum
                        break

                self.__listBoxes[num + 5]["listBox"].select_clear(0, END)
                self.__listBoxes[num + 5]["listBox"].select_set(selector)
                self.__listBoxes[num + 5]["listBox"].yview(selector)

                self.__data[num + 7] = self.__listBoxes[num + 5]["dataList"][selector].split("::")[1]

                forceSelect = selector

        self.__listBoxes[num + 5]["listBox"].config(state = self.__listBoxes[num + 5]["state"])
        self.__hexEntries[num]["object"].changeState(self.__hexEntries[num]["state"])

        if forceSelect != None:
           self.__listBoxes[num + 5]["listBox"].config(state = NORMAL)
           self.__listBoxes[num + 5]["listBox"].select_clear(0, END)
           self.__listBoxes[num + 5]["listBox"].select_set(forceSelect)
           self.__listBoxes[num + 5]["listBox"].yview(forceSelect)

        self.__changeData(self.__data)

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