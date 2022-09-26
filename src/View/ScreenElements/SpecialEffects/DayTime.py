from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from time import sleep
import re

class DayTime:
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
        if data[4] == "#":
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

        self.__listOfFrames = []
        self.__labels = []

        frameMax = 4
        words = ["xPoz", "dataVar", "dataVar", "dataVar"]

        self.__listBoxes = []

        for num in range(0, frameMax):
            f = Frame(self.__uniqueFrame, width=self.__w // frameMax,
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       height=self.__h)

            f.pack_propagate(False)
            f.pack(side=LEFT, anchor=E, fill=Y)

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

            l = Label(f,
                          text=self.__dictionaries.getWordFromCurrentLanguage(words[num]) + ":",
                          font=self.__smallFont, fg=self.__colors.getColor("font"),
                          bg=self.__colors.getColor("window"), justify=CENTER
                          )

            l.pack_propagate(False)
            l.pack(side=TOP, anchor=CENTER, fill=BOTH)
            self.__labels.append(l)

            if num == 0:
                self.__constOrVar = IntVar()
                self.__constButton = Radiobutton(f, width=99999,
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

                self.__xConstVal = StringVar()

                self.__xConst = Entry(f,
                                           bg=self.__colors.getColor("boxBackNormal"),
                                           fg=self.__colors.getColor("boxFontNormal"),
                                           width=9999, justify=CENTER,
                                           textvariable=self.__xConstVal,
                                           font=self.__smallFont
                                           )

                self.__xConst.pack_propagate(False)
                self.__xConst.pack(fill=BOTH, side=TOP, anchor=N)

                self.__xConst.bind("<KeyRelease>", self.__changeXConst)
                self.__xConst.bind("<FocusOut>", self.__changeXConst)

                self.__varButton = Radiobutton(f, width=99999,
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

            self.__listBoxes.append({})
            self.__listBoxes[-1]["selected"] = ""

            scrollBar = Scrollbar(f)
            lbox = Listbox(f, width=100000,
                                            height=1000,
                                            yscrollcommand=scrollBar.set,
                                            selectmode=BROWSE,
                                            exportselection=False,
                                            font=self.__smallFont,
                                            justify=LEFT
                                            )

            lbox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
            lbox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
            lbox.pack_propagate(False)

            scrollBar.pack(side=RIGHT, anchor=W, fill=Y)
            lbox.pack(side=LEFT, anchor=W, fill=BOTH)

            scrollBar.config(command=lbox.yview)

            self.__listBoxes[-1]["listBox"] = lbox
            self.__listBoxes[-1]["scrollBar"] = scrollBar

            for item in self.__dataVars:
               self.__listBoxes[-1]["listBox"].insert(END, item)

        if self.isItNum(self.__data[3]):
           self.__constOrVar.set(1)
           self.__listBoxes[0]["listBox"].config(state = DISABLED)
           self.__listBoxes[0]["selected"] = self.__dataVars[0].split("::")[1]
           self.__listBoxes[0]["listBox"].select_set(0)
           self.__xConstVal.set(self.__data[3])

        else:
            self.__constOrVar.set(2)
            self.__xConst.config(state = DISABLED)
            self.__xConstVal.set("36")

            selector = 0
            for itemNum in range(0, len(self.__dataVars)):
                if self.__data[3] == self.__dataVars[itemNum].split("::")[1]:
                   selector = itemNum
                   break

            self.__listBoxes[0]["selected"] = self.__dataVars[selector].split("::")[1]
            self.__listBoxes[0]["listBox"].select_set(0)

        for num in range(1,4):
            selector = 0
            if self.__data[3 + num] == "#":
               self.__data[3 + num] = self.__dataVars[0].split("::")[1]

            for itemNum in range(0, len(self.__dataVars)):
                if self.__dataVars[itemNum].split("::")[1] == self.__data[3 + num]:
                   selector = itemNum
                   break

            self.__listBoxes[num]["listBox"].select_set(selector)
            self.__listBoxes[num]["selected"] = self.__dataVars[selector].split("::")[1]
            self.__data[num + 3] = self.__listBoxes[num]["selected"]

        for num in range(0,4):
            self.__listBoxes[num]["listBox"].bind("<ButtonRelease-1>", self.__changeListBox)
            self.__listBoxes[num]["listBox"].bind("<KeyRelease-Up>", self.__changeListBox)
            self.__listBoxes[num]["listBox"].bind("<KeyRelease-Down>", self.__changeListBox)

    def __changeXConst(self, event):
        if self.__constOrVar.get() == 2: return

    def __changeIfConstOrVar(self, event):
        if self.__constOrVar.get() == 1:
           self.__listBoxes[0]["listBox"].config(state = DISABLED)
           self.__xConst.config(state = NORMAL)

           self.__data[3] = self.__xConstVal.get()

        else:
            self.__listBoxes[0]["listBox"].config(state=NORMAL)
            self.__xConst.config(state=DISABLED)

            selector = 0
            for itemNum in range(0, len(self.__dataVars)):
                if self.__dataVars[itemNum].split("::")[1] == self.__listBoxes[0]["selected"]:
                    selector = itemNum
                    break

            


    def __changeListBox(self, event):
        numInList = 0
        for num in range(0, 4):
            if self.__listBoxes[num]["listBox"] == event.widget:
               numInList = num
               break

        if numInList == 0 and self.__constOrVar.get() == 1: return
        if self.__listBoxes[numInList]["selected"] != self.__dataVars[self.__listBoxes[numInList]["listBox"].curselection()[0]].split("::")[1]:
           self.__listBoxes[numInList]["selected"] = self.__dataVars[self.__listBoxes[numInList]["listBox"].curselection()[0]].split("::")[1]
           self.__data[3+num] = self.__listBoxes[numInList]["selected"]
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