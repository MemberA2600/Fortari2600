from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from time import sleep
import re


class SevenDigits:
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

        self.__loadPictures()

        itWasHash = False
        if data[3] == "#":
            itWasHash = True

        self.__addElements()
        if itWasHash == True:
            self.__changeData(data)

    def __loadPictures(self):

        self.__listOfPictures  = []

        import os

        for root, dirs, files in os.walk(self.__loader.mainWindow.projectPath + "bigSprites/"):
            for file in files:
                ok   = False
                mode = ""
                frames = 0

                if file.endswith(".asm"):
                    f = open(root + "/" + file, "r")
                    text = f.read()
                    f.close()

                    firstLine  = text.replace("\r", "").split("\n")[0]
                    secondLine = text.replace("\r", "").split("\n")[1]
                    fourthLine = text.replace("\r", "").split("\n")[3]

                    if "Height" in firstLine:
                        try:
                            num = int(firstLine.split("=")[1])
                            if num == 8:
                                ok = True
                            else:
                                ok = False
                        except:
                            pass

                    if ok == True:
                       if "Mode=double" in fourthLine:
                           ok = False
                       else:
                           ok = True

                           if "Mode=simple" in fourthLine:
                               mode = "simple"
                           else:
                               mode = "overlay"

                    if ok == True:

                        try:
                            frames = int(secondLine.split("=")[1])
                        except:
                            pass

                        if mode == "simple" and frames > 9:
                            self.__listOfPictures.append(file.replace(".asm", "") + "_(Big)")

        for root, dirs, files in os.walk(self.__loader.mainWindow.projectPath + "sprites/"):
            for file in files:
                ok = False
                frames = 0

                if file.endswith(".asm"):
                    f = open(root + "/" + file, "r")
                    text = f.read()
                    f.close()

                    firstLine = text.replace("\r", "").split("\n")[0]
                    secondLine = text.replace("\r", "").split("\n")[1]
                    frames = 0

                    if "Height" in firstLine:
                        try:
                            num = int(firstLine.split("=")[1])
                            if num == 8:
                                ok = True
                        except:
                            pass

                    if ok == True:
                        try:
                            frames = int(secondLine.split("=")[1])
                        except:
                            pass

                        if frames > 9:
                            self.__listOfPictures.append(file.replace(".asm", "") + "_(Normal)")

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

        self.__frame1 = Frame(self.__uniqueFrame, width=self.__w // 6,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h)

        self.__frame1.pack_propagate(False)
        self.__frame1.pack(side=LEFT, anchor=E, fill=Y)

        self.__frame2 = Frame(self.__uniqueFrame, width=self.__w // 6,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h)

        self.__frame2.pack_propagate(False)
        self.__frame2.pack(side=LEFT, anchor=E, fill=Y)

        self.__frame3 = Frame(self.__uniqueFrame, width=self.__w // 6,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h)

        self.__frame3.pack_propagate(False)
        self.__frame3.pack(side=LEFT, anchor=E, fill=Y)

        self.__frame4 = Frame(self.__uniqueFrame, width=self.__w // 6,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h)

        self.__frame4.pack_propagate(False)
        self.__frame4.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__frame5 = Frame(self.__uniqueFrame, width=self.__w // 6,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h)

        self.__frame5.pack_propagate(False)
        self.__frame5.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__frame6 = Frame(self.__uniqueFrame, width=self.__w // 6,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h)

        self.__frame6.pack_propagate(False)
        self.__frame6.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__lastDigit = 10
        dataVars     = self.__data[3:self.__lastDigit]
        digitNum     = self.__data[self.__lastDigit]
        slotMode     = self.__data[self.__lastDigit+1]
        color        = self.__data[self.__lastDigit+3]
        font         = self.__data[self.__lastDigit+4]

        self.__label1 = Label(self.__frame1,
                              text=self.__dictionaries.getWordFromCurrentLanguage("dataVar") + ":",
                              font=self.__smallFont, fg=self.__colors.getColor("font"),
                              bg=self.__colors.getColor("window"), justify=CENTER
                              )

        self.__label1.pack_propagate(False)
        self.__label1.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__label2 = Label(self.__frame2,
                              text=self.__dictionaries.getWordFromCurrentLanguage("dataVar") + ":",
                              font=self.__smallFont, fg=self.__colors.getColor("font"),
                              bg=self.__colors.getColor("window"), justify=CENTER
                              )

        self.__label2.pack_propagate(False)
        self.__label2.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__label3 = Label(self.__frame3,
                              text=self.__dictionaries.getWordFromCurrentLanguage("dataVar") + ":",
                              font=self.__smallFont, fg=self.__colors.getColor("font"),
                              bg=self.__colors.getColor("window"), justify=CENTER
                              )

        self.__label3.pack_propagate(False)
        self.__label3.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__label4 = Label(self.__frame4,
                              text=self.__dictionaries.getWordFromCurrentLanguage("dataVar") + ":",
                              font=self.__smallFont, fg=self.__colors.getColor("font"),
                              bg=self.__colors.getColor("window"), justify=CENTER
                              )

        self.__label4.pack_propagate(False)
        self.__label4.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__frame1_1 = Frame(self.__frame1, width=self.__w // 6,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h // 3)

        self.__frame1_1.pack_propagate(False)
        self.__frame1_1.pack(side=TOP, anchor=N, fill=X)

        self.__frame1_2 = Frame(self.__frame2, width=self.__w // 6,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h // 3)

        self.__frame1_2.pack_propagate(False)
        self.__frame1_2.pack(side=TOP, anchor=N, fill=X)

        self.__frame1_3 = Frame(self.__frame3, width=self.__w // 6,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h // 3)

        self.__frame1_3.pack_propagate(False)
        self.__frame1_3.pack(side=TOP, anchor=N, fill=X)

        self.__frame1_4 = Frame(self.__frame4, width=self.__w // 6,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h // 3)

        self.__frame1_4.pack_propagate(False)
        self.__frame1_4.pack(side=TOP, anchor=N, fill=X)



        w = ((self.__w // 7) * 2 ) // 3
        h = self.__h // 6

        self.__byteVars = []
        for address in self.__loader.virtualMemory.memory.keys():
            for variable in self.__loader.virtualMemory.memory[address].variables.keys():
                var = self.__loader.virtualMemory.memory[address].variables[variable]
                if ((var.validity == "global" or
                     var.validity == self.__currentBank) and
                     var.type     == "byte" and
                        (var.system == False or
                         var.iterable == True or
                         var.linkable == True)
                ):
                    self.__byteVars.append(address + "::" + variable)

        self.__nibbleVars = []
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
                    self.__nibbleVars.append(address + "::" + variable)


        self.__varListBoxes         = []
        varListBoxScrollBars        = []
        self.__varBoxSettings       = []


        frames = [self.__frame1_1, self.__frame1,
                  self.__frame1_2, self.__frame2,
                  self.__frame1_3, self.__frame3,
                  self.__frame1_4
                  ]

        for frame in frames:
            __varListBoxScrollBar = Scrollbar(frame)
            __varListBox = Listbox(frame, width=100000,
                                             height=1000,
                                             yscrollcommand=__varListBoxScrollBar.set,
                                             selectmode=BROWSE,
                                             exportselection=False,
                                             font=self.__smallFont,
                                             justify=LEFT
                                             )

            __varListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
            __varListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
            __varListBox.pack_propagate(False)

            __varListBoxScrollBar.pack(side=RIGHT, anchor=W, fill=Y)
            __varListBox.pack(side=LEFT, anchor=W, fill=BOTH)
            __varListBoxScrollBar.config(command=__varListBox.yview)
            self.__varListBoxes.append(__varListBox)
            varListBoxScrollBars.append(__varListBoxScrollBar)
            self.__varBoxSettings.append("byte")

        self.__varListBox1 = self.__varListBoxes[0]
        self.__varListBox2 = self.__varListBoxes[1]
        self.__varListBox3 = self.__varListBoxes[2]
        self.__varListBox4 = self.__varListBoxes[3]
        self.__varListBox5 = self.__varListBoxes[4]
        self.__varListBox6 = self.__varListBoxes[5]
        self.__varListBox7 = self.__varListBoxes[6]


        self.__digitLabel = Label(self.__frame5,
                              text=self.__dictionaries.getWordFromCurrentLanguage("numOfDigits") + ":",
                              font=self.__smallFont, fg=self.__colors.getColor("font"),
                              bg=self.__colors.getColor("window"), justify=CENTER
                              )

        self.__digitLabel.pack_propagate(False)
        self.__digitLabel.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__digitNum = StringVar()

        if self.isItNum(digitNum) == True:
            self.__digitNum.set(digitNum)
        else:
            self.__digitNum.set("7")

        self.__digitsEntry = Entry(self.__frame5,
                                   bg=self.__colors.getColor("boxBackNormal"),
                                   fg=self.__colors.getColor("boxFontNormal"),
                                   width=9999, justify=CENTER,
                                   textvariable=self.__digitNum,
                                   font=self.__smallFont
                                   )

        self.__digitsEntry.pack_propagate(False)
        self.__digitsEntry.pack(fill=X, side=TOP, anchor=N)

        self.__digitsEntry.bind("<KeyRelease>", self.__changeDigits)
        self.__digitsEntry.bind("<FocusOut>", self.__changeDigits)

        self.__lastSelecteds = ["", "", "", "", "", "", ""]

        self.__slotMode = IntVar()
        self.__slotMode.set(int(slotMode))

        for itemNum in range(0, len(dataVars)):
            if dataVars[itemNum] == "#":
               self.__lastSelecteds[itemNum] = self.__nibbleVars[0].split("::")[1]
               self.__data[itemNum+3]        = self.__nibbleVars[0].split("::")[1]
            else:
               self.__lastSelecteds[itemNum] = dataVars[itemNum]

        self.__slotButton = Checkbutton(self.__frame5, width=99999,
                                             text=self.__dictionaries.getWordFromCurrentLanguage("slotMachine"),
                                             bg=self.__colors.getColor("window"),
                                             fg=self.__colors.getColor("font"),
                                             justify=LEFT, font=self.__smallFont,
                                             variable=self.__slotMode,
                                             activebackground=self.__colors.getColor("highLight"),
                                             activeforeground=self.__loader.colorPalettes.getColor("font"),
                                             command=self.__slotChanged
                                             )

        self.__slotButton.pack_propagate(False)
        self.__slotButton.pack(fill=X, side=TOP, anchor=N)

        for varListBox in self.__varListBoxes:
            varListBox.bind("<ButtonRelease-1>", self.__changeVar)
            varListBox.bind("<KeyRelease-Up>", self.__changeVar)
            varListBox.bind("<KeyRelease-Down>", self.__changeVar)

        self.__fillDataVarListBoxes(False, True)

        self.__fontLabel = Label(self.__frame5,
                              text=self.__dictionaries.getWordFromCurrentLanguage("spriteName") + ":",
                              font=self.__smallFont, fg=self.__colors.getColor("font"),
                              bg=self.__colors.getColor("window"), justify=CENTER
                              )

        self.__fontLabel.pack_propagate(False)
        self.__fontLabel.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__fontOptionFrame1_1   = Frame(self.__frame5, width=self.__w // 7,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height = self.__h // 17)

        self.__fontOptionFrame1_1.pack_propagate(False)
        self.__fontOptionFrame1_1.pack(side=TOP, anchor=N, fill=X)

        self.__fontOptionFrame1_2   = Frame(self.__frame5, width=self.__w // 7,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height = self.__h // 17)

        self.__fontOptionFrame1_2.pack_propagate(False)
        self.__fontOptionFrame1_2.pack(side=TOP, anchor=N, fill=X)

        self.__fontOptionFrame1_3   = Frame(self.__frame5, width=self.__w // 7,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height = self.__h // 17)

        self.__fontOptionFrame1_3.pack_propagate(False)
        self.__fontOptionFrame1_3.pack(side=TOP, anchor=N, fill=X)

        self.__fontOption1 = IntVar()

        self.__fontOptionButton1_1 = Radiobutton(self.__fontOptionFrame1_1, width=999999,
                                         text=self.__dictionaries.getWordFromCurrentLanguage("default"),
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__smallFont,
                                         variable=self.__fontOption1,
                                         activebackground=self.__colors.getColor("highLight"),
                                         activeforeground=self.__loader.colorPalettes.getColor("font"),
                                         value=1, command=self.__changedFontOption1
                                         )

        self.__fontOptionButton1_1.pack_propagate(False)
        self.__fontOptionButton1_1.pack(fill=X, side=TOP, anchor=N)

        self.__fontOptionButton1_2 = Radiobutton(self.__fontOptionFrame1_2, width=999999,
                                         text=self.__dictionaries.getWordFromCurrentLanguage("digital"),
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__smallFont,
                                         variable=self.__fontOption1,
                                         activebackground=self.__colors.getColor("highLight"),
                                         activeforeground=self.__loader.colorPalettes.getColor("font"),
                                         value=2, command=self.__changedFontOption2
                                         )

        self.__fontOptionButton1_2.pack_propagate(False)
        self.__fontOptionButton1_2.pack(fill=X, side=TOP, anchor=N)

        self.__fontOptionButton1_3 = Radiobutton(self.__fontOptionFrame1_3, width=999999,
                                         text=self.__dictionaries.getWordFromCurrentLanguage("custom"),
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__smallFont,
                                         variable=self.__fontOption1,
                                         activebackground=self.__colors.getColor("highLight"),
                                         activeforeground=self.__loader.colorPalettes.getColor("font"),
                                         value=3, command=self.__changedFontOption3
                                         )

        self.__fontOptionButton1_3.pack_propagate(False)
        self.__fontOptionButton1_3.pack(fill=X, side=TOP, anchor=N)

        self.__fontVarListScrollBar1 = Scrollbar(self.__frame5)
        self.__fontVarListBox1 = Listbox(self.__frame5, width=100000,
                                         height=1000,
                                         yscrollcommand=self.__fontVarListScrollBar1.set,
                                         selectmode=BROWSE,
                                         exportselection=False,
                                         font=self.__smallFont,
                                         justify=LEFT
                                         )

        self.__fontVarListBox1.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__fontVarListBox1.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__fontVarListBox1.pack_propagate(False)

        self.__fontVarListScrollBar1.pack(side=RIGHT, anchor=W, fill=Y)
        self.__fontVarListBox1.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__fontVarListBoxSelected = ""

        self.__fontVarListScrollBar1.config(command=self.__fontVarListBox1.yview)

        for item in self.__listOfPictures: self.__fontVarListBox1.insert(END, item)

        if len(self.__listOfPictures) == 0:
           self.__fontOptionButton1_3.config(state = DISABLED)
           font = "default"

        self.__changedFontData(font)
        self.__saveIt = self.__fontOption1.get()

        self.__fontVarListBox1.bind("<ButtonRelease-1>", self.__changeFontVar)
        self.__fontVarListBox1.bind("<KeyRelease-Up>", self.__changeFontVar)
        self.__fontVarListBox1.bind("<KeyRelease-Down>", self.__changeFontVar)

        from GradientFrame import GradientFrame
        self.__gradientFrame = GradientFrame(self.__loader, self.__frame6,
                                             self.__changeData, self.__h, self.__data, self.dead, 8, "small", self.__lastDigit+2)

        self.__colorSettings = IntVar()
        self.__colorConstButton = Radiobutton(self.__frame4, width=99999,
                                         text=self.__dictionaries.getWordFromCurrentLanguage("constant"),
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__smallFont,
                                         variable=self.__colorSettings,
                                         activebackground=self.__colors.getColor("highLight"),
                                         activeforeground=self.__loader.colorPalettes.getColor("font"),
                                         value=1, command=self.colorSettingsChange1
                                         )

        self.__colorConstButton.pack_propagate(False)
        self.__colorConstButton.pack(fill=X, side=TOP, anchor=N)

        from HexEntry import HexEntry
        self.__fuckinColors = ["$16"]

        if self.isItHex(color): self.__fuckinColors[0] = color
        self.__colorEntry = HexEntry(self.__loader, self.__frame4, self.__colors, self.__colorDict,
                                     self.__normalFont, self.__fuckinColors, 0, None, self.__chengeMainColor)

        self.__colorVarButton = Radiobutton(self.__frame4, width=99999,
                                         text=self.__dictionaries.getWordFromCurrentLanguage("variable"),
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__smallFont,
                                         variable=self.__colorSettings,
                                         activebackground=self.__colors.getColor("highLight"),
                                         activeforeground=self.__loader.colorPalettes.getColor("font"),
                                         value=2, command=self.colorSettingsChange2
                                         )
        self.__colorVarButton.pack_propagate(False)
        self.__colorVarButton.pack(fill=X, side=TOP, anchor=N)

        self.__colorVarListScrollBar1 = Scrollbar(self.__frame4)
        self.__colorVarListBox1 = Listbox(self.__frame4, width=100000,
                                         height=1000,
                                         yscrollcommand=self.__colorVarListScrollBar1.set,
                                         selectmode=BROWSE,
                                         exportselection=False,
                                         font=self.__smallFont,
                                         justify=LEFT
                                         )

        self.__colorVarListBox1.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__colorVarListBox1.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__colorVarListBox1.pack_propagate(False)

        self.__colorVarListScrollBar1.pack(side=RIGHT, anchor=W, fill=Y)
        self.__colorVarListBox1.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__colorVarListBoxSelected = ""
        self.__colorVarListScrollBar1.config(command=self.__colorVarListBox1.yview)

        for item in self.__nibbleVars: self.__colorVarListBox1.insert(END, item)

        self.__colorVarListBox1.bind("<ButtonRelease-1>", self.__changeColorVar)
        self.__colorVarListBox1.bind("<KeyRelease-Up>", self.__changeColorVar)
        self.__colorVarListBox1.bind("<KeyRelease-Down>", self.__changeColorVar)

        if self.isItHex(color):
           self.__colorSettings.set(1)
           self.__colorVarListBox1.config(state = DISABLED)
        else:
           self.__colorSettings.set(2)
           self.__colorEntry.changeState(DISABLED)

           selector = 0
           for itemNum in range(0, len(self.__nibbleVars)):
               if color == self.__nibbleVars[itemNum].split("::")[1]:
                  selector = itemNum
                  self.__colorVarListBoxSelected = color
                  break

           self.__colorVarListBox1.select_set(selector)
           self.__colorVarListBox1.yview(selector)


    def colorSettingsChange1(self):
        self.__colorVarListBoxSelected = self.__nibbleVars[self.__colorVarListBox1.curselection()[0]]
        self.__colorVarListBox1.config(state = DISABLED)
        self.__colorEntry.changeState(NORMAL)

        self.__colorVarListBox1.select_clear(0, END)
        self.__data[self.__lastDigit+3] = self.__colorEntry.getValue()
        self.__changeData(self.__data)

    def colorSettingsChange2(self):
        self.__colorVarListBox1.config(state = NORMAL)
        self.__colorEntry.changeState(DISABLED)

        selected = 0
        for itemNum in range(0, len(self.__nibbleVars)):
            if self.__colorVarListBoxSelected == self.__nibbleVars[itemNum].split("::")[1]:
               selected = itemNum
               break

        self.__colorVarListBox1.select_set(selected)
        self.__colorVarListBox1.yview(selected)

        self.__data[self.__lastDigit+3] = self.__nibbleVars[selected].split("::")[1]
        self.__changeData(self.__data)


    def __changeColorVar(self, event):
        if self.__colorSettings.get() == 1: return

        if self.__colorVarListBoxSelected != self.__nibbleVars[self.__colorVarListBox1.curselection()[0]]:
           self.__colorVarListBoxSelected  = self.__nibbleVars[self.__colorVarListBox1.curselection()[0]].split("::")[1]
           self.__data[self.__lastDigit+3] = self.__colorVarListBoxSelected
           self.__changeData(self.__data)

    def __changeFontVar(self, event):
        if self.__fontOption1.get() != 3: return
        if self.__fontVarListBoxSelected   != self.__listOfPictures[self.__fontVarListBox1.curselection()[0]]:
           self.__fontVarListBoxSelected   = self.__listOfPictures[self.__fontVarListBox1.curselection()[0]]
           self.__data[self.__lastDigit+4] = self.__fontVarListBoxSelected
           self.__changeData(self.__data)

    def __changedFontData(self, data):
        if   data == "default":
             self.__fontOption1.set(1)
             try:
                 self.__fontVarListBoxSelected = self.__listOfPictures[self.__fontVarListBox1.curselection()[0]]
             except:
                 self.__fontVarListBoxSelected = self.__listOfPictures[0]

             self.__fontVarListBox1.select_clear(0, END)
             self.__fontVarListBox1.config(state = DISABLED)
             self.__data[self.__lastDigit+4] = data

        elif data == "digital":
             self.__fontOption1.set(2)
             try:
                 self.__fontVarListBoxSelected = self.__listOfPictures[self.__fontVarListBox1.curselection()[0]]
             except:
                 self.__fontVarListBoxSelected = self.__listOfPictures[0]

             self.__fontVarListBox1.select_clear(0, END)
             self.__fontVarListBox1.config(state = DISABLED)
             self.__data[self.__lastDigit+4] = data

        else:
            self.__fontOption1.set(3)
            self.__fontVarListBox1.config(state = NORMAL)

            self.__fontVarListBoxSelected = data

            foundIt = False

            for itemNum in range(0, len(self.__listOfPictures)):
                if self.__listOfPictures[itemNum] == self.__fontVarListBoxSelected:
                   self.__fontVarListBox1.select_set(itemNum)
                   self.__fontVarListBox1.yview(itemNum)

                   self.__data[self.__lastDigit+4] = data
                   foundIt = True
                   break

            if foundIt == False:
                self.__fontOption1.set(2)
                try:
                    self.__fontVarListBoxSelected = self.__listOfPictures[self.__fontVarListBox1.curselection()[0]]
                except:
                    self.__fontVarListBoxSelected = self.__listOfPictures[0]

                self.__fontVarListBox1.select_clear(0, END)
                self.__fontVarListBox1.config(state=DISABLED)
                self.__data[self.__lastDigit+4] = data



    def __changedFontOption1(self):
        self.__changedFontOption(self.__fontOptionButton1_1)

    def __changedFontOption2(self):
        self.__changedFontOption(self.__fontOptionButton1_2)

    def __changedFontOption3(self):
        self.__changedFontOption(self.__fontOptionButton1_3)

    def __changedFontOption(self, widget):
        www = {
            self.__fontOptionButton1_1: "default",
            self.__fontOptionButton1_2: "digital",
            self.__fontOptionButton1_3: self.__fontVarListBoxSelected
        }
        self.__changedFontData(www[widget])

        if self.__saveIt != self.__fontOption1.get(): self.__changeData(self.__data)
        self.__saveIt = self.__fontOption1.get()


    def __chengeMainColor(self, event):
        if self.__colorSettings == 2: return

        if self.__colorEntry.getValue() != self.__data[self.__lastDigit+3]:
            temp = self.__colorEntry.getValue()
            if self.isItHex(temp) == True:
                temp = temp[:2] + "6"
                self.__data[self.__lastDigit+3] = temp
                self.__colorEntry.setValue(temp)
                self.__changeData(self.__data)

    def __changeDigits(self, event):
        if self.isItNum(self.__digitNum.get()) == False:
            self.__digitsEntry.config(
                bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                fg=self.__loader.colorPalettes.getColor("boxFontUnSaved")
            )
        else:
            self.__digitsEntry.config(
                bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                fg=self.__loader.colorPalettes.getColor("boxFontNormal")
            )
            if self.__digitNum.get() != self.__data[self.__lastDigit]:
                temp = self.__digitNum.get()
                if int(temp) > 7:
                    temp = "7"
                elif int(temp) < 1:
                    temp = "1"
                self.__digitNum.set(temp)
                self.__data[self.__lastDigit] = self.__digitNum.get()

        self.__fillDataVarListBoxes(True, False)
        self.__fillDataVarListBoxes(True, False)


    def __changeVar(self, event):
        lists = {
            "nibble": self.__nibbleVars,
            "byte": self.__byteVars
        }

        widget = event.widget
        varListNum = 0

        for varBoxNum in range(0, len(self.__varListBoxes)):
            if widget == self.__varListBoxes[varBoxNum]:
               varListNum = varBoxNum
               break

        activeNum = self.__getActiveNum()
        if varListNum + 1 > activeNum:
           return

        settingsDependingOnDigitNum = self.__getSettingsDependingOnDigitNum()
        typ      = settingsDependingOnDigitNum[varListNum]
        listType = lists[typ]

        if self.__lastSelecteds[varListNum] != listType[widget.curselection()[0]].split("::")[1]:
           self.__lastSelecteds[varListNum] = listType[widget.curselection()[0]].split("::")[1]
           self.__data[3+varListNum]        = self.__lastSelecteds[varListNum]
           self.__changeData(self.__data)

    def __getSettingsDependingOnDigitNum(self):
        settingsDependingOnDigitNum = []
        digitNum = int(self.__digitNum.get())

        if self.__slotMode.get() == 0:
            for num in range(0, digitNum//2):
                settingsDependingOnDigitNum.append("byte")

            if digitNum%2 == 1:
                settingsDependingOnDigitNum.append("nibble")
            else:
                settingsDependingOnDigitNum.append("byte")

            while len(settingsDependingOnDigitNum) < 4:
                settingsDependingOnDigitNum.append("byte")

        else:
            for num in range(0, 7):
                settingsDependingOnDigitNum.append("byte")

        for num in range(0, len(settingsDependingOnDigitNum)):
            self.__varBoxSettings[num] = settingsDependingOnDigitNum[num]


        return settingsDependingOnDigitNum


    def __getActiveNum(self):
        if self.__slotMode.get() == 0:
           return (int(self.__digitNum.get())//2) + (int(self.__digitNum.get())%2)
        else:
           return int(self.__digitNum.get())

    def __slotChanged(self):
        self.__data[self.__lastDigit+1] = str(self.__slotMode.get())
        self.__fillDataVarListBoxes(True, False)

    def __fillDataVarListBoxes(self, change, init):
        lists = {
            "nibble": self.__nibbleVars,
            "byte": self.__byteVars
        }

        if init == False:
           for num in range(0, 7):
               myList = self.__varListBoxes[num]
               typ    = self.__varBoxSettings[num]

               try:
                   self.__lastSelecteds[num] = lists[typ][myList.curselection()[0]].split("::")[1]
               except:
                   pass
               myList.select_clear(0, END)
               myList.delete(0, END)

        else:
            item = self.__byteVars[0].split("::")[1]
            self.__lastSelecteds = [item, item, item, item, item, item, item]

        settingsDependingOnDigitNum = self.__getSettingsDependingOnDigitNum()
        activeNum = self.__getActiveNum()

        last = int(self.__digitNum.get())
        if self.__slotMode.get() == 0:
           last = last//2 + last%2

        for num in range(0, 7):
            myList = self.__varListBoxes[num]
            typ = self.__varBoxSettings[num]

            selectNum = 0
            for itemNum in range(0, len(lists[typ])):
                myList.insert(END, lists[typ][itemNum])
                if lists[typ][itemNum].split("::")[1] == self.__lastSelecteds[num]:
                    selectNum = itemNum

            if num < last:
                myList.select_set(selectNum)
                myList.yview(selectNum)

                self.__lastSelecteds[num] = lists[typ][selectNum].split("::")[1]
                self.__data[3+num]        = self.__lastSelecteds[num]

            if activeNum < num+1:
               myList.config(state = DISABLED)
               myList.select_clear(0, END)
            else:
                myList.config(state=NORMAL)

        if change == True: self.__changeData(self.__data)

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
