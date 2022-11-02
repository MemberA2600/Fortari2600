from tkinter import *
from SubMenu import SubMenu
from threading import Thread

class MiniMapMaker:

    def __init__(self, loader):
        self.__loader = loader
        self.__mainWindow = self.__loader.mainWindow

        self.dead = False
        self.changed = False
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

        self.__focused = None
        self.__screenSize = self.__loader.screenSize

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize*0.65), False, False, False)
        self.__bigFont = self.__fontManager.getFont(int(self.__fontSize*1.15), False, False, False)

        self.__ctrl = False
        self.__draw = 0

        self.__delay   = 0
        self.__counter = 0
        self.__changed = 0

        self.__ctrl = False
        self.__middle = False
        self.__draw = 0

        self.__sizes = [self.__screenSize[0] / 1.25, self.__screenSize[1] / 1.20 - 40]
        self.__window = SubMenu(self.__loader, "minimap", self.__sizes[0], self.__sizes[1], None, self.__addElements, 1)

        self.dead = True

    def __closeWindow(self):
        if self.changed == True:
            answer = self.__fileDialogs.askYesNoCancel("notSavedFile", "notSavedFileMessage")
            if answer == "Yes":
                pass
            elif answer == "Cancel":
                self.__topLevelWindow.deiconify()
                self.__topLevelWindow.focus()
                return

        self.dead = True
        self.__topLevelWindow.destroy()
        self.__loader.topLevels.remove(self.__topLevelWindow)

    def __addElements(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()
        self.__topLevelWindow.protocol('WM_DELETE_WINDOW', self.__closeWindow)

        self.__stepX = 16
        self.__stepY = 8
        self.__matrix = [4, 4]

        self.__indexX = 0
        self.__indexY = 0

        self.__editorFrame = Frame(self.__topLevelWindow,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0], height = round(self.__sizes[1] * 4.35) // 6
                                   )
        self.__editorFrame.pack_propagate(False)
        self.__editorFrame.pack(side=TOP, anchor=N, fill=X)

        self.__controllerFrame = Frame(self.__topLevelWindow,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0], height = round(self.__sizes[1] * 1.65) // 6
                                   )
        self.__controllerFrame.pack_propagate(False)
        self.__controllerFrame.pack(side=TOP, anchor=N, fill=BOTH)

        self.__hor = 48
        self.__ver = 36

        self.__w = (self.__sizes[0] // self.__hor) - 1
        self.__h = (self.__sizes[1] * 4 // 5 // self.__ver)-1

        self.__frames     = []
        self.__subFrames  = []
        self.__matrixButtons = []
        self.__dataMatrix    = []

        self.__finished = False
        t1 = Thread(target = self.__drawTable)
        t1.daemon = True
        t1.start()

        self.__openSaveFrameTesting = Frame(self.__controllerFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0] // 2.5, height = self.__sizes[1]
                                   )
        self.__openSaveFrameTesting.pack_propagate(False)
        self.__openSaveFrameTesting.pack(side=LEFT, anchor=E, fill=Y)

        from time import sleep
        while self.__openSaveFrameTesting.winfo_height() < 2:
            sleep(0.05)

        self.__openSaveFrameTesting1 = Frame(self.__openSaveFrameTesting,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0] // 2.5, height = self.__openSaveFrameTesting.winfo_height() // 5 * 2
                                   )
        self.__openSaveFrameTesting1.pack_propagate(False)
        self.__openSaveFrameTesting1.pack(side=TOP, anchor=N, fill=X)

        self.__openSaveFrameTesting2 = Frame(self.__openSaveFrameTesting,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0] // 2.5, height = self.__openSaveFrameTesting.winfo_height() // 5
                                   )
        self.__openSaveFrameTesting2.pack_propagate(False)
        self.__openSaveFrameTesting2.pack(side=TOP, anchor=N, fill=X)

        from VisualLoaderFrame import VisualLoaderFrame

        self.__spriteLoader = VisualLoaderFrame(self.__loader, self.__openSaveFrameTesting1, round(self.__sizes[1] // 28),
                                                self.__normalFont, self.__smallFont, None, "Haunted_Evil_Dungeon",
                                                "spriteName", self.__checkIfValidFileName, round(self.__sizes[0] // 5),
                                                self.__openMM, self.__saveMM)

        from EmuTestFrame import EmuTestFrame

        self.__testWithEmulatorFrame = EmuTestFrame(self.__loader, self.__openSaveFrameTesting2, round(self.__sizes[1] // 28),
                                                    self.__normalFont,  round(self.__sizes[0] // 5),
                                                    self.__loadTest, TOP, N)


        self.__layoutFrame = Frame(self.__controllerFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0] // 4.5, height = self.__sizes[1]
                                   )
        self.__layoutFrame.pack_propagate(False)
        self.__layoutFrame.pack(side=LEFT, anchor=E, fill=Y)

        text = self.__dictionaries.getWordFromCurrentLanguage("numOfLines")
        if text.endswith(":") == False: text += ":"
        self.__numberOfLines = Label(self.__layoutFrame,
                                    text=text,
                                    font=self.__normalFont, fg=self.__colors.getColor("font"),
                                    bg=self.__colors.getColor("window")
                                    )

        self.__numberOfLines.pack_propagate(False)
        self.__numberOfLines.pack(side=TOP, anchor=N, fill=X)

        self.__numOfLinesVal = StringVar()
        self.__numOfLines = Entry(self.__layoutFrame,
                                  name="lineNum",
                                  bg=self.__colors.getColor("boxBackNormal"),
                                  fg=self.__colors.getColor("boxFontNormal"),
                                  width=9999, justify=CENTER, state = DISABLED,
                                  textvariable=self.__numOfLinesVal,
                                  font=self.__normalFont
                                  )

        self.__numOfLines.pack_propagate(False)
        self.__numOfLines.pack(fill=X, side=TOP, anchor=N)

        self.__numOfLinesVal.set(str(self.__stepY))

        self.__numOfLines.bind("<FocusOut>", self.__chamgeConst)
        self.__numOfLines.bind("<KeyRelease>", self.__chamgeConst)

        while self.__layoutFrame.winfo_height() < 2: sleep(0.05)

        self.__offsetEntryFrame = Frame(self.__layoutFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0] // 4.5, height = self.__layoutFrame.winfo_height() // 3.25
                                   )
        self.__offsetEntryFrame.pack_propagate(False)
        self.__offsetEntryFrame.pack(side=TOP, anchor=N, fill=X)

        self.__offsetEntryFrame1 = Frame(self.__offsetEntryFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0] // 9, height = self.__layoutFrame.winfo_height() // 3.25
                                   )
        self.__offsetEntryFrame1.pack_propagate(False)
        self.__offsetEntryFrame1.pack(side=LEFT, anchor=E, fill=Y)

        self.__offsetEntryFrame2 = Frame(self.__offsetEntryFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0] // 9, height = self.__layoutFrame.winfo_height() // 3.25
                                   )
        self.__offsetEntryFrame2.pack_propagate(False)
        self.__offsetEntryFrame2.pack(side=LEFT, anchor=E, fill=Y)

        text = self.__dictionaries.getWordFromCurrentLanguage("xOffset")
        if text.endswith(":") == False: text += ":"

        self.__offsetLabel1 = Label(self.__offsetEntryFrame1,
                                    text=text,
                                    font=self.__smallFont, fg=self.__colors.getColor("font"),
                                    bg=self.__colors.getColor("window")
                                    )

        self.__offsetLabel1.pack_propagate(False)
        self.__offsetLabel1.pack(side=TOP, anchor=N, fill=X)

        text = self.__dictionaries.getWordFromCurrentLanguage("yOffset")
        if text.endswith(":") == False: text += ":"

        self.__offsetLabel2 = Label(self.__offsetEntryFrame2,
                                    text=text,
                                    font=self.__smallFont, fg=self.__colors.getColor("font"),
                                    bg=self.__colors.getColor("window")
                                    )

        self.__offsetLabel2.pack_propagate(False)
        self.__offsetLabel2.pack(side=TOP, anchor=N, fill=X)

        self.__offsetVal1 = StringVar()
        self.__offsetEntry1 = Entry(self.__offsetEntryFrame1,
                                  name="offSetX",
                                  bg=self.__colors.getColor("boxBackNormal"),
                                  fg=self.__colors.getColor("boxFontNormal"),
                                  width=9999, justify=CENTER, state = DISABLED,
                                  textvariable=self.__offsetVal1,
                                  font=self.__smallFont
                                  )

        self.__offsetEntry1.pack_propagate(False)
        self.__offsetEntry1.pack(fill=X, side=TOP, anchor=N)

        self.__offsetVal2 = StringVar()
        self.__offsetEntry2 = Entry(self.__offsetEntryFrame2,
                                  name="offSetY",
                                  bg=self.__colors.getColor("boxBackNormal"),
                                  fg=self.__colors.getColor("boxFontNormal"),
                                  width=9999, justify=CENTER, state = DISABLED,
                                  textvariable=self.__offsetVal2,
                                  font=self.__smallFont
                                  )

        self.__offsetEntry2.pack_propagate(False)
        self.__offsetEntry2.pack(fill=X, side=TOP, anchor=N)

        self.__offsetEntry1.bind("<FocusOut>", self.__chamgeConst)
        self.__offsetEntry1.bind("<KeyRelease>", self.__chamgeConst)
        self.__offsetEntry2.bind("<FocusOut>", self.__chamgeConst)
        self.__offsetEntry2.bind("<KeyRelease>", self.__chamgeConst)

        self.__offsetVal1.set(str(self.__indexX))
        self.__offsetVal2.set(str(self.__indexY))

        self.__topLevelWindow.bind("<KeyPress-Control_L>", self.shiftON)
        self.__topLevelWindow.bind("<KeyRelease-Control_L>", self.shiftOff)
        self.__topLevelWindow.bind("<KeyPress-Control_R>", self.shiftON)
        self.__topLevelWindow.bind("<KeyRelease-Control_R>", self.shiftOff)
        self.__topLevelWindow.bind("<Button-2>", self.drawMode)

        self.__controllerButtons = Frame(self.__layoutFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0] // 4.5, height = self.__sizes[1]
                                   )
        self.__controllerButtons.pack_propagate(False)
        self.__controllerButtons.pack(side=TOP, anchor=N, fill=BOTH)

        while self.__controllerButtons.winfo_height() < 2: sleep(0.005)

        buttonH = self.__controllerButtons.winfo_height() // 3

        self.__upFrame = Frame(self.__controllerButtons,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0] // 4.5, height = buttonH
                                   )
        self.__upFrame.pack_propagate(False)
        self.__upFrame.pack(side=TOP, anchor=N, fill=X)

        self.__horFrame = Frame(self.__controllerButtons,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0] // 4.5, height = buttonH
                                   )
        self.__horFrame.pack_propagate(False)
        self.__horFrame.pack(side=TOP, anchor=N, fill=X)

        self.__downFrame = Frame(self.__controllerButtons,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0] // 4.5, height = buttonH
                                   )
        self.__downFrame.pack_propagate(False)
        self.__downFrame.pack(side=TOP, anchor=N, fill=X)

        self.__upButton = Button(self.__upFrame, height = buttonH,
                                 width = round( self.__sizes[0] // 4.5), name="up",
                   font = self.__smallFont,
                   bg=self.__loader.colorPalettes.getColor("window"),
                   fg=self.__loader.colorPalettes.getColor("font"),
                   activebackground=self.__loader.colorPalettes.getColor("highLight"),
                   state=DISABLED, command = self.__pressedUp, text = "/\\"
                   )
        self.__upButton.pack_propagate(False)
        self.__upButton.pack(side=TOP, anchor=N, fill=BOTH)

        self.__downButton = Button(self.__downFrame, height = buttonH,
                                 width = round( self.__sizes[0] // 4.5), name="down",
                   font = self.__smallFont,
                   bg=self.__loader.colorPalettes.getColor("window"),
                   fg=self.__loader.colorPalettes.getColor("font"),
                   activebackground=self.__loader.colorPalettes.getColor("highLight"),
                   state=DISABLED, command = self.__pressedDown, text = "\\/"
                   )
        self.__downButton.pack_propagate(False)
        self.__downButton.pack(side=TOP, anchor=N, fill=BOTH)

        self.__leftFrame = Frame(self.__horFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0] // 9, height = buttonH
                                   )
        self.__leftFrame.pack_propagate(False)
        self.__leftFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__rightFrame = Frame(self.__horFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0] // 9, height = buttonH
                                   )
        self.__rightFrame.pack_propagate(False)
        self.__rightFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__leftButton = Button(self.__leftFrame, height = buttonH,
                                 width = round( self.__sizes[0] // 9), name="left",
                   font = self.__smallFont,
                   bg=self.__loader.colorPalettes.getColor("window"),
                   fg=self.__loader.colorPalettes.getColor("font"),
                   activebackground=self.__loader.colorPalettes.getColor("highLight"),
                   state=DISABLED, command = self.__pressedLeft, text = "<<"
                   )
        self.__leftButton.pack_propagate(False)
        self.__leftButton.pack(side=TOP, anchor=N, fill=BOTH)

        self.__rightButton = Button(self.__rightFrame, height = buttonH,
                                 width = round( self.__sizes[0] // 9), name="right",
                   font = self.__smallFont,
                   bg=self.__loader.colorPalettes.getColor("window"),
                   fg=self.__loader.colorPalettes.getColor("font"),
                   activebackground=self.__loader.colorPalettes.getColor("highLight"),
                   state=DISABLED, command = self.__pressedRight, text = ">>"
                   )
        self.__rightButton.pack_propagate(False)
        self.__rightButton.pack(side=TOP, anchor=N, fill=BOTH)

        self.__colorsFrame = Frame(self.__controllerFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0] // 5.5, height = self.__sizes[1]
                                   )
        self.__colorsFrame.pack_propagate(False)
        self.__colorsFrame.pack(side=LEFT, anchor=E, fill=Y)

        labels             = ["COLUPF", "COLUBK", "spriteColor", "testColor", "ballColor"]
        self.__colorLabels = []
        self.__hexEntries  = []
        self.__hexValues   = ["$40","$04","$48","$00", "$0e"]

        for num in range(0,5):
            text = self.__dictionaries.getWordFromCurrentLanguage(labels[num])
            if text.endswith(":") == False: text += ":"

            l = Label(self.__colorsFrame, text=text,
                      font=self.__miniFont, fg=self.__colors.getColor("font"),
                      bg=self.__colors.getColor("window")
                      )
            l.pack_propagate(False)
            l.pack(side=TOP, anchor=N, fill=X)

            from HexEntry import HexEntry

            hexEntry = HexEntry(self.__loader, self.__colorsFrame, self.__colors, self.__colorDict,
                                self.__miniFont, self.__hexValues, num, None, self.__changeHex)
            self.__hexEntries.append(hexEntry)

        self.__playfieldImportFrame = Frame(self.__controllerFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0] // 5.5, height = self.__sizes[1]
                                   )
        self.__playfieldImportFrame.pack_propagate(False)
        self.__playfieldImportFrame.pack(side=LEFT, anchor=E, fill=BOTH)

        text = self.__dictionaries.getWordFromCurrentLanguage("importPlayfield")
        if text.endswith(":") == False: text += ":"

        self.__PFImportLabel = Label(self.__playfieldImportFrame,
                                    text=text,
                                    font=self.__smallFont, fg=self.__colors.getColor("font"),
                                    bg=self.__colors.getColor("window")
                                    )

        self.__PFImportLabel.pack_propagate(False)
        self.__PFImportLabel.pack(side=TOP, anchor=N, fill=X)

        text = self.__dictionaries.getWordFromCurrentLanguage("region")
        if text.endswith(":") == False: text += ":"

        self.__regionLabel = Label(self.__playfieldImportFrame,
                                    text=text,
                                    font=self.__smallFont, fg=self.__colors.getColor("font"),
                                    bg=self.__colors.getColor("window")
                                    )

        self.__regionLabel.pack_propagate(False)
        self.__regionLabel.pack(side=TOP, anchor=N, fill=X)

        while self.__playfieldImportFrame.winfo_height() < 2: sleep(0.0005)

        self.__regionFrame = Frame(self.__playfieldImportFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0] // 5.5,
                                   height = self.__playfieldImportFrame.winfo_height() // 4
                                   )
        self.__regionFrame.pack_propagate(False)
        self.__regionFrame.pack(side=TOP, anchor=N, fill=X)

        while self.__regionFrame.winfo_height() < 2: sleep(0.0005)

        self.__regionFrame1 = Frame(self.__regionFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__regionFrame.winfo_width() // 2,
                                   height = self.__regionFrame.winfo_height() // 4
                                   )
        self.__regionFrame1.pack_propagate(False)
        self.__regionFrame1.pack(side=LEFT, anchor=E, fill=Y)

        self.__regionFrame2 = Frame(self.__regionFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__regionFrame.winfo_width() // 2,
                                   height = self.__regionFrame.winfo_height() // 4
                                   )
        self.__regionFrame2.pack_propagate(False)
        self.__regionFrame2.pack(side=LEFT, anchor=E, fill=Y)


        self.__regionLabelX = Label(self.__regionFrame1,
                                    text="X",
                                    font=self.__smallFont, fg=self.__colors.getColor("font"),
                                    bg=self.__colors.getColor("window")
                                    )

        self.__regionLabelX.pack_propagate(False)
        self.__regionLabelX.pack(side=TOP, anchor=N, fill=X)

        self.__regionLabelY = Label(self.__regionFrame2,
                                    text="Y",
                                    font=self.__smallFont, fg=self.__colors.getColor("font"),
                                    bg=self.__colors.getColor("window")
                                    )

        self.__regionLabelY.pack_propagate(False)
        self.__regionLabelY.pack(side=TOP, anchor=N, fill=X)

        self.__regionEntryVal1 = StringVar()
        self.__regionEntryVal2 = StringVar()

        self.__regionEntry1 = Entry(self.__regionFrame1,
                                  name="regionX",
                                  bg=self.__colors.getColor("boxBackNormal"),
                                  fg=self.__colors.getColor("boxFontNormal"),
                                  width=9999, justify=CENTER, state = DISABLED,
                                  textvariable=self.__regionEntryVal1,
                                  font=self.__smallFont
                                  )

        self.__regionEntry1.pack_propagate(False)
        self.__regionEntry1.pack(fill=X, side=TOP, anchor=N)

        self.__regionEntry2 = Entry(self.__regionFrame2,
                                    name="regionX",
                                    bg=self.__colors.getColor("boxBackNormal"),
                                    fg=self.__colors.getColor("boxFontNormal"),
                                    width=9999, justify=CENTER, state=DISABLED,
                                    textvariable=self.__regionEntryVal2,
                                    font=self.__smallFont
                                    )

        self.__regionEntry2.pack_propagate(False)
        self.__regionEntry2.pack(fill=X, side=TOP, anchor=N)

        self.__regionEntryVal1.set("0")
        self.__regionEntryVal2.set("0")

        self.__regionEntry1.bind("<FocusOut>", self.__chamgeConst)
        self.__regionEntry1.bind("<KeyRelease>", self.__chamgeConst)
        self.__regionEntry2.bind("<FocusOut>", self.__chamgeConst)
        self.__regionEntry2.bind("<KeyRelease>", self.__chamgeConst)

        self.__openSaveFrameTesting3 = Frame(self.__openSaveFrameTesting,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0] // 2.5, height = self.__openSaveFrameTesting.winfo_height()
                                   )
        self.__openSaveFrameTesting3.pack_propagate(False)
        self.__openSaveFrameTesting3.pack(side=TOP, anchor=N, fill=BOTH)

        text = self.__dictionaries.getWordFromCurrentLanguage("dimensions")
        if text.endswith(":") == False: text += ":"

        self.__dimensionsLabel = Label(self.__openSaveFrameTesting3,
                                    text=text,
                                    font=self.__smallFont, fg=self.__colors.getColor("font"),
                                    bg=self.__colors.getColor("window")
                                    )

        self.__dimensionsLabel.pack_propagate(False)
        self.__dimensionsLabel.pack(side=TOP, anchor=N, fill=X)

        while self.__openSaveFrameTesting3.winfo_height() < 2 : sleep(0.005)

        self.__dimensionFrame1 = Frame(self.__openSaveFrameTesting3,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__openSaveFrameTesting3.winfo_width() // 2, height = self.__openSaveFrameTesting3.winfo_height()
                                   )
        self.__dimensionFrame1.pack_propagate(False)
        self.__dimensionFrame1.pack(side=LEFT, anchor=E, fill=Y)

        self.__dimensionFrame2 = Frame(self.__openSaveFrameTesting3,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__openSaveFrameTesting3.winfo_width() // 2, height = self.__openSaveFrameTesting3.winfo_height()
                                   )
        self.__dimensionFrame2.pack_propagate(False)
        self.__dimensionFrame2.pack(side=TOP, anchor=N, fill=Y)

        self.__dimensionEntryVal1 = StringVar()
        self.__dimensionEntryVal2 = StringVar()


        self.__dimensionLabelX = Label(self.__dimensionFrame1,
                                    text="X",
                                    font=self.__smallFont, fg=self.__colors.getColor("font"),
                                    bg=self.__colors.getColor("window")
                                    )

        self.__dimensionLabelX.pack_propagate(False)
        self.__dimensionLabelX.pack(side=TOP, anchor=N, fill=X)

        self.__dimensionLabelY = Label(self.__dimensionFrame2,
                                    text="Y",
                                    font=self.__smallFont, fg=self.__colors.getColor("font"),
                                    bg=self.__colors.getColor("window")
                                    )

        self.__dimensionLabelY.pack_propagate(False)
        self.__dimensionLabelY.pack(side=TOP, anchor=N, fill=X)

        self.__dimensionEntryVal1 = StringVar()
        self.__dimensionEntryVal2 = StringVar()

        self.__dimensionEntry1 = Entry(self.__dimensionFrame1,
                                  name="dimensionX",
                                  bg=self.__colors.getColor("boxBackNormal"),
                                  fg=self.__colors.getColor("boxFontNormal"),
                                  width=9999, justify=CENTER, state = DISABLED,
                                  textvariable=self.__dimensionEntryVal1,
                                  font=self.__smallFont
                                  )

        self.__dimensionEntry1.pack_propagate(False)
        self.__dimensionEntry1.pack(fill=X, side=TOP, anchor=N)

        self.__dimensionEntry2 = Entry(self.__dimensionFrame2,
                                    name="dimensionY",
                                    bg=self.__colors.getColor("boxBackNormal"),
                                    fg=self.__colors.getColor("boxFontNormal"),
                                    width=9999, justify=CENTER, state=DISABLED,
                                    textvariable=self.__dimensionEntryVal2,
                                    font=self.__smallFont
                                    )

        self.__dimensionEntry2.pack_propagate(False)
        self.__dimensionEntry2.pack(fill=X, side=TOP, anchor=N)

        self.__dimensionEntryVal1.set(str(self.__matrix[0]))
        self.__dimensionEntryVal2.set(str(self.__matrix[1]))

        self.__dimensionEntry1.bind("<FocusOut>", self.__chamgeConst)
        self.__dimensionEntry1.bind("<KeyRelease>", self.__chamgeConst)
        self.__dimensionEntry2.bind("<FocusOut>", self.__chamgeConst)
        self.__dimensionEntry2.bind("<KeyRelease>", self.__chamgeConst)

        self.__checkVal = IntVar()

        self.__checked = Checkbutton(self.__playfieldImportFrame, width=99999,
                                             text=self.__dictionaries.getWordFromCurrentLanguage("fillThru"),
                                             bg=self.__colors.getColor("window"),
                                             fg=self.__colors.getColor("font"),
                                             justify=LEFT, font=self.__miniFont,
                                             variable=self.__checkVal,
                                             activebackground=self.__colors.getColor("highLight")
                                     )

        self.__checked.pack_propagate(False)
        self.__checked.pack(fill=X, side=TOP, anchor=N)
        self.__checkVal.set(1)

        text = self.__dictionaries.getWordFromCurrentLanguage("importPlayfield")

        self.__loadPlayField = Button(self.__playfieldImportFrame, height=round(self.__w), width=round(self.__h),
                   bg=self.__loader.colorPalettes.getColor("window"),
                   fg=self.__loader.colorPalettes.getColor("font"),
                   activebackground=self.__loader.colorPalettes.getColor("highLight"),
                   text = text, command = self.__loadPF,
                   font = self.__normalFont, state=DISABLED
                   )
        self.__loadPlayField.pack_propagate(False)
        self.__loadPlayField.pack(side=LEFT, anchor=E, fill=X)

        t2 = Thread(target=self.__loop)
        t2.daemon = True
        t2.start()

    def __loadPF(self):
        limit1 = self.__stepY
        limit2 = len(self.__dataMatrix) - (self.__indexY * self.__stepY)

        if limit1 > limit2: limit1 = limit2

        fpath = self.__fileDialogs.askForFileName("openFile", False, ["a26", "*"],
                                                  self.__loader.mainWindow.projectPath + "playfields/")

        if fpath == "":
            return

        f = open(fpath, "r")
        text = f.read()
        f.close()

        lines = text.replace("\r","").split("\n")

        counter = 0

        """
        pieces = {0: 0, 1: 0}

        for line in lines[2:]:
            counter += 1
            if (self.__checkVal.get() == 0 and counter > limit1) or \
               (self.__checkVal.get() == 1 and counter > limit2):
               break

            line = line.split(" ")
            line.pop(-1)
            for number in line:
               try:
                   pieces[int(number)] += 1
               except:
                   pass

        isItFilled = False
        if pieces[1] > pieces[0]: isItFilled = True
        """

        dataWeNeed = []
        endData = []

        for line in lines[2:]:
            counter += 1
            if (self.__checkVal.get() == 0 and counter > limit1) or \
               (self.__checkVal.get() == 1 and counter > limit2):
               break

            line = line.split(" ")
            line.pop(-1)

            sections = [
                line[0:4],
                line[4:12],
                line[12:20],
                line[20:28],
                line[28:36],
                line[36:40]
            ]

            dataWeNeed.append(sections)
            endData.append([[],[],[],[],[],[]])

        for sectionNum in range(0,6):
            numbers = {0: 0, 1: 0}
            dominant = 0
            for lineNum in range(0, len(dataWeNeed)):
                numbers[0] += dataWeNeed[lineNum][sectionNum].count("0")
                numbers[1] += dataWeNeed[lineNum][sectionNum].count("1")

            if numbers[1] > numbers[0]: dominant = 1
            for lineNum in range(0, len(dataWeNeed)):
                if sectionNum in (0, 5):
                   for num in range(0,4,2):
                       if dataWeNeed[lineNum][sectionNum][num]     == \
                          dataWeNeed[lineNum][sectionNum][num + 1] : endData[lineNum][sectionNum].append(int(dataWeNeed[lineNum][sectionNum][num]))
                       else                                        : endData[lineNum][sectionNum].append(1 - dominant)
                else:
                    if dataWeNeed[lineNum][sectionNum][0:3].count("0") > 1: endData[lineNum][sectionNum].append(0)
                    else                                                : endData[lineNum][sectionNum].append(1)

                    if dataWeNeed[lineNum][sectionNum][3]     == \
                       dataWeNeed[lineNum][sectionNum][4]     : endData[lineNum][sectionNum].append(int(dataWeNeed[lineNum][sectionNum][3]))
                    else                                      : endData[lineNum][sectionNum].append(1 - dominant)

                    if dataWeNeed[lineNum][sectionNum][5:8].count("0") > 1: endData[lineNum][sectionNum].append(0)
                    else                                                : endData[lineNum][sectionNum].append(1)


        startX = int(self.__regionEntryVal1.get()) * self.__stepX
        startY = int(self.__regionEntryVal2.get()) * self.__stepY

        for lineNum in range(0, len(endData)):
            theLine = []
            for sectionNum in range(0,6):
                for number in range(0, len(endData[lineNum][sectionNum])):
                    theLine.append(endData[lineNum][sectionNum][number])

            for number in range(0,16):
                self.__dataMatrix[startY + lineNum][startX + number] = theLine[number]

        self.__turnOnOff()
        self.__changed = True

        self.__topLevelWindow.deiconify()
        self.__topLevelWindow.focus()

    def __changeHex(self, event):
        item = 0
        for num in range(0,4):
            if event.widget == self.__hexEntries[num].getEntry():
               item = num
               break

        if self.isItHex(self.__hexEntries[item].getValue()):
           self.__hexValues[item] = self.__hexEntries[item].getValue()

    def __pressedUp(self):
        self.__offsetVal2.set(int(self.__offsetVal2.get()) - 1)
        num = int(self.__offsetVal2.get())

        if num > self.getMsximum("Y"): num = self.getMsximum("Y")
        if num < 0: num = 0

        self.__offsetVal2.set(str(num))
        self.__indexY = num

        self.__createDataMatrix()
        self.__turnOnOff()

    def __pressedDown(self):
        self.__offsetVal2.set(int(self.__offsetVal2.get()) + 1)
        num = int(self.__offsetVal2.get())

        if num > self.getMsximum("Y"): num = self.getMsximum("Y")
        if num < 0: num = 0

        self.__offsetVal2.set(str(num))
        self.__indexY = num

        self.__createDataMatrix()
        self.__turnOnOff()

    def __pressedLeft(self):
        self.__offsetVal1.set(int(self.__offsetVal1.get()) - 1)
        num = int(self.__offsetVal1.get())

        if num > self.getMsximum("X"): num = self.getMsximum("X")
        if num < 0: num = 0

        self.__offsetVal1.set(str(num))
        self.__indexX = num

        self.__createDataMatrix()
        self.__turnOnOff()

    def __pressedRight(self):
        self.__offsetVal1.set(int(self.__offsetVal1.get()) + 1)
        num = int(self.__offsetVal1.get())

        if num > self.getMsximum("X"): num = self.getMsximum("X")
        if num < 0: num = 0

        self.__offsetVal1.set(str(num))
        self.__indexX = num

        self.__createDataMatrix()
        self.__turnOnOff()


    def __loop(self):
        done = False

        from time import sleep
        while self.dead == False and self.__loader.mainWindow.dead == False:
            if self.__finished and done == False:
               done = True
               self.__numOfLines.config(state = NORMAL)
               self.__offsetEntry1.config(state = NORMAL)
               self.__offsetEntry2.config(state = NORMAL)
               self.__regionEntry1.config(state = NORMAL)
               self.__regionEntry2.config(state = NORMAL)
               self.__dimensionEntry1.config(state = NORMAL)
               self.__dimensionEntry2.config(state = NORMAL)
               self.__loadPlayField.config(state = NORMAL)

            if self.__finished:
               if self.__indexY > 0:
                   self.__upButton.config(state = NORMAL)
               else:
                   self.__upButton.config(state=DISABLED)

               if self.__indexY < self.getMsximum("Y"):
                   self.__downButton.config(state = NORMAL)
               else:
                   self.__downButton.config(state = DISABLED)

               if self.__indexX > 0:
                   self.__leftButton.config(state = NORMAL)
               else:
                   self.__leftButton.config(state = DISABLED)

               if self.__indexX < self.getMsximum("X"):
                   self.__rightButton.config(state = NORMAL)
               else:
                   self.__rightButton.config(state = DISABLED)

               if self.changed == False:
                   self.__spriteLoader.disableSave()

               else:
                   self.__spriteLoader.enableSave()

            sleep(0.005)

    def __chamgeConst(self, event):
        if self.__finished == False: return

        call = False
        if self.isItNum(self.__offsetVal2.get()) == False:
            event.widget.config(bg=self.__colors.getColor("boxBackUnSaved"),
                                fg=self.__colors.getColor("boxFontUnSaved"))

            return

        event.widget.config(bg=self.__colors.getColor("boxBackNormal"),
                            fg=self.__colors.getColor("boxFontNormal"))

        if event.widget == self.__numOfLines:
            num = int(self.__numOfLines.get())
            if num < 0: num = 0
            if num > self.__ver: num = self.__ver
            self.__numOfLinesVal.set(str(num))
            self.__stepY = num
            call = True

        elif event.widget == self.__offsetEntry1:
            num = int(self.__offsetVal1.get())

            if num > self.getMsximum("X"): num = self.getMsximum("X")
            if num < 0: num = 0

            self.__offsetVal1.set(str(num))
            self.__indexX = num
            call = True

        elif event.widget == self.__offsetEntry2:
            num = int(self.__offsetVal2.get())

            if num > self.getMsximum("Y"): num = self.getMsximum("Y")
            if num < 0: num = 0

            self.__offsetVal2.set(str(num))
            self.__indexY = num
            call = True

        elif event.widget == self.__regionEntry1:
            num = int(self.__regionEntryVal1.get())
            if num > self.__matrix[0]-1: num = self.__matrix[0]-1
            if num < 0: num = 0

            self.__regionEntryVal1.set(str(num))
            self.__offsetVal1.set(str(num * self.__stepX))

            self.__indexX = num * self.__stepX
            call = True

        elif event.widget == self.__regionEntry2:
            num = int(self.__regionEntryVal2.get())
            if num > self.__matrix[1]-1: num = self.__matrix[1]-1
            if num < 0: num = 0

            self.__regionEntryVal2.set(str(num))
            self.__offsetVal2.set(str(num * self.__stepY))

            self.__indexY = num * self.__stepY
            call = True

        elif event.widget == self.__dimensionEntry1:
            num = int(self.__dimensionEntryVal1.get())
            if num < 1: num = 1
            if num > 256: num = 256

            self.__matrix[0] = num
            self.__dimensionEntryVal1.set(str(num))

            num = int(self.__offsetVal1.get())

            if num > self.getMsximum("X"): num = self.getMsximum("X")
            if num < 0: num = 0

            self.__offsetVal1.set(str(num))
            self.__indexX = num
            call = True

        elif event.widget == self.__dimensionEntry2:
            num = int(self.__dimensionEntryVal2.get())
            if num < 1: num = 1
            if num > 256: num = 256

            self.__matrix[1] = num
            self.__dimensionEntryVal2.set(str(num))

            num = int(self.__offsetVal2.get())

            if num > self.getMsximum("Y"): num = self.getMsximum("Y")
            if num < 0: num = 0

            self.__offsetVal2.set(str(num))
            self.__indexY = num
            call = True

        if call:
            self.__createDataMatrix()
            self.__turnOnOff()

    def getMsximum(self, dir):
        if dir == "X":
            return (self.__matrix[1] * self.__stepX) - self.__hor - 1
        else:
            return (self.__matrix[0] * self.__stepY) - self.__ver - 1

    def __checkIfValidFileName(self, event):

        name = str(event.widget).split(".")[-1]

        value  = None
        widget = None
        if name == "spriteName":
            widget = self.__spriteLoader.getEntry()
            value = self.__spriteLoader.getValue()


        if self.__loader.io.checkIfValidFileName(value) and (" " not in value):
            widget.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                      fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                      )

        else:
            widget.config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                                      fg=self.__loader.colorPalettes.getColor("boxFontUnSaved"),
                                      )

    def __openMM(self):
        pass

    def __saveMM(self):
        pass

    def __loadTest(self):
        pass

    def __drawTable(self):
        for theY in range(0, self.__ver):
            f = Frame(self.__editorFrame,
                      bg = self.__loader.colorPalettes.getColor("window"),
                      width = self.__sizes[0], height = self.__h
                      )
            f.pack_propagate(False)
            f.pack(side=TOP, anchor=N, fill=X)
            self.__frames.append(f)
            self.__soundPlayer.playSound("Pong")
            self.__matrixButtons.append([])

            for theX in range(0, self.__hor):
                f = Frame(self.__frames[-1],
                          bg=self.__loader.colorPalettes.getColor("window"),
                          width=self.__w, height=self.__h
                          )
                f.pack_propagate(False)
                f.pack(side=LEFT, anchor=E, fill=Y)
                self.__subFrames.append(f)

                b = Button(f, height = round(self.__w), width = round(self.__h), name = str(theY) + "_" + str(theX),
                            bg = self.__loader.colorPalettes.getColor("boxBackNormal"),
                           activebackground = self.__loader.colorPalettes.getColor("highLight"),
                           relief=GROOVE, state = DISABLED
                           )
                b.pack_propagate(False)
                b.pack(side=LEFT, anchor=E, fill = BOTH)

                self.__matrixButtons[-1].append(b)

                b.bind("<Button-1>", self.__clicked)
                b.bind("<Button-3>", self.__clicked)
                b.bind("<Enter>", self.__enter)

        self.__createDataMatrix()
        self.__turnOnOff()
        self.__finished = True

    def __createDataMatrix(self):
        w = self.__matrix[0] * self.__stepX
        h = self.__matrix[1] * self.__stepY

        addOrPop = h - len(self.__dataMatrix)

        if   addOrPop > 0:
            for num in range(0, addOrPop):
                self.__dataMatrix.append([])
                for num in range(0, w):
                    self.__dataMatrix[-1].append(0)

        elif addOrPop < 0:
            for num in range(0, abs(addOrPop)):
                self.__dataMatrix.pop(-1)

        for subList in self.__dataMatrix:
            addOrPop = w - len(subList)
            if   addOrPop > 0:
               for num in range(0, addOrPop):
                   subList.append(0)
            elif addOrPop < 0:
                for num in range(0, abs(addOrPop)):
                   subList.pop(-1)

        #print(len(self.__dataMatrix), len(self.__dataMatrix[0]))
        #print(self.getMsximum("Y"), self.getMsximum("X"))

    def __turnOnOff(self):
        for theY in range(0, self.__ver):
            for theX in range(0, self.__hor):
                self.colorButton(theX, theY)

    def colorButton(self, theX, theY):
        w = (self.__matrix[0] * self.__stepX)
        h = (self.__matrix[1] * self.__stepY)

        colors = [
            self.__loader.colorPalettes.getColor("boxBackNormal"),
            self.__loader.colorPalettes.getColor("boxFontUnSaved"),
            self.__loader.colorPalettes.getColor("font"),
            self.__loader.colorPalettes.getColor("boxBackUnSaved")
        ]

        #print(theX, theY, theX + self.__indexX, theY + self.__indexY )
        chsnger = ((theX + self.__indexX) // self.__stepX) % 2 + (((theY + self.__indexY) // self.__stepY) % 2) == 1

        disable = False
        try:
            teszt = self.__dataMatrix[theY + self.__indexY][theX + self.__indexX]
        except:
            disable = True

        if (theX >= w + self.__indexX or theY + self.__indexY >= h) or disable == True:
            self.__matrixButtons[theY][theX].config(
                state=DISABLED,
                bg=self.__loader.colorPalettes.getColor("fontDisabled")
            )
        elif self.__dataMatrix[theY + self.__indexY][theX + self.__indexX] == 1:
            if chsnger:
                self.__matrixButtons[theY][theX].config(
                    state=NORMAL,
                    bg=colors[3]
                )
            else:
                self.__matrixButtons[theY][theX].config(
                    state=NORMAL,
                    bg=colors[2]
                )

        elif chsnger:
            self.__matrixButtons[theY][theX].config(
                state=NORMAL,
                bg=colors[1]
            )
        else:
            self.__matrixButtons[theY][theX].config(
                state=NORMAL,
                bg=colors[0]
            )

        self.__changed = True

    def __getNameXY(self, event):
        name = str(event.widget).split(".")[-1]
        numbers = name.split("_")
        origY = int(numbers[0])
        origX = int(numbers[1])
        currentX = origX + self.__indexX
        currentY = origY + self.__indexY

        return(name, origX, origY, currentX, currentY)

    def __clicked(self, event):
        if self.__finished == False: return

        name, origX, origY, currentX, currentY = self.__getNameXY(event)
        if (currentX >= self.__matrix[1] * self.__stepX) or\
           (currentY >= self.__matrix[0] * self.__stepY): return

        colors = [
            self.__loader.colorPalettes.getColor("boxBackNormal"),
            self.__loader.colorPalettes.getColor("boxFontUnSaved"),
            self.__loader.colorPalettes.getColor("font"),
            self.__loader.colorPalettes.getColor("boxBackUnSaved")
        ]

        button = 0
        try:
            button = int(str(event).split(" ")[3].split("=")[1])
        except:
            if self.__ctrl:
                button = 3
            else:
                button = 1

        if self.__ctrl == False and button == 3:
            return

        if self.__ctrl == False:
            self.__dataMatrix[currentY][currentX] = 1 - self.__dataMatrix[currentY][currentX]
        else:
            if button == 1:
                self.__dataMatrix[currentY][currentX] = 1
            else:
                self.__dataMatrix[currentY][currentX] = 0

        self.colorButton(origX, origY)

    def __enter(self, event):
        if self.__draw == 0: return
        self.__clicked(event)

    def shiftON(self, event):
        self.__ctrl = True

    def shiftOff(self, event):
        self.__ctrl = False

    def drawMode(self, event):
        if self.__draw == 1:
           self.__draw = 0
        else:
           self.__draw = 1

    def isItBin(self, num):
        if num[0] != "%": return False

        try:
            teszt = int("0b" + num[1:], 2)
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

    def isItNum(self, num):
        try:
            num = int(num)
            return True
        except:
            return False