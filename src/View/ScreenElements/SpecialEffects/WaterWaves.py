from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from time import sleep
import re

class WaterWaves:
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

        self.__frame1 = Frame(self.__uniqueFrame, width=self.__w // 3,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  height=self.__h)

        self.__frame1.pack_propagate(False)
        self.__frame1.pack(side=LEFT, anchor=E, fill=Y)

        self.__frame2 = Frame(self.__uniqueFrame, width=self.__w // 3,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  height=self.__h)

        self.__frame2.pack_propagate(False)
        self.__frame2.pack(side=LEFT, anchor=E, fill=Y)

        self.__frame3 = Frame(self.__uniqueFrame, width=self.__w // 3,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  height=self.__h)

        self.__frame3.pack_propagate(False)
        self.__frame3.pack(side=LEFT, anchor=E, fill=Y)

        self.__label1 = Label(self.__frame1,
                  text=self.__dictionaries.getWordFromCurrentLanguage("dataVar") + ":",
                  font=self.__smallFont, fg=self.__colors.getColor("font"),
                  bg=self.__colors.getColor("window"), justify=CENTER
                  )

        self.__label1.pack_propagate(False)
        self.__label1.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__label2 = Label(self.__frame2,
                  text=self.__dictionaries.getWordFromCurrentLanguage("baseColor") + ":",
                  font=self.__smallFont, fg=self.__colors.getColor("font"),
                  bg=self.__colors.getColor("window"), justify=CENTER
                  )

        self.__label2.pack_propagate(False)
        self.__label2.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__label3 = Label(self.__frame3,
                  text=self.__dictionaries.getWordFromCurrentLanguage("gradient") + ":",
                  font=self.__smallFont, fg=self.__colors.getColor("font"),
                  bg=self.__colors.getColor("window"), justify=CENTER
                  )

        self.__label3.pack_propagate(False)
        self.__label3.pack(side=TOP, anchor=CENTER, fill=BOTH)

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

        for item in self.__dataVars:
            self.__listBox1.insert(END, item)


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

        from HexEntry import HexEntry
        self.__c = ["$00"]
        self.__hexEntry = HexEntry(self.__loader, self.__frame2, self.__colors, self.__colorDict,
                             self.__normalFont, self.__c, 0, None, self.__changeHex)

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

        for item in self.__colorVars:
            self.__listBox2.insert(END, item)

        selector = 0
        for itemNum in range(0, len(self.__dataVars)):
           if self.__data[3] == self.__dataVars[itemNum].split("::")[1]:
              selector = itemNum
              break

        self.__lastSelecteds = []

        self.__lastSelecteds.append(self.__dataVars[selector].split("::")[1])
        self.__data[3] = self.__lastSelecteds[0]

        self.__listBox1.select_set(selector)

        if self.isItHex(self.__data[4]):
           self.__constOrVar.set(1)
           self.__hexEntry.changeState(NORMAL)
           self.__listBox2.config(state = DISABLED)

           self.__hexEntry.setValue(self.__data[4])
           self.__lastSelecteds.append(self.__colorVars[0].split("::")[1])

        else:
           self.__constOrVar.set(2)
           self.__hexEntry.changeState(DISABLED)
           self.__listBox2.config(state=NORMAL)

           selector = 0
           for itemNum in range(0, len(self.__colorVars)):
               if self.__colorVars[itemNum].split("::")[1] == self.__data[4]:
                  selector = itemNum
                  break

           self.__lastSelecteds.append(self.__colorVars[selector].split("::")[1])
           self.__data[4] = self.__lastSelecteds[1]
           self.__listBox2.select_set(selector)

        self.__listBox1.bind("<ButtonRelease-1>", self.__changeSelected)
        self.__listBox1.bind("<KeyRelease-Up>", self.__changeSelected)
        self.__listBox1.bind("<KeyRelease-Down>", self.__changeSelected)
        self.__listBox2.bind("<ButtonRelease-1>", self.__changeSelected)
        self.__listBox2.bind("<KeyRelease-Up>", self.__changeSelected)
        self.__listBox2.bind("<KeyRelease-Down>", self.__changeSelected)

        self.__hexValues  = []
        self.__hexEntries = []

        nums = self.__data[5].split("|")

        for num in range(0, 6):
            self.__hexValues.append(nums[num])
            hexEntry = HexEntry(self.__loader, self.__frame3, self.__colors, self.__colorDict,
                             self.__normalFont, self.__hexValues, num, None,  self.__changeHex)
            self.__hexEntries.append(hexEntry)

    def __changeSelected(self, event):
        if event.widget == self.__listBox2 and self.__constOrVar.get() == 1: return

        lists = {
            self.__listBox1: self.__dataVars,
            self.__listBox2: self.__colorVars
        }
        lasts = {
            self.__listBox1: 0,
            self.__listBox2: 1
        }
        dataNum = {
            self.__listBox1: 3,
            self.__listBox2: 4
        }

        if self.__lastSelecteds[lasts[event.widget]] != lists[event.widget][event.widget.curselection()[0]].split("::")[1]:
           self.__lastSelecteds[lasts[event.widget]] = lists[event.widget][event.widget.curselection()[0]].split("::")[1]
           self.__data[dataNum[event.widget]] = self.__lastSelecteds[lasts[event.widget]]
           self.__changeData(self.__data)

    def __changeHex(self, event):

        theHex = self.__hexEntry
        for num in range(0, len(self.__hexEntries)):
            if event.widget == self.__hexEntries[num].getEntry():
               theHex = self.__hexEntries[num]

        if theHex not in self.__hexEntries and self.__constOrVar.get() == 2: return

        if self.isItHex(theHex.getValue()):
           if theHex not in self.__hexEntries:
              self.__data[4] = self.__hexEntry.getValue()
           else:
              numOfHex = self.__hexEntries.index(theHex)
              val      = theHex.getValue()

              fuckIt = self.__data[5].split("|")
              fuckIt[numOfHex] = "$0" + val[2]
              theHex.setValue(fuckIt[numOfHex])
              self.__data[5] = "|".join(fuckIt)

           self.__changeData(self.__data)

    def __changeIfConstOrVar(self):
        if self.__constOrVar.get() == 1:
           self.__hexEntry.changeState(NORMAL)
           self.__listBox2.config(state = DISABLED)

           self.__data[4] = self.__hexEntry.getValue()
        else:
           self.__hexEntry.changeState(DISABLED)
           self.__listBox2.config(state=NORMAL)

           self.__listBox2.select_clear(0, END)
           selector = 0
           for itemNum in range(0, len(self.__colorVars)):
               if self.__colorVars[itemNum].split("::")[1] == self.__data[4]:
                  selector = itemNum
                  break

           self.__listBox2.select_set(selector)
           self.__lastSelecteds[1] = self.__colorVars[selector].split("::")[1]
           self.__data[4]          = self.__lastSelecteds[1]

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