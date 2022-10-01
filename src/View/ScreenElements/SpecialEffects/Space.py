from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from time import sleep
import re

class Space:
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

        self.__byteVars = []
        self.__iterVars = []

        for address in self.__loader.virtualMemory.memory.keys():
            for variable in self.__loader.virtualMemory.memory[address].variables.keys():
                var = self.__loader.virtualMemory.memory[address].variables[variable]
                if ((var.validity == "global" or
                     var.validity == self.__currentBank) and
                        (var.system == False or
                         var.iterable == True or
                         var.linkable == True) and
                        var.type == "byte"
                ):
                    self.__byteVars.append(address + "::" + variable)

                if ((var.type == "byte") and
                        (var.validity == "global" or
                         var.validity == self.__currentBank) and
                        (var.system == False or
                         var.iterable == True)
                ):
                    self.__iterVars.append(address + "::" + variable)

        self.__frame1 = Frame(self.__uniqueFrame, width=self.__w // 2,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  height=self.__h)

        self.__frame1.pack_propagate(False)
        self.__frame1.pack(side=LEFT, anchor=E, fill=Y)

        self.__frame2 = Frame(self.__uniqueFrame, width=self.__w // 2,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  height=self.__h)

        self.__frame2.pack_propagate(False)
        self.__frame2.pack(side=LEFT, anchor=E, fill=Y)

        self.__label1 = Label(self.__frame1,
                  text=self.__dictionaries.getWordFromCurrentLanguage("xPoz") + ":",
                  font=self.__smallFont, fg=self.__colors.getColor("font"),
                  bg=self.__colors.getColor("window"), justify=CENTER
                  )

        self.__label1.pack_propagate(False)
        self.__label1.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__label2 = Label(self.__frame2,
                  text=self.__dictionaries.getWordFromCurrentLanguage("colorVar") + ":",
                  font=self.__smallFont, fg=self.__colors.getColor("font"),
                  bg=self.__colors.getColor("window"), justify=CENTER
                  )

        self.__label2.pack_propagate(False)
        self.__label2.pack(side=TOP, anchor=CENTER, fill=BOTH)

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

        self.__constOrVar = IntVar()
        self.__constButton = Radiobutton(self.__frame2, width=99999,
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

        self.__directionLabel = Label(self.__frame2,
                  text=self.__dictionaries.getWordFromCurrentLanguage("direction") + ":",
                  font=self.__smallFont, fg=self.__colors.getColor("font"),
                  bg=self.__colors.getColor("window"), justify=LEFT
                  )

        self.__directionLabel.pack_propagate(False)
        self.__directionLabel.pack(side=TOP, anchor=N, fill=X)

        self.__frameLeftRight = Frame(self.__frame2, width=self.__w // 2,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  height=self.__h//12)

        self.__frameLeftRight.pack_propagate(False)
        self.__frameLeftRight.pack(side=TOP, anchor=N, fill=X)

        self.__leftOrRight = IntVar()
        self.__leftButton = Radiobutton(self.__frameLeftRight, width=4,
                                         text="<<",
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__bigFont,
                                         variable=self.__leftOrRight,
                                         activebackground=self.__colors.getColor("highLight"),
                                         value=1, command=self.__changeDirection
                                         )

        self.__leftButton.pack_propagate(False)

        self.__rightButton = Radiobutton(self.__frameLeftRight, width=4,
                                         text=">>",
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__bigFont,
                                         variable=self.__leftOrRight,
                                         activebackground=self.__colors.getColor("highLight"),
                                         value=2, command=self.__changeDirection
                                         )

        self.__rightButton.pack_propagate(False)
        self.__leftButton.pack(fill=Y, side=LEFT, anchor=E)
        self.__rightButton.pack(fill=Y, side=RIGHT, anchor=W)

        self.__speedLabel = Label(self.__frame2,
                  text=self.__dictionaries.getWordFromCurrentLanguage("speed"),
                  font=self.__smallFont, fg=self.__colors.getColor("font"),
                  bg=self.__colors.getColor("window"), justify=LEFT
                  )

        self.__speedLabel.pack_propagate(False)
        self.__speedLabel.pack(side=TOP, anchor=N, fill=X)

        self.__speedConstVal = StringVar()

        self.__speedConst = Entry(self.__frame2,
                              bg=self.__colors.getColor("boxBackNormal"),
                              fg=self.__colors.getColor("boxFontNormal"),
                              width=9999, justify=CENTER,
                              textvariable=self.__speedConstVal,
                              font=self.__smallFont
                              )

        self.__speedConst.pack_propagate(False)
        self.__speedConst.pack(fill=Y, side=TOP, anchor=N)

        self.__lineLabel = Label(self.__frame2,
                  text=self.__dictionaries.getWordFromCurrentLanguage("numOfLines"),
                  font=self.__smallFont, fg=self.__colors.getColor("font"),
                  bg=self.__colors.getColor("window"), justify=LEFT
                  )

        self.__lineLabel.pack_propagate(False)
        self.__lineLabel.pack(side=TOP, anchor=N, fill=X)

        self.__lineConstVar = StringVar()

        self.__lineConst = Entry(self.__frame2,
                              bg=self.__colors.getColor("boxBackNormal"),
                              fg=self.__colors.getColor("boxFontNormal"),
                              width=9999, justify=CENTER,
                              textvariable=self.__lineConstVar,
                              font=self.__smallFont
                              )

        self.__lineConst.pack_propagate(False)
        self.__lineConst.pack(fill=Y, side=TOP, anchor=N)

        self.__varButton = Radiobutton(self.__frame2, width=99999,
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

        for item in self.__iterVars:
            self.__listBox1.insert(END, item)

        for item in self.__byteVars:
            self.__listBox2.insert(END, item)

        selector = 0
        for itemNum in range(0, len(self.__iterVars)):
            if self.__data[3] == self.__iterVars[itemNum].split("::")[1]:
               selector = itemNum
               break

        self.__lastSelecteds = []
        self.__lastSelecteds.append(self.__iterVars[selector].split("::")[1])
        self.__listBox1.select_set(selector)
        self.__data[3] = self.__lastSelecteds[-1]

        self.__dirAndPower = {
            "000": [1, 3],
            "001": [1, 2],
            "010": [1, 1],
            "011": [1, 0],
            "100": [2, 1],
            "101": [2, 2],
            "110": [2, 3],
            "111": [2, 3]
        }

        selector = 0
        if self.isItBin(self.__data[4]):
           self.__listBox2.config(state = DISABLED)
           self.__leftButton.config(state = NORMAL)
           self.__rightButton.config(state = NORMAL)
           self.__speedConst.config(state = NORMAL)
           self.__lineConst.config(state = NORMAL)

           lines = self.__data[4][1:6]
           dir   = self.__dirAndPower[self.__data[4][6:]]

           self.__lineConstVar.set(str(int("0b"+lines, 2)))
           self.__leftOrRight.set(dir[0])
           self.__speedConstVal.set(str(dir[1]))

           self.__lastSelecteds.append(self.__byteVars[0].split("::")[1])
           self.__listBox2.select_set(0)

           self.__constOrVar.set(1)

        else:
           self.__listBox2.config(state=NORMAL)
           self.__leftButton.config(state=DISABLED)
           self.__rightButton.config(state=DISABLED)
           self.__speedConst.config(state=DISABLED)
           self.__lineConst.config(state=DISABLED)

           for itemNum in range(0, len(self.__byteVars)):
               if self.__byteVars[itemNum].split("::")[1] == self.__data[4]:
                  selector = itemNum
                  break

           self.__lastSelecteds.append(self.__byteVars[selector].split("::")[1])
           self.__data[4] = self.__lastSelecteds[-1]
           self.__listBox2.select_set(selector)

           self.__leftOrRight.set(1)
           self.__lineConstVar.set("15")
           self.__speedConstVal.set("2")

           self.__constOrVar.set(2)

        self.__listBox1.bind("<ButtonRelease-1>", self.__changeSelected)
        self.__listBox1.bind("<KeyRelease-Up>", self.__changeSelected)
        self.__listBox1.bind("<KeyRelease-Down>", self.__changeSelected)
        self.__listBox2.bind("<ButtonRelease-1>", self.__changeSelected)
        self.__listBox2.bind("<KeyRelease-Up>", self.__changeSelected)
        self.__listBox2.bind("<KeyRelease-Down>", self.__changeSelected)
        self.__speedConst.bind("<KeyRelease>", self.__changeEntry)
        self.__speedConst.bind("<FocusOut>", self.__changeEntry)
        self.__lineConst.bind("<KeyRelease>", self.__changeEntry)
        self.__lineConst.bind("<FocusOut>", self.__changeEntry)

    def __changeEntry(self, event):
        if self.__constOrVar.get() == 2: return

        values = {
            self.__lineConst : self.__lineConstVar,
            self.__speedConst: self.__speedConstVal
                }

        maximum = {
            self.__lineConst : 32,
            self.__speedConst: 7
                }

        minimum = {
            self.__lineConst : 1,
            self.__speedConst: 0
                }

        val = values[event.widget].get()
        if self.isItNum(val) == False:
            event.widget.config(
                bg=self.__colors.getColor("boxBackUnSaved"),
                fg=self.__colors.getColor("boxFontUnSaved")
            )
            return
        else:
            event.widget.config(
                bg=self.__colors.getColor("boxBackNormal"),
                fg=self.__colors.getColor("boxFontNormal")
            )

        val = int(val)
        if val < minimum[event.widget]: val = minimum[event.widget]
        if val > maximum[event.widget]: val = maximum[event.widget]

        values[event.widget].set(val)
        try:
            self.__changeDirection()
        except:
            pass

    def __changeSelected(self, event):
        nums = {
            self.__listBox1: 0,
            self.__listBox2: 1
        }

        self.__lists = [self.__iterVars, self.__byteVars]
        num = nums[event.widget]

        if num == 1 and self.__constOrVar.get() == 1:
           return

        if self.__lastSelecteds[num] != self.__lists[num][event.widget.curselection()[0]].split("::")[1]:
           self.__lastSelecteds[num] =  self.__lists[num][event.widget.curselection()[0]].split("::")[1]
           self.__data[3 + num]      =  self.__lastSelecteds[num]
           self.__changeData(self.__data)

    def __changeIfConstOrVar(self):
        if self.__constOrVar.get() == 1:
            self.__listBox2.config(state=DISABLED)
            self.__leftButton.config(state=NORMAL)
            self.__rightButton.config(state=NORMAL)
            self.__speedConst.config(state=NORMAL)
            self.__lineConst.config(state=NORMAL)

            try:
                self.__changeDirection()
            except:
                pass

        else:
            self.__listBox2.config(state=NORMAL)
            self.__leftButton.config(state=DISABLED)
            self.__rightButton.config(state=DISABLED)
            self.__speedConst.config(state=DISABLED)
            self.__lineConst.config(state=DISABLED)

            selector = 0
            for itemNum in range(0, len(self.__byteVars)):
                if self.__byteVars[itemNum].split("::")[1] == self.__lastSelecteds[1]:
                    selector = itemNum
                    break

            self.__data[4] = self.__lastSelecteds[1]
            self.__listBox2.select_set(selector)
            self.__changeData(self.__data)

    def __changeDirection(self):
        data = [self.__leftOrRight.get(), int(self.__speedConstVal.get())]
        if self.__speedConstVal.get() == "0":
           data[0] = 1

        lastPart = "000"
        for key in self.__dirAndPower.keys():
            if self.__dirAndPower[key] == data:
               lastPart = key
               break

        firstPart = bin(int(self.__lineConstVar.get())-1).replace("0b", "")
        while len(firstPart) < 5:
            firstPart = "0" + firstPart

        self.__data[4] = "%" + firstPart + lastPart
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