from tkinter import *
from ScreenSetterFrameBase import ScreenSetterFrameBase

class Menu:

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

        self.__name         = StringVar()
        self.__name.set(self.__data[0])
        self.dead = [False]

        self.__loadPictures()

        if len(self.__listOfPictures) > 0:
            itWasHash = False
            if self.__data[2] == "#":
                itWasHash = True

            self.__setterBase = ScreenSetterFrameBase(loader, baseFrame, data, self.__name, changeName, self.dead, itemNames)
            self.__addElements()

            if itWasHash == True:
                self.__changeData(self.__data)
        else:
            blankAnimation(["missing", {
                               "item": "menu", "folder": self.__loader.mainWindow.projectPath.split("/")[-2]+"/menus"
                           }])

    def __loadPictures(self):

        self.__listOfPictures = []

        import os

        for root, dirs, files in os.walk(self.__loader.mainWindow.projectPath + "menus/"):
            for file in files:
                if file.endswith(".asm"):
                   self.__listOfPictures.append(file.replace(".asm", ""))


    def __addElements(self):
        self.__uniqueFrame = Frame(self.__baseFrame, width=self.__w,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h)

        self.__uniqueFrame.pack_propagate(False)
        self.__uniqueFrame.pack(side=TOP, anchor=N, fill=X)

        self.__listFrame = Frame(self.__uniqueFrame, width=self.__w,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h // 10 * 4)

        self.__listFrame.pack_propagate(False)
        self.__listFrame.pack(side=TOP, anchor=N, fill=X)

        self.__varListScrollBar = Scrollbar(self.__listFrame)
        self.__varListBox = Listbox(self.__listFrame, width=100000,
                                    height=1000,
                                    yscrollcommand=self.__varListScrollBar.set,
                                    selectmode=BROWSE,
                                    exportselection=False,
                                    font=self.__smallFont,
                                    justify=LEFT
                                    )

        self.__varListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__varListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__varListBox.pack_propagate(False)

        self.__varListScrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__varListBox.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__varListScrollBar.config(command=self.__varListBox.yview)

        for item in self.__listOfPictures:
            self.__varListBox.insert(END, item)


        selector = 0
        if self.__data[2] != "#":
           for itemNum in range(0, len(self.__listOfPictures)):
               if self.__data[2] == self.__listOfPictures[itemNum]:
                  selector = itemNum
                  break
        else:
            self.__data[2] = self.__listOfPictures[0]

        self.__varListBox.select_set(selector)
        self.__varListBox.yview(selector)

        self.__lastSprite = self.__listOfPictures[selector]

        self.__menuColors = []

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__varListBox, "<ButtonRelease-1>", self.__changeMenu, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__varListBox, "<KeyRelease-Up>", self.__changeMenu, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__varListBox, "<KeyRelease-Down>", self.__changeMenu, 1)

        #self.__varListBox.bind("<ButtonRelease-1>", self.__changeMenu)
        #self.__varListBox.bind("<KeyRelease-Up>", self.__changeMenu)
        #self.__varListBox.bind("<KeyRelease-Down>", self.__changeMenu)

        if self.__data[4] == "#":
           self.__getBasicDataOfPicture()
           for num in range(4, 7):
               self.__data[num] = self.__menuColors[num-4]

        else:
            for num in range(4, 7):
                self.__menuColors.append(self.__data[num])


        self.__bottomFrame = Frame(self.__uniqueFrame, width=self.__w,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h)

        self.__bottomFrame.pack_propagate(False)
        self.__bottomFrame.pack(side=TOP, anchor=N, fill=BOTH)

        self.__frames = []

        for num in range(0,4):
            frame = Frame(self.__bottomFrame, width=self.__w // 4,
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       height=self.__h)

            frame.pack_propagate(False)
            frame.pack(side=LEFT, anchor=E, fill=Y)
            self.__frames.append(frame)

        self.__dataVar = StringVar()

        self.__labelXXX = Label(self.__frames[0],
                       text=self.__dictionaries.getWordFromCurrentLanguage("dataVar")+":",
                       font=self.__smallFont, fg=self.__colors.getColor("font"),
                       bg=self.__colors.getColor("window"), justify=CENTER
                       )

        self.__labelXXX.pack_propagate(False)
        self.__labelXXX.pack(side=TOP, anchor=CENTER, fill=X)

        self.__dataVarScrollBar = Scrollbar(self.__frames[0])
        self.__dataVarListBox = Listbox(self.__frames[0], width=100000,
                                    height=1000, name="listBox_1",
                                    yscrollcommand=self.__dataVarScrollBar.set,
                                    selectmode=BROWSE,
                                    exportselection=False,
                                    font=self.__smallFont,
                                    justify=LEFT
                                    )

        self.__dataVarListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__dataVarListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__dataVarListBox.pack_propagate(False)

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__dataVarListBox, "<ButtonRelease-1>", self.__changeListBoxItem, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__dataVarListBox, "<KeyRelease-Up>"  , self.__changeListBoxItem, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__dataVarListBox, "<KeyRelease-Down>", self.__changeListBoxItem, 1)

        #self.__dataVarListBox.bind("<ButtonRelease-1>", self.__changeListBoxItem)
        #self.__dataVarListBox.bind("<KeyRelease-Up>", self.__changeListBoxItem)
        #self.__dataVarListBox.bind("<KeyRelease-Down>", self.__changeListBoxItem)

        self.__dataVarScrollBar.config(command=self.__dataVarListBox.yview)


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
                    self.__dataVarListBox.insert(END, self.__allVars[-1])

        self.__defaultButton = Button(self.__frames[0], width=99999,
                                         text=self.__dictionaries.getWordFromCurrentLanguage("defaultColors"),
                                         bg=self.__colors.getColor("window"),
                                         fg=self.__colors.getColor("font"),
                                         justify=LEFT, font=self.__normalFont,
                                         activebackground=self.__loader.colorPalettes.getColor("highLight"),
                                         activeforeground=self.__loader.colorPalettes.getColor("font"),
                                         command=self.__setDefaults
                                         )

        self.__defaultButton.pack_propagate(False)
        self.__defaultButton.pack(fill=X, side=BOTTOM, anchor=N)

        self.__dataVarScrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__dataVarListBox.pack(side=LEFT, anchor=W, fill=BOTH)

        selector = 0
        if self.__data[3] == "#":
           self.__data[3] = self.__allVars[0].split("::")[1]
        else:
            for itemNum in range(0, len(self.__allVars)):
                if self.__allVars[itemNum].split("::")[1] == self.__data[3]:
                   selector = itemNum
                   break

        self.__dataVarListBox.select_set(selector)
        self.__dataVarListBox.yview(selector)

        self.__setColorDataFromData()

        self.__hexEntries = {
            "inactive": [],
            "background": [],
            "active": []
        }

        from HexEntry import HexEntry

        txt = ["inactiveColor", "activeColor", "backColor"]

        frameNum = 0
        for key in self.__hexEntries:
            frameNum += 1
            label = Label(self.__frames[frameNum],
                                    text=self.__dictionaries.getWordFromCurrentLanguage(txt[frameNum-1]) + ":",
                                    font=self.__smallFont, fg=self.__colors.getColor("font"),
                                    bg=self.__colors.getColor("window"), justify=CENTER
                                    )

            label.pack_propagate(False)
            label.pack(side=TOP, anchor=CENTER, fill=X)

            for num in range(0,8):
                hexEntry = HexEntry(self.__loader, self.__frames[frameNum], self.__colors, self.__colorDict,
                                    self.__bigFont, self.__colorData[key], num, None, self.__changeHex)

                self.__hexEntries[key].append(hexEntry)

    def __changeMenu(self, event):
        if self.__data[2] != self.__listOfPictures[self.__varListBox.curselection()[0]]:
           self.__data[2] = self.__listOfPictures[self.__varListBox.curselection()[0]]
           self.__getBasicDataOfPicture()

           self.__changeData(self.__data)

    def __changeHex(self, event):
        hexEntry = event.widget
        dataPozList = {
            "inactive": 4, "background": 5, "active": 6
        }

        for key in self.__hexEntries:
            for num in range(0,8):
                if hexEntry == self.__hexEntries[key][num].getEntry():
                   entry = self.__hexEntries[key][num]

                   if self.isItHex(entry.getValue()) == True:
                      val = entry.getValue()
                      dataPoz = dataPozList[key]
                      newData = self.__data[dataPoz].split("|")
                      newData[num] = val
                      self.__data[dataPoz] = "|".join(newData)
                      self.__changeData(self.__data)
                   break


    def __setColorDataFromData(self):
        self.__colorData = {
            "inactive": self.__data[4].split("|"),
            "background": self.__data[5].split("|"),
            "active": self.__data[6].split("|")
        }

    def __setDefaults(self):
        name = self.__listOfPictures[self.__varListBox.curselection()[0]] + ".a26"
        fullname = self.__loader.mainWindow.projectPath + "/menus/" + name

        f = open(fullname, "r")
        data = f.readlines()
        f.close()

        num  = 3
        num2 = -1
        keys = ["inactive", "background", "active"]

        for line in data[5:8]:
            num  += 1
            num2 += 1
            line = line.replace("\n", "").replace("\r","").split(" ")
            self.__data[num] = "|".join(line)

            key = keys[num2]
            for num3 in range(0,8):
                self.__hexEntries[key][num3].setValue(line[num3])

        self.__changeData(self.__data)

    def __changeListBoxItem(self, event):
        if self.__data[3] != self.__allVars[self.__dataVarListBox.curselection()[0]].split("::")[1]:
           self.__data[3] = self.__allVars[self.__dataVarListBox.curselection()[0]].split("::")[1]
           self.__changeData(self.__data)

    def __getBasicDataOfPicture(self):
        name = self.__listOfPictures[self.__varListBox.curselection()[0]] + ".a26"
        fullname = self.__loader.mainWindow.projectPath + "/menus/" + name

        f = open(fullname, "r")
        data = f.readlines()
        f.close()

        for line in data[5:8]:
            self.__menuColors.append("|".join(line.replace("\n", "").replace("\r","").split(" ")))

    def isItHex(self, num):
        if num[0] != "$": return False

        try:
            teszt = int("0x" + num[1:], 16)
            return True
        except:
            return False