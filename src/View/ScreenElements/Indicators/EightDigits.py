from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from time import sleep
import re


class EightDigits:
    def __init__(self, loader, baseFrame, data, changeData, w, h, currentBank, dead):
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

        self.__listOfPictures  = []
        self.__listOfPictures2 = []

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

                    self.__listOfPictures.append(file.replace(".asm", "") + "_(Big)")
                    if mode == "simple" and frames > 9:
                        self.__listOfPictures2.append(file.replace(".asm", "") + "_(Big)")

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

                    self.__listOfPictures.append(file.replace(".asm", "") + "_(Normal)")
                    if frames > 9:
                        self.__listOfPictures2.append(file.replace(".asm", "") + "_(Normal)")

        dataVars     = self.__data[3:11]
        digitNum     = self.__data[11]
        slotMode     = self.__data[12]
        gradientNum  = self.__data[13]
        color        = self.__data[14]
        font         = self.__data[15]

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
                  self.__frame1_4, self.__frame4,
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
        self.__varListBox8 = self.__varListBoxes[7]

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
            self.__digitNum.set("8")

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

        self.__lastSelecteds = ["", "", "", "", "", "", "", ""]

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
                                             command=self.__slotChanged
                                             )

        self.__slotButton.pack_propagate(False)
        self.__slotButton.pack(fill=X, side=TOP, anchor=N)

        for varListBox in self.__varListBoxes:
            varListBox.bind("<ButtonRelease-1>", self.__changeVar)
            varListBox.bind("<KeyRelease-Up>", self.__changeVar)
            varListBox.bind("<KeyRelease-Down>", self.__changeVar)

        self.__fillDataVarListBoxes(False, True)

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
            if self.__digitNum.get() != self.__data[11]:
                temp = self.__digitNum.get()
                if int(temp) > 8:
                    temp = "8"
                elif int(temp) < 1:
                    temp = "1"
                self.__digitNum.set(temp)
                self.__data[11] = self.__digitNum.get()

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
            for num in range(0, 8):
                settingsDependingOnDigitNum.append("byte")

        return settingsDependingOnDigitNum


    def __getActiveNum(self):
        if self.__slotMode.get() == 0:
           return (int(self.__digitNum.get())//2) + (int(self.__digitNum.get())%2)
        else:
           return int(self.__digitNum.get())

    def __slotChanged(self):
        pass

    def __fillDataVarListBoxes(self, change, init):
        lists = {
            "nibble": self.__nibbleVars,
            "byte": self.__byteVars
        }

        settingsDependingOnDigitNum = self.__getSettingsDependingOnDigitNum()

        if init == False:
           for num in range(0, len(settingsDependingOnDigitNum)):
               myList = self.__varListBoxes[num]
               typ    = self.__varBoxSettings[num]

               self.__lastSelecteds[num] = lists[typ][myList.curselection()[0]]
               myList.select_clear(0, END)
               myList.delete(0, END)

        activeNum = self.__getActiveNum()

        for num in range(0, 8):
            myList = self.__varListBoxes[num]
            typ = self.__varBoxSettings[num]

            selectNum = 0
            for itemNum in range(0, len(lists[typ])):
                myList.insert(END, lists[typ][itemNum])
                if lists[typ][itemNum].split("::")[1] == self.__lastSelecteds[num]:
                    selectNum = itemNum

            myList.select_set(selectNum)
            self.__lastSelecteds[num] = lists[typ][selectNum]
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
