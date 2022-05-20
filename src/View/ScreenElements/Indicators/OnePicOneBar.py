from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from time import sleep
import re


class OnePicOneBar:

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
        if itWasHash == True: self.__changeData(data)

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

        self.__frame1 = Frame(self.__uniqueFrame, width=self.__w // 7,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h)

        self.__frame1.pack_propagate(False)
        self.__frame1.pack(side=LEFT, anchor=E, fill=Y)

        self.__frame2 = Frame(self.__uniqueFrame, width=self.__w // 7,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h)

        self.__frame2.pack_propagate(False)
        self.__frame2.pack(side=LEFT, anchor=E, fill=Y)

        self.__frame3 = Frame(self.__uniqueFrame, width=self.__w // 7,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h)

        self.__frame3.pack_propagate(False)
        self.__frame3.pack(side=LEFT, anchor=E, fill=Y)

        self.__frame4 = Frame(self.__uniqueFrame, width=self.__w // 7,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h)

        self.__frame4.pack_propagate(False)
        self.__frame4.pack(side=LEFT, anchor=E, fill=Y)

        self.__frame5 = Frame(self.__uniqueFrame, width=self.__w // 7,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h)

        self.__frame5.pack_propagate(False)
        self.__frame5.pack(side=LEFT, anchor=E, fill=Y)

        self.__frame6 = Frame(self.__uniqueFrame, width=(self.__w // 7) * 2,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h)

        self.__frame6.pack_propagate(False)
        self.__frame6.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__label1 = Label(self.__frame1,
                              text=self.__dictionaries.getWordFromCurrentLanguage("dataVar") + ":",
                              font=self.__smallFont, fg=self.__colors.getColor("font"),
                              bg=self.__colors.getColor("window"), justify=CENTER
                              )

        self.__label1.pack_propagate(False)
        self.__label1.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__label2 = Label(self.__frame2,
                              text=self.__dictionaries.getWordFromCurrentLanguage("maxVal") + ":",
                              font=self.__smallFont, fg=self.__colors.getColor("font"),
                              bg=self.__colors.getColor("window"), justify=CENTER
                              )

        self.__label2.pack_propagate(False)
        self.__label2.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__label3 = Label(self.__frame3,
                              text=self.__dictionaries.getWordFromCurrentLanguage("color") + ":",
                              font=self.__smallFont, fg=self.__colors.getColor("font"),
                              bg=self.__colors.getColor("window"), justify=CENTER
                              )

        self.__label3.pack_propagate(False)
        self.__label3.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__label4 = Label(self.__frame4,
                              text=self.__dictionaries.getWordFromCurrentLanguage("gradient") + ":",
                              font=self.__smallFont, fg=self.__colors.getColor("font"),
                              bg=self.__colors.getColor("window"), justify=CENTER
                              )

        self.__label4.pack_propagate(False)
        self.__label4.pack(side=TOP, anchor=CENTER, fill=BOTH)

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

        self.__dataVarListScrollBar = Scrollbar(self.__frame1)
        self.__dataVarListBox = Listbox(self.__frame1, width=100000,
                                        height=1000,
                                        yscrollcommand=self.__dataVarListScrollBar.set,
                                        selectmode=BROWSE,
                                        exportselection=False,
                                        font=self.__smallFont,
                                        justify=LEFT
                                        )

        self.__dataVarListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__dataVarListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__dataVarListBox.pack_propagate(False)

        self.__dataVarListScrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__dataVarListBox.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__dataVarListScrollBar.config(command=self.__dataVarListBox.yview)

        for item in self.__dataVars:
            self.__dataVarListBox.insert(END, item)

        self.__dataVarListBox.select_clear(0)
        if self.__data[3] == "#":
            self.__data[3] = self.__dataVars[0].split("::")[1]
            self.__dataVarListBox.select_set(0)
        else:
            for itemNum in range(0, len(self.__dataVars)):
                if self.__dataVars[itemNum] == self.__data[3]:
                    self.__dataVarListBox.select_set(itemNum)
                    break

        self.__dataVarListBox.bind("<ButtonRelease-1>", self.__changedDataVar)
        self.__dataVarListBox.bind("<KeyRelease-Up>", self.__changedDataVar)
        self.__dataVarListBox.bind("<KeyRelease-Down>", self.__changedDataVar)


        self.__maxVar = StringVar()

        if self.isItNum(self.__data[4]) == True:
            self.__maxVar.set(self.__data[4])
        else:
            self.__maxVar.set("255")

        self.__maxVarEntry = Entry(self.__frame2,
                                   bg=self.__colors.getColor("boxBackNormal"),
                                   fg=self.__colors.getColor("boxFontNormal"),
                                   width=9999, justify=CENTER,
                                   textvariable=self.__maxVar,
                                   font=self.__smallFont
                                   )

        self.__maxVarEntry.pack_propagate(False)
        self.__maxVarEntry.pack(fill=X, side=TOP, anchor=N)

        self.__colorOption = IntVar()

        self.__constButton = Radiobutton(self.__frame3, width=99999,
                                         text=self.__dictionaries.getWordFromCurrentLanguage("constant"),
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__miniFont,
                                         variable=self.__colorOption,
                                         activebackground=self.__colors.getColor("highLight"),
                                         value=1, command=self.XXX
                                         )

        self.__constButton.pack_propagate(False)
        self.__constButton.pack(fill=X, side=TOP, anchor=N)

        from HexEntry import HexEntry
        self.__color = [self.__data[5]]

        self.__constEntry = HexEntry(self.__loader, self.__frame3, self.__colors, self.__colorDict,
                                     self.__normalFont, self.__color, 0, None, self.__chamgeConst)

        self.__varButton = Radiobutton(self.__frame3, width=99999,
                                       text=self.__dictionaries.getWordFromCurrentLanguage("variable"),
                                       bg=self.__colors.getColor("window"),
                                       fg=self.__colors.getColor("font"),
                                       justify=LEFT, font=self.__smallFont,
                                       variable=self.__colorOption,
                                       activebackground=self.__colors.getColor("highLight"),
                                       value=2, command=self.XXX
                                       )

        self.__varButton.pack_propagate(False)
        self.__varButton.pack(fill=X, side=TOP, anchor=N)

        self.__colorVarListScrollBar = Scrollbar(self.__frame3)
        self.__colorVarListBox = Listbox(self.__frame3, width=100000,
                                         height=1000,
                                         yscrollcommand=self.__colorVarListScrollBar.set,
                                         selectmode=BROWSE,
                                         exportselection=False,
                                         font=self.__smallFont,
                                         justify=LEFT
                                         )

        self.__colorVarListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__colorVarListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__colorVarListBox.pack_propagate(False)

        self.__colorVarListScrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__colorVarListBox.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__colorVarListScrollBar.config(command=self.__colorVarListBox.yview)

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

        for item in self.__colorVars:
            self.__colorVarListBox.insert(END, item)

        if self.isItHex(self.__data[5]) == True:
            self.__colorOption.set(1)
            self.__constEntry.setValue(self.__data[5])
            self.__color[0] = self.__data[5]
            self.__constEntry.changeState(NORMAL)
            self.__colorVarListBox.select_clear(0, END)
            self.__colorVarListBox.config(state=DISABLED)
        else:
            self.__colorOption.set(2)
            self.__constEntry.setValue("$40")
            self.__color[0] = "$40"
            self.__constEntry.changeState(DISABLED)
            self.__colorVarListBox.config(state=NORMAL)
            for selector in range(0, len(self.__colorVars)):
                if self.__colorVars[selector].split("::")[1] == self.__data[5]:
                    self.__colorVarListBox.select_set(selector)
                    break

        from GradientFrame import GradientFrame
        self.__gradientFrame = GradientFrame(self.__loader, self.__frame4,
                                             self.__changeData, self.__h, self.__data, self.dead, 8, "small", 6)

        self.__maxVarEntry.bind("<KeyRelease>", self.__changeMaxEntry)
        self.__maxVarEntry.bind("<FocusOut>", self.__changeMaxEntry)
        self.__colorVarListBox.bind("<ButtonRelease-1>", self.__changedColorVar)
        self.__colorVarListBox.bind("<KeyRelease-Up>", self.__changedColorVar)
        self.__colorVarListBox.bind("<KeyRelease-Down>", self.__changedColorVar)

        try:
            self.__lastSet = self.__colorVars[self.__colorVarListBox.curselection()[0]]
        except:
            self.__lastSet = self.__colorVars[0]

        try:
            self.__lastConst = self.__constEntry.getValue()
        except:
            self.__lastConst = "$00"


        ### From here comes the real fun

        self.__listOfPictures = []
        import os

        for root, dirs, files in os.walk(self.__loader.mainWindow.projectPath+"bigSprites/"):
            for file in files:
                ok = False
                if file.endswith(".asm"):
                   f = open(root + "/" + file, "r")
                   text = f.read()
                   f.close()

                   firstLine = text.replace("\r", "").split("\n")[0]
                   if "Height" in firstLine:
                       try:
                          num = int(firstLine.split("=")[1])
                          if num == 8:
                             ok = True
                       except:
                          pass
                if ok == True:
                    self.__listOfPictures.append(file.replace(".asm", ""))

        self.__label5 = Label(self.__frame5,
                              text=self.__dictionaries.getWordFromCurrentLanguage("spriteName") + ":",
                              font=self.__smallFont, fg=self.__colors.getColor("font"),
                              bg=self.__colors.getColor("window"), justify=CENTER
                              )

        self.__label5.pack_propagate(False)
        self.__label5.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__picVarListScrollBar = Scrollbar(self.__frame5)
        self.__picVarListBox = Listbox(self.__frame5, width=100000,
                                         height=1000,
                                         yscrollcommand=self.__picVarListScrollBar.set,
                                         selectmode=BROWSE,
                                         exportselection=False,
                                         font=self.__smallFont,
                                         justify=LEFT
                                         )

        self.__picVarListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__picVarListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__picVarListBox.pack_propagate(False)

        self.__picVarListScrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__picVarListBox.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__picVarListScrollBar.config(command=self.__picVarListBox.yview)

        for item in self.__listOfPictures:
            self.__picVarListBox.insert(END, item)

        self.__picVarListBox.select_clear(0, END)
        if self.__data[7] == "#":
           self.__data[7] = self.__listOfPictures[0]
           self.__picVarListBox.select_set(0)
        else:
           for itemNum in range(0, len(self.__listOfPictures)):
               if self.__data[7] == self.__listOfPictures[itemNum]:
                  self.__picVarListBox.select_set(itemNum)
                  break

        self.__lastPicture = self.__data[7]
        self.__picVarListBox.bind("<ButtonRelease-1>", self.__changedPicture)
        self.__picVarListBox.bind("<KeyRelease-Up>", self.__changedPicture)
        self.__picVarListBox.bind("<KeyRelease-Down>", self.__changedPicture)

        self.__label6 = Label(self.__frame6,
                              text=self.__dictionaries.getWordFromCurrentLanguage("spriteVar") + ":",
                              font=self.__smallFont, fg=self.__colors.getColor("font"),
                              bg=self.__colors.getColor("window"), justify=CENTER
                              )

        self.__label6.pack_propagate(False)
        self.__label6.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__picOption = IntVar()

        self.__constButton2 = Radiobutton(self.__frame6, width=99999,
                                         text=self.__dictionaries.getWordFromCurrentLanguage("constant"),
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__smallFont,
                                         variable=self.__picOption,
                                         activebackground=self.__colors.getColor("highLight"),
                                         value=1, command=self.XXX2
                                         )

        self.__constButton2.pack_propagate(False)
        self.__constButton2.pack(fill=X, side=TOP, anchor=N)

        w = ((self.__w // 7) * 2 ) // 3
        h = self.__h // 6

        self.__frame6C = Frame(self.__frame6, width= (self.__w // 7) * 2,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=h)

        self.__frame6C.pack_propagate(False)
        self.__frame6C.pack(side=TOP, anchor=N, fill=Y)

        self.__frame6_1 = Frame(self.__frame6C, width=w,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=h)

        self.__frame6_1.pack_propagate(False)
        self.__frame6_1.pack(side=LEFT, anchor=E, fill=Y)

        self.__frame6_2 = Frame(self.__frame6C, width=w,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=h)

        self.__frame6_2.pack_propagate(False)
        self.__frame6_2.pack(side=LEFT, anchor=E, fill=Y)

        self.__frame6_3 = Frame(self.__frame6C, width=w,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=h)

        self.__frame6_3.pack_propagate(False)
        self.__frame6_3.pack(side=LEFT, anchor=E, fill=Y)

        self.__varButton2 = Radiobutton(self.__frame6, width=99999,
                                       text=self.__dictionaries.getWordFromCurrentLanguage("variable"),
                                       bg=self.__colors.getColor("window"),
                                       fg=self.__colors.getColor("font"),
                                       justify=LEFT, font=self.__smallFont,
                                       variable=self.__picOption,
                                       activebackground=self.__colors.getColor("highLight"),
                                       value=2, command=self.XXX2
                                       )

        self.__varButton2.pack_propagate(False)
        self.__varButton2.pack(fill=X, side=TOP, anchor=N)

        self.__mirrorLabel = Label(self.__frame6_1,
                              text=self.__dictionaries.getWordFromCurrentLanguage("mirrored") + ":",
                              font=self.__miniFont, fg=self.__colors.getColor("font"),
                              bg=self.__colors.getColor("window"), justify=CENTER
                              )

        self.__mirrorLabel.pack_propagate(False)
        self.__mirrorLabel.pack(side=TOP, anchor=CENTER, fill=X)

        self.__nusizLabel = Label(self.__frame6_2,
                              text="NUSIZ:",
                              font=self.__miniFont, fg=self.__colors.getColor("font"),
                              bg=self.__colors.getColor("window"), justify=CENTER
                              )

        self.__nusizLabel.pack_propagate(False)
        self.__nusizLabel.pack(side=TOP, anchor=CENTER, fill=X)

        self.__indexLabel = Label(self.__frame6_3,
                              text=self.__dictionaries.getWordFromCurrentLanguage("index"),
                              font=self.__miniFont, fg=self.__colors.getColor("font"),
                              bg=self.__colors.getColor("window"), justify=CENTER
                              )

        self.__indexLabel.pack_propagate(False)
        self.__indexLabel.pack(side=TOP, anchor=CENTER, fill=X)

        self.__mirrored = IntVar()

        self.__mirroredButton = Checkbutton(self.__frame6_1, width=99999,
                                       text=self.__dictionaries.getWordFromCurrentLanguage("mirrored"),
                                       bg=self.__colors.getColor("window"),
                                       fg=self.__colors.getColor("font"),
                                       justify=LEFT, font=self.__smallFont,
                                       variable=self.__mirrored,
                                       activebackground=self.__colors.getColor("highLight"),
                                       command=self.__mirroredChanged
                                       )

        self.__mirroredButton.pack_propagate(False)
        self.__mirroredButton.pack(fill=X, side=TOP, anchor=N)
        if self.__data[8][4] == "1" and self.__data[8][0] == "%":
           self.__mirrored.set(1)
        else:
           self.__mirrored.set(0)

        from NUSIZFrame import NUSIZFrame

        self.__nusizFrame = NUSIZFrame(self.__loader, self.__frame6_2, self.__changeData,
                                       h, self.__data, self.dead, "small", 8, w)

        self.__frameNumVar = StringVar()

        self.__frameNumEntry = Entry(self.__frame6_3,
                                   bg=self.__colors.getColor("boxBackNormal"),
                                   fg=self.__colors.getColor("boxFontNormal"),
                                   width=9999, justify=CENTER,
                                   textvariable=self.__frameNumVar,
                                   font=self.__smallFont
                                   )

        self.__frameNumEntry.pack_propagate(False)
        self.__frameNumEntry.pack(fill=X, side=TOP, anchor=N)

        try:
            self.__frameNumVar.set(
                str(
                    int(
                        "0b"+self.__data[8][:4],
                        2
                    )
                )
            )
        except:
            self.__frameNumVar.set("0")


        self.__frameNumEntry.bind("<KeyRelease>", self.__frameNumChanged)
        self.__frameNumEntry.bind("<FocusOut>", self.__frameNumChanged)


        self.__frame6B = Frame(self.__frame6, width=(self.__w // 7) * 2,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h)

        self.__frame6B.pack_propagate(False)
        self.__frame6B.pack(side=TOP, anchor=N, fill=BOTH)

        self.__picVarListScrollBar = Scrollbar(self.__frame6B)
        self.__picVarListBox = Listbox(self.__frame6B, width=100000,
                                        height=1000,
                                        yscrollcommand=self.__picVarListScrollBar.set,
                                        selectmode=BROWSE,
                                        exportselection=False,
                                        font=self.__smallFont,
                                        justify=LEFT
                                        )

        self.__picVarListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__picVarListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__picVarListBox.pack_propagate(False)

        self.__picVarListScrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__picVarListBox.pack(side=LEFT, anchor=W, fill=BOTH)

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

        for item in self.__byteVars:
            self.__picVarListBox.insert(END, item)

        if self.__data[8][0] == "%":
           self.__lastSetPic = 0
        else:
           for itemNum in range(0, len(self.__byteVars)):
               if self.__byteVars[itemNum].split("::")[1] == self.__data[8][0]:
                  self.__lastSetPic = itemNum
                  self.__picVarListBox.select_set(0, self.__lastSetPic)
                  break

        if self.__data[8][0] == "%":
            self.__picOption.set(1)
            self.__picVarListBox.config(state = DISABLED)
        else:
            self.__picOption.set(2)
            self.__mirroredButton.config(state=DISABLED)
            self.__frameNumEntry.config(state=DISABLED)
            self.__nusizFrame.changeState(DISABLED)

        self.__picVarListBox.bind("<ButtonRelease-1>", self.__changedPicVar)
        self.__picVarListBox.bind("<KeyRelease-Up>", self.__changedPicVar)
        self.__picVarListBox.bind("<KeyRelease-Down>", self.__changedPicVar)


    def __changedPicVar(self, event):
        if self.__lastSetPic != self.__picVarListBox.curselection()[0]:
            self.__lastSetPic = self.__picVarListBox.curselection()[0]
            self.__data[8]    = self.__data[8] = self.__byteVars[self.__lastSetPic].split("::")[1]
            self.__changeData(self.__data)

    def __mirroredChanged(self):
        if self.__picOption.get() == 1:
           self.__data[8] = self.__data[8][:5] + str(self.__mirrored.get()) +  self.__data[8][6:]
           self.__changeData(self.__data)

    def __frameNumChanged(self, event):
        if self.__picOption.get() == 1:
           try:
               num = int(self.__frameNumVar.get())
           except:
               self.__frameNumEntry.config(bg = self.__colors.getColor("boxBackUnSaved"),
                                           fg = self.__colors.getColor("boxFontUnSaved")
                                           )
           self.__frameNumEntry.config(bg = self.__colors.getColor("boxBackNormal"),
                                        fg = self.__colors.getColor("boxFontNormal")
                                        )

           if   num > 15:
                num = 15
           elif num < 0:
                num = 0

           self.__frameNumVar.set(str(num))
           d = bin(int(self.__frameNumVar.get())).replace("0b", "")
           while len(d) < 4:
               d = "0" + d

           if self.__data[8][1:5] != d:
              self.__data[8] = "%" + d + self.__data[8][5:]
              self.__changeData(self.__data)

    def XXX2(self):
        if self.__picOption.get() == 1:
           self.__lastSetPic = self.__picVarListBox.curselection()[0]
           self.__picVarListBox.select_clear(0, END)
           self.__picVarListBox.config(state = DISABLED)

           self.__mirroredButton.config(state = NORMAL)
           self.__frameNumEntry.config(state = NORMAL)
           self.__nusizFrame.changeState(NORMAL)

           d1 = bin(int(self.__nusizFrame.getValue())).replace("0b", "")
           d2 = bin(int(self.__mirrored.get())).replace("0b", "")
           d3 = bin(int(self.__frameNumVar.get())).replace("0b", "")

           while len(d1) < 4:
              d1 = "0" + d1

           while len(d3) < 3:
              d3 = "0" + d3

           self.__data[8] = "%" + d1 + d2 + d3

        else:
           self.__mirroredButton.config(state=DISABLED)
           self.__frameNumEntry.config(state=DISABLED)
           self.__nusizFrame.changeState(DISABLED)

           self.__picVarListBox.config(state = NORMAL)
           self.__picVarListBox.select_set(self.__lastSetPic)

           self.__data[8] = self.__byteVars[self.__lastSetPic].split("::")[1]

        self.__changeData(self.__data)


    def __changedPicture(self, event):
        if self.__listOfPictures[self.__picVarListBox.curselection()[0]] != self.__data[7]:
           self.__data[7] =  self.__listOfPictures[self.__picVarListBox.curselection()[0]]
           self.__changeData(self.__data)

    def __chamgeConst(self, event):
        if self.__constEntry.getValue() != self.__data[5]:
            temp = self.__constEntry.getValue()
            if self.isItHex(temp) == True:
                temp = temp[:2] + "0"
                self.__data[5] = temp
                self.__constEntry.setValue(temp)
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

    def XXX(self):
        if self.__colorOption.get() == 1:
            try:
                self.__lastSet = self.__colorVars[self.__colorVarListBox.curselection()[0]]
            except:
                self.__lastSet = self.__colorVars[0]
            self.__colorVarListBox.select_clear(0, END)
            self.__constEntry.setValue(self.__lastConst)
            self.__colorVarListBox.config(state=DISABLED)
            self.__constEntry.changeState(NORMAL)
            self.__chamgeConst(None)
        else:
            self.__lastConst = self.__constEntry.getValue()
            self.__constEntry.changeState(DISABLED)
            self.__colorVarListBox.config(state=NORMAL)
            for itemNum in range(0, len(self.__colorVars)):
                if self.__colorVars[itemNum] == self.__lastSet:
                    self.__colorVarListBox.select_set(itemNum)
                    break

            self.__changedColorVar(None)

    def __changedDataVar(self, event):
        if self.__data[3] != self.__dataVars[self.__dataVarListBox.curselection()[0]].split("::")[1]:
            self.__data[3] = self.__dataVars[self.__dataVarListBox.curselection()[0]].split("::")[1]
            self.__changeData(self.__data)

    def __changedColorVar(self, event):
        if self.__data[5] != self.__colorVars[self.__colorVarListBox.curselection()[0]].split("::")[1]:
            self.__data[5] = self.__colorVars[self.__colorVarListBox.curselection()[0]].split("::")[1]
            self.__changeData(self.__data)

    def __changeMaxEntry(self, event):
        if self.isItNum(self.__maxVar.get()) == False:
            self.__maxVarEntry.config(
                bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                fg=self.__loader.colorPalettes.getColor("boxFontUnSaved")
            )
        else:
            self.__maxVarEntry.config(
                bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                fg=self.__loader.colorPalettes.getColor("boxFontNormal")
            )
            if self.__maxVar.get() != self.__data[4]:
                temp = self.__maxVar.get()
                if int(temp) > 255:
                    temp = "255"
                elif int(temp) < 1:
                    temp = "1"
                self.__maxVar.set(temp)
                self.__data[4] = self.__maxVar.get()
                self.__changeData(self.__data)

