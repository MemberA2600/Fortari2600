from tkinter import *

class Gradient:
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
        if data[3] == "#":
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

        self.__frame1 = Frame(self.__uniqueFrame, width=self.__w // 3,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  height=self.__h)

        self.__frame1.pack_propagate(False)
        self.__frame1.pack(side=LEFT, anchor=E, fill=Y)

        self.__frame2 = Frame(self.__uniqueFrame, width=self.__w // 3,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  height=self.__h)

        self.__frame2.pack_propagate(False)
        self.__frame2.pack(side=LEFT, anchor=E, fill=Y)

        self.__frame3 = Frame(self.__uniqueFrame, width=self.__w // 3,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  height=self.__h)

        self.__frame3.pack_propagate(False)
        self.__frame3.pack(side=LEFT, anchor=E, fill=Y)

        self.__label1 = Label(self.__frame1,
                  text=self.__dictionaries.getWordFromCurrentLanguage("dataVar") + ":",
                  font=self.__smallFont, fg=self.__colors.getColor("font"),
                  bg=self.__colors.getColor("window"), justify=CENTER
                  )

        self.__label1.pack_propagate(False)
        self.__label1.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__label2 = Label(self.__frame2,
                  text=self.__dictionaries.getWordFromCurrentLanguage("numOfLines") + ":",
                  font=self.__smallFont, fg=self.__colors.getColor("font"),
                  bg=self.__colors.getColor("window"), justify=CENTER
                  )

        self.__label2.pack_propagate(False)
        self.__label2.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__label3 = Label(self.__frame3,
                  text=self.__dictionaries.getWordFromCurrentLanguage("gradient") + ":",
                  font=self.__smallFont, fg=self.__colors.getColor("font"),
                  bg=self.__colors.getColor("window"), justify=CENTER
                  )

        self.__label3.pack_propagate(False)
        self.__label3.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__colorVars = []
        for address in self.__loader.virtualMemory.memory.keys():
            for variable in self.__loader.virtualMemory.memory[address].variables.keys():
                var = self.__loader.virtualMemory.memory[address].variables[variable]
                if ((var.type == "byte" or var.type == "nibble") and
                        (var.validity == "global" or
                         var.validity == self.__currentBank) and
                        (var.system == False or
                         var.iterable == True or
                         var.linkable == True)
                ):
                    self.__colorVars.append(address + "::" + variable)

        self.__dataVars = []
        for address in self.__loader.virtualMemory.memory.keys():
            for variable in self.__loader.virtualMemory.memory[address].variables.keys():
                var = self.__loader.virtualMemory.memory[address].variables[variable]
                if ((var.validity == "global" or
                     var.validity == self.__currentBank) and
                        (var.system == False or
                         var.iterable == True or
                         var.linkable == True)
                ):
                    self.__dataVars.append(address + "::" + variable)


        self.__scrollBar1 = Scrollbar(self.__frame1)
        self.__listBox1 = Listbox(self.__frame1, width=100000,
                       height=1000,
                       yscrollcommand=self.__scrollBar1.set,
                       selectmode=BROWSE,
                       exportselection=False,
                       font=self.__smallFont,
                       justify=LEFT
                       )

        self.__listBox1.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__listBox1.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__listBox1.pack_propagate(False)

        self.__scrollBar1.pack(side=RIGHT, anchor=W, fill=Y)
        self.__listBox1.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__scrollBar1.config(command=self.__listBox1.yview)

        for item in self.__dataVars:
            self.__listBox1.insert(END, item)

        self.__numOfLinesVar = StringVar()
        self.__numOfLines = Entry(self.__frame2,
                              bg=self.__colors.getColor("boxBackNormal"),
                              fg=self.__colors.getColor("boxFontNormal"),
                              width=9999, justify=CENTER,
                              textvariable=self.__numOfLinesVar,
                              font=self.__smallFont
                              )

        self.__numOfLines.pack_propagate(False)
        self.__numOfLines.pack(fill=Y, side=TOP, anchor=N)

        self.__label5 = Label(self.__frame2,
                  text=self.__dictionaries.getWordFromCurrentLanguage("direction") + ":",
                  font=self.__smallFont, fg=self.__colors.getColor("font"),
                  bg=self.__colors.getColor("window"), justify=CENTER
                  )

        self.__label5.pack_propagate(False)
        self.__label5.pack(side=TOP, anchor=CENTER, fill=BOTH)

        hDiv = 9

        self.__subFrameX = Frame(self.__frame2, width=self.__w // 3,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  height=self.__h//hDiv)

        self.__subFrameX.pack_propagate(False)
        self.__subFrameX.pack(side=TOP, anchor=N, fill=X)

        self.__subFrame1X = Frame(self.__subFrameX, width=self.__w // 6,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  height=self.__h//hDiv)

        self.__subFrame1X.pack_propagate(False)
        self.__subFrame1X.pack(side=LEFT, anchor=E, fill=Y)

        self.__subFrame2X = Frame(self.__subFrameX, width=self.__w // 6,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  height=self.__h//hDiv)

        self.__subFrame2X.pack_propagate(False)
        self.__subFrame2X.pack(side=LEFT, anchor=E, fill=Y)

        self.__oh = IntVar()
        self.__oh.set(int(self.__data[7]))

        self.__verButton = Radiobutton(self.__subFrame1X, width=99999,
                                         text=self.__dictionaries.getWordFromCurrentLanguage("vertical"),
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__smallFont,
                                         variable=self.__oh,
                                         activebackground=self.__colors.getColor("highLight"),
                                         activeforeground=self.__loader.colorPalettes.getColor("font"),
                                         value=1, command=self.__changeDirection
                                         )

        self.__verButton.pack_propagate(False)
        self.__verButton.pack(fill=X, side=TOP, anchor=N)

        self.__horButton = Radiobutton(self.__subFrame2X, width=99999,
                                         text=self.__dictionaries.getWordFromCurrentLanguage("horizontal"),
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__smallFont,
                                         variable=self.__oh,
                                         activebackground=self.__colors.getColor("highLight"),
                                         activeforeground=self.__loader.colorPalettes.getColor("font"),
                                         value=2, command=self.__changeDirection
                                         )

        self.__horButton.pack_propagate(False)
        self.__horButton.pack(fill=X, side=TOP, anchor=N)

        self.__leftOrRight = IntVar()
        self.__leftOrRight.set(int(self.__data[8]))

        self.__leftButton = Radiobutton(self.__subFrame1X, width=99999,
                                         text="<<",
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__smallFont,
                                         variable=self.__leftOrRight,
                                         activebackground=self.__colors.getColor("highLight"),
                                         activeforeground=self.__loader.colorPalettes.getColor("font"),
                                         value=1, command=self.__changeDirection
                                         )

        self.__leftButton.pack_propagate(False)
        self.__leftButton.pack(fill=X, side=TOP, anchor=N)

        self.__rightButton = Radiobutton(self.__subFrame2X, width=99999,
                                         text=">>",
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__smallFont,
                                         variable=self.__leftOrRight,
                                         activebackground=self.__colors.getColor("highLight"),
                                         activeforeground=self.__loader.colorPalettes.getColor("font"),
                                         value=2, command=self.__changeDirection
                                         )

        self.__rightButton.pack_propagate(False)
        self.__rightButton.pack(fill=X, side=TOP, anchor=N)

        self.__label4 = Label(self.__frame2,
                  text=self.__dictionaries.getWordFromCurrentLanguage("color") + ":",
                  font=self.__smallFont, fg=self.__colors.getColor("font"),
                  bg=self.__colors.getColor("window"), justify=CENTER
                  )

        self.__label4.pack_propagate(False)
        self.__label4.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__constOrVar = IntVar()
        self.__constButton = Radiobutton(self.__frame2, width=99999,
                                         text=self.__dictionaries.getWordFromCurrentLanguage("constant"),
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__smallFont,
                                         variable=self.__constOrVar,
                                         activebackground=self.__colors.getColor("highLight"),
                                         activeforeground=self.__loader.colorPalettes.getColor("font"),
                                         value=1, command=self.__changeIfConstOrVar
                                         )

        self.__constButton.pack_propagate(False)
        self.__constButton.pack(fill=X, side=TOP, anchor=N)

        self.__subFrame = Frame(self.__frame2, width=self.__w // 3,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  height=self.__h//hDiv)

        self.__subFrame.pack_propagate(False)
        self.__subFrame.pack(side=TOP, anchor=N, fill=X)

        self.__subFrame1 = Frame(self.__subFrame, width=self.__w // 6,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  height=self.__h//hDiv)

        self.__subFrame1.pack_propagate(False)
        self.__subFrame1.pack(side=LEFT, anchor=E, fill=Y)

        self.__subFrame2 = Frame(self.__subFrame, width=self.__w // 6,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  height=self.__h//hDiv)

        self.__subFrame2.pack_propagate(False)
        self.__subFrame2.pack(side=LEFT, anchor=E, fill=Y)

        self.__rainbowOrOther = IntVar()
        from HexEntry import HexEntry

        self.__rainbowButton = Radiobutton(self.__subFrame1, width=99999,
                                         text=self.__dictionaries.getWordFromCurrentLanguage("rainbow"),
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__smallFont,
                                         variable=self.__rainbowOrOther,
                                         activebackground=self.__colors.getColor("highLight"),
                                         activeforeground=self.__loader.colorPalettes.getColor("font"),
                                         value=1, command=self.__changeColorMode
                                         )

        self.__rainbowButton.pack_propagate(False)
        self.__rainbowButton.pack(fill=X, side=TOP, anchor=N)

        self.__oneColorButton = Radiobutton(self.__subFrame2, width=99999,
                                         text=self.__dictionaries.getWordFromCurrentLanguage("oneColor"),
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__smallFont,
                                         variable=self.__rainbowOrOther,
                                         activebackground=self.__colors.getColor("highLight"),
                                         activeforeground=self.__loader.colorPalettes.getColor("font"),
                                         value=2, command=self.__changeColorMode
                                         )

        self.__oneColorButton.pack_propagate(False)
        self.__oneColorButton.pack(fill=X, side=TOP, anchor=N)

        self.__oneColorVal   = ["$00"]
        self.__oneColorEntry = HexEntry(self.__loader, self.__subFrame2, self.__colors, self.__colorDict,
                                     self.__normalFont, self.__oneColorVal, 0, None, self.__changeHex)

        self.__varButton = Radiobutton(self.__frame2, width=99999,
                                         text=self.__dictionaries.getWordFromCurrentLanguage("variable"),
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__smallFont,
                                         variable=self.__constOrVar,
                                         activebackground=self.__colors.getColor("highLight"),
                                         activeforeground=self.__loader.colorPalettes.getColor("font"),
                                         value=2, command=self.__changeIfConstOrVar
                                         )

        self.__varButton.pack_propagate(False)
        self.__varButton.pack(fill=X, side=TOP, anchor=N)

        self.__scrollBar2 = Scrollbar(self.__frame2)
        self.__listBox2 = Listbox(self.__frame2, width=100000,
                       height=1000,
                       yscrollcommand=self.__scrollBar2.set,
                       selectmode=BROWSE,
                       exportselection=False,
                       font=self.__smallFont,
                       justify=LEFT
                       )

        self.__listBox2.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__listBox2.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__listBox2.pack_propagate(False)

        self.__scrollBar2.pack(side=RIGHT, anchor=W, fill=Y)
        self.__listBox2.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__scrollBar2.config(command=self.__listBox2.yview)

        for item in self.__colorVars:
            self.__listBox2.insert(END, item)

        if self.__data[3] == "#":
           self.__data[3] = self.__dataVars[0].split("::")[1]

        selector = 0
        for itemNum in range(0, len(self.__dataVars)):
            if self.__data[3] == self.__dataVars[itemNum].split("::")[1]:
                selector = itemNum
                break

        self.__lastSelecteds = []
        self.__lastSelecteds.append(self.__dataVars[selector].split("::")[1])
        self.__listBox1.select_set(selector)
        self.__listBox1.yview(selector)

        self.__numOfLinesVar.set(self.__data[4])

        if self.__data[5] == "#":
           self.__data[5] = self.__colorVars[0].split("::")[1]

        if self.isItHex(self.__data[5]):
           self.__constOrVar.set(1)
           self.__listBox2.config(state = DISABLED)
           self.__lastSelecteds.append(self.__colorVars[0].split("::")[1])

           if self.__data[5] == "$FF":
              self.__rainbowOrOther.set(1)
              self.__oneColorEntry.changeState(DISABLED)
           else:
              self.__rainbowOrOther.set(2)
              self.__oneColorEntry.changeState(NORMAL)
              self.__oneColorEntry.setValue(self.__data[5])
        else:
            self.__oneColorEntry.changeState(DISABLED)
            self.__rainbowButton.config(state = DISABLED)
            self.__oneColorButton.config(state = DISABLED)

            self.__constOrVar.set(2)
            selector = 0
            for itemNum in range(0, len(self.__colorVars)):
                if self.__colorVars[itemNum].split("::")[1] == self.__data[5]:
                   selector = itemNum
                   break
            self.__lastSelecteds.append(self.__colorVars[selector].split("::")[1])
            self.__listBox2.select_set(selector)
            self.__listBox2.yview(selector)


        self.__listBox1.bind("<ButtonRelease-1>", self.__changeSelected)
        self.__listBox1.bind("<KeyRelease-Up>", self.__changeSelected)
        self.__listBox1.bind("<KeyRelease-Down>", self.__changeSelected)
        self.__listBox2.bind("<ButtonRelease-1>", self.__changeSelected)
        self.__listBox2.bind("<KeyRelease-Up>", self.__changeSelected)
        self.__listBox2.bind("<KeyRelease-Down>", self.__changeSelected)
        self.__numOfLines.bind("<KeyRelease>", self.__changeEntry)
        self.__numOfLines.bind("<FocusOut>", self.__changeEntry)

        self.__hexEntries = {}
        self.__maxNum     = 32
        self.__hexFrames  = []
        perLine           = 4
        numOfLines        = self.__maxNum // perLine
        self.__hexValues  = []

        for num in range(0, self.__maxNum):
            self.__hexValues.append("$00")

        for num in range(0, numOfLines):

            h = round((self.__h // numOfLines)*0.5)

            f = Frame(self.__frame3, width=self.__w,
                      bg=self.__loader.colorPalettes.getColor("window"),
                      height= h)

            f.pack_propagate(False)
            f.pack(side=TOP, anchor=N, fill = X)

            self.__hexFrames.append(f)

            f1 = Frame(f, width=self.__w // perLine // 3,
                       bg=self.__loader.colorPalettes.getColor("window"),
                       height= h)

            f1.pack_propagate(False)
            f1.pack(side=LEFT, anchor=E, fill=Y)

            f2 = Frame(f, width=self.__w // perLine // 3,
                       bg=self.__loader.colorPalettes.getColor("window"),
                       height= h)

            f2.pack_propagate(False)
            f2.pack(side=LEFT, anchor=E, fill=Y)

            f3 = Frame(f, width=self.__w // perLine // 3,
                       bg=self.__loader.colorPalettes.getColor("window"),
                       height= h)

            f3.pack_propagate(False)
            f3.pack(side=LEFT, anchor=E, fill=Y)

            f4 = Frame(f, width=self.__w // perLine // 3,
                       bg=self.__loader.colorPalettes.getColor("window"),
                       height= h)

            f4.pack_propagate(False)
            f4.pack(side=LEFT, anchor=E, fill=Y)

            font = self.__smallFont

            hexEntry1 = HexEntry(self.__loader, f1, self.__colors, self.__colorDict,
                                 font, self.__hexValues, num, None, self.__changeHex2)

            hexEntry2 = HexEntry(self.__loader, f2, self.__colors, self.__colorDict,
                                 font, self.__hexValues, num + numOfLines, None, self.__changeHex2)

            hexEntry3 = HexEntry(self.__loader, f3, self.__colors, self.__colorDict,
                                 font, self.__hexValues, num + (numOfLines * 2), None, self.__changeHex2)

            hexEntry4 = HexEntry(self.__loader, f4, self.__colors, self.__colorDict,
                                 font, self.__hexValues, num + (numOfLines * 3), None, self.__changeHex2)

            self.__hexEntries[num]                    = hexEntry1
            self.__hexEntries[num +  numOfLines]      = hexEntry2
            self.__hexEntries[num + (numOfLines * 2)] = hexEntry3
            self.__hexEntries[num + (numOfLines * 3)] = hexEntry4

        self.__button = Button(
            self.__frame3, width=self.__w,
            bg=self.__colors.getColor("window"),
            fg=self.__colors.getColor("font"),
            font = self.__normalFont,
            command = self.generatePattern,
            text = self.__dictionaries.getWordFromCurrentLanguage("generateRandom")
            )

        self.__button.pack_propagate(False)
        self.__button.pack(side=TOP, anchor = N)

        if self.__data[6] == "#":
            self.generatePattern()
        else:
            items = self.__data[6].split("|")
            for itemNum in range(0, len(items)):
                self.__hexEntries[itemNum].setValue(items[itemNum])

        self.disabler()
        self.XYZ()

    def __changeHex2(self, event):
        selector = 0
        for entryNum in range(0, len(self.__hexEntries)):
            if self.__hexEntries[entryNum].getEntry() == event.widget:
               selector = entryNum
               break

        numOfEntry = selector
        entry = self.__hexEntries[numOfEntry]

        if self.isItHex(entry.getValue()) == False:
            event.widget.config(
                bg=self.__colors.getColor("boxBackUnSaved"),
                fg=self.__colors.getColor("boxFontUnSaved")
            )
            return

        v = entry.getValue()
        v = "$0"+v[2]
        entry.setValue(v)

        temp = self.__data[6].split("|")
        if temp[numOfEntry] != entry.getValue():
            temp[numOfEntry] = entry.getValue()
            self.__data[6] = "|".join(temp)
            self.__changeData(self.__data)

    def __changeDirection(self):
        self.__data[7] = str(self.__oh.get())
        self.__data[8] = str(self.__leftOrRight.get())

        self.XYZ()
        self.__changeData(self.__data)

    def XYZ(self):
        if self.__oh.get() == 1:
           self.__leftButton.config(state = DISABLED)
           self.__rightButton.config(state = DISABLED)
           self.__constButton.config(state = NORMAL)
           self.__varButton.config(state = NORMAL)

           self.__changeIfConstOrVar()
        else:
            self.__constButton.config(state=DISABLED)
            self.__varButton.config(state=DISABLED)
            self.__rainbowButton.config(state=DISABLED)
            self.__oneColorButton.config(state=DISABLED)
            self.__oneColorEntry.changeState(DISABLED)
            self.__listBox2.config(state=DISABLED)

            self.__constOrVar.set(1)
            self.__rainbowOrOther.set(1)
            self.__data[5] = "$FF"

            self.__leftButton.config(state=NORMAL)
            self.__rightButton.config(state=NORMAL)


    def disabler(self):
        try:
            lineNum = int(self.__numOfLinesVar.get())

            for num in range(0, self.__maxNum):
                if num+1 > lineNum:
                    self.__hexEntries[num].changeState(DISABLED)
                else:
                    self.__hexEntries[num].changeState(NORMAL)
        except:
            pass

    def generatePattern(self):
        numOfLines = int(self.__data[4])
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

        self.__data[6] = result
        items = result.split("|")
        for itemNum in range(0, len(items)):
            self.__hexEntries[itemNum].setValue(items[itemNum])

        self.__changeData(self.__data)

    def __changeEntry(self, event):
        if self.isItNum(self.__numOfLinesVar.get()) == False:
            event.widget.config(
                bg=self.__colors.getColor("boxBackUnSaved"),
                fg=self.__colors.getColor("boxFontUnSaved")
            )
            return
        event.widget.config(
            bg=self.__colors.getColor("boxBackNormal"),
            fg=self.__colors.getColor("boxFontNormal")
        )
        num = int(self.__numOfLinesVar.get())
        if num < 1            : num = 1
        if num > self.__maxNum: num = self.__maxNum

        self.__numOfLinesVar.set(str(num))
        self.__data[4] = str(num)
        self.__changeData(self.__data)
        self.disabler()

    def __changeSelected(self, event):
        if self.__constOrVar.get() == 1 and event.widget == self.__listBox2: return

        lists   = [self.__listBox1, self.__listBox2]
        values  = [self.__dataVars, self.__colorVars]
        dataNum = [3, 5]

        num = lists.index(event.widget)

        if self.__data[dataNum[num]] != values[num][event.widget.curselection()[0]].split("::")[1]:
           self.__lastSelecteds[num] = values[num][event.widget.curselection()[0]].split("::")[1]
           self.__data[dataNum[num]] = self.__lastSelecteds[num]
           self.__changeData(self.__data)

    def __changeHex(self, event):
        if self.__constOrVar.get() == 2 or self.__rainbowOrOther.get() == 1: return
        val = self.__oneColorEntry.getValue()
        if self.isItHex(val) == False:
            return

        val = val[:2] + "0"
        self.__data[5] = val
        self.__oneColorEntry.setValue(val)
        self.__changeData(self.__data)

    def __changeIfConstOrVar(self):
        if self.__constOrVar.get() == 2:
           self.__oneColorButton.config(state = DISABLED)
           self.__rainbowButton.config(state = DISABLED)
           self.__oneColorEntry.changeState(DISABLED)
           self.__listBox2.config(state = NORMAL)

           selector = 0
           for itemNum in range(0, len(self.__colorVars)):
               if self.__lastSelecteds[1] == self.__colorVars[itemNum].split("::")[1]:
                  selector = itemNum
                  break

           self.__data[5] = self.__colorVars[selector].split("::")[1]
           self.__lastSelecteds[1] = self.__data[5]
           self.__listBox2.select_clear(0, END)
           self.__listBox2.select_set(selector)
           self.__listBox2.yview(selector)

        else:
           self.__oneColorButton.config(state=NORMAL)
           self.__rainbowButton.config(state=NORMAL)
           self.__listBox2.config(state=DISABLED)

           if self.__rainbowOrOther.get() == 1:
              self.__oneColorEntry.changeState(DISABLED)
              self.__data[5] = "$FF"
           else:
              self.__oneColorEntry.changeState(NORMAL)
              if self.isItHex(self.__oneColorEntry.getValue()):
                 self.__data[5] = self.__oneColorEntry.getValue()

        self.__changeData(self.__data)

    def __changeColorMode(self):
        if self.__constOrVar.get() == 2: return
        if self.__rainbowOrOther.get() == 1:
           self.__data[5] = "$FF"
           self.__oneColorEntry.changeState(DISABLED)
           self.__changeData(self.__data)
        else:
            self.__oneColorEntry.changeState(NORMAL)
            val = self.__oneColorEntry.getValue()
            if self.isItHex(val) == False:
                return

            self.__data[5] = self.__oneColorEntry.getValue()
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