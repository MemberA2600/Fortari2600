from SubMenu import SubMenu
from SubMenuLabel import SubMenuLabel
from SubMenuFrame import SubMenuFrame
from tkinter import *
import re
from time import sleep
from threading import Thread

class MusicComposer:

    def __init__(self, loader, mainWindow, tiaScreens):
        self.__loader = loader
        self.__mainWindow = mainWindow

        self.firstLoad = True
        self.dead = False
        self.changed = False

        self.__virtualMemory = self.__loader.virtualMemory
        self.__loader.stopThreads.append(self)
        self.__colorDict = self.__loader.colorDict

        self.__caller = 0
        self.forceShit = False
        self.reset = False

        self.__choosenOne = None
        self.__screenMax = 0
        self.__maxChannels = 999

        self.__calculatingThread = None
        self.__frames = {}

        self.__bankEntries = {
            1: None,
            2: None,
        }

        self.__errorCounters = {
            "selected": 0,
            "beats": 0,
            "fadeOut": 0,
            "toneLenght": 0,
            "corrector": 0,
            "bank1": 0,
            "bank2": 0,
            "maxChannels": 0,
        }

        self.__pressed = {"1": False, "3": False}

        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs
        self.__fontManager = self.__loader.fontManager
        self.__fontSize = int(self.__screenSize[0]/1300 * self.__screenSize[1]/1050*14)
        self.__colors = self.__loader.colorPalettes
        self.__colorDict = self.__loader.colorDict
        self.__piaNotes = self.__loader.piaNotes
        self.__io = self.__loader.io

        self.__picturePath = None
        self.__banks = [3,4]
        self.__variables = [None, None, None, None]
        self.__colorConstans = ["$18", "$00", "$00", "$44", "$34", "$14"]


        self.focused = None
        self.__screenSize = self.__loader.screenSize

        self.__numberBuffer = []

        self.__func = None
        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__bigFont = self.__fontManager.getFont(int(self.__fontSize*1.10), False, False, False)
        self.__tinyFont = self.__fontManager.getFont(int(self.__fontSize*0.35), False, False, False)
        self.__tinyFont2 = self.__fontManager.getFont(int(self.__fontSize*0.50), False, False, False)


        if tiaScreens == None:
            from TiaScreens import TiaScreens
            self.__tiaScreens = TiaScreens(self.__loader)

        if self.__loader.virtualMemory.kernel == "common":
            self.__func = self.__addElementsCommon

        self.__ctrl = False
        self.__draw = 0

        self.__sizes = {
            "common": [self.__screenSize[0] / 1.10, self.__screenSize[1]/1.10  - 35]
        }

        self.__alreadyDone = False

        self.__window = SubMenu(self.__loader, "music", self.__sizes["common"][0],
                                self.__sizes["common"][1], None, self.__func, 1)

        self.dead = True


    def __errorSum(self):
        s = 0

        for key in self.__errorCounters:
            s += self.__errorCounters[key]

        return(s)

    def checker(self):
        from time import sleep
        while(self.dead==False and self.__loader.mainWindow.dead == False
        ):
            try:
                if self.__runningThreads == 0 and len(self.__piaNoteTable) > 0:

                    self.__ButtonInsertBefore.config(state=NORMAL)
                    self.__ButtonInsertAfter.config(state=NORMAL)
                    self.__importButton.config(state=NORMAL)
                    for button in self.__channelButtons:
                        button.enable()
                    self.__dividerSetter.enable()
                    self.__fadeOutSetter.enable()
                    self.__frameLenSetter.enable()
                    self.__correctorSetter.enable()
                    #self.__maxChannelsSetter.enable()

                    self.__IOButtons()
                    if self.reset == True:
                        self.__channelNum[0] = 1
                        self.__currentSelected.set(0)
                        self.reset = False


                    if self.__channelNum[0] != self.__tiaScreens.currentChannel:
                        self.__tiaScreens.currentChannel = self.__channelNum[0]
                        self.reColorAll()
                    self.checkScreenSetter()

            except Exception as e:
                print(str(e))
                self.__loader.logger.errorLog(e)


            sleep(0.4)

    def reColorAll(self):
        for name in self.__piaNoteTable:
            X = int(name.split(",")[0])
            Y = int(name.split(",")[1])

            self.colorButton(X, Y, self.__piaNoteTable[name])

    def __IOButtons(self):
        self.__openButton.changeState(True)
        self.__saveButton.changeState(False)
        self.__testingButton.changeState(False)
        self.__summaButton.changeState(False)
        self.__copyButton.changeState(False)
        self.__pasteButton.changeState(False)
        self.__eraseButton.changeState(False)

        if self.__tiaScreens.isThisScreenEmpty() == False:
            self.__eraseButton.changeState(True)
            self.__copyButton.changeState(True)

        if self.__tiaScreens.screenBuffer != None:
            self.__pasteButton.changeState(True)

        if (self.__io.checkIfValidFileName(self.__songTitle.get()) == True and
            self.__io.checkIfValidFileName(self.__artistName.get())) and self.__errorSum() == 0:
                self.__testingButton.changeState(self.__tiaScreens.isThereAnyNote())
                self.__summaButton.changeState(self.__tiaScreens.isThereAnyNote())


        if self.changed == True:
            if (self.__io.checkIfValidFileName(self.__songTitle.get()) == True and
                    self.__io.checkIfValidFileName(self.__artistName.get())) and self.__errorSum() == 0:
                self.__saveButton.changeState(True)


    def checkScreenSetter(self):

        if (self.__currentSelected.get() != str(self.__tiaScreens.currentScreen+1) or
            self.__tiaScreens.screenMax != self.__screenMax or
            self.forceShit == True):

            self.forceShit = False

            self.__currentSelected.set(str(self.__tiaScreens.currentScreen+1))
            self.__screenMax = self.__tiaScreens.screenMax

            if self.__tiaScreens.screenMax > 0:

                self.__SetSelectedEntry.config(state=NORMAL)
                if self.__tiaScreens.currentScreen>0:
                    self.__ButtonPrev.config(state=NORMAL)
                else:
                    self.__ButtonPrev.config(state=DISABLED)

                if self.__tiaScreens.currentScreen<self.__screenMax:
                    self.__ButtonNext.config(state=NORMAL)
                else:
                    self.__ButtonNext.config(state=DISABLED)
                self.__deleteCurrentButton.config(state=NORMAL)


            else:
                self.__SetSelectedEntry.config(state=DISABLED)
                self.__ButtonPrev.config(state=DISABLED)
                self.__ButtonNext.config(state=DISABLED)
                self.__deleteCurrentButton.config(state=DISABLED)



    def __addElementsCommon(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()

        self.__editorFrame = Frame(self.__topLevelWindow,
                                   height=round(self.__topLevel.getTopLevelDimensions()[1]),
                                   bg=self.__colors.getColor("window"))
        self.__editorFrame.pack_propagate(False)
        self.__editorFrame.pack(side=TOP, fill=X)

        self.__selectedChannelFrame = Frame(self.__editorFrame,
                                   height=round(self.__topLevel.getTopLevelDimensions()[1]*0.065),
                                   bg=self.__colors.getColor("window"))
        self.__selectedChannelFrame.pack_propagate(False)
        self.__selectedChannelFrame.pack(side=TOP, fill=X)

        self.__selectorForReal = Frame(self.__selectedChannelFrame,
                                   width=round(self.__topLevel.getTopLevelDimensions()[0]*0.3),
                                   bg=self.__colors.getColor("window"))
        self.__selectorForReal.pack_propagate(False)
        self.__selectorForReal.pack(side=LEFT, fill=Y)

        self.__selectorLabel = Label(self.__selectorForReal,
                                     width=len(self.__dictionaries.getWordFromCurrentLanguage("selectChannel"))+1,
                                     bg = self.__colors.getColor("window"),
                                     fg = self.__colors.getColor("font"),
                                     text = self.__dictionaries.getWordFromCurrentLanguage("selectChannel"),
                                     font = self.__normalFont,
                                     justify=LEFT
                                     )
        self.__selectorLabel.pack(side=LEFT, fill=Y, anchor=W)

        self.__selectorButtons = Frame(self.__selectorForReal,
                                   width=round(self.__topLevel.getTopLevelDimensions()[0]*0.25),
                                   bg=self.__colors.getColor("window"))
        self.__selectorButtons.pack_propagate(False)
        self.__selectorButtons.pack(side=LEFT, fill=Y)

        self.__channelNum = [1]
        from ChannelChangerButton import ChannelChangerButton

        self.__channelButtons = []
        for num in range(1,5):
            __channel1Button = ChannelChangerButton(self.__loader, self.__bigFont, num,
                                           self.__channelNum,
                                           round(self.__topLevel.getTopLevelDimensions()[0]*0.002),
                                           self.__selectorButtons)
            self.__channelButtons.append(__channel1Button)


        self.__channelFrame = Frame(self.__editorFrame, height=round(self.__topLevel.getTopLevelDimensions()[1]*0.75),
                                    bg = self.__colors.getColor("window"),
                                    width=self.__topLevel.getTopLevelDimensions()[0])
        self.__channelFrame.pack_propagate(False)
        self.__channelFrame.pack(side=TOP, anchor=N, fill=X)

        self.__h = round(self.__topLevel.getTopLevelDimensions()[1]*0.60*0.66)

        self.__trembleChannel = Frame(self.__channelFrame, height=self.__h,
                                    bg = self.__colors.getColor("window"),
                                      width=self.__topLevel.getTopLevelDimensions()[0]
                                      )
        self.__trembleChannel.pack_propagate(False)
        self.__trembleChannel.pack(side=TOP, anchor=N, fill=X)

        """
        self.__XXX = Frame(self.__channelFrame, height=round(self.__h*0.01),
                                    bg = self.__colors.getColor("window"))
        self.__XXX.pack_propagate(False)
        self.__XXX.pack(side=TOP, anchor=N, fill=X)
        """

        self.__bassNUM = 0.7

        self.__bassChannel = Frame(self.__channelFrame, height=round(self.__h*self.__bassNUM),
                                    bg = self.__colors.getColor("window"),
                                   width=self.__topLevel.getTopLevelDimensions()[0])
        self.__bassChannel.pack_propagate(False)
        self.__bassChannel.pack(side=TOP, anchor=N, fill=X)

        self.__drumNUM = 0.35

        self.__drumChannel = Frame(self.__channelFrame, height=round(self.__h*self.__drumNUM),
                                    bg = self.__colors.getColor("window"),
                                   width=self.__topLevel.getTopLevelDimensions()[0])
        self.__drumChannel.pack_propagate(False)
        self.__drumChannel.pack(side=TOP, anchor=N, fill=X)

        #self.__bass = True
        self.__buzz = 1
        self.__correctNotes = 2 # Can be 0-2
        self.__fadeOutLen = 1
        self.__dividerLen = 4   # Has effect over 2, goes to 4
        self.__vibratio = 1
        self.__vibratio2 = 1
        self.__frameLen = 2

        self.__piaNoteTable = {}

        self.__patterns = {}
        self.createPattenrs()

        self.__runningThreads = 5

        t1 = Thread(target=self.__drawField, args=(self.__trembleChannel, self.__h,
                                                   69, 31, self.__patterns["tremble"],
                                                   "tremble"))
        t1.daemon = True
        t1.start()

        t2 = Thread(target=self.__drawField, args=(self.__bassChannel, round(self.__h*self.__bassNUM),
                                                   30, 2, self.__patterns["bass"],
                                                   "bass"))
        t2.daemon = True
        t2.start()

        t3 = Thread(target=self.__drawDrums, args=(self.__drumChannel, round(self.__h*self.__drumNUM)))
        t3.daemon = True
        t3.start()

        t4 = Thread(target=self.drawAllTheOthers)
        t4.daemon = True
        t4.start()

        self.__bottomFrame = Frame(self.__editorFrame,
                                   height=99999,
                                   bg=self.__colors.getColor("window"))
        self.__bottomFrame.pack_propagate(False)
        self.__bottomFrame.pack(side=TOP, fill=BOTH)

        t5 = Thread(target=self.drawBottom)
        t5.daemon = True
        t5.start()

        t99 = Thread(target=self.checker)
        t99.daemon = True
        t99.start()

        self.__topLevelWindow.bind("<KeyPress-Control_L>", self.shiftON)
        self.__topLevelWindow.bind("<KeyRelease-Control_L>", self.shiftOff)
        self.__topLevelWindow.bind("<KeyPress-Control_R>", self.shiftON)
        self.__topLevelWindow.bind("<KeyRelease-Control_R>", self.shiftOff)
        #self.__topLevelWindow.bind('<ButtonPress-1>', self.pressed)
        #self.__topLevelWindow.bind('<ButtonRelease-1>', self.released)
        #self.__topLevelWindow.bind('<ButtonPress-3>', self.pressed)
        #self.__topLevelWindow.bind('<ButtonRelease-3>', self.released)
        self.__topLevelWindow.bind("<Button-2>", self.button2)
        self.__topLevelWindow.bind("<KeyPress>", self.pressedNumber)

        """
    def pressed(self, event):
        self.__pressed[str(event.num)] = True

    def released(self, event):
        self.__pressed[str(event.num)] = False
        """

    def drawBottom(self):

        self.__bottomFrame1 = Frame(self.__bottomFrame,
                                   width=round(self.__topLevel.getTopLevelDimensions()[0]*0.5),
                                    height=9999,
                                   bg=self.__colors.getColor("window"))
        self.__bottomFrame1.pack_propagate(False)
        self.__bottomFrame1.pack(side=LEFT, fill=Y)

        self.__artistName = StringVar()
        self.__artistName.set("Stellazy")

        self.__songTitle = StringVar()
        self.__songTitle.set("'til my ears bleed pixels")

        from SongInput import SongInput

        self.__artistEntry = SongInput(self.__loader, self.__bottomFrame1,
                                       round(self.__topLevel.getTopLevelDimensions()[0] * 0.5),
                                       round(self.__topLevel.getTopLevelDimensions()[1] * 0.03),
                                       "artist", self.__artistName, self.__smallFont,
                                       self.focusIn, self.focusOut
                                       )

        self.__songEntry = SongInput(self.__loader, self.__bottomFrame1,
                                       round(self.__topLevel.getTopLevelDimensions()[0] * 0.5),
                                       round(self.__topLevel.getTopLevelDimensions()[1] * 0.03),
                                       "title", self.__songTitle, self.__smallFont,
                                     self.focusIn, self.focusOut
                                     )


        self.__buttonFrame = Frame(self.__bottomFrame1,
                                   height=round(self.__topLevel.getTopLevelDimensions()[1]*0.05),
                                    width=9999,
                                   bg=self.__colors.getColor("window"))
        self.__buttonFrame.pack_propagate(False)
        self.__buttonFrame.pack(side=TOP, fill=X)

        from MCButton import MCButton

        w = round(self.__topLevel.getTopLevelDimensions()[0] * 0.065)

        self.__summaButton = MCButton(self.__loader, self.__buttonFrame, "sum", w, self.__justBytesThread)
        self.__testingButton = MCButton(self.__loader, self.__buttonFrame, "stella", w, self.__testingCurrent)
        self.__saveButton = MCButton(self.__loader, self.__buttonFrame, "save", w, self.__saveDataToFile)
        self.__openButton = MCButton(self.__loader, self.__buttonFrame, "open", w, self.__openFile)

        self.__bankLabelText = StringVar()
        self.__bankLabel = Label(self.__buttonFrame, textvariable = self.__bankLabelText,
                                 width=999999, font = self.__smallFont,
                                 bg = self.__colors.getColor("window"),
                                 fg = self.__colors.getColor("font"))

        self.__bankLabel.pack_propagate(False)
        self.__bankLabel.pack(side=RIGHT, fill=BOTH)

        self.__setBankLabelText([0,0])

        self.__musicROM = IntVar()
        self.__musicROM.set(0)

        self.__buttonFrame2 = Frame(self.__bottomFrame1,
                                   height=round(self.__topLevel.getTopLevelDimensions()[1]*0.05),
                                    width=9999,
                                   bg=self.__colors.getColor("window"))
        self.__buttonFrame2.pack_propagate(False)
        self.__buttonFrame2.pack(side=TOP, fill=X)

        self.__eraseButton = MCButton(self.__loader, self.__buttonFrame2, "erase", w, self.__eraseScreen)
        self.__pasteButton = MCButton(self.__loader, self.__buttonFrame2, "paste", w, self.__pasteScreen)
        self.__copyButton = MCButton(self.__loader, self.__buttonFrame2, "copy", w, self.__copyScreen)

        self.__ignoreFrame = Frame(self.__buttonFrame2,
                                   height=round(self.__topLevel.getTopLevelDimensions()[1]*0.05),
                                    width=9999,
                                   bg=self.__colors.getColor("window"))
        self.__ignoreFrame.pack_propagate(False)
        self.__ignoreFrame.pack(side=LEFT, fill=BOTH)

        self.__ignore1 = StringVar()
        self.__ignore2 = StringVar()

        self.__ignoreEntry2 = Entry(self.__ignoreFrame,
                                    bg = self.__colors.getColor("boxBackNormal"), textvariable = self.__ignore2,
                                    fg = self.__colors.getColor("boxFontNormal"),
                                    font = self.__smallFont, width=2)
        self.__ignoreEntry2.pack_propagate(False)

        self.__signLabel = Label(self.__ignoreFrame, text = " - ",
                                 font = self.__smallFont,
                                 bg = self.__colors.getColor("window"),
                                 fg = self.__colors.getColor("font"))

        self.__signLabel.pack_propagate(False)

        self.__ignoreEntry1 = Entry(self.__ignoreFrame,
                                    bg = self.__colors.getColor("boxBackNormal"), textvariable = self.__ignore1,
                                    fg = self.__colors.getColor("boxFontNormal"),
                                    font = self.__smallFont, width=2)
        self.__ignoreEntry1.pack_propagate(False)

        self.__ignoreEntry1.bind("<FocusIn>", self.focusIn)
        self.__ignoreEntry1.bind("<FocusOut>", self.__checkIgnoreEntries)
        self.__ignoreEntry1.bind("<KeyRelease>", self.__checkIgnoreEntries)

        self.__ignoreEntry2.bind("<FocusIn>", self.focusIn)
        self.__ignoreEntry2.bind("<FocusOut>", self.__checkIgnoreEntries)
        self.__ignoreEntry2.bind("<KeyRelease>", self.__checkIgnoreEntries)

        self.__SetSelectedEntry.bind("<FocusIn>", self.focusIn)
        self.__SetSelectedEntry.bind("<FocusOut>", self.checkSelectedEntry)
        self.__SetSelectedEntry.bind("<KeyRelease>", self.checkSelectedEntry)


        self.__ignoreLabel = Label(self.__ignoreFrame, text = " "*5 + self.__dictionaries.getWordFromCurrentLanguage("ignoreNotes")+" "*2,
                                 font = self.__smallFont,
                                 bg = self.__colors.getColor("window"),
                                 fg = self.__colors.getColor("font"))

        self.__ignoreLabel.pack_propagate(False)
        self.__ignoreLabel.pack(side=LEFT)
        self.__ignoreEntry1.pack(side=LEFT)
        self.__signLabel.pack(side=LEFT)
        self.__ignoreEntry2.pack(side=LEFT)


        self.__buttonFrame3 = Frame(self.__bottomFrame1,
                                   height=round(self.__topLevel.getTopLevelDimensions()[1]*0.05),
                                    width=9999,
                                   bg=self.__colors.getColor("window"))
        self.__buttonFrame3.pack_propagate(False)
        self.__buttonFrame3.pack(side=TOP, fill=X)

        self.__saveItAsMusicRom =  Checkbutton(self.__buttonFrame3, variable=self.__musicROM,
                text=self.__dictionaries.getWordFromCurrentLanguage("generateMusicRom")+"   ",
                bg=self.__colors.getColor("window"),
                fg=self.__colors.getColor("font"),
                font=self.__smallFont, justify=LEFT,
                activebackground=self.__colors.getColor("highLight"))

        self.__saveItAsMusicRom.pack_propagate(False)
        self.__saveItAsMusicRom.pack(side=RIGHT, fill=BOTH, anchor=N)

        self.__bottomFrame2 = Frame(self.__bottomFrame,
                                   width=round(self.__topLevel.getTopLevelDimensions()[0]*0.5),
                                    height=9999,
                                   bg=self.__colors.getColor("window"))
        self.__bottomFrame2.pack_propagate(False)
        self.__bottomFrame2.pack(side=LEFT, fill=BOTH)


        self.__bottomFrame2Third1 = Frame(self.__bottomFrame2,
                                   width=round(self.__topLevel.getTopLevelDimensions()[0]*0.5*0.33),
                                    height=9999,
                                   bg=self.__colors.getColor("window"))
        self.__bottomFrame2Third1.pack_propagate(False)
        self.__bottomFrame2Third1.pack(side=LEFT, fill=Y)

        self.__listTitle = Label(self.__bottomFrame2Third1,
                              bg=self.__colors.getColor("window"),
                              fg=self.__colors.getColor("font"),
                              text = self.__dictionaries.getWordFromCurrentLanguage("cover"),
                              font = self.__normalFont
                                      )

        self.__listTitle.pack_propagate(False)
        self.__listTitle.pack(side=TOP, fill=BOTH)

        self.__lBoxFrame = Frame(self.__bottomFrame2Third1,
                                   width=round(self.__topLevel.getTopLevelDimensions()[0]*0.5*0.33),
                                    height=9999,
                                   bg=self.__colors.getColor("window"))
        self.__lBoxFrame.pack_propagate(False)
        self.__lBoxFrame.pack(side=TOP, fill=BOTH)

        self.__scrollBar = Scrollbar(self.__lBoxFrame)
        self.__listBox = Listbox(self.__lBoxFrame, width=99999,
                                 yscrollcommand=self.__scrollBar.set,
                                 selectmode=BROWSE,
                                 exportselection=False
                                 )
        self.__scrollBar.pack(side=RIGHT, anchor=SW, fill=Y)
        self.__listBox.pack(side=LEFT, anchor=SW, fill=BOTH)
        self.__listBox.pack_propagate(False)
        self.__loader.listBoxes["musicComposer"] = self.__listBox

        self.__scrollBar.config(command=self.__listBox.yview)

        self.__listBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__listBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__listBox.config(font=self.__smallFont)

        from os import walk

        self.__listItems = ["*Fortari Logo*"]
        for root, dirs, filenames in walk(self.__loader.mainWindow.projectPath + "/64px/"):
            for filename in filenames:
                self.__listItems.append(".".join(filename.split(".")[:-1]).split("/")[-1])

        for item in self.__listItems:
            self.__listBox.insert(END, item)

        self.__listBox.selection_set(0)

        self.__bottomFrame2Third2 = Frame(self.__bottomFrame2,
                                   width=round(self.__topLevel.getTopLevelDimensions()[0]*0.5*0.33),
                                    height=9999,
                                   bg=self.__colors.getColor("window"))
        self.__bottomFrame2Third2.pack_propagate(False)
        self.__bottomFrame2Third2.pack(side=LEFT, fill=Y)

        self.__bankTitle = Label(self.__bottomFrame2Third2,
                              bg=self.__colors.getColor("window"),
                              fg=self.__colors.getColor("font"),
                              text = self.__dictionaries.getWordFromCurrentLanguage("banksToLock"),
                              font = self.__smallFont
                                      )

        self.__bankTitle.pack_propagate(False)
        self.__bankTitle.pack(side=TOP, fill=BOTH)

        self.__theTwoBanksFrame = Frame(self.__bottomFrame2Third2,
                                   width=round(self.__topLevel.getTopLevelDimensions()[0]*0.5*0.33),
                                    height=round(self.__topLevel.getTopLevelDimensions()[1]*0.03),
                                   bg=self.__colors.getColor("window"))
        self.__theTwoBanksFrame.pack_propagate(False)
        self.__theTwoBanksFrame.pack(side=TOP, fill=X)

        from MusicBankFrameEntry import MusicBankFrameEntry

        self.__bank1 = MusicBankFrameEntry(self.__loader, self.__theTwoBanksFrame, self.__topLevel,
                                           self.__banks, 0, self.focusIn, self.focusOut,
                                           self.__normalFont, self.__errorCounters,
                                           self.__bankEntries, [self.__artistName, self.__songTitle]
                                           )

        self.__bank2 = MusicBankFrameEntry(self.__loader, self.__theTwoBanksFrame, self.__topLevel,
                                           self.__banks, 1, self.focusIn, self.focusOut,
                                           self.__normalFont, self.__errorCounters,
                                           self.__bankEntries, [self.__artistName, self.__songTitle]
                                           )

        self.__colorTitle = Label(self.__bottomFrame2Third2,
                              bg=self.__colors.getColor("window"),
                              fg=self.__colors.getColor("font"),
                              text = self.__dictionaries.getWordFromCurrentLanguage("textColors"),
                              font = self.__smallFont
                                      )

        self.__colorTitle.pack_propagate(False)
        self.__colorTitle.pack(side=TOP, fill=BOTH)

        self.__theTwoColorsFrame = Frame(self.__bottomFrame2Third2,
                                   width=round(self.__topLevel.getTopLevelDimensions()[0]*0.5*0.33),
                                    height=round(self.__topLevel.getTopLevelDimensions()[1]*0.03),
                                   bg=self.__colors.getColor("window"))
        self.__theTwoColorsFrame.pack_propagate(False)
        self.__theTwoColorsFrame.pack(side=TOP, fill=X)

        self.__theTwoColorsFrame1 = Frame(self.__theTwoColorsFrame,
                                   width=round(self.__topLevel.getTopLevelDimensions()[0]*0.5*0.16),
                                    height=round(self.__topLevel.getTopLevelDimensions()[1]*0.03),
                                   bg=self.__colors.getColor("window"))
        self.__theTwoColorsFrame1.pack_propagate(False)
        self.__theTwoColorsFrame1.pack(side=LEFT, fill=Y)

        self.__theTwoColorsFrame2 = Frame(self.__theTwoColorsFrame,
                                   width=round(self.__topLevel.getTopLevelDimensions()[0]*0.5*0.16),
                                    height=round(self.__topLevel.getTopLevelDimensions()[1]*0.03),
                                   bg=self.__colors.getColor("window"))
        self.__theTwoColorsFrame2.pack_propagate(False)
        self.__theTwoColorsFrame2.pack(side=LEFT, fill=Y)

        from HexEntry import HexEntry

        self.__frontColor = HexEntry(self.__loader, self.__theTwoColorsFrame1, self.__colors,
                              self.__colorDict, self.__normalFont, self.__colorConstans, 0, self.focusIn, self.focusOut)

        self.__backColor = HexEntry(self.__loader, self.__theTwoColorsFrame2, self.__colors,
                              self.__colorDict, self.__normalFont, self.__colorConstans, 1, self.focusIn, self.focusOut)

        self.__colorTitle = Label(self.__bottomFrame2Third2,
                              bg=self.__colors.getColor("window"),
                              fg=self.__colors.getColor("font"),
                              text = self.__dictionaries.getWordFromCurrentLanguage("frameColor"),
                              font = self.__smallFont
                                      )

        self.__colorTitle.pack_propagate(False)
        self.__colorTitle.pack(side=TOP, fill=BOTH)

        self.__frameColorFrame = Frame(self.__bottomFrame2Third2,
                                   width=round(self.__topLevel.getTopLevelDimensions()[0]*0.5*0.33),
                                    height=round(self.__topLevel.getTopLevelDimensions()[1]*0.03),
                                   bg=self.__colors.getColor("window"))
        self.__frameColorFrame.pack_propagate(False)
        self.__frameColorFrame.pack(side=LEFT, fill=Y)

        self.__frameColor = HexEntry(self.__loader, self.__frameColorFrame, self.__colors,
                              self.__colorDict, self.__normalFont, self.__colorConstans, 2, self.focusIn, self.focusOut)


        self.__runningThreads -= 1

        self.__bottomFrame2Third3 = Frame(self.__bottomFrame2,
                                   width=round(self.__topLevel.getTopLevelDimensions()[0]*0.5*0.33),
                                    height=9999,
                                   bg=self.__colors.getColor("window"))
        self.__bottomFrame2Third3.pack_propagate(False)
        self.__bottomFrame2Third3.pack(side=LEFT, fill=BOTH)

        self.__visualizerColorsTitle = Label(self.__bottomFrame2Third3,
                              bg=self.__colors.getColor("window"),
                              fg=self.__colors.getColor("font"),
                              text = self.__dictionaries.getWordFromCurrentLanguage("visualizerColors"),
                              font = self.__smallFont
                                      )

        self.__visualizerColorsTitle.pack_propagate(False)
        self.__visualizerColorsTitle.pack(side=TOP, fill=X)

        self.__visualizerColorsFrame = Frame(self.__bottomFrame2Third3,
                                   width=round(self.__topLevel.getTopLevelDimensions()[0]*0.5*0.33),
                                    height=round(self.__topLevel.getTopLevelDimensions()[1]*0.03),
                                   bg=self.__colors.getColor("window"))
        self.__visualizerColorsFrame.pack_propagate(False)
        self.__visualizerColorsFrame.pack(side=TOP, fill=Y)

        self.__visualizerColorsFrame1 = Frame(self.__visualizerColorsFrame,
                                   width=round(self.__topLevel.getTopLevelDimensions()[0]*0.5*0.10),
                                    height=round(self.__topLevel.getTopLevelDimensions()[1]*0.03),
                                   bg=self.__colors.getColor("window"))
        self.__visualizerColorsFrame1.pack_propagate(False)
        self.__visualizerColorsFrame1.pack(side=LEFT, fill=Y)

        self.__visualizerColorsFrame2 = Frame(self.__visualizerColorsFrame,
                                              width=round(self.__topLevel.getTopLevelDimensions()[0] * 0.5 * 0.10),
                                              height=round(self.__topLevel.getTopLevelDimensions()[1] * 0.03),
                                              bg=self.__colors.getColor("window"))
        self.__visualizerColorsFrame2.pack_propagate(False)
        self.__visualizerColorsFrame2.pack(side=LEFT, fill=Y)

        self.__visualizerColorsFrame3 = Frame(self.__visualizerColorsFrame,
                                              width=round(self.__topLevel.getTopLevelDimensions()[0] * 0.5 * 0.10),
                                              height=round(self.__topLevel.getTopLevelDimensions()[1] * 0.03),
                                              bg=self.__colors.getColor("window"))
        self.__visualizerColorsFrame3.pack_propagate(False)
        self.__visualizerColorsFrame3.pack(side=LEFT, fill=Y)

        self.__visualColor1 = HexEntry(self.__loader, self.__visualizerColorsFrame1, self.__colors,
                              self.__colorDict, self.__normalFont, self.__colorConstans, 3, self.focusIn, self.focusOut)

        self.__visualColor2 = HexEntry(self.__loader, self.__visualizerColorsFrame2, self.__colors,
                              self.__colorDict, self.__normalFont, self.__colorConstans, 4, self.focusIn, self.focusOut)

        self.__visualColor3 = HexEntry(self.__loader, self.__visualizerColorsFrame3, self.__colors,
                              self.__colorDict, self.__normalFont, self.__colorConstans, 5, self.focusIn, self.focusOut)

        self.__importMediaTitle = Label(self.__bottomFrame2Third3,
                              bg=self.__colors.getColor("window"),
                              fg=self.__colors.getColor("font"),
                              text = self.__dictionaries.getWordFromCurrentLanguage("importMedia"),
                              font = self.__smallFont
                                      )

        self.__importMediaTitle.pack_propagate(False)
        self.__importMediaTitle.pack(side=TOP, fill=X)

        self.__importMediaFrame = Frame(self.__bottomFrame2Third3,
                                   width=round(self.__topLevel.getTopLevelDimensions()[0]*0.5*0.33),
                                    height=round(self.__topLevel.getTopLevelDimensions()[1]*0.03),
                                   bg=self.__colors.getColor("window"))
        self.__importMediaFrame.pack_propagate(False)
        self.__importMediaFrame.pack(side=TOP, fill=Y)

        self.__importButton = Button(self.__importMediaFrame,
                              bg=self.__colors.getColor("window"),
                              fg=self.__colors.getColor("font"),
                              text = self.__dictionaries.getWordFromCurrentLanguage("importFile"),
                              font = self.__normalFont, command = self.openMedium, state=DISABLED
                                      )
        self.__importButton.pack_propagate(False)
        self.__importButton.pack(fill=BOTH)

        self.__removePercuss = IntVar()
        self.__removePercuss.set(0)

        self.__removeOutside = IntVar()
        self.__removeOutside.set(1)

        self.__veryBottomFrame = Frame(self.__bottomFrame2Third3,
                                   width=round(self.__topLevel.getTopLevelDimensions()[0]*0.5*0.33),
                                    height=round(self.__topLevel.getTopLevelDimensions()[1]*0.05),
                                   bg=self.__colors.getColor("window"))
        self.__veryBottomFrame.pack_propagate(False)
        self.__veryBottomFrame.pack(side=TOP, fill=BOTH)


        self.__removerPercussBox =  Checkbutton(self.__veryBottomFrame, variable=self.__removePercuss,
                text=self.__dictionaries.getWordFromCurrentLanguage("cutPerc"),
                bg=self.__colors.getColor("window"),
                fg=self.__colors.getColor("font"),
                font=self.__smallFont, justify=LEFT,
                command=self.changedSetToYes,
                activebackground=self.__colors.getColor("highLight"))


        self.__removerPercussBox.pack_propagate(False)
        self.__removerPercussBox.pack(side=TOP, fill=BOTH, anchor=E)

        self.__removeOutsideBox =  Checkbutton(self.__veryBottomFrame, variable=self.__removeOutside,
                text=self.__dictionaries.getWordFromCurrentLanguage("cutNoneSeen"),
                bg=self.__colors.getColor("window"),
                fg=self.__colors.getColor("font"),
                font=self.__tinyFont2, justify=LEFT,
                command=self.changedSetToYes,
                activebackground=self.__colors.getColor("highLight"))


        self.__removeOutsideBox.pack_propagate(False)
        self.__removeOutsideBox.pack(side=TOP, fill=BOTH, anchor=E)

    def __checkIgnoreEntries(self, event):
        if len(self.__ignore1.get()) > 2:
            self.__ignore1.set(self.__ignore1.get()[:2])
        if len(self.__ignore2.get()) > 2:
            self.__ignore2.set(self.__ignore2.get()[:2])

        num1 = 0
        num2 = 0

        if self.__ignore1.get() != "" :
            while True:
                try:
                    if self.__ignore1.get() == "":
                        break
                    num1 = int(self.__ignore1.get())
                    break
                except:
                    self.__ignore1.set(self.__ignore1.get()[:-1])

            if num1 < 0:
                self.__ignore1.set("0")

        if self.__ignore2.get() != "" :
            while True:
                try:
                    if self.__ignore2.get() == "":
                        break
                    num2 = int(self.__ignore2.get())
                    break
                except:
                    self.__ignore2.set(self.__ignore2.get()[:-1])

            if num2 < 0:
                self.__ignore2.set("0")


        if self.__ignore1.get() != "" and self.__ignore2.get() != "":
            if num1 > num2:
                temp = self.__ignore1.get()

                self.__ignore1.set(self.__ignore2.get())
                self.__ignore2.set(temp)



    def __eraseScreen(self):
        for X in range(0,self.__tiaScreens.numOfFieldsW):
            self.eraseRow(X)

    def __copyScreen(self):
        self.__tiaScreens.copyScreen()

    def __pasteScreen(self):
        self.__tiaScreens.pasteScreen()
        self.forceShit = True
        self.reColorAll()

    def setMaxChannels(self, value):
        self.__maxChannels = int(value)

    def changedSetToYes(self):
        self.changed = True

    def __justBytesThread(self):
        from threading import Thread

        if self.__calculatingThread == None:
            self.__bankLabelText.set(self.__dictionaries.getWordFromCurrentLanguage("calculating"))
            t = Thread(target=self.__justBytes, args=[True])
            t.daemon = True
            t.start()
            self.__calculatingThread = True

    def __justBytes(self, playSound):
        from Compiler import Compiler

        numOfBanks = Compiler(self.__loader, "common",
                              "getMusicBytes", [
                                self.__tiaScreens.composeData(self.__correctNotes,
                                                              self.__buzz,
                                                              self.__fadeOutLen,
                                                              self.__frameLen,
                                                              self.__vibratio,
                                                              self.__vibratio2,
                                                              int(self.__removePercuss.get()),
                                                              self.__maxChannels,
                                                              int(self.__removeOutside.get()),
                                                              "NTSC", self.getRangeToCut())])

        if numOfBanks.musicMode == "mono" or numOfBanks.musicMode == "stereo":
            try:
                self.__banks[0] = int(self.__bank1.getValue())
                self.__virtualMemory.registerNewLock(self.__banks[0], name, "music", 0, "LAST")
            except:
                pass
        elif numOfBanks.musicMode == "double":
            try:
                self.__banks[0] = int(self.__bank1.getValue())
                self.__virtualMemory.registerNewLock(self.__banks[0], name, "music", 0, None)
            except:
                pass

            try:
                self.__banks[1] = int(self.__bank2.getValue())
                self.__virtualMemory.registerNewLock(self.__banks[1], name, "music", 1, "LAST")
            except:
                pass

        self.__setBankLabelText(numOfBanks.bytes)
        if playSound == True:
            from random import randint
            num = randint(0,1000)
            if num <995:
                self.__loader.soundPlayer.playSound("OK")
            else:
                self.__loader.soundPlayer.playSound("Probe")
        self.__calculatingThread = None


    def __setBankLabelText(self, data):
        numbers = []

        for number in data:
            number = str(number)
            while len(number)<5:
                number = "0" + number
            numbers.append(number)

        if data[0]<3601 and data[1]<3601:
            self.__bankLabelText.set("Bank0: " +numbers[0]+" Bank1: "+numbers[1])
            self.__bankLabel.config(
                bg=self.__colors.getColor("window"),
                fg=self.__colors.getColor("font")
            )
        else:
            if data[0]<data[1]:
                tooMuch = data[0]
            else:
                tooMuch = data[1]

            #n = str(tooMuch-3600)
            #while len(n)<5:
            #    n = "0" + n

            self.__bankLabelText.set(self.__dictionaries.getWordFromCurrentLanguage("overflow").upper())
            self.__bankLabel.config(
                bg=self.__colors.getColor("boxBackUnSaved"),
                fg=self.__colors.getColor("boxFontUnSaved")
            )


    def openMedium(self):
        if self.changed == True:
            answer = self.__fileDialogs.askYesNoCancel("notSavedFile", "notSavedFileMessage")
            self.__topLevelWindow.deiconify()
            self.__topLevelWindow.focus()

            if answer == "Cancel":
                self.__topLevelWindow.deiconify()
                self.__topLevelWindow.focus()
                return
            elif answer == "Yes":
                self.__saveDataToFile()

        fileName = self.__fileDialogs.askForFileName("openFile", False,
                                                     ["mid", "sid", ["vgm", "vgz"], "mod", "*"],
                                                  self.__loader.mainWindow.projectPath)

        functions = {
            "mid": self.convertMidi,
            "sid": self.convertSID,
            "vgm": self.convertVGM,
            "vgz": self.convertVGM,
            "mod": None
        }

        converted = None
        errorText = ""

        extension = fileName.split(".")[-1]
        if extension in functions.keys():
            #try:
                converted, songTitle = functions[extension](fileName)
            #except Exception as e:
                #errorText = str(e)
        else:
            for func in functions.keys():
                try:
                    converted, songTitle = function[func](fileName)
                except Exception as e:
                    errorText += str(e)

        if converted == None:
            self.__fileDialogs.displayError("importError", "importErrorMessage", None, errorText)
        else:
            counter = 0
            theLen = 0


            # Did not found any midis that had all notes corresponding a divider and also it won't improve
            # storage, so I commented this out.

            #if self.__fortran == False:
            for num in range(0, 16):
                try:
                    if (len(converted[num]) > 0):
                        theLen = len(converted[num])
                        break
                except Exception as e:
                    pass

            screenMaxNum = theLen // self.__tiaScreens.numOfFieldsW
            self.__tiaScreens.initWithGivenNumberOfScreens(screenMaxNum)
            self.__tiaScreens.insertDataFromConverted(converted, theLen, screenMaxNum)

            #else:
            #    self.__tiaScreens.insertDataFromFortranConverted(converted)

            #print(theLen, screenMaxNum)

            self.__justBytesThread()

            self.reset = True
            self.reColorAll()

            self.__frameLen = int(1)
            self.__frameLenSetter.setValue("1")

            self.__artistName.set("")
            self.__songTitle.set(songTitle)
            #print(self.__tiaScreens.screenMax, self.__screenMax)
            self.__soundPlayer.playSound("Success")


        self.changed = False
        self.forceShit = True
        self.__topLevelWindow.deiconify()
        self.__topLevelWindow.focus()

    def convertVGM(self, path):
        from VGMConverter import VGMConverter

        vgmConverter = VGMConverter(self.__loader, path, int(self.__removePercuss.get()),
                                    self.__maxChannels, int(self.__removeOutside.get()), self.getRangeToCut())

        return (vgmConverter.result, vgmConverter.songName)

    def convertSID(self, path):
        from SIDConverter import SIDConverter

        sidConverter = SIDConverter(self.__loader, path, int(self.__removePercuss.get()),
                                    self.__maxChannels, int(self.__removeOutside.get()), self.getRangeToCut())

        return (sidConverter.result, sidConverter.songName)

    def convertMidi(self, path):
        from MidiConverter import MidiConverter

        midiConverter = MidiConverter(path, self.__loader, int(self.__removePercuss.get()),
                                      self.__maxChannels, int(self.__removeOutside.get()), 1, self.getRangeToCut())

        return (midiConverter.result, midiConverter.songName)



    def __testingCurrent(self):
        from threading import Thread

        t = Thread(target=self.__testingCurrentThread)
        t.daemon = True
        t.start()


    def getRangeToCut(self):
        if self.__ignore1.get() == "" and self.__ignore2.get() == "":
            return(None)

        if self.__ignore1.get() == "":
            smallest = 0
        else:
            smallest = int(self.__ignore1.get())

        if self.__ignore2.get() == "":
            largest = 100
        else:
            largest = int(self.__ignore2.get())

        numbers = range(smallest, largest + 1, 1)
        if (self.__removePercuss.get()) == 0:
            new = []
            for number in numbers:
                if number not in range(89, 96, 1):
                    new.append(number)

            numbers = new

        return(numbers)

    def __testingCurrentThread(self):


        extracted = self.__tiaScreens.composeData(
            self.__correctNotes, self.__buzz, self.__fadeOutLen, self.__frameLen, self.__vibratio, self.__vibratio2,
            int(self.__removePercuss.get()), self.__maxChannels, int(self.__removeOutside.get()), "NTSC", self.getRangeToCut())
        #self.testPrinting(extracted)

        if self.__listItems[self.__listBox.curselection()[0]] == "*Fortari Logo*":
            self.__picturePath = None
        else:
            self.__picturePath = (self.__loader.mainWindow.projectPath
                                  +"/64px/"+self.__listItems[self.__listBox.curselection()[0]]
                                  +".asm")

        if self.__picturePath == None:
            pictureData = [27, 27, 0]
        else:
            textLoaded = open(self.__picturePath, "r").read().split("pic64px")[2]
            lines = textLoaded.count("BYTE")
            pictureData = [lines, lines, 0]

        if self.__musicROM.get() == 0:
            path = "temp/"
        else:
            path = "generatedMusicROMs/"
            try:
                import os
                os.mkdir("generatedMusicROMs")
            except:
                pass

        from Compiler import Compiler
        C = Compiler(self.__loader, "common", "music", [self.__picturePath, path, True, self.__artistName.get(),
                                                        self.__songTitle.get(), extracted, self.__banks,
                                                        self.__variables, self.__colorConstans, pictureData])

        self.__setBankLabelText(C.bytes)


    def testPrinting(self, data):
        for channelNum in range(0,len(data)):
            print("Channel_"+str(channelNum))
            for tiaNote in data[channelNum]:
                print("("+str(tiaNote.volume)+", "+str(tiaNote.channel)+", "+str(tiaNote.freq)+", " + str(tiaNote.duration)+ ")")



    def __saveDataToFile(self):
        import os

        fileName = self.__loader.mainWindow.projectPath+"musics/"+self.__artistName.get().replace(" ", "_")+"_-_"+self.__songTitle.get().replace(" ", "_")+".a26"

        if os.path.exists(fileName):
            answer = self.__fileDialogs.askYesOrNo("musicExists", "musicExistsMessage")
            self.__topLevelWindow.deiconify()
            self.__topLevelWindow.focus()

            if answer == "No":
                return


        text = self.__artistName.get()+"\n"+self.__songTitle.get()+"\n"

        text+=(str(self.__buzz)+","+str(self.__correctNotes)+","+str(self.__fadeOutLen)+","+
                str(self.__dividerLen)+","+str(self.__vibratio)+","+str(self.__vibratio2)+
                ","+str(self.__frameLen)+","+str(self.__removePercuss.get())+
               ","+str(self.__maxChannels)+","+str(self.__removeOutside.get())+"\n"
               )


        #text += str(self.__banks[0])+","+str(self.__banks[1])+","+str(self.__banks[2])+","+str(self.__banks[3])+"\n"
        text += str(self.__banks[0])+","+str(self.__banks[1])+"\n"

        self.__saveASMThread(fileName)

        data = "\n".join([
            self.__tiaScreens.getWholeChannelDate(1),
            self.__tiaScreens.getWholeChannelDate(2),
            self.__tiaScreens.getWholeChannelDate(3),
            self.__tiaScreens.getWholeChannelDate(4)
        ])

        text += data
        file = open(fileName, "w")
        file.write(text)
        file.close()

        self.__justBytes(False)
        self.__topLevelWindow.deiconify()
        self.__topLevelWindow.focus()
        self.changed = False
        self.__soundPlayer.playSound("Success")

    def __saveASMThread(self, fileName):
        from threading import Thread

        t = Thread(target=self.__saveASMThread, args=[fileName])
        t.daemon = True
        t.start()

    def __saveASM(self, fileName):
        from Compiler import Compiler
        numOfBanks = Compiler(self.__loader, "common",
                              "getMusicBytes", [
                                self.__tiaScreens.composeData(self.__correctNotes,
                                                              self.__buzz,
                                                              self.__fadeOutLen,
                                                              self.__frameLen,
                                                              self.__vibratio,
                                                              self.__vibratio2,
                                                              int(self.__removePercuss.get()),
                                                              self.__maxChannels,
                                                              self.__removeOutside.get(),
                                                              "NTSC", self.getRangeToCut())])

        name = (self.__artistName.get() + "_-_" + self.__songTitle.get()).replace(" ", "_")

        for bankNum in range(0, len(numOfBanks.banks)):
            F = open(fileName.replace(".a26", "_bank"+str(bankNum)+"_"+numOfBanks.musicMode+".asm"), "w")
            F.write(numOfBanks.banks[bankNum])
            F.close()

        if numOfBanks.musicMode == "mono" or numOfBanks.musicMode == "stereo":
            try:
                self.__banks[0] = int(self.__bank1.getValue())
                self.__virtualMemory.registerNewLock(self.__banks[0], name, "music", 0, "LAST")
            except:
                pass
        elif numOfBanks.musicMode == "double":
            try:
                self.__banks[0] = int(self.__bank1.getValue())
                self.__virtualMemory.registerNewLock(self.__banks[0], name, "music", 0, None)
            except:
                pass

            try:
                self.__banks[1] = int(self.__bank2.getValue())
                self.__virtualMemory.registerNewLock(self.__banks[1], name, "music", 1, "LAST")
            except:
                pass


    def __openFile(self):
        if self.changed == True:
            answer = self.__fileDialogs.askYesNoCancel("notSavedFile", "notSavedFileMessage")
            self.__topLevelWindow.deiconify()
            self.__topLevelWindow.focus()

            if answer == "Cancel":
                self.__topLevelWindow.deiconify()
                self.__topLevelWindow.focus()
                return
            elif answer == "Yes":
                self.__saveDataToFile()

        fileName = self.__fileDialogs.askForFileName("openFile", False, ["a26", "*"],
                                                  self.__loader.mainWindow.projectPath + "musics/")

        if fileName == "":
            self.__soundPlayer.playSound("Error")
            self.__topLevelWindow.deiconify()
            self.__topLevelWindow.focus()
            return

        file = open(fileName, "r")
        text = file.read()
        file.close()

        lines = text.replace("\r", "").split("\n")
        numbers = lines[2].split(",")

        self.__buzz = int(numbers[0])
        self.__buzzer.set(int(numbers[0]))
        self.__vibratio = int(numbers[4])
        self.__vibrator.set(int(numbers[4]))

        self.__vibratio2 = int(numbers[5])
        self.__vibrator2.set(int(numbers[5]))

        self.__correctNotes = int(numbers[1])
        self.__correctorSetter.setValue(numbers[1])
        self.__fadeOutLen = int(numbers[2])
        self.__fadeOutSetter.setValue(numbers[2])
        self.__dividerLen = int(numbers[3])
        self.__dividerSetter.setValue(numbers[3])
        self.__frameLen = int(numbers[6])
        self.__frameLenSetter.setValue(numbers[6])
        self.__removePercuss.set(int(numbers[7]))
        self.__maxChannels = int(numbers[8])
        self.__removeOutside.set(int(numbers[9]))

        #self.__maxChannelsSetter.setValue(numbers[8])

        self.__artistName.set(lines[0])
        self.__songTitle.set(lines[1])

        bbb = lines[3].split(",")

        self.__bank1.setValue(bbb[0])
        self.__bank2.setValue(bbb[1])
        #self.__bank3.setValue(bbb[2])
        #self.__bank4.setValue(bbb[3])

        self.__banks = [int(bbb[0]), int(bbb[1])]

        name = (self.__artistName.get() + "_-_" + self.__songTitle.get()).replace(" ", "_")
        self.__tiaScreens.getLoadedInputAndSetData(self, lines[4:])

        self.__soundPlayer.playSound("Success")
        self.__topLevelWindow.deiconify()
        self.__topLevelWindow.focus()

        self.__justBytesThread()

        self.changed = False



    def drawAllTheOthers(self):

        self.__screenSetter = Frame(self.__selectedChannelFrame,
                                   width=round(self.__topLevel.getTopLevelDimensions()[0]*0.15),
                                   bg=self.__colors.getColor("window"))
        self.__screenSetter.pack_propagate(False)
        self.__screenSetter.pack(side=LEFT, anchor = W, fill=Y)

        self.__screenSetterUp = Frame(self.__screenSetter,
                                      height=round(self.__topLevel.getTopLevelDimensions()[1] * 0.025),
                                      bg=self.__colors.getColor("window"))
        self.__screenSetterUp.pack_propagate(False)
        self.__screenSetterUp.pack(side=TOP, anchor = N, fill=X)

        self.__labelSelectedS = Label(self.__screenSetterUp,
                              bg=self.__colors.getColor("window"),
                              fg=self.__colors.getColor("font"),
                              text = self.__dictionaries.getWordFromCurrentLanguage("selectedScreen"),
                              font = self.__normalFont
                                      )
        self.__labelSelectedS.pack_propagate(False)
        self.__labelSelectedS.pack(side=TOP, fill=X)

        self.__screenSetterDown = Frame(self.__screenSetter,
                                      bg=self.__colors.getColor("window"),
                                        height=round(self.__topLevel.getTopLevelDimensions()[1] * 0.025)
                                        )
        self.__screenSetterDown.pack_propagate(False)
        self.__screenSetterDown.pack(side=TOP, anchor = N, fill=BOTH)

        self.__ButtonPrevFrame = Frame(self.__screenSetterDown,
                                      bg=self.__colors.getColor("window"),
                                       width=round(self.__topLevel.getTopLevelDimensions()[0] * 0.05),
                                       )
        self.__ButtonPrevFrame.pack_propagate(False)
        self.__ButtonPrevFrame.pack(side=LEFT, anchor = W, fill=Y)

        self.__ButtonPrev = Button(self.__ButtonPrevFrame,
                              bg=self.__colors.getColor("window"),
                              fg=self.__colors.getColor("font"),
                              text="<<",
                              font=self.__normalFont,
                              state = DISABLED,
                              command = self.__PrevScreen
                              )
        self.__ButtonPrev.pack_propagate(False)
        self.__ButtonPrev.pack(fill=BOTH)

        self.__currentSelected = StringVar()
        self.__currentSelected.set(str(self.__tiaScreens.currentScreen+1))

        self.__SetSelectedEntryFrame = Frame(self.__screenSetterDown,
                                      bg=self.__colors.getColor("window"),
                                       width=round(self.__topLevel.getTopLevelDimensions()[0] * 0.05)
                                       )
        self.__SetSelectedEntryFrame.pack_propagate(False)
        self.__SetSelectedEntryFrame.pack(side=LEFT, anchor = W, fill=Y)


        self.__SetSelectedEntry = Entry(self.__SetSelectedEntryFrame,
                                      bg=self.__colors.getColor("boxBackNormal"),
                                        fg=self.__colors.getColor("boxFontNormal"),
                                       width=round(self.__topLevel.getTopLevelDimensions()[0] * 0.05),
                                        textvariable = self.__currentSelected,
                                        state = DISABLED, justify=CENTER,
                                        font=self.__normalFont
                                       )

        self.__SetSelectedEntry.pack_propagate(False)
        self.__SetSelectedEntry.pack(fill=BOTH)


        self.__SetSelectedEntry.bind("<FocusIn>", self.focusIn)
        self.__SetSelectedEntry.bind("<FocusOut>", self.checkSelectedEntry)
        self.__SetSelectedEntry.bind("<KeyRelease>", self.checkSelectedEntry)


        self.__ButtonNextFrame = Frame(self.__screenSetterDown,
                                      bg=self.__colors.getColor("window"),
                                       width=round(self.__topLevel.getTopLevelDimensions()[0] * 0.05)
                                       )
        self.__ButtonNextFrame.pack_propagate(False)
        self.__ButtonNextFrame.pack(side=LEFT, anchor = W, fill=Y)

        self.__ButtonNext = Button(self.__ButtonNextFrame,
                              bg=self.__colors.getColor("window"),
                              fg=self.__colors.getColor("font"),
                              text=">>",
                              font=self.__normalFont,
                              state = DISABLED,
                              command=self.__NextScreen
                              )
        self.__ButtonNext.pack_propagate(False)
        self.__ButtonNext.pack(fill=BOTH)

        self.__screenInsertDeleteFrame= Frame(self.__selectedChannelFrame,
                                    width=round(self.__topLevel.getTopLevelDimensions()[0] * 0.1),
                                    bg=self.__colors.getColor("window"))
        self.__screenInsertDeleteFrame.pack_propagate(False)
        self.__screenInsertDeleteFrame.pack(side=LEFT, anchor=W, fill=Y)

        self.__insertButtonFrame1 = Frame(self.__screenInsertDeleteFrame,
                                    height=round(self.__topLevel.getTopLevelDimensions()[1] * 0.016),
                                    bg=self.__colors.getColor("window"))
        self.__insertButtonFrame1.pack_propagate(False)
        self.__insertButtonFrame1.pack(side=TOP, anchor=N, fill=X)

        self.__insertButtonFrame2 = Frame(self.__screenInsertDeleteFrame,
                                    height=round(self.__topLevel.getTopLevelDimensions()[1] * 0.016),
                                    bg=self.__colors.getColor("window"))
        self.__insertButtonFrame2.pack_propagate(False)
        self.__insertButtonFrame2.pack(side=TOP, anchor=N, fill=X)

        self.__deleteButtonFrame = Frame(self.__screenInsertDeleteFrame,
                                    height=round(self.__topLevel.getTopLevelDimensions()[1] * 0.016),
                                    bg=self.__colors.getColor("window"))
        self.__deleteButtonFrame.pack_propagate(False)
        self.__deleteButtonFrame.pack(side=TOP, anchor=N, fill=X)

        self.__ButtonInsertBefore = Button(self.__insertButtonFrame1,
                              bg=self.__colors.getColor("window"),
                              fg=self.__colors.getColor("font"),
                              text="<<"+self.__dictionaries.getWordFromCurrentLanguage("insertScreen"),
                              font=self.__tinyFont2, command=self.__insertBefore,
                              state=DISABLED
                              )
        self.__ButtonInsertBefore.pack_propagate(False)
        self.__ButtonInsertBefore.pack(side=TOP, anchor=N, fill=BOTH)

        self.__ButtonInsertAfter = Button(self.__insertButtonFrame2,
                              bg=self.__colors.getColor("window"),
                              fg=self.__colors.getColor("font"),
                              text=self.__dictionaries.getWordFromCurrentLanguage("insertScreen")+">>",
                              font=self.__tinyFont2, command=self.__insertAfter,
                                          state=DISABLED

                                          )
        self.__ButtonInsertAfter.pack_propagate(False)
        self.__ButtonInsertAfter.pack(side=TOP, anchor=N, fill=BOTH)

        self.__deleteCurrentButton = Button(self.__deleteButtonFrame,
                              bg=self.__colors.getColor("window"),
                              fg=self.__colors.getColor("font"),
                              text=self.__dictionaries.getWordFromCurrentLanguage("deleteCurrentScreen"),
                              font=self.__tinyFont2,
                              state = DISABLED,
                              command = self.__deleteCurrent)

        self.__deleteCurrentButton.pack_propagate(False)
        self.__deleteCurrentButton.pack(side=TOP, anchor=N, fill=BOTH)


        self.__smallSetterBox = Frame(self.__selectedChannelFrame,
                                   width=round(self.__topLevel.getTopLevelDimensions()[0]*0.12),
                                   bg=self.__colors.getColor("window"))
        self.__smallSetterBox.pack_propagate(False)
        self.__smallSetterBox.pack(side=LEFT, anchor = W, fill=Y)

        self.__buzzer = IntVar()
        self.__buzzer.set(1)

        self.__vibrator = IntVar()
        self.__vibrator.set(1)

        self.__vibrator2 = IntVar()
        self.__vibrator2.set(1)

        self.__buzzSetter = Checkbutton(self.__smallSetterBox, variable = self.__buzzer,
                                        text=self.__dictionaries.getWordFromCurrentLanguage("buzzer"),
                                        bg=self.__colors.getColor("window"),
                                        fg=self.__colors.getColor("font"),
                                        font=self.__tinyFont2, justify=LEFT,
                                        command = self.setBuzz,
                                        activebackground=self.__colors.getColor("highLight")
                                        )

        self.__buzzSetter.pack_propagate(False)
        self.__buzzSetter.pack(side=TOP, anchor=W)

        self.__vibrSetter = Checkbutton(self.__smallSetterBox, variable = self.__vibrator,
                                        text=self.__dictionaries.getWordFromCurrentLanguage("vibratio").replace("##", "04"),
                                        bg=self.__colors.getColor("window"),
                                        fg=self.__colors.getColor("font"),
                                        font=self.__tinyFont2, justify=LEFT,
                                        command=self.setVibratio,
                                        activebackground = self.__colors.getColor("highLight")
                                        )

        self.__vibrSetter.pack_propagate(False)
        self.__vibrSetter.pack(side=TOP, anchor=W)

        self.__vibrSetter2 = Checkbutton(self.__smallSetterBox, variable = self.__vibrator2,
                                        text=self.__dictionaries.getWordFromCurrentLanguage("vibratio").replace("##", "12"),
                                        bg=self.__colors.getColor("window"),
                                        fg=self.__colors.getColor("font"),
                                        font=self.__tinyFont2, justify=LEFT,
                                        command=self.setVibratio2,
                                         activebackground=self.__colors.getColor("highLight")
                                        )

        self.__vibrSetter2.pack_propagate(False)
        self.__vibrSetter2.pack(side=TOP, anchor=W)

        from FrameLabelEntryUpDown import FrameLabelEntryUpDown

        self.__dividerSetter = FrameLabelEntryUpDown(self.__loader, self.__selectedChannelFrame,
                                                     round(self.__topLevel.getTopLevelDimensions()[0] * 0.05),
                                                     round(self.__topLevel.getTopLevelDimensions()[1] * 0.05),
                                                     "beat", 1, 4, self.__tinyFont2, self.__sizeAll, self.__dividerLen, self.__normalFont,
                                                     "beats", self.__errorCounters, self.focusIn, self.focusOut
                                                     )

        self.__fadeOutSetter = FrameLabelEntryUpDown(self.__loader, self.__selectedChannelFrame,
                                                     round(self.__topLevel.getTopLevelDimensions()[0] * 0.05),
                                                     round(self.__topLevel.getTopLevelDimensions()[1] * 0.05),
                                                     "fadeOut", 0, 4, self.__tinyFont2, self.setFadeOut, self.__fadeOutLen, self.__normalFont,
                                                     "fadeOut", self.__errorCounters, self.focusIn, self.focusOut
                                                     )

        self.__frameLenSetter = FrameLabelEntryUpDown(self.__loader, self.__selectedChannelFrame,
                                                     round(self.__topLevel.getTopLevelDimensions()[0] * 0.05),
                                                     round(self.__topLevel.getTopLevelDimensions()[1] * 0.05),
                                                     "toneLen", 1, 255, self.__tinyFont2, self.setFrameLen, self.__frameLen, self.__normalFont,
                                                     "toneLenght", self.__errorCounters, self.focusIn, self.focusOut
                                                     )

        self.__correctorSetter = FrameLabelEntryUpDown(self.__loader, self.__selectedChannelFrame,
                                                     round(self.__topLevel.getTopLevelDimensions()[0] * 0.05),
                                                     round(self.__topLevel.getTopLevelDimensions()[1] * 0.05),
                                                     "corrector", 0, 2, self.__tinyFont2, self.setCorrection, self.__correctNotes, self.__normalFont,
                                                     "corrector", self.__errorCounters, self.focusIn, self.focusOut
                                                     )

        self.__runningThreads -= 1

    def setFadeOut(self, num):
        self.__fadeOutLen = num
        self.changed = True

    def setFrameLen(self, num):
        self.__frameLen = num
        self.changed = True

    def setCorrection(self, num):
        self.__correctNotes = num
        self.changed = True

    def __insertBefore(self):
        self.__tiaScreens.insertBefore()
        self.__currentSelected.set(str(self.__tiaScreens.currentScreen))
        self.changed = True

    def __insertAfter(self):
        self.__tiaScreens.insertAfter()
        self.changed = True

    def __deleteCurrent(self):
        self.__tiaScreens.deleteCurrent()
        self.__topLevelWindow.deiconify()
        self.__topLevelWindow.focus()
        self.forceShit = True
        self.__goScreen()
        self.changed = True


    def setBuzz(self):
        self.__buzz = self.__buzzer.get()
        self.changed = True

    def setVibratio(self):
        self.__vibratio = self.__vibrator.get()
        self.changed = True

    def setVibratio2(self):
        self.__vibratio2 = self.__vibrator2.get()
        self.changed = True

    def __PrevScreen(self):
        if self.__runningThreads>0:
            return

        self.__tiaScreens.currentScreen-=1
        self.__goScreen()

    def __NextScreen(self):
        if self.__runningThreads>0:
            return

        self.__tiaScreens.currentScreen+=1
        self.__goScreen()

    def checkSelectedEntry(self, event):
        if "FocusOut" in str(event):
            self.focusOut(event)
        if self.__runningThreads>0:
            return

        try:
            number = int(self.__currentSelected.get())
            self.__SetSelectedEntry.config(
                bg = self.__colors.getColor("boxBackNormal"),
                fg = self.__colors.getColor("boxFontNormal")
            )
            self.changed = True
        except:
            self.__SetSelectedEntry.config(
                bg = self.__colors.getColor("boxBackUnSaved"),
                fg = self.__colors.getColor("boxFontUnSaved")

            )
            self.__errorCounters["selected"] = 1
            return

        self.__errorCounters["selected"] = 0
        if number<1:
            number = 1
            self.__currentSelected.set("1")
        elif number > self.__tiaScreens.screenMax:
            number = self.__tiaScreens.screenMax
            self.__currentSelected.set(str(self.__tiaScreens.screenMax))

        if number != self.__tiaScreens.currentScreen+1:
            self.__tiaScreens.currentScreen = number-1
            self.__goScreen()

    def __goScreen(self):
        screen = self.__tiaScreens.allData[self.__tiaScreens.currentChannel-1][self.__tiaScreens.currentScreen]["screen"]
        screenY = self.__tiaScreens.allData[self.__tiaScreens.currentChannel-1][self.__tiaScreens.currentScreen]["Y"]

        self.__currentSelected.set(str(self.__tiaScreens.currentScreen+1))

        for Y in range(0,100):
            for X in range(0, self.__tiaScreens.numOfFieldsW):
                try:
                    cell = screen[Y][X]
                    Button = self.__piaNoteTable[str(X)+","+str(Y)]

                    if cell["volume"] == 0:
                        Button.config(text = "")
                    else:
                        Button.config(text = str(cell["volume"]))


                    self.colorButton(X, Y, Button)
                    self.reSize(X,Y)
                except:
                    pass


        self.forceShit = True

    def __sizeAll(self, number):
        self.__dividerLen = number
        for button in self.__piaNoteTable:
            name = str(button).split(".")[-1]
            Y, X = self.getXYfromName(name)
            self.reSize(X, Y)

    def pressedNumber(self, event):
        if self.focused != None:
            return
        try:
            number = int(event.char)
        except:
            return

        if len(self.__numberBuffer)>1:
            self.__numberBuffer.pop(0)

        self.__numberBuffer.append(number)

        if self.__choosenOne!=None:
            try:
                number = self.__numberBuffer[0]*10+self.__numberBuffer[1]
                if number<16:

                    button = self.__choosenOne
                    buttonValues = self.buttonValuesFromWidget(button)

                    name = str(button).split(".")[-1]
                    Y, X = self.getXYfromName(name)

                    if number == 0:
                        self.__tiaScreens.setTileValue(X, Y, 0, 0, 0, 0)
                    else:
                        self.setValues(X, Y)
                        self.__tiaScreens.setTileValue(X, Y, number,
                                                       buttonValues["channel"], buttonValues["freq"], 1)



                    self.colorButton(X, Y, button)
                    self.__numberBuffer = []

            except Exception as e:
                pass
                #print(self.__numberBuffer)
                #self.__loader.logger.errorLog(e)

    def reSize(self, X, Y):
        name = str(X)+","+str(Y)
        w = round(round(self.__topLevel.getTopLevelDimensions()[0] * 0.85) / self.__tiaScreens.numOfFieldsW)

        if self.__dividerLen > 1 and (X + 1) % self.__dividerLen == 0:
            w = w*0.95
        self.__frames[name].config(width=w)


    def button2(self, event):
        self.__draw = 1 - self.__draw

    def createPattenrs(self):
        from copy import deepcopy

        pattern = []
        octave = [0,1,0,1,0,0,1,0,1,0,1,0]
        for num in range(0, 3):
            pattern.extend(deepcopy(octave))
        pattern.append(0)
        self.__patterns["tremble"] = pattern

        pattern = []
        octave = [0,1,0,1,0,0,1,0,1,0,1,0]
        for num in range(0, 2):
            pattern.extend(deepcopy(octave))
        pattern.extend([0,1,0,1,0])
        self.__patterns["bass"] = pattern


    def __drawDrums(self, frame, frameH):
        numofFieldsW = self.__tiaScreens.numOfFieldsW
        numofFieldsH = 3

        listenButtons = Frame(frame, bg = self.__colors.getColor("window"),
                              width=round(self.__topLevel.getTopLevelDimensions()[0]*0.08))
        listenButtons.pack_propagate(False)
        listenButtons.pack(side=LEFT, anchor=W, fill=Y)

        setPanel = Frame(frame, bg = self.__colors.getColor("window"),
                         width=round(self.__topLevel.getTopLevelDimensions()[0]*0.92))
        setPanel.pack_propagate(False)
        setPanel.pack(side=LEFT, anchor=W, fill=BOTH)

        baseW = round(round(self.__topLevel.getTopLevelDimensions()[0] * 0.85) / numofFieldsW)
        baseH = round(frameH*self.__drumNUM / numofFieldsH * 0.6)

        self.drumSetNames = ["15,20", "8,0", "15,2", "8,8", "2,0", "3,0", "3,1"]

        self.drumButton(self.drumSetNames[0], self.__dictionaries.getWordFromCurrentLanguage("drum"), 0, listenButtons, baseW, baseH)
        self.drumButton(self.drumSetNames[1], self.__dictionaries.getWordFromCurrentLanguage("hat")+"-1", 1, listenButtons, baseW, baseH)
        self.drumButton(self.drumSetNames[2], self.__dictionaries.getWordFromCurrentLanguage("hat")+"-2", 2, listenButtons, baseW, baseH)
        self.drumButton(self.drumSetNames[3], self.__dictionaries.getWordFromCurrentLanguage("snare"), 3, listenButtons, baseW, baseH)
        self.drumButton(self.drumSetNames[4], self.__dictionaries.getWordFromCurrentLanguage("horn"), 4, listenButtons, baseW, baseH)
        self.drumButton(self.drumSetNames[5], self.__dictionaries.getWordFromCurrentLanguage("buzz")+"-1", 5, listenButtons, baseW, baseH)
        self.drumButton(self.drumSetNames[6], self.__dictionaries.getWordFromCurrentLanguage("buzz")+"-2", 6, listenButtons, baseW, baseH)

        theY = 0
        for yY in range(0,7):
            color1 = "white"
            color2 = "black"
            if yY % 2 == 1:
                color1 = "black"
                color2 = "white"

            theX = 0
            for counter in range(0, numofFieldsW):
                if self.__dividerLen > 1 and (counter + 1) % self.__dividerLen == 0:
                    theW = round(baseW*0.95)
                else:
                    theW = baseW

                f = Frame(setPanel, width=theW, height=baseH, bg=color1,
                          name = str(counter) + "," +str(yY+89))
                f.pack_propagate(False)
                f.place(x=theX, y=theY)

                self.__frames[str(counter) + "," +str(yY+89)] = f

                b = Button(f, width=theW, height=baseH, bg=color1,
                           fg=color2,
                           font=self.__tinyFont2,
                           name=str(counter) + "," + str(yY+89),
                           activebackground=self.__colors.getColor("highLight"))

                self.__tiaScreens.setColorValue(counter, yY+89, color1)
                self.colorButton(counter, yY+89, b)
                b.pack_propagate(False)
                b.pack(fill=BOTH)
                self.__piaNoteTable[str(counter) + "," + str(yY+89)] = b

                b.bind("<ButtonPress-1>", self.clickedButton)
                b.bind("<MouseWheel>", self.mouseWheel)
                b.bind("<Enter>", self.enterCommon)
                b.bind("<Leave>", self.leave)


                theX+=baseW
            theY+=baseH
        self.__runningThreads-=1

    def drumButton(self, name, text, multi, frame, baseW, baseH):
        f = Frame(frame, width=baseW*3, height=baseH, bg="white")
        f.pack_propagate(False)
        f.place(x=0, y=baseH*multi)

        if multi % 2 == 0:
            color1 = "white"
            color2 = "black"
        else:
            color2 = "white"
            color1 = "black"

        b = Button(f, width=baseW*3, height=baseH, bg=color1, fg=color2,
                    font=self.__tinyFont, name=name,
                   text = text,
                   activebackground=self.__colors.getColor("highLight")
                   )
        b.pack_propagate(False)
        b.pack(fill=BOTH)
        b.bind("<ButtonPress-1>", self.playNote1)


    def __drawField(self, frame, frameH, start, end, pattern, key):

        if key == "bass":
            frameH * self.__bassNUM

        numofFieldsH = start-end
        numofFieldsW = self.__tiaScreens.numOfFieldsW

        listenButtons = Frame(frame, bg = self.__colors.getColor("window"),
                              width=round(self.__topLevel.getTopLevelDimensions()[0]*0.08))
        listenButtons.pack_propagate(False)
        listenButtons.pack(side=LEFT, anchor=W, fill=Y)

        setPanel = Frame(frame, bg = self.__colors.getColor("window"),
                         width=round(self.__topLevel.getTopLevelDimensions()[0]*0.92))
        setPanel.pack_propagate(False)
        setPanel.pack(side=LEFT, anchor=W, fill=BOTH)

        YPoz = 0
        counter = 0

        for theY in range(start-1, end, -1):
            baseH = round(frameH / numofFieldsH)
            H = baseH
            baseW = round(round(self.__topLevel.getTopLevelDimensions()[0]*0.85) / numofFieldsW)
            color1 = "white"
            color2 = "black"
            if pattern[counter] == 1:
                color1 = "black"
                color2 = "white"

            notes = self.__piaNotes.getTiaValue(theY, None)
            if (key == "tremble"):
                self.__soundPlayer.playSound("Pong")

                self.deleteKey(notes, "1")
                self.deleteKey(notes, "6")
            elif (key == "bass"):
                self.deleteKey(notes, "4")
                self.deleteKey(notes, "12")

            X = baseW*counter

            self.createPianoButtons(listenButtons, notes, baseW, H, YPoz, color1, color2)
            self.createEditorButtons(setPanel, baseW, H, YPoz, color1, color2, theY)

            #print(start, end-1, theY)
            counter+=1
            YPoz+=H
        self.__runningThreads-=1

    def createEditorButtons(self, frame, W, H, Y, colorBack, colorFont, theY):
        counter = 0
        for X in range(0, self.__tiaScreens.numOfFieldsW, 1):
            theX = X
            X = counter * W

            if self.__dividerLen > 1 and (counter + 1) % self.__dividerLen == 0:
                theW = round(W*0.95)
            else:
                theW = W

            f = Frame(frame, width=theW, height=H, bg=colorBack,
                      name = str(counter) + "," +str(theY))
            f.pack_propagate(False)
            f.place(x=X, y=Y)

            self.__frames[str(counter) + "," + str(theY)] = f

            self.__tiaScreens.setColorValue(theX, theY, colorBack)

            b = Button(f, width=theW, height=H, bg=colorBack,
                       fg=colorFont,
                       font=self.__tinyFont2,
                       name=str(counter) + "," + str(theY),
                       activebackground=self.__colors.getColor("highLight"))

            self.colorButton(theX, theY, b)
            b.pack_propagate(False)
            b.pack(fill=BOTH)
            self.__piaNoteTable[str(counter) + "," + str(theY)] = b
            counter+=1

            b.bind("<ButtonPress-1>", self.clickedButton)
            b.bind("<MouseWheel>", self.mouseWheel)
            b.bind("<Enter>", self.enterCommon)
            b.bind("<Leave>", self.leave)

    def clickedButton(self, event):
        if self.__runningThreads>0:
            return

        name = str(event.widget).split(".")[-1]
        Y, X = self.getXYfromName(name)

        buttonValues = self.__tiaScreens.getTileValue(X,Y)
        buttonValues["enabled"] = 1 - buttonValues["enabled"]

        if buttonValues["enabled"] == 0:
            self.__tiaScreens.setTileValue(X, Y, 0, 0, 0, 0)
            self.colorButton(X,Y,event.widget)
        else:
            self.eraseRow(X)
            self.setValues(X, Y)
            self.colorButton(X,Y,event.widget)

        self.changed = True

    def setValues(self, X, Y):
        notes = self.__piaNotes.getTiaValue(Y, None)

        if (Y > 31):
            self.deleteKey(notes, "1")
            self.deleteKey(notes, "6")
        elif (Y < 32):
            self.deleteKey(notes, "4")
            self.deleteKey(notes, "12")

        if Y > 88:
            note = self.drumSetNames[Y-89]
            C = int(note.split(",")[0])
            F = int(note.split(",")[1])

        elif len(notes) == 1:
            if type(notes[list(notes.keys())[0]]) == list:
                if self.__correctNotes > 0:
                    from random import randint
                    num = randint(0, len(notes[list(notes.keys())[0]])-1)

                    C = int(list(notes.keys())[0])
                    F = int(notes[list(notes.keys())[0]][num])
                else:
                    C = int(list(notes.keys())[0])
                    N = 0

                    for num in range(0,len(notes[list(notes.keys())[0]])):
                        N+=int(notes[list(notes.keys())[0]][num])

                    F = round(N / len(notes[list(notes.keys())[0]]))

            else:
                C = int(list(notes.keys())[0])
                F = int(notes[list(notes.keys())[0]])
        else:
            dominants = self.__tiaScreens.getDomimantChannel()

            C = None
            for num in dominants:
                if num in notes.keys():
                    C = num
                    F = notes[num]

            if C == None:
                C = int(list(notes.keys())[0])
                F = int(notes[list(notes.keys())[0]])

        self.__tiaScreens.setTileValue(X, Y, 8, C, F, 1)
        if self.__buzz == 1 and C == 6:
            C = 7
        self.__piaNotes.playTia(8, C, F)

    def eraseRow(self, X):
        for Y in range(0,100):
            try:
                self.__tiaScreens.setTileValue(X, Y, 0, 0, 0, 0)
                self.colorButton(X,Y,self.__piaNoteTable[str(X)+","+str(Y)])
            except:
                pass

        self.__tiaScreens.setMinusOne(X)

    def colorButton(self, X, Y, button):
        buttonValues = self.__tiaScreens.getTileValue(X, Y)

        if buttonValues["enabled"] == 0:

            if (self.__tiaScreens.currentChannel < 3 or
                self.__tiaScreens.getIfUpperIsOccupied(X) == False):

                if buttonValues["color"] == "white":
                    color2 = "black"
                else:
                    color2 = "white"
                button.config(bg = buttonValues["color"], fg = color2, text = "")
            else:
                button.config(bg=self.__colors.getColor("fontDisabled"),
                              fg=self.__colors.getColor("font"),
                              text="")

        else:
            if (self.__tiaScreens.currentChannel < 3 or
                self.__tiaScreens.getIfUpperIsOccupied(X) == False):

                button.config(bg = self.__colors.getColor("boxBackUnSaved"),
                              fg = self.__colors.getColor("boxFontUnSaved"),
                              text = str(buttonValues["volume"]))
            else:
                button.config(bg = self.__colors.getColor("fontDisabled"),
                              fg = self.__colors.getColor("boxFontUnSaved"),
                              text = str(buttonValues["volume"]))



    def createPianoButtons(self, frame, notes, W, H, Y, colorBack, colorFont):
        counter = 0
        for channel in notes.keys():
            if type(notes[channel]) != list:
                X = counter * W
                #print(Y*H)
                f = Frame(frame, width=W, height=H, bg = colorBack)
                f.pack_propagate(False)
                f.place(x=X, y=Y)

                b = Button(f, width=W, height=H, bg = colorBack,
                           fg = colorFont, text=str(channel) + ": " + str(notes[channel]),
                           font=self.__tinyFont,
                           name = str(channel) + "," + str(notes[channel]),
                           activebackground=self.__colors.getColor("highLight")
                           )

                #self.__piaNoteTable[str(channel) + "," + str(notes[channel])] = b

                b.bind("<ButtonPress-1>", self.playNote1)
                #b.bind("<ButtonPress-1>", self.released())

                b.pack_propagate(False)
                b.pack(fill=BOTH)

                if channel == "6":
                    counter+=1
                    X = counter * W

                    f = Frame(frame, width=W, height=H, bg=colorBack)
                    f.pack_propagate(False)
                    f.place(x=X, y=Y)

                    b = Button(f, width=W, height=H, bg=colorBack,
                               fg=colorFont, text = "7: " + str(notes[channel]),
                               font=self.__tinyFont,
                               name="7," + str(notes[channel]),
                               activebackground=self.__colors.getColor("highLight")
                               )

                    b.bind("<ButtonPress-1>", self.playNote1)
                    # b.bind("<ButtonPress-1>", self.released())

                    b.pack_propagate(False)
                    b.pack(fill=BOTH)

            #self.__piaNoteTable
            counter +=1

    def playNote1(self, event):
        name = str(event.widget).split(".")[-1]
        note, channel = self.getXYfromName(name)
        self.__piaNotes.playTia(8, int(channel), int(note))


    def deleteKey(self, d, key):
        try:
            del d[key]
        except:
            pass

    def mouseWheel(self, event):
        if self.__runningThreads>0:
            return

        buttonValues = self.buttonValuesFromWidget(event.widget)

        if buttonValues["volume"] == 0:
            return
        elif event.delta == 120:
            if buttonValues["volume"] == 15:
                V = 1
            else:
                V = buttonValues["volume"] + 1
        else:
            if buttonValues["volume"] == 1:
                V = 15
            else:
                V = buttonValues["volume"] - 1

        event.widget.config(text=str(V))
        name = str(event.widget).split(".")[-1]
        Y, X = self.getXYfromName(name)
        self.__tiaScreens.setTileValue(X, Y,
                                    V ,
                                    buttonValues["channel"],
                                    buttonValues["freq"],
                                    1)
        self.changed = True

    def buttonValuesFromWidget(self, w):
        name = str(w).split(".")[-1]
        Y, X = self.getXYfromName(name)
        return self.__tiaScreens.getTileValue(X, Y)




    def enterCommon(self, event):
        if self.__runningThreads > 0:
            return

        if self.__draw == 1:
            buttonValues = self.buttonValuesFromWidget(event.widget)

            if self.__ctrl == False:
                if buttonValues["enabled"] == 1:
                    self.__tiaScreens.setTileValue(X, Y, 0, 0, 0, 0)
                    self.colorButton(X, Y, event.widget)
            else:
                if buttonValues["enabled"] == 0:
                    self.eraseRow(X)
                    self.setValues(X, Y)
                    self.colorButton(X, Y, event.widget)

            self.changed = True


        self.__choosenOne = event.widget


        """
        if self.__ctrl == True:
            name = str(event.widget).split(".")[-1]
            Y, X = self.getXYfromName(name)
            buttonValues = self.__tiaScreens.getTileValue(X, Y)

            if buttonValues["enabled"] == 1 and self.__pressed["3"] == True:
                self.__tiaScreens.setTileValue(X, Y, 0, 0, 0, 0)
                self.colorButton(X, Y, event.widget)
            if buttonValues["enabled"] == 0 and self.__pressed["1"] == True:
                self.eraseRow(X)
                self.setValues(X, Y)
                self.colorButton(X, Y, event.widget)
        """

    def leave(self, event):
        self.__choosenOne = None

    def focusIn(self, event):
        self.focused = event.widget

    def focusOut(self, event):
        self.focused = None

    def shiftON(self, event):
        self.__ctrl = True

    def shiftOff(self, event):
        self.__ctrl = False

    def getXYfromName(self, w):
        name = str(w).split(".")[-1]
        try:
            Y = int(name.split(",")[0])
            X = int(name.split(",")[1])
            return X,Y
        except:
            return