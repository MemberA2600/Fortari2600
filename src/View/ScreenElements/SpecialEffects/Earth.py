from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from time import sleep
import re

class Earth:
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
        if "#" in data:
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

        numOf = 3
        self.__framesAndLabels = []
        self.__labels    = ["dataVar", "colorVar", "gradient"]
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

            if num in (0, 1):
               if num  == 1:
                   self.__constOrVar = IntVar()
                   self.__constButton2 = Radiobutton(f, width=99999,
                                                     text=self.__dictionaries.getWordFromCurrentLanguage("constant"),
                                                     bg=self.__colors.getColor("window"),
                                                     fg=self.__colors.getColor("font"),
                                                     justify=LEFT, font=self.__smallFont,
                                                     variable=self.__constOrVar,
                                                     activebackground=self.__colors.getColor("highLight"),
                                                     activeforeground=self.__loader.colorPalettes.getColor("font"),
                                                     value=1, command=self.__changeIfConstOrVar
                                                     )

                   self.__constButton2.pack_propagate(False)
                   self.__constButton2.pack(fill=X, side=TOP, anchor=N)

                   self.__staticColors = ["$D8"]

                   self.__hexEntry1 = HexEntry(self.__loader, f, self.__colors, self.__colorDict,
                                               self.__normalFont, self.__staticColors, 0, None, self.__changeHex)

                   self.__varButton = Radiobutton(f, width=99999,
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

               self.__listBoxes.append({})
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
               s.config(command=l.yview)

               lists = [self.__containers, self.__colorVars]

               for item in lists[num]:
                   l.insert(END, item)

               self.__listBoxes[-1]["listBox"] = l
               self.__listBoxes[-1]["selected"] = ""
               self.__listBoxes[-1]["scrollBar"] = s
               self.__listBoxes[-1]["dataList"] = lists[num]

               l.bind("<ButtonRelease-1>", self.__changeSelected)
               l.bind("<KeyRelease-Up>", self.__changeSelected)
               l.bind("<KeyRelease-Down>", self.__changeSelected)
        else:

            numberOfHexes = 56
            self.__hexEntries = []
            self.__hexValues = []

            rows  = 4
            lines = numberOfHexes // rows

            for y in range(0, lines ):
                f1 = Frame(f, width=self.__w,
                          bg=self.__loader.colorPalettes.getColor("window"),
                          height=self.__h // lines // 1.5)

                f1.pack_propagate(False)
                f1.pack(side=TOP, anchor=N, fill=X)

                for x in range(0, rows):
                    f2 = Frame(f1, width=self.__w // rows // 3,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h)

                    f2.pack_propagate(False)
                    f2.pack(side=LEFT, anchor=E, fill=Y)

                    self.__hexValues.append("$00")
                    self.__hexEntries.append(HexEntry(self.__loader, f2, self.__colors, self.__colorDict,
                                                      self.__smallFont, self.__hexValues, -1, None, self.__changeHex))


        if self.__data[3] == "#":
           self.__data[3] = self.__listBoxes[0]["dataList"][0].split("::")[1]

        selector = 0
        for itemNum in range(0, len(self.__listBoxes[0]["dataList"])):
            if self.__data[3] == self.__listBoxes[0]["dataList"][itemNum].split("::")[1]:
               selector = itemNum
               break

        self.__listBoxes[0]["listBox"].select_set(selector)
        self.__listBoxes[0]["listBox"].yview(selector)

        self.__listBoxes[0]["selected"] = self.__listBoxes[0]["dataList"][selector].split("::")[1]

        if self.isItHex(self.__data[4]) == True:
           self.__constOrVar.set(1)
           self.__listBoxes[1]["listBox"].config(state = DISABLED)
           self.__staticColors[0] = self.__data[4]
           self.__hexEntry1.setValue(self.__data[4])

           self.__listBoxes[1]["selected"] = self.__listBoxes[1]["dataList"][0].split("::")[1]

        else:
           self.__constOrVar.set(2)
           self.__hexEntry1.changeState(DISABLED)

           selector = 0
           for itemNum in range(0, len(self.__listBoxes[1]["dataList"])):
               if self.__data[4] == self.__listBoxes[1]["dataList"][itemNum].split("::")[1]:
                   selector = itemNum
                   break

           self.__listBoxes[1]["listBox"].select_set(selector)
           self.__listBoxes[1]["listBox"].yview(selector)

           self.__listBoxes[1]["selected"] = self.__listBoxes[1]["dataList"][selector].split("::")[1]

        data = []
        if self.__data[5] == "#":
            data = self.__loader.io.loadSubModule("Earth_BG_Colors").replace("\r", "").replace(" ", "").replace("\t", "").split("\n")
            self.__data[5] = "|".join(data)
        else:
            data = self.__data[5].split("|")

        for itemNum in range(0, len(data)):
            self.__hexValues[itemNum]  = data[itemNum]
            self.__hexEntries[itemNum].setValue(data[itemNum])

    def __changeSelected(self, event):
        selectNum = 0
        if event.widget == self.__listBoxes[0]["listBox"]:
           selectNum = 0
        else:
           selectNum = 1

        if selectNum == 1 and self.__constOrVar.get() == 1: return

        if self.__listBoxes[selectNum]["selected"] != self.__listBoxes[selectNum]["dataList"][
           self.__listBoxes[selectNum]["listBox"].curselection()[0]
                                      ].split("::")[1]:
            self.__listBoxes[selectNum]["selected"] = self.__listBoxes[selectNum]["dataList"][
            self.__listBoxes[selectNum]["listBox"].curselection()[0]
            ].split("::")[1]

            self.__data[selectNum + 3] = self.__listBoxes[selectNum]["selected"]
            self.__changeData(self.__data)

    def __changeHex(self, event):
        if event.widget == self.__hexEntry1 and self.__constOrVar.get() == 2: return

        if event.widget == self.__hexEntry1.getEntry():
           if self.isItHex(self.__hexEntry1.getValue()):
              self.__data[4] = self.__hexEntry1.getValue()

        else:
            selectNum = 0
            for itemNum in range(0, len(self.__hexEntries)):
                if event.widget == self.__hexEntries[itemNum].getEntry():
                   selectNum = itemNum
                   break

            hexEntry = self.__hexEntries[selectNum]
            if self.isItHex(hexEntry.getValue()):
               data = self.__data[5].split("|")
               data[selectNum] = hexEntry.getValue()
               self.__data[5] = "|".join(data)
        self.__changeData(self.__data)

    def __changeIfConstOrVar(self):
        if self.__constOrVar.get() == 1:
           self.__hexEntry1.changeState(state = NORMAL)
           self.__listBoxes[1]["listBox"].config(state = DISABLED)

           if self.isItHex(self.__hexEntry1.getValue()):
              self.__data[4] = self.__hexEntry1.getValue()
        else:
            self.__hexEntry1.changeState(state=DISABLED)
            self.__listBoxes[1]["listBox"].config(state=NORMAL)

            self.__listBoxes[1]["listBox"].select_clear(0, END)
            selector = 0

            for itemNum in range(0, len(self.__listBoxes[1]["dataList"])):
                if self.__listBoxes[1]["selected"] == self.__listBoxes[1]["dataList"][itemNum].split("::")[1]:
                   selector = itemNum
                   break

            self.__listBoxes[1]["listBox"].select_set(selector)
            self.__listBoxes[1]["listBox"].yview(selector)

            self.__data[4] = self.__listBoxes[1]["selected"]

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