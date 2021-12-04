from tkinter import *

class ChangeDrumsAndOrder:

    def __init__(self, loader, mainWindow, channelAttributes, sorter, rawData, removeDrums):
        self.__loader = loader
        self.__mainWindow = mainWindow

        self.__sorter = sorter
        self.__channelAttributes = channelAttributes
        self.__rawData = rawData

        if removeDrums == False:
            try:
                self.__drumData = self.__rawData[9]["joined"]
                if self.__drumData != "":
                    self.__drums = True
                else:
                    self.__drums = False
            except Exception as e:
                self.__drums = False
        else:
            self.__drums = False

        if self.__drums == False:
            self.__drumData = None

        self.dead = False
        self.__loader.stopThreads.append(self)

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
        self.__tinyFont = self.__fontManager.getFont(int(self.__fontSize*0.35), False, False, False)


        self.__screenSize = self.__loader.screenSize

        self.__sizes = (self.__screenSize[0] / 3, self.__screenSize[1]/3  - 40)
        self.__soundPlayer.playSound("Ask")

        from SubMenu import SubMenu

        self.__window = SubMenu(self.__loader, "drums", self.__sizes[0],
                                self.__sizes[1], None, self.__addElements, 2)

        self.dead = True

    def __closeWindow(self):
        self.dead = True
        if self.__drums == True:
            self.__saveDrums()
        self.__topLevelWindow.destroy()
        self.__loader.topLevels.remove(self.__topLevelWindow)

    def __saveDrums(self):
        tempDrumData = self.__drumData.split("\n")
        newLines = []

        for line in tempDrumData:
            line = line.split(" ")
            try:
                key = line[1]
                if key != "0":
                    val = self.__drumValues[key]
                    newKey = key
                    for item in self.__drumDict.keys():
                        GGG = self.__drumDict[item]
                        if GGG[0] == val:
                           newKey = str(GGG[1][0])
                           break

                    line[1] = newKey
            except:
                pass
            line = " ".join(line)
            newLines.append(line)

        self.__rawData[9]["joined"] = "\n".join(newLines)

    def __addElements(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()
        self.__topLevelWindow.protocol('WM_DELETE_WINDOW', self.__closeWindow)

        self.__songOrderFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"),
                                width = self.__sizes[0], height = self.__sizes[1]//3)
        self.__songOrderFrame.pack_propagate(False)
        self.__songOrderFrame.pack(side=TOP, anchor=N, fill=X)

        self.__drumFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"),
                                      width=self.__sizes[0], height=round(self.__sizes[1]/3*2))
        self.__drumFrame.pack_propagate(False)
        self.__drumFrame.pack(side=TOP, anchor=N, fill=X)

        from SpriteEditorListBox import SpriteEditorListBox

        self.__songOrderFrameHalf = Frame(self.__songOrderFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                width = self.__sizes[0]//2, height = self.__sizes[1]//2)
        self.__songOrderFrameHalf.pack_propagate(False)
        self.__songOrderFrameHalf.pack(side=LEFT, anchor=E, fill=Y)

        self.__drumFrameHalf = Frame(self.__drumFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                width = self.__sizes[0]//2, height = self.__sizes[1]//2)
        self.__drumFrameHalf.pack_propagate(False)
        self.__drumFrameHalf.pack(side=LEFT, anchor=E, fill=Y)

        self.__orderListBox = SpriteEditorListBox(self.__loader, self.__songOrderFrame, self.__miniFont)
        self.__drumListBox = SpriteEditorListBox(self.__loader, self.__drumFrame, self.__smallFont)

        self.__songOrderLabel = Label(self.__songOrderFrameHalf,
                                    text=self.__dictionaries.getWordFromCurrentLanguage("channelPrio"),
                                    font=self.__smallFont, fg=self.__colors.getColor("font"),
                                    bg=self.__colors.getColor("window")
                                    )

        self.__songOrderLabel.pack_propagate(False)
        self.__songOrderLabel.pack(side=TOP, anchor=N, fill=X)

        self.__drumLabel = Label(self.__drumFrameHalf,
                                    text=self.__dictionaries.getWordFromCurrentLanguage("drumSettings"),
                                    font=self.__smallFont, fg=self.__colors.getColor("font"),
                                    bg=self.__colors.getColor("window")
                                    )

        self.__drumLabel.pack_propagate(False)
        self.__drumLabel.pack(side=TOP, anchor=N, fill=X)

        self.__display = []

        for item in self.__sorter:
            self.__display.append(self.__channelAttributes[item[0]])
            self.__display[-1]["channelNum"] = item[0]
        self.__fillOrderListBox(0)

        self.__selectedOrderList = None
        self.__currentPoz = 0

        self.__label1 = Label(self.__songOrderFrameHalf,
                                    text=self.__dictionaries.getWordFromCurrentLanguage("drumSettings"),
                                    font=self.__tinyFont, fg=self.__colors.getColor("font"),
                                    bg=self.__colors.getColor("window")
                                    )

        self.__drumLabel.pack_propagate(False)
        self.__drumLabel.pack(side=TOP, anchor=N, fill=X)

        self.__buttonFrame1 = Frame(self.__songOrderFrameHalf, bg=self.__loader.colorPalettes.getColor("window"),
                                width = self.__sizes[0]//2, height = self.__sizes[1]//2)
        self.__buttonFrame1.pack_propagate(False)
        self.__buttonFrame1.pack(side=TOP, anchor=E, fill=BOTH)

        self.__buttonFrame1_1 = Frame(self.__buttonFrame1, bg=self.__loader.colorPalettes.getColor("window"),
                                width = self.__sizes[0]//4, height = self.__sizes[1]//2)
        self.__buttonFrame1_1.pack_propagate(False)
        self.__buttonFrame1_1.pack(side=LEFT, anchor=E, fill=Y)

        self.__buttonFrame1_2 = Frame(self.__buttonFrame1, bg=self.__loader.colorPalettes.getColor("window"),
                                width = self.__sizes[0]//4, height = self.__sizes[1]//2)
        self.__buttonFrame1_2.pack_propagate(False)
        self.__buttonFrame1_2.pack(side=LEFT, anchor=E, fill=Y)

        self.__moveUpButton = Button(self.__buttonFrame1_1, bg=self.__loader.colorPalettes.getColor("window"),
                                   text="<<", width=99999, font = self.__normalFont,
                                   state=DISABLED,
                                   command=self.__moveSelectedUp)

        self.__moveDownButton = Button(self.__buttonFrame1_2, bg=self.__loader.colorPalettes.getColor("window"),
                                   text=">>", width=99999, font = self.__normalFont,
                                   state=DISABLED,
                                   command=self.__moveSelectedDown)

        self.__moveUpButton.pack_propagate(False)
        self.__moveUpButton.pack(fill=BOTH)

        self.__moveDownButton.pack_propagate(False)
        self.__moveDownButton.pack(fill=BOTH)

        __drumNotes = {}
        if self.__drumData != None:
            drumList = self.__drumData.split("\n")
            for line in drumList:
                line = line.split(" ")
                try:
                    if line[1] not in __drumNotes:
                        __drumNotes[line[1]] = 1
                    else:
                        __drumNotes[line[1]]+= 1
                except:
                    pass

        try:
            del __drumNotes["0"]
        except:
            pass

        __drumNotes = sorted(__drumNotes.items(), key=lambda x: x[1], reverse=True)

        from copy import deepcopy

        #self.__tempDrumData = deepcopy(self.__drumData)


        from threading import Thread

        instruments = self.__loader.io.loadWholeText("config/midiPercuss.txt").split("\n")

        self.__instruments = {}
        for item in instruments:
            item = item.split("=")
            try:
                self.__instruments[item[0]] = item[1]
            except:
                pass

        per = 10

        self.__drumSetLine1 = Frame(self.__drumFrameHalf, bg=self.__loader.colorPalettes.getColor("window"),
                                width = self.__sizes[0]//2, height = self.__sizes[1]//per)
        self.__drumSetLine1.pack_propagate(False)
        self.__drumSetLine1.pack(side=TOP, anchor=N, fill=X)

        self.__drumSetLine1_1 = Frame(self.__drumSetLine1, bg=self.__loader.colorPalettes.getColor("window"),
                                width = self.__sizes[0]//4, height = self.__sizes[1]//per)
        self.__drumSetLine1_1.pack_propagate(False)
        self.__drumSetLine1_1.pack(side=LEFT, anchor=E, fill=Y)

        self.__drumSetLine1_2 = Frame(self.__drumSetLine1, bg=self.__loader.colorPalettes.getColor("window"),
                                width = self.__sizes[0]//4, height = self.__sizes[1]//per)
        self.__drumSetLine1_2.pack_propagate(False)
        self.__drumSetLine1_2.pack(side=LEFT, anchor=E, fill=Y)

        self.__drumSetLine2 = Frame(self.__drumFrameHalf, bg=self.__loader.colorPalettes.getColor("window"),
                                width = self.__sizes[0]//2, height = self.__sizes[1])
        self.__drumSetLine2.pack_propagate(False)
        self.__drumSetLine2.pack(side=TOP, anchor=N, fill=BOTH)

        self.__drumSetLine2_1 = Frame(self.__drumSetLine2, bg=self.__loader.colorPalettes.getColor("window"),
                                width = self.__sizes[0]//4, height = self.__sizes[1]//per)
        self.__drumSetLine2_1.pack_propagate(False)
        self.__drumSetLine2_1.pack(side=LEFT, anchor=E, fill=Y)

        self.__drumSetLine2_1_1 = Frame(self.__drumSetLine2_1, bg=self.__loader.colorPalettes.getColor("window"),
                                width = self.__sizes[0]//4, height = self.__sizes[1]//per)
        self.__drumSetLine2_1_1.pack_propagate(False)
        self.__drumSetLine2_1_1.pack(side=TOP, anchor=E, fill=X)

        self.__drumSetLine2_2 = Frame(self.__drumSetLine2, bg=self.__loader.colorPalettes.getColor("window"),
                                width = self.__sizes[0]//4, height = self.__sizes[1])
        self.__drumSetLine2_2.pack_propagate(False)
        self.__drumSetLine2_2.pack(side=LEFT, anchor=E, fill=Y)

        self.__midiLabel = Label(self.__drumSetLine1_1,
                                    text=self.__dictionaries.getWordFromCurrentLanguage("midiInstrument"),
                                    font=self.__miniFont, fg=self.__colors.getColor("font"),
                                    bg=self.__colors.getColor("window")
                                    )

        self.__midiLabel.pack_propagate(False)
        self.__midiLabel.pack(side=LEFT, fill=BOTH)

        self.__atariLabel = Label(self.__drumSetLine2_1_1,
                                    text=self.__dictionaries.getWordFromCurrentLanguage("atariInstrument"),
                                    font=self.__miniFont, fg=self.__colors.getColor("font"),
                                    bg=self.__colors.getColor("window")
                                    )

        self.__atariLabel.pack_propagate(False)
        self.__atariLabel.pack(side=LEFT, fill=BOTH)


        self.__instrumentName = StringVar()
        self.__instrumentEntry = Entry(self.__drumSetLine1_2,
                                       textvariable = self.__instrumentName, width=99999999,
                                       font=self.__miniFont, fg=self.__colors.getColor("boxFontNormal"),
                                       bg=self.__colors.getColor("boxBackNormal"),
                                       state = DISABLED, justify = CENTER
                                       )

        self.__instrumentEntry.pack_propagate(False)
        self.__instrumentEntry.pack(side=LEFT, fill=BOTH)

        self.__drumAlias = {}
        self.__drumDict = {
            89: [
                "Drum",
                [35, 36, 41, 43, 45, 47, 48, 50, 64, 65, 66, 78, 79]
            ],
            90: [
                "High Hat - 1",
                [42, 44, 51, 73, 76]
            ],
            91: [
                "High Hat - 2",
                [46, 52, 55, 74, 77]
            ],
            92: [
                "Snare",
                [38, 54, 56, 57, 69, 70, 75]
            ],
            93: [
                "Horn",
                [37, 53, 59]
            ],
            94: [
                "Buzz - 1",
                [39, 48, 57, 60, 62, 67, 71, 80]
            ],
            95: [
                "Buzz - 2",
                [40, 49, 61, 63, 68, 72, 81]
            ]
        }

        __drumNames = []
        for note in self.__drumDict.keys():
            __drumNames.append(self.__drumDict[note][0])

        self.__drumValues = {}
        for item in __drumNotes:
            item = item[0]
            for num in self.__drumDict.keys():
                if int(item) in self.__drumDict[num][1]:
                    self.__drumValues[item] = self.__drumDict[num][0]
                    break

        #print(self.__drumNames)
        #print(self.__drumValues)

        self.__optionSelected = None

        self.__optionBox = Listbox(self.__drumSetLine2_2,
                                   font=self.__miniFont, fg=self.__colors.getColor("boxFontNormal"),
                                   bg=self.__colors.getColor("boxBackNormal"),
                                   justify=CENTER, width=9999999, height = len(__drumNames),
                                   selectmode=BROWSE,
                                   exportselection=False
                                   )
        for item in __drumNames:
            self.__optionBox.insert(END, item)

        self.__optionBox.pack_propagate(False)
        self.__optionBox.pack(side=TOP, fill=BOTH)

        self.__selectedDrumList = None
        if self.__drums == True:
            self.__fillDrumList(__drumNotes)
        else:
            self.__drumListBox.disableBox()
            self.__optionBox.config(state=DISABLED)

        self.__exitButton = Button(self.__drumSetLine2_1,
                                   font=self.__miniFont, fg=self.__colors.getColor("font"),
                                   bg=self.__colors.getColor("window"),
                                   justify=CENTER, width=9999999,
                                   command = self.__closeWindow, text = self.__dictionaries.getWordFromCurrentLanguage("ok")
                                   )

        self.__exitButton.pack_propagate(False)
        self.__exitButton.pack(side=BOTTOM, anchor = S, fill=X)


        t = Thread(target = self.__checker)
        t.daemon = True
        t.start()

    def __fillDrumList(self, drumNotes):
        listBox = self.__drumListBox.getListBox()
        listBox.selection_clear(0, END)

        listBox.delete(0, END)
        for item in drumNotes:
            string = str(item[0])+" ("+str(item[1])+")"
            listBox.insert(END, string)

        listBox.selection_set(0)
        self.__selectedDrumList = None

    def __moveSelectedUp(self):
        if self.__selectedOrderList == self.__orderListBox.getSelected():
            self.__moveSelected(self.__currentPoz-1)

    def __moveSelectedDown(self):
        if self.__selectedOrderList == self.__orderListBox.getSelected():
            self.__moveSelected(self.__currentPoz+1)

    def __moveSelected(self, poz):
        from copy import deepcopy

        oneToCutOut = deepcopy(self.__display[self.__currentPoz])
        self.__display.pop(self.__currentPoz)
        self.__display.insert(poz, oneToCutOut)

        oneToCutOut2 = deepcopy(self.__sorter[self.__currentPoz])
        self.__sorter.pop(self.__currentPoz)
        self.__sorter.insert(poz, oneToCutOut2)

        self.__fillOrderListBox(poz)

    def __checker(self):
        from time import sleep

        while self.dead == False:
            if self.__selectedOrderList != self.__orderListBox.getSelected():
                self.__selectedOrderList = self.__orderListBox.getSelected()
                key = int(self.__selectedOrderList.split(":")[0])
                for item in self.__display:
                    if item["channelNum"] == key or item["channelNum"] == str(key):
                        self.__currentPoz = self.__display.index(item)
                        break
                self.__moveUpButton.config(state=NORMAL)
                self.__moveDownButton.config(state=NORMAL)
                if self.__currentPoz == 0:
                   self.__moveUpButton.config(state = DISABLED)
                if self.__currentPoz == len(self.__display)-1:
                    self.__moveDownButton.config(state=DISABLED)
            if self.__drums == True:
                if self.__selectedDrumList != self.__drumListBox.getSelected():
                    self.__selectedDrumList = self.__drumListBox.getSelected()

                    key = self.__selectedDrumList.split(" ")[0]
                    try:
                        self.__instrumentName.set(self.__instruments[key])
                    except:
                        self.__instrumentName.set("???")

                    fuck = None
                    try:
                        fuck = self.__drumValues[key]
                    except:
                        for d in self.__drumDict.keys():
                            if int(key) in self.__drumDict[d][1]:
                                fuck = self.__drumDict[d][0]
                                break

                    if fuck != None:
                        for num in range(0, len(self.__drumDict)):
                            self.__optionBox.selection_clear(0, END)
                            self.__optionBox.selection_set(num)
                            if self.__optionBox.get(self.__optionBox.curselection()) == fuck:
                                break
    
                if self.__optionSelected != self.__optionBox.get(self.__optionBox.curselection()):
                    self.__optionSelected = self.__optionBox.get(self.__optionBox.curselection())
                    drumNote = self.__selectedDrumList.split(" ")[0]
                    self.__drumValues[drumNote] = self.__optionSelected

    def __fillOrderListBox(self, select):
        listBox = self.__orderListBox.getListBox()
        listBox.selection_clear(0, END)

        listBox.delete(0, END)
        for item in self.__display:
            string = str(item["channelNum"]) + ": tiaChannel("+str(item["dominantTiaChannel"])+"), "+ \
                     "priority("+str(round(item["priority"], 2))+")"

            listBox.insert(END, string)

        listBox.selection_set(select)
        self.__selectedOrderList = None
