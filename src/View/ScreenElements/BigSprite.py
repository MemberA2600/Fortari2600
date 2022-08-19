from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from time import sleep

from ScreenSetterFrameBase import ScreenSetterFrameBase

class BigSprite:

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

        self.__loadPictures()

        if len(self.__listOfPictures) > 0:
            itWasHash = False
            if self.__data[2] == "#":
                itWasHash = True

            self.__setterBase = ScreenSetterFrameBase(loader, baseFrame, data, self.__name, changeName, self.dead, itemNames)
            self.__addElements()

            if itWasHash == True:
                self.__changeData(self.__data)
        else:
            blankAnimation({
                "item": "bigSprite / sprite",
                "folder": "'" + self.__loader.mainWindow.projectPath.split("/")[-2] + "/bigSprites' / '" +
                          self.__loader.mainWindow.projectPath.split("/")[-2] + "/sprites'"
            })

    def __loadPictures(self):

        self.__listOfPictures = []

        import os

        for root, dirs, files in os.walk(self.__loader.mainWindow.projectPath + "bigSprites/"):
            for file in files:
                if file.endswith(".asm"):
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

        sprite      = self.__data[2]
        vars        = self.__data[3:6]
        height      = self.__data[6]
        lineHeigth  = self.__data[7]
        mode        = self.__data[8]

        self.__listFrame = Frame(self.__uniqueFrame, width=self.__w,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h // 10 * 4)

        self.__listFrame.pack_propagate(False)
        self.__listFrame.pack(side=TOP, anchor=N, fill=X)

        self.__varListScrollBar = Scrollbar(self.__listFrame)
        self.__varListBox = Listbox(self.__listFrame, width=100000,
                                    height=1000,
                                    yscrollcommand=self.__varListScrollBar.set,
                                    selectmode=BROWSE,
                                    exportselection=False,
                                    font=self.__smallFont,
                                    justify=LEFT
                                    )

        self.__varListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__varListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__varListBox.pack_propagate(False)

        self.__varListScrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__varListBox.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__varListScrollBar.config(command=self.__varListBox.yview)

        for item in self.__listOfPictures:
            self.__varListBox.insert(END, item)

        selector = 0
        if sprite != "#":
           for itemNum in range(0, len(self.__listOfPictures)):
               if sprite == self.__listOfPictures[itemNum]:
                  selector = itemNum
                  break
        else:
            sprite = self.__listOfPictures[0]
            self.__data[2] = sprite

        self.__varListBox.select_set(selector)
        self.__lastSprite = self.__listOfPictures[selector]
        self.__getBasicDataOfPicture()

        self.__bottomFrame = Frame(self.__uniqueFrame, width=self.__w,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h)

        self.__bottomFrame.pack_propagate(False)
        self.__bottomFrame.pack(side=TOP, anchor=N, fill=BOTH)

        self.__frames = []
        frameNum = 4

        words = ["spriteVar", "color", "xPoz"]

        for num in range(0, frameNum):
            frame1 = Frame(self.__bottomFrame, width=self.__w // frameNum,
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       height=self.__h)

            frame1.pack_propagate(False)
            frame1.pack(side=LEFT, anchor=E, fill=Y)

            self.__frames.append(frame1)

            if num < len(words):
                if words[num] != None:
                    word = self.__dictionaries.getWordFromCurrentLanguage(words[num])
                    if word.endswith(":") == False: word += ":"

                    label1 = Label(frame1,
                                   text = word,
                                   font=self.__normalFont, fg=self.__colors.getColor("font"),
                                   bg=self.__colors.getColor("window"), justify=CENTER
                                   )

                    label1.pack_propagate(False)
                    label1.pack(side=TOP, anchor=CENTER, fill=X)

        self.__byteVars     = []
        self.__nibbleVars   = []
        self.__allVars      = []

        for address in self.__loader.virtualMemory.memory.keys():
            for variable in self.__loader.virtualMemory.memory[address].variables.keys():
                var = self.__loader.virtualMemory.memory[address].variables[variable]
                if ((var.validity == "global" or
                     var.validity == self.__currentBank) and
                        (var.system == False or
                         var.iterable == True or
                         var.linkable == True)
                ):
                    self.__allVars.append(address + "::" + variable)
                    if   var.type     == "byte":
                        self.__byteVars.append(address + "::" + variable)
                        self.__nibbleVars.append(address + "::" + variable)
                    elif var.type     == "nibble":
                        self.__nibbleVars.append(address + "::" + variable)

        self.__options = []

        for num in range(0, 3):
            self.__options.append({})
            self.__options[-1]["option"]    = IntVar()
            self.__options[-1]["constant"]  = Radiobutton(self.__frames[num], width=99999,
                                              name = "button" + str(num) + "_C",
                                              text=self.__dictionaries.getWordFromCurrentLanguage("constant"),
                                              bg=self.__colors.getColor("window"),
                                              fg=self.__colors.getColor("font"),
                                              justify=LEFT, font=self.__smallFont,
                                              variable=self.__options[-1]["option"],
                                              activebackground=self.__colors.getColor("highLight"),
                                              value=1
                                              )
            self.__options[-1]["constant"].bind("<ButtonRelease-1>", self.__changeSettings)
            self.__options[-1]["constant"].pack_propagate(False)
            self.__options[-1]["constant"].pack(fill=X, side=TOP, anchor=N)

            self.__options[-1]["variable"]  = Radiobutton(self.__frames[num], width=99999,
                                              name = "button" + str(num) + "_V",
                                              text=self.__dictionaries.getWordFromCurrentLanguage("variable"),
                                              bg=self.__colors.getColor("window"),
                                              fg=self.__colors.getColor("font"),
                                              justify=LEFT, font=self.__smallFont,
                                              variable=self.__options[-1]["option"],
                                              activebackground=self.__colors.getColor("highLight"),
                                              value=2
                                              )
            self.__options[-1]["variable"].bind("<ButtonRelease-1>", self.__changeSettings)
            self.__options[-1]["variable"].pack_propagate(False)

        self.__labelXXX = Label(self.__frames[0],
                       text=self.__dictionaries.getWordFromCurrentLanguage("index"),
                       font=self.__smallFont, fg=self.__colors.getColor("font"),
                       bg=self.__colors.getColor("window"), justify=CENTER
                       )

        self.__labelXXX.pack_propagate(False)
        self.__labelXXX.pack(side=TOP, anchor=CENTER, fill=X)

        self.__spriteSettingsVar = StringVar()

        self.__spriteSettingsEntry = Entry(self.__frames[0],
                                        bg=self.__colors.getColor("boxBackNormal"),
                                        fg=self.__colors.getColor("boxFontNormal"),
                                        width=9999, justify = CENTER,
                                        textvariable=self.__spriteSettingsVar,
                                        font=self.__smallFont
                                        )

        self.__spriteSettingsEntry.pack_propagate(False)
        self.__spriteSettingsEntry.pack(fill=X, side = TOP, anchor = N)

        self.__mirrored1 = IntVar()
        self.__mirroredButton1 = Checkbutton(self.__frames[0], width=99999,
                                             text=self.__dictionaries.getWordFromCurrentLanguage("mirrored"),
                                             bg=self.__colors.getColor("window"),
                                             fg=self.__colors.getColor("font"),
                                             justify=LEFT, font=self.__smallFont,
                                             variable=self.__mirrored1,
                                             activebackground=self.__colors.getColor("highLight"),
                                             command=self.__mirroredChanged
                                             )

        self.__mirroredButton1.pack_propagate(False)
        self.__mirroredButton1.pack(fill=X, side=TOP, anchor=N)

        self.__labelYYY = Label(self.__frames[0],
                       text="NUSIZ:",
                       font=self.__smallFont, fg=self.__colors.getColor("font"),
                       bg=self.__colors.getColor("window"), justify=CENTER
                       )

        self.__labelYYY.pack_propagate(False)
        self.__labelYYY.pack(side=TOP, anchor=CENTER, fill=X)

        self.__nusizVal = StringVar()

        self.__nusizEntry = Entry(self.__frames[0],
                                        bg=self.__colors.getColor("boxBackNormal"),
                                        fg=self.__colors.getColor("boxFontNormal"),
                                        width=9999, justify = CENTER,
                                        textvariable=self.__nusizVal,
                                        font=self.__smallFont
                                        )

        self.__nusizEntry.pack_propagate(False)
        self.__nusizEntry.pack(fill=X, side = TOP, anchor = N)

        self.__options[0]["variable"].pack(fill=X, side=TOP, anchor=N)

        self.__spriteSettingsVarScrollBar = Scrollbar(self.__frames[0])
        self.__spriteSettingsVarListBox = Listbox(self.__frames[0], width=100000,
                                    height=1000, name="listBox_1",
                                    yscrollcommand=self.__spriteSettingsVarScrollBar.set,
                                    selectmode=BROWSE,
                                    exportselection=False,
                                    font=self.__smallFont,
                                    justify=LEFT
                                    )

        self.__spriteSettingsVarListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__spriteSettingsVarListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__spriteSettingsVarListBox.pack_propagate(False)

        self.__spriteSettingsVarScrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__spriteSettingsVarListBox.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__spriteSettingsVarScrollBar.config(command=self.__spriteSettingsVarListBox.yview)
        for var in self.__nibbleVars:
            self.__spriteSettingsVarListBox.insert(END, var)

        if vars[0] == "#":
            vars[0] = self.__nibbleVars[0].split("::")[1]
            self.__data[3] = vars[0]

        self.__lastSelectedspriteSettings = [vars[0]]
        if self.isItBin(vars[0]):
           # self.__spriteSettingsVar.set(vars[0])
           self.__spriteSettingsVarListBox.config(state = DISABLED)
           self.__options[0]["option"].set(1)
           bytes = self.__data[3].replace("%", "")

           self.__spriteSettingsVar.set(str(int("0b"+bytes[0:4], 2)))
           self.__mirrored1.set(int(bytes[4]))
           self.__nusizVal.set(str(int("0b"+bytes[5:8], 2)))

        else:
           selector = 0
           for itemNum in range(0, len(self.__nibbleVars)):
               if self.__nibbleVars[itemNum].split("::")[1] == vars[0]:
                  selector = itemNum
                  break
           self.__lastSelectedspriteSettings[0] = self.__nibbleVars[selector].split("::")[1]
           self.__spriteSettingsVarListBox.select_set(selector)
           self.__spriteSettingsEntry.config(state = DISABLED)
           self.__mirroredButton1.config(state = DISABLED)
           self.__nusizEntry.config(state = DISABLED)
           self.__options[0]["option"].set(2)
           self.__spriteSettingsVar.set("0")
           self.__mirrored1.set(0)
           self.__nusizVal.set("0")

        self.__spriteSettingsVarListBox.bind("<ButtonRelease-1>", self.__changeListBoxItem)
        self.__spriteSettingsVarListBox.bind("<KeyRelease-Up>", self.__changeListBoxItem)
        self.__spriteSettingsVarListBox.bind("<KeyRelease-Down>", self.__changeListBoxItem)

        self.__spriteSettingsEntry.bind("<KeyRelease>", self.__changedSpriteConst)
        self.__spriteSettingsEntry.bind("<FocusOut>", self.__changedSpriteConst)
        self.__nusizEntry.bind("<KeyRelease>", self.__changedSpriteConst)
        self.__nusizEntry.bind("<FocusOut>", self.__changedSpriteConst)

        from HexEntry import HexEntry
        self.__fuckinColors = ["$00"]

        self.__constantHex = HexEntry(self.__loader, self.__frames[1], self.__colors, self.__colorDict,
                                     self.__smallFont, self.__fuckinColors, 0, None, self.__changeHex)

        self.__options[1]["variable"].pack(fill=X, side=TOP, anchor=N)

        self.__backColorScrollBar = Scrollbar(self.__frames[1])
        self.__backColorListBox = Listbox(self.__frames[1], width=100000,
                                    height=1000, name="listBox_2",
                                    yscrollcommand=self.__backColorScrollBar.set,
                                    selectmode=BROWSE,
                                    exportselection=False,
                                    font=self.__smallFont,
                                    justify=LEFT
                                    )

        self.__backColorListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__backColorListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__backColorListBox.pack_propagate(False)

        self.__backColorScrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__backColorListBox.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__backColorScrollBar.config(command=self.__backColorListBox.yview)

        for var in self.__nibbleVars:
            self.__backColorListBox.insert(END, var)

        if vars[1] == "#":
            vars[1] = "$00"
            self.__data[4] = vars[1]

        self.__lastBackColorSelected = [self.__nibbleVars[0].split("::")[1]]

        if self.isItHex(vars[1]):
           self.__constantHex.setValue(vars[1])
           self.__backColorListBox.config(state = DISABLED)
           self.__options[1]["option"].set(1)
        else:
           selector = 0
           for itemNum in range(0, len(self.__nibbleVars)):
               if self.__nibbleVars[itemNum].split("::")[1] == vars[1]:
                  selector = itemNum
                  break
           self.__lastBackColorSelected[0] = self.__nibbleVars[selector].split("::")[1]
           self.__backColorListBox.select_set(selector)
           self.__constantHex.changeState(DISABLED)
           self.__options[1]["option"].set(2)

        self.__backColorListBox.bind("<ButtonRelease-1>", self.__changeListBoxItem)
        self.__backColorListBox.bind("<KeyRelease-Up>", self.__changeListBoxItem)
        self.__backColorListBox.bind("<KeyRelease-Down>", self.__changeListBoxItem)

        self.__xVal   = StringVar()

        self.__xEntry = Entry(self.__frames[2],
                                        bg=self.__colors.getColor("boxBackNormal"),
                                        fg=self.__colors.getColor("boxFontNormal"),
                                        width=9999, justify = CENTER,
                                        textvariable=self.__xVal,
                                        font=self.__smallFont
                                        )

        self.__xEntry.pack_propagate(False)
        self.__xEntry.pack(fill=X, side = TOP, anchor = N)

        self.__options[2]["variable"].pack(fill=X, side=TOP, anchor=N)

        self.__xSettingsVarScrollBar = Scrollbar(self.__frames[2])
        self.__xSettingsVarListBox = Listbox(self.__frames[2], width=100000,
                                    height=1000, name="listBox_3",
                                    yscrollcommand=self.__xSettingsVarScrollBar.set,
                                    selectmode=BROWSE,
                                    exportselection=False,
                                    font=self.__smallFont,
                                    justify=LEFT
                                    )

        self.__xSettingsVarListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__xSettingsVarListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__xSettingsVarListBox.pack_propagate(False)

        self.__xSettingsVarListBox.pack(side=RIGHT, anchor=W, fill=Y)
        self.__xSettingsVarListBox.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__xSettingsVarScrollBar.config(command=self.__xSettingsVarListBox.yview)
        for var in self.__byteVars:
            self.__xSettingsVarListBox.insert(END, var)

        self.__xSettingsVarListBox.bind("<ButtonRelease-1>", self.__changeListBoxItem)
        self.__xSettingsVarListBox.bind("<KeyRelease-Up>", self.__changeListBoxItem)
        self.__xSettingsVarListBox.bind("<KeyRelease-Down>", self.__changeListBoxItem)
        self.__xEntry.bind("<KeyRelease>", self.__changeXEntry)
        self.__xEntry.bind("<FocusOut>", self.__changeXEntry)

        self.__lastXSelected = [self.__byteVars[0].split("::")[1]]

        if vars[2] == "#":
           vars[2] =  self.__byteVars[0].split("::")[1]
           self.__options[2]["option"].set(2)
           self.__xEntry.config(state = DISABLED)
           self.__xSettingsVarListBox.select_set(0)
           self.__data[5] = vars[2]
           self.__xVal.set("127")

        else:
            var = vars[2]
            if self.isItNum(var):
               self.__options[2]["option"].set(1)
               self.__xSettingsVarListBox.config(state = DISABLED)
               self.__xVal.set(var)

            else:
               selector = 0
               for itemNum in range(0, len(self.__byteVars)):
                   if self.__byteVars[itemNum].split("::")[1] == vars[2]:
                       selector = itemNum
                       break

               self.__options[2]["option"].set(2)
               self.__xEntry.config(state = DISABLED)
               self.__xSettingsVarListBox.select_set(selector)
               self.__lastXSelected[0] = self.__byteVars[selector].split("::")[1]
               self.__xVal.set("127")

        self.__label1 = Label(self.__frames[3],
                       text=self.__dictionaries.getWordFromCurrentLanguage("height"),
                       font=self.__smallFont, fg=self.__colors.getColor("font"),
                       bg=self.__colors.getColor("window"), justify=CENTER
                       )

        self.__label1.pack_propagate(False)
        self.__label1.pack(side=TOP, anchor=CENTER, fill=X)

        self.__heightVal = StringVar()
        self.__heightEntry = Entry(self.__frames[3],
                                        bg=self.__colors.getColor("boxBackNormal"),
                                        fg=self.__colors.getColor("boxFontNormal"),
                                        width=9999, justify = CENTER,
                                        textvariable=self.__heightVal,
                                        font=self.__smallFont
                                        )

        self.__heightEntry.pack_propagate(False)
        self.__heightEntry.pack(fill=X, side = TOP, anchor = N)

        if   height == "#" or int(height) > self.__maxHeight:
             height = str(self.__maxHeight)
             self.__data[6] = height

        self.__heightVal.set(height)

        self.__label2 = Label(self.__frames[3],
                       text=self.__dictionaries.getWordFromCurrentLanguage("lineHeight"),
                       font=self.__smallFont, fg=self.__colors.getColor("font"),
                       bg=self.__colors.getColor("window"), justify=CENTER
                       )

        self.__label2.pack_propagate(False)
        self.__label2.pack(side=TOP, anchor=CENTER, fill=X)

        self.__lineHeightVal = StringVar()
        self.__lineHeightEntry = Entry(self.__frames[3],
                                        bg=self.__colors.getColor("boxBackNormal"),
                                        fg=self.__colors.getColor("boxFontNormal"),
                                        width=9999, justify = CENTER,
                                        textvariable=self.__lineHeightVal,
                                        font=self.__smallFont
                                        )

        self.__lineHeightEntry.pack_propagate(False)
        self.__lineHeightEntry.pack(fill=X, side = TOP, anchor = N)

        if lineHeigth == "#":
            lineHeigth = str(self.__lineHeightDefault)
            self.__data[7] = lineHeigth

        self.__lineHeightVal.set(lineHeigth)

        self.__label3 = Label(self.__frames[3],
                       text=self.__dictionaries.getWordFromCurrentLanguage("spriteType"),
                       font=self.__smallFont, fg=self.__colors.getColor("font"),
                       bg=self.__colors.getColor("window"), justify=CENTER
                       )

        self.__label3.pack_propagate(False)
        self.__label3.pack(side=TOP, anchor=CENTER, fill=X)

        # simple, double, overlay

        self.__modeOption = IntVar()
        self.__modeButton1 = Radiobutton(self.__frames[3], width=99999,
                                         text=self.__dictionaries.getWordFromCurrentLanguage("simple"),
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__smallFont,
                                         variable=self.__modeOption,
                                         activebackground=self.__colors.getColor("highLight"),
                                         value=1, command=self.__changeMode
                                         )

        self.__modeButton1.pack_propagate(False)
        self.__modeButton1.pack(fill=X, side=TOP, anchor=N)

        self.__modeButton2 = Radiobutton(self.__frames[3], width=99999,
                                         text=self.__dictionaries.getWordFromCurrentLanguage("double"),
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__smallFont,
                                         variable=self.__modeOption,
                                         activebackground=self.__colors.getColor("highLight"),
                                         value=2, command=self.__changeMode
                                         )

        self.__modeButton2.pack_propagate(False)
        self.__modeButton2.pack(fill=X, side=TOP, anchor=N)

        self.__modeButton3 = Radiobutton(self.__frames[3], width=99999,
                                         text=self.__dictionaries.getWordFromCurrentLanguage("overlay"),
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__smallFont,
                                         variable=self.__modeOption,
                                         activebackground=self.__colors.getColor("highLight"),
                                         value=3, command=self.__changeMode
                                         )

        self.__modeButton3.pack_propagate(False)
        self.__modeButton3.pack(fill=X, side=TOP, anchor=N)

        self.__defaultButton = Button(self.__frames[3], width=99999,
                                         text=self.__dictionaries.getWordFromCurrentLanguage("default"),
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__normalFont,
                                         activebackground=self.__colors.getColor("highLight"),
                                         command=self.__setDefaults
                                         )

        self.__defaultButton.pack_propagate(False)
        self.__defaultButton.pack(fill=X, side=BOTTOM, anchor=N)

        modes = ["simple", "double", "overlay"]
        if mode == "#":
            mode = self.__defaultMode
            self.__data[8] = mode

        self.__modeOption.set(modes.index(mode)+1)

        self.__heightEntry.bind("<KeyRelease>", self.__changeConstEntry)
        self.__heightEntry.bind("<FocusOut>", self.__changeConstEntry)

        self.__lineHeightEntry.bind("<KeyRelease>", self.__changeConstEntry)
        self.__lineHeightEntry.bind("<FocusOut>", self.__changeConstEntry)

        self.__varListBox.bind("<ButtonRelease-1>", self.__changeSprite)
        self.__varListBox.bind("<KeyRelease-Up>", self.__changeSprite)
        self.__varListBox.bind("<KeyRelease-Down>", self.__changeSprite)

    def __changeSprite(self, event):
        if self.__lastSprite != self.__listOfPictures[self.__varListBox.curselection()[0]]:
           self.__lastSprite = self.__listOfPictures[self.__varListBox.curselection()[0]]
           self.__getBasicDataOfPicture()

           if self.isItNum(self.__spriteSettingsVar.get()):
              val = int(self.__spriteSettingsVar.get())
              if val > self.__maxNumberOfFrames - 1:
                 val = self.__maxNumberOfFrames - 1
                 self.__spriteSettingsVar.set(str(val))

           self.__heightVal.set(str(self.__maxHeight))
           self.__lineHeightVal.set(str(self.__lineHeightDefault))

           modes = ["simple", "double", "overlay"]
           self.__modeOption.set(modes.index(self.__defaultMode) + 1)

           self.__data[2] = self.__lastSprite
           self.__data[6] = self.__heightVal.get()
           self.__data[7] = self.__lineHeightVal.get()
           self.__data[8] = modes[self.__modeOption.get()-1]

           if self.__options[0]["option"] == 1:
              self.__changedSpriteConst("FUCK")

           self.__changeData(self.__data)

    def __setDefaults(self):
        self.__heightVal.set(str(self.__maxHeight))
        self.__lineHeightVal.set(str(self.__lineHeightDefault))

        modes = ["simple", "double", "overlay"]
        self.__modeOption.set(modes.index(self.__defaultMode)+1)

        self.__data[6] = self.__heightVal.get()
        self.__data[7] = self.__lineHeightVal.get()
        self.__data[8] = modes[self.__modeOption.get() - 1]

        if self.__options[0]["option"] == 1:
            self.__changedSpriteConst("FUCK")

        self.__changeData(self.__data)

    def __changeConstEntry(self, event):
        entries = [self.__heightEntry, self.__lineHeightEntry]
        num     = entries.index(event.widget)

        vals    = [self.__heightVal, self.__lineHeightVal]
        value   = vals[num].get()

        if self.isItNum(value) == False:
            entries[num].config(
                bg = self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                fg = self.__loader.colorPalettes.getColor("boxFontUnSaved")
            )
            return
        entries[num].config(
            bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
            fg=self.__loader.colorPalettes.getColor("boxFontNormal")
        )

        value = int(value)
        if value < 1:   value = 1
        if value > 255: value = 255

        maxs    = [self.__maxHeight, 255]
        if value > maxs[num]: value = maxs[num]

        vals[num].set(str(value))
        self.__data[6+num] = str(value)
        self.__changeData(self.__data)

    def __changeMode(self):
        modes = ["simple", "double", "overlay"]

        self.__data[8] = modes[self.__modeOption.get() - 1]
        self.__changeData(self.__data)

    def __changeXEntry(self, event):
        val = self.__xVal.get()
        try:
            num = int(val)
        except:
            self.__xEntry.config(
                bg = self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                fg = self.__loader.colorPalettes.getColor("boxFontUnSaved")
            )
            return

        self.__xEntry.config(
            bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
            fg=self.__loader.colorPalettes.getColor("boxFontNormal")
        )

        if num < 0  : num = 0
        if num > 255: num = 255

        self.__xVal.set(str(num))

        self.__data[5] = val
        self.__changeData(self.__data)

    def __changeHex(self, event):
        val = self.__constantHex.getValue()
        if self.isItHex(val) == True:
           if val != self.__data[3]:
              val            = val[:2] + str(int(val[2]) // 2 * 2)
              self.__constantHex.setValue(val)
              self.__data[4] = val
              self.__changeData(self.__data)

    def __mirroredChanged(self):
        self.__changedSpriteConst(None)

    def __changedSpriteConst(self, event):
        isThereError = False

        num  = 0
        num2 = 0
        temp = self.__spriteSettingsVar.get()
        try:
            num = int(temp)
            self.__spriteSettingsEntry.config(
                bg = self.__loader.colorPalettes.getColor("boxBackNormal"),
                fg = self.__loader.colorPalettes.getColor("boxFontNormal")
            )
        except:
            self.__spriteSettingsEntry.config(
                bg = self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                fg = self.__loader.colorPalettes.getColor("boxFontUnSaved")
            )
            isThereError = True

        temp = self.__nusizVal.get()
        try:
            num2 = int(temp)
            self.__nusizEntry.config(
                bg = self.__loader.colorPalettes.getColor("boxBackNormal"),
                fg = self.__loader.colorPalettes.getColor("boxFontNormal")
            )
        except:
            self.__nusizEntry.config(
                bg = self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                fg = self.__loader.colorPalettes.getColor("boxFontUnSaved")
            )
            isThereError = True

        if isThereError == True: return
        if num > 15: num = 15
        if num > self.__maxNumberOfFrames - 1: num = self.__maxNumberOfFrames - 1
        if num < 0: num = 0

        self.__spriteSettingsVar.set(str(num))

        if num2 > 7: num2 = 7
        if num2 < 0: num2 = 0

        self.__nusizVal.set(str(num2))

        frameNum = bin(num).replace("0b", "")
        while len(frameNum) < 4: frameNum = "0"+frameNum

        nusiz = bin(num2).replace("0b", "")
        while len(nusiz) < 3: nusiz = "0"+nusiz

        self.__data[3] = "%"+frameNum+str(self.__mirrored1.get())+nusiz
        if event != "FUCK": self.__changeData(self.__data)

    def __changeListBoxItem(self, event):
        lboxes  = [self.__spriteSettingsVarListBox, self.__backColorListBox, self.__xSettingsVarListBox]
        types   = [self.__nibbleVars, self.__nibbleVars, self.__byteVars]
        lasts   = [self.__lastSelectedspriteSettings, self.__lastBackColorSelected, self.__lastXSelected]

        name    = str(event.widget).split(".")[-1]
        num     = int(name[-1])-1
        lbox    = lboxes[num]
        value   = types[num][lbox.curselection()[0]].split("::")[1]

        if value == lasts[num][0]: return

        lasts[num][0] = value
        self.__data[3+num] = value
        self.__changeData(self.__data)

    def __changeSettings(self, event):
        name = str(event.widget).split(".")[-1]
        things = name[6:].split("_")
        num  = int(things[0])
        mode = things[1]

        entries     = [[self.__spriteSettingsEntry, self.__mirroredButton1, self.__nusizEntry],
                       [self.__constantHex.getEntry()],
                       [self.__xEntry]]

        lasts       = [self.__lastSelectedspriteSettings, self.__lastBackColorSelected, self.__lastXSelected]
        lboxes      = [self.__spriteSettingsVarListBox  , self.__backColorListBox     , self.__xSettingsVarListBox]
        lists       = [self.__nibbleVars                , self.__nibbleVars           , self.__byteVars]

        if mode.upper() == "C":
           for item in entries[num]:
               item.config(state = NORMAL)

           lboxes [num].config(state = DISABLED)
           newData = ""
           if   num == 0:
                newData = "%"
                first = bin(int(self.__spriteSettingsVar.get())).replace("0b", "")
                while len(first) < 4: first = "0" + first
                newData += first + str(self.__mirrored1.get())
                second =  bin(int(self.__nusizVal.get())).replace("0b", "")
                while len(second) < 3: second = "0" + second
                newData += second
           elif num == 1:
                val = self.__constantHex.getValue()
                if self.isItHex(val):
                   newData = val
           elif num == 2:
               val = self.__xVal.get()
               if self.isItNum(val):
                   newData = val

           if newData != "":
               self.__data[3+num] = newData
               self.__changeData(self.__data)
        else:
            for item in entries[num]:
                item.config(state=DISABLED)
            lboxes[num].config(state=NORMAL)

            selector = 0
            for itemNum in range(0, len(lists[num])):
                if lasts[num][0] == lists[num][itemNum].split("::")[1]:
                    selector = itemNum
                    break

            lasts[num][0] = lists[num][selector].split("::")[1]

            lboxes[num].select_clear(0, END)
            lboxes[num].select_set(selector)
            self.__data[3+num] = lasts[num][0]
            self.__changeData(self.__data)

    def isItBin(self, value):
        if   value.startswith("%") == False: return False
        elif len(value) != 9:                return False

        try:
            num = int(value.replace("%", "0b"), 2)
            return True
        except:
            return False

    def __getBasicDataOfPicture(self):
        name = self.__listOfPictures[self.__varListBox.curselection()[0]].split("_(")[0] + ".asm"
        typ  = self.__listOfPictures[self.__varListBox.curselection()[0]].split("_(")[1][:-1]

        folder = "sprites"

        if typ == "Big":
           folder = "bigSprites"

        fullname = self.__loader.mainWindow.projectPath + "/" + folder + "/" + name
        f = open(fullname, "r")
        lines = f.readlines()
        f.close()

        data = {}

        for line in lines:
            if line.startswith("*") or line.startswith("#") and ("=" in line):
               line = line.split("=")
               data[line[0].split(" ")[1]] = line[1].replace("\n", "").replace("\r", "")

        try:
            self.__maxNumberOfFrames = int(data["Frames"])
        except:
            self.__maxNumberOfFrames = 1

        try:
            self.__maxHeight = int(data["Height"])
        except:
            self.__maxHeight = 1

        try:
            self.__lineHeightDefault = int(data["LineHeight"])
        except:
            # sprites are 3 lines height
            self.__lineHeightDefault = 3

        try:
            self.__defaultMode = data["Mode"]
        except:
            self.__defaultMode = "simple"

    def isItNum(self, num):
        try:
            num = int(num)
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