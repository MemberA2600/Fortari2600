from tkinter import *
from ScreenSetterFrameBase import ScreenSetterFrameBase
import os
from time import sleep

class Picture48px:

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
        self.__lastSelectedPic = None

        self.__height = -1
        self.__numOfFrames = -1

        if len(self.__varList) != 0:

            """
            self.__tempSaved  = [None, None]
            self.__values     = [None, None]

            for num in range(0,2):
                try:
                    self.__values[num]    = self.convertToNum(self.__data[4+num])
                except:
                    self.__tempSaved[num] = self.__data[4+num]
            """
            wasHash = False
            if self.__data[2] == "#":
               wasHash = True
            self.__setterBase = ScreenSetterFrameBase(loader, baseFrame, data, self.__name, changeName, self.dead, itemNames)
            self.__addElements(wasHash)
        else:
            blankAnimation(["missing", {
                               "item": "48pxPicture", "folder": self.__loader.mainWindow.projectPath.split("/")[-2]+"/48px"
                           }])

    def __loadPictures(self):
        folder = self.__loader.mainWindow.projectPath + "48px"

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
                                   height=self.__h // 10 * 3)

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

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__varListBox, "<ButtonRelease-1>",
                                                            self.selectOtherPicture,
                                                            1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__varListBox, "<KeyRelease-Up>",
                                                            self.selectOtherPicture,
                                                            1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__varListBox, "<KeyRelease-Down>",
                                                            self.selectOtherPicture,
                                                            1)

        self.__varListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__varListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__varListBox.pack_propagate(False)

        self.__varListScrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__varListBox.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__varListScrollBar.config(command=self.__varListBox.yview)
        for var in self.__varList:
            self.__varListBox.insert(END, var)

        self.__setterBase.registerError("no48px")

        if len(self.__varList) == 0:
           self.__setterBase.changeErrorState("no48px", True)
           self.__varListBox.config(state = DISABLED)
        else:
           h = self.__h // 10 * 7

           if self.__data[2] == "#" or self.__data[2] not in self.__varList:
              self.__data[2] = self.__varList[0]

           for itemNum in range(0, len(self.__varList)):
               if self.__varList[itemNum] == self.__data[2]:
                  self.__varListBox.select_clear(0, END)
                  self.__varListBox.select_set(itemNum)

           self.__allVars  = []
           self.__byteVars = []
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
                       self.__allVars.append(address + "::" + variable)
                       if var.type == "byte":
                          self.__byteVars.append(address + "::" + variable)

           self.__byteVars.sort()

           self.__allOthersFrame = Frame(self.__uniqueFrame, width=self.__w,
                                     bg=self.__loader.colorPalettes.getColor("window"),
                                     height=h)

           self.__allOthersFrame.pack_propagate(False)
           self.__allOthersFrame.pack(side=TOP, anchor=N, fill=BOTH)

           self.__keys = [
               "frameNum", "displayedHeight", "heightIndex", "speed+FIndex"
           ]

           staticOnly                    = [True, False, False, False]
           self.__varTypeLists           = [None, self.__allVars, self.__allVars, self.__byteVars]
           specials                      = ["includedFrames", None, None, None]
           self.__specialLabelsandFrames = []

           self.getHeightFrameNum()
           defaults                      = [self.__numOfFrames, self.__height, 0, 0]

           w = self.__w // len(self.__keys)

           self.__dataElements = {}
           for keyNum in range(0, len(self.__keys)):
               key = self.__keys[keyNum]
               self.__dataElements[key] = {}
               self.__dataElements[key]["frame"] = Frame(self.__allOthersFrame, width=w,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=h)

               self.__dataElements[key]["frame"].pack_propagate(False)
               self.__dataElements[key]["frame"].pack(side=LEFT, anchor=E, fill=Y)

               self.__dataElements[key]["label"] = Label(self.__dataElements[key]["frame"], width=w,
                                                         bg=self.__loader.colorPalettes.getColor("window"),
                                                         fg=self.__loader.colorPalettes.getColor("font"),
                                                         text = self.__dictionaries.getWordFromCurrentLanguage(key),
                                                         font = self.__smallFont,
                                                         height=1)
               self.__dataElements[key]["label"].pack_propagate(False)
               self.__dataElements[key]["label"].pack(side=TOP, anchor=N, fill=X)

               if staticOnly[keyNum] == False:
                  self.__dataElements[key]["optionVar"]   = IntVar()
                  self.__dataElements[key]["optionFrame1"] = Frame(self.__dataElements[key]["frame"], width=self.__w,
                                                bg=self.__loader.colorPalettes.getColor("window"),
                                                height=h // 16)

                  self.__dataElements[key]["optionFrame1"].pack_propagate(False)
                  self.__dataElements[key]["optionFrame1"].pack(side=TOP, anchor=N, fill=X)

                  self.__dataElements[key]["optionButton1"] = Radiobutton(self.__dataElements[key]["optionFrame1"], width=99999,
                                                       text=self.__dictionaries.getWordFromCurrentLanguage("constant"),
                                                       name = "optionButton1_" + key,
                                                       bg=self.__colors.getColor("window"),
                                                       fg=self.__colors.getColor("font"),
                                                       justify=LEFT, font=self.__smallFont,
                                                       variable=self.__dataElements[key]["optionVar"],
                                                       activebackground=self.__loader.colorPalettes.getColor(
                                                           "highLight"),
                                                       activeforeground=self.__loader.colorPalettes.getColor("font"),
                                                       value=1, command=self.pressedOptionButton
                                                       )

                  self.__dataElements[key]["optionButton1"].pack_propagate(False)
                  self.__dataElements[key]["optionButton1"].pack(side=TOP, anchor=N, fill=BOTH)

               self.__dataElements[key]["entryFrame"] = Frame(self.__dataElements[key]["frame"], width=self.__w,
                                                                bg=self.__loader.colorPalettes.getColor("window"),
                                                                height=h // 16)

               self.__dataElements[key]["entryFrame"].pack_propagate(False)
               self.__dataElements[key]["entryFrame"].pack(side=TOP, anchor=N, fill=X)

               self.__dataElements[key]["entryVar"] = StringVar()
               self.__dataElements[key]["entry"] = Entry(self.__dataElements[key]["entryFrame"], name = "entry_" + key,
                                        bg=self.__colors.getColor("boxBackNormal"),
                                        fg=self.__colors.getColor("boxFontNormal"),
                                        width=9999, justify = CENTER,
                                        textvariable=self.__dataElements[key]["entryVar"],
                                        font=self.__smallFont
                                        )

               self.__dataElements[key]["entry"].pack_propagate(False)
               self.__dataElements[key]["entry"].pack(side=TOP, anchor=N, fill=BOTH)

               self.__loader.threadLooper.bindingMaster.addBinding(self, self.__dataElements[key]["entry"], "<FocusOut>",
                                                                   self.__changeConst, 1)
               self.__loader.threadLooper.bindingMaster.addBinding(self, self.__dataElements[key]["entry"], "<KeyRelease>",
                                                                   self.__changeConst, 1)


               if staticOnly[keyNum] == False:
                   self.__dataElements[key]["optionFrame2"] = Frame(self.__dataElements[key]["frame"], width=self.__w,
                                                                    bg=self.__loader.colorPalettes.getColor("window"),
                                                                    height=h // 16)

                   self.__dataElements[key]["optionFrame2"].pack_propagate(False)
                   self.__dataElements[key]["optionFrame2"].pack(side=TOP, anchor=N, fill=X)

                   self.__dataElements[key]["optionButton2"] = Radiobutton(self.__dataElements[key]["optionFrame2"],
                                                                           width=99999,
                                                                           text=self.__dictionaries.getWordFromCurrentLanguage(
                                                                               "variable"),
                                                                           name="optionButton2_" + key,
                                                                           bg=self.__colors.getColor("window"),
                                                                           fg=self.__colors.getColor("font"),
                                                                           justify=LEFT, font=self.__smallFont,
                                                                           variable=self.__dataElements[key][
                                                                               "optionVar"],
                                                                           activebackground=self.__loader.colorPalettes.getColor(
                                                                               "highLight"),
                                                                           activeforeground=self.__loader.colorPalettes.getColor(
                                                                               "font"),
                                                                           value=2, command=self.pressedOptionButton
                                                                           )

                   self.__dataElements[key]["optionButton2"].pack_propagate(False)
                   self.__dataElements[key]["optionButton2"].pack(side=TOP, anchor=N, fill=BOTH)

                   self.__dataElements[key]["listBoxFrame"] = Frame(self.__dataElements[key]["frame"], width=self.__w,
                                                                    bg=self.__loader.colorPalettes.getColor("window"),
                                                                    height=h )

                   self.__dataElements[key]["listBoxFrame"].pack_propagate(False)
                   self.__dataElements[key]["listBoxFrame"].pack(side=TOP, anchor=N, fill=BOTH)

                   self.__dataElements[key]["scrollBar"] = Scrollbar(self.__dataElements[key]["listBoxFrame"])
                   self.__dataElements[key]["listBox"]   = Listbox(self.__dataElements[key]["listBoxFrame"], width=100000, name="listBox_" + key,
                                                                   height=1000,
                                                                   yscrollcommand=self.__dataElements[key]["scrollBar"].set,
                                                                   selectmode=BROWSE,
                                                                   exportselection=False,
                                                                   font=self.__smallFont,
                                                                   justify=LEFT
                                                                   )

                   self.__dataElements[key]["listBox"].config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
                   self.__dataElements[key]["listBox"].config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
                   self.__dataElements[key]["listBox"].pack_propagate(False)

                   self.__dataElements[key]["scrollBar"].pack(side=RIGHT, anchor=W, fill=Y)
                   self.__dataElements[key]["listBox"].pack(side=LEFT, anchor=W, fill=BOTH)

                   self.__dataElements[key]["scrollBar"].config(command=self.__dataElements[key]["listBox"].yview)
                   self.__dataElements[key]["lastSelected"] = 0

                   for varName in self.__varTypeLists[keyNum]:
                       self.__dataElements[key]["listBox"].insert(END, varName)

                   self.__loader.threadLooper.bindingMaster.addBinding(self, self.__dataElements[key]["listBox"], "<ButtonRelease-1>",
                                                                       self.clickedListBox1, 1)
                   self.__loader.threadLooper.bindingMaster.addBinding(self, self.__dataElements[key]["listBox"], "<KeyRelease-Up>",
                                                                       self.clickedListBox1, 1)
                   self.__loader.threadLooper.bindingMaster.addBinding(self, self.__dataElements[key]["listBox"], "<KeyRelease-Down>",
                                                                       self.clickedListBox1, 1)

               dataNum   = keyNum + 3
               isItConst = False
               try:
                   num       = self.convertToNum(self.__data[dataNum])
                   isItConst = True
               except:
                   pass

               if isItConst:
                  if num == -1:
                     self.__data[dataNum] = str(defaults[keyNum])


                  self.__dataElements[key]["entryVar"].set(self.__data[dataNum])
                  if staticOnly[keyNum] == False:
                     self.__dataElements[key]["optionVar"].set(1)
                     self.pressedOptionButton()
               else:
                   self.__dataElements[key]["optionVar"].set(2)
                   thisIsIt = 0

                   for varNum in range(0, len(self.__varTypeLists[keyNum])):
                       if self.__data[dataNum] == self.__varTypeLists[keyNum][varNum]:
                          thisIsIt = varNum
                          break

                   self.__dataElements[key]["lastSelected"] = thisIsIt
                   self.pressedOptionButton()

               if specials[keyNum] != None:
                  f = Frame(self.__dataElements[key]["frame"], width=w,
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       height=h // 16)

                  f.pack_propagate(False)
                  f.pack(side=TOP, anchor=N, fill=X)

                  l = Label(f, width=w,
                            bg=self.__loader.colorPalettes.getColor("window"),
                            fg=self.__loader.colorPalettes.getColor("font"),
                            text = self.__dictionaries.getWordFromCurrentLanguage(specials[keyNum]),
                            font = self.__smallFont,
                            height=1)
                  l.pack_propagate(False)
                  l.pack(side=TOP, anchor=N, fill=BOTH)

                  self.__specialLabelsandFrames.append([f, l])

                  if  specials[keyNum] == "includedFrames":
                      self.__rangeEntryVars = []
                      self.__rangeEntries   = []

                      f2 = Frame(self.__dataElements[key]["frame"], width=w,
                                           bg=self.__loader.colorPalettes.getColor("window"),
                                           height=h // 16)

                      f2.pack_propagate(False)
                      f2.pack(side=TOP, anchor=N, fill=X)

                      w1 = w // 12 * 5
                      w2 = w - (w1 * 2)

                      f2_1 = Frame(f2,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=h // 16, width = w1)

                      f2_1.pack_propagate(False)
                      f2_1.pack(side=LEFT, anchor=E, fill=Y)

                      f2_2 = Frame(f2,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=h // 16, width = w2)

                      f2_2.pack_propagate(False)
                      f2_2.pack(side=LEFT, anchor=E, fill=Y)

                      f2_3 = Frame(f2,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=h // 16, width = w1)

                      f2_3.pack_propagate(False)
                      f2_3.pack(side=LEFT, anchor=E, fill=Y)

                      self.__specialLabelsandFrames.append(f2)
                      self.__specialLabelsandFrames.append(f2_1)
                      self.__specialLabelsandFrames.append(f2_2)
                      self.__specialLabelsandFrames.append(f2_3)

                      l2_2 = Label(f2_2, width=w,
                                bg=self.__loader.colorPalettes.getColor("window"),
                                fg=self.__loader.colorPalettes.getColor("font"),
                                text="-",
                                font=self.__normalFont,
                                height=1)
                      l2_2.pack_propagate(False)
                      l2_2.pack(side=TOP, anchor=N, fill=BOTH)

                      self.__specialLabelsandFrames.append(l2_2)

                      e1V = StringVar()
                      e2V = StringVar()

                      self.__rangeEntryVars.append(e1V)
                      self.__rangeEntryVars.append(e2V)

                      e1 = Entry(f2_1, name="entry_from",
                                 bg=self.__colors.getColor("boxBackNormal"),
                                 fg=self.__colors.getColor("boxFontNormal"),
                                 width=9999, justify=CENTER,
                                 textvariable=e1V,
                                 font=self.__normalFont
                                 )

                      e1.pack_propagate(False)
                      e1.pack(side=TOP, anchor=N, fill=BOTH)

                      e2 = Entry(f2_3, name="entry_to",
                                 bg=self.__colors.getColor("boxBackNormal"),
                                 fg=self.__colors.getColor("boxFontNormal"),
                                 width=9999, justify=CENTER,
                                 textvariable=e2V,
                                 font=self.__normalFont
                                 )

                      e2.pack_propagate(False)
                      e2.pack(side=TOP, anchor=N, fill=BOTH)

                      self.__loader.threadLooper.bindingMaster.addBinding(self, e1, "<FocusOut>",
                                                                          self.__changedFromTo, 1)
                      self.__loader.threadLooper.bindingMaster.addBinding(self, e1, "<KeyRelease>",
                                                                          self.__changedFromTo, 1)

                      self.__loader.threadLooper.bindingMaster.addBinding(self, e2, "<FocusOut>",
                                                                          self.__changedFromTo, 1)
                      self.__loader.threadLooper.bindingMaster.addBinding(self, e2, "<KeyRelease>",
                                                                          self.__changedFromTo, 1)

                      if self.__data[7] == "-1" or self.__data[8] == "-1":
                         self.__data[7] = "0"
                         self.__data[8] = str(self.__numOfFrames - 1)

                      e1V.set(self.__data[7])
                      e2V.set(self.__data[8])

                      self.__rangeEntries.append(e1)
                      self.__rangeEntries.append(e2)

           self.selectOtherPicture(None)

        self.__changeData(self.__data)

    def clickedListBox1(self, event):
        listBox     = event.widget
        key         = str(listBox).split(".")[-1].split("_")[-1]
        keyNum      = self.__keys.index(key)
        dataKey     = keyNum + 3

        lastSelected = self.__dataElements[key]["lastSelected"]

        if lastSelected != self.__dataElements[key]["listBox"].curselection()[0]:
           lastSelected         = self.__dataElements[key]["listBox"].curselection()[0]
           self.__data[dataKey] = self.__varTypeLists[keyNum][lastSelected]
           self.__changeData(self.__data)

    def __changedFromTo(self, event):
        entry    = event.widget
        name     = str(entry).split(".")[-1].split("_")[-1]

        index    = self.__rangeEntries.index(entry)

        entryVal = self.__rangeEntryVars[index]

        try:
            num = self.convertToNum(entryVal.get())
        except:
            entry.config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                         fg=self.__loader.colorPalettes.getColor("boxFontUnSaved"))
            return

        entry.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                     fg=self.__loader.colorPalettes.getColor("boxFontNormal"))

        if  name == "from":
            currentFrom = num
            try:
                currentTo = self.convertToNum(self.__rangeEntryVars[1 - index].get())
            except:
                currentTo = self.__numOfFrames - 1
        else:
            currentTo   = num
            try:
                currentFrom = self.convertToNum(self.__rangeEntryVars[1 - index].get())
            except:
                currentFrom = 0

        self.checkTheEntries(currentFrom, currentTo)

    def pressedOptionButton(self):
        for keyNum in range(0, len(self.__keys)):

            key     = self.__keys[keyNum]
            dataNum = keyNum + 3

            if key in self.__dataElements.keys():
                if "optionVar" in self.__dataElements[key]:
                    was = self.__data[dataNum]

                    if self.__dataElements[key]["optionVar"].get() == 1:
                       self.__dataElements[key]["listBox"].config(state = DISABLED)
                       self.__dataElements[key]["entry"]  .config(state = NORMAL)

                       self.__data[dataNum] = self.__dataElements[key]["entryVar"].get()
                    else:
                       self.__dataElements[key]["listBox"].config(state=NORMAL)
                       self.__dataElements[key]["entry"]  .config(state=DISABLED)

                       self.__dataElements[key]["listBox"].select_clear(0, END)
                       self.__dataElements[key]["listBox"].select_set(self.__dataElements[key]["lastSelected"])
                       self.__data[dataNum] = self.__varTypeLists[keyNum][self.__dataElements[key]["lastSelected"]]

                    if was != self.__data[dataNum]:
                       self.__changeData(self.__data)

    def selectOtherPicture(self, event):
        selected = self.__varListBox.curselection()[0]
        if selected != self.__lastSelectedPic:
           self.__lastSelectedPic = selected
           was = self.__data[2]
           self.__data[2] = self.__varList[selected]
           self.__varListBox.select_clear(0, END)
           self.__varListBox.select_set(selected)

           if was != self.__data[2]:
              self.getHeightFrameNum()

              defaults = [self.__numOfFrames, self.__height, 0, 0]

              for keyNum in range(0, len(self.__keys)):
                  key = self.__keys[keyNum]

                  self.__dataElements[key]["entryVar"].set(str(defaults[keyNum]))

                  change = True
                  if "optionVar" in self.__dataElements[key].keys():
                      if self.__dataElements[key]["optionVar"].get() == 2:
                          change = False
                  if change:
                     self.__data[keyNum + 3] = str(defaults[keyNum])

              #print(self.__height, self.__numOfFrames)

              defaults = []


              """
              for key in ["frameNum", "displayedHeight", "heightIndex", "speed+FIndex"]:
                  wasField = self.__dataElements[key]["entryVar"].get()
                  num      = self.checkKey(key)

                  #print(key, num)

                  if   "%" in wasField:
                        txt = bin(num).replace("0b", "")
                        txt = "%" + (8 - len(txt)) * "0" + txt
                  elif "$" in wasField:
                        txt = bin(num).replace("0x", "")
                        txt = "$" + (2 - len(txt)) * "0" + txt
                  else:
                        txt = str(num)

                  if wasField != txt:
                     self.__dataElements[key]["entryVar"].set(txt)
                     self.__data[self.__keys.index(key) + 3] = txt

              
              if self.__height != -1 and self.__numOfFrames != -1:
                  try:
                      currentFrom = self.convertToNum(self.__rangeEntryVars[0].get())
                  except:
                      currentFrom = 0

                  try:
                      currentTo = self.convertToNum(self.__rangeEntryVars[1].get())
                  except:
                      currentTo = self.__numOfFrames - 1

                  self.checkTheEntries(currentFrom, currentTo)
              """
              if self.__height != -1 and self.__numOfFrames != -1:
                 currentFrom = 0
                 currentTo   = self.__numOfFrames - 1
                 self.checkTheEntries(currentFrom, currentTo)

              self.__changeData(self.__data)

    def checkKey(self, key):
        if   key == "frameNum":
             return self.checkConst("frameNum"       , 1, self.__numOfFrames    , self.__numOfFrames    , [0, 1, 2, 3, 4, 5, 6, 7])
        elif key == "displayedHeight":
             return self.checkConst("displayedHeight", 1, self.__height   , self.__height         , [0, 1, 2, 3, 4, 5, 6, 7])
        elif key == "heightIndex":
             return self.checkConst("heightIndex"    , 0, self.__height - 1     , self.__height - 1     , [0, 1, 2, 3, 4, 5, 6, 7])
        elif key == "speed+FIndex":
             return self.checkConst("speed+FIndex"   , 0, self.__numOfFrames - 1, self.__numOfFrames - 1, [0, 1, 2, 3])

        #print(key)


    def checkConst(self, key, min_, max_, default, bits):
        startIndex = min(bits)
        endIndex   = max(bits)

        try:
            as8bits   = bin(self.convertToNum(self.__dataElements[key]["entryVar"].get())).replace("0b", "")
        except:
            as8bits   = bin(default).replace("0b", "")

        as8bits = (8 - len(as8bits)) * "0" + as8bits

        if len(bits) != 8:
            slice = as8bits[7 - endIndex: 8 - startIndex]
        else:
            slice = as8bits

        __8bitVal = int("0b" + slice, 2)
        if __8bitVal > max_:
            __8bitVal = max_

        if __8bitVal < min_:
            __8bitVal = min_

        if len(bits) == 8:
            return __8bitVal
        else:
            thatBits = bin(__8bitVal).replace("0b", "")
            if len(thatBits) > len(bits):
                thatBits = thatBits[:-1 * (len(bits))]
            elif len(thatBits) < len(bits):
                thatBits = (len(bits) - len(thatBits)) * "0" + thatBits

            as8bits = as8bits[:7 - endIndex] + thatBits + as8bits[8 - startIndex:]
            return int("0b" + as8bits, 2)

        #print(key)

    """
    def checkUpdateConst(self, key, min_, max_, default, bits):
        wasOK  = False
        ifNot8 = None
        startIndex = -1
        endIndex   = -1

        original   = self.__dataElements[key]["entryVar"].get()

        #print(">>", key, default)

        try:
            if len(bits) == 8:
               num = self.convertToNum(self.__dataElements[key]["entryVar"].get())
            else:
               ifNot8 = bin(self.convertToNum(self.__dataElements[key]["entryVar"].get())).replace("0b", "")
               ifNot8 = (8 - len(ifNot8)) * "0" + ifNot8

               startIndex = 7 - max(bits)
               endIndex   = 7 - min(bits)

               slice = ifNot8[startIndex:endIndex + 1]

               num = int("0b" + slice, 2)

            if num > max_ or num < min_:
                num = default
            else:
                wasOK = True
        except:
            if len(bits) == 8:
               num = default
            else:
               ifNot8 = bin(default).replace("0b", "")
               ifNot8 = (8 - len(ifNot8)) * "0" + ifNot8

               startIndex = 7 - max(bits)
               endIndex   = 7 - min(bits)

               slice = ifNot8[startIndex:endIndex + 1]

               num = int("0b" + slice, 2)

        print(key, num)

        if key == "frameNum":
            try:
                currentFrom = self.convertToNum(self.__rangeEntryVars[0].get())
            except:
                currentFrom = 0

            try:
                currentTo = self.convertToNum(self.__rangeEntryVars[1].get())
            except:
                currentTo = self.__numOfFrames - 1

            self.checkTheEntries(currentFrom, currentTo)

        elif key == "heightIndex":
            try:
                dHeigth = self.convertToNum(self.__dataElements["displayedHeight"]["entryVar"].get())
                if num > self.__height - dHeigth - 1: num = self.__height - dHeigth - 1
                wasOK = False
            except:
                pass

        if len(bits) != 8:
           start   = ifNot8[0:startIndex]
           end     = ifNot8[endIndex : 8]
           between = bin(num).replace("0b", "")
           between = (8 - len(between)) * "0" + between

           num = int("0b" + start + between + end, 2)

        return num
        """
    def getHeightFrameNum(self):
        path = self.__loader.mainWindow.projectPath + "48px/" + self.__data[2] + ".asm"
        f = open(path, "r")
        lines = f.read().replace("\r", "").split("\n")
        f.close()

        self.__height = -1
        self.__numOfFrames = -1
        for line in lines:
            if line.startswith("* Height="):
                self.__height = int(line.split("=")[1])
            if line.startswith("* Frames="):
                self.__numOfFrames = int(line.split("=")[1])

        #print(self.__height, self.__numOfFrames)

    def checkTheEntries(self, currentFrom, currentTo):
        if currentFrom < 0 or currentFrom > self.__numOfFrames - 1:
           currentFrom = 0

        if currentTo < 0 or currentTo > self.__numOfFrames - 1:
            currentTo = self.__numOfFrames - 1

        if currentFrom > currentTo: currentFrom, currentTo = currentTo, currentFrom

        self.__rangeEntryVars[0].set(str(currentFrom))
        self.__rangeEntryVars[1].set(str(currentTo))

        self.__rangeEntries[0].icursor(len(self.__rangeEntryVars[0].get()))
        self.__rangeEntries[1].icursor(len(self.__rangeEntryVars[1].get()))

        self.__rangeEntries[0].config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                      fg=self.__loader.colorPalettes.getColor("boxFontNormal"))

        self.__rangeEntries[1].config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                      fg=self.__loader.colorPalettes.getColor("boxFontNormal"))

        self.__dataElements["frameNum"]["entry"].config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                      fg=self.__loader.colorPalettes.getColor("boxFontNormal"))

        self.__dataElements["frameNum"]["entryVar"].set(str(currentTo - currentFrom + 1))

        if self.__data[7]         != str(currentFrom) \
        or self.__data[8]         != str(currentTo)   :
           self.__data[7]          = str(currentFrom)
           self.__data[8]          = str(currentTo)
           self.__changeData(self.__data)

    def convertToNum(self, s):
        if   s.startswith("%"):
             return int(s.replace("%", "0b"), 2)
        elif s.startswith("$"):
             return int(s.replace("$", "0x"), 16)
        else:
             return int(s)

    def __changeConst(self, event):
        entry    = event.widget
        key      = str(entry).split(".")[-1].split("_")[-1]

        entryVal = self.__dataElements[key]["entryVar"]

        try:
            num  = self.convertToNum(entryVal.get())
        except:
            entry.config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                         fg=self.__loader.colorPalettes.getColor("boxFontUnSaved"))
            return

        entry.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                     fg=self.__loader.colorPalettes.getColor("boxFontNormal"))

        if num < 0:
           num = 0

        if num > 255:
           num = 255

        num   = self.checkKey(key)
        force = False

        if key == "frameNum":
            try:
                currentFrom = self.convertToNum(self.__rangeEntryVars[0].get())
            except:
                currentFrom = 0

            try:
                currentTo = self.convertToNum(self.__rangeEntryVars[1].get())
            except:
                currentTo = self.__numOfFrames - 1

            self.checkTheEntries(currentFrom, currentTo)

        elif key == "heightIndex":
            try:
                dHeigth = self.convertToNum(self.__dataElements["displayedHeight"]["entryVar"].get())
                if num > self.__height - dHeigth - 1: num = self.__height - dHeigth - 1
                force = True
            except:
                pass

        elif key == "speed+FIndex":
            try:
                fullNum  = bin(self.convertToNum(self.__dataElements["speed+FIndex"]["entryVar"].get())).replace("0b", "")
                fullNum  = (8 - len(fullNum)) * "0" + fullNum

                frameNum = int("0b" + fullNum[4:], 2)
                force    = True
                #self.__numOfFrames = 1
                self.__dataElements["frameNum"]["entryVar"].set("1")

                self.checkTheEntries(frameNum, frameNum)

            except:
                pass

        focusOut = False
        if str(event).split(" ")[0] == "<FocusOut":
           focusOut = True

        if   entryVal.get().startswith("%"):
             numStr = bin(num).replace("0b", "")

             if focusOut:
                 while len(numStr) < 8:
                     numStr = "0" + numStr

             numStr = "%" + numStr
        elif entryVal.get().startswith("$"):
             numStr = hex(num).replace("0x", "")

             if focusOut:
                 while len(numStr) < 2:
                     numStr = "0" + numStr

             numStr = "$" + numStr.upper()
        else:
             numStr = str(num)

        entryVal.set(numStr)
        entry.icursor(len(entryVal.get()))

        #print(entryVal.get(), was)
        dataNum = self.__keys.index(key) + 3
        if self.__data[dataNum] != entryVal.get() or force:
           self.__data[dataNum]  = entryVal.get()
           self.__changeData(self.__data)