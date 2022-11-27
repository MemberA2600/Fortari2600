from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from time import sleep
import re

class DigitClock:
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

        self.__listOfPictures = []

        import os

        for root, dirs, files in os.walk(self.__loader.mainWindow.projectPath + "bigSprites/"):
            for file in files:
                ok = False
                mode = ""
                frames = 0

                if file.endswith(".asm"):
                    f = open(root + "/" + file, "r")
                    text = f.read()
                    f.close()

                    firstLine = text.replace("\r", "").split("\n")[0]
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

        self.__frame1 = Frame(self.__uniqueFrame, width=self.__w // 5,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h)

        self.__frame1.pack_propagate(False)
        self.__frame1.pack(side=LEFT, anchor=E, fill=Y)

        self.__frame2 = Frame(self.__uniqueFrame, width=self.__w // 5,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h)

        self.__frame2.pack_propagate(False)
        self.__frame2.pack(side=LEFT, anchor=E, fill=Y)

        self.__frame3 = Frame(self.__uniqueFrame, width=self.__w // 5,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h)

        self.__frame3.pack_propagate(False)
        self.__frame3.pack(side=LEFT, anchor=E, fill=Y)

        self.__frame4 = Frame(self.__uniqueFrame, width=self.__w // 5,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h)

        self.__frame4.pack_propagate(False)
        self.__frame4.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__frame5 = Frame(self.__uniqueFrame, width=self.__w // 5,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h)

        self.__frame5.pack_propagate(False)
        self.__frame5.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__nibbleVars = []
        self.__byteVars   = []

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
                    if var.type == "byte": self.__byteVars.append(address + "::" + variable)


        dataVars    = self.__data[3:6]
        color       = self.__data[6]
        font        = self.__data[7]
        x24hours    = self.__data[8]
        divider     = self.__data[9]
        gradient    = self.__data[10]
        #decrement   = self.__data[11]

        # DataVar 0 contains the bits for decrementing and stop

        mainFrames = [self.__frame1, self.__frame2]
        subFrames = []

        for item in mainFrames:
            subFrames.append([])

            frame1 = Frame(item, width=self.__w // 5,
                                  bg=self.__loader.colorPalettes.getColor("window"),
                                  height=self.__h//2.5)

            frame1.pack_propagate(False)
            frame1.pack(side=TOP, anchor=E, fill=X)

            frame2 = Frame(item, width=self.__w // 5,
                                  bg=self.__loader.colorPalettes.getColor("window"),
                                  height=self.__h//2.5)

            frame2.pack_propagate(False)
            frame2.pack(side=TOP, anchor=E, fill=X)

            subFrames[-1].append(frame1)
            subFrames[-1].append(frame2)

        tempFrames = [subFrames[0][0], subFrames[0][1], subFrames[1][0]]
        self.__varsAndLists = []

        counter = 0
        for item in tempFrames:
            label = Label(item,
                              text=self.__dictionaries.getWordFromCurrentLanguage("dataVar") + ":",
                              font=self.__smallFont, fg=self.__colors.getColor("font"),
                              bg=self.__colors.getColor("window"), justify=CENTER
                              )

            label.pack_propagate(False)
            label.pack(side=TOP, anchor=CENTER, fill=BOTH)

            self.__varsAndLists.append({})
            self.__varsAndLists[counter]["var"] = StringVar()

            selector = 0
            for itemNum in range(0, len(self.__byteVars)):
                item = self.__byteVars[itemNum].split("::")[1]
                if item == dataVars[counter]:
                   selector = itemNum
                   break

            self.__varsAndLists[counter]["selected"] = selector
            self.__varsAndLists[counter]["scrollbar"] = Scrollbar(tempFrames[counter])
            self.__varsAndLists[counter]["listbox"] = Listbox(tempFrames[counter], width=100000,
                                                       name = "varBox"+str(counter),
                                                       height=1000,
                                                       yscrollcommand= self.__varsAndLists[counter]["scrollbar"].set,
                                                       selectmode=BROWSE,
                                                       exportselection=False,
                                                       font=self.__smallFont,
                                                       justify=LEFT
                                                       )

            self.__varsAndLists[counter]["listbox"].config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
            self.__varsAndLists[counter]["listbox"].config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
            self.__varsAndLists[counter]["listbox"].pack_propagate(False)

            self.__varsAndLists[counter]["scrollbar"].pack(side=RIGHT, anchor=W, fill=Y)
            self.__varsAndLists[counter]["listbox"].pack(side=LEFT, anchor=W, fill=BOTH)
            self.__varsAndLists[counter]["scrollbar"].config(command=self.__varsAndLists[counter]["listbox"].yview)

            for item in self.__byteVars:
                self.__varsAndLists[counter]["listbox"].insert(END, item)

                self.__varsAndLists[counter]["scrollbar"].pack(side=RIGHT, anchor=W, fill=Y)
                self.__varsAndLists[counter]["listbox"].pack(side=LEFT, anchor=W, fill=BOTH)

            self.__varsAndLists[counter]["listbox"].select_set(selector)
            self.__varsAndLists[counter]["listbox"].yview(selector)


            self.__varsAndLists[counter]["listbox"].bind("<ButtonRelease-1>", self.__changeDataVar)
            self.__varsAndLists[counter]["listbox"].bind("<KeyRelease-Up>", self.__changeDataVar)
            self.__varsAndLists[counter]["listbox"].bind("<KeyRelease-Down>", self.__changeDataVar)
            self.__data[3+counter] = self.__byteVars[selector].split("::")[1]

            counter += 1

        self.__x24Hours = IntVar()
        self.__x24Hours.set(int(x24hours))

        self.__x24Hoursb = Checkbutton(subFrames[1][1], width=99999,
                                             text=self.__dictionaries.getWordFromCurrentLanguage("24hours"),
                                             bg=self.__colors.getColor("window"),
                                             fg=self.__colors.getColor("font"),
                                             justify=LEFT, font=self.__smallFont,
                                             variable=self.__x24Hours,
                                             activebackground=self.__colors.getColor("highLight"),
                                             command=self.__x24HoursChanged
                                             )

        self.__x24Hoursb.pack_propagate(False)
        self.__x24Hoursb.pack(fill=X, side=TOP, anchor=N)

        """
        self.__decrement = IntVar()
        self.__decrement.set(int(decrement))

        self.__decrementb = Checkbutton(subFrames[1][1], width=99999,
                                             text=self.__dictionaries.getWordFromCurrentLanguage("decrement"),
                                             bg=self.__colors.getColor("window"),
                                             fg=self.__colors.getColor("font"),
                                             justify=LEFT, font=self.__smallFont,
                                             variable=self.__decrement,
                                             activebackground=self.__colors.getColor("highLight"),
                                             command=self.__decrementChanged
                                             )

        self.__decrementb.pack_propagate(False)
        self.__decrementb.pack(fill=X, side=TOP, anchor=N)
        """

        self.__dividerLabel = Label(subFrames[1][1],
                              text=self.__dictionaries.getWordFromCurrentLanguage("divider") + ":",
                              font=self.__smallFont, fg=self.__colors.getColor("font"),
                              bg=self.__colors.getColor("window"), justify=CENTER
                              )

        self.__dividerLabel.pack_propagate(False)
        self.__dividerLabel.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__divider = StringVar()
        self.__divider.set(divider)

        self.__dividerEntry = Entry(subFrames[1][1],
                                   bg=self.__colors.getColor("boxBackNormal"),
                                   fg=self.__colors.getColor("boxFontNormal"),
                                   width=9999, justify=CENTER,
                                   textvariable=self.__divider,
                                   font=self.__smallFont
                                   )

        self.__dividerEntry.pack_propagate(False)
        self.__dividerEntry.pack(fill=X, side=TOP, anchor=N)

        self.__dividerEntry.bind("<KeyRelease>", self.__changedDivider)
        self.__dividerEntry.bind("<FocusOut>", self.__changedDivider)

        from GradientFrame import GradientFrame
        self.__gradientFrame = GradientFrame(self.__loader, self.__frame5,
                                             self.__changeData, self.__h, self.__data, self.dead, 8, "small", 10)

        self.__colorSettings = IntVar()
        self.__colorConstButton = Radiobutton(self.__frame3, width=99999,
                                         text=self.__dictionaries.getWordFromCurrentLanguage("constant"),
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__smallFont,
                                         variable=self.__colorSettings,
                                         activebackground=self.__colors.getColor("highLight"),
                                         value=1, command=self.__colorToConst
                                         )

        self.__colorConstButton.pack_propagate(False)
        self.__colorConstButton.pack(fill=X, side=TOP, anchor=N)

        from HexEntry import HexEntry
        self.__fuckinColors = ["$16"]

        if self.isItHex(color): self.__fuckinColors[0] = color
        self.__colorEntry = HexEntry(self.__loader, self.__frame3, self.__colors, self.__colorDict,
                                     self.__normalFont, self.__fuckinColors, 0, None, self.__changeColorVar)

        self.__colorVarButton = Radiobutton(self.__frame3, width=99999,
                                         text=self.__dictionaries.getWordFromCurrentLanguage("variable"),
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__smallFont,
                                         variable=self.__colorSettings,
                                         activebackground=self.__colors.getColor("highLight"),
                                         value=2, command=self.__colorToVar
                                         )
        self.__colorVarButton.pack_propagate(False)
        self.__colorVarButton.pack(fill=X, side=TOP, anchor=N)

        self.__colorVarListScrollBar1 = Scrollbar(self.__frame3)
        self.__colorVarListBox1 = Listbox(self.__frame3, width=100000,
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

        for item in self.__nibbleVars: self.__colorVarListBox1.insert(END, item)

        self.__colorVarListBoxSelected = self.__nibbleVars[0].split("::")[1]

        self.__colorVarListBox1.bind("<ButtonRelease-1>", self.__changeColorVar)
        self.__colorVarListBox1.bind("<KeyRelease-Up>", self.__changeColorVar)
        self.__colorVarListBox1.bind("<KeyRelease-Down>", self.__changeColorVar)

        if self.isItHex(color):
           self.__colorSettings.set(1)
           self.__colorVarListBox1.config(state = DISABLED)
           self.__colorVarListBox1.select_set(0)
           self.__colorVarListBox1.yview(0)

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
                                         value=3, command=self.__changedFontOption3
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

    def __changeFontVar(self, event):
        if self.__fontOption1.get() != 3: return
        if self.__fontVarListBoxSelected   != self.__listOfPictures[self.__fontVarListBox1.curselection()[0]]:
           self.__fontVarListBoxSelected   = self.__listOfPictures[self.__fontVarListBox1.curselection()[0]]
           self.__data[7] = self.__fontVarListBoxSelected
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
             self.__data[7] = data

        elif data == "digital":
             self.__fontOption1.set(2)
             try:
                 self.__fontVarListBoxSelected = self.__listOfPictures[self.__fontVarListBox1.curselection()[0]]
             except:
                 self.__fontVarListBoxSelected = self.__listOfPictures[0]

             self.__fontVarListBox1.select_clear(0, END)
             self.__fontVarListBox1.config(state = DISABLED)
             self.__data[7] = data

        else:
            self.__fontOption1.set(3)
            self.__fontVarListBox1.config(state = NORMAL)

            self.__fontVarListBoxSelected = data

            foundIt = False

            for itemNum in range(0, len(self.__listOfPictures)):
                if self.__listOfPictures[itemNum] == self.__fontVarListBoxSelected:
                   self.__fontVarListBox1.select_set(itemNum)
                   self.__fontVarListBox1.yview(itemNum)

                   self.__data[7] = data
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
                self.__data[7] = data

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


    def __colorToConst(self):
        self.__colorVarListBox1.config(state = DISABLED)
        self.__colorEntry.changeState(NORMAL)
        self.__data[6] = self.__colorEntry.getValue()
        self.__changeData(self.__data)

    def __colorToVar(self):
        self.__colorVarListBox1.config(state = NORMAL)
        self.__colorEntry.changeState(DISABLED)

        self.__colorVarListBox1.select_clear(0, END)
        selector = 0
        for itemNum in range(0, len(self.__nibbleVars)):
            item = self.__nibbleVars[itemNum].split("::")[1]
            if item == self.__colorVarListBoxSelected:
               selector = itemNum
               break

        self.__colorVarListBox1.select_set(selector)
        self.__colorVarListBox1.yview(selector)

        self.__data[6] = self.__nibbleVars[selector].split("::")[1]
        self.__changeData(self.__data)

    def __changeColorVar(self, event):
        if self.__colorVarListBoxSelected   != self.__nibbleVars[self.__colorVarListBox1.curselection()[0]].split("::")[1]:
           self.__colorVarListBoxSelected   = self.__nibbleVars[self.__colorVarListBox1.curselection()[0]].split("::")[1]
           self.__data[6]                   = self.__colorVarListBoxSelected
           self.__changeData(self.__data)

    def __changedDivider(self, event):
        self.__changeMaxEntry(self.__divider, self.__dividerEntry, 9)

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



            if int(maxVar.get()) < 1:
               maxVar.set("1")

            if maxVar.get() != "1":
                binary = bin(int(maxVar.get())-1).replace("0b", "")
                while len(binary) < 8: binary = "0" + binary

                firstOne = None
                for num2 in range(0, len(binary)):
                    if binary[num2] == "1":
                       firstOne = num2
                       break

                if firstOne != None:
                   binary = binary[:firstOne] + "1" * (8 - firstOne)

                maxVar.set(str(int("0b"+binary, 2)+1))

            if maxVar.get() != self.__data[num]:
                temp = maxVar.get()
                if int(temp) > 256:
                    temp = "256"
                elif int(temp) < 1:
                    temp = "1"
                maxVar.set(temp)
                self.__data[num] = maxVar.get()
                self.__changeData(self.__data)

    """
    def __decrementChanged(self):
        self.__data[11] = str(self.__decrement.get())
        self.__changeData(self.__data)
    """

    def __x24HoursChanged(self):
        self.__data[8] = str(self.__x24Hours.get())
        self.__changeData(self.__data)

    def __changeDataVar(self, event):
        name        = str(event.widget).split(".")[-1]
        number      = int(name[-1])
        dataHolders = self.__varsAndLists[number]

        if dataHolders["selected"] != dataHolders["listbox"].curselection()[0]:
           dataHolders["selected"] = dataHolders["listbox"].curselection()[0]
           self.__data[number+3]   = self.__byteVars[dataHolders["selected"]].split("::")[1]
           self.__changeData(self.__data)

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