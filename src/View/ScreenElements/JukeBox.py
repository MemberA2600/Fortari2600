from tkinter import *
from ScreenSetterFrameBase import ScreenSetterFrameBase

class JukeBox:

    def __init__(self, loader, baseFrame, data, changeName, changeData, w, h, currentBank, blankAnimation, topLevelWindow, itemNames):

        self.__loader = loader
        self.__baseFrame = baseFrame
        self.__data = data.split(" ")
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
        self.__fontSize = int(self.__screenSize[0]/1300 * self.__screenSize[1]/1050*14)
        self.__colors = self.__loader.colorPalettes
        self.__colorDict = self.__loader.colorDict

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize*0.65), False, False, False)
        self.__bigFont = self.__fontManager.getFont(int(self.__fontSize*1.15), False, False, False)
        self.__bigFont2 = self.__fontManager.getFont(int(self.__fontSize*1.5), False, False, False)
        self.__tinyFont = self.__fontManager.getFont(int(self.__fontSize*0.50), False, False, False)


        self.__name         = StringVar()
        self.__name.set(self.__data[0])
        self.dead  = [False]
        self.__num = - 1

        self.__loadMusicData()

        if len(list(self.__musicData.keys())) != 0:

            self.__loadPictures()
            self.__loadVars()
            #itWasHash = False

            if self.__data[2] == "#":
                itWasHash = True

            self.__setterBase = ScreenSetterFrameBase(loader, baseFrame, data, self.__name, changeName, self.dead, itemNames)
            self.__addElements()

            #if itWasHash == True:
            #    self.__changeData(self.__data)

        else:
            blankAnimation(["missing", {
                               "item": "music / waveform", "folder": self.__loader.mainWindow.projectPath.split("/")[-2]+"/musics / " + \
                                                                     self.__loader.mainWindow.projectPath.split("/")[
                                                                         -2] + "/waveforms"
                           }])

    def __loadVars(self):
        self.__byteVars     = []
        self.__nibbleVars   = []
        self.__allVars      = []

        for address in self.__loader.virtualMemory.memory.keys():
            for variable in self.__loader.virtualMemory.memory[address].variables.keys():
                var = self.__loader.virtualMemory.memory[address].variables[variable]
                if ((var.validity == "global" or
                     var.validity == self.__currentBank) and
                        (var.system == False or
                         var.iterable == True or
                         var.linkable == True)
                ):
                    self.__allVars.append(address + "::" + variable)
                    if   var.type     == "byte":
                        self.__byteVars.append(address + "::" + variable)
                        self.__nibbleVars.append(address + "::" + variable)
                    elif var.type     == "nibble":
                        self.__nibbleVars.append(address + "::" + variable)

    def __loadMusicData(self):
        self.__musicData = {}
        import os

        locks = self.__loader.virtualMemory.returnBankLocks()

        for root, dir, files in os.walk(self.__loader.mainWindow.projectPath + "/musics/"):
            for file in files:
                if file.endswith(".a26"):
                   name = ".".join(file.split(".")[:-1])
                   asmPairs = []

                   for root, dir, files in os.walk(self.__loader.mainWindow.projectPath + "/musics/"):
                       for file in files:
                           if (name in file) and ("overflow" not in file.split("_")[-1]) and\
                                    (file.endswith(".asm")) and ("engine.asm" not in file):
                               asmPairs.append(file)

                   if len(asmPairs) == 0: continue

                   self.__musicData[name] = []
                   if len(asmPairs) == 2: self.__musicData[name].append("double")
                   else:  self.__musicData[name].append("simple")

                   self.__musicData[name].append("music")

        for root, dir, files in os.walk(self.__loader.mainWindow.projectPath + "/waveforms/"):
            for file in files:
                if file.endswith(".asm"):
                    name = ".".join(file.split(".")[:-1])
                    self.__musicData[name] = ["simple", "waveform"]

    def __loadPictures(self):

        self.__jukeBoxPix = []

        self.__loader.io.loadAnimationFrames("jukebox", 4, self.__jukeBoxPix, "png", (self.__w, round((self.__w / 1260) * 198), 1))

    def __addElements(self):
        self.__uniqueFrame = Frame(self.__baseFrame, width=self.__w,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h)

        self.__uniqueFrame.pack_propagate(False)
        self.__uniqueFrame.pack(side=TOP, anchor=N, fill=X)

        self.__jukeFrame = Label(self.__uniqueFrame, width=self.__w,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=round((self.__w / 1260) * 198),
                                   image = self.__jukeBoxPix[0]
                                 )

        self.__jukeFrame.pack_propagate(False)
        self.__jukeFrame.pack(side=TOP, anchor=N, fill=X)

        self.__errorText = StringVar()

        self.__errorLine = Label(self.__uniqueFrame, width=self.__w,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   fg=self.__loader.colorPalettes.getColor("font"),
                                   height=1,
                                   font = self.__smallFont,
                                   textvariable = self.__errorText
                                 )

        self.__errorLine.pack_propagate(False)
        self.__errorLine.pack(side=TOP, anchor=N, fill=X)

        # If others are needed, put it before this comment

        self.__boxFrame = Label(self.__uniqueFrame, width=self.__w,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=9999999
                                 )

        self.__boxFrame.pack_propagate(False)
        self.__boxFrame.pack(side=TOP, anchor=N, fill=BOTH)

        divider = 3

        self.__availableFrame = Frame(self.__boxFrame, width=self.__w // divider,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=9999999
                                 )

        self.__availableFrame.pack_propagate(False)
        self.__availableFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__availableLabel = Label(self.__availableFrame,
                                   text=self.__dictionaries.getWordFromCurrentLanguage("availableMusic")+":",
                                   font=self.__smallFont, fg=self.__colors.getColor("font"),
                                   bg=self.__colors.getColor("window"), justify=CENTER
                                   )

        self.__availableLabel.pack_propagate(False)
        self.__availableLabel.pack(side=TOP, anchor=CENTER, fill=X)

        self.__availableScrollBar = Scrollbar(self.__availableFrame)
        self.__availableListBox = Listbox(   self.__availableFrame, width=100000, name = "availableList",
                                        height=1000,
                                        yscrollcommand=self.__availableScrollBar.set,
                                        selectmode=BROWSE,
                                        exportselection = False,
                                        font = self.__miniFont,
                                        justify = LEFT
                                    )

        self.__availableListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__availableListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__availableListBox.pack_propagate(False)

        self.__availableScrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__availableListBox.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__availableScrollBar.config(command=self.__availableListBox.yview)

        self.__availableListBox.bind("<ButtonRelease-1>", self.aListBoxChanged)
        self.__availableListBox.bind("<KeyRelease-Up>", self.aListBoxChanged)
        self.__availableListBox.bind("<KeyRelease-Down>", self.aListBoxChanged)

        listOfMusic = self.__data[2]
        if    listOfMusic == "#": listOfMusic = []
        else: listOfMusic = listOfMusic.split("|")

        self.__availableListBoxItems    = []
        self.__addedListBoxItems        = []

        for key in self.__musicData.keys():
            if key not in listOfMusic:
                self.__availableListBox.insert(END, key)
                self.__availableListBoxItems.append(key)

        self.__buttonsFrame = Frame(self.__boxFrame, width=self.__w // divider,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=9999999
                                 )

        self.__buttonsFrame.pack_propagate(False)
        self.__buttonsFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__removeButton = Button(self.__buttonsFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                   text = "<<", font = self.__bigFont,
                                   width= 99999, height = 1,
                                   state=DISABLED,
                                   fg = self.__loader.colorPalettes.getColor("font"),
                                   activebackground=self.__loader.colorPalettes.getColor("highLight"),
                                   activeforeground=self.__loader.colorPalettes.getColor("font"),
                                   command=self.__removeSelected)

        self.__removeButton.pack_propagate(False)
        self.__removeButton.pack(fill=X, side = BOTTOM, anchor = S)

        self.__addButton = Button(self.__buttonsFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                   text = ">>", font = self.__bigFont,
                                   width= 99999, height = 1,
                                   state=DISABLED,
                                   fg = self.__loader.colorPalettes.getColor("font"),
                                   activebackground=self.__loader.colorPalettes.getColor("highLight"),
                                   activeforeground=self.__loader.colorPalettes.getColor("font"),
                                   command=self.__addNew)

        self.__addButton.pack_propagate(False)
        self.__addButton.pack(fill=X, side = BOTTOM, anchor = S)

        self.__banksNeededLabel = Label(self.__buttonsFrame,
                                   text=self.__dictionaries.getWordFromCurrentLanguage("banksNeeded")+":",
                                   font=self.__miniFont, fg=self.__colors.getColor("font"),
                                   bg=self.__colors.getColor("window"), justify=CENTER
                                   )

        self.__banksNeededLabel.pack_propagate(False)


        self.__banksNeededVal = StringVar()
        self.__banksNeededEntry = Entry(self.__buttonsFrame,
                                   bg=self.__colors.getColor("boxBackNormal"),
                                   fg=self.__colors.getColor("boxFontNormal"),
                                   width=9999, justify=CENTER,
                                   textvariable=self.__banksNeededVal,
                                   font=self.__smallFont, state = DISABLED
                                   )

        self.__banksNeededEntry.pack_propagate(False)
        self.__banksNeededEntry.pack(fill=X, side=BOTTOM, anchor=N)
        self.__banksNeededLabel.pack(side=BOTTOM, anchor=CENTER, fill=X)

        self.__addedFrame = Frame(self.__boxFrame, width=self.__w // divider,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=9999999
                                 )

        self.__addedFrame.pack_propagate(False)
        self.__addedFrame.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__addedLabel = Label(self.__addedFrame,
                                   text=self.__dictionaries.getWordFromCurrentLanguage("addedMusic")+":",
                                   font=self.__smallFont, fg=self.__colors.getColor("font"),
                                   bg=self.__colors.getColor("window"), justify=CENTER
                                   )

        self.__addedLabel.pack_propagate(False)
        self.__addedLabel.pack(side=TOP, anchor=CENTER, fill=X)

        self.__addedScrollBar = Scrollbar(self.__addedFrame)
        self.__addedListBox = Listbox(   self.__addedFrame, width=100000, name = "addedList",
                                        height=1000,
                                        yscrollcommand=self.__addedScrollBar.set,
                                        selectmode=BROWSE,
                                        exportselection = False,
                                        font = self.__miniFont,
                                        justify = LEFT
                                    )

        self.__addedListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__addedListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__addedListBox.pack_propagate(False)

        self.__addedScrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__addedListBox.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__addedScrollBar.config(command=self.__addedListBox.yview)

        for item in listOfMusic:
            self.__addedListBox.insert(END, item)
            self.__addedListBoxItems.append(item)

        self.__addedListBox.bind("<ButtonRelease-1>", self.aListBoxChanged)
        self.__addedListBox.bind("<KeyRelease-Up>", self.aListBoxChanged)
        self.__addedListBox.bind("<KeyRelease-Down>", self.aListBoxChanged)

        self.__selecteds = {"availableList": "",
                            "addedList": ""}

        self.__banksLabel = Label(self.__buttonsFrame,
                                   text=self.__dictionaries.getWordFromCurrentLanguage("banksLocked")+":",
                                   font=self.__smallFont, fg=self.__colors.getColor("font"),
                                   bg=self.__colors.getColor("window"), justify=CENTER
                                   )

        self.__banksLabel.pack_propagate(False)

        self.__bankCheckBoxes = []
        self.__bankBoxesFrame = Frame(self.__buttonsFrame, width=self.__w,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h // 10
                                 )

        self.__bankBoxesFrame.pack_propagate(False)
        self.__banksLabel.pack(side=TOP, anchor=CENTER, fill=X)
        self.__bankBoxesFrame.pack(side=TOP, anchor=N, fill=X)

        self.__checkBoxFunctions = [
            self.__checkBoxPressed3,
            self.__checkBoxPressed4,
            self.__checkBoxPressed5,
            self.__checkBoxPressed6,
            self.__checkBoxPressed7,
            self.__checkBoxPressed8,
        ]

        for num in range(3, 9):
            item = {}
            item["value"]  = IntVar()
            item["frame"]  = Frame(self.__bankBoxesFrame, width=self.__w // divider // 6,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h // 10
                                   )

            item["frame"].pack_propagate(False)
            item["frame"].pack(side=LEFT, anchor=W, fill=Y)



            item["button"] = Checkbutton(item["frame"],
                                                 name="bankButton_"+str(num) ,
                                                 text=str(num),
                                                 bg=self.__colors.getColor("window"),
                                                 fg=self.__colors.getColor("font"),
                                                 justify=LEFT, font=self.__normalFont,
                                                 variable=item["value"], state = DISABLED,
                                                 activebackground=self.__colors.getColor("highLight"),
                                                 activeforeground=self.__loader.colorPalettes.getColor("font"),
                                                 command = self.__checkBoxFunctions[num-3]
                                            )

            item["button"].pack_propagate(False)
            item["button"].pack(fill=BOTH, side=TOP, anchor=CENTER)
            self.__bankCheckBoxes.append(item)

        self.__autoButton = Button(self.__buttonsFrame, width=99999,
                                         text=self.__dictionaries.getWordFromCurrentLanguage("autoLock"),
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__smallFont,
                                         activebackground=self.__loader.colorPalettes.getColor("highLight"),
                                         activeforeground=self.__loader.colorPalettes.getColor("font"),
                                         command=self.__autoLock
                                         )

        self.__autoButton.pack_propagate(False)
        self.__autoButton.pack(fill=X, side=TOP, anchor=N)

        self.__lll = Label(self.__buttonsFrame,
                                   text=self.__dictionaries.getWordFromCurrentLanguage("soundDataVars")+":",
                                   font=self.__smallFont, fg=self.__colors.getColor("font"),
                                   bg=self.__colors.getColor("window"), justify=CENTER
                                   )

        self.__lll.pack_propagate(False)
        self.__lll.pack(fill=X, side=TOP, anchor=N)

        self.__panelsFrame = Frame(self.__buttonsFrame, width=self.__w // divider,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h
                              )

        self.__panelsFrame.pack_propagate(False)
        self.__panelsFrame.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__panelsFrames = []
        for num in range(0,4):
            self.__panelsFrames.append({})

            f = Frame(self.__panelsFrame, width=self.__w // divider // 4,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=self.__h
                              )

            f.pack_propagate(False)
            f.pack(side=LEFT, anchor=E, fill=Y)
            self.__panelsFrames[-1]["frame"] = f

            scrollBar = Scrollbar(f)
            listBox = Listbox(              f, width=100000, name = "varListBox_" + str(num),
                                            height=1000,
                                            yscrollcommand=scrollBar.set,
                                            selectmode=BROWSE,
                                            exportselection = False,
                                            font = self.__tinyFont,
                                            justify = LEFT
                                        )

            listBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
            listBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
            listBox.pack_propagate(False)

            scrollBar.pack(side=RIGHT, anchor=W, fill=Y)
            listBox.pack(side=LEFT, anchor=W, fill=BOTH)

            scrollBar.config(command=listBox.yview)
            data = self.__data[3 + num]

            selector = 0
            n = -1
            for item in self.__byteVars:
                n += 1
                listBox.insert(END, item)
                item = item.split("::")[1]
                if item == data:
                   selector = n

            listBox.select_set(selector)
            listBox.yview(selector)

            listBox.yview(selector)
            self.__panelsFrames[-1]["listbox"]   = listBox
            self.__panelsFrames[-1]["selected"]  = data
            self.__panelsFrames[-1]["scrollbar"] = scrollBar

            self.__panelsFrames[-1]["listbox"].bind("<ButtonRelease-1>", self.__changeDataListBox)
            self.__panelsFrames[-1]["listbox"].bind("<KeyRelease-Up>", self.__changeDataListBox)
            self.__panelsFrames[-1]["listbox"].bind("<KeyRelease-Down>", self.__changeDataListBox)


        self.__setButtonsAndErros()
        self.__error = True

        self.__loader.threadLooper.addToThreading(self, self.jukeAnimation, [], 1)

        #t = Thread(target=self.jukeAnimation)
        #t.daemon = True
        #t.start()

    def __changeDataListBox(self, event):
        num = int(str(event.widget).split(".")[-1].split("_")[-1])

        if self.__panelsFrames[num]["selected"] != self.__byteVars[self.__panelsFrames[num]["listbox"].curselection()[0]].split("::")[1]:
           self.__panelsFrames[num]["selected"] = self.__byteVars[self.__panelsFrames[num]["listbox"].curselection()[0]].split("::")[1]
           self.__data[3+num]                   = self.__panelsFrames[num]["selected"]
           if self.__error == False: self.__changeData(self.__data)


    def __setCheckBoxes(self):
        if self.__selecteds["addedList"] == "":
           self.__autoButton.config(state = DISABLED)
           for num in range(0, 6):
               self.__bankCheckBoxes[num]["button"].config(state = DISABLED)
        else:
            lockedBanks = self.__loader.virtualMemory.returnBankLocks()
            for num in range(0, 6):
                self.__bankCheckBoxes[num]["button"].config(state=NORMAL)

            self.__autoButton.config(state=NORMAL)
            lockForItem = 0

            bNeeded = {"simple": 1, "double": 2}
            neededBanks = bNeeded[self.__musicData[self.__selecteds["addedList"]][0]]

            for bank in lockedBanks:
                itemNum = int(bank[-1])-3
                name = lockedBanks[bank].name
                self.__bankCheckBoxes[itemNum]["value"].set(1)
                if name != self.__selecteds["addedList"]:
                   self.__bankCheckBoxes[itemNum]["button"].config(state=DISABLED)
                else:
                   lockForItem += 1

            if lockForItem < neededBanks:
               self.setErrorLabel("jukeBoxError2", True, {
                                   "item": self.__selecteds["addedList"], "number": str(neededBanks-lockForItem)
                                    })
            else:
                for num in range(0, 6):
                    if self.__bankCheckBoxes[num]["value"].get() == 0:
                       self.__bankCheckBoxes[num]["button"].config(state=DISABLED)
                self.__autoButton.config(state=DISABLED)
                self.__error = False

            if self.__error == False:
                self.setErrorLabel("", False, None)
                self.saveData()

    def __checkBoxPressed3(self):
        self.__checkBoxPressed(3)

    def __checkBoxPressed4(self):
        self.__checkBoxPressed(4)

    def __checkBoxPressed5(self):
        self.__checkBoxPressed(5)

    def __checkBoxPressed6(self):
        self.__checkBoxPressed(6)

    def __checkBoxPressed7(self):
        self.__checkBoxPressed(7)

    def __checkBoxPressed8(self):
        self.__checkBoxPressed(8)

    def __checkBoxPressed(self, bankNum):
        #if event.widget.cget("state") == DISABLED:
        #    return

        num     = bankNum-3
        value = self.__bankCheckBoxes[num]["value"].get()

        if value == 0:
            bank = "bank" + str(bankNum)
            self.__loader.virtualMemory.locks[bank] = None
        else:
            bNeeded         = {"simple": 1, "double": 2}
            name            = self.__selecteds["addedList"]

            neededBanks     = bNeeded[self.__musicData[name][0]]
            freeBanks = self.__loader.virtualMemory.getBanksAvailableForLocking()
            typ = self.__musicData[name][1]
            mode = self.__musicData[name][0]
            self.tryToAddNewLock(neededBanks, bankNum, name, typ)


        #print(self.__loader.virtualMemory.returnBankLocks().keys())
        self.__setCheckBoxes()

    def tryToAddNewLock(self, neededBanks, bankNum, name, typ):

        if typ == "music" and neededBanks == 2:
           locks = self.__loader.virtualMemory.returnBankLocks()
           for key in locks.keys():
               lock = locks[key]
               if lock.name == name and lock.type == typ:
                  neededBanks -= 1

        if neededBanks == 1:
            if typ == "waveform":
                self.__loader.virtualMemory.registerNewLock(bankNum, name,
                                                            typ, 0, "LAST")
            else:
                locks = self.__loader.virtualMemory.returnBankLocks()
                alreadyNum = None
                for key in locks.keys():
                    lock = locks[key]
                    if lock.name == name and lock.type == typ:
                        alreadyNum = int(lock.number)

                    if alreadyNum == 0:
                        self.__loader.virtualMemory.registerNewLock(bankNum, name,
                                                                    typ, 1, "LAST")
                    else:
                        self.__loader.virtualMemory.registerNewLock(bankNum, name,
                                                                    typ, 0, "")

        elif neededBanks == 2:
            #   With current settings, this means you want to set a music lock and
            #   there are no current locks for data.

            self.__loader.virtualMemory.registerNewLock(bankNum,
                                                        self.__selecteds["addedList"],
                                                        typ, 0, "")

    def aListBoxChanged(self, event):
        name = str(event.widget).split(".")[-1]
        listBox = event.widget
        lists = {"availableList": self.__availableListBoxItems,
                 "addedList"    : self.__addedListBoxItems}

        self.__selecteds[name] = lists[name][listBox.curselection()[0]]
        self.__setButtonsAndErros()


    def setErrorLabel(self, text, error, listOfChangers):
        try:
            newText = self.__loader.dictionaries.getWordFromCurrentLanguage(text)
        except:
            newText = text

        if listOfChangers != None:
           for key in listOfChangers.keys():
               newText = newText.replace("#"+key+"#", listOfChangers[key])

        self.__errorText.set(newText)

        if error == False:
           self.__error = False
           self.__errorLine.config(
               bg=self.__loader.colorPalettes.getColor("window"),
               fg=self.__loader.colorPalettes.getColor("font"),
           )
        else:
            self.__error = True
            self.__errorLine.config(
                    bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                    fg=self.__loader.colorPalettes.getColor("boxFontUnSaved"),
                )

    def __setButtonsAndErros(self):
        self.__error = False

        if len(self.__addedListBoxItems) > 0:
           self.__removeButton.config(state = NORMAL)
        else:
           self.setErrorLabel("jukeBoxError1", True, None)
           self.__removeButton.config(state = DISABLED)

        try:
            teszt = self.__addedListBoxItems[self.__addedListBox.curselection()[0]]
        except Exception as e:
            self.__removeButton.config(state=DISABLED)

        bNeeded = {"simple": 1, "double": 2}

        freeBanks     = self.__loader.virtualMemory.getBanksAvailableForLocking()
        try:
            selectedItem  = self.__availableListBoxItems[self.__availableListBox.curselection()[0]]

            neededBanks   = bNeeded[self.__musicData[selectedItem][0]]
            self.__banksNeededVal.set(str(neededBanks))

            if neededBanks > len(freeBanks):
                self.__addButton.config(state=DISABLED)
            else:
                self.__addButton.config(state=NORMAL)
        except Exception as e:
            #print(str(e))
            self.__addButton.config(state=DISABLED)
            self.__banksNeededVal.set("")

        self.__setCheckBoxes()

        if self.__error == False:
            self.setErrorLabel("", False, None)
            self.saveData()

    def __addNew(self):
        itemSelected = self.__availableListBoxItems[self.__availableListBox.curselection()[0]]
        self.__availableListBoxItems.remove(itemSelected)
        self.__addedListBoxItems.append(itemSelected)
        self.__addedListBoxItems.sort()

        self.__selecteds["availableList"]   = ""
        self.__selecteds["addedList"]       = itemSelected

        #self.__autoLock(itemSelected)
        self.__alignListBoxes()

    def __autoLock(self):
        name = self.__selecteds["addedList"]
        locks = self.__loader.virtualMemory.returnBankLocks()
        alreadyLockedForItem = 0

        for key in locks.keys():
            if locks[key].name == name:
               alreadyLockedForItem += 1

        bNeeded = {"simple": 1, "double": 2}
        locksNeeded = bNeeded[self.__musicData[name][0]]
        freeBanks = self.__loader.virtualMemory.getBanksAvailableForLocking()

        difference = locksNeeded - alreadyLockedForItem

        for bankNum in freeBanks:
            if difference == 0:
                break

            else:
                hasMemoryAdded = False
                for address in self.__loader.virtualMemory.memory.keys():
                    for varName in self.__loader.virtualMemory.memory[address].variables:
                        if self.__loader.virtualMemory.memory[address].variables[varName].validity == "bank" + str(bankNum):
                           hasMemoryAdded = True
                           break

                if hasMemoryAdded == True: continue

                hasCode = False

                for section in self.__loader.virtualMemory.codes["bank" + str(bankNum)]:
                    valids = ["enter", "leave", "overscan", "subroutines", "vblank"]
                    if section in valids:
                        code = self.__loader.virtualMemory.codes["bank" + str(bankNum)][section].code.split("\n")
                        for line in code:
                            line = line.replace("\n", "").replace("\r", "")
                            if line[0] == "#" or line[0] == "*" or line == "":
                                continue
                            else:
                                hasCode = True
                                break
                    if hasCode == True: break

                if hasCode == True: continue

                self.tryToAddNewLock(locksNeeded, bankNum, name, self.__musicData[name][1])
                difference -= 1

            self.__setCheckBoxes()


    def __removeSelected(self):
        itemSelected = self.__addedListBoxItems[self.__addedListBox.curselection()[0]]
        self.__addedListBoxItems.remove(itemSelected)
        self.__availableListBoxItems.append(itemSelected)
        self.__availableListBoxItems.sort()

        self.__selecteds["availableList"] = itemSelected
        self.__selecteds["addedList"] = ""

        locks = self.__loader.virtualMemory.returnBankLocks()
        for key in locks:
            if locks[key].name == itemSelected:
                self.__loader.virtualMemory.locks[key] = None
                self.__bankCheckBoxes[int(key[-1]) - 3]["value"].set(0)

        self.__alignListBoxes()

    def __alignListBoxes(self):

        self.__availableListBox.select_clear(0, END)
        self.__addedListBox.select_clear(0, END)

        self.__availableListBox.delete(0, END)
        self.__addedListBox.delete(0, END)

        for item in self.__availableListBoxItems:
            self.__availableListBox.insert(END, item)

        for item in self.__addedListBoxItems:
            self.__addedListBox.insert(END, item)

        if self.__selecteds["availableList"] != "":
           selector = 0
           for itemNum in range(0, len(self.__availableListBoxItems)):
               if self.__availableListBoxItems[itemNum] == self.__selecteds["availableList"]:
                   selector = itemNum
                   break

           self.__availableListBox.select_set(selector)
           self.__availableListBox.yview(selector)

        if self.__selecteds["addedList"] != "":
            selector = 0
            for itemNum in range(0, len(self.__addedListBoxItems)):
                if self.__addedListBoxItems[itemNum] == self.__selecteds["addedList"]:
                    selector = itemNum
                    break

            self.__addedListBox.select_set(selector)
            self.__addedListBox.yview(selector)

        self.__setButtonsAndErros()

    def jukeAnimation(self):
        self.__num += 1
        if self.__num > 2: self.__num = 0
        try:
            self.__jukeFrame.config(image=self.__jukeBoxPix[self.__num])
        except:
            pass

    def saveData(self):
        self.__data[2] = "|".join(self.__addedListBoxItems)
        self.__changeData(self.__data)
