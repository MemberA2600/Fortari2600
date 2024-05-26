from tkinter import *
from ScreenSetterFrameBase import ScreenSetterFrameBase
import os

class Picture64px:

    def __init__(self, loader, baseFrame, data, changeName, changeData, w, h, currentBank, blankAnimation, topLevelWindow, itemNames):
        self.__loader = loader
        self.__baseFrame = baseFrame
        self.__data = data.split(" ")
        self.__w = w
        self.__h = h
        self.__currentBank = currentBank
        self.__maxH = 255

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

        self.__name = StringVar()
        self.__name.set(self.__data[0])
        self.dead = [False]
        self.__lastData = None

        self.__loadPictures()

        if len(self.__varList) != 0:

            self.__tempSaved  = [None, None]
            self.__values     = [None, None]

            for num in range(0,2):
                try:
                    self.__values[num] = int(self.__data[4+num])
                except:
                    self.__tempSaved[num] = self.__data[4+num]

            wasHash = False
            if self.__data[2] == "#":
               wasHash = True
            self.__setterBase = ScreenSetterFrameBase(loader, baseFrame, data, self.__name, changeName, self.dead, itemNames)
            self.__addElements(wasHash)
        else:
            blankAnimation(["missing", {
                               "item": "64pxPicture", "folder": self.__loader.mainWindow.projectPath.split("/")[-2]+"/64px"
                           }])

    def __loadPictures(self):
        folder = self.__loader.mainWindow.projectPath + "64px"

        self.__varList = []
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith(".asm"):
                    self.__varList.append(file[:-4])

        self.__varList.sort()

    def __addElements(self, wasHash):
        self.__uniqueFrame = Frame(self.__baseFrame, width=self.__w,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h)

        self.__uniqueFrame.pack_propagate(False)
        self.__uniqueFrame.pack(side=TOP, anchor=N, fill=X)

        self.__listFrame = Frame(self.__uniqueFrame, width=self.__w,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h // 10 * 5)

        self.__listFrame.pack_propagate(False)
        self.__listFrame.pack(side=TOP, anchor=N, fill=X)

        self.__varListScrollBar = Scrollbar(self.__listFrame)
        self.__varListBox = Listbox(   self.__listFrame, width=100000,
                                        height=1000,
                                        yscrollcommand=self.__varListScrollBar.set,
                                        selectmode=BROWSE,
                                        exportselection = False,
                                        font = self.__smallFont,
                                        justify = LEFT
                                    )

        self.__varListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__varListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__varListBox.pack_propagate(False)

        self.__varListScrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__varListBox.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__varListScrollBar.config(command=self.__varListBox.yview)
        for var in self.__varList:
            self.__varListBox.insert(END, var)


        self.__setterBase.registerError("no64px")
        if len(self.__varList) == 0:
           self.__setterBase.changeErrorState("no64px", True)
           self.__varListBox.config(state = DISABLED)
        else:

            self.__loader.threadLooper.bindingMaster.addBinding(self, self.__varListBox, "<ButtonRelease-1>", self.clickedListBox,
                                                                1)
            self.__loader.threadLooper.bindingMaster.addBinding(self, self.__varListBox, "<KeyRelease-Up>", self.clickedListBox,
                                                                1)
            self.__loader.threadLooper.bindingMaster.addBinding(self, self.__varListBox, "<KeyRelease-Down>", self.clickedListBox,
                                                                1)

            #self.__varListBox.bind("<ButtonRelease-1>", self.clickedListBox)
            #self.__varListBox.bind("<KeyRelease-Up>", self.clickedListBox)
            #self.__varListBox.bind("<KeyRelease-Down>", self.clickedListBox)

            self.__tempSet = self.__varList[0]

            if self.__data[2] == "#":
                self.setIt(0)

            else:
                found = False
                for itemNum in range(0, len(self.__varList)):
                    if self.__varList[itemNum] == self.__data[2]:
                       found = True
                       self.setIt(itemNum)
                       break

                if found == False:
                   self.setIt(0)

        self.__column1 = Frame(self.__uniqueFrame, width=self.__w // 3,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h // 10 * 5)

        self.__column1.pack_propagate(False)
        self.__column1.pack(side=LEFT, anchor=E, fill=Y)

        self.__column2 = Frame(self.__uniqueFrame, width=self.__w // 3,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h // 10 * 5)

        self.__column2.pack_propagate(False)
        self.__column2.pack(side=LEFT, anchor=E, fill=Y)

        self.__column3 = Frame(self.__uniqueFrame, width=self.__w // 3,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h // 10 * 5)

        self.__column3.pack_propagate(False)
        self.__column3.pack(side=LEFT, anchor=E, fill=Y)

        self.__label1 = Label(self.__column1,
                                   text=self.__dictionaries.getWordFromCurrentLanguage("height"),
                                   font=self.__normalFont, fg=self.__colors.getColor("font"),
                                   bg=self.__colors.getColor("window"), justify=CENTER
                                   )

        self.__label1.pack_propagate(False)
        self.__label1.pack(side=TOP, anchor=CENTER, fill=X)

        self.__label2 = Label(self.__column2,
                                   text=self.__dictionaries.getWordFromCurrentLanguage("displayedHeight"),
                                   font=self.__normalFont, fg=self.__colors.getColor("font"),
                                   bg=self.__colors.getColor("window"), justify=CENTER
                                   )

        self.__label2.pack_propagate(False)
        self.__label2.pack(side=TOP, anchor=CENTER, fill=X)

        self.__label3 = Label(self.__column3,
                                   text=self.__dictionaries.getWordFromCurrentLanguage("heightIndex"),
                                   font=self.__normalFont, fg=self.__colors.getColor("font"),
                                   bg=self.__colors.getColor("window"), justify=CENTER
                                   )

        self.__label3.pack_propagate(False)
        self.__label3.pack(side=TOP, anchor=CENTER, fill=X)

        self.__heightVar = StringVar()
        self.__heightVar.set(self.__data[3])

        self.__heightEntry = Entry(self.__column1,
                                        bg=self.__colors.getColor("boxBackNormal"),
                                        fg=self.__colors.getColor("boxFontNormal"),
                                        width=9999, justify = CENTER,
                                        textvariable=self.__heightVar,
                                        font=self.__normalFont
                                        )

        self.__heightEntry.pack_propagate(False)
        self.__heightEntry.pack(fill=X, side = TOP, anchor = N)

        self.__varConst1 = IntVar()
        if self.isItNum(self.__data[4]) == True:
           self.__varConst1.set(1)
        else:
           self.__varConst1.set(2)

        self.__varConst2 = IntVar()
        if self.isItNum(self.__data[5]) == True:
           self.__varConst2.set(1)
        else:
           self.__varConst2.set(2)

        self.__constantButton1 = Radiobutton(self.__column2, width=99999,
                                             text=self.__dictionaries.getWordFromCurrentLanguage("constant"),
                                             bg=self.__colors.getColor("window"),
                                             fg=self.__colors.getColor("font"),
                                             justify=LEFT, font=self.__normalFont,
                                             variable=self.__varConst1,
                                             activebackground=self.__loader.colorPalettes.getColor("highLight"),
                                             activeforeground=self.__loader.colorPalettes.getColor("font"),
                                             value=1, command=self.XXX1
                                             )

        self.__constantButton1.pack_propagate(False)
        self.__constantButton1.pack(side=TOP, anchor=N, fill=X)

        self.__heightIndexVar = StringVar()
        self.__heightIndexVar.set(self.__data[3])

        self.__heightIndexEntry = Entry(self.__column2, name = "heightIndexEntry",
                                        bg=self.__colors.getColor("boxBackNormal"),
                                        fg=self.__colors.getColor("boxFontNormal"),
                                        width=9999, justify = CENTER,
                                        textvariable=self.__heightIndexVar,
                                        font=self.__normalFont
                                        )

        self.__heightIndexEntry.pack_propagate(False)
        self.__heightIndexEntry.pack(fill=X, side = TOP, anchor = N)

        if self.__varConst1.get == 1:
           self.__heightIndexVar.set(self.__data[4])
        else:
           self.__heightIndexEntry.config(state=DISABLED)

        self.__variableButton1 = Radiobutton( self.__column2, width = 99999,
                                             text=self.__dictionaries.getWordFromCurrentLanguage("variable"),
                                             bg=self.__colors.getColor("window"),
                                             fg=self.__colors.getColor("font"),
                                             justify=LEFT, font=self.__normalFont,
                                             variable = self.__varConst1,
                                             activebackground=self.__loader.colorPalettes.getColor("highLight"),
                                             activeforeground=self.__loader.colorPalettes.getColor("font"),
                                             value = 2, command = self.XXX1
        )

        self.__variableButton1.pack_propagate(False)
        self.__variableButton1.pack(side = TOP, anchor = N, fill = X)

        self.__varList1 = []
        for address in self.__loader.virtualMemory.memory.keys():
            for variable in self.__loader.virtualMemory.memory[address].variables.keys():
                var = self.__loader.virtualMemory.memory[address].variables[variable]
                if (
                        (var.validity == "global" or
                        var.validity == self.__currentBank) and
                        (var.system == False or
                        var.iterable == True or
                        var.linkable == True
                        )
                ):
                   self.__varList1.append(address + "::" + variable)

        self.__varList1.sort()

        self.__varListScrollBar1 = Scrollbar(self.__column2)
        self.__varListBox1 = Listbox(   self.__column2, width=100000, name = "varListBox1",
                                        height=1000,
                                        yscrollcommand=self.__varListScrollBar1.set,
                                        selectmode=BROWSE,
                                        exportselection = False,
                                        font = self.__smallFont,
                                        justify = LEFT
                                    )

        self.__varListBox1.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__varListBox1.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__varListBox1.pack_propagate(False)

        self.__varListScrollBar1.pack(side=RIGHT, anchor=W, fill=Y)
        self.__varListBox1.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__varListScrollBar1.config(command=self.__varListBox1.yview)

        for item in self.__varList1:
            self.__varListBox1.insert(END, item)

        if self.__varConst1.get() == 1:
            self.__varListBox1.select_clear(0, END)
            self.__varListBox1.config(state = DISABLED)
        else:
            self.__varListBox1.config(state = NORMAL)
            selected = 0
            for itemNum in range(0, len(self.__varList1)):
                if self.__varList1[itemNum] == self.__data[4]:
                   selected = itemNum
                   break
            self.__varListBox1.select_clear(0, END)
            self.__varListBox1.select_set(selected)
            self.__varListBox1.yview(selected)

            self.__tempSaved[0] = selected

        self.__constantButton2 = Radiobutton(self.__column3, width=99999,
                                             text=self.__dictionaries.getWordFromCurrentLanguage("constant"),
                                             bg=self.__colors.getColor("window"),
                                             fg=self.__colors.getColor("font"),
                                             justify=LEFT, font=self.__normalFont,
                                             variable=self.__varConst2,
                                             activebackground=self.__loader.colorPalettes.getColor("highLight"),
                                             activeforeground=self.__loader.colorPalettes.getColor("font"),
                                             value=1, command=self.XXX2
                                             )

        self.__constantButton2.pack_propagate(False)
        self.__constantButton2.pack(side=TOP, anchor=N, fill=X)

        self.__indexVar = StringVar()
        self.__indexVar.set(self.__data[3])

        self.__indexEntry = Entry(self.__column3, name = "indexEntry",
                                        bg=self.__colors.getColor("boxBackNormal"),
                                        fg=self.__colors.getColor("boxFontNormal"),
                                        width=9999, justify=CENTER,
                                        textvariable=self.__indexVar,
                                        font=self.__normalFont
                                        )

        self.__indexEntry.pack_propagate(False)
        self.__indexEntry.pack(fill=X, side=TOP, anchor=N)

        if self.__varConst2.get == 1:
           self.__indexVar.set(self.__data[5])
        else:
           self.__indexEntry.config(state=DISABLED)

        self.__variableButton2 = Radiobutton(self.__column3, width=99999,
                                             text=self.__dictionaries.getWordFromCurrentLanguage("variable"),
                                             bg=self.__colors.getColor("window"),
                                             fg=self.__colors.getColor("font"),
                                             justify=LEFT, font=self.__normalFont,
                                             variable=self.__varConst2,
                                             activebackground=self.__loader.colorPalettes.getColor("highLight"),
                                             activeforeground=self.__loader.colorPalettes.getColor("font"),
                                             value=2, command=self.XXX2
                                             )

        self.__variableButton2.pack_propagate(False)
        self.__variableButton2.pack(side=TOP, anchor=N, fill=X)

        self.__varListScrollBar2 = Scrollbar(self.__column3)
        self.__varListBox2 = Listbox(   self.__column3, width=100000, name = "varListBox2",
                                        height=1000,
                                        yscrollcommand=self.__varListScrollBar2.set,
                                        selectmode=BROWSE,
                                        exportselection = False,
                                        font = self.__smallFont,
                                        justify = LEFT
                                    )

        self.__varListBox2.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__varListBox2.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__varListBox2.pack_propagate(False)

        self.__varListScrollBar2.pack(side=RIGHT, anchor=W, fill=Y)
        self.__varListBox2.pack(side=LEFT, anchor=W, fill=BOTH)

        for item in self.__varList1:
            self.__varListBox2.insert(END, item)

        self.__varListScrollBar2.config(command=self.__varListBox1.yview)

        if self.__varConst2.get() == 1:
            self.__varListBox2.select_clear(0, END)
            self.__varListBox2.config(state = DISABLED)
        else:
            self.__varListBox2.config(state = NORMAL)
            selected = 0
            for itemNum in range(0, len(self.__varList1)):
                if self.__varList1[itemNum] == self.__data[5]:
                   selected = itemNum
                   break
            self.__varListBox2.select_clear(0, END)
            self.__varListBox2.select_set(selected)
            self.__varListBox2.yview(selected)

            self.__tempSaved[1] = selected

        self.__vars = [
            {"option"    : self.__varConst1,
             "entry"     : self.__heightIndexEntry,
             "listBox"   : self.__varListBox1,
             "value"     : self.__heightIndexVar,
             "min"       : 1,
             },
            {"option"    : self.__varConst2,
             "entry"     : self.__indexEntry,
             "listBox"   : self.__varListBox2,
             "value"     : self.__indexVar,
             "min"       : 0
             }

        ]

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__indexEntry      , "<FocusOut>"       , self.__chamgeConst  , 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__indexEntry      , "<KeyRelease>"     , self.__chamgeConst  , 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__heightIndexEntry, "<KeyRelease>"     , self.__chamgeConst  , 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__heightIndexEntry, "<KeyRelease>"     , self.__chamgeConst  , 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__varListBox1     , "<ButtonRelease-1>", self.clickedListBox1, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__varListBox2     , "<ButtonRelease-1>", self.clickedListBox1, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__varListBox1     , "<KeyRelease-Up>"  , self.clickedListBox1, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__varListBox1     , "<KeyRelease-Down>", self.clickedListBox1, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__varListBox2     , "<KeyRelease-Up>"  , self.clickedListBox1, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__varListBox2     , "<KeyRelease-Down>", self.clickedListBox1, 1)

        #self.__indexEntry.bind("<FocusOut>", self.__chamgeConst)
        #self.__indexEntry.bind("<KeyRelease>", self.__chamgeConst)
        #self.__heightIndexEntry.bind("<FocusOut>", self.__chamgeConst)
        #self.__heightIndexEntry.bind("<KeyRelease>", self.__chamgeConst)
        #self.__varListBox1.bind("<ButtonRelease-1>", self.clickedListBox1)
        #self.__varListBox2.bind("<ButtonRelease-1>", self.clickedListBox1)
        #self.__varListBox1.bind("<KeyRelease-Up>", self.clickedListBox1)
        #self.__varListBox1.bind("<KeyRelease-Down>", self.clickedListBox1)
        #self.__varListBox2.bind("<KeyRelease-Up>", self.clickedListBox1)
        #self.__varListBox2.bind("<KeyRelease-Down>", self.clickedListBox1)

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__heightEntry, "<FocusOut>"  , self.heightConstStuff, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__heightEntry, "<KeyRelease>", self.heightConstStuff, 1)

        #self.__heightEntry.bind("<FocusOut>", self.heightConstStuff)
        #self.__heightEntry.bind("<KeyRelease>", self.heightConstStuff)

        if wasHash == True:
           self.__heightVar.set(str(self.__maxH))
           self.__heightIndexVar.set(str(self.__maxH))
           self.__data[3] = str(self.__maxH)
           self.__data[4] = str(self.__maxH)
           self.__values[0] = self.__data[4]

           self.__lastData = None
           self.setIt(0)

        self.setIt1(None, 0)
        self.setIt1(None, 1)

    def isItNum(self, num):
        try:
            num = int(num)
            return True
        except:
            return False

    def XXX1(self):
        self.setIt1(None, 0)

    def XXX2(self):
        self.setIt1(None, 1)

    def setIt1(self, data, num):
        if self.__vars[num]["option"].get() == 2:
           self.__vars[num]["entry"].config(state = DISABLED)
           self.__vars[num]["listBox"].config(state=NORMAL)

           if data == None:
               selector = 0
               for itemNum in range(0, len(self.__varList1)):
                   if self.__varList1[itemNum] == self.__tempSaved[num]:
                      selector = itemNum
                      break

               self.__tempSaved[num] = self.__varList1[selector]
               self.__data[4+num] = self.__tempSaved[num]
               self.__vars[num]["listBox"].select_clear(0, END)
               self.__vars[num]["listBox"].select_set(selector)
               self.__vars[num]["listBox"].yview(selector)

               if self.__data[3] != '0' and self.__data[4] != '0': self.__changeData(self.__data)

           else:
               self.__tempSaved[num] = self.__varList1[data]
               if self.__data[4+num] != self.__tempSaved[num]:
                    self.__data[4+num] = self.__tempSaved[num]
                    if self.__data[3] != '0' and self.__data[4] != '0': self.__changeData(self.__data)

           #print(self.__loader.virtualMemory.getVariableByName2(self.__tempSet).usedBits)
        else:
            self.__vars[num]["listBox"].select_clear(0, END)
            self.__vars[num]["listBox"].config(state = DISABLED)
            self.__vars[num]["entry"].config(state=NORMAL)

            if data == None:
               self.__vars[num]["value"].set(str(self.__values[num]))
               self.__data[4+num] = str(self.__values[num])
               self.__changeData(self.__data)
            else:
               backUp = self.__values[num]
               self.__values[num]  = int(self.__vars[num]["value"].get())
               if data != backUp:
                   self.__data[4+num]   = str(self.__values[num])
                   if self.__data[3] != '0' and self.__data[4] != '0': self.__changeData(self.__data)

        self.__checkMaxHeight()

    def getName(self, event):
        return str(event.widget).split(".")[-1]

    def heightConstStuff(self, event):
        try:
            num = int(self.__heightVar.get())
        except:
            self.__heightEntry.config(
                bg=self.__colors.getColor("boxBackUnSaved"),
                fg=self.__colors.getColor("boxFontUnSaved"))
            self.__setterBase.changeErrorState("mustBeVar2", True)

            return(False)

        self.__heightEntry.config(
            bg=self.__colors.getColor("boxBackNormal"),
            fg=self.__colors.getColor("boxFontNormal"))
        self.__setterBase.changeErrorState("mustBeVar2", False)

        if num < 1      : num = 1
        elif num > 255  : num = 255

        if str(event).split(" ")[0][1:] != "FocusOut": return False

        self.__heightVar.set(str(num))
        self.__checkMaxHeight()

    def clickedListBox1(self, event):
        name = self.getName(event)
        nums = {
            "varListBox1": 0,
            "varListBox2": 1
        }
        num = nums[name]

        if self.__vars[num]["option"].get() == 1:
            return
        self.__checkMaxHeight()
        self.setIt1(self.__vars[num]["listBox"].curselection()[0], num)


    def __chamgeConst(self, event):
        name = self.getName(event)
        nums = {
            "heightIndexEntry": 0,
            "indexEntry"      : 1
        }
        num = nums[name]

        if self.__vars[num]["option"].get() == 2:
            return

        if self.__checkIfConstIsRight(event, num) == True: self.setIt1(self.__vars[num]["value"].get(), num)

    def __checkIfConstIsRight(self, event, offset):
        try:
            num = int(self.__vars[offset]["value"].get())
        except:
            self.__vars[offset]["entry"].config(
                bg=self.__colors.getColor("boxBackUnSaved"),
                fg=self.__colors.getColor("boxFontUnSaved"))
            self.__setterBase.changeErrorState("mustBeVar2", True)

            return(False)

        self.__vars[offset]["entry"].config(
            bg=self.__colors.getColor("boxBackNormal"),
            fg=self.__colors.getColor("boxFontNormal"))
        self.__setterBase.changeErrorState("mustBeVar2", False)

        if   num < self.__vars[offset]["min"]     : num = self.__vars[offset]["min"]
        elif num > self.__vars[offset]["min"]+255 : num = self.__vars[offset]["min"]+255

        if str(event).split(" ")[0][1:] != "FocusOut": return False

        self.__vars[offset]["value"].set(str(num))
        return True

    def clickedListBox(self, event):
        self.setIt(self.__varListBox.curselection()[0])
        self.__forceMaxHeight()
        self.__values[0] = str(self.__maxH)
        self.__values[1] = "0"


    def setIt(self, selected):
        if self.__lastData != self.__varList[selected]:
            self.__lastData = self.__varList[selected]
            self.__data[2]  = self.__varList[selected]
            num = 0
            for itemNum in range(0, len(self.__varList)):
                if self.__varList[itemNum] == self.__data[2]:
                    num = itemNum
                    break

            self.__varListBox.select_clear(0, END)
            self.__varListBox.select_set(num)
            self.__varListBox.yview(num)

            #if self.__data[3] != '0' and self.__data[4] != '0': self.__changeData(self.__data)
            self.__maxH = self.getMaxHeight()
            self.__forceMaxHeight()

    def __checkMaxHeight(self):
        try:
            if int(self.__heightVar.get()) > self.__maxH:
               self.__heightVar.set(str(self.__maxH))

            if int(self.__indexVar.get()) > self.__maxH-1:
               self.__indexVar.set(str(self.__maxH-1))

            if int(self.__heightIndexVar.get()) > self.__maxH:
               self.__heightIndexVar.set(str(self.__maxH))

            self.__data[3] = self.__heightVar.get()
            if self.__varConst2 == 1:
                self.__data[5] = self.__indexVar.get()
            if self.__varConst1 == 1:
                self.__data[4] = self.__heightIndexVar.get()
            if self.__data[3] != '0' and self.__data[4] != '0': self.__changeData(self.__data)

        except Exception as e:
            #print(str(e))
            pass

    def __forceMaxHeight(self):
        try:
            self.__heightVar.set(str(self.__maxH))
            self.__indexVar.set("0")
            self.__heightIndexVar.set(str(self.__maxH))
            self.__data[3] = self.__heightVar.get()
            self.__data[5] = self.__indexVar.get()
            self.__data[4] = self.__heightIndexVar.get()

            if self.__data[3] != '0' and self.__data[4] != '0': self.__changeData(self.__data)
        except Exception as e:
            #print(str(e))
            pass

    def getMaxHeight(self):
        fileName1 = self.__loader.mainWindow.projectPath+"64px/"     +\
                    self.__varList[self.__varListBox.curselection()[0]] +\
                    ".a26"
        fileName2 = self.__loader.mainWindow.projectPath+"64px/"     +\
                    self.__varList[self.__varListBox.curselection()[0]] +\
                    ".asm"

        if os.path.exists(fileName1):
           f   = open(fileName1, "r")
           txt = f.read().replace("\r", "").split("\n")
           f.close()

           return(int(txt[0]))
        else:
           f = open(fileName2, "r")
           lines = f.read().replace("\r", "").split("\n")
           f.close()

           foundByte = False
           counter   = 0
           for line in lines:
               if "BYTE" in line.upper():
                   foundByte = True
                   counter  += 1
               else:
                   if foundByte == True:
                      break
           return counter