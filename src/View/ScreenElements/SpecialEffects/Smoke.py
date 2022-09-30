from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from time import sleep
import re

class Smoke:
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

        self.__nibbleVars = []
        self.__byteVars   = []
        self.__iterVars   = []

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
                if ((var.type == "byte") and
                        (var.validity == "global" or
                         var.validity == self.__currentBank) and
                        (var.system == False or
                         var.iterable == True )
                ):
                    self.__iterVars.append(address + "::" + variable)


        self.__frames = []
        self.__words = ["dataVar", "spriteColor", "backColor", "gradientSprite", "gradientBack"]
        self.__listBoxes = [{}, {}, {}]

        for num in range(0, 5):
            self.__frames.append(Frame(self.__uniqueFrame, width=self.__w // 5,
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       height=self.__h))

            self.__frames[-1].pack_propagate(False)
            self.__frames[-1].pack(side=LEFT, anchor=E, fill=Y)

            label = Label(self.__frames[-1],
                              text=self.__dictionaries.getWordFromCurrentLanguage(self.__words[num]) + ":",
                              font=self.__smallFont, fg=self.__colors.getColor("font"),
                              bg=self.__colors.getColor("window"), justify=CENTER
                              )

            label.pack_propagate(False)
            label.pack(side=TOP, anchor=CENTER, fill=BOTH)

        from HexEntry import HexEntry
        self.__fuckinColors = ["$02", "$74"]
        self.__colorEntries = []
        self.__changerButtons = [{}, {}]

        counter = -2
        for num in range(0,3):
            isItHex = False
            commands = [self.__changerButtonPressedC0, self.__changerButtonPressedV0,
                        self.__changerButtonPressedC1, self.__changerButtonPressedV1,]

            if num > 0:

                counter += 2
                self.__changerButtons[num - 1]["value"] = IntVar()
                self.__changerButtons[num - 1]["constantB"] = self.__createButton(self.__frames[num],
                                                                              "constant", self.__changerButtons[num - 1]["value"],
                                                                              commands[counter], 1
                                                                              )

                isItHex = self.isItHex(self.__data[num+3])

                if isItHex: self.__fuckinColors[num-1] = self.__data[num+3]
                self.__colorEntries.append( HexEntry(self.__loader, self.__frames[num], self.__colors, self.__colorDict,
                                            self.__normalFont, self.__fuckinColors, num-1, None, self.__changeColorVar))

                self.__changerButtons[num - 1]["variableB"] = self.__createButton(self.__frames[num],
                                                                              "variable", self.__changerButtons[num - 1]["value"],
                                                                              commands[counter+1], 2
                                                                              )

            self.__listBoxes[num]["variable"] = StringVar()
            self.__listBoxes[num]["scrollbar"] = Scrollbar(self.__frames[num])
            sb = self.__listBoxes[num]["scrollbar"]

            self.__listBoxes[num]["listbox"] = Listbox(self.__frames[num], width=100000,
                                                          name=self.__words[num],
                                                          height=1000,
                                                          yscrollcommand = sb.set,
                                                          selectmode=BROWSE,
                                                          exportselection=False,
                                                          font=self.__smallFont,
                                                          justify=LEFT
                                                          )
            self.__listBoxes[num]["listbox"].config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
            self.__listBoxes[num]["listbox"].config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
            self.__listBoxes[num]["listbox"].pack_propagate(False)

            self.__listBoxes[num]["scrollbar"].pack(side=RIGHT, anchor=W, fill=Y)
            self.__listBoxes[num]["listbox"].pack(side=LEFT, anchor=W, fill=BOTH)
            self.__listBoxes[num]["scrollbar"].config(command=self.__listBoxes[num]["listbox"].yview)

            self.__listBoxes[num]["listbox"].bind("<ButtonRelease-1>", self.__clickedListBox)
            self.__listBoxes[num]["listbox"].bind("<KeyRelease-Up>", self.__clickedListBox)
            self.__listBoxes[num]["listbox"].bind("<KeyRelease-Down>", self.__clickedListBox)

            if num != 0:
                for item in self.__byteVars:
                    self.__listBoxes[num]["listbox"].insert(END, item)
            else:
                for item in self.__iterVars:
                    self.__listBoxes[num]["listbox"].insert(END, item)

            if isItHex == True:
               self.__changerButtons[num-1]["value"].set(1)
               self.__colorEntries[num-1].changeState(NORMAL)
               self.__listBoxes[num]["listbox"].config(state = DISABLED)
               self.__listBoxes[num]["lastSelected"] = self.__byteVars[0].split("::")[-1]
            else:
               if num > 0:
                   self.__changerButtons[num - 1]["value"].set(2)
                   self.__colorEntries[num - 1].changeState(DISABLED)
                   self.__listBoxes[num]["listbox"].config(state=NORMAL)

               selector = 0
               if num > 0:
                   for num2 in range(0, len(self.__byteVars)):
                       if self.__byteVars[num2].split("::")[1] == self.__data[num+3]:
                          selector = num2
                          break

                   self.__listBoxes[num]["lastSelected"] = self.__byteVars[selector].split("::")[-1]

               else:
                   for num2 in range(0, len(self.__iterVars)):
                       if self.__iterVars[num2].split("::")[1] == self.__data[num+3]:
                          selector = num2
                          break
                   self.__listBoxes[num]["lastSelected"] = self.__iterVars[selector].split("::")[-1]

               self.__listBoxes[num]["listbox"].select_set(selector)
               if num > 0:
                   if self.__data[num+3] == "#": self.__data[num+3] =\
                       self.__byteVars[self.__listBoxes[num]["listbox"].curselection()[0]].split("::")[1]
               else:
                   if self.__data[num+3] == "#": self.__data[num+3] =\
                       self.__iterVars[self.__listBoxes[num]["listbox"].curselection()[0]].split("::")[1]

        self.__gradients = [self.__data[6].split("|"), self.__data[7].split("|")]
        self.__gradientEntries = [[], []]

        for groupNum in range(0, 2):
            for colorNum in range(0,16):
                self.__gradientEntries[groupNum].append(HexEntry(self.__loader, self.__frames[groupNum+3], self.__colors, self.__colorDict,
                                                    self.__smallFont, self.__gradients[groupNum], colorNum, None,
                                                    self.__changeGradientColorVar))

       # self.__listBoxes[0]["listbox"].itemconfig(0, fg = self.__loader.colorPalettes.getColor("fontDisabled"))
       # self.__listBoxes[0]["listbox"].itemconfig(1, fg = self.__loader.colorPalettes.getColor("fontDisabled"))

    def __changeGradientColorVar(self, event):
        group = 0
        for groupNum in range(0, 2):
            for colorNum in range(0,16):
                if self.__gradientEntries[groupNum][colorNum].getEntry() == event.widget:
                   group = groupNum

        temp = []
        wasError = False
        for colorNum in range(0,16):
            if self.isItHex(self.__gradientEntries[group][colorNum].getValue()):
                temp.append(self.__gradientEntries[group][colorNum].getValue())
            else:
                wasError = True
                break

        if wasError == False:
            self.__data[group + 6] = "|".join(temp)
            self.__changeData(self.__data)


    def __createButton(self, frame, textKey, variable, func, val):
        button = Radiobutton(frame, width=99999,
                                         text=self.__dictionaries.getWordFromCurrentLanguage(textKey),
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__smallFont,
                                         variable=variable,
                                         activebackground=self.__colors.getColor("highLight"),
                                         value=val, command=func
                                         )

        button.pack_propagate(False)
        button.pack(fill=X, side=TOP, anchor=N)

        return button

    def __clickedListBox(self, event):
        name = str(event.widget).split(".")[-1]
        num  = self.__words.index(name)
        this = None

        if num > 0:
           if self.__changerButtons[num-1]["value"].get() == 1: return
           this = self.__byteVars[self.__listBoxes[num]["listbox"].curselection()[0]].split("::")[1]
        else:
           this = self.__iterVars[self.__listBoxes[num]["listbox"].curselection()[0]].split("::")[1]

        if this != self.__listBoxes[num]["lastSelected"]:
           self.__listBoxes[num]["lastSelected"]    = this
           self.__data[num+3]                       = this
           self.__changeData(self.__data)

    def __changerButtonPressedC0(self):
        self.__changerButtonPressed("C", 0)

    def __changerButtonPressedV0(self):
        self.__changerButtonPressed("V", 0)

    def __changerButtonPressedC1(self):
        self.__changerButtonPressed("C", 1)

    def __changerButtonPressedV1(self):
        self.__changerButtonPressed("V", 1)

    def __changerButtonPressed(self, typ, num):
        if typ == "C":
           self.__colorEntries[num].changeState(NORMAL)
           self.__listBoxes[num+1]["listbox"].config(state = DISABLED)
           self.__data[num+4] = self.__colorEntries[num].getValue()
           self.__changeData(self.__data)
        else:
           self.__colorEntries[num].changeState(DISABLED)
           self.__listBoxes[num+1]["listbox"].config(state = NORMAL)
           self.__listBoxes[num+1]["listbox"].selection_clear(0, END)
           selector = 0
           for itemNum in range(0, len(self.__byteVars)):
               if self.__byteVars[itemNum].split("::")[1] == self.__listBoxes[num+1]["lastSelected"]:
                  selector = itemNum
                  break

           self.__listBoxes[num+1]["listbox"].select_set(selector)
           self.__data[num+4] = self.__byteVars[selector].split("::")[1]
           self.__changeData(self.__data)

    def __changeColorVar(self, event):
        num = 0
        for num in range(0, 2):
            if self.__colorEntries[num].getEntry() == event.widget: break

        if self.__changerButtons[num]["value"].get() == 2: return
        if self.__colorEntries[num].getValue() != self.__data[num+4]:
           self.__data[num+4] = self.__colorEntries[num].getValue()
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