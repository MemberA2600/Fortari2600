from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from time import sleep
import re


class TwelveIconsOrDigits:
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
            if itWasHash == True:
                self.__changeData(data)

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

        self.__frame1_5 = Frame(self.__uniqueFrame, width=self.__w // 6,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h)

        self.__frame1_5.pack_propagate(False)
        self.__frame1_5.pack(side=LEFT, anchor=E, fill=Y)

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

        icon            = self.__data[3]
        dataVar         = self.__data[4]
        digitColor      = self.__data[5]
        digitFont       = self.__data[6]
        digitGradient   = self.__data[7]
        colorMode       = self.__data[8]
        picSettings     = self.__data[9]
        forceDigits     = self.__data[10]

        self.__init     = True

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

        self.__lastSelectedPicture = ""


        if icon == "#":
           self.__lastSelectedPicture = self.__listOfPictures[0]
           self.__picListBox1.select_set(0)
           self.__picListBox1.yview(0)

           self.__data[3] = self.__lastSelectedPicture
        else:
           selector = 0
           for itemNum in range(0, len(self.__listOfPictures)):
               if self.__listOfPictures[itemNum] == icon:
                  selector = itemNum
                  break

           self.__lastSelectedPicture = self.__listOfPictures[selector]
           self.__picListBox1.select_set(selector)
           self.__picListBox1.yview(selector)

        self.__label2 = Label(self.__frame2,
                              text=self.__dictionaries.getWordFromCurrentLanguage("dataVar") + ":",
                              font=self.__normalFont, fg=self.__colors.getColor("font"),
                              bg=self.__colors.getColor("window"), justify=CENTER
                              )

        self.__label2.pack_propagate(False)
        self.__label2.pack(side=TOP, anchor=CENTER, fill=BOTH)

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


        self.__dataVarListScrollBar = Scrollbar(self.__frame2)
        self.__dataVarListBox = Listbox(self.__frame2, width=100000,
                                        height=1000,
                                        yscrollcommand=self.__dataVarListScrollBar.set,
                                        selectmode=BROWSE,
                                        exportselection=False,
                                        font=self.__normalFont,
                                        justify=LEFT
                                        )

        self.__dataVarListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__dataVarListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__dataVarListBox.pack_propagate(False)

        self.__dataVarListScrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__dataVarListBox.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__dataVarListScrollBar.config(command=self.__dataVarListBox.yview)
        self.__lastDataVar = ""

        for item in self.__dataVars:
            self.__dataVarListBox.insert(END, item)

        if dataVar == "#":
           self.__dataVarListBox.select_set(0)
           self.__dataVarListBox.yview(0)

           self.__lastDataVar = self.__dataVars[0].split("::")[1]
           self.__data[4] = self.__lastDataVar
        else:
           selector = 0
           for itemNum in range(0, len(self.__dataVars)):
               if dataVar == self.__dataVars[itemNum].split("::")[1]:
                  selector = itemNum
                  break

           self.__dataVarListBox.select_set(selector)
           self.__dataVarListBox.yview(selector)

           self.__lastDataVar = self.__dataVars[selector].split("::")[1]

        self.__sameColor = IntVar()

        self.__sameButton = Checkbutton(self.__frame3, width=99999,
                                         text=self.__dictionaries.getWordFromCurrentLanguage("sameColor"),
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__smallFont,
                                         variable=self.__sameColor,
                                         activebackground=self.__colors.getColor("highLight"),
                                         activeforeground=self.__loader.colorPalettes.getColor("font"),
                                         command=self.__changeSame
                                         )

        self.__sameButton.pack_propagate(False)
        self.__sameButton.pack(fill=X, side=TOP, anchor=N)

        self.__sameColor.set(int(colorMode))

        self.__constOrVar = IntVar()

        self.__constButton = Radiobutton(self.__frame3, width=99999,
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

        from HexEntry import HexEntry
        if self.isItHex(digitColor):
            self.__textColor = [digitColor]
            self.__constOrVar.set(1)
            self.__lastTextColor = self.__colorVars[0].split("::")[-1]
            self.__data[6] = self.__lastTextColor
        else:
            self.__textColor = ["$06"]
            self.__constOrVar.set(2)
            self.__lastTextColor = digitColor


        self.__hexEntry = HexEntry(self.__loader, self.__frame3, self.__colors, self.__colorDict,
                                     self.__normalFont, self.__textColor, 0, None, self.__changeConstant)

        self.__varButton = Radiobutton(self.__frame3, width=99999,
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

        self.__textColorVarListScrollBar = Scrollbar(self.__frame3)
        self.__textColorVarListBox = Listbox(self.__frame3, width=100000,
                                         height=1000,
                                         yscrollcommand=self.__textColorVarListScrollBar.set,
                                         selectmode=BROWSE,
                                         exportselection=False,
                                         font=self.__normalFont,
                                         justify=LEFT
                                         )

        self.__textColorVarListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__textColorVarListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__textColorVarListBox.pack_propagate(False)

        self.__textColorVarListScrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__textColorVarListBox.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__textColorVarListScrollBar.config(command=self.__textColorVarListBox.yview)

        for item in self.__colorVars:
            self.__textColorVarListBox.insert(END, item)

        from GradientFrame import GradientFrame
        self.__gradientFrame = GradientFrame(self.__loader, self.__frame5,
                                             self.__changeData, self.__h, self.__data, self.dead, 8, "normal", 7)

        self.__changeSame()
        self.__fontLabel = Label(self.__frame4,
                              text=self.__dictionaries.getWordFromCurrentLanguage("spriteName") + ":",
                              font=self.__smallFont, fg=self.__colors.getColor("font"),
                              bg=self.__colors.getColor("window"), justify=CENTER
                              )

        self.__fontLabel.pack_propagate(False)
        self.__fontLabel.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__fontOptionFrame1_1   = Frame(self.__frame4, width=self.__w // 7,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height = self.__h // 17)

        self.__fontOptionFrame1_1.pack_propagate(False)
        self.__fontOptionFrame1_1.pack(side=TOP, anchor=N, fill=X)

        self.__fontOptionFrame1_2   = Frame(self.__frame4, width=self.__w // 7,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height = self.__h // 17)

        self.__fontOptionFrame1_2.pack_propagate(False)
        self.__fontOptionFrame1_2.pack(side=TOP, anchor=N, fill=X)

        self.__fontOptionFrame1_3   = Frame(self.__frame4, width=self.__w // 7,
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
                                         activeforeground=self.__loader.colorPalettes.getColor("font"),
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
                                         activeforeground=self.__loader.colorPalettes.getColor("font"),
                                         value=3, command=self.__changedFontOption1_3
                                         )

        self.__fontOptionButton1_3.pack_propagate(False)
        self.__fontOptionButton1_3.pack(fill=X, side=TOP, anchor=N)

        self.__fontVarListScrollBar1 = Scrollbar(self.__frame4)
        self.__fontVarListBox1 = Listbox(self.__frame4, width=100000,
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

        for item in self.__listOfPictures2:
            self.__fontVarListBox1.insert(END, item)

        self.__lastFont = ""
        try:
            self.__lastSelectedFont = self.__listOfPictures2[0]
        except:
            self.__lastSelectedFont = ""

        if digitFont == "#":
           self.__fontOption1.set(1)
           self.__lastFont = "default"
           self.__data[6] = self.__lastFont
           self.__fontVarListBox1.config(state=DISABLED)

        else:
            if    digitFont == "default":
                  self.__fontOption1.set(1)
                  self.__lastFont = "default"
                  self.__fontVarListBox1.config(state = DISABLED)


            elif  digitFont == "digital":
                  self.__fontOption1.set(2)
                  self.__lastFont = "digital"
                  self.__fontVarListBox1.config(state = DISABLED)

            else:
                  if len(self.__listOfPictures2) > 0:
                      self.__fontOption1.set(3)
                      selector = 0
                      for itemNum in range(0, len(self.__listOfPictures2)):
                          if digitFont == self.__listOfPictures2[itemNum]:
                             selector = itemNum
                             break

                      self.__fontVarListBox1.selection_set(selector)
                      self.__lastFont = self.__listOfPictures2[selector]
                      self.__lastSelectedFont = self.__lastFont
                  else:
                      self.__fontOption1.set(1)

        if len(self.__listOfPictures2) == 0:
            self.__fontOptionButton1_3.config(state=DISABLED)
            self.__fontVarListBox1.config(state=DISABLED)

        self.__picListBox1.bind("<ButtonRelease-1>", self.__changePicture)
        self.__picListBox1.bind("<KeyRelease-Up>", self.__changePicture)
        self.__picListBox1.bind("<KeyRelease-Down>", self.__changePicture)

        self.__dataVarListBox.bind("<ButtonRelease-1>", self.__changeDataVar)
        self.__dataVarListBox.bind("<KeyRelease-Up>", self.__changeDataVar)
        self.__dataVarListBox.bind("<KeyRelease-Down>", self.__changeDataVar)

        self.__fontVarListBox1.bind("<ButtonRelease-1>", self.__changeFont)
        self.__fontVarListBox1.bind("<KeyRelease-Up>", self.__changeFont)
        self.__fontVarListBox1.bind("<KeyRelease-Down>", self.__changeFont)

        self.__textColorVarListBox.bind("<ButtonRelease-1>", self.__changeFontColorVar)
        self.__textColorVarListBox.bind("<KeyRelease-Up>", self.__changeFontColorVar)
        self.__textColorVarListBox.bind("<KeyRelease-Down>", self.__changeFontColorVar)

        self.__lastBits = "%00000000"

        self.__forceDigistsVal = IntVar()
        self.__forceDigists = Checkbutton(self.__frame1_5, width=99999,
                                       text=self.__dictionaries.getWordFromCurrentLanguage("digitsOnly"),
                                       bg=self.__colors.getColor("window"),
                                       fg=self.__colors.getColor("font"),
                                       justify=LEFT, font=self.__smallFont,
                                       variable=self.__forceDigistsVal,
                                       activebackground=self.__colors.getColor("highLight"),
                                       activeforeground=self.__loader.colorPalettes.getColor("font"),
                                       command=self.__changeForce
                                       )

        self.__forceDigists.pack_propagate(False)
        self.__forceDigists.pack(fill=X, side=TOP, anchor=N)

        if forceDigits == "1": self.__forceDigistsVal.set(1)


        self.__picSettingsOption1 = IntVar()

        self.__constButton3 = Radiobutton(self.__frame1_5, width=99999,
                                         text=self.__dictionaries.getWordFromCurrentLanguage("constant"),
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__smallFont,
                                         variable=self.__picSettingsOption1,
                                         activebackground=self.__colors.getColor("highLight"),
                                         activeforeground=self.__loader.colorPalettes.getColor("font"),
                                         value=1, command=self.__changeIconSettings
                                         )

        self.__constButton3.pack_propagate(False)
        self.__constButton3.pack(fill=X, side=TOP, anchor=N)

        self.__indexFrame1 = Frame(self.__frame1_5, width=self.__w // 7,
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
        self.__mirroredButton1 = Checkbutton(self.__frame1_5, width=99999,
                                       text=self.__dictionaries.getWordFromCurrentLanguage("mirrored"),
                                       bg=self.__colors.getColor("window"),
                                       fg=self.__colors.getColor("font"),
                                       justify=LEFT, font=self.__smallFont,
                                       variable=self.__mirrored1,
                                       activebackground=self.__colors.getColor("highLight"),
                                       activeforeground=self.__loader.colorPalettes.getColor("font"),
                                       command=self.__mirroredChanged1
                                       )

        self.__mirroredButton1.pack_propagate(False)

     #   self.__mirroredButton1.pack(fill=X, side=TOP, anchor=N)

        self.__varButton3 = Radiobutton(self.__frame4, width=99999,
                                       text=self.__dictionaries.getWordFromCurrentLanguage("variable"),
                                       bg=self.__colors.getColor("window"),
                                       fg=self.__colors.getColor("font"),
                                       justify=LEFT, font=self.__smallFont,
                                       variable=self.__picSettingsOption1,
                                       activebackground=self.__colors.getColor("highLight"),
                                       activeforeground=self.__loader.colorPalettes.getColor("font"),
                                       value=2, command=self.__changeIconSettings
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

        self.__varButton3 = Radiobutton(self.__frame1_5, width=99999,
                                       text=self.__dictionaries.getWordFromCurrentLanguage("variable"),
                                       bg=self.__colors.getColor("window"),
                                       fg=self.__colors.getColor("font"),
                                       justify=LEFT, font=self.__smallFont,
                                       variable=self.__picSettingsOption1,
                                       activebackground=self.__colors.getColor("highLight"),
                                       activeforeground=self.__loader.colorPalettes.getColor("font"),
                                       value=2, command=self.__changeIconSettings
                                       )

        self.__varButton3.pack_propagate(False)
        self.__varButton3.pack(fill=X, side=TOP, anchor=N)

        self.__picVarScrollBar1 = Scrollbar(self.__frame1_5)
        self.__picVarListBox1 = Listbox(self.__frame1_5, width=100000,
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
        self.__lastSelectedPictureVar = None

        for item in self.__colorVars:
            self.__picVarListBox1.insert(END, item)

        if picSettings[0] == "%":
            self.__picSettingsOption1.set(1)
            self.__lastSelectedPictureVar = self.__colorVars[0].split("::")[1]

            self.__picVarListBox1.config(state=DISABLED)

            mirrored = picSettings[5]
            index = picSettings[1:5]
            nusiz = picSettings[5:]

            self.__mirrored1.set(int(mirrored))
            self.__indexVal1.set(str(int("0b" + index, 2)))

        else:
            self.__mirroredButton1.config(state=DISABLED)
            self.__indexEntry1.config(state=DISABLED)

            self.__picSettingsOption1.set(2)

            self.__mirrored1.set(0)
            self.__indexVal1.set("0")

            selector = 0
            for itemNum in range(0, len(self.__colorVars)):
                if self.__colorVars[itemNum].split("::")[1] == picSettings:
                    selector = itemNum
                    break

            self.__picVarListBox1.select_set(selector)
            self.__picVarListBox1.yview(selector)

            self.__lastSelectedPictureVar = self.__colorVars[selector].split("::")[1]

        self.__init     = False

        self.__indexEntry1.bind("<KeyRelease>", self.__changeIndexAndMirroring1)
        self.__indexEntry1.bind("<FocusOut>", self.__changeIndexAndMirroring1)

        self.__picVarListBox1.bind("<ButtonRelease-1>", self.__changedPicVar1)
        self.__picVarListBox1.bind("<KeyRelease-Up>", self.__changedPicVar1)
        self.__picVarListBox1.bind("<KeyRelease-Down>", self.__changedPicVar1)


    def __changeForce(self):
        self.__data[10] = str(self.__forceDigistsVal.get())
        self.__changeData(self.__data)

    def __changeIconSettings(self):

        if self.__picSettingsOption1.get() == 1:
            self.__lastSelectedPictureVar = self.__colorVars[self.__picVarListBox1.curselection()[0]].split("::")[1]
            self.__picVarListBox1.config(state=DISABLED)
            self.__mirroredButton1.config(state=NORMAL)
            self.__indexEntry1.config(state=NORMAL)

            self.__changeIndexAndMirroring1(None)

        else:
            self.__mirroredButton1.config(state=DISABLED)
            self.__indexEntry1.config(state=DISABLED)
            self.__picVarListBox1.config(state=NORMAL)

            selector = 0
            for itemNum in range(0, len(self.__colorVars)):
                if self.__colorVars[itemNum].split("::")[1] == self.__lastSelectedPictureVar:
                    selector = itemNum
                    break

            self.__picVarListBox1.select_set(selector)
            self.__picVarListBox1.yview(selector)

            self.__data[9] = self.__colorVars[selector].split("::")[1]

        self.__changeData(self.__data)

    def __changeIndexAndMirroring1(self, event):
        if self.__picSettingsOption1.get() == 2: return

        mirrored = str(self.__mirrored1.get())
        try:
            number = int(self.__indexVal1.get())
        except:
            self.__indexEntry1.config(
                bg = self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                fg = self.__loader.colorPalettes.getColor("boxFontUnSaved")
            )
            return

        bg = self.__loader.colorPalettes.getColor("boxBackNormal"),
        fg = self.__loader.colorPalettes.getColor("boxFontNormal")

        if   number < 0:  number = 0
        elif number > 15: number = 15

        index = bin(number).replace("0b", "")
        while len(index) < 4:
            index = "0" + index

        self.__data[9] = "%" + index + mirrored + "000"
        self.__changeData(self.__data)

    def __mirroredChanged1(self):
        if self.__picSettingsOption1.get() == 2: return
        self.__changeIndexAndMirroring1(None)

    def __changedPicVar1(self, event):
        if self.__picSettingsOption1.get() == 1: return

        if self.__lastSelectedPictureVar != self.__colorVars[self.__picVarListBox1.curselection()[0]].split("::")[1]:
           self.__lastSelectedPictureVar = self.__colorVars[self.__picVarListBox1.curselection()[0]].split("::")[1]
           self.__data[9]                = self.__lastSelectedPictureVar
           self.__changeData(self.__data)

    def __changePicture(self, event):
        if self.__lastSelectedPicture != self.__listOfPictures[self.__picListBox1.curselection()[0]]:
           self.__lastSelectedPicture = self.__listOfPictures[self.__picListBox1.curselection()[0]]
           self.__data[3]             = self.__lastSelectedPicture
           self.__changeData(self.__data)

    def __changeDataVar(self, event):
        if self.__lastDataVar != self.__dataVars[self.__dataVarListBox.curselection()[0]].split("::")[1]:
           self.__lastDataVar  = self.__dataVars[self.__dataVarListBox.curselection()[0]].split("::")[1]
           self.__data[4]      = self.__lastDataVar
           self.__changeData(self.__data)


    def __changedFontOption1_1(self):
        if self.__data[6]   != "default":
           self.__data[6]   = "default"
           self.__fontVarListBox1.config(state = DISABLED)
           self.__changeData(self.__data)

    def __changedFontOption1_2(self):
        if self.__data[6]   != "digital":
           self.__data[6]   = "digital"
           self.__fontVarListBox1.config(state = DISABLED)
           self.__changeData(self.__data)


    def __changedFontOption1_3(self):
        self.__fontVarListBox1.config(state = NORMAL)
        selector = 0
        for itemNum in range(0, len(self.__listOfPictures2)):
            if self.__listOfPictures2[itemNum] == self.__lastSelectedFont:
                selector = itemNum
                break
        self.__fontVarListBox1.select_set(selector)
        self.__fontVarListBox1.yview(selector)

        self.__data[6]   = self.__lastSelectedFont
        self.__lastFont  = self.__lastSelectedFont
        self.__changeData(self.__data)


    def __changeConstant(self, event):
        if self.__constOrVar.get() == "2": return

        if self.isItHex(self.__hexEntry.getValue()) ==  True and self.__hexEntry.getValue() != self.__data[5]:
           self.__hexEntry.setValue(self.__hexEntry.getValue()[:2] + "6")
           self.__data[5] = self.__hexEntry.getValue()
           self.__changeData(self.__data)

    def __changeSame(self):
        if self.__sameColor.get() == 1:
           self.__textColorVarListBox.config(state = DISABLED)
           self.__hexEntry.changeState(DISABLED)
           self.__gradientFrame.changeState(DISABLED)
           self.__constButton.config(state = DISABLED)
           self.__varButton.config(state = DISABLED)

        else:
           self.__textColorVarListBox.config(state = NORMAL)
           self.__hexEntry.changeState(NORMAL)
           self.__gradientFrame.changeState(NORMAL)
           self.__constButton.config(state = NORMAL)
           self.__varButton.config(state = NORMAL)

           self.__changeIfConstOrVar()

        self.__data[8] = str(self.__sameColor.get())
        if self.__init == False: self.__changeData(self.__data)

    def __changeFont(self, event):
        if self.__fontOption1.get() != 3: return

        if self.__data[6] != self.__listOfPictures2[self.__fontVarListBox1.curselection()[0]]:
           self.__data[6] = self.__listOfPictures2[self.__fontVarListBox1.curselection()[0]]
           self.__lastFont = self.__data[6]
           self.__lastSelectedFont = self.__lastFont
           self.__changeData(self.__data)

    def __changeFontColorVar(self, event):
        if self.__sameColor.get() == 1: return

        if self.__lastTextColor != self.__colorVars[self.__textColorVarListBox.curselection()[0]].split("::")[1]:
           self.__lastTextColor  = self.__colorVars[self.__textColorVarListBox.curselection()[0]].split("::")[1]
           self.__data[5]        = self.__lastTextColor
           self.__changeData(self.__data)

    def __changeIfConstOrVar(self):
        if self.__sameColor.get() == 1: return

        if self.__constOrVar.get() == 1:
           self.__textColorVarListBox.config(state=DISABLED)
           self.__hexEntry.changeState(NORMAL)
           self.__data[5] = self.__hexEntry.getValue()

        else:
           self.__hexEntry.changeState(DISABLED)
           self.__textColorVarListBox.config(state=NORMAL)

           selector = 0
           self.__textColorVarListBox.select_clear(0, END)
           for itemNum in range(0, len(self.__colorVars)):
               # print(self.__lastTextColor, self.__colorVars[itemNum].split("::")[1])
               if self.__colorVars[itemNum].split("::")[1] == self.__lastTextColor:
                  selector = itemNum
                  break

           self.__textColorVarListBox.selection_set(selector)
           self.__lastTextColor = self.__colorVars[self.__textColorVarListBox.curselection()[0]].split("::")[1]
           self.__data[5]       = self.__lastTextColor

        if self.__init == False: self.__changeData(self.__data)

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
