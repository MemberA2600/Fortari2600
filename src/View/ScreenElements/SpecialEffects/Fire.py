from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from time import sleep
import re

class Fire:
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

        # self.__nibbleVars = []
        self.__byteVars   = []

        for address in self.__loader.virtualMemory.memory.keys():
            for variable in self.__loader.virtualMemory.memory[address].variables.keys():
                var = self.__loader.virtualMemory.memory[address].variables[variable]
                if ((var.type == "byte" or var.type == "nibble") and
                        (var.validity == "global" or
                         var.validity == self.__currentBank) and
                        (var.system == False or
                         var.iterable == True )

                ):
                  #  self.__nibbleVars.append(address + "::" + variable)
                    if var.type == "byte": self.__byteVars.append(address + "::" + variable)


        self.__dataFrame = Frame(self.__uniqueFrame, width=self.__w // 5,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__h)

        self.__dataFrame.pack_propagate(False)
        self.__dataFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__constantsFrame = Frame(self.__uniqueFrame, width=self.__w // 5,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__h)

        self.__constantsFrame.pack_propagate(False)
        self.__constantsFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__colorsMainFrame = Frame(self.__uniqueFrame, width=self.__w // 5 * 3,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__h)

        self.__colorsMainFrame.pack_propagate(False)
        self.__colorsMainFrame.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__firstLabel = Label(self.__dataFrame,
                      text=self.__dictionaries.getWordFromCurrentLanguage("dataVar") + ":",
                      font=self.__smallFont, fg=self.__colors.getColor("font"),
                      bg=self.__colors.getColor("window"), justify=CENTER
                      )

        self.__firstLabel.pack_propagate(False)
        self.__firstLabel.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__dataVar = StringVar()
        self.__scrollBar = Scrollbar(self.__dataFrame)

        self.__listBox = Listbox(self.__dataFrame, width=100000,
                                                   height=1000,
                                                   yscrollcommand=self.__scrollBar.set,
                                                   selectmode=BROWSE,
                                                   exportselection=False,
                                                   font=self.__smallFont,
                                                   justify=LEFT
                                                   )
        self.__listBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__listBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__listBox.pack_propagate(False)

        self.__listBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__listBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__listBox.pack_propagate(False)

        self.__scrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__listBox.pack(side=LEFT, anchor=W, fill=BOTH)
        self.__scrollBar.config(command=self.__listBox.yview)

        self.__listBox.bind("<ButtonRelease-1>", self.__clickedListBox)
        self.__listBox.bind("<KeyRelease-Up>", self.__clickedListBox)
        self.__listBox.bind("<KeyRelease-Down>", self.__clickedListBox)

        for item in self.__byteVars:
            self.__listBox.insert(END, item)

        self.__secondLabel = Label(self.__constantsFrame,
                      text=self.__dictionaries.getWordFromCurrentLanguage("speed"),
                      font=self.__smallFont, fg=self.__colors.getColor("font"),
                      bg=self.__colors.getColor("window"), justify=CENTER
                      )

        self.__secondLabel.pack_propagate(False)
        self.__secondLabel.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__speedVar = StringVar()
        self.__speedEntry = Entry(self.__constantsFrame,
                                        name = "speed",
                                        bg=self.__colors.getColor("boxBackNormal"),
                                        fg=self.__colors.getColor("boxFontNormal"),
                                        width=9999, justify = CENTER,
                                        textvariable=self.__speedVar,
                                        font=self.__normalFont
                                        )

        self.__speedEntry.pack_propagate(False)
        self.__speedEntry.pack(fill=X, side = TOP, anchor = N)

        self.__speedEntry.bind("<FocusOut>", self.__chamgeConst)
        self.__speedEntry.bind("<KeyRelease>", self.__chamgeConst)

        self.__particles = IntVar()
        self.__checkBox = Checkbutton(self.__constantsFrame,
                                     text=self.__dictionaries.getWordFromCurrentLanguage("particles"),
                                     bg=self.__colors.getColor("window"),
                                     fg=self.__colors.getColor("font"),
                                     justify=LEFT, font=self.__normalFont,
                                     variable=self.__particles,
                                     activebackground=self.__colors.getColor("highLight"),
                                     command=self.saveHeight
                                     )

        self.__checkBox.pack_propagate(False)
        self.__checkBox.pack(fill=BOTH, side=TOP, anchor=CENTER)

        self.__thirdLabel = Label(self.__constantsFrame,
                      text=self.__dictionaries.getWordFromCurrentLanguage("height"),
                      font=self.__smallFont, fg=self.__colors.getColor("font"),
                      bg=self.__colors.getColor("window"), justify=CENTER
                      )

        self.__thirdLabel.pack_propagate(False)
        self.__thirdLabel.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__heightVar = StringVar()
        self.__heightEntry = Entry(self.__constantsFrame,
                                        name="height",
                                        bg=self.__colors.getColor("boxBackNormal"),
                                        fg=self.__colors.getColor("boxFontNormal"),
                                        width=9999, justify = CENTER,
                                        textvariable=self.__heightVar,
                                        font=self.__normalFont
                                        )

        self.__heightEntry.pack_propagate(False)
        self.__heightEntry.pack(fill=X, side = TOP, anchor = N)

        self.__heightEntry.bind("<FocusOut>", self.__chamgeConst)
        self.__heightEntry.bind("<KeyRelease>", self.__chamgeConst)

        selector = 0
        for itemNum in range(0, len(self.__byteVars)):
            if self.__byteVars[itemNum].split("::")[1] == self.__data[3]:
               selector = itemNum
               break

        self.__listBox.select_set(selector)
        self.__listBox.yview(selector)

        if self.__data[3] == "#": self.__data[3] = self.__byteVars[0].split("::")[1]


        if self.isItNum(self.__data[4]):
           self.__speedVar.set(self.__data[4])
        else:
           self.__speedVar.set("2")

        if self.isItNum(self.__data[5]):
            self.__heightVar.set(self.__data[5])
        else:
            self.__heightVar.set("6")
            self.__data[5] = "6"

        if self.__data[5] == "0":
           self.__particles.set(0)
           self.__heightEntry.config(state = DISABLED)
           self.__heightVar.set("1")
        else:
            self.__particles.set(1)
            self.__heightEntry.config(state=NORMAL)
            self.__heightVar.set(self.__data[5])

        self.__lastSelected = self.__data[3]

        self.__fourthLabel = Label(self.__colorsMainFrame,
                      text=self.__dictionaries.getWordFromCurrentLanguage("gradient")+":",
                      font=self.__smallFont, fg=self.__colors.getColor("font"),
                      bg=self.__colors.getColor("window"), justify=CENTER
                      )

        self.__fourthLabel.pack_propagate(False)
        self.__fourthLabel.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__colorsFrame = Frame(self.__colorsMainFrame, width=self.__w // 5 * 3,
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       height=self.__h)

        self.__colorsFrame.pack_propagate(False)
        self.__colorsFrame.pack(side=TOP, anchor=N, fill=BOTH)

        self.__colorFrameList = []

        self.__fuckinColors = self.__data[6].split("|")
        for num in range(0, 2):

            self.__colorFrameList.append({})

            colorFrame = Frame(self.__colorsFrame, width=self.__w // 10 * 3,
                                           bg=self.__loader.colorPalettes.getColor("window"),
                                           height=self.__h)
    
            colorFrame.pack_propagate(False)
            colorFrame.pack(side=LEFT, anchor=E, fill=Y)
            self.__colorFrameList[-1]["frame"] = colorFrame

            self.__colorFrameList[-1]["hexEntries"] = []

            for num2 in range(0,16):
                from HexEntry import HexEntry

                hexEntry = HexEntry(self.__loader, colorFrame, self.__colors, self.__colorDict,
                                    self.__smallFont, self.__fuckinColors, (num*8) + num2, None,
                                    self.__changeGradientColorVar)
                self.__colorFrameList[-1]["hexEntries"].append(hexEntry)

    def __changeGradientColorVar(self, event):
        poz = [0,0]

        for num in range(0,2):
            for num2 in range(0,16):
                if event.widget == self.__colorFrameList[num]["hexEntries"][num2].getEntry():
                   poz = [num, num2]
                   break

        if self.isItHex(self.__colorFrameList[poz[0]]["hexEntries"][poz[1]].getValue()) == True:
           temp = []
           wasError = False
           for num in range(0, 2):
               for num2 in range(0, 16):
                   if self.isItHex(self.__colorFrameList[num]["hexEntries"][num2].getValue()):
                      temp.append(self.__colorFrameList[num]["hexEntries"][num2].getValue())
                   else:
                       wasError = True
                       break
               if wasError: break

           if wasError == False:
              self.__data[6] = "|".join(temp)
              self.__changeData(self.__data)

    def __clickedListBox(self, event):
        if self.__lastSelected != self.__byteVars[self.__listBox.curselection()[0]].split("::")[1]:
           self.__lastSelected = self.__byteVars[self.__listBox.curselection()[0]].split("::")[1]
           self.__data[3]      = self.__lastSelected
           self.__changeData(self.__data)

    def __chamgeConst(self, event):
        if event.widget.cget("state") == DISABLED: return
        values = {"height": self.__heightVar, "speed": self.__speedVar}
        valids = {"height": [1, 12], "speed": [0, 7]}

        name = str(event.widget).split(".")[-1]
        if self.isItNum(values[name].get()) == False:
           event.widget.config(
               bg=self.__colors.getColor("boxBackUnSaved"),
               fg=self.__colors.getColor("boxFontUnSaved")
           )
        else:
            event.widget.config(
                bg=self.__colors.getColor("boxBackNormal"),
                fg=self.__colors.getColor("boxFontNormal")
            )

            num = int(values[name].get())
            if num < valids[name][0]: num = valids[name][0]
            if num > valids[name][1]: num = valids[name][1]

            values[name].set(str(num))
            if name == "height":
                self.saveHeight()
            else:
                self.__data[4] = str(num)
                self.__changeData(self.__data)


    def saveHeight(self):
        if self.__particles.get() == 0:
            self.__heightEntry.config(state=DISABLED)
            self.__data[5] = "0"
        else:
            self.__heightEntry.config(state=NORMAL)
            self.__data[5] = self.__heightVar.get()

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