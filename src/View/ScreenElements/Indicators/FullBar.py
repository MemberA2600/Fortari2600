from tkinter import *
from copy import deepcopy

class FullBar:

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

        self.__frame3 = Frame(self.__uniqueFrame, width=self.__w // 5 * 2,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h)

        self.__frame3.pack_propagate(False)
        self.__frame3.pack(side=LEFT, anchor=E, fill=Y)

        self.__frame4 = Frame(self.__uniqueFrame, width=self.__w // 5,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h)

        self.__frame4.pack_propagate(False)
        self.__frame4.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__label1 = Label(  self.__frame1,
                        text=self.__dictionaries.getWordFromCurrentLanguage("dataVar")+":",
                        font=self.__normalFont, fg=self.__colors.getColor("font"),
                        bg=self.__colors.getColor("window"), justify=CENTER
                     )

        self.__label1.pack_propagate(False)
        self.__label1.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__label2 = Label(  self.__frame2,
                        text=self.__dictionaries.getWordFromCurrentLanguage("maxVal")+":",
                        font=self.__normalFont, fg=self.__colors.getColor("font"),
                        bg=self.__colors.getColor("window"), justify=CENTER
                     )

        self.__label2.pack_propagate(False)
        self.__label2.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__label3 = Label(  self.__frame3,
                        text=self.__dictionaries.getWordFromCurrentLanguage("color")+":",
                        font=self.__normalFont, fg=self.__colors.getColor("font"),
                        bg=self.__colors.getColor("window"), justify=CENTER
                     )

        self.__label3.pack_propagate(False)
        self.__label3.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__label4 = Label(  self.__frame4,
                        text=self.__dictionaries.getWordFromCurrentLanguage("gradient")+":",
                        font=self.__normalFont, fg=self.__colors.getColor("font"),
                        bg=self.__colors.getColor("window"), justify=CENTER
                     )

        self.__label4.pack_propagate(False)
        self.__label4.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__dataVars = []
        for address in self.__loader.virtualMemory.memory.keys():
            for variable in self.__loader.virtualMemory.memory[address].variables.keys():
                var = self.__loader.virtualMemory.memory[address].variables[variable]
                if (   (var.validity == "global" or
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
                                          font=self.__normalFont,
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
           self.__dataVarListBox.yview(0)

        else:

           selector = 0
           for itemNum in range(0, len(self.__dataVars)):
               if self.__dataVars[itemNum].split("::")[1] == self.__data[3]:
                  selector = itemNum
                  break

           self.__dataVarListBox.select_set(selector)
           self.__dataVarListBox.yview(selector)

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__dataVarListBox, "<ButtonRelease-1>", self.__changedDataVar, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__dataVarListBox, "<KeyRelease-Up>"  , self.__changedDataVar, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__dataVarListBox, "<KeyRelease-Down>", self.__changedDataVar, 1)

        #self.__dataVarListBox.bind("<ButtonRelease-1>", self.__changedDataVar)
        #self.__dataVarListBox.bind("<KeyRelease-Up>", self.__changedDataVar)
        #self.__dataVarListBox.bind("<KeyRelease-Down>", self.__changedDataVar)


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
                             font=self.__normalFont
                             )

        self.__maxVarEntry.pack_propagate(False)
        self.__maxVarEntry.pack(fill=X, side=TOP, anchor=N)

        self.__colorOption = IntVar()

        self.__constButton = Radiobutton( self.__frame3, width = 99999,
                                             text=self.__dictionaries.getWordFromCurrentLanguage("constant"),
                                             bg=self.__colors.getColor("window"),
                                             fg=self.__colors.getColor("font"),
                                             justify=LEFT, font=self.__smallFont,
                                             variable = self.__colorOption,
                                             activebackground = self.__colors.getColor("highLight"),
                                             activeforeground=self.__loader.colorPalettes.getColor("font"),
                                             value = 1, command = self.XXX
        )

        self.__constButton.pack_propagate(False)
        self.__constButton.pack(fill=X, side=TOP, anchor=N)

        from HexEntry import HexEntry
        if "|" in self.__data[5]:
            self.__color = self.__data[5].split("|")
        else:
            self.__color = ["$40", "$30", "$10"]

        self.__constFrames = Frame(self.__frame3, width=self.__w // 5 * 2,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h // 16)

        self.__constFrames.pack_propagate(False)
        self.__constFrames.pack(side=TOP, anchor=N, fill=Y)

        self.__constFrame1 = Frame(self.__constFrames, width=(self.__w // 5 * 2) // 3,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h // 16)

        self.__constFrame1.pack_propagate(False)
        self.__constFrame1.pack(side=LEFT, anchor=E, fill=Y)

        self.__constFrame2 = Frame(self.__constFrames, width=(self.__w // 5 * 2) // 3,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h // 16)

        self.__constFrame2.pack_propagate(False)
        self.__constFrame2.pack(side=LEFT, anchor=E, fill=Y)

        self.__constFrame3 = Frame(self.__constFrames, width=(self.__w // 5 * 2) // 3,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h // 16)

        self.__constFrame3.pack_propagate(False)
        self.__constFrame3.pack(side=LEFT, anchor=E, fill=Y)



        self.__constEntry = HexEntry(self.__loader, self.__constFrame1, self.__colors, self.__colorDict,
                                     self.__normalFont, self.__color, 0, None, self.__chamgeConst)

        self.__constEntry2 = HexEntry(self.__loader, self.__constFrame2, self.__colors, self.__colorDict,
                                     self.__normalFont, self.__color, 0, None, self.__chamgeConst2)

        self.__constEntry3 = HexEntry(self.__loader, self.__constFrame3, self.__colors, self.__colorDict,
                                     self.__normalFont, self.__color, 0, None, self.__chamgeConst3)


        self.__varButton = Radiobutton(self.__frame3, width=99999,
                                         text=self.__dictionaries.getWordFromCurrentLanguage("variable"),
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__smallFont,
                                         variable=self.__colorOption,
                                         activebackground=self.__colors.getColor("highLight"),
                                         activeforeground=self.__loader.colorPalettes.getColor("font"),
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
                                          font=self.__normalFont,
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

        if len(self.__data[5].split("|")) == 3:
           self.__colorOption.set(1)
           self.__color = self.__data[5].split("|")
           self.__constEntry.setValue(self.__color[0])
           self.__constEntry.changeState(NORMAL)
           self.__constEntry2.setValue(self.__color[1])
           self.__constEntry2.changeState(NORMAL)
           self.__constEntry3.setValue(self.__color[2])
           self.__constEntry3.changeState(NORMAL)

           self.__colorVarListBox.select_clear(0, END)
           self.__colorVarListBox.config(state = DISABLED)
        else:
           self.__colorOption.set(2)
           self.__color = ["$40", "$30", "$f0"]
           self.__constEntry.setValue(self.__color[0])
           self.__constEntry.changeState(DISABLED)
           self.__constEntry2.setValue(self.__color[1])
           self.__constEntry2.changeState(DISABLED)
           self.__constEntry3.setValue(self.__color[2])
           self.__constEntry3.changeState(DISABLED)
           self.__colorVarListBox.config(state = NORMAL)

           selector = 0
           for itemNum in range(0, len(self.__colorVars)):
               if self.__colorVars[itemNum].split("::")[1] == self.__data[5]:
                  selector = itemNum
                  break
           self.__colorVarListBox.select_set(selector)
           self.__colorVarListBox.yview(selector)


        from GradientFrame import GradientFrame
        self.__gradientFrame = GradientFrame(self.__loader, self.__frame4,
                                             self.__changeData, self.__h, self.__data, self.dead, 8, "normal", 6)

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__maxVarEntry, "<KeyRelease>"         , self.__changeMaxEntry      , 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__maxVarEntry, "<FocusOut>"           , self.__changeMaxEntry      , 1)

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__colorVarListBox, "<ButtonRelease-1>", self.__changedColorVar, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__colorVarListBox, "<KeyRelease-Up>"  , self.__changedColorVar, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__colorVarListBox, "<KeyRelease-Down>", self.__changedColorVar, 1)


        #self.__maxVarEntry.bind("<KeyRelease>", self.__changeMaxEntry)
        #self.__maxVarEntry.bind("<FocusOut>", self.__changeMaxEntry)
        #self.__colorVarListBox.bind("<ButtonRelease-1>", self.__changedColorVar)
        #self.__colorVarListBox.bind("<KeyRelease-Up>", self.__changedColorVar)
        #self.__colorVarListBox.bind("<KeyRelease-Down>", self.__changedColorVar)

        try:
            self.__lastSet   = self.__colorVars[self.__colorVarListBox.curselection()[0]]
        except:
            self.__lastSet   = self.__colorVars[0]

        self.__lastConst = deepcopy(self.__color)

    def __dotsChanged(self):
        self.__data[7] = str(self.__dotMode.get())
        self.__changeData(self.__data)

    def __chamgeConst(self, event):
        self.__grrrrrr(0, self.__constEntry)

    def __chamgeConst2(self, event):
        self.__grrrrrr(1, self.__constEntry2)

    def __chamgeConst3(self, event):
        self.__grrrrrr(2, self.__constEntry3)


    def __grrrrrr(self, num, entry):
        if self.__constEntry.getValue() != self.__color[num]:
           temp = entry.getValue()
           if self.isItHex(temp) == True:
              temp = temp[:2] + "0"
              self.__color[num] = temp
              entry.setValue(temp)
              self.__data[5] = "|".join(self.__color)
              self.__changeData(self.__data)

    def isItHex(self, num):
        if num[0] != "$": return False

        try:
            teszt = int("0x"+num[1:], 16)
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
           self.__constEntry.setValue(self.__lastConst[0])
           self.__constEntry2.setValue(self.__lastConst[1])
           self.__constEntry3.setValue(self.__lastConst[2])

           self.__colorVarListBox.config(state = DISABLED)
           self.__constEntry.changeState(NORMAL)
           self.__constEntry2.changeState(NORMAL)
           self.__constEntry3.changeState(NORMAL)

           self.__chamgeConst(None)
           self.__chamgeConst2(None)
           self.__chamgeConst3(None)

        else:
           self.__lastConst[0] = self.__constEntry.getValue()
           self.__lastConst[1] = self.__constEntry2.getValue()
           self.__lastConst[2] = self.__constEntry3.getValue()

           self.__constEntry.changeState(DISABLED)
           self.__constEntry2.changeState(DISABLED)
           self.__constEntry3.changeState(DISABLED)

           self.__colorVarListBox.config(state = NORMAL)
           selector = 0
           for itemNum in range(0, len(self.__colorVars)):
               if self.__colorVars[itemNum] == self.__lastSet:
                  selector = itemNum
                  break

           self.__colorVarListBox.select_set(selector)
           self.__colorVarListBox.yview(selector)

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
                bg = self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                fg = self.__loader.colorPalettes.getColor("boxFontUnSaved")
           )
        else:
            self.__maxVarEntry.config(
                bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                fg=self.__loader.colorPalettes.getColor("boxFontNormal")
            )

            binary = bin(int(self.__maxVar.get())).replace("0b", "")
            while len(binary) < 8: binary = "0" + binary

            firstOne = None
            for num in range(0, len(binary)):
                if binary[num] == "1":
                   firstOne = num
                   break

            if firstOne != None:
               binary = binary[:firstOne] + "1" * (8 - firstOne)

            self.__maxVar.set(str(int("0b"+binary, 2)))

            if self.__maxVar.get() != self.__data[4]:
               temp = self.__maxVar.get()
               if   int(temp) > 255: temp = "255"
               elif int(temp) < 1  : temp = "1"
               self.__maxVar.set(temp)
               self.__data[4] = self.__maxVar.get()
               self.__changeData(self.__data)

