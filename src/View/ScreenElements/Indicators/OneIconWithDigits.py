from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from time import sleep
import re


class OneIconWithDigits:
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

        if len(self.__listOfPictures) == 0:
            blankAnimation({
                               "item": "bigSprite / sprite", "folder": "'" +self.__loader.mainWindow.projectPath.split("/")[-2]+"/bigSprites' / '" +
                                                                         self.__loader.mainWindow.projectPath.split("/")[-2]+"/sprites'"
                           })
        else:
            itWasHash = False
            if data[3] == "#":
                itWasHash = True

            self.__addElements()
            if itWasHash == True: self.__changeData(data)

    def __loadPictures(self):
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

        self.__label1 = Label(self.__frame1,
                              text=self.__dictionaries.getWordFromCurrentLanguage("spriteName") + ":",
                              font=self.__smallFont, fg=self.__colors.getColor("font"),
                              bg=self.__colors.getColor("window"), justify=CENTER
                              )

        self.__label1.pack_propagate(False)
        self.__label1.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__picListScrollBar1 = Scrollbar(self.__frame1)
        self.__picListBox1 = Listbox(self.__frame1, width=100000,
                                    height=1000,
                                    yscrollcommand=self.__picListScrollBar1.set,
                                    selectmode=BROWSE,
                                    exportselection=False,
                                    font=self.__miniFont,
                                    justify=LEFT
                                    )

        self.__picListBox1.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__picListBox1.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__picListBox1.pack_propagate(False)

        self.__picListScrollBar1.pack(side=RIGHT, anchor=W, fill=Y)
        self.__picListBox1.pack(side=LEFT, anchor=W, fill=BOTH)
        self.__picListScrollBar1.config(command=self.__picListBox1.yview)

        for item in self.__listOfPictures:
            self.__picListBox1.insert(END, item)

        self.__lastSelectedPictures = [ "" , "" ]

        if self.__data[3] == "#":
           self.__picListBox1.select_set(0)
           self.__lastSelectedPictures[0] = self.__listOfPictures[0]
           self.__data[3] = self.__listOfPictures[0]

        else:
           for itemNum in range(0, len(self.__listOfPictures)):
               if self.__data[3] == self.__listOfPictures[itemNum]:
                  self.__picListBox1.select_set(itemNum)
                  self.__lastSelectedPictures[0] = self.__listOfPictures[itemNum]
                  break

        self.__picListBox1.bind("<ButtonRelease-1>", self.__changedPicture1)
        self.__picListBox1.bind("<KeyRelease-Up>", self.__changedPicture1)
        self.__picListBox1.bind("<KeyRelease-Down>", self.__changedPicture1)

        from NUSIZFrame import NUSIZFrame

        self.__nusizLabel = Label(self.__frame4,
                                  text="NUSIZ:",
                                  font=self.__smallFont, fg=self.__colors.getColor("font"),
                                  bg=self.__colors.getColor("window"), justify=CENTER
                                  )

        self.__nusizLabel.pack_propagate(False)
        self.__nusizLabel.pack(side=TOP, anchor=CENTER, fill=X)

        self.__nusizFrame1 = NUSIZFrame(self.__loader, self.__frame4, self.__changeData,
                                        self.__h // 4, self.__data, self.dead, "small", 5, self.__w // 7, True)

        self.__lastBits = ["%00000000", "%00000000"]

        self.__picOption1 = IntVar()

        self.__constButton1 = Radiobutton(self.__frame2, width=99999,
                                         text=self.__dictionaries.getWordFromCurrentLanguage("constant"),
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__smallFont,
                                         variable=self.__picOption1,
                                         activebackground=self.__colors.getColor("highLight"),
                                         value=1, command=self.XXX1
                                         )

        self.__constButton1.pack_propagate(False)
        self.__constButton1.pack(fill=X, side=TOP, anchor=N)

        from HexEntry import HexEntry
        self.__fuckinColors = ["$16", "$86"]

        w = ((self.__w // 7) * 2 ) // 3
        h = self.__h // 6


        self.__constEntry1 = HexEntry(self.__loader, self.__frame2, self.__colors, self.__colorDict,
                                     self.__normalFont, self.__fuckinColors, 0, None, self.__chamgeConst1)

        self.__varButton1 = Radiobutton(self.__frame2, width=99999,
                                       text=self.__dictionaries.getWordFromCurrentLanguage("variable"),
                                       bg=self.__colors.getColor("window"),
                                       fg=self.__colors.getColor("font"),
                                       justify=LEFT, font=self.__smallFont,
                                       variable=self.__picOption1,
                                       activebackground=self.__colors.getColor("highLight"),
                                       value=2, command=self.XXX2
                                       )

        self.__varButton1.pack_propagate(False)
        self.__varButton1.pack(fill=X, side=TOP, anchor=N)

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

        self.__colorVarListScrollBar1 = Scrollbar(self.__frame2)
        self.__colorVarListBox1 = Listbox(self.__frame2, width=100000,
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

        self.__colorVarListScrollBar1.config(command=self.__colorVarListBox1.yview)

        for item in self.__colorVars:
            self.__colorVarListBox1.insert(END, item)

        self.__lastSelectedColors = ["", ""]

        if self.isItHex(self.__data[4]) == True:
           self.__picOption1.set(1)
           self.__fuckinColors[0] = self.__data[4]
           self.__colorVarListBox1.config(state = DISABLED)
           self.__lastSelectedColors[0] = self.__colorVars[0].split("::")[1]
           self.__constEntry1.setValue(self.__data[4])
        else:
           self.__picOption1.set(2)
           self.__constEntry1.changeState(DISABLED)
           for itemNum in range(0, len(self.__colorVars)):
               if self.__data[4] == self.__colorVars[itemNum].split("::")[1]:
                  self.__lastSelectedColors[0] = self.__data[4]
                  self.__colorVarListBox1.select_set(itemNum)
                  break


        self.__colorVarListBox1.bind("<ButtonRelease-1>", self.__changedColorVar1)
        self.__colorVarListBox1.bind("<KeyRelease-Up>", self.__changedColorVar1)
        self.__colorVarListBox1.bind("<KeyRelease-Down>", self.__changedColorVar1)

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

        self.__dataVarFrame1 = Frame(self.__frame3, width=self.__w // 7,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h // 3)

        self.__dataVarFrame2 = Frame(self.__frame3, width=self.__w // 7,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h // 3)

        self.__labelData1 = Label(self.__frame3,
                              text=self.__dictionaries.getWordFromCurrentLanguage("dataVar") + ":",
                              font=self.__smallFont, fg=self.__colors.getColor("font"),
                              bg=self.__colors.getColor("window"), justify=CENTER
                              )

        self.__labelData1.pack_propagate(False)

        self.__labelData2 = Label(self.__frame3,
                              text=self.__dictionaries.getWordFromCurrentLanguage("dataVar") + ":",
                              font=self.__smallFont, fg=self.__colors.getColor("font"),
                              bg=self.__colors.getColor("window"), justify=CENTER
                              )

        self.__labelData2.pack_propagate(False)

        self.__dataVarFrame1.pack_propagate(False)
        self.__labelData1.pack(side=TOP, anchor=CENTER, fill=BOTH)
        self.__dataVarFrame1.pack(side=TOP, anchor=N, fill=X)

        self.__dataVarFrame2.pack_propagate(False)
        self.__labelData2.pack(side=TOP, anchor=CENTER, fill=BOTH)
        self.__dataVarFrame2.pack(side=TOP, anchor=N, fill=BOTH)

        self.__dataVarScrollBar1 = Scrollbar(self.__dataVarFrame1)
        self.__dataVarListBox1 = Listbox(self.__dataVarFrame1, width=100000,
                                         height=1000,
                                         yscrollcommand=self.__dataVarScrollBar1.set,
                                         selectmode=BROWSE,
                                         exportselection=False,
                                         font=self.__smallFont,
                                         justify=LEFT
                                         )

        self.__dataVarListBox1.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__dataVarListBox1.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__dataVarListBox1.pack_propagate(False)

        self.__dataVarScrollBar1.pack(side=RIGHT, anchor=W, fill=Y)
        self.__dataVarListBox1.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__dataVarScrollBar1.config(command=self.__dataVarListBox1.yview)

        self.__dataVarListBox1.bind("<ButtonRelease-1>", self.__changedDataVar1)
        self.__dataVarListBox1.bind("<KeyRelease-Up>", self.__changedDataVar1)
        self.__dataVarListBox1.bind("<KeyRelease-Down>", self.__changedDataVar1)

        self.__dataVarScrollBar2 = Scrollbar(self.__dataVarFrame2)
        self.__dataVarListBox2 = Listbox(self.__dataVarFrame2, width=200000,
                                         height=2000,
                                         yscrollcommand=self.__dataVarScrollBar2.set,
                                         selectmode=BROWSE,
                                         exportselection=False,
                                         font=self.__smallFont,
                                         justify=LEFT
                                         )

        self.__dataVarListBox2.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__dataVarListBox2.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__dataVarListBox2.pack_propagate(False)

        self.__dataVarScrollBar2.pack(side=RIGHT, anchor=W, fill=Y)
        self.__dataVarListBox2.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__dataVarScrollBar2.config(command=self.__dataVarListBox2.yview)

        for item in self.__dataVars:
            self.__dataVarListBox1.insert(END, item)
            self.__dataVarListBox2.insert(END, item)

        self.__dataVarListBox2.bind("<ButtonRelease-1>", self.__changedDataVar2)
        self.__dataVarListBox2.bind("<KeyRelease-Up>", self.__changedDataVar2)
        self.__dataVarListBox2.bind("<KeyRelease-Down>", self.__changedDataVar2)

        if self.__data[7] == "#":
           self.__data[7] = self.__dataVars[0].split("::")[1]
           self.__dataVarListBox1.select_set(0)
        else:
           for itemNum in range(0, len(self.__dataVars)):
               if self.__dataVars[itemNum].split("::")[1] == self.__data[7]:
                  self.__dataVarListBox1.select_set(itemNum)

        if self.__data[8] == "#":
           self.__data[8] = self.__dataVars[0].split("::")[1]
           self.__dataVarListBox2.select_set(0)
        else:
           for itemNum in range(0, len(self.__dataVars)):
               if self.__dataVars[itemNum].split("::")[1] == self.__data[8]:
                  self.__dataVarListBox2.select_set(itemNum)

        self.__picSettingsOption1 = IntVar()

        self.__constButton3 = Radiobutton(self.__frame4, width=99999,
                                         text=self.__dictionaries.getWordFromCurrentLanguage("constant"),
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__smallFont,
                                         variable=self.__picSettingsOption1,
                                         activebackground=self.__colors.getColor("highLight"),
                                         value=1, command=self.XXX5
                                         )

        self.__constButton3.pack_propagate(False)
        self.__constButton3.pack(fill=X, side=TOP, anchor=N)

        self.__indexFrame1 = Frame(self.__frame4, width=self.__w // 7,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h // 16)

        self.__indexFrame1.pack_propagate(False)
        self.__indexFrame1.pack(side=TOP, anchor=N, fill=X)

        self.__indexFrame1_1 = Frame(self.__indexFrame1, width=self.__w // 14,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h // 16)

        self.__indexFrame1_1.pack_propagate(False)
        self.__indexFrame1_1.pack(side=LEFT, anchor=E, fill=Y)

        self.__indexFrame1_2 = Frame(self.__indexFrame1, width=self.__w // 14,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h // 16)

        self.__indexFrame1_2.pack_propagate(False)
        self.__indexFrame1_2.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__mirrored1 = IntVar()
        self.__mirroredButton1 = Checkbutton(self.__frame4, width=99999,
                                       text=self.__dictionaries.getWordFromCurrentLanguage("mirrored"),
                                       bg=self.__colors.getColor("window"),
                                       fg=self.__colors.getColor("font"),
                                       justify=LEFT, font=self.__smallFont,
                                       variable=self.__mirrored1,
                                       activebackground=self.__colors.getColor("highLight"),
                                       command=self.__mirroredChanged1
                                       )

        self.__mirroredButton1.pack_propagate(False)
        self.__mirroredButton1.pack(fill=X, side=TOP, anchor=N)

        self.__varButton3 = Radiobutton(self.__frame4, width=99999,
                                       text=self.__dictionaries.getWordFromCurrentLanguage("variable"),
                                       bg=self.__colors.getColor("window"),
                                       fg=self.__colors.getColor("font"),
                                       justify=LEFT, font=self.__smallFont,
                                       variable=self.__picSettingsOption1,
                                       activebackground=self.__colors.getColor("highLight"),
                                       value=2, command=self.XXX6
                                       )

        self.__varButton3.pack_propagate(False)
        self.__varButton3.pack(fill=X, side=TOP, anchor=N)

        self.__indexLabel = Label(self.__indexFrame1_1,
                              text=self.__dictionaries.getWordFromCurrentLanguage("index"),
                              font=self.__smallFont, fg=self.__colors.getColor("font"),
                              bg=self.__colors.getColor("window"), justify=CENTER
                              )

        self.__indexLabel.pack_propagate(False)
        self.__indexLabel.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__indexVal1 = StringVar()
        self.__indexEntry1 = Entry(self.__indexFrame1_2,
                                   bg=self.__colors.getColor("boxBackNormal"),
                                   fg=self.__colors.getColor("boxFontNormal"),
                                   width=9999, justify=CENTER,
                                   textvariable=self.__indexVal1,
                                   font=self.__smallFont
                                   )

        self.__indexEntry1.pack_propagate(False)
        self.__indexEntry1.pack(fill=BOTH, side=TOP, anchor=N)

        self.__indexEntry1.bind("<KeyRelease>", self.__changeIndexAndMirroring1)
        self.__indexEntry1.bind("<FocusOut>", self.__changeIndexAndMirroring1)

        self.__lastBits = ["%00000000", "%00000000"]


        self.__picVarScrollBar1 = Scrollbar(self.__frame4)
        self.__picVarListBox1 = Listbox(self.__frame4, width=100000,
                                         height=1000,
                                         yscrollcommand=self.__picVarScrollBar1.set,
                                         selectmode=BROWSE,
                                         exportselection=False,
                                         font=self.__smallFont,
                                         justify=LEFT
                                         )

        self.__picVarListBox1.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__picVarListBox1.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__picVarListBox1.pack_propagate(False)

        self.__picVarScrollBar1.pack(side=RIGHT, anchor=W, fill=Y)
        self.__picVarListBox1.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__picVarScrollBar1.config(command=self.__picVarListBox1.yview)

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

        for item in self.__colorVars:
            self.__picVarListBox1.insert(END, item)

        self.__lastSelectedPictureVars = ["", ""]

        if self.__data[5][0] == "%":
           self.__picSettingsOption1.set(1)
           self.__lastSelectedPictureVars[0] = self.__colorVars[0].split("::")[1]

           self.__picVarListBox1.config(state = DISABLED)

           mirrored = self.__data[5][5]
           index    = self.__data[5][1:5]
           nusiz    = self.__data[5][5:]

           self.__mirrored1.set(int(mirrored))
           self.__indexVal1.set(str(int("0b"+index, 2)))
           self.__nusizFrame1.setValue(str(int("0b"+nusiz, 2)))

        else:
           self.__mirroredButton1.config(state = DISABLED)
           self.__indexEntry1.config(state = DISABLED)
           self.__nusizFrame1.changeState(DISABLED)

           self.__picSettingsOption1.set(2)

           self.__mirrored1.set(0)
           self.__indexVal1.set("0")

           selector = 0
           for itemNum in range(0, len(self.__colorVars)):
               if self.__colorVars[itemNum].split("::")[1] == self.__data[5]:
                  selector = itemNum
                  break

           self.__lastSelectedPictureVars[0] = self.__data[5]
           self.__picVarListBox1.select_set(selector)

        self.__indexEntry1.bind("<KeyRelease>", self.__changeIndexAndMirroring1)
        self.__indexEntry1.bind("<FocusOut>", self.__changeIndexAndMirroring1)

        self.__picVarListBox1.bind("<ButtonRelease-1>", self.__changedPicVar1)
        self.__picVarListBox1.bind("<KeyRelease-Up>", self.__changedPicVar1)
        self.__picVarListBox1.bind("<KeyRelease-Down>", self.__changedPicVar1)

        from GradientFrame import GradientFrame
        self.__gradientFrame = GradientFrame(self.__loader, self.__frame6,
                                             self.__changeData, self.__h, self.__data, self.dead, 8, "small", 10)

        self.__digitLabel = Label(self.__frame5,
                              text=self.__dictionaries.getWordFromCurrentLanguage("numOfDigits") + ":",
                              font=self.__smallFont, fg=self.__colors.getColor("font"),
                              bg=self.__colors.getColor("window"), justify=CENTER
                              )

        self.__digitLabel.pack_propagate(False)
        self.__digitLabel.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__digitNum = StringVar()

        if self.isItNum(self.__data[6]) == True:
            self.__digitNum.set(self.__data[6])
            if int(self.__data[6]) < 3:
                self.__dataVarListBox2.config(state=DISABLED)
            else:
                self.__dataVarListBox2.config(state=NORMAL)


        else:
            self.__digitNum.set("2")
            self.__dataVarListBox2.config(state=DISABLED)

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
                                         value=1, command=self.__changedFontOption1_1
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
                                         value=2, command=self.__changedFontOption1_2
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
                                         value=3, command=self.__changedFontOption1_3
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

        self.__fontVarListScrollBar1.config(command=self.__fontVarListBox1.yview)

        try:
            self.__fontListSelect = [self.__listOfPictures2[0], self.__listOfPictures2[0]]
        except:
            self.__fontListSelect = ["", ""]



        self.__fontVarListBox1.bind("<ButtonRelease-1>", self.__changedFontVarListBox1)
        self.__fontVarListBox1.bind("<KeyRelease-Up>", self.__changedFontVarListBox1)
        self.__fontVarListBox1.bind("<KeyRelease-Down>", self.__changedFontVarListBox1)

        for item in self.__listOfPictures2:
            self.__fontVarListBox1.insert(END, item)

        if  self.__data[9] == "#":
            self.__data[9] = "default"
            self.__fontOption1.set(1)
            self.__fontVarListBox1.config(state = DISABLED)

        else:
            if   self.__data[9] == "default":
                self.__fontOption1.set(1)
                self.__fontVarListBox1.config(state = DISABLED)
            elif self.__data[9] == "digital":
                self.__fontOption1.set(2)
                self.__fontVarListBox1.config(state = DISABLED)
            else:
                if len(self.__listOfPictures2) > 0:
                    self.__fontOption1.set(3)
                    foundIt = False
                    for itemNum in range(0, len(self.__listOfPictures2)):
                        if self.__listOfPictures2[itemNum] == self.__data[9]:
                           self.__fontVarListBox1.select_set(itemNum)
                           self.__fontListSelect[0] = self.__data[9]
                           foundIt = True
                           break

                    if foundIt == False:
                        self.__fontOption1.set(1)
                        self.__fontVarListBox1.config(state=DISABLED)
                else:
                    self.__fontOption1.set(1)

        if len(self.__listOfPictures2) == 0:
            self.__fontOptionButton1_3.config(state=DISABLED)
            self.__fontVarListBox1.config(state=DISABLED)

        if   int(self.__digitNum.get()) == 1:
            self.__dataListBoxVarTypes = ["nibble", "byte"]
        elif int(self.__digitNum.get()) == 3:
            self.__dataListBoxVarTypes = ["byte", "nibble"]

        else:
            self.__dataListBoxVarTypes = ["byte", "byte"]

        self.__lastFirst  = self.__data[7]
        self.__lastSecond = self.__data[8]
        self.__fillDataVarListBoxes(False)
        #self.__changeData(self.__data)

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
            if self.__digitNum.get() != self.__data[6]:
                temp = self.__digitNum.get()
                if int(temp) > 4:
                    temp = "4"
                elif int(temp) < 1:
                    temp = "1"
                self.__digitNum.set(temp)
                self.__data[6] = self.__digitNum.get()

                if int(temp) < 3:
                   self.__dataVarListBox2.config(state = DISABLED)
                else:
                   self.__dataVarListBox2.config(state=NORMAL)

                # If the second is off, we leave it as byte! It does not matter anyway
                if int(self.__digitNum.get()) == 1:
                    self.__dataListBoxVarTypes = ["nibble", "byte"]
                elif int(self.__digitNum.get()) == 3:
                    self.__dataListBoxVarTypes = ["byte", "nibble"]
                else:
                    self.__dataListBoxVarTypes = ["byte", "byte"]

                self.__fillDataVarListBoxes(True)


    def __fillDataVarListBoxes(self, change):
        lists = {
            "nibble"    : self.__colorVars,
            "byte"      : self.__byteVars
        }

        listBox1Vars    = lists[self.__dataListBoxVarTypes[0]]
        listBox2Vars    = lists[self.__dataListBoxVarTypes[1]]

        self.__dataVarListBox1.select_clear(0, END)
        self.__dataVarListBox2.select_clear(0, END)

        self.__dataVarListBox1.delete(0, END)
        self.__dataVarListBox2.delete(0, END)

        for item in listBox1Vars:
            self.__dataVarListBox1.insert(END, item)

        for item in listBox2Vars:
            self.__dataVarListBox2.insert(END, item)

        selectNums = [0, 0]
        for itemNum in range(0, len(listBox1Vars)):
            if listBox1Vars[itemNum].split("::")[1] == self.__lastFirst:
               selectNums[0] = itemNum
               break

        for itemNum in range(0, len(listBox2Vars)):
            if listBox2Vars[itemNum].split("::")[1] == self.__lastSecond:
               selectNums[1] = itemNum
               break

        self.__data[7] = listBox1Vars[selectNums[0]].split("::")[1]
        self.__data[8] = listBox2Vars[selectNums[1]].split("::")[1]

        self.__dataVarListBox1.select_set(selectNums[0])
        self.__dataVarListBox2.select_set(selectNums[1])

        if change == True: self.__changeData(self.__data)


    def __changedFontVarListBox1(self, event):
        if self.__fontOption1.get() != 3:
            return

        if self.__listOfPictures2[self.__fontVarListBox1.curselection()[0]] != self.__fontListSelect[0]:
           self.__fontListSelect[0] = self.__listOfPictures2[self.__fontVarListBox1.curselection()[0]]
           self.__data[9]           = self.__fontListSelect[0]
           self.__changeData(self.__data)


    def __changedFontOption1_1(self):
        self.__fontVarListBox1.select_clear(0, END)
        self.__fontVarListBox1.config(state = DISABLED)
        self.__data[9]  = "default"
        self.__changeData(self.__data)

    def __changedFontOption1_2(self):
        self.__fontVarListBox1.select_clear(0, END)
        self.__fontVarListBox1.config(state = DISABLED)
        self.__data[9]  = "digital"
        self.__changeData(self.__data)

    def __changedFontOption1_3(self):
        self.__fontVarListBox1.config(state = NORMAL)
        selector = 0
        for itemNum in range(0, len(self.__listOfPictures2)):
            if self.__listOfPictures2[itemNum] == self.__fontListSelect[0]:
                selector = itemNum
                break

        self.__fontVarListBox1.select_set(selector)
        self.__data[9] = self.__fontListSelect[0]
        self.__changeData(self.__data)

    def __chamgeConst1(self, event):
        if self.__constEntry1.getValue() != self.__data[4]:
            temp = self.__constEntry1.getValue()
            if self.isItHex(temp) == True:
                temp = temp[:2] + "6"
                self.__data[4] = temp
                self.__constEntry1.setValue(temp)
                self.__changeData(self.__data)

    def XXX_ConstOn(self, constEntry, lastSelected, lastSelectedNum, colorVarListBox, dataNum, variables):
        constEntry.changeState(state = NORMAL)
        lastSelected[lastSelectedNum] = variables[colorVarListBox.curselection()[0]].split("::")[1]
        colorVarListBox.select_clear(0, END)
        colorVarListBox.config(state = DISABLED)

        if self.isItHex(constEntry.getValue()) == True:
            self.__data[dataNum] = constEntry.getValue()
            self.__changeData(self.__data)

    def XXX_VarOn(self, constEntry, lastSelected, lastSelectedNum, colorVarListBox, dataNum, variables):
        constEntry.changeState(state = DISABLED)
        colorVarListBox.config(state = NORMAL)

        selector = 0
        for itemNum in range(0, len(variables)):
            if variables[itemNum].split("::")[1] == lastSelected[lastSelectedNum]:
               selector = itemNum
               break

        colorVarListBox.select_set(selector)
        self.__data[dataNum] = lastSelected[lastSelectedNum]
        self.__changeData(self.__data)

    def XXX1(self):
        self.XXX_ConstOn(self.__constEntry1,
                         self.__lastSelectedColors,
                         0,
                         self.__colorVarListBox1,
                         4,
                         self.__colorVars
                         )

    def XXX2(self):
        self.XXX_VarOn(self.__constEntry1,
                       self.__lastSelectedColors,
                       0,
                       self.__colorVarListBox1,
                       4,
                       self.__colorVars)

    def XXX_changeToPicSettingsConst(self, mirrored, indexEntry, indexVal, lastSelected, listBox, selectNum, dataNum, mirroredButton, nusizFrame):
        mirroredButton.config(state=NORMAL)
        indexEntry.config(state=NORMAL)
        nusizFrame.changeState(NORMAL)

        lastSelected[selectNum] = self.__colorVars[listBox.curselection()[0]].split("::")[1]
        listBox.config(state=DISABLED)

        mirrored = str(mirrored.get())
        try:
            indexNum = bin(int(indexVal.get())).replace("0b", "")
            while len(indexNum) < 4: indexNum = "0" + indexNum

            self.__data[dataNum] = "%" + indexNum + mirrored + nusizFrame.getValue()
            self.__changeData(self.__data)
        except:
            pass


    def XXX5(self):
        self.XXX_changeToPicSettingsConst(self.__mirrored1,
                                          self.__indexEntry1,
                                          self.__indexVal1,
                                          self.__lastSelectedPictureVars,
                                          self.__picVarListBox1,
                                          0, 5,
                                          self.__mirroredButton1,
                                          self.__nusizFrame1
                                          )

    def XXX6(self):
        self.__changedPicVar(
            self.__mirroredButton1,
            self.__indexEntry1,
            self.__picVarListBox1,
            self.__colorVars,
            self.__lastSelectedPictureVars,
            5, 0, self.__nusizFrame1
        )

    def __changedPicVar(self, mirroredButton, indexEntry, picVarListBox, variables, lastSelected, dataNum, selectNum, nusizFrame):
        mirroredButton.config(state = DISABLED)
        indexEntry.config(state = DISABLED)
        nusizFrame.changeState(DISABLED)

        picVarListBox.config(state = NORMAL)
        picVarListBox.select_clear(0, END)

        selector  = 0
        for itemNum in range(0, len(variables)):
            if lastSelected[selectNum] == variables[itemNum].split("::")[1]:
               selector = itemNum
               break

        picVarListBox.select_set(selector)
        self.__data[dataNum] = variables[selector].split("::")[1]
        self.__changeData(self.__data)

    def __changedPicVar_TheRealOne(self, picOption, lastSelected, selectNum, dataNum, listBox):
        if picOption.get() == 1:
           return

        if lastSelected[selectNum] != self.__colorVars[listBox.curselection()[0]].split("::")[1]:
           lastSelected[selectNum] = self.__colorVars[listBox.curselection()[0]].split("::")[1]
           self.__data[dataNum]    = lastSelected[selectNum]
           self.__changeData(self.__data)


    def __changedPicVar1(self, event):
        self.__changedPicVar_TheRealOne(self.__picSettingsOption1,
                                        self.__lastSelectedPictureVars,
                                        0, 5,
                                        self.__picVarListBox1
                                        )


    def __mirroredChanged1(self):
        # self.__changeIndexAndMirroring1(None)
        self.__changeIndexAndMirroring(self.__picSettingsOption1,
                                       self.__mirrored1,
                                       self.__indexVal1,
                                       self.__indexEntry1,
                                       5,
                                       self.__nusizFrame1
                                       )

    def __changeIndexAndMirroring(self, picSettings, mirrorVar, indexVal, indexEntry, dataNum, nusizFrame):
        if picSettings.get() == 2:
           return

        mirrored = str(mirrorVar.get())
        try:
            frameNum = int(indexVal.get())
        except:
            indexEntry.config(
                bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                fg=self.__loader.colorPalettes.getColor("boxFontUnSaved")
            )
            return
        indexEntry.config(
            bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
            fg=self.__loader.colorPalettes.getColor("boxFontNormal")
        )

        if frameNum > 15: frameNum = 15
        if frameNum < 0 : frameNum = 0

        indexVal.set(str(frameNum))

        num = bin(frameNum)[2:]
        while len(num) < 4:
            num = "0" + num

        nusiz = bin(int(nusizFrame.getValue())).replace("0b", "")
        while len(nusiz) < 3:
            nusiz = "0" + nusiz

        self.__data[dataNum] = "%" + num + mirrored + nusiz
        self.__changeData(self.__data)


    def __changeIndexAndMirroring1(self, event):
        self.__changeIndexAndMirroring(self.__picSettingsOption1,
                                       self.__mirrored1,
                                       self.__indexVal1,
                                       self.__indexEntry1,
                                       5, self.__nusizFrame1)

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

    def __changeMaxEntry(self, maxVar, maxVarEntry, num):
        if self.isItNum(maxVar.get()) == False:
            maxVarEntry.config(
                bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                fg=self.__loader.colorPalettes.getColor("boxFontUnSaved")
            )
        else:
            maxVarEntry.config(
                bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                fg=self.__loader.colorPalettes.getColor("boxFontNormal")
            )
            if maxVar.get() != self.__data[num]:
                temp = maxVar.get()
                if int(temp) > 255:
                    temp = "255"
                elif int(temp) < 1:
                    temp = "1"
                maxVar.set(temp)
                self.__data[num] = maxVar.get()
                self.__changeData(self.__data)

    def __changedPicture1(self, event):
        if self.__listOfPictures[self.__picListBox1.curselection()[0]] != self.__data[3]:
           self.__data[3] =  self.__listOfPictures[self.__picListBox1.curselection()[0]]
           self.__changeData(self.__data)


    def __changedDataVar1(self, event):
        lists = {
            "nibble"    : self.__colorVars,
            "byte"      : self.__byteVars
        }

        listBoxVars    = lists[self.__dataListBoxVarTypes[0]]

        if self.__dataVars[self.__dataVarListBox1.curselection()[0]].split("::")[1] != self.__data[7]:
           self.__data[7] =  listBoxVars[self.__dataVarListBox1.curselection()[0]].split("::")[1]
           self.__lastFirst = self.__data[8]
           self.__changeData(self.__data)

    def __changedDataVar2(self, event):
        lists = {
            "nibble"    : self.__colorVars,
            "byte"      : self.__byteVars
        }

        listBoxVars    = lists[self.__dataListBoxVarTypes[1]]

        if self.__dataVars[self.__dataVarListBox2.curselection()[0]].split("::")[1] != self.__data[8]:
           self.__data[8] =  listBoxVars[self.__dataVarListBox2.curselection()[0]].split("::")[1]
           self.__lastSecond = self.__data[8]
           self.__changeData(self.__data)

    def __changedColorVar1(self, event):
        if self.__picOption1.get() == 1:
           return

        if self.__dataVars[self.__colorVarListBox1.curselection()[0]].split("::")[1] != self.__data[4]:
           self.__data[4] =  self.__colorVars[self.__colorVarListBox1.curselection()[0]].split("::")[1]
           self.__changeData(self.__data)