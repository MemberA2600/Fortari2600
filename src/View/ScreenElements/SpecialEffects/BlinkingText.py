from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from time import sleep
import re

class BlinkingText:

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

        self.__ctrl = False
        self.__middle = False
        self.__draw = 0

        self.dead = dead

        self.__topLevelWindow = self.__loader.topLevels[0]

        self.__topLevelWindow.bind("<KeyPress-Control_L>", self.shiftON)
        self.__topLevelWindow.bind("<KeyRelease-Control_L>", self.shiftOff)
        self.__topLevelWindow.bind("<KeyPress-Control_R>", self.shiftON)
        self.__topLevelWindow.bind("<KeyRelease-Control_R>", self.shiftOff)
        self.__topLevelWindow.bind("<Button-2>", self.drawMode)

        itWasHash = False
        if "#" in data:
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
        t = Thread(target=self.__addElementsThread)
        t.daemon = True
        t.start()


    def __addElementsThread(self):

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

        from HexEntry import HexEntry

        while self.__uniqueFrame.winfo_width() < 2:
            sleep(0.00001)

        secondH = round(self.__uniqueFrame.winfo_width() * 0.43)

        self.__upperFrame = Frame(self.__uniqueFrame, width=self.__w,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=round(secondH // 3 * 1.75))

        self.__upperFrame.pack_propagate(False)
        self.__upperFrame.pack(side=TOP, anchor=N, fill=X)

        self.__bottomFrame = Frame(self.__uniqueFrame, width=self.__w,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=secondH // 3)

        self.__bottomFrame.pack_propagate(False)
        self.__bottomFrame.pack(side=TOP, anchor=N, fill=BOTH)

        self.__coloumns    = []
        self.__subColoumns = []

        t = Thread(target=self.__createMatrix)
        t.daemon = True
        t.start()

        self.__labels = []
        text = [self.__dictionaries.getWordFromCurrentLanguage("container"),
                self.__dictionaries.getWordFromCurrentLanguage("colorVar"),
                self.__dictionaries.getWordFromCurrentLanguage("speed"),
                self.__dictionaries.getWordFromCurrentLanguage("gradient")
                ]

        for num in range(0, len(text)):
            if text[num][-1] != ":": text[num] = text[num] + ":"

        self.__listBoxes = []
        datas = [self.__containers, self.__colorVars]

        maxNum = 5
        self.__staticColors = ["$16", "$44"]

        self.__colorThings    = []
        self.__gradientThings = []

        for num in range(0, maxNum):
            f = Frame(self.__upperFrame, width=self.__w // maxNum,
                                      bg=self.__loader.colorPalettes.getColor("window"),
                                      height=round(secondH // 3 * 1.75))

            f.pack_propagate(False)
            f.pack(side=LEFT, anchor=E, fill=Y)

            self.__coloumns.append(f)

            if num == 0:
                for num2 in range(0, 2):

                    f1 = Frame(f, width=self.__w // maxNum,
                                              bg=self.__loader.colorPalettes.getColor("window"),
                                              height=round(secondH // 3 * 1.75) // 2)

                    f1.pack_propagate(False)
                    f1.pack(side=TOP, anchor=N, fill=X)

                    self.__subColoumns.append(f1)

                    l = Label(f1, text=text[num],
                              font=self.__smallFont, fg=self.__colors.getColor("font"),
                              bg=self.__colors.getColor("window"), justify=CENTER
                              )

                    l.pack_propagate(False)
                    l.pack(side=TOP, anchor=CENTER, fill=X)

                    self.__labels.append(l)
                    self.__listBoxes.append({})

                    s = Scrollbar(f1)
                    l = Listbox(f1, width=100000,
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

                    self.__listBoxes[-1]["listBox"]     = l
                    self.__listBoxes[-1]["selected"]    = ""
                    self.__listBoxes[-1]["scrollBar"]   = s
                    self.__listBoxes[-1]["dataList"]    = datas[num]

                    for item in self.__listBoxes[-1]["dataList"]:
                        l.insert(END, item)

            elif num in (1, 2):
                self.__colorThings.append({})

                f1 = Frame(f, width=self.__w // maxNum,
                           bg=self.__loader.colorPalettes.getColor("window"),
                           height=secondH // 3)

                f1.pack_propagate(False)
                f1.pack(side=TOP, anchor=N, fill=X)

                f2 = Frame(f, width=self.__w // maxNum,
                           bg=self.__loader.colorPalettes.getColor("window"),
                           height=secondH // 3)

                f2.pack_propagate(False)
                f2.pack(side=TOP, anchor=N, fill=X)

                self.__subColoumns.append(f1)
                self.__subColoumns.append(f2)

                l = Label(f1, text=text[1],
                          font=self.__smallFont, fg=self.__colors.getColor("font"),
                          bg=self.__colors.getColor("window"), justify=CENTER
                          )

                l.pack_propagate(False)
                l.pack(side=TOP, anchor=CENTER, fill=X)
                self.__labels.append(l)

                v = IntVar()

                commands = [self.__changeIfConstOrVar1,self.__changeIfConstOrVar2]

                b = Radiobutton(f1, width=99999,
                                                 text=self.__dictionaries.getWordFromCurrentLanguage("constant"),
                                                 bg=self.__colors.getColor("window"),
                                                 fg=self.__colors.getColor("font"),
                                                 justify=LEFT, font=self.__smallFont,
                                                 variable=v,
                                                 activebackground=self.__colors.getColor("highLight"),
                                                 activeforeground=self.__loader.colorPalettes.getColor("font"),
                                                 value=1, command=commands[num-1]
                                                 )

                b.pack_propagate(False)
                b.pack(fill=X, side=TOP, anchor=N)

                hex = HexEntry(self.__loader, f1, self.__colors, self.__colorDict,
                                           self.__normalFont, self.__staticColors, num-1, None, self.__changeHex)

                self.__colorThings[-1]["variable"]    = v
                self.__colorThings[-1]["constButton"] = b
                self.__colorThings[-1]["hexEntry"]    = hex
                self.__colorThings[-1]["hexValue"]    = self.__staticColors[num-1]

                b = Radiobutton(f2, width=99999,
                                                 text=self.__dictionaries.getWordFromCurrentLanguage("variable"),
                                                 bg=self.__colors.getColor("window"),
                                                 fg=self.__colors.getColor("font"),
                                                 justify=LEFT, font=self.__smallFont,
                                                 variable=v,
                                                 activebackground=self.__colors.getColor("highLight"),
                                                 activeforeground=self.__loader.colorPalettes.getColor("font"),
                                                 value=2, command=commands[num-1]
                                                 )

                b.pack_propagate(False)
                b.pack(fill=X, side=TOP, anchor=N)

                self.__listBoxes.append({})

                s = Scrollbar(f2)
                l = Listbox(f2, width=100000,
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

                self.__listBoxes[-1]["listBox"] = l
                self.__listBoxes[-1]["selected"] = ""
                self.__listBoxes[-1]["scrollBar"] = s
                self.__listBoxes[-1]["dataList"] = datas[1]

                for item in self.__listBoxes[-1]["dataList"]:
                    l.insert(END, item)

                self.__colorThings[-1]["varButton"] = b
                self.__colorThings[-1]["listBox"]   = self.__listBoxes[-1]

                if num == 1:
                    l = Label(f1, text=text[2],
                              font=self.__smallFont, fg=self.__colors.getColor("font"),
                              bg=self.__colors.getColor("window"), justify=CENTER
                              )

                    l.pack_propagate(False)
                    l.pack(side=TOP, anchor=CENTER, fill=X)
                    self.__labels.append(l)

                    self.__speedVar = StringVar()
                    self.__speed = Entry(f1,
                                         name="speed",
                                         bg=self.__colors.getColor("boxBackNormal"),
                                         fg=self.__colors.getColor("boxFontNormal"),
                                         width=9999, justify=CENTER,
                                         textvariable=self.__speedVar,
                                         font=self.__normalFont
                                         )

                    self.__speed.pack_propagate(False)
                    self.__speed.pack(fill=X, side=TOP, anchor=N)

                    self.__speed.bind("<FocusOut>", self.__chamgeConst)
                    self.__speed.bind("<KeyRelease>", self.__chamgeConst)

            elif num > 2:
                l = Label(f, text=text[3],
                          font=self.__smallFont, fg=self.__colors.getColor("font"),
                          bg=self.__colors.getColor("window"), justify=CENTER
                          )

                l.pack_propagate(False)
                l.pack(side=TOP, anchor=CENTER, fill=X)
                self.__labels.append(l)

                self.__gradientThings.append({})
                self.__gradientThings[-1]["hexEntries"] = []
                self.__gradientThings[-1]["hexValues"]  = []
                self.__gradientThings[-1]["button"]    = []

                for num2 in range(0, 8):
                    self.__gradientThings[-1]["hexValues"].append("$00")

                    h =      HexEntry(self.__loader, f, self.__colors, self.__colorDict,
                             self.__smallFont, self.__gradientThings[-1]["hexValues"],
                             num2, None, self.__changeHex)

                    self.__gradientThings[-1]["hexEntries"].append(h)

                genPatterns = [self.__generatePattern1, self.__generatePattern2]

                button = Button(
                        f, width=self.__w,
                        bg=self.__colors.getColor("window"),
                        fg=self.__colors.getColor("font"),
                        activebackground=self.__loader.colorPalettes.getColor("highLight"),
                        activeforeground=self.__loader.colorPalettes.getColor("font"),
                        font=self.__normalFont,
                        command=genPatterns[num-3],
                        text=self.__dictionaries.getWordFromCurrentLanguage("generateRandom")
                    )

                button.pack_propagate(False)
                button.pack(side=TOP, anchor = N, fill = BOTH)

                self.__gradientThings[-1]["button"].append(button)

        for num in range(0, len(self.__listBoxes)):
            listBox = self.__listBoxes[num]["listBox"]
            listBox.bind("<ButtonRelease-1>", self.__changeListBox)
            listBox.bind("<KeyRelease-Up>", self.__changeListBox)
            listBox.bind("<KeyRelease-Down>", self.__changeListBox)

        if self.__data[3] == "#": self.__data[3] = self.__listBoxes[0]["dataList"][0].split("::")[1]
        if self.__data[4] == "#": self.__data[4] = self.__listBoxes[1]["dataList"][0].split("::")[1]

        if self.__data[8] == "#": self.__generatePattern(0)
        else:
           items = self.__data[8].split("|")
           for itemNum in range(0, len(items)):
               self.__gradientThings[0]["hexValues"][itemNum]  = items[itemNum]
               self.__gradientThings[0]["hexEntries"][itemNum].setValue(items[itemNum])

        if self.__data[9] == "#": self.__generatePattern(1)
        else:
           items = self.__data[9].split("|")
           for itemNum in range(0, len(items)):
               self.__gradientThings[1]["hexValues"][itemNum]  = items[itemNum]
               self.__gradientThings[1]["hexEntries"][itemNum].setValue(items[itemNum])

        container1 = self.__data[3]
        container2 = self.__data[4]
        foreGround = self.__data[5]
        backGround = self.__data[6]
        speed      = self.__data[7]


        self.setSelectOnListBox(0, container1)
        self.setSelectOnListBox(1, container2)

        for colorNum in range(0, 2):
            colors = [foreGround, backGround]
            if self.isItHex(self.__data[5+colorNum]) == True:
               self.__colorThings[colorNum]["variable"].set(1)
               self.__colorThings[colorNum]["hexEntry"].setValue(colors[colorNum])
               self.__colorThings[colorNum]["hexValue"] = colors[colorNum]

               self.__colorThings[colorNum]["listBox"]["listBox"].config(state = DISABLED)
            else:
               self.__colorThings[colorNum]["variable"].set(2)
               self.__colorThings[colorNum]["hexEntry"].changeState(DISABLED)

               self.setSelectOnListBox(colorNum + 2, colors[colorNum])

        self.__speedVar.set(speed)

#        self.__changeData(self.__data)

    def __createMatrix(self):
        while self.__bottomFrame.winfo_width() < 2: sleep(0.00001)

        noOfRows    = 8
        noOfColumns = 64

        w = round(self.__bottomFrame.winfo_width()  // noOfColumns * 1.02)
        h = round(self.__bottomFrame.winfo_height() * 0.80) // noOfRows

        self.__matrixRowFrames  = []
        self.__matrixCellFrames = []
        self.__matrixButtons    = []

        matrix = self.__data[10]

        self.__matrixValues = []

        for startIndex in range(0, 512, 64):
            line = matrix[startIndex:startIndex+64]
            self.__matrixValues.append([])
            for charIndex in range(0, 64):
                self.__matrixValues[-1].append(line[charIndex])

        for num in range(0, noOfRows):

            f = Frame(self.__bottomFrame, width=w,
                       bg=self.__loader.colorPalettes.getColor("window"),
                       height=h )

            f.pack_propagate(False)
            f.pack(side=TOP, anchor=N, fill=X)

            self.__matrixRowFrames.append(f)
            self.__matrixCellFrames.append([])
            self.__matrixButtons.append([])
            self.__soundPlayer.playSound("Pong")

            for num2 in range(0, noOfColumns):
                sf = Frame(f, width=w,
                          bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                          height=h)

                sf.pack_propagate(False)
                sf.pack(side=RIGHT, anchor=W, fill=Y)

                b = Button(sf, height = w, width = h, name = str(num) + "_" + str(num2),
                            bg = self.__loader.colorPalettes.getColor("boxBackNormal"),
                           activebackground = self.__loader.colorPalettes.getColor("highLight"),
                           relief=GROOVE, state = DISABLED
                           )
                b.pack_propagate(False)
                b.pack(side=LEFT, anchor=E, fill = BOTH)

                if self.__matrixValues[num][num2] == "1":
                   b.config(bg = self.__loader.colorPalettes.getColor("boxFontNormal"))

                self.__matrixCellFrames[-1].append(sf)
                self.__matrixButtons[-1].append(b)

        self.genBottomBottom()

        for listOfButtons in self.__matrixButtons:
            for button in listOfButtons:
                button.config(state = NORMAL)
                button.bind("<Button-1>", self.__clicked)
                button.bind("<Button-3>", self.__clicked)
                button.bind("<Enter>", self.__enter)

    def genBottomBottom(self):
        self.__bottomOfBottom = Frame(self.__bottomFrame, height=9999999, width=999999,
                                      bg=self.__loader.colorPalettes.getColor("window"),
                                      )
        self.__bottomOfBottom.pack_propagate(False)
        self.__bottomOfBottom.pack(side=TOP, anchor=N, fill=BOTH)

        self.__entryFrame = Frame(self.__bottomOfBottom, height=9999999,
                                  width=round(self.__bottomFrame.winfo_width() * 0.75),
                                  bg=self.__loader.colorPalettes.getColor("window"),
                                  )
        self.__entryFrame.pack_propagate(False)
        self.__entryFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__genButtonFrame = Frame(self.__bottomOfBottom, height=9999999,
                                      width=round(self.__bottomFrame.winfo_width() * 0.75),
                                      bg=self.__loader.colorPalettes.getColor("window"),
                                      )
        self.__genButtonFrame.pack_propagate(False)
        self.__genButtonFrame.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__textVar = StringVar()
        self.__text = Entry(self.__entryFrame,
                            name="fuck",
                            bg=self.__colors.getColor("boxBackNormal"),
                            fg=self.__colors.getColor("boxFontNormal"),
                            width=9999, justify=CENTER,
                            textvariable=self.__textVar,
                            font=self.__normalFont
                            )

        self.__text.pack_propagate(False)
        self.__text.pack(fill=X, side=TOP, anchor=N)

        self.__text.bind("<FocusOut>", self.__chamgeConstText)
        self.__text.bind("<KeyRelease>", self.__chamgeConstText)

        self.__genButton = Button(
            self.__genButtonFrame, width=999999,
            bg=self.__colors.getColor("window"),
            fg=self.__colors.getColor("font"),
            activebackground=self.__loader.colorPalettes.getColor("highLight"),
            activeforeground=self.__loader.colorPalettes.getColor("font"),
            font=self.__normalFont,
            command=self.__generateText,
            text=self.__dictionaries.getWordFromCurrentLanguage("generateText")
        )

        self.__genButton.pack_propagate(False)
        self.__genButton.pack(side=TOP, anchor=N, fill=BOTH)

    def __generateText(self):
        text = self.__textVar.get()
        textToReturn = ["", "", "", "", "", "", "", ""]
        first = True

        for letter in text:
            if first == True:
               first = False
            else:
               for num in range(0, 8):
                   textToReturn[num] += "0"

            letterData = self.__loader.fontManager.getAtariChar(letter)
            for num in range(0, 8):
                textToReturn[num] += letterData[num]

        adder     = 64 - len(textToReturn[0])
        halfAdder = adder // 2

        for num in range(0, 8):
            textToReturn[num] = (halfAdder * "0") + textToReturn[num] + ((adder - halfAdder) * "0")
            textToReturn[num] =  textToReturn[num][::-1]
            for charNum in range(0,64):
                self.__matrixValues[num][charNum] = textToReturn[num][charNum]
                if textToReturn[num][charNum] == "1":
                   self.__matrixButtons[num][charNum].config(bg = self.__colors.getColor("boxFontNormal"))
                else:
                   self.__matrixButtons[num][charNum].config(bg=self.__colors.getColor("boxBackNormal"))

        newString = ""
        for numList in self.__matrixValues:
            newString += "".join(numList)

        self.__data[10] = newString
        self.__changeData(self.__data)

    def __chamgeConstText(self, event):
        self.__textVar.set(self.__textVar.get()[:10])

    def __clicked(self, event):
        name = str(event.widget).split(".")[-1]
        theY = int(name.split("_")[0])
        theX = int(name.split("_")[1])

        self.__matrixValues[theY][theX] = str(1 - int(self.__matrixValues[theY][theX]))
        if self.__matrixValues[theY][theX] == "1":
           event.widget.config(bg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        else:
           event.widget.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))

        newString = ""
        for numList in self.__matrixValues:
            newString += "".join(numList)

        self.__data[10] = newString
        self.__changeData(self.__data)

    def __enter(self, event):
        if self.__draw == 0: return
        self.__clicked(event)

    def shiftON(self, event):
        self.__ctrl = True

    def shiftOff(self, event):
        self.__ctrl = False

    def drawMode(self, event):
        if self.__draw == 1:
           self.__draw = 0
        else:
           self.__draw = 1


    def __changeListBox(self, event):
        boxNum  = 0
        listBox = event.widget
        for num in range(0, len(self.__listBoxes)):
            if listBox == self.__listBoxes[num]["listBox"]:
               boxNum = num

        currentSelectedIndex = self.__listBoxes[boxNum]["listBox"].curselection()[0]
        currentSelected      = self.__listBoxes[boxNum]["dataList"][currentSelectedIndex].split("::")[1]
        self.__listBoxes[boxNum]["selected"] = currentSelected

        self.setSelectOnListBox(boxNum, currentSelected)

        self.__data[boxNum + 3] = currentSelected
        self.__changeData(self.__data)


    def setSelectOnListBox(self, boxNum, currentValue):
        self.__listBoxes[boxNum]["listBox"].select_clear(0, END)
        selector = 0
        for itemNum in range(0, len(self.__listBoxes[boxNum]["dataList"])):
            item = self.__listBoxes[boxNum]["dataList"][itemNum].split("::")[1]
            if item == currentValue:
               selector = itemNum
               break

        self.__listBoxes[boxNum]["selected"] = self.__listBoxes[boxNum]["dataList"][selector].split("::")[1]
        self.__listBoxes[boxNum]["listBox"].select_set(selector)

    def __generatePattern1(self):
        self.__generatePattern(0)

    def __generatePattern2(self):
        self.__generatePattern(1)

    def __generatePattern(self, thatNum):
        numOfLines = 8
        patternSize = 3

        from datetime import datetime
        from random import randint

        time = datetime.now()
        importantNum = int(str(time).split(".")[-1]) % 2

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
            currentNum += changerList[r] * randint(1, 3)
            if currentNum < 0: currentNum = 1
            if currentNum > 7: currentNum = 6

            listOfNums.append(patterns[currentNum])

        result = "|".join(listOfNums) + "|" + "|".join(deepcopy(listOfNums[::-1]))

        self.__data[8+thatNum] = result

        items = result.split("|")

        for itemNum in range(0, len(items)):
            self.__gradientThings[thatNum]["hexEntries"][itemNum].setValue(items[itemNum])
            self.__gradientThings[thatNum]["hexValues"][itemNum] = items[itemNum]

        self.__changeData(self.__data)


    def __chamgeConst(self, event):
        while True:
            try:
                that = self.__speedVar.get()
                if that != "":
                   number = int(that)
                else:
                   return
                break
            except:
                self.__speedVar.set(self.__speedVar.get()[:-1])
            sleep(0.00001)

        if number < 0: number = 0
        if number > 3: number = 3

        self.__speedVar.set(str(number))
        self.__data[7] = str(number)
        self.__changeData(self.__data)

    def __changeIfConstOrVar1(self):
        self.__changeIfConstOrVar(0)

    def __changeIfConstOrVar2(self):
        self.__changeIfConstOrVar(1)

    def __changeIfConstOrVar(self, poz):
        newValue = self.__colorThings[poz]["variable"].get()

        hexEntry     = self.__colorThings[poz]["hexEntry"]
        hexVal       = self.__colorThings[poz]["hexValue"]

        listBox      = self.__colorThings[poz]["listBox"]["listBox"]
        listSelected = self.__colorThings[poz]["listBox"]["selected"]

        if newValue  == 1:
           hexEntry.changeState(NORMAL)
           listBox.config(state = DISABLED)

           self.__data[poz + 5] = hexVal
        else:
           hexEntry.changeState(DISABLED)
           listBox.config(state=NORMAL)

           self.__data[poz + 5] = listSelected
           self.setSelectOnListBox(poz+2, listSelected)

        self.__changeData(self.__data)

    def __changeHex(self, event):
        entry    = event.widget
        hexEntry = None
        home     = None
        entryNum = 0
        subNum   = None

        for num in range(0, 2):
            if entry == self.__colorThings[num]["hexEntry"].getEntry():
               hexEntry = self.__colorThings[num]["hexEntry"]
               home     = self.__colorThings
               entryNum = num
               break

        if home == None:
           for num in range(0, 2):
               for num2 in range(0, 8):
                   if entry == self.__gradientThings[num]["hexEntries"][num2].getEntry():
                      hexEntry = self.__gradientThings[num]["hexEntries"][num2]
                      entryNum = num
                      subNum   = num2
                      home     = self.__gradientThings
                      break

        if self.isItHex(hexEntry.getValue()) == False: return

        newVal = hexEntry.getValue()
        if len(newVal) == 2:
           newVal += "0"

        hexEntry.setValue(newVal)
        if home == self.__colorThings:
           self.__colorThings[entryNum]["hexValue"] = newVal
           self.__data[entryNum + 5] = newVal

        else:
           self.__gradientThings[entryNum]["hexValues"][subNum] = newVal

           items = []
           for num in range(0, 8):
               items.append(self.__gradientThings[entryNum]["hexValues"][num])

           self.__data[entryNum + 8] = "|".join(items)


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