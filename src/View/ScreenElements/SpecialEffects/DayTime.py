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

        frameMax = 5
        words = ["xPoz", "dataVar", "dataVar", "dataVar", "speedConst"]

        self.__listBoxes = []

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

        for num in range(0, frameMax):
            f = Frame(self.__uniqueFrame, width=self.__w // frameMax,
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       height=self.__h)

            f.pack_propagate(False)
            f.pack(side=LEFT, anchor=E, fill=Y)

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

                self.__xConst.bind("<KeyRelease>", self.__changeConst)
                self.__xConst.bind("<FocusOut>", self.__changeConst)

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

            if num < 4:
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

                if num == 0:
                    for item in self.__byteVars:
                       self.__listBoxes[-1]["listBox"].insert(END, item)
                else:
                    for item in self.__iterVars:
                       self.__listBoxes[-1]["listBox"].insert(END, item)
            else:
                l = Label(f,
                          text=self.__dictionaries.getWordFromCurrentLanguage("sunMoon") + ":",
                          font=self.__miniFont, fg=self.__colors.getColor("window"),
                          bg=self.__colors.getColor("font"), justify=CENTER
                          )

                l.pack_propagate(False)
                l.pack(side=TOP, anchor=CENTER, fill=BOTH)
                self.__labels.append(l)

                self.__spriteSpeed1Val = StringVar()
                self.__spriteSpeed1 = Entry(f,
                                           bg=self.__colors.getColor("boxBackNormal"),
                                           fg=self.__colors.getColor("boxFontNormal"),
                                           width=9999, justify=CENTER,
                                           textvariable=self.__spriteSpeed1Val,
                                           font=self.__smallFont
                                           )

                self.__spriteSpeed1.pack_propagate(False)
                self.__spriteSpeed1.pack(fill=BOTH, side=TOP, anchor=N)

                self.__spriteSpeed1.bind("<KeyRelease>", self.__changeConst)
                self.__spriteSpeed1.bind("<FocusOut>", self.__changeConst)

                l = Label(f,
                          text=self.__dictionaries.getWordFromCurrentLanguage("cloud") + ":",
                          font=self.__smallFont, fg=self.__colors.getColor("window"),
                          bg=self.__colors.getColor("font"), justify=CENTER
                          )

                l.pack_propagate(False)
                l.pack(side=TOP, anchor=CENTER, fill=BOTH)
                self.__labels.append(l)

                self.__spriteSpeed2Val = StringVar()
                self.__spriteSpeed2 = Entry(f,
                                           bg=self.__colors.getColor("boxBackNormal"),
                                           fg=self.__colors.getColor("boxFontNormal"),
                                           width=9999, justify=CENTER,
                                           textvariable=self.__spriteSpeed2Val,
                                           font=self.__smallFont
                                           )

                self.__spriteSpeed2.pack_propagate(False)
                self.__spriteSpeed2.pack(fill=BOTH, side=TOP, anchor=N)

                self.__spriteSpeed2.bind("<KeyRelease>", self.__changeConst)
                self.__spriteSpeed2.bind("<FocusOut>", self.__changeConst)

        if self.isItNum(self.__data[3]):
           self.__constOrVar.set(1)
           self.__listBoxes[0]["listBox"].config(state = DISABLED)
           self.__listBoxes[0]["selected"] = self.__byteVars[0].split("::")[1]
           self.__listBoxes[0]["listBox"].select_set(0)
           self.__xConstVal.set(self.__data[3])

        else:
            self.__constOrVar.set(2)
            self.__xConst.config(state = DISABLED)
            self.__xConstVal.set("36")

            selector = 0
            for itemNum in range(0, len(self.__byteVars)):
                if self.__data[3] == self.__byteVars[itemNum].split("::")[1]:
                   selector = itemNum
                   break

            self.__listBoxes[0]["selected"] = self.__byteVars[selector].split("::")[1]
            self.__listBoxes[0]["listBox"].select_set(0)

        for num in range(1,4):
            selector = 0
            if self.__data[3 + num] == "#":
               self.__data[3 + num] = self.__iterVars[0].split("::")[1]

            for itemNum in range(0, len(self.__iterVars)):
                if self.__iterVars[itemNum].split("::")[1] == self.__data[3 + num]:
                   selector = itemNum
                   break

            self.__listBoxes[num]["listBox"].select_set(selector)
            self.__listBoxes[num]["selected"] = self.__iterVars[selector].split("::")[1]
            self.__data[num + 3] = self.__listBoxes[num]["selected"]

        for num in range(0,4):
            self.__listBoxes[num]["listBox"].bind("<ButtonRelease-1>", self.__changeListBox)
            self.__listBoxes[num]["listBox"].bind("<KeyRelease-Up>", self.__changeListBox)
            self.__listBoxes[num]["listBox"].bind("<KeyRelease-Down>", self.__changeListBox)

        self.__spriteSpeed1Val.set(self.__data[7])
        self.__spriteSpeed2Val.set(self.__data[8])


    def __changeConst(self, event):
        pairs = {
            self.__xConst:          self.__xConstVal,
            self.__spriteSpeed1:    self.__spriteSpeed1Val,
            self.__spriteSpeed2:    self.__spriteSpeed2Val
        }

        if event.widget == self.__xConst:
            if self.__constOrVar.get() == 2: return

        valueHolder = pairs[event.widget]
        if self.isItNum(valueHolder.get()) == False:
            event.widget.config(
                bg = self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                fg = self.__loader.colorPalettes.getColor("boxFontUnSaved")
            )
            return

        event.widget.config(
            bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
            fg=self.__loader.colorPalettes.getColor("boxFontNormal")
        )

        num = int(valueHolder.get())

        minMax = {
            self.__xConst:          [35, 128],
            self.__spriteSpeed1:    [0, 7],
            self.__spriteSpeed2:    [0, 7]
        }

        numberOfData = {
            self.__xConst:          3,
            self.__spriteSpeed1:    7,
            self.__spriteSpeed2:    8
        }

        if num < minMax[event.widget][0]: num = minMax[event.widget][0]
        if num > minMax[event.widget][1]: num = minMax[event.widget][1]

        pairs[event.widget].set(str(num))
        self.__data[numberOfData[event.widget]] = str(num)
        self.__changeData(self.__data)

    def __changeIfConstOrVar(self):
        if self.__constOrVar.get() == 1:
           self.__listBoxes[0]["listBox"].config(state = DISABLED)
           self.__xConst.config(state = NORMAL)

           self.__data[3] = self.__xConstVal.get()

        else:
            self.__listBoxes[0]["listBox"].config(state=NORMAL)
            self.__xConst.config(state=DISABLED)

            selector = 0
            for itemNum in range(0, len(self.__byteVars)):
                if self.__byteVars[itemNum].split("::")[1] == self.__listBoxes[0]["selected"]:
                    selector = itemNum
                    break

            self.__data[3] = self.__listBoxes[0]["selected"]
            self.__listBoxes[0]["listBox"].select_clear(0, END)
            self.__listBoxes[0]["listBox"].select_set(selector)

        self.__changeData(self.__data)

    def __changeListBox(self, event):
        numInList = 0
        for num in range(0, 4):
            if self.__listBoxes[num]["listBox"] == event.widget:
               numInList = num
               break

        if numInList == 0 and self.__constOrVar.get() == 1: return
        if numInList == 0:
            if self.__listBoxes[numInList]["selected"] != self.__byteVars[self.__listBoxes[numInList]["listBox"].curselection()[0]].split("::")[1]:
               self.__listBoxes[numInList]["selected"] = self.__byteVars[self.__listBoxes[numInList]["listBox"].curselection()[0]].split("::")[1]
               self.__data[3+numInList] = self.__listBoxes[numInList]["selected"]
               self.__changeData(self.__data)
        else:
            if self.__listBoxes[numInList]["selected"] != self.__iterVars[self.__listBoxes[numInList]["listBox"].curselection()[0]].split("::")[1]:
               self.__listBoxes[numInList]["selected"] = self.__iterVars[self.__listBoxes[numInList]["listBox"].curselection()[0]].split("::")[1]
               self.__data[3+numInList] = self.__listBoxes[numInList]["selected"]
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