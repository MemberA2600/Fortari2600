from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from time import sleep
import re

class _3DLandScape:
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
        if "#" is data:
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

                self.__constOrVar2 = IntVar()
                self.__constButton2 = Radiobutton(f, width=99999,
                                                 text=self.__dictionaries.getWordFromCurrentLanguage("constant"),
                                                 bg=self.__colors.getColor("window"),
                                                 fg=self.__colors.getColor("font"),
                                                 justify=LEFT, font=self.__smallFont,
                                                 variable=self.__constOrVar2,
                                                 activebackground=self.__colors.getColor("highLight"),
                                                 value=1, command=self.__changeIfConstOrVar
                                                 )

                self.__constButton2.pack_propagate(False)
                self.__constButton2.pack(fill=X, side=TOP, anchor=N)

                subF = Frame(f, width=self.__w // numOf,
                                  bg=self.__loader.colorPalettes.getColor("window"),
                                  height=self.__h//30)

                subF.pack_propagate(False)
                subF.pack(side=TOP, anchor=N, fill=X)
                self.__framesAndLabels.append(f)

                self.__topBottomVar = IntVar()
                self.__topBottom = Checkbutton(subF,
                                              text=self.__dictionaries.getWordFromCurrentLanguage("verticalMir"),
                                              bg=self.__colors.getColor("window"),
                                              fg=self.__colors.getColor("font"),
                                              justify=LEFT, font=self.__miniFont,
                                              variable=self.__topBottomVar,
                                              activebackground=self.__colors.getColor("highLight"),
                                              command=self.__changeCheck
                                              )

                self.__topBottom.pack_propagate(False)
                self.__topBottom.pack(fill=Y, side=LEFT, anchor=E)

                subF = Frame(f, width=self.__w // numOf,
                                  bg=self.__loader.colorPalettes.getColor("window"),
                                  height=self.__h//30)

                subF.pack_propagate(False)
                subF.pack(side=TOP, anchor=N, fill=X)
                self.__framesAndLabels.append(f)

                self.__moveBackVar = IntVar()
                self.__moveBack = Checkbutton(subF,
                                              text=self.__dictionaries.getWordFromCurrentLanguage("moveBack"),
                                              bg=self.__colors.getColor("window"),
                                              fg=self.__colors.getColor("font"),
                                              justify=LEFT, font=self.__miniFont,
                                              variable=self.__moveBackVar,
                                              activebackground=self.__colors.getColor("highLight"),
                                              command=self.__changeCheck
                                              )

                self.__moveBack.pack_propagate(False)
                self.__moveBack.pack(fill=Y, side=LEFT, anchor=E)

                subF = Frame(f, width=self.__w // numOf,
                                  bg=self.__loader.colorPalettes.getColor("window"),
                                  height=self.__h//30)

                subF.pack_propagate(False)
                subF.pack(side=TOP, anchor=N, fill=X)
                self.__framesAndLabels.append(f)

                self.__curvedVar = IntVar()
                self.__curved = Checkbutton(subF,
                                              text=self.__dictionaries.getWordFromCurrentLanguage("curved"),
                                              bg=self.__colors.getColor("window"),
                                              fg=self.__colors.getColor("font"),
                                              justify=LEFT, font=self.__miniFont,
                                              variable=self.__curvedVar,
                                              activebackground=self.__colors.getColor("highLight"),
                                              command=self.__changeCheck
                                              )

                self.__curved.pack_propagate(False)
                self.__curved.pack(fill=Y, side=LEFT, anchor=E)

                subF = Frame(f, width=self.__w // numOf,
                                  bg=self.__loader.colorPalettes.getColor("window"),
                                  height=self.__h//30)

                subF.pack_propagate(False)
                subF.pack(side=TOP, anchor=N, fill=X)
                self.__framesAndLabels.append(f)

                self.__gapsVar = IntVar()
                self.__gaps = Checkbutton(subF,
                                              text=self.__dictionaries.getWordFromCurrentLanguage("gaps"),
                                              bg=self.__colors.getColor("window"),
                                              fg=self.__colors.getColor("font"),
                                              justify=LEFT, font=self.__miniFont,
                                              variable=self.__gapsVar,
                                              activebackground=self.__colors.getColor("highLight"),
                                              command=self.__changeCheck
                                              )

                self.__gaps.pack_propagate(False)
                self.__gaps.pack(fill=Y, side=LEFT, anchor=E)

                self.__varButton2 = Radiobutton(f, width=99999,
                                                 text=self.__dictionaries.getWordFromCurrentLanguage("variable"),
                                                 bg=self.__colors.getColor("window"),
                                                 fg=self.__colors.getColor("font"),
                                                 justify=LEFT, font=self.__smallFont,
                                                 variable=self.__constOrVar2,
                                                 activebackground=self.__colors.getColor("highLight"),
                                                 value=2, command=self.__changeIfConstOrVar
                                                 )

                self.__varButton2.pack_propagate(False)
                self.__varButton2.pack(fill=X, side=TOP, anchor=N)


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

                self.__staticColors = ["$40"]

                self.__hexEntry1 = HexEntry(self.__loader, f, self.__colors, self.__colorDict,
                                           self.__normalFont, self.__staticColors, 0, None, self.__changeHex)

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

            elif num == 2:
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

                text = self.__dictionaries.getWordFromCurrentLanguage("linesOfPattern")
                if text.endswith(":") == False: text = text + ":"

                l3 = Label(f, text=text,
                           font=self.__smallFont, fg=self.__colors.getColor("font"),
                           bg=self.__colors.getColor("window"), justify=CENTER
                           )

                l3.pack_propagate(False)
                l3.pack(side=TOP, anchor=CENTER, fill=X)

                self.__framesAndLabels.append(l3)

                self.__patternLinesVar = StringVar()
                self.__patternLines = Entry(f,
                                          name="patternLines",
                                          bg=self.__colors.getColor("boxBackNormal"),
                                          fg=self.__colors.getColor("boxFontNormal"),
                                          width=9999, justify=CENTER,
                                          textvariable=self.__patternLinesVar,
                                          font=self.__normalFont
                                          )

                self.__patternLines.pack_propagate(False)
                self.__patternLines.pack(fill=X, side=TOP, anchor=N)

                self.__patternLines.bind("<FocusOut>", self.__chamgeConst)
                self.__patternLines.bind("<KeyRelease>", self.__chamgeConst)

                text = self.__dictionaries.getWordFromCurrentLanguage("speed")
                if text.endswith(":") == False: text = text + ":"

                l4 = Label(f, text=text,
                           font=self.__smallFont, fg=self.__colors.getColor("font"),
                           bg=self.__colors.getColor("window"), justify=CENTER
                           )

                l4.pack_propagate(False)
                l4.pack(side=TOP, anchor=CENTER, fill=X)

                self.__framesAndLabels.append(l4)

                self.__speedVar = StringVar()
                self.__speed = Entry(f,
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

                    hexEntry1 = HexEntry(self.__loader, subF1, self.__colors, self.__colorDict,
                                        self.__normalFont, self.__hexValues, num2, None, self.__changeHex)

                    hexEntry2 = HexEntry(self.__loader, subF2, self.__colors, self.__colorDict,
                                        self.__normalFont, self.__hexValues, num2+15, None, self.__changeHex)

                    self.__hexEntries[num2]     = hexEntry1
                    self.__hexEntries[num2+16]  = hexEntry2

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

            if num < 2:
                l.bind("<ButtonRelease-1>", self.__changeSelected)
                l.bind("<KeyRelease-Up>", self.__changeSelected)
                l.bind("<KeyRelease-Down>", self.__changeSelected)

        self.setFields()

    def setFields(self):
        if self.isItBin(self.__data[3]) == False:

            selector = 0
            for itemNum in range(0, len(self.__listBoxes[0]["dataList"])):
                if self.__data[3] == self.__listBoxes[0]["dataList"][itemNum].split("::")[1]:
                   #self.__listBoxes[0]["selected"] = self.__listBoxes[0]["dataList"][self.__listBoxes[0]["listBox"].curselection()[0]]
                   selector = itemNum
                   break

            self.__listBoxes[0]["selected"] = self.__listBoxes[0]["dataList"][selector].split("::")[1]
            self.__data[3] = self.__listBoxes[0]["selected"]
            self.__listBoxes[0]["listBox"].select_set(selector)
            self.__topBottom.config(state = DISABLED)
            self.__moveBack.config(state = DISABLED)
            self.__curved.config(state = DISABLED)
            self.__gaps.config(state = DISABLED)
            self.__constOrVar2.set(2)
        else:
            datas = self.__data[3][1:5]
            self.__topBottomVar.set(int(datas[0]))
            self.__moveBackVar.set(int(datas[1]))
            self.__curvedVar.set(int(datas[2]))
            self.__gapsVar.set(int(datas[3]))

            self.__listBoxes[0]["listBox"].config(state = DISABLED)
            self.__listBoxes[0]["selected"] = self.__listBoxes[0]["dataList"][0].split("::")[1]
            self.__constOrVar2.set(1)


        if self.isItHex(self.__data[4]):
           self.__hexEntry1.setValue(self.__data[4])
           self.__listBoxes[1]["listBox"].config(state = DISABLED)
           self.__constOrVar.set(1)
           self.__listBoxes[1]["selected"] = self.__listBoxes[1]["dataList"][0].split("::")[1]

        else:
           self.__hexEntry1.setValue("$40")
           self.__hexEntry1.changeState(DISABLED)
           self.__listBoxes[1]["listBox"].config(state=NORMAL)
           self.__constOrVar.set(2)

           selector = 0
           for itemNum in range(0, len(self.__listBoxes[1]["dataList"])):
               if self.__data[4] == self.__listBoxes[1]["dataList"][itemNum].split("::")[1]:
                   selector = itemNum
                   break

           self.__listBoxes[1]["selected"] = self.__listBoxes[1]["dataList"][selector].split("::")[1]
           self.__data[4] = self.__listBoxes[1]["selected"]
           self.__listBoxes[1]["listBox"].select_set(selector)

        self.__numOfLinesVal.set(self.__data[5])
        self.__patternLinesVar.set(self.__data[6])
        self.__speedVar.set(self.__data[8])

        if self.__data[7] == "#":
            self.__generatePattern()
        else:
            pattern = self.__data[7].split("|")
            for num in range(0, len(pattern)):
                self.__hexEntries[num].setValue(pattern[num])

        self.turnOnOff()

    def __changeCheck(self):
        self.__data[3] = "%" + str(self.__topBottomVar.get()) + \
                               str(self.__moveBackVar.get())  + \
                               str(self.__curvedVar.get())    + \
                               str(self.__gapsVar.get())      + "0000"

        self.__changeData(self.__data)

    def turnOnOff(self):
        numOfLines = int(self.__data[6])

        for num in range(0, 32):
            if num < numOfLines:
               self.__hexEntries[num].changeState(NORMAL)
            else:
               self.__hexEntries[num].changeState(DISABLED)

    def __generatePattern(self):
        numOfLines = int(self.__data[6])
        from datetime import datetime
        from random import randint

        time = datetime.now()
        importantNum = int(str(time).split(".")[-1]) % 2

        patternSize = numOfLines

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

        result = "|".join(listOfNums)

        self.__data[7] = result
        items = result.split("|")
        for itemNum in range(0, len(items)-1):
            self.__hexEntries[itemNum].setValue(items[itemNum])

        self.__changeData(self.__data)

    def __changeSelected(self, event):
        num = 0
        for itemNum in range(0,3):
            if self.__listBoxes[itemNum]["listBox"] == event.widget:
               num = itemNum
               break

        if self.__constOrVar.get() == 1 and num == 1: return
        dataNum = 3 + num

        if self.__listBoxes[num]["selected"] != self.__listBoxes[num]["dataList"][self.__listBoxes[num]["listBox"].curselection()[0]].split("::")[1]:
           self.__listBoxes[num]["selected"] = self.__listBoxes[num]["dataList"][self.__listBoxes[num]["listBox"].curselection()[0]].split("::")[1]
           self.__data[dataNum]              = self.__listBoxes[num]["selected"]
           self.__changeData(self.__data)

    def __chamgeConst(self, event):
        constants = {
            self.__speed:        self.__speedVar,
            self.__patternLines: self.__patternLinesVar,
            self.__numOfLines:   self.__numOfLinesVal
        }

        dataNum = {
            self.__speed:        8,
            self.__patternLines: 6,
            self.__numOfLines:   5
        }

        temp = constants[event.widget].get()
        if self.isItNum(temp) == False:
            event.widget.config(
                bg=self.__colors.getColor("boxBackUnSaved"),
                fg=self.__colors.getColor("boxFontUnSaved")
            )
            return
        event.widget.config(
            bg=self.__colors.getColor("boxBackNormal"),
            fg=self.__colors.getColor("boxFontNormal")
        )

        num = int(temp)
        if num < 1 : num = 1

        if   event.widget == self.__speed:
           if num > 8: num = 8

        elif event.widget == self.__numOfLines:
           if num > 12: num = 12

        elif event.widget == self.__patternLines:
            num -= 1
            num = bin(num).replace("0b", "")
            num = num.replace("0", "1")
            num = int("0b" + num, 2)+1

            if num > 32: num = 32

        num = str(num)
        constants[event.widget].set(num)
        self.__data[dataNum[event.widget]] = str(num)
        if event.widget == self.__patternLines: self.turnOnOff()

        self.__changeData(self.__data)

    def __changeHex(self, event):
        if event.widget == self.__hexEntry1.getEntry():
           if self.__constOrVar.get() == 2: return
           colorVar = self.__hexEntry1.getValue()
           if self.isItHex(colorVar):
              colorVar = colorVar[:2] + "0"
              self.__hexEntry1.setValue(colorVar)
              self.__staticColors[0] = colorVar
              self.__data[4] = colorVar
              self.__changeData(self.__data)

        else:
            num = 0
            for itemNum in range(0, 32):
                if event.widget == self.__hexEntries[itemNum].getEntry():
                   num = itemNum
                   break

            colorVar = self.__hexEntries[num].getValue()
            if self.isItHex(colorVar):
               data = self.__data[7].split("|")
               colorVar = "$0" + colorVar[2]
               self.__hexEntries[num].setValue(colorVar)
               data[num] = colorVar
               self.__data[7] = "|".join(data)
               self.__changeData(self.__data)


    def __changeIfConstOrVar(self):
        if self.__constOrVar.get() == 1:
           self.__listBoxes[1]["listBox"].config(state = DISABLED)
           self.__hexEntry1.changeState(NORMAL)

           self.__data[4] = self.__hexEntry1.getValue()

        else:
           self.__listBoxes[1]["listBox"].config(state=NORMAL)
           self.__hexEntry1.changeState(DISABLED)

           selector = 0
           for itemNum in range(0, len(self.__listBoxes[1]["dataList"])):
               if self.__listBoxes[1]["selected"] == self.__listBoxes[1]["dataList"][itemNum].split("::")[1]:
                  selector = itemNum
                  break

           self.__listBoxes[1]["selected"] = self.__listBoxes[1]["dataList"][selector].split("::")[1]
           self.__data[4] = self.__listBoxes[1]["selected"]
           self.__listBoxes[1]["listBox"].select_clear(0, END)
           self.__listBoxes[1]["listBox"].select_set(selector)

        noUpdate = False
        if self.__constOrVar2.get() == 2:
            self.__listBoxes[0]["listBox"].config(state=NORMAL)
            self.__topBottom.config(state = DISABLED)
            self.__moveBack.config(state = DISABLED)
            self.__gaps.config(state = DISABLED)
            self.__curved.config(state = DISABLED)

            selector = 0
            for itemNum in range(0, len(self.__listBoxes[0]["dataList"])):
                if self.__listBoxes[0]["selected"] == self.__listBoxes[0]["dataList"][itemNum].split("::")[1]:
                    selector = itemNum
                    break

            self.__listBoxes[0]["selected"] = self.__listBoxes[0]["dataList"][selector].split("::")[1]
            self.__data[3] = self.__listBoxes[0]["selected"]
            self.__listBoxes[0]["listBox"].select_clear(0, END)
            self.__listBoxes[0]["listBox"].select_set(selector)
        else:
            self.__listBoxes[0]["listBox"].config(state=DISABLED)
            self.__topBottom.config(state = NORMAL)
            self.__moveBack.config(state = NORMAL)
            self.__gaps.config(state = NORMAL)
            self.__curved.config(state = NORMAL)

            self.__changeCheck()
            noUpdate = True

        if noUpdate == False: self.__changeData(self.__data)

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