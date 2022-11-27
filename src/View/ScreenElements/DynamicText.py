from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from time import sleep

from ScreenSetterFrameBase import ScreenSetterFrameBase

class DynamicText:

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

        itWasHash = False
        if self.__data[2] == "#": itWasHash = True

        self.__setterBase = ScreenSetterFrameBase(loader, baseFrame, data, self.__name, changeName, self.dead,
                                                  itemNames)

        self.__loadVars()
        self.__addElements()

        if itWasHash == True:
            self.__changeData(self.__data)

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

    def __addElements(self):
        self.__uniqueFrame = Frame(self.__baseFrame, width=self.__w,
                                    bg=self.__loader.colorPalettes.getColor("window"),
                                    height=self.__h)

        self.__uniqueFrame.pack_propagate(False)
        self.__uniqueFrame.pack(side=TOP, anchor=N, fill=X)

        thisH = self.__h // 3.5
        thisW = self.__w // 5

        dataFrames = []
        counter = 12

        dataVars = self.__data[2:14]
        colors   = [self.__data[14], self.__data[15]]
        #gradient = self.__data[16]

        #colors = [["blue", "red", "yellow", 'white'],
        #          ["purple", "green", "black", "gray"]]

        for num in range(0, round(thisW * thisH // 3)):
            if counter == 0: break

            mainFrame = Frame(self.__uniqueFrame, width=thisW,
                        bg=self.__loader.colorPalettes.getColor("window"),
                        height=thisH)

            mainFrame.pack_propagate(False)
            mainFrame.pack(side=LEFT, anchor=E, fill=Y)

            for num2 in range(0, 3):
                if counter == 0: break

                # fuckColor = colors[num%2][num2]

                frame = Frame(mainFrame, width=thisW,
                        bg=self.__loader.colorPalettes.getColor("window"),
                        #bg=fuckColor,
                        height=thisH)

                frame.pack_propagate(False)
                frame.pack(side=TOP, anchor=N, fill=X)

                dataFrames.append(frame)
                counter -= 1

        self.__dataListBoxes = []

        for num in range(0, 12):
            self.__dataListBoxes.append({})

            label = Label(dataFrames[num],
                                        text=self.__dictionaries.getWordFromCurrentLanguage("dataVar")+":",
                                        font=self.__smallFont, fg=self.__colors.getColor("font"),
                                        bg=self.__colors.getColor("window"), justify=CENTER
                                        )

            label.pack_propagate(False)
            label.pack(side=TOP, anchor=CENTER, fill=BOTH)

            scrollBar = Scrollbar(dataFrames[num])
            listBox = Listbox(dataFrames[num], width=100000,
                                         height=1000, name = "dataListBox_"+str(num),
                                         yscrollcommand=scrollBar.set,
                                         selectmode=BROWSE,
                                         exportselection=False,
                                         font=self.__miniFont,
                                         justify=CENTER
                                         )

            listBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
            listBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
            listBox.pack_propagate(False)

            scrollBar.pack(side=RIGHT, anchor=W, fill=Y)
            listBox.pack(side=LEFT, anchor=W, fill=BOTH)

            scrollBar.config(command=listBox.yview)

            self.__dataListBoxes[num]["garbage"] = []
            self.__dataListBoxes[num]["garbage"].append(label)
            self.__dataListBoxes[num]["garbage"].append(scrollBar)
            self.__dataListBoxes[num]["listBox"] = listBox

            for item in self.__byteVars:
                self.__dataListBoxes[num]["listBox"].insert(END, item)

            if dataVars[num] == "#":
               self.__data[2 + num] = self.__byteVars[0].split("::")[1]

            selector = 0
            for itemNum in range(0, len(self.__byteVars)):
                if self.__byteVars[itemNum].split("::")[1] == self.__data[2 + num]:
                   selector = itemNum
                   break

            self.__dataListBoxes[num]["listBox"].select_set(selector)
            self.__dataListBoxes[num]["listBox"].yview(selector)
            self.__dataListBoxes[num]["lastSelected"] = self.__byteVars[selector].split("::")[1]

            listBox.bind("<ButtonRelease-1>", self.__changeDataListBox)
            listBox.bind("<KeyRelease-Up>", self.__changeDataListBox)
            listBox.bind("<KeyRelease-Down>", self.__changeDataListBox)

        cFrame = Frame(self.__uniqueFrame, width=thisW,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              height=thisH)

        cFrame.pack_propagate(False)
        cFrame.pack(side=LEFT, anchor=E, fill=Y)

        from HexEntry import HexEntry
        self.__fuckinColors = ["$16", "$00"]

        self.__colorData = []
        for num in range(0, 2):
            self.__colorData.append({})
            frame = Frame(cFrame, width=thisW,
                           bg=self.__loader.colorPalettes.getColor("window"),
                           height=round(thisH*1.5))

            frame.pack_propagate(False)
            frame.pack(side=TOP, anchor=N, fill=X)

            self.__colorData[num]["garbage"] = []
            self.__colorData[num]["garbage"].append(frame)

            texts = ["textColor", "backColor"]

            label = Label(frame,
                                        text=self.__dictionaries.getWordFromCurrentLanguage(texts[num])+":",
                                        font=self.__smallFont, fg=self.__colors.getColor("font"),
                                        bg=self.__colors.getColor("window"), justify=CENTER
                                        )

            label.pack_propagate(False)
            label.pack(side=TOP, anchor=CENTER, fill=X)

            option = IntVar()
            self.__colorData[num]["option"] = option
            color  = colors[num]

            optionButton1 = Radiobutton(frame, width=99999,
                                              name = "button" + str(num) + "_C",
                                              text=self.__dictionaries.getWordFromCurrentLanguage("constant"),
                                              bg=self.__colors.getColor("window"),
                                              fg=self.__colors.getColor("font"),
                                              justify=LEFT, font=self.__smallFont,
                                              variable=option,
                                              activebackground=self.__colors.getColor("highLight"),
                                              value=1
                                              )
            optionButton1.bind("<ButtonRelease-1>", self.__changeColorSettings)
            optionButton1.pack_propagate(False)
            optionButton1.pack(fill=X, side=TOP, anchor=N)

            self.__colorData[num]["constantButton"] = optionButton1

            if self.isItHex(color):
               self.__fuckinColors[num] = color
               option.set(1)
            else:
               option.set(2)

            constantHex = HexEntry(self.__loader, frame, self.__colors, self.__colorDict,
                                   self.__smallFont, self.__fuckinColors, num, None, self.__changeHex)

            self.__colorData[num]["hexEntry"] = constantHex
            optionButton2 = Radiobutton(frame, width=99999,
                                              name = "button" + str(num) + "_V",
                                              text=self.__dictionaries.getWordFromCurrentLanguage("variable"),
                                              bg=self.__colors.getColor("window"),
                                              fg=self.__colors.getColor("font"),
                                              justify=LEFT, font=self.__smallFont,
                                              variable=option,
                                              activebackground=self.__colors.getColor("highLight"),
                                              value=2
                                              )
            optionButton2.bind("<ButtonRelease-1>", self.__changeColorSettings)
            optionButton2.pack_propagate(False)
            optionButton2.pack(fill=X, side=TOP, anchor=N)
            self.__colorData[num]["variableButton"] = optionButton2

            scrollBar = Scrollbar(frame)
            listBox = Listbox(frame, width=100000,
                                         height=1000, name = "colorListBox_"+str(num),
                                         yscrollcommand=scrollBar.set,
                                         selectmode=BROWSE,
                                         exportselection=False,
                                         font=self.__miniFont,
                                         justify=CENTER
                                         )

            listBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
            listBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
            listBox.pack_propagate(False)

            scrollBar.pack(side=RIGHT, anchor=W, fill=Y)
            listBox.pack(side=LEFT, anchor=W, fill=BOTH)

            scrollBar.config(command=listBox.yview)
            self.__colorData[num]["listBox"] = listBox
            self.__colorData[num]["garbage"].append(scrollBar)

            for item in self.__nibbleVars:
                listBox.insert(END, item)

            if option.get() == 1:
               listBox.config(state = DISABLED)
               self.__colorData[num]["lastSelected"] = self.__nibbleVars[0].split("::")[1]
            else:
               constantHex.changeState(DISABLED)
               selector = 0
               for itemNum in range(0, len(self.__nibbleVars)):
                   if color == self.__nibbleVars[itemNum].split("::")[1]:
                      selector = itemNum
                      break

               listBox.select_set(selector)
               listBox.yview(selector)
               self.__colorData[num]["lastSelected"] = self.__nibbleVars[selector].split("::")[1]
            listBox.bind("<ButtonRelease-1>", self.__changeColorListBox)
            listBox.bind("<KeyRelease-Up>", self.__changeColorListBox)
            listBox.bind("<KeyRelease-Down>", self.__changeColorListBox)

        # from GradientFrame import GradientFrame
        # self.__gradientFrame = GradientFrame(self.__loader, self.__uniqueFrame,
        #                                      self.__changeData, self.__h, self.__data, self.dead, 8, "small", 16)
    def __changeColorListBox(self, event):
        name = str(event.widget).split(".")[-1]
        num  = int(name.split("_")[1])

        listBox         = self.__colorData[num]["listBox"]
        lastSelected    = self.__colorData[num]["lastSelected"]
        currentSelected = self.__nibbleVars[listBox.curselection()[0]].split("::")[1]

        if lastSelected != currentSelected:
           self.__data[14 + num] = currentSelected
           self.__changeData(self.__data)

    def __changeDataListBox(self, event):
        name = str(event.widget).split(".")[-1]
        num  = int(name.split("_")[1])

        listBox         = self.__dataListBoxes[num]["listBox"]
        lastSelected    = self.__dataListBoxes[num]["lastSelected"]
        currentSelected = self.__byteVars[listBox.curselection()[0]].split("::")[1]

        if lastSelected != currentSelected:
           self.__data[2 + num] = currentSelected
           self.__changeData(self.__data)

    def __changeColorSettings(self, event):
        name = str(event.widget).split(".")[-1]
        num = int(name[6])
        """
        names = \
            {
            "C": "constantButton", "V": "variableButton"
            }
        typ = names[name[8]]
        """
        # button = self.__colorData[num][typ]
        # value   = self.__colorData[num]["option"].get()

        entry   = self.__colorData[num]["hexEntry"]
        listBox = self.__colorData[num]["listBox"]
        last    = self.__colorData[num]["lastSelected"]

        if name[8] == "C":
           entry.changeState(NORMAL)
           listBox.config(state = DISABLED)

           self.__data[14 + num] = entry.getValue()
           self.__changeData(self.__data)

        else:
            entry.changeState(DISABLED)
            listBox.config(state=NORMAL)

            selector = 0
            listBox.select_clear(0, END)
            for itemNum in range(0, len(self.__nibbleVars)):
                if last == self.__nibbleVars[itemNum].split("::")[1]:
                    selector = itemNum
                    break

            listBox.select_set(selector)
            listBox.yview(selector)
            self.__data[14+num] = self.__nibbleVars[selector].split("::")[1]
            self.__changeData(self.__data)

    def __changeHex(self, event):
        num = 0
        for itemNum in range(0, 2):
            entry = self.__colorData[itemNum]["hexEntry"].getEntry()
            if entry == event.widget:
                num = itemNum
                break

        if self.__colorData[num]["option"] == 2: return
        hexEntry = self.__colorData[num]["hexEntry"]
        self.__data[14 + num] = hexEntry.getValue()
        self.__changeData(self.__data)


    def isItNum(self, num):
        try:
            num = int(num)
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