from tkinter import *
from SubMenu import SubMenu

class MemoryManagerWindow:

    def __init__(self, loader):
        self.__loader = loader
        self.firstLoad = True
        self.__loader.stopThreads.append(self)
        self.dead = False

        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs
        self.__fontManager = self.__loader.fontManager
        self.__fontSize = int(self.__screenSize[0]/1300 * self.__screenSize[1]/1050*14)
        self.__colors = self.__loader.colorPalettes
        self.__colorDict = self.__loader.colorDict
        self.__memory = self.__loader.virtualMemory.memory
        self.__arrays = self.__loader.virtualMemory.arrays
        self.__virtualMemory = self.__loader.virtualMemory

        self.__focused = None
        self.__screenSize = self.__loader.screenSize
        self.__lastBullShit = None

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize*0.65), False, False, False)
        self.__tinyFont = self.__fontManager.getFont(int(self.__fontSize*0.45), False, False, False)
        self.__halfFont = self.__fontManager.getFont(int(self.__fontSize*0.57), False, False, False)

        self.__selectedArr = ""
        self.__selectedVar = ""

        self.__activeVar   = ""
        self.__activeArr   = ""

        self.__varBuffer = []

        self.__selectedInc = ""
        self.__selectedAva = ""

        self.__changed = False
        self.__changedBanks = set()

        self.__changeArrBoxes = True

        self.__sizes = {
            "common": [round(self.__screenSize[0] / 1.3), round(self.__screenSize[1]/1.50  - 25)]
        }


        self.__window = SubMenu(self.__loader, "memoryManager", self.__sizes["common"][0],
                                self.__sizes["common"][1], None, self.__addElements, 1)

        self.dead = True

    def __closeWindow(self):
        if self.__changed == True:
           answer = self.__fileDialogs.askYesOrNo("unsaved", "unsavedText")
           if answer == "Yes":
              self.saveAllBank()

        self.dead = True
        self.__topLevelWindow.destroy()
        self.__loader.topLevels.remove(self.__topLevelWindow)

    def __addElements(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()
        self.__topLevelWindow.protocol('WM_DELETE_WINDOW', self.__closeWindow)

        self.__bankChangerFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"),
                                 height= self.__topLevel.getTopLevelDimensions()[1]//19)
        self.__bankChangerFrame.pack_propagate(False)
        self.__bankChangerFrame.pack(side=TOP, anchor=N, fill=X)

        self.__bankButtons = {}

        for num in range(1, 9):

            f = Frame(self.__bankChangerFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                            width= self.__topLevel.getTopLevelDimensions()[0] // 11,
                                            height=self.__topLevel.getTopLevelDimensions()[1] // 19)
            f.pack_propagate(False)
            f.pack(side=LEFT, anchor=E, fill=Y)

            name = str(num)
            if name == "1":
               name = "global"
            else:
               name = "bank" + name

            b = Button(f, name = name, bg=self.__loader.colorPalettes.getColor("window"),
                        text = name, font = self.__smallFont, width=999999999)
            b.pack_propagate(False)
            b.pack(fill=BOTH)
            b.bind("<Button-1>", self.getNameAndChange)
            self.__bankButtons[num] = [f, b]

        self.__variableHeader = Label(self.__bankChangerFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                      fg=self.__loader.colorPalettes.getColor("font"),
                                 text = self.__dictionaries.getWordFromCurrentLanguage("variables"),
                                 font = self.__normalFont, justify = CENTER
                                      )
        self.__variableHeader.pack_propagate(False)
        self.__variableHeader.pack(side=TOP, anchor=N, fill=BOTH)


        self.__bigFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"),
                                width=self.__topLevel.getTopLevelDimensions()[0],
                                height=self.__topLevel.getTopLevelDimensions()[1] // 19 * 18)

        self.__bigFrame.pack_propagate(False)
        self.__bigFrame.pack(side=TOP, anchor=N, fill=BOTH)

        self.__listBoxesFrame = Frame(self.__bigFrame, bg=self.__loader.colorPalettes.getColor("window"),
                            width = self.__variableHeader.winfo_width())
        self.__listBoxesFrame.pack_propagate(False)
        self.__listBoxesFrame.pack(side=RIGHT, anchor=W, fill=Y)

        self.__variableListBoxFrame = Frame(self.__listBoxesFrame, bg=self.__loader.colorPalettes.getColor("window"),
                            width = self.__variableHeader.winfo_width(),
                            height=round(self.__topLevel.getTopLevelDimensions()[1] // 5 * 2.25 ) - (self.__topLevel.getTopLevelDimensions()[1] // 19 )
                                      )
        self.__variableListBoxFrame.pack_propagate(False)
        self.__variableListBoxFrame.pack(side=TOP, anchor=N, fill=X)

        self.__listBoxScrollBar = Scrollbar(self.__variableListBoxFrame)
        self.__variableListBox = Listbox(   self.__variableListBoxFrame, width=100000,
                                    height=1000,
                                    yscrollcommand=self.__listBoxScrollBar.set,
                                    selectmode=BROWSE,
                                    exportselection = False,
                                    font = self.__smallFont
                                    )
        self.__variableListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__variableListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__variableListBox.pack_propagate(False)

        self.__insertVarButtonFrame = Frame(self.__listBoxesFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                            width= self.__variableHeader.winfo_width(),
                                            height=self.__topLevel.getTopLevelDimensions()[1] // 19)
        self.__insertVarButtonFrame.pack_propagate(False)
        self.__insertVarButtonFrame.pack(side=TOP, anchor=N, fill=X)

        self.__insertVarButton = Button(self.__insertVarButtonFrame,
                                        bg=self.__loader.colorPalettes.getColor("window"),
                                        text = self.__dictionaries.getWordFromCurrentLanguage("selectVar"),
                                        font = self.__smallFont, width=999999999, state = DISABLED,
                                        command = self.insertVar
                                        )
        self.__insertVarButton.pack_propagate(False)
        self.__insertVarButton.pack(side=TOP, anchor=N, fill=BOTH)

        self.__listBoxScrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__variableListBox.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__listBoxScrollBar.config(command=self.__variableListBox.yview)

        self.__arrayHeader = Label(self.__listBoxesFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                      fg=self.__loader.colorPalettes.getColor("font"),
                                 text = self.__dictionaries.getWordFromCurrentLanguage("arrays"),
                                 font = self.__normalFont, justify = CENTER
                                      )
        self.__arrayHeader.pack_propagate(False)
        self.__arrayHeader.pack(side=TOP, anchor=N, fill=X)

        self.__arrayListBoxFrame = Frame(self.__listBoxesFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                            width=self.__variableHeader.winfo_width(),
                                            height=round(self.__topLevel.getTopLevelDimensions()[1] // 5 * 2) - (
                                                        self.__topLevel.getTopLevelDimensions()[1] // 19)
                                            )
        self.__arrayListBoxFrame.pack_propagate(False)
        self.__arrayListBoxFrame.pack(side=TOP, anchor=N, fill=BOTH)

        self.__arrayListBoxScrollBar = Scrollbar(self.__arrayListBoxFrame)
        self.__arrayListBox = Listbox(self.__arrayListBoxFrame, width=100000,
                                         height=1000,
                                         yscrollcommand=self.__arrayListBoxScrollBar.set,
                                         selectmode=BROWSE,
                                         exportselection=False,
                                         font=self.__smallFont
                                         )
        self.__arrayListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__arrayListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__arrayListBox.pack_propagate(False)

        self.__arrayListBoxScrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__arrayListBox.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__arrayListBoxScrollBar.config(command=self.__variableListBox.yview)

        self.__insertArrButtonFrame = Frame(self.__listBoxesFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                            width= self.__variableHeader.winfo_width(),
                                            height=self.__topLevel.getTopLevelDimensions()[1] // 19)
        self.__insertArrButtonFrame.pack_propagate(False)
        self.__insertArrButtonFrame.pack(side=TOP, anchor=N, fill=X)

        self.__insertArrButton = Button(self.__insertArrButtonFrame,
                                        bg=self.__loader.colorPalettes.getColor("window"),
                                        text = self.__dictionaries.getWordFromCurrentLanguage("selectArray"),
                                        font = self.__smallFont, width=999999999, state = DISABLED,
                                        command=self.insertArr)
        self.__insertArrButton.pack_propagate(False)
        self.__insertArrButton.pack(side=TOP, anchor=N, fill=BOTH)

        self.__listBoxScrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__variableListBox.pack(side=LEFT, anchor=W, fill=BOTH)


        self.__allTheOthers = Frame(self.__bigFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                            width=self.__topLevel.getTopLevelDimensions()[0] - self.__variableHeader.winfo_width(),
                                            height=self.__topLevel.getTopLevelDimensions()[1] // 19 * 18)

        self.__allTheOthers.pack_propagate(False)
        self.__allTheOthers.pack(side=RIGHT, anchor=W, fill=BOTH)

        self.__freeMemoryFrameNames = Frame(self.__allTheOthers, bg=self.__loader.colorPalettes.getColor("window"),
                                            width=self.__topLevel.getTopLevelDimensions()[0] - self.__variableHeader.winfo_width(),
                                            height=self.__topLevel.getTopLevelDimensions()[1] // 19)

        self.__freeMemoryFrameNames.pack_propagate(False)
        self.__freeMemoryFrameNames.pack(side=TOP, anchor=N, fill=X)

        self.__freeMemoryFrameValues = Frame(self.__allTheOthers, bg=self.__loader.colorPalettes.getColor("window"),
                                            width=self.__topLevel.getTopLevelDimensions()[0] - self.__variableHeader.winfo_width(),
                                            height=self.__topLevel.getTopLevelDimensions()[1] // 19)

        self.__freeMemoryFrameValues.pack_propagate(False)
        self.__freeMemoryFrameValues.pack(side=TOP, anchor=N, fill=X)

        self.__freeMamoryNames = []
        self.__freeMamoryValues = []
        self.__freeMamoryTexts = []
        names = [
            "basicRam", "basicRamLocal", "saraRam", "saraRamLocal"
        ]

        self.__fuckColors = [
            ["window", "font"], ["fontDisabled", "font"]
        ]

        for num in range(0,4):
            F = Frame(self.__freeMemoryFrameNames, bg=self.__loader.colorPalettes.getColor("window"),
                      width=(self.__topLevel.getTopLevelDimensions()[0] - self.__variableHeader.winfo_width()) // 4,
                      height=self.__topLevel.getTopLevelDimensions()[1] // 19)

            F.pack_propagate(False)
            F.pack(side=LEFT, anchor=E, fill=Y)

            L = Label(F, bg=self.__loader.colorPalettes.getColor(self.__fuckColors[num%2][0]),
                         fg=self.__loader.colorPalettes.getColor(self.__fuckColors[num%2][1]), justify = CENTER,
                         width=999999, font = self.__halfFont,
                         text = self.__dictionaries.getWordFromCurrentLanguage(names[num]))

            L.pack_propagate(False)
            L.pack(side=BOTTOM, anchor=S, fill=BOTH)
            self.__freeMamoryNames.append(L)

            textShit = StringVar()

            F = Frame(self.__freeMemoryFrameValues, bg=self.__loader.colorPalettes.getColor("window"),
                      width=(self.__topLevel.getTopLevelDimensions()[0] - self.__variableHeader.winfo_width()) // 4,
                      height=self.__topLevel.getTopLevelDimensions()[1] // 19)

            F.pack_propagate(False)
            F.pack(side=LEFT, anchor=E, fill=Y)

            L = Label(F, bg=self.__loader.colorPalettes.getColor(self.__fuckColors[num%2][0]),
                         fg=self.__loader.colorPalettes.getColor(self.__fuckColors[num%2][1]), justify = CENTER,
                         width=999999, font = self.__smallFont,
                         textvariable = textShit)

            L.pack_propagate(False)
            L.pack(side=BOTTOM, anchor=S, fill=BOTH)
            self.__freeMamoryValues.append(L)
            self.__freeMamoryTexts.append(textShit)

        self.__variableFrame = Frame(self.__allTheOthers, bg=self.__loader.colorPalettes.getColor("window"),
                      width=(self.__topLevel.getTopLevelDimensions()[0] - self.__variableHeader.winfo_width()) // 4,
                      height=self.__topLevel.getTopLevelDimensions()[1] // 19 * 8)

        self.__variableFrame.pack_propagate(False)
        self.__variableFrame.pack(side=TOP, anchor=N, fill=X)

        self.__arrayFrame = Frame(self.__allTheOthers, bg=self.__loader.colorPalettes.getColor("window"),
                      width=(self.__topLevel.getTopLevelDimensions()[0] - self.__variableHeader.winfo_width()) // 4,
                      height=self.__topLevel.getTopLevelDimensions()[1] // 19 * 10)

        self.__arrayFrame.pack_propagate(False)
        self.__arrayFrame.pack(side=TOP, anchor=N, fill=BOTH)

        self.__variableFrameTitle = Frame(self.__variableFrame, bg=self.__loader.colorPalettes.getColor("font"),
                      width=(self.__topLevel.getTopLevelDimensions()[0] - self.__variableHeader.winfo_width()),
                      height=self.__topLevel.getTopLevelDimensions()[1] // 19)

        self.__variableFrameTitle.pack_propagate(False)
        self.__variableFrameTitle.pack(side=TOP, anchor=N, fill=X)

        self.__arrayFrameTitle = Frame(self.__arrayFrame, bg=self.__loader.colorPalettes.getColor("font"),
                      width=(self.__topLevel.getTopLevelDimensions()[0] - self.__variableHeader.winfo_width()),
                      height=self.__topLevel.getTopLevelDimensions()[1] // 19)

        self.__arrayFrameTitle.pack_propagate(False)
        self.__arrayFrameTitle.pack(side=TOP, anchor=N, fill=X)

        self.__variableTitle = Label(self.__variableFrameTitle, bg=self.__loader.colorPalettes.getColor("font"),
                                      fg=self.__loader.colorPalettes.getColor("window"), justify = LEFT,
                                 text = " " + self.__dictionaries.getWordFromCurrentLanguage("manageVariable"),
                                 font = self.__normalFont)
        self.__variableTitle.pack_propagate(False)
        self.__variableTitle.pack(side=LEFT, anchor=E, fill=X)

        self.__arrayTitle = Label(self.__arrayFrameTitle, bg=self.__loader.colorPalettes.getColor("font"),
                                  fg=self.__loader.colorPalettes.getColor("window"), justify = LEFT,
                                 text = " " + self.__dictionaries.getWordFromCurrentLanguage("manageArray"),
                                 font = self.__normalFont)
        self.__arrayTitle.pack_propagate(False)
        self.__arrayTitle.pack(side=LEFT, anchor=E, fill=X)

        self.__varNameFrame = Frame(self.__variableFrame, bg=self.__loader.colorPalettes.getColor("window"),
                      width=(self.__topLevel.getTopLevelDimensions()[0] - self.__variableHeader.winfo_width()),
                      height=self.__topLevel.getTopLevelDimensions()[1] // 19)

        self.__varNameFrame.pack_propagate(False)
        self.__varNameFrame.pack(side=TOP, anchor=N, fill=X)

        self.__varNameLabel = Label(self.__varNameFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                      fg=self.__loader.colorPalettes.getColor("font"), justify = LEFT,
                                 text = " " + self.__dictionaries.getWordFromCurrentLanguage("varName"),
                                 font = self.__smallFont)
        self.__varNameLabel.pack_propagate(False)
        self.__varNameLabel.pack(side=LEFT, anchor=E, fill=Y)

        self.__varName = StringVar()
        self.__varNameEntry =  Entry(self.__varNameFrame, name="varEntry",
                               bg=self.__colors.getColor("boxBackNormal"),
                               fg=self.__colors.getColor("boxFontNormal"),
                               width=30,
                               textvariable=self.__varName,
                               font=self.__smallFont)

        self.__varNameEntry.pack_propagate(False)
        self.__varNameEntry.pack(side=LEFT, anchor=E, fill=Y)

        self.__varNameEntry.bind("<KeyRelease>", self.checkIfValid)
        self.__varNameEntry.bind("<FocusOut>", self.checkIfValid)

        self.__varError = StringVar()
        self.__varErrorLabel = Label(self.__varNameFrame, width=9999999,
                                     bg=self.__loader.colorPalettes.getColor("font"),
                                     fg=self.__loader.colorPalettes.getColor("highLight"),
                                     textvariable = self.__varError, font = self.__miniFont)

        self.__varErrorLabel.pack_propagate(False)
        self.__varErrorLabel.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__varOOO = Frame(self.__variableFrame, bg=self.__loader.colorPalettes.getColor("window"),
                      width=(self.__topLevel.getTopLevelDimensions()[0] - self.__variableHeader.winfo_width()),
                      height=self.__topLevel.getTopLevelDimensions()[1] // 19 * 19)

        self.__varOOO.pack_propagate(False)
        self.__varOOO.pack(side=TOP, anchor=N, fill=BOTH)


        self.__varTypeFrame = Frame(self.__varOOO, bg=self.__loader.colorPalettes.getColor("window"),
                      width=self.__varNameLabel.winfo_width(),
                      height=9999999999)

        self.__varTypeFrame.pack_propagate(False)
        self.__varTypeFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__typeListBox = Listbox(   self.__varTypeFrame, width=100000,
                                    height=1000, justify = CENTER,
                                    selectmode=BROWSE,
                                    exportselection = False,
                                    font = self.__smallFont
                                    )
        self.__typeListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__typeListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__typeListBox.pack_propagate(False)
        self.__typeListBox.pack(fill=BOTH)

        self.__typeListBox.bind("<ButtonRelease-1>", self.__changeVarType)
        self.__typeListBox.bind("<KeyRelease-Up>", self.__changeVarType)
        self.__typeListBox.bind("<KeyRelease-Down>", self.__changeVarType)

        self.__varTypes = self.__virtualMemory.types

        for item in self.__varTypes:
            self.__typeListBox.insert(END, item)

        self.__varWWW = Frame(self.__varOOO, bg="black",
                      width=9999999,
                      height=self.__topLevel.getTopLevelDimensions()[1] // 19)

        self.__varWWW.pack_propagate(False)
        self.__varWWW.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__varIndicatorsFrame = Frame(self.__varWWW, bg=self.__loader.colorPalettes.getColor("window"),
                      width=(self.__topLevel.getTopLevelDimensions()[0] - self.__variableHeader.winfo_width()-self.__varNameLabel.winfo_width()),
                      height=self.__topLevel.getTopLevelDimensions()[1] // 19)

        self.__varIndicatorsFrame.pack_propagate(False)
        self.__varIndicatorsFrame.pack(side=TOP, anchor=N, fill=X)

        self.__varIndicatorFrameAddress = Frame(self.__varIndicatorsFrame, bg=self.__loader.colorPalettes.getColor("window"),
                      width = (self.__topLevel.getTopLevelDimensions()[0] -
                               self.__variableHeader.winfo_width()-
                               self.__varNameLabel.winfo_width()) // 2,
                      height=self.__topLevel.getTopLevelDimensions()[1] // 19)
        self.__varIndicatorFrameAddress.pack_propagate(False)
        self.__varIndicatorFrameAddress.pack(side=LEFT, anchor=E, fill=Y)


        self.__varIndicatorAddress = Label(self.__varIndicatorFrameAddress,
                                                bg=self.__loader.colorPalettes.getColor("fontDisabled"),
                                           text = self.__dictionaries.getWordFromCurrentLanguage("varAddress"),
                                           fg = self.__loader.colorPalettes.getColor("font"),
                                           justify = CENTER, font = self.__smallFont
                                           )

        self.__varIndicatorAddress.pack_propagate(False)
        self.__varIndicatorAddress.pack(side=TOP, anchor=N, fill=BOTH)

        self.__varIndicatorFrameBits = Frame(self.__varIndicatorsFrame, bg=self.__loader.colorPalettes.getColor("window"),
                      width = (self.__topLevel.getTopLevelDimensions()[0] -
                               self.__variableHeader.winfo_width()-
                               self.__varNameLabel.winfo_width()) // 2,
                      height=self.__topLevel.getTopLevelDimensions()[1] // 19)
        self.__varIndicatorFrameBits.pack_propagate(False)
        self.__varIndicatorFrameBits.pack(side=LEFT, anchor=E, fill=BOTH)


        self.__varIndicatorBits = Label(self.__varIndicatorFrameBits,
                                                bg=self.__loader.colorPalettes.getColor("fontDisabled"),
                                           text = self.__dictionaries.getWordFromCurrentLanguage("usedBits"),
                                           fg = self.__loader.colorPalettes.getColor("font"),
                                           justify = CENTER, font = self.__smallFont
                                           )

        self.__varIndicatorBits.pack_propagate(False)
        self.__varIndicatorBits.pack(side=TOP, anchor=N, fill=BOTH)

        self.__varIndicators2Frame = Frame(self.__varWWW, bg=self.__loader.colorPalettes.getColor("window"),
                      width=(self.__topLevel.getTopLevelDimensions()[0] - self.__variableHeader.winfo_width()-self.__varNameLabel.winfo_width()),
                      height=self.__topLevel.getTopLevelDimensions()[1] // 19)

        self.__varIndicators2Frame.pack_propagate(False)
        self.__varIndicators2Frame.pack(side=TOP, anchor=N, fill=X)

        self.__varCheckBoxes = Frame(self.__varWWW, bg=self.__loader.colorPalettes.getColor("window"),
                      width=(self.__topLevel.getTopLevelDimensions()[0] - self.__variableHeader.winfo_width()-self.__varNameLabel.winfo_width()),
                      height=self.__topLevel.getTopLevelDimensions()[1] // 19)

        self.__varCheckBoxes.pack_propagate(False)
        self.__varCheckBoxes.pack(side=TOP, anchor=N, fill=X)

        self.__colorVarMode = IntVar()
        self.__bcdMode      = IntVar()

        self.__colorButton = Checkbutton(self.__varCheckBoxes, width=len(self.__dictionaries.getWordFromCurrentLanguage("colorVar")),
                                             text=self.__dictionaries.getWordFromCurrentLanguage("colorVar"),
                                             bg=self.__colors.getColor("window"),
                                             fg=self.__colors.getColor("font"),
                                             justify=LEFT, font=self.__smallFont,
                                             variable=self.__colorVarMode,
                                             activebackground=self.__colors.getColor("highLight"),
                                             command=None
                                             )

        self.__colorButton.pack_propagate(False)
        self.__colorButton.pack(fill=Y, side=LEFT, anchor=E)

        self.__bcdButton = Checkbutton(self.__varCheckBoxes, width=len(self.__dictionaries.getWordFromCurrentLanguage("bcd")),
                                             text=self.__dictionaries.getWordFromCurrentLanguage("bcd"),
                                             bg=self.__colors.getColor("window"),
                                             fg=self.__colors.getColor("font"),
                                             justify=LEFT, font=self.__smallFont,
                                             variable=self.__bcdMode,
                                             activebackground=self.__colors.getColor("highLight"),
                                             command=None
                                             )

        self.__bcdButton.pack_propagate(False)
        self.__bcdButton.pack(fill=Y, side=LEFT, anchor=E)

        self.__address = StringVar()
        self.__bits    = StringVar()

        self.__address.set("-")
        self.__bits.set("-")

        self.__varIndicatorFrameAddressVal = Frame(self.__varIndicators2Frame, bg=self.__loader.colorPalettes.getColor("window"),
                      width = (self.__topLevel.getTopLevelDimensions()[0] -
                               self.__variableHeader.winfo_width()-
                               self.__varNameLabel.winfo_width()) // 2,
                      height=self.__topLevel.getTopLevelDimensions()[1] // 19)
        self.__varIndicatorFrameAddressVal.pack_propagate(False)
        self.__varIndicatorFrameAddressVal.pack(side=LEFT, anchor=E, fill=Y)


        self.__varIndicatorAddressVal = Label(self.__varIndicatorFrameAddressVal,
                                                bg=self.__loader.colorPalettes.getColor("window"),
                                           textvariable = self.__address,
                                           fg = self.__loader.colorPalettes.getColor("font"),
                                           justify = CENTER, font = self.__smallFont
                                           )

        self.__varIndicatorAddressVal.pack_propagate(False)
        self.__varIndicatorAddressVal.pack(side=TOP, anchor=N, fill=BOTH)

        self.__varIndicatorFrameBitsVal = Frame(self.__varIndicators2Frame, bg=self.__loader.colorPalettes.getColor("window"),
                      width = (self.__topLevel.getTopLevelDimensions()[0] -
                               self.__variableHeader.winfo_width()-
                               self.__varNameLabel.winfo_width()) // 2,
                      height=self.__topLevel.getTopLevelDimensions()[1] // 19)
        self.__varIndicatorFrameBitsVal.pack_propagate(False)
        self.__varIndicatorFrameBitsVal.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__varIndicatorBitsVal = Label(self.__varIndicatorFrameBitsVal,
                                                bg=self.__loader.colorPalettes.getColor("window"),
                                           textvariable = self.__bits,
                                           fg = self.__loader.colorPalettes.getColor("font"),
                                           justify = CENTER, font = self.__smallFont
                                           )

        self.__varIndicatorBitsVal.pack_propagate(False)
        self.__varIndicatorBitsVal.pack(side=TOP, anchor=N, fill=BOTH)

        self.__varButtons = Frame(self.__varWWW, bg=self.__loader.colorPalettes.getColor("window"),
                      width=(self.__topLevel.getTopLevelDimensions()[0] - self.__variableHeader.winfo_width()-self.__varNameLabel.winfo_width()),
                      height=self.__topLevel.getTopLevelDimensions()[1] // 19)

        self.__varButtons.pack_propagate(False)
        self.__varButtons.pack(side=TOP, anchor=N, fill=X)

        self.__createButtonFrame = Frame(self.__varButtons, bg=self.__loader.colorPalettes.getColor("window"),
                      width=self.__varButtons.winfo_width()//3,
                      height=self.__topLevel.getTopLevelDimensions()[1] // 19)

        self.__createButtonFrame.pack_propagate(False)
        self.__createButtonFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__createButton = Button(self.__createButtonFrame,
                                        bg=self.__loader.colorPalettes.getColor("window"),
                                        text = self.__dictionaries.getWordFromCurrentLanguage("create"),
                                        font = self.__smallFont, width=999999999, state = DISABLED,
                                        command = self.createVar
                                        )
        self.__createButton.pack_propagate(False)
        self.__createButton.pack(side=TOP, anchor=N, fill=BOTH)

        self.__modifyButtonFrame = Frame(self.__varButtons, bg=self.__loader.colorPalettes.getColor("window"),
                      width=self.__varButtons.winfo_width()//3,
                      height=self.__topLevel.getTopLevelDimensions()[1] // 19)

        self.__modifyButtonFrame.pack_propagate(False)
        self.__modifyButtonFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__modifyButton = Button(self.__modifyButtonFrame,
                                        bg=self.__loader.colorPalettes.getColor("window"),
                                        text = self.__dictionaries.getWordFromCurrentLanguage("modify"),
                                        font = self.__smallFont, width=999999999, state = DISABLED,
                                        command = self.modifyVar
                                        )
        self.__modifyButton.pack_propagate(False)
        self.__modifyButton.pack(side=TOP, anchor=N, fill=BOTH)

        self.__deleteButtonFrame = Frame(self.__varButtons, bg=self.__loader.colorPalettes.getColor("window"),
                      width=self.__varButtons.winfo_width()//3,
                      height=self.__topLevel.getTopLevelDimensions()[1] // 19)

        self.__deleteButtonFrame.pack_propagate(False)
        self.__deleteButtonFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__deleteButton = Button(self.__deleteButtonFrame,
                                        bg=self.__loader.colorPalettes.getColor("window"),
                                        text = self.__dictionaries.getWordFromCurrentLanguage("delete"),
                                        font = self.__smallFont, width=999999999, state = DISABLED,
                                        command = self.deleteVar
                                        )
        self.__deleteButton.pack_propagate(False)
        self.__deleteButton.pack(side=TOP, anchor=N, fill=BOTH)

        self.__arrNameFrame = Frame(self.__arrayFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                    width=(self.__topLevel.getTopLevelDimensions()[
                                               0] - self.__variableHeader.winfo_width()),
                                    height=self.__topLevel.getTopLevelDimensions()[1] // 19)

        self.__arrNameFrame.pack_propagate(False)
        self.__arrNameFrame.pack(side=TOP, anchor=N, fill=X)

        self.__arrNameFrameFrame = Frame(self.__arrNameFrame, bg=self.__loader.colorPalettes.getColor("window"),
                      width=self.__varNameLabel.winfo_width(),
                      height=9999999999)

        self.__arrNameFrameFrame.pack_propagate(False)
        self.__arrNameFrameFrame.pack(side=LEFT, anchor=E, fill=Y)


        self.__arrNameLabel = Label(self.__arrNameFrameFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                    fg=self.__loader.colorPalettes.getColor("font"), justify=LEFT,
                                    text=" " + self.__dictionaries.getWordFromCurrentLanguage("arrName"),
                                    font=self.__smallFont)
        self.__arrNameLabel.pack_propagate(False)
        self.__arrNameLabel.pack(side=LEFT, anchor=E, fill=Y)

        self.__arrName = StringVar()
        self.__arrNameEntry = Entry(self.__arrNameFrame, name="arrEntry",
                                    bg=self.__colors.getColor("boxBackNormal"),
                                    fg=self.__colors.getColor("boxFontNormal"),
                                    width=30,
                                    textvariable=self.__arrName,
                                    font=self.__smallFont)

        self.__arrNameEntry.pack_propagate(False)
        self.__arrNameEntry.pack(side=LEFT, anchor=E, fill=Y)

        self.__arrNameEntry.bind("<KeyRelease>", self.checkIfValid)
        self.__arrNameEntry.bind("<FocusOut>", self.checkIfValid)

        self.__arrError = StringVar()
        self.__arrErrorLabel = Label(self.__arrNameFrame, width=9999999,
                                     bg=self.__loader.colorPalettes.getColor("font"),
                                     fg=self.__loader.colorPalettes.getColor("highLight"),
                                     textvariable=self.__arrError, font=self.__miniFont)

        self.__arrErrorLabel.pack_propagate(False)
        self.__arrErrorLabel.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__buttonsFrame = Frame(self.__arrayFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                    width=(self.__topLevel.getTopLevelDimensions()[
                                               0] - self.__variableHeader.winfo_width()),
                                    height=self.__topLevel.getTopLevelDimensions()[1] // 19)

        self.__buttonsFrame.pack_propagate(False)
        self.__buttonsFrame.pack(side=BOTTOM, anchor=S, fill=X)

        self.__arrMain = Frame(self.__arrayFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                    width=(self.__topLevel.getTopLevelDimensions()[
                                               0] - self.__variableHeader.winfo_width()),
                                    height=self.__topLevel.getTopLevelDimensions()[1])

        self.__arrMain.pack_propagate(False)
        self.__arrMain.pack(side=BOTTOM, anchor=S, fill=BOTH)

        self.__arrButtonsFrame = Frame(self.__arrMain, bg=self.__loader.colorPalettes.getColor("window"),
                      width=self.__varNameLabel.winfo_width(),
                      height=9999999999)

        self.__arrButtonsFrame.pack_propagate(False)
        self.__arrButtonsFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__moveButtonsFrame = Frame(self.__arrButtonsFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                    width=(self.__topLevel.getTopLevelDimensions()[
                                               0] - self.__variableHeader.winfo_width()),
                                    height=self.__topLevel.getTopLevelDimensions()[1] // 19)

        self.__moveButtonsFrame.pack_propagate(False)
        self.__moveButtonsFrame.pack(side=TOP, anchor=N, fill=X)

        self.__moveButtonsFrame1 = Frame(self.__moveButtonsFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                    width=self.__varNameLabel.winfo_width() // 2,
                                    height=self.__topLevel.getTopLevelDimensions()[1] // 19)

        self.__moveButtonsFrame1.pack_propagate(False)
        self.__moveButtonsFrame1.pack(side=LEFT, anchor=E, fill=Y)

        self.__moveButtonsFrame2 = Frame(self.__moveButtonsFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                    width=self.__varNameLabel.winfo_width() // 2,
                                    height=self.__topLevel.getTopLevelDimensions()[1] // 19)

        self.__moveButtonsFrame2.pack_propagate(False)
        self.__moveButtonsFrame2.pack(side=LEFT, anchor=E, fill=Y)

        self.__arrMove1Button = Button(self.__moveButtonsFrame1,
                                        bg=self.__loader.colorPalettes.getColor("window"),
                                        text = "<<", width=99999,
                                        font = self.__normalFont, state = DISABLED,
                                        command = self.__moveToIncluded
                                        )
        self.__arrMove1Button.pack_propagate(False)
        self.__arrMove1Button.pack(side=LEFT, anchor=CENTER, fill=BOTH)

        self.__arrMove2Button = Button(self.__moveButtonsFrame2,
                                        bg=self.__loader.colorPalettes.getColor("window"),
                                        text = ">>", width=99999,
                                        font = self.__normalFont, state = DISABLED,
                                        command = self.__moveToAvailable
                                        )
        self.__arrMove2Button.pack_propagate(False)
        self.__arrMove2Button.pack(side=RIGHT, anchor=CENTER, fill=BOTH)

        self.__arrCreateButton = Button(self.__arrButtonsFrame,
                                        bg=self.__loader.colorPalettes.getColor("window"),
                                        text = self.__dictionaries.getWordFromCurrentLanguage("create"),
                                        font = self.__miniFont, width=999999999, state = DISABLED,
                                        command = self.__createArr
                                        )
        self.__arrCreateButton.pack_propagate(False)
        self.__arrCreateButton.pack(side=TOP, anchor=N, fill=X)

        self.__arrModifyButton = Button(self.__arrButtonsFrame,
                                        bg=self.__loader.colorPalettes.getColor("window"),
                                        text = self.__dictionaries.getWordFromCurrentLanguage("modify"),
                                        font = self.__miniFont, width=999999999, state = DISABLED,
                                        command = self.__modifyArr
                                        )
        self.__arrModifyButton.pack_propagate(False)
        self.__arrModifyButton.pack(side=TOP, anchor=N, fill=X)

        self.__arrDeleteButton = Button(self.__arrButtonsFrame,
                                        bg=self.__loader.colorPalettes.getColor("window"),
                                        text = self.__dictionaries.getWordFromCurrentLanguage("delete"),
                                        font = self.__miniFont, width=999999999, state = DISABLED,
                                        command = self.__deleteArr
                                        )
        self.__arrDeleteButton.pack_propagate(False)
        self.__arrDeleteButton.pack(side=TOP, anchor=N, fill=X)

        self.__arrListBoxFrame1 = Frame(self.__arrMain, bg=self.__loader.colorPalettes.getColor("window"),
                                    width=((self.__topLevel.getTopLevelDimensions()[0] -
                                            self.__variableHeader.winfo_width() -
                                            self.__varNameLabel.winfo_width()) // 2),
                                    height=self.__topLevel.getTopLevelDimensions()[1] // 19)

        self.__arrListBoxFrame1.pack_propagate(False)
        self.__arrListBoxFrame1.pack(side=LEFT, anchor=E, fill=Y)

        self.__arrListBoxFrame2 = Frame(self.__arrMain, bg=self.__loader.colorPalettes.getColor("window"),
                                    width=((self.__topLevel.getTopLevelDimensions()[0] -
                                            self.__variableHeader.winfo_width() -
                                            self.__varNameLabel.winfo_width()) // 2),
                                    height=self.__topLevel.getTopLevelDimensions()[1] // 19)

        self.__arrListBoxFrame2.pack_propagate(False)
        self.__arrListBoxFrame2.pack(side=LEFT, anchor=E, fill=Y)

        self.__arrListBoxLabel1 = Label(self.__arrListBoxFrame1, width=9999999,
                                     bg=self.__loader.colorPalettes.getColor("window"),
                                     fg=self.__loader.colorPalettes.getColor("font"),
                                     font=self.__miniFont,
                                     text = self.__dictionaries.getWordFromCurrentLanguage("arrVariables"),
                                     justify = CENTER)

        self.__arrListBoxLabel1.pack_propagate(False)
        self.__arrListBoxLabel1.pack(side=TOP, anchor=N, fill=X)

        self.__arrListBoxLabel2 = Label(self.__arrListBoxFrame2, width=9999999,
                                     bg=self.__loader.colorPalettes.getColor("window"),
                                     fg=self.__loader.colorPalettes.getColor("font"),
                                     font=self.__miniFont,
                                     text = self.__dictionaries.getWordFromCurrentLanguage("arrAvailable"),
                                     justify = CENTER)

        self.__arrListBoxLabel2.pack_propagate(False)
        self.__arrListBoxLabel2.pack(side=TOP, anchor=N, fill=X)

        self.__sb1 = Scrollbar(self.__arrListBoxFrame1)
        self.__arrListBox1 = Listbox(   self.__arrListBoxFrame1, width=100000, name = "box1",
                                    height=1000,
                                    yscrollcommand=self.__sb1.set,
                                    selectmode=BROWSE,
                                    exportselection = False,
                                    font = self.__smallFont
                                    )
        self.__arrListBox1.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__arrListBox1.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__arrListBox1.pack_propagate(False)
        self.__sb1.config(command=self.__arrListBox1.yview)


        self.__sb1.pack(side=RIGHT, anchor=W, fill=Y)
        self.__arrListBox1.pack(side=LEFT, anchor=E, fill = BOTH)

        self.__sb2 = Scrollbar(self.__arrListBoxFrame2)
        self.__arrListBox2 = Listbox(   self.__arrListBoxFrame2, width=100000, name = "box2",
                                    height=1000,
                                    yscrollcommand=self.__sb2.set,
                                    selectmode=BROWSE,
                                    exportselection = False,
                                    font = self.__smallFont
                                    )
        self.__arrListBox2.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__arrListBox2.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__arrListBox2.pack_propagate(False)

        self.__sb2.pack(side=RIGHT, anchor=W, fill=Y)
        self.__sb2.config(command=self.__arrListBox2.yview)
        self.__arrListBox2.pack(side=LEFT, anchor=E, fill = BOTH)

        self.__arrListBox1.bind("<Button-1>", self.__removeSelect)
        self.__arrListBox2.bind("<Button-1>", self.__removeSelect)

        self.__mainButtons = Frame(self.__buttonsFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                    width=((self.__topLevel.getTopLevelDimensions()[0] -
                                            self.__variableHeader.winfo_width() -
                                            self.__varNameLabel.winfo_width())),
                                    height=self.__topLevel.getTopLevelDimensions()[1] // 19)

        self.__mainButtons.pack_propagate(False)
        self.__mainButtons.pack(side=BOTTOM, anchor=S, fill=Y)

        self.__mainButtons1 = Frame(self.__mainButtons, bg=self.__loader.colorPalettes.getColor("window"),
                                    width=self.__mainButtons.winfo_width()//3,
                                    height=self.__topLevel.getTopLevelDimensions()[1] // 19)

        self.__mainButtons1.pack_propagate(False)
        self.__mainButtons1.pack(side=LEFT, anchor=E, fill=Y)

        while (self.__mainButtons1.winfo_width()) == 1:
               self.__mainButtons1.config(width=self.__mainButtons.winfo_width()//3)
               self.__mainButtons1.pack(side=LEFT, anchor=E, fill=Y)

        self.__mainButtons2 = Frame(self.__mainButtons, bg=self.__loader.colorPalettes.getColor("window"),
                                    width=self.__mainButtons.winfo_width()//3,
                                    height=self.__topLevel.getTopLevelDimensions()[1] // 19)

        self.__mainButtons2.pack_propagate(False)
        self.__mainButtons2.pack(side=LEFT, anchor=E, fill=Y)

        while (self.__mainButtons2.winfo_width()) == 1:
               self.__mainButtons2.config(width=self.__mainButtons.winfo_width()//3)
               self.__mainButtons2.pack(side=LEFT, anchor=E, fill=Y)

        self.__mainButtons3 = Frame(self.__mainButtons, bg=self.__loader.colorPalettes.getColor("window"),
                                    width=self.__mainButtons.winfo_width()//3,
                                    height=self.__topLevel.getTopLevelDimensions()[1] // 19)

        self.__mainButtons3.pack_propagate(False)
        self.__mainButtons3.pack(side=LEFT, anchor=E, fill=Y)

        while (self.__mainButtons3.winfo_width()) == 1:
               self.__mainButtons3.config(width=self.__mainButtons.winfo_width()//3)
               self.__mainButtons3.pack(side=LEFT, anchor=E, fill=Y)

        self.__OK = Button(self.__mainButtons1,
                                        bg=self.__loader.colorPalettes.getColor("window"),
                                        text = self.__dictionaries.getWordFromCurrentLanguage("saveToFile"),
                                        font = self.__miniFont, width=999999999,
                                        command = self.saveOneBank
                                        )
        self.__OK.pack_propagate(False)
        self.__OK.pack(side=TOP, anchor=N, fill=BOTH)

        self.__OKBank = Button(self.__mainButtons2,
                                        bg=self.__loader.colorPalettes.getColor("window"),
                                        text = self.__dictionaries.getWordFromCurrentLanguage("saveToFileBank"),
                                        font = self.__miniFont, width=999999999,
                                        command = self.saveAllBank
                                        )
        self.__OKBank.pack_propagate(False)
        self.__OKBank.pack(side=TOP, anchor=N, fill=BOTH)

        self.__Cancel = Button(self.__mainButtons3,
                                        bg=self.__loader.colorPalettes.getColor("window"),
                                        text = self.__dictionaries.getWordFromCurrentLanguage("restoreFile"),
                                        font = self.__miniFont, width=999999999,
                                        command = self.restoreBank
                                        )
        self.__Cancel.pack_propagate(False)
        self.__Cancel.pack(side=TOP, anchor=N, fill=BOTH)

        self.__hauntedFrame = Frame(self.__varWWW, bg="black",
                                    width=self.__varWWW.winfo_width(),
                                    height=self.__varWWW.winfo_height())
        self.__hauntedFrame.pack_propagate(False)
        self.__hauntedFrame.pack(side=LEFT, anchor=E, fill=BOTH)

        from Haunted import Haunted

        self.__haunted = Haunted(self.__loader, self.__hauntedFrame, self.__topLevelWindow, self)

        # From here goes the setings
        self.__bankButtons[1][1].config(
            bg=self.__loader.colorPalettes.getColor("font"),
            fg=self.__loader.colorPalettes.getColor("window")
        )
        self.changeSlot('global')

        self.__loader.threadLooper.addToThreading(self, self.loop, [])

        #from threading import Thread
        #t = Thread(target=self.loop)
        #t.daemon = True
        #t.start()

    def __changeVarType(self, event):
        if self.__virtualMemory.types[list(self.__virtualMemory.types.keys())[self.__typeListBox.curselection()[0]]] < 4:
           self.__colorButton.config(state = DISABLED)
           self.__bcdButton.config(state = DISABLED)
           self.__colorVarMode.set(0)
           self.__bcdMode.set(0)
        else:
           self.__colorButton.config(state=NORMAL)
           self.__bcdButton.config(state=NORMAL)

    def restoreBank(self):
        if self.__selectedSlot == "global":
            self.__virtualMemory.moveMemorytoVariables("bank1")
        else:
            self.__virtualMemory.moveMemorytoVariables(self.__selectedSlot)

        self.__changedBanks.remove(self.__selectedSlot)
        if len(self.__changedBanks) == 0:
            self.__changed = False

    def saveOneBank(self):
        if self.__selectedSlot == "global":
            self.__virtualMemory.moveVariablesToMemory("bank1")
        else:
            self.__virtualMemory.moveVariablesToMemory(self.__selectedSlot)

        self.__changedBanks.remove(self.__selectedSlot)
        if len(self.__changedBanks) == 0:
            self.__changed = False
        self.__virtualMemory.archieve()

    def saveAllBank(self):
        for num in range(1,9):
            self.__virtualMemory.moveVariablesToMemory("bank"+str(num))

        self.__changed = False
        self.__changedBanks.clear()
        self.__virtualMemory.archieve()

    def __removeSelect(self, event):
        other = {
            "box1": self.__arrListBox2,
            "box2": self.__arrListBox1,
        }

        name = str(event.widget).split(".")[-1]
        other[name].select_clear(0, END)

    def __createArr(self):
        self.__virtualMemory.addArray(self.__arrName.get())
        name = self.__arrName.get()
        self.__activeArr = name
        for variable in self.__included:
            varName = variable.split(" ")[0]
            self.__loader.virtualMemory.addItemsToArray(
                self.__activeArr, varName,
                self.__loader.virtualMemory.getVariableByName(varName, None)
            )

        bank = self.__loader.virtualMemory.getArrayValidity(name)
        if self.__selectedSlot != bank:
           self.getNameAndChange(bank)
        else:
            self.__arrayListBox.select_clear(0, END)
            self.__arrayLst.append(name)
            self.__arrayLst.sort()
            self.__arrayListBox.delete(0, END)
            self.__arrayLst = self.getAllArraysOfSlot(bank)
            for item in self.__arrayLst:
                self.__arrayListBox.insert(END, item)

        counter = 0
        for item in self.__arrayLst:
            item = item.split(" ")[0]
            if item == name:
               self.__arrayListBox.select_set(counter)
               self.__arrayListBox.yview(counter)
            else:
                counter += 1

        self.__changed = True
        self.__changedBanks.add(self.__selectedSlot)

    def __modifyArr(self):
        self.__deleteArr()
        self.__createArr()

    def __deleteArr(self):
        name = self.__arrName.get()
        self.__activeArr = name

        bank = self.__loader.virtualMemory.getArrayValidity(name)
        self.__loader.virtualMemory.removeArray(name)

        for item in self.__arrayLst:
            itemName = item.split(" ")[0]
            if itemName == name:
               self.__arrayLst.remove(item)
               break

        self.__arrayListBox.delete(0, END)
        for item in self.__arrayLst:
            self.__arrayListBox.insert(END, item)

        self.__changed = True
        self.__changedBanks.add(self.__selectedSlot)

    def __moveToIncluded(self):

        self.__available.remove(self.__selectedAva)
        self.__included.append(self.__selectedAva)

        self.__available.sort()
        self.__included.sort()

        self.__arrListBox1.select_clear(0, END)
        self.__arrListBox2.select_clear(0, END)

        self.__arrListBox1.delete(0, END)
        self.__arrListBox2.delete(0, END)

        for item in self.__included:
            self.__arrListBox1.insert(END, item)

        for item in self.__available:
            self.__arrListBox2.insert(END, item)

        counter = 0
        for item in self.__included:
            if item == self.__selectedAva:
                self.__arrListBox1.select_set(counter)
                break
            else:
                counter+=1

        self.__selectedInc = self.__selectedAva
        self.__selectedAva = ""

        self.__arrListBox1.yview(counter)
        self.__changeArrBoxes = False

        self.checkIfValid("arrEntry")

    def __moveToAvailable(self):
        self.__included.remove(self.__selectedInc)
        self.__available.append(self.__selectedInc)

        self.__available.sort()
        self.__included.sort()

        self.__arrListBox1.select_clear(0, END)
        self.__arrListBox2.select_clear(0, END)

        self.__arrListBox1.delete(0, END)
        self.__arrListBox2.delete(0, END)

        for item in self.__included:
            self.__arrListBox1.insert(END, item)

        for item in self.__available:
            self.__arrListBox2.insert(END, item)

        counter = 0
        for item in self.__available:
            if item == self.__selectedInc:
                self.__arrListBox2.select_set(counter)
                break
            else:
                counter+=1

        self.__selectedAva = self.__selectedInc
        self.__selectedInc = ""

        self.__arrListBox2.yview(counter)

        self.__changeArrBoxes = False
        self.checkIfValid("arrEntry")


    def fillArrListBoxes(self):
        self.__included = []
        self.__available = []

        if self.__arrName.get()==self.__activeArr and self.__activeArr != "":
            for address in self.__memory.keys():
                for variable in self.__memory[address].variables.keys():
                    if (self.__memory[address].variables[variable].iterable == True and
                            variable in list(self.__arrays[self.__activeArr].keys())):
                        self.__included.append(variable + " (" + self.__memory[address].variables[variable].validity + ")")
        self.__included.sort()

        self.__available = []
        for address in self.__memory.keys():
            for variable in self.__memory[address].variables.keys():
                if ((variable + " (" + self.__memory[address].variables[variable].validity + ")" not in self.__included) and
                        self.__memory[address].variables[variable].iterable == True and
                        (self.__memory[address].variables[variable].validity == "global" or
                         self.__memory[address].variables[variable].validity == self.__selectedSlot)):
                    self.__available.append(variable + " (" + self.__memory[address].variables[variable].validity + ")")
        self.__available.sort()

        self.__arrListBox1.select_clear(0,END)
        self.__arrListBox2.select_clear(0,END)

        self.__arrListBox1.delete(0,END)
        self.__arrListBox2.delete(0,END)

        for item in self.__included:
            self.__arrListBox1.insert(END, item)

        for item in self.__available:
            self.__arrListBox2.insert(END, item)

    def createVar(self):
        self.__virtualMemory.archieve()
        success = self.__virtualMemory.addVariable(self.__varName.get(),
                                  self.__typeListBox.get(self.__typeListBox.curselection()[0]),
                                  self.__selectedSlot, self.__colorVarMode.get(), self.__bcdMode.get()
                                  )
        if success == True:
            self.__changed = True
            self.__changedBanks.add(self.__selectedSlot)

            name = self.__varName.get()
            self.changeSlot(self.__selectedSlot)

            counter = 0
            for item in self.__variableList:
                if item.startswith(name):
                    self.__variableListBox.select_clear(0, END)
                    self.__variableListBox.select_set(counter)
                else:
                    counter+=1
        else:
            self.__virtualMemory.getArcPrev()
            self.__virtualMemory.archieved.pop(-1)

        return success

    def deleteVar(self):
        self.__virtualMemory.removeVariable(self.__varName.get(),
                                                       self.__selectedSlot)
        self.__changed = True
        self.__changedBanks.add(self.__selectedSlot)

        self.__varName.set("")
        self.changeSlot(self.__selectedSlot)


    def modifyVar(self):
        self.__virtualMemory.archieve()
        self.__virtualMemory.removeVariable(self.__varName.get(),
                                                   self.__selectedSlot)
        success = self.createVar()
        if success == False:
            self.__virtualMemory.getArcPrev()
            self.__virtualMemory.archieved.pop(-1)


    def insertVar(self):
        for address in self.__memory.keys():
            for variable in self.__memory[address].variables.keys():
                if variable == self.__selectedVar.split(" ")[0]:
                   self.__address.set(address)
                   __bits = ""
                   for b in self.__memory[address].variables[variable].usedBits:
                       __bits += str(b) + ", "

                   self.__bits.set(__bits[:-2])
                   self.__activeVar = self.__selectedVar.split(" ")[0]
                   self.__typeListBox.select_clear(0, END)
                   self.__typeListBox.select_set(
                       list(self.__varTypes.keys()).index(self.__memory[address].variables[variable].type)
                   )

                   self.__varBuffer = [
                       address, __bits, list(self.__varTypes.keys()).index(self.__memory[address].variables[variable].type)
                   ]
                   self.__varName.set(self.__selectedVar.split(" ")[0])

                   if self.__memory[address].variables[variable].color == True:
                      self.__colorVarMode.set(1)
                   else:
                      self.__colorVarMode.set(0)

                   if self.__memory[address].variables[variable].bcd   == True:
                      self.__bcdMode.set(1)
                   else:
                      self.__bcdMode.set(0)

                   if len(self.__memory[address].variables[variable].usedBits) < 4:
                      self.__bcdMode.set(0)
                      self.__colorVarMode.set(0)
                      self.__colorButton.config(state = DISABLED)
                      self.__bcdButton.config(state = DISABLED)
                   else:
                      self.__colorButton.config(state=NORMAL)
                      self.__bcdButton.config(state=NORMAL)

                   self.__createButton.config(state=DISABLED)
                   self.__modifyButton.config(state=NORMAL)
                   self.__deleteButton.config(state=NORMAL)

                   return

    def insertArr(self):
        self.__arrName.set(
            self.__selectedArr.split(" ")[0]
        )
        self.__activeArr = self.__selectedArr.split(" ")[0]

        self.__arrCreateButton.config(state=DISABLED)
        self.__arrModifyButton.config(state=NORMAL)
        self.__arrDeleteButton.config(state=NORMAL)

        self.fillArrListBoxes()

    def checkIfValid(self, event):
        variables = {
            "varEntry": (self.__varName, "var", self.__varError, self.__varNameEntry),
            "arrEntry": (self.__arrName, "arr", self.__arrError, self.__arrNameEntry)
        }

        if type(event) == str:
            name = event
        else:
            name = str(event.widget).split(".")[-1]

        error = self.checkIfNameOK(variables[name][0].get(),
                                   variables[name][1])

        if error == None:
           variables[name][3].config(
               bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
               fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
           variables[name][2].set("")

           if variables[name][0].get() == self.__activeVar and self.__activeVar != "":
               self.__address.set(self.__varBuffer[0])
               self.__bits.set(self.__varBuffer[1])
               self.__typeListBox.select_clear(0,END)
               self.__typeListBox.select_set(self.__varBuffer[2])
               self.__createButton.config(state=DISABLED)
               self.__modifyButton.config(state=NORMAL)
               self.__deleteButton.config(state=NORMAL)

           elif variables[name][0].get() == self.__activeArr:
               self.__arrCreateButton.config(state=DISABLED)
               self.__arrModifyButton.config(state=NORMAL)
               self.__arrDeleteButton.config(state=NORMAL)
               if self.__changeArrBoxes and self.__lastBullShit != self.__activeArr:
                    self.fillArrListBoxes()
               self.__lastBullShit = self.__activeArr

           else:
               if variables[name][1] == "var":
                   self.__address.set("-")
                   self.__bits.set("-")
                   self.__createButton.config(state=NORMAL)
                   self.__modifyButton.config(state=DISABLED)
                   self.__deleteButton.config(state=DISABLED)

               else:
                   self.__arrCreateButton.config(state=NORMAL)
                   self.__arrModifyButton.config(state=DISABLED)
                   self.__arrDeleteButton.config(state=DISABLED)
                   if self.__changeArrBoxes and self.__lastBullShit != "new":
                       self.fillArrListBoxes()
                   self.__lastBullShit = "new"


        else:
            variables[name][3].config(
                bg = self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                fg = self.__loader.colorPalettes.getColor("boxFontUnSaved"))
            variables[name][2].set(self.__dictionaries.getWordFromCurrentLanguage(error))
            self.__address.set("-")
            self.__bits.set("-")
            self.__createButton.config(state=DISABLED)
            self.__modifyButton.config(state=DISABLED)
            self.__deleteButton.config(state=DISABLED)
        self.__changeArrBoxes = True

    def checkIfNameOK(self, name, typ):
        if len(name) == 0: return(None)
        if len(name) < 4: return("varNameTooShort")
        import re
        if len(re.findall(r'^[a-zA-Z][a-zA-Z0-9_-]+$', name)) == 0: return "varNameNotValid"
        for address in self.__memory.keys():
            if name in self.__memory[address].variables.keys():
                if self.__memory[address].variables[name].system == True:
                    return "systemVar"

        if typ == "var":
           thisMayBeIt = self.__selectedVar
        else:
           thisMayBeIt = self.__selectedArr

        thisMayBeIt = thisMayBeIt.split(" ")[0]

        temp = []
        for address in self.__memory:
            if name in self.__memory[address].variables.keys():
                temp.append(name)

        if name != thisMayBeIt:
            if name in self.__arrays.keys(): return "alreadyArr"
            if name in temp: return "alreadyVar"

        for command in self.__loader.syntaxList.keys():
            if command == name: return "commandName"
            else:
                for alias in self.__loader.syntaxList[command].alias:
                    if alias == name: return "commandName"

        for delimiter in self.__loader.config.getValueByKey("validObjDelimiters").replace("\r", "").split(" "):
            if delimiter in name: return "delimiterInName"

        for delimiter in self.__loader.config.getValueByKey("validLineDelimiters").replace("\r", "").split(" "):
            if delimiter in name: return "delimiterInName"


        if name.lower().startswith("bank"): return "startWithBank"

        return(None)

    def loop(self):
        from time import sleep
        while self.__loader.mainWindow.dead == False and self.dead == False:
            #self.__colorFiller.config(bg = self.__loader.mainWindow.getLoopColor())

            try:
                if len(self.__variableList) > 0:
                    self.__insertVarButton.config(state = NORMAL)
                else:
                    self.__insertVarButton.config(state = DISABLED)

                if len(self.__arrayLst) > 0:
                    self.__insertArrButton.config(state = NORMAL)
                else:
                    self.__insertArrButton.config(state = DISABLED)
            except:
                pass

            try:
                if self.__variableListBox.get(self.__variableListBox.curselection()[0]) != self.__selectedVar:
                    if len(self.__variableList) == 0:
                        self.__variableList = ""
                    else:
                        self.__selectedVar = self.__variableListBox.get(self.__variableListBox.curselection()[0])

                if self.__arrayListBox.get(self.__arrayListBox.curselection()[0]) != self.__selectedArr:
                    if len(self.__arrayLst) == 0:
                        self.__selectedArr = ""
                    else:
                        self.__selectedArr = self.__arrayListBox.get(self.__arrayListBox.curselection()[0])
            except:
                pass

            try:
                if len(self.__included) == 0:
                   self.__selectedInc = ""
                   self.__arrMove2Button.config(state = DISABLED)
                   self.__arrCreateButton.config(state = DISABLED)
                   self.__arrModifyButton.config(state = DISABLED)
                else:
                    self.__selectedInc = self.__included[self.__arrListBox1.curselection()[0]]
                    self.__arrMove2Button.config(state=NORMAL)

            except Exception as e:
                    #print(str(e))
                    try:
                        self.__selectedInc = ""
                        self.__arrMove2Button.config(state=DISABLED)
                    except:
                        pass

            try:
                if len(self.__available) == 0:
                    self.__selectedAva = ""
                    self.__arrMove1Button.config(state = DISABLED)
                else:
                    self.__selectedAva = self.__available[self.__arrListBox2.curselection()[0]]
                    self.__arrMove1Button.config(state=NORMAL)

            except Exception as e:
                    try:
                    #print(str(e))
                        self.__selectedAva = ""
                        self.__arrMove1Button.config(state = DISABLED)
                    except:
                        pass

            sleep(0.05)

    def getNameAndChange(self, event):
        if type(event) == str:
            name = event
        else:
            name = str(event.widget).split(".")[-1]
        for b in self.__bankButtons.keys():
            self.__bankButtons[b][1].config(
                bg=self.__loader.colorPalettes.getColor("window"),
                fg=self.__loader.colorPalettes.getColor("font")
            )

        try:
            event.widget.config(
                bg=self.__loader.colorPalettes.getColor("font"),
                fg=self.__loader.colorPalettes.getColor("window")
            )
        except:
            if name == 'global':
                numkey = 1
            else:
                numkey = int(name[-1])

            self.__bankButtons[numkey][1].config(
                bg=self.__loader.colorPalettes.getColor("font"),
                fg=self.__loader.colorPalettes.getColor("window")
            )

        self.changeSlot(name)

    def changeSlot(self, slot):
        self.__selectedSlot = slot
        self.__variableList = self.getAllVariablesOfSlot(slot)

        self.__variableListBox.select_clear(0,END)
        self.__arrayListBox.select_clear(0,END)

        self.__variableListBox.delete(0, END)
        for item in self.__variableList:
            self.__variableListBox.insert(END, item)
        self.__variableListBox.select_clear(0,END)
        self.__variableListBox.select_set(0)

        self.__arrayLst = self.getAllArraysOfSlot(slot)
        self.__arrayListBox.delete(0, END)
        for item in self.__arrayLst:
            self.__arrayListBox.insert(END, item)
        self.__arrayListBox.select_clear(0,END)
        self.__arrayListBox.select_set(0)

        self.__freeRAM = self.calculateFreeRAM(slot)
        for num in range(0,4):
            if slot == "global" and num%2 == 1 :
                self.__freeMamoryTexts[num].set("- bytes - bits")
            else:
                self.__freeMamoryTexts[num].set(
                    str(self.__freeRAM[num] // 8 ) + " bytes " +
                    str(self.__freeRAM[num] %  8 ) + " bits"
                )

                if self.__freeRAM[num] // 8 == 1:
                    self.__freeMamoryTexts[num].set(self.__freeMamoryTexts[num].get().replace("bytes", "byte"))
                if self.__freeRAM[num] %  8 == 1:
                    self.__freeMamoryTexts[num].set(self.__freeMamoryTexts[num].get().replace("bits", "bit"))

                if self.__freeRAM[num] // 8 == 0 and self.__freeRAM[num] % 8 == 0:
                    self.__freeMamoryValues[num].config(
                        bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                        fg=self.__loader.colorPalettes.getColor("boxFontUnSaved")
                    )
                else:
                    self.__freeMamoryValues[num].config(
                        bg=self.__loader.colorPalettes.getColor(self.__fuckColors[num % 2][0]),
                        fg=self.__loader.colorPalettes.getColor(self.__fuckColors[num % 2][1])
                    )

        self.fillArrListBoxes()

    def getAllVariablesOfSlot(self, slot):
        variableList = []
        for address in self.__memory:
            for var in self.__memory[address].variables.keys():
                if (self.__memory[address].variables[var].validity == slot
                and self.__memory[address].variables[var].system == False):
                    variableList.append(var+" ("+address+", "+
                                        self.__memory[address].variables[var].type+")")
        variableList.sort()
        return variableList

    def getAllArraysOfSlot(self, slot):
        arrayList = []
        for name in self.__arrays.keys():
            if self.__loader.virtualMemory.getArrayValidity(name) == slot:
                arrayList.append(name+" (" +self.__loader.virtualMemory.getArrayValidity(name)+ ")")

        arrayList.sort()
        return arrayList

    def calculateFreeRAM(self, slot):
        basic = 0
        sara = 0
        basicLocal = 0
        saraLocal = 0
        for address in self.__memory.keys():
            if len(address) == 3:
                basic+=len(self.__memory[address].freeBits["global"])
                if slot != "global":
                    basicLocal += len(self.__memory[address].freeBits[slot])
            else:
                sara+=len(self.__memory[address].freeBits["global"])
                if slot != "global":
                    saraLocal += len(self.__memory[address].freeBits[slot])

        return(basic, basicLocal, sara, saraLocal)