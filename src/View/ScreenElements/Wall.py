from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from time import sleep

from ScreenSetterFrameBase import ScreenSetterFrameBase

class Wall:

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
        self.__maxNum = 24

        self.__loadPictures()
        self.__loadVariables()

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
        self.__listOfPictures = []

        import os

        for root, dirs, files in os.walk(self.__loader.mainWindow.projectPath + "bigSprites/"):
            for file in files:
                if file.endswith(".asm"):
                    f = open(root + "/" + file)
                    text = f.read().replace("\r", "").split("\n")
                    f.close()

                    try:
                        mode = text[3].split("Mode=")[1]
                    except:
                        mode = None
                    if mode in ("simple", "overlay"):
                        self.__listOfPictures.append(file.replace(".asm", "") + "_(Big)")

        for root, dirs, files in os.walk(self.__loader.mainWindow.projectPath + "sprites/"):
            for file in files:

                if file.endswith(".asm"):
                    self.__listOfPictures.append(file.replace(".asm", "") + "_(Normal)")


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

        from HexEntry import HexEntry

        for num in range(0, maxFrames):

            if num in range(0,3):
                f = Frame(self.__uniqueFrame, width=self.__w // maxFrames,
                                      bg=self.__loader.colorPalettes.getColor("window"),
                                      height=self.__h)

                f.pack_propagate(False)
                f.pack(side=LEFT, anchor=E, fill=Y)

                self.__framesAndLabels.append(f)

                f1 = Frame(f, width=self.__w // maxFrames,
                          bg=self.__loader.colorPalettes.getColor("window"),
                          height=self.__h // 2.25)

                f1.pack_propagate(False)
                f1.pack(side=TOP, anchor=N, fill=X)

                text = self.__dictionaries.getWordFromCurrentLanguage("dataVar")
                if text.endswith(":") == False: text = text + ":"

                l1 = Label(f1,        text=text,
                                      font=self.__smallFont, fg=self.__colors.getColor("font"),
                                      bg=self.__colors.getColor("window"), justify=CENTER
                                      )

                l1.pack_propagate(False)
                l1.pack(side=TOP, anchor=CENTER, fill=BOTH)

                self.__framesAndLabels.append([f1, l1])

                f2 = Frame(f, width=self.__w // maxFrames,
                           bg=self.__loader.colorPalettes.getColor("window"),
                           height=self.__h)

                f2.pack_propagate(False)
                f2.pack(side=TOP, anchor=N, fill=BOTH)

                text = self.__dictionaries.getWordFromCurrentLanguage("dataVar")
                if text.endswith(":") == False: text = text + ":"

                l2 = Label(f2, text=text,
                           font=self.__smallFont, fg=self.__colors.getColor("font"),
                           bg=self.__colors.getColor("window"), justify=CENTER
                           )

                l2.pack_propagate(False)
                l2.pack(side=TOP, anchor=CENTER, fill=BOTH)

                self.__framesAndLabels.append([f2, l2])

                frames = [f1, f2]
                for num2 in range(0, 2):
                    self.__listBoxes.append({})

                    s = Scrollbar(frames[num2])
                    l = Listbox(frames[num2], width=100000,
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

                    for item in self.__byteVars:
                        l.insert(END, item)

                    self.__listBoxes[-1]["listBox"]     = l
                    self.__listBoxes[-1]["selected"]    = ""
                    self.__listBoxes[-1]["scrollBar"]   = s
                    self.__listBoxes[-1]["dataList"]    = self.__byteVars

            elif num == 3:

                f = Frame(self.__uniqueFrame, width=self.__w // maxFrames,
                                      bg=self.__loader.colorPalettes.getColor("window"),
                                      height=self.__h)

                f.pack_propagate(False)
                f.pack(side=LEFT, anchor=E, fill=Y)

                self.__framesAndLabels.append(f)

                text = self.__dictionaries.getWordFromCurrentLanguage("color")
                if text.endswith(":") == False: text = text + ":"

                l = Label(f,         text=text,
                                      font=self.__smallFont, fg=self.__colors.getColor("font"),
                                      bg=self.__colors.getColor("window"), justify=CENTER
                                      )

                l.pack_propagate(False)
                l.pack(side=TOP, anchor=CENTER, fill=BOTH)

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

                self.__staticColors = ["$20"]

                self.__hexEntry1 = HexEntry(self.__loader, f, self.__colors, self.__colorDict,
                                            self.__normalFont, self.__staticColors, 0, None, self.__changeHex)

                text = self.__dictionaries.getWordFromCurrentLanguage("index")
                if text.endswith(":") == False: text = text + ":"

                l2 = Label(f,         text=text,
                                      font=self.__smallFont, fg=self.__colors.getColor("font"),
                                      bg=self.__colors.getColor("window"), justify=CENTER
                                      )

                l2.pack_propagate(False)
                l2.pack(side=TOP, anchor=CENTER, fill=BOTH)

                self.__framesAndLabels.append(l2)

                self.__indexNumVal = StringVar()
                self.__indexNum = Entry(f,
                                          name="indexNum",
                                          bg=self.__colors.getColor("boxBackNormal"),
                                          fg=self.__colors.getColor("boxFontNormal"),
                                          width=9999, justify=CENTER,
                                          textvariable=self.__indexNumVal,
                                          font=self.__normalFont
                                          )

                self.__indexNum.pack_propagate(False)
                self.__indexNum.pack(fill=X, side=TOP, anchor=N)

                self.__indexNum.bind("<FocusOut>", self.__chamgeConst)
                self.__indexNum.bind("<KeyRelease>", self.__chamgeConst)

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

                for item in self.__byteVars:
                    l.insert(END, item)

                self.__listBoxes[-1]["listBox"] = l
                self.__listBoxes[-1]["selected"] = ""
                self.__listBoxes[-1]["scrollBar"] = s
                self.__listBoxes[-1]["dataList"] = self.__byteVars

            elif num == 4:
                f = Frame(self.__uniqueFrame, width=self.__w // maxFrames,
                                      bg=self.__loader.colorPalettes.getColor("window"),
                                      height=self.__h)

                f.pack_propagate(False)
                f.pack(side=LEFT, anchor=E, fill=Y)

                self.__framesAndLabels.append(f)

                text = self.__dictionaries.getWordFromCurrentLanguage("sprite")
                if text.endswith(":") == False: text = text + ":"

                l = Label(f,         text=text,
                                      font=self.__smallFont, fg=self.__colors.getColor("font"),
                                      bg=self.__colors.getColor("window"), justify=CENTER
                                      )

                l.pack_propagate(False)
                l.pack(side=TOP, anchor=CENTER, fill=BOTH)

                self.__hasSprite = IntVar()
                self.__emptySprite = Radiobutton(f, width=99999,
                                                 text=self.__dictionaries.getWordFromCurrentLanguage("none"),
                                                 bg=self.__colors.getColor("window"),
                                                 fg=self.__colors.getColor("font"),
                                                 justify=LEFT, font=self.__smallFont,
                                                 variable=self.__hasSprite,
                                                 activebackground=self.__colors.getColor("highLight"),
                                                 value=1, command=self.__hasSpriteOrNone
                                                 )

                self.__emptySprite.pack_propagate(False)
                self.__emptySprite.pack(fill=X, side=TOP, anchor=N)

                text = self.__dictionaries.getWordFromCurrentLanguage("numOfLines")
                if text.endswith(":") == False: text = text + ":"

                l = Label(f,         text=text,
                                      font=self.__smallFont, fg=self.__colors.getColor("font"),
                                      bg=self.__colors.getColor("window"), justify=CENTER
                                      )

                l.pack_propagate(False)
                l.pack(side=TOP, anchor=CENTER, fill=BOTH)

                self.__numOfLinesVal = StringVar()
                self.__numOfLines = Entry(f,
                                          name="lineNum",
                                          bg=self.__colors.getColor("boxBackNormal"),
                                          fg=self.__colors.getColor("boxFontNormal"),
                                          width=9999, justify=CENTER,
                                          textvariable=self.__numOfLinesVal,
                                          font=self.__normalFont
                                          )

                self.__numOfLines.pack_propagate(False)
                self.__numOfLines.pack(fill=X, side=TOP, anchor=N)

                self.__numOfLines.bind("<FocusOut>", self.__chamgeConst)
                self.__numOfLines.bind("<KeyRelease>", self.__chamgeConst)

                self.__setSprite = Radiobutton(f, width=99999,
                                                 text=self.__dictionaries.getWordFromCurrentLanguage("custom"),
                                                 bg=self.__colors.getColor("window"),
                                                 fg=self.__colors.getColor("font"),
                                                 justify=LEFT, font=self.__smallFont,
                                                 variable=self.__hasSprite,
                                                 activebackground=self.__colors.getColor("highLight"),
                                                 value=2, command=self.__hasSpriteOrNone
                                                 )

                self.__setSprite.pack_propagate(False)
                self.__setSprite.pack(fill=X, side=TOP, anchor=N)

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

                for item in self.__listOfPictures:
                    l.insert(END, item)

                self.__listBoxes[-1]["listBox"] = l
                self.__listBoxes[-1]["selected"] = ""
                self.__listBoxes[-1]["scrollBar"] = s
                self.__listBoxes[-1]["dataList"] = self.__listOfPictures
            elif num == 5:
                f = Frame(self.__uniqueFrame, width=self.__w // maxFrames,
                                      bg=self.__loader.colorPalettes.getColor("window"),
                                      height=self.__h)

                f.pack_propagate(False)
                f.pack(side=LEFT, anchor=E, fill=Y)

                self.__framesAndLabels.append(f)

                text = self.__dictionaries.getWordFromCurrentLanguage("gradient")
                if text.endswith(":") == False: text = text + ":"

                l = Label(f,         text=text,
                                      font=self.__smallFont, fg=self.__colors.getColor("font"),
                                      bg=self.__colors.getColor("window"), justify=CENTER
                                      )

                l.pack_propagate(False)
                l.pack(side=TOP, anchor=CENTER, fill=BOTH)

                self.__hexValues  = []

                for num2 in range(0, self.__maxNum):
                    self.__hexValues.append("$00")

                    hexEntry1 = HexEntry(self.__loader, f, self.__colors, self.__colorDict,
                                        self.__smallFont, self.__hexValues, num2, None, self.__changeHex)

                    self.__hexEntries.append(hexEntry1)

                self.__button = Button(
                        f, width=self.__w,
                        bg=self.__colors.getColor("window"),
                        fg=self.__colors.getColor("font"),
                        font=self.__normalFont,
                        command=self.generatePattern,
                        text=self.__dictionaries.getWordFromCurrentLanguage("generateRandom")
                    )

                self.__button.pack_propagate(False)
                self.__button.pack(side=TOP, anchor=N)

        for num in range(0,6):
            if self.__data[num + 2] == "#":
               self.__data[num + 2] = self.__listBoxes[num]["dataList"][0].split("::")[1]

            selector = 0
            for itemNum in range(0, len(self.__listBoxes[num]["dataList"])):
                if self.__data[num + 2] == self.__listBoxes[num]["dataList"][itemNum].split("::")[1]:
                    selector = itemNum
                    break

            self.__listBoxes[num]["selected"] = self.__listBoxes[num]["dataList"][selector].split("::")[1]
            self.__listBoxes[num]["listBox"].select_set(selector)

        if self.isItHex(self.__data[8]) == True:
            self.__listBoxes[6]["listBox"].config(state = DISABLED)
            self.__hexEntry1.changeState(NORMAL)
            self.__hexEntry1.setValue(self.__data[8][:2]+"0")
            self.__listBoxes[6]["selected"] = self.__listBoxes[6]["dataList"][0].split("::")[1]
            self.__constOrVar.set(1)

            self.__indexNum.config(state = NORMAL)
            self.__indexNumVal.set(str(int("0x" + self.__data[8][2], 16)))

        else:
            self.__listBoxes[6]["listBox"].config(state = NORMAL)
            self.__hexEntry1.changeState(DISABLED)
            self.__staticColors = ["$20"]

            selector = 0
            for itemNum in range(0, len(self.__listBoxes[6]["dataList"])):
                if self.__data[8] == self.__listBoxes[6]["dataList"][itemNum].split("::")[1]:
                    selector = itemNum
                    break

            self.__listBoxes[6]["selected"] = self.__listBoxes[6]["dataList"][selector].split("::")[1]
            self.__listBoxes[6]["listBox"].select_set(selector)
            self.__indexNum.config(state = DISABLED)
            self.__indexNumVal.set("0")

            self.__constOrVar.set(2)

        if self.__data[9] == "*None*":
           self.__hasSprite.set(1)
           self.__numOfLines.config(state = NORMAL)

           self.__numOfLinesVal.set(self.__data[10])
           self.__listBoxes[7]["listBox"].select_set(0)
           self.__listBoxes[7]["selected"] = self.__listBoxes[7]["dataList"][0]
           self.__listBoxes[7]["listBox"].config(state = DISABLED)

        else:
           self.__hasSprite.set(2)
           self.__numOfLines.config(state=DISABLED)
           self.__listBoxes[7]["listBox"].config(state = NORMAL)

           selector = 0
           for itemNum in range(0, len(self.__listBoxes[7]["dataList"])):
                if self.__data[9] == self.__listBoxes[7]["dataList"][itemNum]:
                    selector = itemNum
                    break

           self.__listBoxes[7]["selected"] = self.__listBoxes[7]["dataList"][selector]
           self.__listBoxes[7]["listBox"].select_set(selector)

           self.__numOfLinesVal.set(str(self.__loadAndGetLineSize(self.__listBoxes[7]["selected"])))


        for listNum in range(0, len(self.__listBoxes)):
            l = self.__listBoxes[listNum]["listBox"]
            l.bind("<ButtonRelease-1>", self.__changeSelected)
            l.bind("<KeyRelease-Up>", self.__changeSelected)
            l.bind("<KeyRelease-Down>", self.__changeSelected)


        if self.__data[11] == "#":
            self.generatePattern()
        else:
            datas = self.__data[11].split("|")
            for itemNum in range(0, self.__maxNum):
                self.__hexEntries[itemNum].setValue(datas[itemNum])

        self.turnOnOff()

    def __changeSelected(self, event):
        listNum = 0

        for lNum in range(0, len(self.__listBoxes)):
            if self.__listBoxes[lNum]["listBox"] == event.widget:
                listNum = lNum

        if (listNum == 6 and self.__constOrVar.get() == 1) or (listNum == 8 and self.__hasSprite.get() == 7): return


        if listNum == 7:
            if self.__listBoxes[listNum]["selected"] != self.__listBoxes[listNum]["dataList"][ self.__listBoxes[listNum]["listBox"].curselection()[0] ]:
                self.__listBoxes[listNum]["selected"] = self.__listBoxes[listNum]["dataList"][ self.__listBoxes[listNum]["listBox"].curselection()[0]]
                self.__data[listNum + 2] = self.__listBoxes[listNum]["selected"]
                self.__data[10] = str(self.__loadAndGetLineSize(self.__data[9]))

                self.__changeData(self.__data)

        else:
            if self.__listBoxes[listNum]["selected"] != self.__listBoxes[listNum]["dataList"][ self.__listBoxes[listNum]["listBox"].curselection()[0] ].split("::")[1]:
                self.__listBoxes[listNum]["selected"] = self.__listBoxes[listNum]["dataList"][ self.__listBoxes[listNum]["listBox"].curselection()[0]].split("::")[1]
                self.__data[listNum + 2] = self.__listBoxes[listNum]["selected"]
                self.__changeData(self.__data)

    def __loadAndGetLineSize(self, fileName):
        name = fileName.split("_(")[0]
        typ  = fileName.split("_(")[1][:-1]

        if typ == "Normal":
           longName = self.__loader.mainWindow.projectPath + "sprites/"+name+".asm"
        else:
           longName = self.__loader.mainWindow.projectPath + "bigSprites/" + name + ".asm"

        f = open(longName, "r")
        text = f.read().replace("\r", "").split("\n")
        f.close()

        return int(text[0].split("Height=")[1])

    def turnOnOff(self):
        numOfLines = int(self.__data[10])

        for num in range(0, self.__maxNum):
            if num < numOfLines:
               self.__hexEntries[num].changeState(NORMAL)
            else:
               self.__hexEntries[num].changeState(DISABLED)

    def generatePattern(self):
        numOfLines = int(self.__data[10])
        from datetime import datetime
        from random import randint

        time = datetime.now()
        importantNum = int(str(time).split(".")[-1]) % 2

        patternSize = (numOfLines // 2 + numOfLines % 2) - 1

        patterns = {
            0: "$00",
            1: "$02",
            2: "$04",
            3: "$06",
            4: "$08",
            5: "$0A",
            6: "$0C",
            7: "$0E",
        }

        changer = [[1, 1, 1, -1, -1], [1, 1, -1, -1, -1]]

        currentNum = importantNum * 7
        changerList = changer[importantNum]

        listOfNums = [patterns[currentNum]]

        for num in range(0, patternSize):
            r = randint(0, 4)
            currentNum += changerList[r]
            if currentNum < 0: currentNum = 1
            if currentNum > 7: currentNum = 6

            listOfNums.append(patterns[currentNum])

        result = ""
        if numOfLines % 2 == 0:
            result = "|".join(listOfNums) + "|" + "|".join(listOfNums[::-1])
        else:
            result = "|".join(listOfNums[:-1]) + "|" + "|".join(listOfNums[::-1])

        self.__data[11] = result
        items = result.split("|")
        for itemNum in range(0, len(items)):
            self.__hexEntries[itemNum].setValue(items[itemNum])

        self.__changeData(self.__data)

    def __changeIfConstOrVar(self):
        if self.__constOrVar.get() == 1:
           self.__hexEntry1.changeState(NORMAL)
           self.__listBoxes[6]["listBox"].config(state = DISABLED)
           self.__indexNum.config(state = NORMAL)
           self.__data[8] = self.__hexEntry1.getValue()[:2] + hex(int(self.__indexNumVal.get())).replace("0x", "")

        else:
           self.__hexEntry1.changeState(DISABLED)
           self.__listBoxes[6]["listBox"].config(state=NORMAL)
           self.__data[8] = self.__listBoxes[6]["selected"]
           self.__indexNum.config(state = DISABLED)

           selector = 0
           for itemNum in range(0, len(self.__listBoxes[6]["dataList"])):
               try:
                   if self.__listBoxes[6]["selected"] == self.__listBoxes[6]["dataList"][ self.__listBoxes[6]["listBox"].curselection()[0] ].split("::")[1]:
                      selector = itemNum
                      break
               except:
                   pass

           self.__listBoxes[6]["listBox"].select_clear(0, END)
           self.__listBoxes[6]["listBox"].select_set(selector)

           self.__data[8] = self.__listBoxes[6]["selected"]

        self.__changeData(self.__data)

    def __hasSpriteOrNone(self):
        if self.__hasSprite.get() == 1:
           self.__numOfLines.config(state = NORMAL)
           self.__listBoxes[7]["listBox"].config(state = DISABLED)
           self.__data[10] = self.__numOfLinesVal.get()
           self.__data[9]  = "*None*"
        else:
           self.__numOfLines.config(state=DISABLED)
           self.__listBoxes[7]["listBox"].config(state=NORMAL)

           selector = 0
           try:
               for itemNum in range(0, len(self.__listBoxes[7]["dataList"])):
                   if self.__listBoxes[7]["selected"] == self.__listBoxes[7]["dataList"][ self.__listBoxes[7]["listBox"].curselection()[0] ]:
                      selector = itemNum
                      break
           except:
               pass

           self.__listBoxes[7]["listBox"].select_clear(0, END)
           self.__listBoxes[7]["listBox"].select_set(selector)

           self.__data[9]  = self.__listBoxes[7]["selected"]
           self.__data[10] = str(self.__loadAndGetLineSize(self.__data[9]))

        self.__changeData(self.__data)
        self.turnOnOff()

    def __changeHex(self, event):
        if event.widget == self.__hexEntry1.getEntry():
           if self.__constOrVar.get() == 2: return
           colorVar = self.__hexEntry1.getValue()
           if self.isItHex(colorVar):
              colorVar = colorVar[:2] + "0"
              self.__hexEntry1.setValue(colorVar)
              self.__staticColors[0] = colorVar
              self.__data[8] = colorVar[:2] + hex(int(self.__indexNumVal.get())).replace("0x", "")
              self.__changeData(self.__data)

        else:
            num = 0
            for itemNum in range(0, self.__maxNum):
                if event.widget == self.__hexEntries[itemNum].getEntry():
                   num = itemNum
                   break

            colorVar = self.__hexEntries[num].getValue()
            if self.isItHex(colorVar):
               data = self.__data[11].split("|")
               colorVar = "$0" + colorVar[2]
               self.__hexEntries[num].setValue(colorVar)
               data[num] = colorVar
               self.__data[11] = "|".join(data)
               self.__changeData(self.__data)

    def __chamgeConst(self, event):
        if event.widget == self.__numOfLines:
            if self.__hasSprite.get() == 2: return

            if self.isItNum(self.__numOfLinesVal.get()) == False:
                event.widget.config(
                    bg=self.__colors.getColor("boxBackUnSaved"),
                    fg=self.__colors.getColor("boxFontUnSaved")
                )
                return
            event.widget.config(
                bg=self.__colors.getColor("boxBackNormal"),
                fg=self.__colors.getColor("boxFontNormal")
            )

            num = int(self.__numOfLinesVal.get())

            if num < 1: num = 1
            if num > self.__maxNum : num = self.__maxNum

            self.__numOfLinesVal.set(str(num))
            self.__data[10] = self.__numOfLinesVal.get()
            self.__changeData(self.__data)
            self.turnOnOff()
        else:
            if self.__constOrVar.get() == 2: return
            if self.isItNum(self.__indexNumVal.get()) == False:
                event.widget.config(
                    bg=self.__colors.getColor("boxBackUnSaved"),
                    fg=self.__colors.getColor("boxFontUnSaved")
                )
                return
            event.widget.config(
                bg=self.__colors.getColor("boxBackNormal"),
                fg=self.__colors.getColor("boxFontNormal")
            )

            num = int(self.__indexNumVal.get())

            if num < 0: num = 0
            if num > 15: num = 15

            self.__indexNumVal.set(str(num))
            self.__data[8] = self.__hexEntry1.getValue()[:2] + hex(int(self.__indexNumVal.get())).replace("0x", "")
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