from tkinter import *

class EditorBigFrame:

    def __init__(self, loader, frame):

        self.__loader = loader
        self.__editor = self.__loader.mainWindow

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
        self.__syntaxList = self.__loader.syntaxList
        self.__objectMaster = self.__loader.virtualMemory.objectMaster
        self.__foundError     = False

        self.__words = ["lineNum", "level", "command#1", "command#2", "command#3",
                        "param#1", "param#2", "param#3", "comment", "updateRow"]
        self.__subroutines = []

        self.__focused = None
        self.__screenSize = self.__loader.screenSize
        self.__counter    = 0
        self.__counter2    = 0
        self.firstTry = True

        self.__cursorPoz  = [1,0]
        self.__listOfItems = []

        self.__destroyables = {}
        self.__lastButton   = None
        self.__focused2 = None
        #self.__searchLine = 0

        self.__lbFocused = False

        self.exiters = ["exit", "goto", "return", "leave", "resetScreen", "resetGame"]
        self.__unreachableLVL = -1
        self.__unreachableNum = -1

        miniSize = 0.65
        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize*miniSize), False, False, False)
        self.__tinyFont = self.__fontManager.getFont(int(self.__fontSize*0.45), False, False, False)
        self.__halfFont = self.__fontManager.getFont(int(self.__fontSize*0.57), False, False, False)

        self.__changed = False
        self.__frame = Frame(frame, width=self.__editor.getWindowSize()[0],
                                   height=self.__editor.getWindowSize()[1],
                                   bg=self.__colors.getColor("window"))
        self.__frame.pack_propagate(False)
        self.__frame.pack(side=TOP, anchor = N, fill=BOTH)
        self.__frame.pack(side=TOP, anchor = N, fill=BOTH)

        sizes = (0.20, 0.60, 0.20)

        self.__leftFrame = Frame(self.__frame, width=round(self.__editor.getWindowSize()[0]*sizes[0]),
                                   height=self.__editor.getWindowSize()[1],
                                   bg=self.__colors.getColor("window"))
        self.__leftFrame.pack_propagate(False)
        self.__leftFrame.pack(side=LEFT, anchor = E, fill=Y)

        self.__mainFrame = Frame(self.__frame, width=round(self.__editor.getWindowSize()[0]*sizes[1]),
                                   height=self.__editor.getWindowSize()[1],
                                   bg=self.__colors.getColor("window"))
        self.__mainFrame.pack_propagate(False)
        self.__mainFrame.pack(side=LEFT, anchor = E, fill=Y)

        self.__rightFrame = Frame(self.__frame, width=round(self.__editor.getWindowSize()[0]*sizes[2]),
                                   height=self.__editor.getWindowSize()[1],
                                   bg=self.__colors.getColor("window"))
        self.__rightFrame.pack_propagate(False)
        self.__rightFrame.pack(side=LEFT, anchor = E, fill=Y)

        self.activeMode = None
        # Valid modes: intro, editor, locked, empty
        self.__selectedMode = "intro"

        self.addBindings()

        self.__highLightWord       = None
        self.__highLightIgnoreCase = True

        from threading import Thread
        self.__ctrl = False

        self.__focusOutItems = []
        self.__theNumOfLine  = 0

        t = Thread(target=self.loop)
        t.daemon = True
        t.start()

    def addBindings(self):
        self.__bankButtons    = self.__editor.changerButtons
        self.__sectionButtons = self.__editor.sectionButtons

        for button in self.__bankButtons:
            button.bind("<ButtonRelease-1>", self.changeSomething)

        for button in self.__sectionButtons:
            button.bind("<ButtonRelease-1>", self.changeSomething)

    def changeSomething(self, event):
        from copy import deepcopy

        button = event.widget
        if button in self.__bankButtons:
           self.__currentBank = "bank" + str(self.__bankButtons.index(button)+2)
        else:
           secs = deepcopy(self.__loader.sections)
           for item in ['local_variables', 'screen_bottom', 'screen_top', 'special_read_only']:
               secs.remove(item)

           self.__currentSection = secs[self.__sectionButtons.index(button)]

        self.loadCurrentFromMemory()

    def __focusIn(self, event):
        self.__focused  = event.widget
        self.__focused2 = event.widget

        textToPrint = self.__getFakeLine(self.__codeEditorItems)

        selectPosizions = []
        errorPositions = []

        objectList = self.__objectMaster.getStartingObjects()
        objectList.append("game")

        self.__lineTinting(textToPrint, objectList, self.__theNumOfLine,
                           selectPosizions, errorPositions, "lineEditor", None, None)

    def __insertPressed(self, event):
        self.__insertSelectedFromBox()

    def __insertSelectedFromBox(self):
        try:
            selected = self.__listOfItems[self.__listBoxOnTheRight.curselection()[0]]
        except:
            return

        if self.__focused2 == None:
           return

        if self.__focused2 == self.__codeBox:
           text = self.__codeBox.get(0.0, END).split("\n")
           theLine = text[self.__cursorPoz[0]-1]
           currentWord = self.getCurrentWord(theLine)

           cutPoz = self.__cursorPoz[1] - len(currentWord)

           theLine = theLine[:cutPoz] + selected + theLine[self.__cursorPoz[1]:]
           text[self.__cursorPoz[0]-1] = theLine

           self.updateText(text)
        else:
           for itemName in self.__codeEditorItems.keys():
               item = self.__codeEditorItems[itemName]
               if type(item) == list:
                  if item[1] == self.__focused2:
                     item[0].set(selected)
                     item[1].focus()
                     item[1].icursor(len(selected))

                     self.__codeEditorItems["updateRow"].config(state=NORMAL)
                     textToPrint = self.__getFakeLine(self.__codeEditorItems)

                     selectPosizions = []
                     errorPositions = []
                     objectList = self.__objectMaster.getStartingObjects()

                     self.__lineTinting(textToPrint, objectList, self.__theNumOfLine,
                                        selectPosizions, errorPositions, "lineEditor", None, None)
                     break

    def getCurrentBank(self):
        return self.__currentBank

    def loop(self):
        from time import sleep

        while self.__editor.dead == False:
            if self.activeMode != self.__selectedMode:
               if self.activeMode != None:
                   self.__removeSlaves()

               self.activeMode = self.__selectedMode
               self.__editor.editor.unbind("<Insert>")

               if self.__selectedMode == "intro":
                  self.__createIntroScreen()
               elif  self.__selectedMode == "empty":
                  pass
               elif  self.__selectedMode == "job":
                  self.__createJobWindows()

            if self.__counter > 0:
               self.__counter -= 1

            if self.__counter2 > 0:
               self.__counter2 -= 1

            if self.__counter  == 1: self.__counterEnded()
            if self.__counter2 == 1: self.__counterEnded2()

            if self.activeMode == "job":
                for bankNum in range(2,9):
                    key = "bank" + str(bankNum)
                    if self.__virtualMemory.locks[key] == None:
                        self.__bankButtons[bankNum - 2].config(state=NORMAL)
                    else:
                        self.__bankButtons[bankNum - 2].config(state=DISABLED)

                if self.__virtualMemory.locks[self.__currentBank] == None:
                   state = NORMAL
                else:
                   state = DISABLED


                for button in self.__sectionButtons:
                    button.config(state = state)

                if  self.__foundError    == False:
                    self.__compileASMButton.config(state = NORMAL)
                else:
                    self.__compileASMButton.config(state = DISABLED)

            else:
                for button in self.__sectionButtons:
                    button.config(state = DISABLED)
                for button in self.__bankButtons:
                    button.config(state = DISABLED)

            curSel = None
            try:
                curSel = self.__listBoxOnTheRight.curselection()[0]
                self.__button.config(state = NORMAL)
            except:
                try:
                    self.__button.config(state = DISABLED)
                except:
                    pass

            sleep(0.05)

    def __removeSlaves(self):
        self.__mainFrame.config(bg = self.__loader.colorPalettes.getColor("window"))
        self.__leftFrame.config(bg = self.__loader.colorPalettes.getColor("window"))
        self.__rightFrame.config(bg = self.__loader.colorPalettes.getColor("window"))

        self.__destroyables = {}

        for slave in self.__leftFrame.pack_slaves():
            slave.destroy()

        for slave in self.__mainFrame.pack_slaves():
            slave.destroy()

        for slave in self.__rightFrame.pack_slaves():
            slave.destroy()

    def __createIntroScreen(self):
        from AtariLogo import AtariLogo

        self.__mainFrame.config(bg = "black")
        self.__leftFrame.config(bg = "black")
        self.__rightFrame.config(bg = "black")

        atariLogo = AtariLogo(self.__loader, self.__mainFrame, self.__leftFrame, self.__rightFrame)

        self.__destroyables["AtariLogo"] = atariLogo

    def setMode(self, mode):
        self.__selectedMode = mode

    def getMode(self):
        return self.activeMode

    def __createJobWindows(self):
        from tkinter import scrolledtext

        per = 25

        self.__codeFrameEditor = Frame(self.__mainFrame, width= self.__mainFrame.winfo_width(),
                                 height=self.__editor.getWindowSize()[1] // per,
                                 bg=self.__colors.getColor("window"))

        self.__codeFrameEditor.pack_propagate(False)
        self.__codeFrameEditor.pack(side=BOTTOM, anchor=S, fill=X)

        self.__codeFrameHeader = Frame(self.__mainFrame, width= self.__mainFrame.winfo_width(),
                                 height=self.__editor.getWindowSize()[1] // per,
                                 bg=self.__colors.getColor("window"))

        self.__codeFrameHeader.pack_propagate(False)
        self.__codeFrameHeader.pack(side=BOTTOM, anchor=S, fill=X)

        self.__codeBox    = scrolledtext.ScrolledText(self.__mainFrame, width=999999, height=self.__mainFrame.winfo_height(), wrap=NONE)
        self.__hscrollbar = Scrollbar(self.__mainFrame, orient=HORIZONTAL, command=self.__codeBox.xview)
        self.__codeBox.config(xscrollcommand=self.__hscrollbar.set)
        self.__hscrollbar.pack(side=BOTTOM, fill=X, anchor=S)
        self.__codeBox.pack(fill=BOTH, side=BOTTOM, anchor=S)

        self.__codeBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                        fg=self.__loader.colorPalettes.getColor("boxFontNormal"))

        self.__codeBox.bind("<Key>", self.__keyPressed)
        self.__codeBox.bind("<KeyRelease>", self.__keyReleased)
        self.__codeBox.bind("<MouseWheel>", self.__mouseWheel)
        self.__codeBox.bind("<FocusIn>", self.__loader.mainWindow.focusIn)
        self.__codeBox.bind("<FocusOut>", self.focusOut)
        self.__codeBox.bind("<ButtonRelease-1>", self.clicked)

        self.__editor.editor.bind("<Insert>", self.__insertPressed)

        self.__currentBank    = "bank2"
        self.__currentSection = "overscan"

        self.__validKeys = [
            "enter", "leave", "overscan", "vblank", "subroutines"
        ]

        self.__getFont()
        sizes = (0.20, 0.60, 0.20)

        self.__labelFrames       = []
        self.__codeEditorItems   = {}

        self.createCodeLine(self.__labelFrames, self.__codeEditorItems, True)

        self.__button = Button(
            self.__rightFrame, width=round(self.__editor.getWindowSize()[0]*sizes[2]),
            bg=self.__colors.getColor("window"),
            fg=self.__colors.getColor("font"),
            font=self.__normalFont, state = DISABLED,
            command=self.__insertSelectedFromBox,
            text=self.__dictionaries.getWordFromCurrentLanguage("insertItem")
        )

        self.__button.pack_propagate(False)
        self.__button.pack(side=BOTTOM, anchor=S, fill=X)

        text = self.__dictionaries.getWordFromCurrentLanguage("recommendations")
        if text.endswith(":") == False: text += ":"

        self.__labelOnTheRight = Label(self.__rightFrame, text=text,
                  font=self.__smallFont, fg=self.__colors.getColor("font"),
                  bg=self.__colors.getColor("window"), justify=CENTER
                  )

        self.__labelOnTheRight.pack_propagate(False)
        self.__labelOnTheRight.pack(side=TOP, anchor=CENTER, fill=BOTH)

        s = Scrollbar(self.__rightFrame)
        l = Listbox(self.__rightFrame, width=100000,
                    height=1000,
                    yscrollcommand=s.set,
                    selectmode=BROWSE,
                    exportselection=False,
                    font=self.__smallFont,
                    justify=LEFT
                    )

        l.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        l.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        l.pack_propagate(False)

        s.pack(side=RIGHT, anchor=W, fill=Y)
        l.pack(side=LEFT, anchor=W, fill=BOTH)

        s.config(command=l.yview)

        self.__scrollBarOnTheRight = s
        self.__listBoxOnTheRight   = l
        self.firstTry = True

        self.__listBoxOnTheRight.bind("<FocusIn>", self.__lbFocusIn)
        self.__listBoxOnTheRight.bind("<FocusOut>", self.__lbFocusOut)

        fSize = self.__editor.getWindowSize()[1] // 6

        self.__searchFrame = Frame(self.__leftFrame, width=self.__editor.getWindowSize()[0],
                                   height=fSize,
                                   bg=self.__colors.getColor("window"))
        self.__searchFrame.pack_propagate(False)
        self.__searchFrame.pack(side=TOP, anchor = N, fill=X)

        hSize =  fSize // 6

        self.__slabel = Label(self.__searchFrame, text=self.__dictionaries.getWordFromCurrentLanguage("findWord"),
                      font=self.__normalFont,
                      fg = self.__loader.colorPalettes.getColor("font"),
                      bg = self.__loader.colorPalettes.getColor("window"),
                      justify=CENTER
                      )

        self.__slabel.pack_propagate(False)
        self.__slabel.pack(side=TOP, anchor=N, fill=BOTH)

        self.__searchEntryFrame = Frame(self.__searchFrame, width=self.__editor.getWindowSize()[0],
                                   height=hSize,
                                   bg=self.__colors.getColor("window"))
        self.__searchEntryFrame.pack_propagate(False)
        self.__searchEntryFrame.pack(side=TOP, anchor = N, fill=X)

        self.__sentryVar = StringVar()

        self.__sentry = Entry(self.__searchEntryFrame, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                      width=99999,
                      fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                      textvariable=self.__sentryVar,
                      font=self.__smallFont, justify=LEFT,
                      )
        self.__sentry.pack_propagate()
        self.__sentry.pack(side=TOP, anchor=N, fill=BOTH)

        self.__sentry.bind("<FocusOut>", self.__changeHighLightWord)
        self.__sentry.bind("<KeyRelease>", self.__changeHighLightWord)

        self.__searchBoxFrame = Frame(self.__searchFrame, width=self.__editor.getWindowSize()[0],
                                   height=hSize,
                                   bg=self.__colors.getColor("window"))
        self.__searchBoxFrame.pack_propagate(False)
        self.__searchBoxFrame.pack(side=TOP, anchor = N, fill=X)

        self.__ignoreCase = IntVar()
        self.__ignoreCaseButton = Checkbutton(self.__searchBoxFrame,
                                       text=self.__dictionaries.getWordFromCurrentLanguage("ignoreCase"),
                                       bg=self.__colors.getColor("window"),
                                       fg=self.__colors.getColor("font"),
                                       justify=LEFT, font=self.__miniFont,
                                       variable=self.__ignoreCase,
                                       activebackground=self.__colors.getColor("highLight"),
                                       activeforeground=self.__loader.colorPalettes.getColor("font"),
                                       command=self.__ignoreCaseChange
                                       )

        self.__ignoreCaseButton.pack_propagate(False)
        self.__ignoreCaseButton.pack(fill=X, side=LEFT, anchor=E)

        self.__searchButtonsFrame = Frame(self.__searchFrame, width=self.__editor.getWindowSize()[0],
                                   height=hSize,
                                   bg=self.__colors.getColor("window"))
        self.__searchButtonsFrame.pack_propagate(False)
        self.__searchButtonsFrame.pack(side=TOP, anchor = N, fill=X)

        half = round((self.__editor.getWindowSize()[0]*sizes[0]) // 2)

        self.__searchButtonsFrame1 = Frame(self.__searchButtonsFrame, width=half,
                                   height=hSize,
                                   bg=self.__colors.getColor("window"))
        self.__searchButtonsFrame1.pack_propagate(False)
        self.__searchButtonsFrame1.pack(side=LEFT, anchor = E, fill=X)

        self.__searchButtonsFrame2 = Frame(self.__searchButtonsFrame, width=half,
                                   height=hSize,
                                   bg=self.__colors.getColor("window"))
        self.__searchButtonsFrame2.pack_propagate(False)
        self.__searchButtonsFrame2.pack(side=LEFT, anchor = E, fill=BOTH)

        self.__searchButton1 = Button(
            self.__searchButtonsFrame1, width=999999999,
            bg=self.__colors.getColor("window"),
            fg=self.__colors.getColor("font"),
            font=self.__normalFont, state = DISABLED,
            command=self.prevFound,
            text="<<"
        )

        self.__searchButton1.pack_propagate(False)
        self.__searchButton1.pack(side=TOP, anchor = N, fill = BOTH)

        self.__searchButton2 = Button(
            self.__searchButtonsFrame2, width=999999999,
            bg=self.__colors.getColor("window"),
            fg=self.__colors.getColor("font"),
            font=self.__normalFont, state=DISABLED,
            command=self.nextFound,
            text=">>"
        )

        self.__searchButton2.pack_propagate(False)
        self.__searchButton2.pack(side=TOP, anchor=N, fill=BOTH)

        self.__replaceEntryFrame = Frame(self.__searchFrame, width=self.__editor.getWindowSize()[0],
                                   height=hSize,
                                   bg=self.__colors.getColor("window"))
        self.__replaceEntryFrame.pack_propagate(False)
        self.__replaceEntryFrame.pack(side=TOP, anchor = N, fill=X)

        self.__rentryVal = StringVar()
        self.__rentry = Entry(self.__replaceEntryFrame, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                      width=99999,
                      fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                      textvariable=self.__rentryVal,
                      font=self.__smallFont, justify=LEFT,
                      )
        self.__rentry.pack_propagate()
        self.__rentry.pack(side=TOP, anchor=N, fill=BOTH)

        self.__replaceButtonFrame = Frame(self.__searchFrame, width=self.__editor.getWindowSize()[0],
                                   height=hSize,
                                   bg=self.__colors.getColor("window"))
        self.__replaceButtonFrame.pack_propagate(False)
        self.__replaceButtonFrame.pack(side=TOP, anchor = N, fill=X)

        self.__replaceButtonFrame1 = Frame(self.__replaceButtonFrame, width=half,
                                   height=hSize,
                                   bg=self.__colors.getColor("window"))
        self.__replaceButtonFrame1.pack_propagate(False)
        self.__replaceButtonFrame1.pack(side=LEFT, anchor = E, fill=X)

        self.__replaceButtonFrame2 = Frame(self.__replaceButtonFrame, width=half,
                                   height=hSize,
                                   bg=self.__colors.getColor("window"))
        self.__replaceButtonFrame2.pack_propagate(False)
        self.__replaceButtonFrame2.pack(side=LEFT, anchor = E, fill=BOTH)


        self.__replaceButton1 = Button(
            self.__replaceButtonFrame1, width=999999999,
            bg=self.__colors.getColor("window"),
            fg=self.__colors.getColor("font"),
            font=self.__smallFont, state = DISABLED,
            command=self.replaceInLine,
            text=self.__dictionaries.getWordFromCurrentLanguage("replaceInLine")
        )

        self.__replaceButton2 = Button(
            self.__replaceButtonFrame2, width=999999999,
            bg=self.__colors.getColor("window"),
            fg=self.__colors.getColor("font"),
            font=self.__smallFont, state = DISABLED,
            command=self.replaceAll,
            text=self.__dictionaries.getWordFromCurrentLanguage("replaceAll")
        )

        self.__replaceButton1.pack_propagate(False)
        self.__replaceButton1.pack(side=TOP, anchor = N, fill = BOTH)

        self.__replaceButton2.pack_propagate(False)
        self.__replaceButton2.pack(side=TOP, anchor = N, fill = BOTH)

        self.__prettyFrame = Frame(self.__leftFrame, width=self.__editor.getWindowSize()[0],
                                   height=fSize//4,
                                   bg=self.__colors.getColor("window"))
        self.__prettyFrame.pack_propagate(False)
        self.__prettyFrame.pack(side=TOP, anchor = N, fill=X)

        self.__alissFrame = Frame(self.__leftFrame, width=self.__editor.getWindowSize()[0],
                                   height=fSize//4,
                                   bg=self.__colors.getColor("window"))
        self.__alissFrame.pack_propagate(False)
        self.__alissFrame.pack(side=TOP, anchor = N, fill=X)

        self.__compileFrame = Frame(self.__leftFrame, width=self.__editor.getWindowSize()[0],
                                   height=fSize//4,
                                   bg=self.__colors.getColor("window"))
        self.__compileFrame.pack_propagate(False)
        self.__compileFrame.pack(side=TOP, anchor = N, fill=X)

        self.__prettyButton = Button(
            self.__prettyFrame, width=999999999,
            bg=self.__colors.getColor("window"),
            fg=self.__colors.getColor("font"),
            font=self.__smallFont,
            command=self.reIndent,
            text=self.__dictionaries.getWordFromCurrentLanguage("reIndent")
        )

        self.__prettyButton.pack_propagate(False)
        self.__prettyButton.pack(side=TOP, anchor = N, fill = BOTH)

        """
        self.__compileFrame = Frame(self.__leftFrame, width=self.__editor.getWindowSize()[0],
                                   height=fSize//2,
                                   bg=self.__colors.getColor("comment"))
        self.__compileFrame.pack_propagate(False)
        self.__compileFrame.pack(side=TOP, anchor = N, fill=X)
        """

        self.__aliasToCommand = Button(
            self.__alissFrame, width=999999999,
            bg=self.__colors.getColor("window"),
            fg=self.__colors.getColor("font"),
            font=self.__smallFont,
            command=self.__convertAliasToCommand,
            text=self.__dictionaries.getWordFromCurrentLanguage("aliasToCommand")
        )


        self.__aliasToCommand.pack_propagate(False)
        self.__aliasToCommand.pack(side=TOP, anchor = N, fill = BOTH)

        self.__compileASMButton = Button(
            self.__compileFrame, width=999999999,
            bg=self.__colors.getColor("window"),
            fg=self.__colors.getColor("font"),
            font=self.__smallFont,
            command=self.compileToASM,
            text=self.__dictionaries.getWordFromCurrentLanguage("convertASM")
        )


        self.__compileASMButton.pack_propagate(False)
        self.__compileASMButton.pack(side=TOP, anchor = N, fill = BOTH)

        self.getLineStructure(None, None, True)
        self.loadCurrentFromMemory()

    def __convertAliasToCommand(self):
        selection = [1.0, self.__codeBox.index(END)]
        try:
            sel_start = self.__codeBox.index("sel.first")
            sel_end   = self.__codeBox.index("sel.last")
            selection = [sel_start, sel_end]
        except:
            pass

        text = self.__codeBox.get(0.0, END).replace("\r","").split("\n")
        newText = []

        start = int(str(selection[0]).split(".")[0])-1
        end   = int(str(selection[1]).split(".")[0])-1

        for lineNum in range(start, end):
            if lineNum >= len(text): break

            foundIt = False
            lineData = self.getLineStructure(lineNum, text, True)
            if lineData["command"][0] not in ['', None, "None"]:
                for c in self.__syntaxList.keys():
                     if lineData["command"][0] in self.__syntaxList[c].alias:
                        s = lineData["command"][1][0]
                        e = lineData["command"][1][1]
                        newText.append(text[lineNum][:s] + c + text[lineNum][e+1:])
                        foundIt = True
            if foundIt == False:
               newText.append(text[lineNum])

        self.updateText(newText)

    def compileToASM(self):
        selection = [1.0, self.__codeBox.index(END)]
        try:
            sel_start = self.__codeBox.index("sel.first")
            sel_end   = self.__codeBox.index("sel.last")
            selection = [sel_start, sel_end]
        except:
            pass

        text = self.__codeBox.get(0.0, END).replace("\r","").split("\n")

        lineNumOfEnd = int(str(selection[1]).split(".")[0])
        thatLine = text[lineNumOfEnd-1]

        selection[0] = str(selection[0]).split(".")[0] + ".0"
        selection[1] = str(selection[1]).split(".")[0] + "." + str(len(thatLine))

        firstLineStruct = self.getLineStructure(int(selection[0].split(".")[0])-1, text, True)
        lastLineStruct  = self.getLineStructure(int(selection[1].split(".")[0])-1, text, True)

        errorFound = False
        errorData  = None

        noneList = ["", "None", None]

        for lineNum in range(firstLineStruct["lineNum"], lastLineStruct["lineNum"] + 1):
            currentLineStructure = self.getLineStructure(lineNum, text, True)

            if currentLineStructure["command"][0] in noneList:
               continue

            if currentLineStructure["command"][0] not in self.__syntaxList:
                foundObjects = self.findObjects(currentLineStructure["command"][0],
                                                self.__objectMaster.getStartingObjects())

                if foundObjects == {}:
                   errorFound = True
                   errorData = {"line": str(lineNum), "type": "command"}
                   break
            else:
                if self.__syntaxList[currentLineStructure["command"][0]].endNeeded == True:
                   endFound = self.findEnd(currentLineStructure, lineNum, text)
                   if endFound == False:
                      errorFound = True
                      errorData  = {"line": str(lineNum), "type": "end"}
                      break
                   else:
                      endY    = endFound[0]
                      if endY > lastLineStruct["lineNum"]: selection[1] = str(endY) + "." + str(len(text[endY]))

                elif currentLineStructure["command"][0].startswith("end-") == True:
                   startFound = self.__findStart(currentLineStructure, lineNum, text)
                   if startFound == False:
                      errorFound = True
                      errorData  = {"line": str(lineNum), "type": "start"}
                      break
                   else:
                      startY    = startFound[0]
                      if startY < firstLineStruct["lineNum"]: selection[0] = str(startY) + ".0"

        if errorFound:
           self.__loader.fileDialogs.displayError("errorOnASMConvert", "errorOnASMConvertText", errorData, None)
        else:
           from FirstCompiler import FirstCompiler

           c = FirstCompiler(self.__loader, self, self.__codeBox.get(selection[0],
                                                                     selection[1]),
                             True, "forEditor", self.__currentBank, self.__currentSection, int(selection[0].split(".")[0]), self.__codeBox.get(0.0, END))
           print(c.result)
           print(c.errorList)


    def loadCurrentFromMemory(self):
        self.__loadFromMemory(self.__currentBank, self.__currentSection)

    def createCodeLine(self, labelFrames, codeEditorItems, appendThem):
        bannerItems = [[self.__dictionaries.getWordFromCurrentLanguage("number")        , 1.5, Label,  None],
                       [self.__dictionaries.getWordFromCurrentLanguage("level")         , 1.5, Label,  None],
                       [self.__dictionaries.getWordFromCurrentLanguage("command") + "#1", 1.75,   Entry,  NORMAL],
                       [self.__dictionaries.getWordFromCurrentLanguage("command") + "#2", 1.75,   Entry,  NORMAL],
                       [self.__dictionaries.getWordFromCurrentLanguage("command") + "#3", 1.75,   Entry,  NORMAL],
                       [self.__dictionaries.getWordFromCurrentLanguage("param") + "#1"  , 2,   Entry,  DISABLED],
                       [self.__dictionaries.getWordFromCurrentLanguage("param") + "#2"  , 2,   Entry,  DISABLED],
                       [self.__dictionaries.getWordFromCurrentLanguage("param") + "#3"  , 2,   Entry,  DISABLED],
                       [self.__dictionaries.getWordFromCurrentLanguage("comment")       , 3,   Entry,  NORMAL],
                       [self.__dictionaries.getWordFromCurrentLanguage("updateRow")     , 1.5, Button, self.updateTextFromDisplay]
                       ]

        colors = [[self.__colors.getColor("font"), self.__colors.getColor("window")],
                  [self.__colors.getColor("window"), self.__colors.getColor("font")]]

        sumItems = 0

        for bannerItem in bannerItems:
            sumItems += len(bannerItem[0]) * bannerItem[1]

        bannerItemLens = []
        xUnit = round((self.__mainFrame.winfo_width() / sumItems))

        for item in bannerItems:
            bannerItemLens.append(
                int(len(item[0])  * xUnit * item[1])
            )

            f = Frame(self.__codeFrameHeader, width=bannerItemLens[-1],
                                         height=99999999,
                                         bg=self.__colors.getColor("window"))
            if appendThem:
                f.pack_propagate(False)
                f.pack(side=LEFT, anchor = E, fill=Y)
                labelFrames.append(f)

            num = bannerItems.index(item)
            c = colors[num%2]

            label = Label(f, text=item[0],
                      font=self.__miniFont, fg=c[0], bg=c[1], justify=CENTER
                      )

            if appendThem:
                label.pack_propagate(False)
                label.pack(side=TOP, anchor=N, fill=BOTH)

            f2 = Frame(self.__codeFrameEditor, width=bannerItemLens[-1],
                                         height=99999999,
                                         bg=self.__colors.getColor("window"))
            if appendThem:
                f2.pack_propagate(False)
                f2.pack(side=LEFT, anchor = E, fill=Y)
                labelFrames.append(f2)

            if   bannerItems[num][2] == Label:
                label = Label(f2, text="-",
                              font=self.__miniFont,
                              fg=self.__colors.getColor("font"),
                              bg=self.__colors.getColor("window"),
                              justify=CENTER
                              )
                if appendThem:
                    label.pack_propagate(False)
                    label.pack(side=TOP, anchor=N, fill=BOTH)

                codeEditorItems[self.__words[num]] = label

            elif bannerItems[num][2] == Entry:
                entryVar = StringVar()

                entry = Entry(f2, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                   width=99999,
                                   fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                   textvariable=entryVar, name=self.__words[num],
                                   font=self.__miniFont, justify=CENTER,
                                   )
                if appendThem:
                    entry.pack_propagate(False)
                    entry.pack(side=TOP, anchor=N, fill=BOTH)
                    self.__focusOutItems.append(entry)

                entry.bind("<KeyRelease>", self.__focusOut)
                entry.bind("<FocusOut>", self.__focusOut)
                entry.bind("<FocusIn>", self.__focusIn)

                codeEditorItems[self.__words[num]] = [entryVar, entry]

            elif bannerItems[num][2] == Button:
                button = Button(f2,      width=9999999,
                                         command=bannerItems[num][3],
                                         state=DISABLED,
                                         font=self.__tinyFont, fg=self.__colors.getColor("font"),
                                         bg=self.__colors.getColor("window"),
                                         text=bannerItems[num][0])
                if appendThem:
                    button.pack_propagate(False)
                    button.pack(fill=X)

                codeEditorItems[self.__words[num]] = button


    def reIndent(self):
        text    = self.__codeBox.get(0.0, END).split("\n")
        newText = []
        for lineNum in range(0, len(text)):
            lineData = self.getLineStructure(lineNum, text, True)

            tempAppendor    = []
            tempDestination = {}

            self.createCodeLine(tempAppendor, tempDestination, False)
            self.createFakeCodeEditorItems(lineData, tempDestination)
            newText.append(self.__getFakeLine(tempDestination))

        self.updateText(newText)

    def updateText(self, text):
        self.__codeBox.delete(0.0, END)
        if type(text) == list:
           self.__codeBox.insert(0.0, "\n".join(text))
        else:
           self.__codeBox.insert(0.0, text)

        self.__codeBox.focus()
        self.__codeBox.mark_set(INSERT,
                                str(self.__cursorPoz[0]) + ".0"
                                )
        self.__codeBox.see(str(self.__cursorPoz[0]) + ".0")
        self.__tintingThread("whole")

    def createFakeCodeEditorItems(self, lineStructure, destination):
        for key in lineStructure:
            if key in self.__words:
               item = destination[key]

               if type(item)  == Label:
                  item.config(text = str(lineStructure[key]))

               elif type(item) == list:
                  if type(item[0]) == StringVar:
                     item[0].set(lineStructure[key][0])
                     if item[0].get() == "None": item[0].set("")

            elif key == "command":
                delimiter = "%"
                dels      = self.__config.getValueByKey('validObjDelimiters').split(" ")

                string = lineStructure["command"][0]
                if string in ("None", None): string = ""

                for d in dels:
                    if d in string:
                       delimiter = d
                       break

                commandParts = string.split(delimiter)
                destination["command#1"][0].set("")
                destination["command#2"][0].set("")
                destination["command#3"][0].set("")

                if commandParts[0] == "game": commandParts = commandParts[1:]


                for num in range(0, len(commandParts)):
                    data = commandParts[num]

                    if data not in [None, "None", ""]:
                       destination["command#" + str(num+1)][0].set(data)

    def replaceInLine(self):
        text = self.__codeBox.get(0.0, END).split("\n")
        lineNum = self.__cursorPoz[0]-1
        text[lineNum] = self.replaceStuff(text[lineNum])

        self.updateText(text)

    def replaceAll(self):
        text = self.__codeBox.get(0.0, END)
        self.updateText(self.replaceStuff(text))

    def replaceStuff(self, text):
        if self.__ignoreCase.get() == 0:
            return text.replace(
                   self.__sentryVar.get(),
                   self.__rentryVal.get()
                   )
        else:
            import re
            return re.sub(self.__sentryVar.get(),
                          self.__rentryVal.get(),
                          text, re.IGNORECASE)


    def prevFound(self):
        self.findTheOne(-1)

    def nextFound(self):
        self.findTheOne(1)

    def findTheOne(self, step):
        text = self.__codeBox.get(0.0, END).split("\n")
        startLine = self.__cursorPoz[0]-1

        if step == 1:
           thisIsTheWay = [
               [startLine, len(text)    , 1],
               [0        , startLine + 1, 1]

           ]
        else:
            thisIsTheWay = [
                [startLine  , -1           , -1],
                [len(text)-1, startLine - 1, -1]
            ]

        foundIt   = False
        foundLine = startLine

        for loopNum in range(0, 2):
            for lineNum in range(
                thisIsTheWay[loopNum][0],
                thisIsTheWay[loopNum][1],
                thisIsTheWay[loopNum][2]
                ):
                line = text[lineNum]
                if self.__highLightWord in line:
                   if loopNum == 0 and lineNum == startLine:
                      continue
                   else:
                      foundIt   = True
                      foundLine = lineNum
                      break

            if foundIt == True: break

        self.__codeBox.mark_set(INSERT, str(foundLine+1)+".0")
        self.setCurzorPoz()
        self.__codeBox.see(str(foundLine + 1) + ".0")

    def __ignoreCaseChange(self):
        self.__highLightIgnoreCase = self.__ignoreCase.get()
        self.__changeHighLightWord(None)

    def __changeHighLightWord(self, event):
        self.__highLightWord = self.__sentryVar.get().replace("\t", " ")
        self.__tintingThread("whole")

        if self.__highLightWord == "":
           status = DISABLED
        else:
           status = NORMAL

        self.__replaceButton1.config(state = status)
        self.__replaceButton2.config(state = status)

        self.__searchButton1.config(state = status)
        self.__searchButton2.config(state = status)

    def __lbFocusIn(self, widget):
        self.__lbFocused = True

    def __lbFocusOut(self, widget):
        self.__lbFocused = False


    def updateTextFromDisplay(self):
        if self.__codeEditorItems["updateRow"].cget("state") == DISABLED: return

        line = self.__getFakeLine(self.__codeEditorItems)

        currentLineNum   = self.__cursorPoz[0]
        text = self.__codeBox.get(0.0, END).split("\n")

        text[currentLineNum-1] = line

        self.__codeBox.delete(0.0, END)
        self.__codeBox.insert(0.0, "\n".join(text))

        self.__codeBox.see(str(currentLineNum) + ".0")

        selectPosizions = []
        errorPositions  = []
        objectList = self.__objectMaster.getStartingObjects()
        objectList.append("game")

        self.__codeBox.mark_set(INSERT, str(currentLineNum)+"."+ str(len(line)))
        self.__codeEditorItems["updateRow"].config(state = DISABLED)
        self.__lineTinting(line, objectList, currentLineNum-1, selectPosizions, errorPositions, "lineTinting", True, None)

        self.__codeBox.focus()

    def focusOut(self, event):
        self.__setTinting("whole")
        self.__loader.mainWindow.focusOut(event)

    def __loadFromMemory(self, bank, section):
        #if self.__loader.virtualMemory.codes[self.__currentBank][self.__currentSection].changed == True:
        #   pass

        self.__codeBox.delete(0.0, END)
        text = self.__loader.virtualMemory.codes[bank][section].code
        self.__codeBox.insert(0.0, text)
        self.__setTinting("whole")

    def __setTinting(self, mode):
        from threading import Thread

        t = Thread(target=self.__tintingThread, args=[mode])
        t.daemon = True
        t.start()

    def __tintingThread(self, mode):
        text = self.__codeBox.get(0.0, END).replace("\t", " ").split("\n")
        self.__focused2 = self.__codeBox

        if self.__lastButton == "Return":
            mode = "whole"

        #objectList, processList = self.__objectMaster.getObjectsAndProcessesValidForGlobalAndBank()
        objectList = self.__objectMaster.getStartingObjects()
        objectList.append("game")

        selectPosizions = []
        errorPositions  = []

        from copy import deepcopy

        self.__subroutines = []
        self.__constants = deepcopy(self.__loader.stringConstants)
        if self.__currentSection in self.__syntaxList["const"].sectionsAllowed:
            self.__constants = self.collectConstantsFromSections(self.__currentBank)

        if self.__currentSection in self.__syntaxList["subroutine"].sectionsAllowed:
            self.__subroutines = self.collectNamesByCommandFromSections("subroutine", None)

        if mode == "whole":
            self.__codeEditorItems["updateRow"].config(state=DISABLED)
            for num in range (1, len(text)+1):
               self.__lineTinting(text[num-1], objectList, num-1, selectPosizions, errorPositions, "lineTinting", True, None)

               for item in selectPosizions:
                   self.removeTag(item[2] + 1, item[0], item[1] + 1, "background")
                   self.addTag(item[2] + 1, item[0], item[1] + 1, "commandBack")

               for item in errorPositions:
                   #print(item, "errorPositions")
                   self.removeTag(item[2] + 1, item[0], item[1] + 1, None)
                   self.addTag(item[2] + 1, item[0], item[1] + 1, "error")

            self.__saveCode()

        else:
            self.__lineTinting(text[mode-1], objectList, mode-1, selectPosizions, errorPositions, "lineTinting", None, None)


    def __saveCode(self):
        text = self.__codeBox.get(0.0, END)
        old  = self.__virtualMemory.codes[self.__currentBank][self.__currentSection].code

        textLines = text.split("\n")
        oldLines  = old.split("\n")

        if textLines[-1] == "":
            text = "\n".join(textLines[:-1])

        if oldLines[-1]  == "":
            old  = "\n".join(oldLines[:-1])

        if text == old:
           return

        self.__virtualMemory.codes[self.__currentBank][self.__currentSection].code    = text
        self.__virtualMemory.codes[self.__currentBank][self.__currentSection].changed = True
        self.__virtualMemory.archieve()

    def callLineTintingFromFirstCompiler(self, line, lineNum, text):
        objectList = self.__objectMaster.getStartingObjects()
        objectList.append("game")

        selectPosizions = []
        errorPositions = []

        self.__lineTinting(line, objectList, lineNum, selectPosizions, errorPositions, "firstCompiler", None, text)

        return errorPositions

    def __lineTinting(self, line, objects, lineNum, selectPosizions, errorPositions, caller, whole, text):

        lineEditorTempDict = {}

        delimiterPoz = self.getFirstValidDelimiterPoz(line)
        yOnTextBox = lineNum + 1

        line = line.replace("\t", " ")
        self.__statement = None

        if caller == "lineTinting":
           self.removeTag(yOnTextBox, 0, len(line), None)

        if text == None:
           text = self.__codeBox.get(1.0, END).replace("\t", " ").split("\n")
        if type(text) == str:
           text = text.replace("\t", " ").split("\n")

        if lineNum >= len(text): return
        if line == "": line = " "

        currentLineStructure = None
        if  caller in ("lineTinting", "firstCompiler"):
            currentLineStructure = self.getLineStructure(lineNum, text, True)
        elif caller == "lineEditor":
            currentLineStructure = self.getLineStructure(0, [line], True)
            currentLineStructure["lineNum"] = lineNum

            for name in self.__words:
                if type(self.__codeEditorItems[name]) == list:
                   self.__codeEditorItems[name][1].config(
                       bg   = self.__loader.colorPalettes.getColor("boxBackNormal"),
                       fg   = self.__loader.colorPalettes.getColor("boxFontNormal"),
                       font = self.__miniFont
                   )

        if line[0] in ("*", "#"): delimiterPoz = 0
        if currentLineStructure["level"] < self.__unreachableLVL:
           self.__unreachableLVL = -1
           self.__unreachableNum = -1

        if delimiterPoz != len(line):
           if caller == "lineTinting":
              self.addTag(yOnTextBox, delimiterPoz, len(line), "comment")
           elif caller == "lineEditor":
              self.configTheItem("comment", "comment")
              lineEditorTempDict["comment"] = "command"

        hasValidCommand = False
        addError        = False
        commandParams   = []

        if currentLineStructure["command"][0] in self.__syntaxList.keys():
           if caller == "lineTinting":
              self.addTag(yOnTextBox, currentLineStructure["command"][1][0],
                                   currentLineStructure["command"][1][1]+1, "command")
           elif caller == "lineEditor":
              self.configTheItem("command#1", "command")
              lineEditorTempDict["command#1"] = "command"

           hasValidCommand = True
           commandParams   = self.__syntaxList[currentLineStructure["command"][0]].params

           if self.__syntaxList[currentLineStructure["command"][0]].endNeeded == True:
                endFound = self.findEnd(currentLineStructure, lineNum, text)
                if endFound == False:
                   addError = True
                   if caller == 'firstCompiler':
                      errorPositions.append(["command", "noEndFound"])

                else:
                    if self.__cursorPoz[0] == yOnTextBox:

                       self.addToPosizions(selectPosizions, self.convertToX1X2Y(endFound))
                       self.addToPosizions(selectPosizions,
                                                 self.convertToX1X2Y(self.getXYfromCommand(currentLineStructure)))


           elif currentLineStructure["command"][0].startswith("end-") == True:
               self.__unreachableLVL = -1
               self.__unreachableNum = -1
               startFound = self.__findStart(currentLineStructure, lineNum, text)
               if startFound == False:
                  addError = True
                  if caller == 'firstCompiler':
                      errorPositions.append(["command", "noStartFound"])
               else:
                   if self.__cursorPoz[0] == yOnTextBox:

                      self.addToPosizions(selectPosizions, self.convertToX1X2Y(startFound))
                      self.addToPosizions(selectPosizions,
                                                self.convertToX1X2Y(self.getXYfromCommand(currentLineStructure)))


           elif currentLineStructure["command"][0] == "case" or currentLineStructure["command"][0] in\
                self.__syntaxList["case"].alias:

                foundAllRelatedForCaseDefault = self.foundAllRelatedForCaseDefault(currentLineStructure, lineNum, text, False)
                if foundAllRelatedForCaseDefault["select"] == False or foundAllRelatedForCaseDefault["end-select"] == False:
                   addError = True
                   if caller == 'firstCompiler':
                      if foundAllRelatedForCaseDefault["select"] == False:
                         errorPositions.append(["command", "noSelectForCase"])

                      if foundAllRelatedForCaseDefault["end-select"] == False:
                         errorPositions.append(["command", "noEndForCase"])

                #print(foundAllRelatedForCaseDefault)
                if addError == False and self.__cursorPoz[0] == yOnTextBox:

                   self.addToPosizions(selectPosizions, self.convertToX1X2Y(foundAllRelatedForCaseDefault["select"]))
                   self.addToPosizions(selectPosizions, self.convertToX1X2Y(foundAllRelatedForCaseDefault["end-select"]))

                   for item in foundAllRelatedForCaseDefault["cases"]:
                       self.addToPosizions(selectPosizions, self.convertToX1X2Y(self.getXYfromCommand(item)))

                   for item in foundAllRelatedForCaseDefault["defaults"]:
                       self.addToPosizions(selectPosizions, self.convertToX1X2Y(self.getXYfromCommand(item)))

           elif currentLineStructure["command"][0] == "default" or currentLineStructure["command"][0] in \
                   self.__syntaxList["default"].alias:

               foundAllRelatedForCaseDefault = self.foundAllRelatedForCaseDefault(currentLineStructure, lineNum, text,
                                                                                    False)

               if foundAllRelatedForCaseDefault["select"] == False or foundAllRelatedForCaseDefault[
                   "end-select"] == False or foundAllRelatedForCaseDefault["numOfDefaults"] > 1 or \
                       foundAllRelatedForCaseDefault["numOfCases"] == 0:
                       addError = True
                       if caller == 'firstCompiler':
                          if foundAllRelatedForCaseDefault["select"] == False:
                             errorPositions.append(["command", "noSelectForDefault"])

                          if foundAllRelatedForCaseDefault["end-select"] == False:
                             errorPositions.append(["command", "noEndForDefault"])

                          if foundAllRelatedForCaseDefault["end-select"] == False:
                             errorPositions.append(["command", "noCaseForDefault"])

               if addError == False and self.__cursorPoz[0] == yOnTextBox:

                   self.addToPosizions(selectPosizions,
                                             self.convertToX1X2Y(foundAllRelatedForCaseDefault["select"]))
                   self.addToPosizions(selectPosizions,
                                             self.convertToX1X2Y(foundAllRelatedForCaseDefault["end-select"]))

                   for item in foundAllRelatedForCaseDefault["cases"]:
                       self.addToPosizions(selectPosizions, self.convertToX1X2Y(self.getXYfromCommand(item)))

                   for item in foundAllRelatedForCaseDefault["defaults"]:
                       self.addToPosizions(selectPosizions, self.convertToX1X2Y(self.getXYfromCommand(item)))

           elif currentLineStructure["command"][0] in ["cycle", "exit"] or \
                currentLineStructure["command"][0] in self.__syntaxList["cycle"].alias or \
                currentLineStructure["command"][0] in self.__syntaxList["exit"].alias:

                foundAllRelatedForDoAndEndDo = self.__foundAllRelatedForDoAndEndDo(currentLineStructure, lineNum, text, "do")

                if foundAllRelatedForDoAndEndDo["start"] == False or foundAllRelatedForDoAndEndDo["end"] == False:
                   addError = True
                   if caller == 'firstCompiler':
                       if foundAllRelatedForDoAndEndDo["start"] == False:
                          errorPositions.append(["command", "noDoForCommand"])

                       if foundAllRelatedForDoAndEndDo["end"] == False:
                          errorPositions.append(["command", "noEndForDo"])


                if addError == False and self.__cursorPoz[0] == yOnTextBox:
                    self.addToPosizions(selectPosizions,
                                              self.convertToX1X2Y(foundAllRelatedForDoAndEndDo["start"]))
                    self.addToPosizions(selectPosizions,
                                              self.convertToX1X2Y(foundAllRelatedForDoAndEndDo["end"]))
                    self.addToPosizions(selectPosizions,
                                              self.convertToX1X2Y(self.getXYfromCommand(currentLineStructure)))

           if currentLineStructure["command"][0] == "do" or\
              currentLineStructure["command"][0] in self.__syntaxList["do"].alias:
              firstPoz = lineNum
              lastPoz = self.findEnd(currentLineStructure, lineNum, text)

              if lastPoz != False:
                 lastPoz = lastPoz[0]

                 if self.infiniteLoop(text, firstPoz, lastPoz):
                     if caller == 'firstCompiler':
                        errorPositions.append(["command", "infiniteLoop"])
                     else:
                        self.addToPosizions(errorPositions,
                                            self.convertToX1X2Y(self.getXYfromCommand(currentLineStructure)))

           elif currentLineStructure["command"][0] == "do-items" or\
              currentLineStructure["command"][0] in self.__syntaxList["do-items"].alias:

              firstPoz  = []
              lastPoz   = []

              if currentLineStructure["level"] == 0:
                 firstPoz = lineNum
                 lastPoz  = self.findEnd(currentLineStructure, lineNum, text)

              else:
                 from copy import deepcopy

                 copied = deepcopy(currentLineStructure)
                 copied["level"] = 0

                 xyz = self.__foundAllRelatedForDoAndEndDo(copied, lineNum, text, "do-items")

                 firstPoz = xyz["start"]
                 lastPoz  = xyz["end"]

              if firstPoz != False and type(firstPoz) != int: firstPoz = firstPoz[0]
              if lastPoz  != False:                           lastPoz  = lastPoz[0]

              listOfDoItems = self.listAllCommandFromTo("do-items", text, None, firstPoz, lastPoz + 1)
              if len(listOfDoItems) > 1:
                 for item in listOfDoItems:
                     if caller != 'firstCompiler':
                         self.addToPosizions(errorPositions,
                                             self.convertToX1X2Y(self.getXYfromCommand(item)))
                     else:
                         errorPositions.append(["command", "iteralError"])

           #print(errorPositions, addError)

           if  ((currentLineStructure["("] == -1 or currentLineStructure[")"] == -1) and
                self.__syntaxList[currentLineStructure["command"][0]].bracketNeeded == True or
               (currentLineStructure["("] != -1 or currentLineStructure[")"] != -1) and
               self.__syntaxList[currentLineStructure["command"][0]].bracketNeeded == False):
                    addError = True
                    #print("#1")
                    if caller == 'firstCompiler':
                       if self.__syntaxList[currentLineStructure["command"][0]].bracketNeeded == True:
                          if currentLineStructure["("] == -1:
                             errorPositions.append(["bracket", "missingOpeningBracket"])
                          if currentLineStructure[")"] == -1:
                             errorPositions.append(["bracket", "missingClosingBracket"])
                       else:
                           errorPositions.append(["bracket", "commandDoesNotNeedBrackets"])

           if self.__currentSection not in self.__syntaxList[currentLineStructure["command"][0]].sectionsAllowed\
           or (currentLineStructure["level"] != self.__syntaxList[currentLineStructure["command"][0]].levelAllowed
           and self.__syntaxList[currentLineStructure["command"][0]].levelAllowed != None
           ):
              addError = True
              #print("#2")
              if self.__currentSection not in self.__syntaxList[currentLineStructure["command"][0]].sectionsAllowed:
                 errorPositions.append(["command", "sectionNotAllowed"])
              if currentLineStructure["level"] != self.__syntaxList[currentLineStructure["command"][0]].levelAllowed\
              and self.__syntaxList[currentLineStructure["command"][0]].levelAllowed != None:
                  errorPositions.append(["command", "levelNotAllowed"])

           if addError == True:
               if caller == "lineTinting":
                  self.removeTag(yOnTextBox, currentLineStructure["command"][1][0],
                              currentLineStructure["command"][1][1] + 1, None)
                  self.addTag(yOnTextBox, currentLineStructure["command"][1][0],
                           currentLineStructure["command"][1][1] + 1, "error")
               elif caller == "lineEditor":
                   self.configTheItem("command#1", "error")
                   lineEditorTempDict["comment#1"] = "error"

        elif currentLineStructure["command"][0] not in (None, "None", ""):
           foundObjects = self.findObjects(currentLineStructure["command"], objects)

           if caller == "lineTinting":
              self.addTag(yOnTextBox, currentLineStructure["command"][1][0],
                        currentLineStructure["command"][1][1] + 1, "error")
           elif caller == "lineEditor":
               self.configTheItem("command#1", "error")
               lineEditorTempDict["comment#1"] = "error"

           asList = list(foundObjects.keys())
           for keyNum in range(0, len(asList)):
              key = asList[keyNum]

              adder = 1
              if key == asList[-1]: adder = 0

              if caller == "lineTinting":
                 self.removeTag(yOnTextBox, foundObjects[key][0][0],
                          foundObjects[key][0][1] + 1 + adder,
                          None)

                 self.addTag(yOnTextBox, foundObjects[key][0][0],
                          foundObjects[key][0][1] + 1,
                          foundObjects[key][1])

              elif caller == "lineEditor":
                  self.configTheItem("command#"+str(keyNum+1), foundObjects[key][1])
                  lineEditorTempDict["command#"+str(keyNum+1)] = foundObjects[key][1]


              if foundObjects[key][1] == "process":
                 hasValidCommand = True

                 validOnes = ["variable", "string", "stringConst", "number"]

                 params          = self.__objectMaster.returnParamsForProcess(currentLineStructure["command"][0])
                 for p in params:
                     if p in validOnes:
                        commandParams.append(p)
                     else:
                        commandParams.append("variable")


        if   currentLineStructure["("] != -1 and currentLineStructure[")"] == -1:
             if caller == "lineTinting":
                self.addTag(yOnTextBox, currentLineStructure["("],
                                     currentLineStructure["("] + 1,
                                     "error")
             elif caller == "firstCompiler":
                errorPositions.append(["bracket", "missingClosingBracket"])

        elif currentLineStructure["("] == -1 and currentLineStructure[")"] != -1:
             if caller == "lineTinting":
                self.addTag(yOnTextBox, currentLineStructure[")"],
                                     currentLineStructure[")"] + 1,
                                     "error")
             elif caller == "firstCompiler":
                errorPositions.append(["bracket", "missingOpeningBracket"])

        elif currentLineStructure["("] != -1 and currentLineStructure[")"] != -1:
            if caller == "lineTinting":
               self.addTag(yOnTextBox, currentLineStructure[")"],
                        currentLineStructure[")"] + 1,
                        "bracket")

               self.addTag(yOnTextBox, currentLineStructure["("],
                        currentLineStructure["("] + 1,
                        "bracket")

        #print(errorPositions, addError)

        if (currentLineStructure["("] != -1 or caller == "lineEditor") and\
            currentLineStructure["param#1"] not in [None, "None", ""]\
            and hasValidCommand == True:
            paramColoring = self.checkParams(currentLineStructure["param#1"],
                                             currentLineStructure["param#2"],
                                             currentLineStructure["param#3"],
                                             currentLineStructure,
                                             currentLineStructure["command"][0], text)

            paramNum = 0
            for item in paramColoring:
                if item[1][0] != -1:
                   if caller == "lineTinting":
                      self.removeTag(yOnTextBox, item[1][0],
                                              item[1][1] + 1,
                                              None)
                      self.addTag(   yOnTextBox, item[1][0],
                                              item[1][1] + 1,
                                              item[0])
                   elif caller == "lineEditor":
                      paramNum += 1

                      isThatStatement, paramN = self.isThatADamnStatement(currentLineStructure, item[1])
                      if isThatStatement == True:
                         paramNum = paramN
                         item[0] = "bracket"

                         for itemS in self.__statement:
                             if itemS["type"] == "error":
                                item[0] = "error"
                                break


                      self.configTheItem("param#" + str(paramNum), item[0])
                      lineEditorTempDict["param#" + str(paramNum)] = item[0]

        if currentLineStructure["command"][0] == "do-frames" or currentLineStructure["command"][0] in\
           self.__syntaxList["do-frames"].alias:
           num1 = None
           num2 = None

           try:
               try:
                   num1 = self.convertStringNumToNumber(currentLineStructure["param#1"][0])
               except:
                   num1 = self.convertStringNumToNumber(self.__constants[currentLineStructure["param#1"][0]])

               if currentLineStructure["param#2"][0] not in [None, "None", ""]:
                  try:
                      num2 = self.convertStringNumToNumber(currentLineStructure["param#2"][0])
                  except:
                      num2 = self.convertStringNumToNumber(self.__constants[currentLineStructure["param#2"][0]])

           except:
                pass

           if num1 != None:
               if (num1 != 1 and self.isPowerOfTwo(num1)) or num1 < 1 == False:
                    if caller == "lineTinting":
                        self.addTag(yOnTextBox, currentLineStructure["param#1"][1][0],
                                   currentLineStructure["param#1"][1][1]+1,
                                   "error")
                    elif caller == "firstCompiler":
                        errorPositions.append(["param#1", "mustBePowerOf2"])

           if num2 != None:
               if num1 < num2 or num2 < 1:
                   if caller == "lineTinting":
                      self.addTag(yOnTextBox, currentLineStructure["param#2"][1][0],
                                  currentLineStructure["param#2"][1][1]+1,
                                 "error")
                   elif caller == "firstCompiler":
                      errorPositions.append(["param#2", "mustBeSmaller"])


        for ind in range(0, len(currentLineStructure["commas"])):
            if ind > len(commandParams) - 2:
               if caller == "lineTinting":
                  self.addTag(yOnTextBox, currentLineStructure["commas"][ind],
                                       currentLineStructure["commas"][ind] + 1,
                                       "error")
               elif caller == "firstCompiler":
                  errorPositions.append(["param#" + str(ind+1), "paramNotNeeded"])

        if currentLineStructure["level"] >= self.__unreachableLVL and self.__unreachableLVL != -1 \
           and currentLineStructure["lineNum"] > self.__unreachableNum:

           if currentLineStructure["command"][0] not in [None, "None", ""]:
               self.removeTag(yOnTextBox, 0, len(line), "background")
               self.addTag(yOnTextBox,    0, len(line), "unreachable")

        if self.__highLightWord not in ("", None):
            if len(line) >= len(self.__highLightWord):
                for startNum in range(0, len(line) - len(self.__highLightWord), 1):
                    thisWord = line[startNum:startNum + len(self.__highLightWord)]
                    thatWord = self.__highLightWord

                    if self.__highLightIgnoreCase == True:
                       thisWord = thisWord.upper()
                       thatWord = thatWord.upper()

                    if thisWord == thatWord:
                       self.removeTag(yOnTextBox, startNum, startNum  + len(self.__highLightWord), "background")
                       self.addTag(yOnTextBox, startNum, startNum + len(self.__highLightWord), "highLight")

        for exitCommand in self.exiters:
            foundExit = False
            if currentLineStructure["command"][0] in [None, "None", ""]: break
            if exitCommand == currentLineStructure["command"][0]: foundExit = True
            if foundExit == False:
               if currentLineStructure["command"][0] in self.__syntaxList[exitCommand].alias:
                  foundExit = True

            if foundExit:
               self.__unreachableLVL = currentLineStructure["level"]
               self.__unreachableNum = currentLineStructure["lineNum"]
               currentLineStructure["unreachable"] = True

        if (yOnTextBox == self.__cursorPoz[0]) and caller == "lineTinting":
           currentWord = self.getCurrentWord(text[lineNum])
           self.updateLineDisplay(currentLineStructure)
           self.__updateListBoxFromCodeEditor(currentWord, currentLineStructure, commandParams, line, text)
        elif caller == "lineEditor":

            for word in ["command", "param"]:
                for num in range(1, 4):
                    key = word + "#" + str(num)
                    if key not in lineEditorTempDict and self.__codeEditorItems[key][0].get() != "":
                       lineEditorTempDict[key] = "error"

            if "command#1" in lineEditorTempDict.keys():
                if lineEditorTempDict["command#1"] in ["command", "error"]:
                   for secondNum in range(2, 4):
                       secondWord = "command#" + str(secondNum)
                       if secondWord in lineEditorTempDict:
                           if lineEditorTempDict[secondWord] != "":
                              self.configTheItem(secondWord, "error")
                              lineEditorTempDict[secondWord] = "error"

                elif lineEditorTempDict["command#1"] == "object":
                     if "command#2" not in lineEditorTempDict.keys():
                         self.configTheItem("command#2", "error")
                         lineEditorTempDict["command#2"] = "error"


                     elif lineEditorTempDict["command#2"] not in ("object", "process"):
                         self.configTheItem("command#2", "error")
                         lineEditorTempDict["command#2"] = "error"


                     if lineEditorTempDict["command#2"] == "object":
                         if "command#3" not in lineEditorTempDict.keys():
                           self.configTheItem("command#3", "error")
                           lineEditorTempDict["command#3"] = "error"

                if "command#2" in lineEditorTempDict and\
                   "command#3" in lineEditorTempDict:
                    if lineEditorTempDict["command#2"] == "process" and \
                       lineEditorTempDict["command#3"] != "":
                       self.configTheItem("command#3", "error")
                       lineEditorTempDict["command#3"] = "error"
                    elif lineEditorTempDict["command#3"] != "process":
                       self.configTheItem("command#3", "error")
                       lineEditorTempDict["command#3"] = "error"

            if "param#1" not in lineEditorTempDict.keys():
               if "param#2" in lineEditorTempDict.keys():
                   self.configTheItem("command#2", "error")
                   lineEditorTempDict["command#2"] = "error"

               if "param#3" in lineEditorTempDict.keys():
                   self.configTheItem("command#3", "error")
                   lineEditorTempDict["command#3"] = "error"

            elif "param#2" not in lineEditorTempDict.keys():
                if "param#3" in lineEditorTempDict.keys():
                    self.configTheItem("command#3", "error")
                    lineEditorTempDict["command#3"] = "error"

            self.updateListBoxFromLineEditor(currentLineStructure, commandParams, lineEditorTempDict, text)

    def infiniteLoop(self, text, firstPoz, lastPoz):

        for word in self.exiters:
            collected = self.listAllCommandFromTo(word, text, None, firstPoz, lastPoz + 1)
            if collected != []: return False

        return True

    def isThatADamnStatement(self, currentLineStructure, dimensions):
        for item in currentLineStructure.keys():
            if item.startswith("param#"):
               S1 = currentLineStructure[item][1][0]
               S2 = dimensions[0]
               E1 = currentLineStructure[item][1][1]
               E2 = dimensions[1]

               statementTyp = "comprass"

               if S2 >= S1 and E2 <= E1:
                   command = None
                   for c in self.__loader.syntaxList.keys():
                       if currentLineStructure["command"][0] == c or currentLineStructure["command"][0] in self.__syntaxList[c].alias:
                          command = self.__loader.syntaxList[c]

                          if c == "calc": statementTyp = "calc"
                          break

                   if "%write" in currentLineStructure["command"][0]:
                       statementTyp = "write"

                   needComprassion = True
                   stringAllowed = False

                   if statementTyp == "calc":
                       needComprassion = False
                   elif statementTyp == "write":
                       needComprassion = False
                       stringAllowed = True

                   paramNum      = int(item.split("#")[1]) - 1
                   if len(command.params) == 0 or paramNum > len(command.params): return False, ""

                   try:
                      selectedParam = command.params[paramNum]
                   except:
                      return False, ""

                   if "statement" in selectedParam:
                      statement = currentLineStructure[item][0]
                      self.__statement = self.getStatementStructure(statement, needComprassion, stringAllowed, 0, currentLineStructure)

                      return True, int(item.split("#")[1])

        return False, ""

    def updateListBoxFromLineEditor(self, currentLineStructure, commandParams, lineEditorTempDict, text):
        wordList = []

        currentWord = ""
        selectedType = ""
        for key in self.__codeEditorItems.keys():
            if type(self.__codeEditorItems[key]) == list:
                if self.__focused == self.__codeEditorItems[key][1]:
                    currentWord = self.__codeEditorItems[key][0].get()
                    selectedType = key
                    break

        if selectedType not in ("comment", ""):
           #print(selectedType)
           entryType = selectedType.split("#")[0]
           entryNum  = int(selectedType.split("#")[1])

           listOfItems = []

           if entryType == "command":
              if entryNum == 1:
                 if ("command#2" not in lineEditorTempDict) and ("command#3") not in lineEditorTempDict:

                     for command in self.__syntaxList.keys():
                         if command.startswith(currentWord):
                            if self.__currentSection in self.__syntaxList[command].sectionsAllowed:
                                listOfItems.append([command, "command"])

                     objList = self.__objectMaster.getStartingObjects()
                     for obj in objList:
                         if obj.startswith(currentWord):
                            listOfItems.append([obj, "object"])

                     listOfItems.sort()
                     for item in listOfItems:
                         if    "command#1" not in lineEditorTempDict.keys():
                               wordList.append(item)
                         elif  item[0].startswith(lineEditorTempDict["command#1"] or item[0] == ""):
                               wordList.append(item)


              if listOfItems == []:
                  listOfItems = self.__objectMaster.returnObjListLike(
                     self.__codeEditorItems["command#1"][0].get(),
                     self.__codeEditorItems["command#2"][0].get(),
                     self.__codeEditorItems["command#3"][0].get(), entryNum
                  )

           elif entryType == "param":
               mustHave = True
               try:
                   listType = commandParams[entryNum - 1]
               except:
                   listType = None
                   mustHave = False

               if listType != None:
                  if listType.startswith("{"):
                     listType = listType[1:-1]
                     mustHave  = False

                  commandString = ""
                  for num in range(1,4):
                      key = "command#" + str(num)
                      if key in lineEditorTempDict.keys():
                         if num > 1: commandString += "%"
                         commandString += self.__codeEditorItems[key][0].get()

                  dummy, ioMethod = self.returnParamsOfObjects(commandString)

                  foundIt, paramTypeAndDimension = self.checkIfParamIsOK(listType, currentWord,
                                                                            ioMethod, None,
                                                                            "dummy", mustHave, selectedType, currentLineStructure, text)
                  if foundIt == True:
                     listType = paramTypeAndDimension[0]
                  else:
                     listType = listType.split("|")

               if type(listType) == list:
                   listOfItems = []
                   for typ in listType:
                       tempList = self.setupList(currentWord, typ, currentLineStructure, selectedType, text)
                       for word in tempList:
                           listOfItems.append(word)

               else:
                   listOfItems = self.setupList(currentWord, listType, currentLineStructure, selectedType, text)


           listOfItems.sort()
           self.fillListBox(listOfItems)

    def reAlignCommandsAndParams(self):
        noneList = ("", None, "None")

        if self.__codeEditorItems["command#1"][0].get() == "game":
           self.__codeEditorItems["command#1"][0].set("")

        for word in ("command", "param"):
            for startNum in range(1,3):
                name1 = word  + "#" + str(startNum)
                name2 = word  + "#" + str(startNum + 1)

                if self.__codeEditorItems[name1][0].get() in noneList and \
                   self.__codeEditorItems[name2][0].get() not in noneList:
                   self.__codeEditorItems[name1][0].set(self.__codeEditorItems[name2][0].get())
                   self.__codeEditorItems[name2][0].set("")

    def returnCurrentBankSection(self):
        return self.__currentBank, self.__currentSection

    def configTheItem(self, name, tagName):
        #print(name, tagName)

        if "background" in self.__tagSettings[tagName]:
            self.__codeEditorItems[name][1].config(
                 background = self.__tagSettings[tagName]["background"])
        else:
            self.__codeEditorItems[name][1].config(
                 background = self.__loader.colorPalettes.getColor("boxBackNormal"))

        if "foreground" in self.__tagSettings[tagName]:
            self.__codeEditorItems[name][1].config(
                foreground = self.__tagSettings[tagName]["foreground"])
        else:
            self.__codeEditorItems[name][1].config(
                foreground = self.__loader.colorPalettes.getColor("boxFontNormal"))

    def __updateListBoxFromCodeEditor(self, currentWord, lineStructure, paramTypes, line, text):
        from copy import deepcopy

        cursorIn     = None
        wordsForList = []
        noneList     = ["", None, "None"]

        for key in lineStructure:
            if key.startswith("param") or key == "command":
               if lineStructure[key][1][0] != -1 and lineStructure[key][1][1] >= lineStructure[key][1][0]:
                  if self.__cursorPoz[1] >= lineStructure[key][1][0] and  self.__cursorPoz[1] <= lineStructure[key][1][1]+1:
                     cursorIn = key

        if cursorIn == None:
            if lineStructure["("] == -1:
                cursorIn = "command"

            elif self.__cursorPoz[1] <= lineStructure["("]:
                cursorIn = "command"

            elif self.__cursorPoz[1] > lineStructure[")"] and lineStructure[")"] != -1:
                cursorIn = "overIt"
            else:
                param = 1
                for commaNum in range(0, len(lineStructure["commas"])):
                    if self.__cursorPoz[1] > lineStructure["commas"][commaNum]:
                        param += 1
                    else:
                        break
                cursorIn = "param#" + str(param)

        if self.getFirstValidDelimiterPoz(line) != len(line):
           if self.__cursorPoz[1] >= self.getFirstValidDelimiterPoz(line) + 1: cursorIn = "overIt"

        if len(currentWord) > 0:
            if currentWord[-1] in ["(", ")", ","]:
               currentWord = ""

        listType = cursorIn

        if  cursorIn == "overIt":
            listType  = None

        elif (currentWord in noneList and lineStructure[cursorIn] not in noneList) or \
              currentWord == lineStructure[cursorIn][0]:

        #elif currentWord == lineStructure[cursorIn][0]:
           if cursorIn == "command" and len(currentWord) > 0:
               if currentWord[-1] in self.__config.getValueByKey("validObjDelimiters").split(" "):
                  listType = "nextObject"

           elif cursorIn.startswith("param#"):
               paramNum = int(cursorIn[-1]) - 1

               params, ioMethod = self.returnParamsOfObjects(lineStructure["command"][0])
               if paramNum > len(params) - 1:
                  listType = None
               else:

                  paramType = params[paramNum]
                  dimension = lineStructure[cursorIn][1]

                  mustHave = True
                  if paramType[0] == "{":
                      paramType = paramType[1:-1]
                      mustHave = False

                  foundIt, paramTypeAndDimension = self.checkIfParamIsOK(paramType, lineStructure[cursorIn][0],
                                                                            ioMethod, None,
                                                                            dimension, mustHave, cursorIn, lineStructure, text)
                  if foundIt == True:
                     listType = paramTypeAndDimension[0]
                  else:
                     listType = paramType.split("|")

        if type(listType) == list:
            wordsForList = []
            for typ in listType:
                tempList = self.setupList(currentWord, typ, lineStructure, cursorIn, text)
                for word in tempList:
                    wordsForList.append(word)
        else:
            wordsForList = self.setupList(currentWord, listType, lineStructure, cursorIn, text)

        self.fillListBox(wordsForList)

    def fillListBox(self, wordsForList):

        selection = 0
        selected  = ""
        try:
            selection = self.__listBoxOnTheRight.curselection()[0]
            selected  = self.__listOfItems[selection]
        except:
            pass

        self.__listOfItems = []
        self.__listBoxOnTheRight.select_clear(0, END)
        self.__listBoxOnTheRight.delete(0, END)

        for item in wordsForList:
            #endIndex = self.__listBoxOnTheRight.index(END)

            if item[0] in self.__listOfItems: continue

            self.__listBoxOnTheRight.insert(END, item[0])
            self.__listOfItems.append(item[0])

            try:
                fg = self.__tagSettings[item[1]]["foreground"]
            except:
                fg = self.__colors.getColor("boxFontNormal")

            try:
                bg = self.__tagSettings[item[1]]["background"]
            except:
                bg = self.__colors.getColor("boxBackNormal")

            listBoxItems = list(self.__listBoxOnTheRight.get(0, END))

            try:
                self.__listBoxOnTheRight.itemconfig(len(listBoxItems)-1, fg = fg, bg = bg)
            except:
                pass

            if selected in self.__listOfItems:
               selection = self.__listOfItems.index(selected)

        self.__listBoxOnTheRight.select_set(selection)

        if self.__lbFocused:
           self.__listBoxOnTheRight.focus()

        # print(currentWord, listType, wordsForList)

    def setupList(self, currentWord, listType, lineStructure, cursorIn, text):
        wordsForList = []

        noneList = ["", None, "None"]

        command = None
        for c in self.__loader.syntaxList.keys():
            if lineStructure["command"][0] == c or lineStructure["command"][0] in self.__syntaxList[c].alias:
               command = self.__loader.syntaxList[c]
               break

        varOnly = False

        if command not in noneList:
            if command.flexSave == True:
               maxParamNum = len(command.params)

               if lineStructure["param#" + str(maxParamNum - 1)][0] in noneList or lineStructure[
                  "param#" + str(maxParamNum - 1)][0] == "missing":
                   if cursorIn == "param#1": varOnly = True

        if   listType == None:
            wordsForList = []
        elif listType == "nextObject":
            objList = self.__objectMaster.returnNextLevel(currentWord[:-1])
            if objList == False: objList = []

            for word in objList:
                wordsForList.append([word, self.__objectMaster.returnObjectOrProcess(word)])
                if wordsForList[-1][1] == "process": wordsForList[-1][1] = "command"

        elif listType == "command":
            dels = self.__config.getValueByKey("validObjDelimiters").split(" ")
            isItObj = False

            delimiter = None

            for d in dels:
                if d in currentWord:
                   isItObj   = True
                   delimiter = d
                   break

            if isItObj == False:
                for key in self.__syntaxList.keys():
                    if key.startswith(currentWord) or currentWord == None:

                       if self.__currentSection in self.__syntaxList[key].sectionsAllowed:
                          wordsForList.append([key, "command"])

                starters = self.__objectMaster.getStartingObjects()
                starters.append("game")
                for obj in starters:
                    if obj.startswith(currentWord) or currentWord == None:
                        wordsForList.append([obj, "object"])
            else:
                line     = delimiter.join(currentWord.split(delimiter)[:-1])
                lastPart = currentWord.split(delimiter)[-1]

                objList = self.__objectMaster.returnNextLevel(line)
                if objList == False: objList = []

                for word in objList:
                    if word.startswith(lastPart) or lastPart == "":
                       wordsForList.append([word, self.__objectMaster.returnObjectOrProcess(word)])
                       if wordsForList[-1][1] == "process": wordsForList[-1][1] = "command"

        elif listType == "variable":
            writable, readOnly, all, nonSystem = self.__virtualMemory.returnVariablesForBank(self.__currentBank)

            if varOnly == True:
               varList = writable
            else:
                if self.doesItWriteInParam(lineStructure, cursorIn, "editor"):
                   varList = writable
                else:
                   varList = all

            for word in varList:
                if word.startswith(currentWord) or currentWord == "":
                   wordsForList.append([word, "variable"])

        elif listType == "array":
            all, writable, readonly = self.__virtualMemory.returnArraysOnValidity(self.__currentBank)

            endFound = self.findWahWah("end-do", lineStructure["lineNum"],
                                         "downAll", text, lineStructure["level"], None, None, None,
                                         lineStructure)

            if endFound == False:
               last      = len(text)
            else:
               last      = endFound[0] + 1

            allCommands = self.listAllCommandFromTo(None, text, None, lineStructure["lineNum"], last)

            willItWrite = False
            for command in allCommands:
                params = [command["param#1"][0], command["param#2"][0],command["param#3"][0]]

                if "item" in params:
                    paramNum = "param#" + str(params.index("item"))
                    if self.doesItWriteInParam(command, paramNum, "editor") == True:
                       willItWrite = True
                       break

            if willItWrite == True:
               arrayList    = writable
            else:
               arrayList    = all

            for array in arrayList:
                if array.startswith(currentWord) or currentWord == "":
                   wordsForList.append([array, "array"])

        elif listType == "stringConst" and varOnly == False:
             constantList = self.collectConstantsFromSections(self.__currentBank)
             for word in constantList:
                 if word.startswith(currentWord) or currentWord == "":
                     wordsForList.append([word, "stringConst"])

        elif listType == "subroutine":
            wordsForList = self.collectNamesByCommandFromSections("subroutine", None)

        # Maybe "statement" will be important here to??

        wordsForList.sort()
        return(wordsForList)

    def collectConstantsFromSections(self, bank):
        from copy import deepcopy

        constants = {}
        constants['"True"']  = self.__loader.stringConstants['"True"']
        constants['"False"'] = self.__loader.stringConstants['"False"']

        for section in self.__syntaxList["const"].sectionsAllowed:
            code = self.__virtualMemory.codes[bank][section].code.replace("\r", "").replace("\t", "").split("\n")

            for lineNum in range(0, len(code)):
                lineStructure = self.getLineStructure(lineNum, code, False)
                if lineStructure["command"][0] == "const" or lineStructure["command"][0] in self.__syntaxList["const"].alias:
                   param1 = lineStructure["param#1"]
                   param2 = lineStructure["param#2"]

                   constants[param1[0]] = {
                       "alias": [param1[0].upper(), param1[0].lower()],
                       "value": param2[0]
                   }

        return constants

    def collectNamesByCommandFromSections(self, word, bank):
        subroutines = []
        if bank == None:
           bank = self.__currentBank

        for section in self.__syntaxList["subroutine"].sectionsAllowed:
            code = self.__virtualMemory.codes[bank][section].code.replace("\r", "").replace("\t", "").split("\n")

            for lineNum in range(0, len(code)):
                lineStructure = self.getLineStructure(lineNum, code, False)
                if lineStructure["command"][0] == word or lineStructure["command"][0] in self.__syntaxList[word].alias:
                   subroutines.append(lineStructure["param#1"])

        return subroutines

    def doesItWriteInParam(self, linstructure, cursorIn, caller):
        dels = self.__config.getValueByKey("validObjDelimiters").split(" ")

        for d in dels:
            if d in linstructure["command"][0]: return False

        params = self.__syntaxList[linstructure["command"][0]].params
        paramNum = int(cursorIn.split("#")[1]) - 1
        canBeThese = []

        try:
            canBeThese = params[paramNum].split("|")

        except Exception as e:
            #print(str(e))
            # print("error:", params, paramNum )
            return(False)

        #if caller == "compiler":
        #   print(cursorIn, linstructure)
        if self.__syntaxList[linstructure["command"][0]].flexSave == True:
            if cursorIn == "param#1" and\
               linstructure["param#" + str(len(self.__syntaxList[linstructure["command"][0]].params))][0] in ["", "None", None]:
               return True
            elif cursorIn == "param#" + str(len(self.__syntaxList[linstructure["command"][0]].params)) and \
                linstructure["param#" + str(len(self.__syntaxList[linstructure["command"][0]].params))][0] not in ["",
                                                                                                                   "None",
                                                                                                                   None]:
                return True

        #if cursorIn == "param#1" or cursorIn == "param#3": print(cursorIn)
        if len(canBeThese) > 0: return False

        if self.__syntaxList[linstructure["command"][0]].does == "write":
           return True
        else:
           return False

    def getXYfromCommand(self, command):
        return [command["lineNum"], command["command"][1]]

    def convertToX1X2Y(self, params):
        return [params[1][0], params[1][1], params[0]]

    def addToPosizions(self, posizions, data):
        if data not in posizions:
           posizions.append(data)

    def __foundAllRelatedForDoAndEndDo(self, currentLineStructure, lineNum, text, word):
        sendBack = {
            "start": False,
            "end"  : False
        }

        starters = [word]
        starters.extend(self.__syntaxList[word].alias)

        ender = None

        for word in starters:
            sendBack["start"] = self.findWahWah(word, lineNum,
                                                   "up", text, currentLineStructure["level"], "-", 0, None,
                                                   currentLineStructure)

            if sendBack["start"] != False:
                ender = "end-"+word.split("-")[0]
                break

        if ender != None:
            sendBack["end"] = self.findWahWah(ender, lineNum,
                                                   "down", text, currentLineStructure["level"], None, None, None,
                                                   currentLineStructure)

        return sendBack


    def foundAllRelatedForCaseDefault(self, currentLineStructure, lineNum, text, isDefault):
        sendBack = {
            "select"         : False,
            "end-select"     : False,
            "numOfDefaults"  : 0,
            "numOfCases"     : 0,
            "defaults"        : [],
            "cases"          : []
        }

        sendBack["select"] = self.findWahWah("select", lineNum,
                             "up", text, currentLineStructure["level"], "-", 0, None, currentLineStructure)

        if sendBack["select"] != False:
           sendBack["end-select"] = self.findWahWah("end-select", lineNum,
                               "down", text, currentLineStructure["level"], None, None, None, currentLineStructure)

        if sendBack["end-select"] != False:
           sendBack["cases"] = self.listAllCommandFromTo("case", text, currentLineStructure["level"],
                              sendBack["select"][0], sendBack["end-select"][0] + 1
                                                          )
           sendBack["defaults"] = self.listAllCommandFromTo("default", text, currentLineStructure["level"],
                              sendBack["select"][0], sendBack["end-select"][0] + 1
                                                          )
           sendBack["numOfCases"] = len(sendBack["cases"])
           sendBack["numOfDefaults"] = len(sendBack["defaults"])

        return sendBack

    def listAllCommandFromTo(self, searchWord, text, level, fromY, toY):
        sendBack = []

        if searchWord != None:
            commandList = [searchWord]
            commandList.extend(self.__syntaxList[searchWord].alias)
        else:
            commandList = []

        for lineNum in range(fromY, toY):
            lineStruct = self.getLineStructure(lineNum, text, True)

            if (lineStruct["level"] == level or level == None):
                if (lineStruct["command"][0] in commandList) or searchWord == None:
                    sendBack.append(lineStruct)

        return sendBack

    def findWahWah(self, key, startPoz, direction, text, level, splitBy, splitPoz, forceEndPoz, currentLineStructure):

        send = False
        searchItems = [key]
        searchItems.extend(self.__syntaxList[searchItems[0]].alias)

        if direction.endswith("All"):
           if direction.startswith("up"):
              direction = "up"
           else:
              direction = "down"

           numList = range(level - 1, -1, -1)

        else:
           numList = [level - 1]

        for lvlNum in numList:
            for item in searchItems:
                if send != False: return send

                send = self.__finderLoop(currentLineStructure, startPoz, text, direction, item,
                                         lvlNum, splitBy, splitPoz, forceEndPoz, False)

        return send

    def findEnd(self, currentLineStructure, lineNum, text):
        endCommand = "end-" + currentLineStructure["command"][0].split("-")[0]

        return self.__finderLoop(currentLineStructure,
                                 lineNum, text, "down", endCommand,
                                 currentLineStructure["level"],
                                 None, None, None, False
                                 )

    def __findStart(self, currentLineStructure, lineNum, text):
        try:
            startCommand = currentLineStructure["command"][0].split("-")[1]
        except:
            startCommand = currentLineStructure["command"][0]

        return self.__finderLoop(currentLineStructure,
                                 lineNum, text, "up", startCommand,
                                 currentLineStructure["level"],
                                 "-", 0, None, False
                                 )

    def __finderLoop(self, currentLineStructure, startPoz, text, direction, compareWord, level, splitBy, splitPoz, forceEndPoz, printMe):
        if direction == "down":
           endPoz = len(text)
           adder  = 1
        else:
           endPoz = -1
           adder  = -1

        if forceEndPoz != None:
           endPoz = forceEndPoz

        for compareLineNum in range(startPoz, endPoz, adder):

            compareLineStructure = self.getLineStructure(compareLineNum, text, True)
            ehhWord = compareLineStructure["command"][0]
            if ehhWord == None: continue
            if splitBy != None:
               ehhWord = ehhWord.split(splitBy)[splitPoz]

            if printMe == True:
               print(compareWord, compareLineNum, ehhWord, ehhWord == compareWord, level == compareLineStructure["level"])

            if ehhWord == compareWord and level == compareLineStructure["level"]:
               return [compareLineStructure["lineNum"], compareLineStructure["command"][1]]

        return False

    def returnParamsOfObjects(self, command):

        listOfValidDelimiters = self.__loader.config.getValueByKey("validObjDelimiters").split(" ")

        objectCommand = False
        for d in listOfValidDelimiters:
            if d in command and command != d:
               objectCommand = True
               break

        if objectCommand == False:
            if command in self.__syntaxList.keys():
               params   = self.__syntaxList[command].params
               ioMethod = self.__syntaxList[command].does
            else:
               params   = []
               ioMethod = None
        else:
            params   = []
            ioMethod = []

            validOnes = ["variable", "string", "stringConst", "number"]

            pList = self.__objectMaster.returnParamsForProcess(command)
            for p in pList:
                if p in validOnes:
                    params.append(p)
                else:
                    params.append("variable")
                ioMethod.append("read")

        return params, ioMethod

    def checkIfParamIsOK(self, paramType, param, ioMethod, returnBack, dimension, mustHave, cursorIn, lineStructure, text):
        foundIt = False
        noneList   = ["None", None, ""]

        command = None
        for c in self.__loader.syntaxList.keys():
            if lineStructure["command"][0] == c or lineStructure["command"][0] in self.__syntaxList[c].alias:
               command = self.__loader.syntaxList[c]
               break

        sendBack   = False
        if returnBack == None:
           returnBack  = []
           sendBack    = True

        if self.__syntaxList[lineStructure["command"][0]].flexSave:
            if lineStructure["param#" + str(len(self.__syntaxList[lineStructure["command"][0]].params))][0] \
                              in ["", "None", None] and cursorIn == "param#1":
                paramTypeList = "variable"
                ioMethod      = "write"

        paramTypeList = paramType.split("|")

        if self.doesItWriteInParam(lineStructure, cursorIn, "editor") == False:
           #if lineStructure["command"][0] == "add" and cursorIn == "param#1": print("!!!")
           ioMethod = "read"

        varOnly = False
        if command.flexSave == True:
           maxParamNum = len(command.params)
           if lineStructure["param#" + str(maxParamNum-1)][0] in noneList or lineStructure["param#" + str(maxParamNum-1)][0] == "missing":
              if cursorIn == "param#1":
                 ioMethod = "write"
                 varOnly  = True

        for pType in paramTypeList:
            if foundIt == True: break

            if param in noneList: continue

            printMe = False

            if pType == "variable":
                if printMe: print(pType)
                writable, readOnly, all, nonSystem = self.__virtualMemory.returnVariablesForBank(self.__currentBank)

                if param in all:
                    foundIt = True

                    if ioMethod == "write" and (param in readOnly):
                       if param == "item":
                          returnBack.append(
                              [self.isItemAcceptedForWrite(lineStructure, text), dimension])
                          #print(returnBack[-1])

                       else:
                          returnBack.append(["error", dimension])
                    else:
                       returnBack.append(["variable", dimension])
                    break
            elif pType == "number":
                if varOnly: continue
                if printMe: print(pType)

                import re

                numberRegexes = {"dec": r'^\d{1,3}$',
                                 "bin": r'^[b|%][0-1]{1,8}$',
                                 "hex": r'^[$|z|h][0-9a-fA-F]{1,2}$'
                                 }

                for key in numberRegexes.keys():
                    test = re.findall(numberRegexes[key], param)
                    if len(test) > 0:
                       foundIt = True
                       returnBack.append(["number", dimension])
                       if key == "dec":
                          toNum = int(param)
                          if toNum > 255:
                             returnBack[-1][0] = "error"

            elif pType == "array":
                if printMe: print(pType)

                writable, readOnly, all = self.__virtualMemory.returnArraysOnValidity(self.__currentBank)
                if param in all:
                    foundIt = True

                    if ioMethod == "write" and (param in readOnly):
                       returnBack.append(["error", dimension])
                    else:
                       returnBack.append(["array", dimension])
                    break

            elif pType == "subroutine":
                if printMe: print(pType)

                if param in self.__subroutines:
                    returnBack.append(["subroutine", dimension])
                    foundIt = True

            elif pType in ["string", "stringConst"]:
                if varOnly: continue
                if printMe: print(pType)

                delimiters = self.__config.getValueByKey("validStringDelimiters")
                errorLevel = -1

                if param[0] in delimiters:
                    delimiter = param[0]

                    if param[-1] != delimiter:
                       returnBack.append(["error", dimension])
                       errorLevel = 1
                       foundIt = True

                    else:
                       if delimiter in param[1:-1]:
                          returnBack.append(["error", dimension])
                          errorLevel = 2
                          foundIt = True

                       else:
                          stringConst = False
                          for key in self.__constants.keys():
                              if stringConst == True:
                                 break

                              testWord = param.replace(delimiter, '"')
                              if testWord == key or testWord in self.__constants[key]["alias"]:
                                 stringConst = True

                          if stringConst == True:
                             foundIt = True
                             returnBack.append(["stringConst", dimension])
                          else:
                             if pType == "string":
                                foundIt = True
                                returnBack.append(["string", dimension])
                             else:
                                foundIt = True
                                returnBack.append(["error", dimension])

                else:
                    errorLevel = 0
                    # returnBack.append(["error", dimension])
                    # foundIt = True

            elif pType == "statement":
                if printMe: print(pType)

                needComprassion = True
                stringAllowed   = False
                if lineStructure["command"][0] == "calc" or lineStructure["command"][0] in self.__syntaxList["calc"].alias:
                   needComprassion = False

                elif "%write" in lineStructure["command"][0]:
                    stringAllowed   = True
                    needComprassion = False

                addIndex = lineStructure[cursorIn][1][0]
                statementData = self.getStatementStructure(param, needComprassion, stringAllowed, addIndex, lineStructure)
                self.__statement = statementData
                foundIt = True

                # if cursorIn == "param#1": raise ValueError

                for item in statementData:
                    returnBack.append([item["type"], item["position"]])

        if foundIt == False:
           if mustHave == False and param in noneList:
              returnBack.append(["missing", dimension])
           else:
              returnBack.append(["error", dimension])

        if sendBack: return foundIt, returnBack[-1]

    def getStatementStructure(self, param, needComprassion, stringAllowed, addIndex, lineStructure):

        statementData = []

        startIndex = 0
        inside     = False
        currentDel = None

        delimiters  = self.__config.getValueByKey("validStringDelimiters").split(" ")
        arithmetics = self.__config.getValueByKey("validArithmetics").split(" ")

        for charNum in range(0, len(param)):
            if inside == False:
                if param[charNum] in (" ", "(", ")") or\
                   param[charNum] in arithmetics     or\
                   charNum == len(param) - 1:

                   endIndex = charNum
                   if charNum == len(param) - 1:
                      endIndex +=1

                   if endIndex != startIndex                         and\
                       param[startIndex:endIndex] not in ["(", ")"]  and\
                       param[startIndex:endIndex] not in arithmetics:

                       if param[endIndex-1] == ")":
                          endIndex -= 1

                       #print(param[startIndex:endIndex], startIndex, endIndex-1)
                       statementData.append(
                           {
                               "word"    : param[startIndex:endIndex],
                               "type"    : self.getType(param[startIndex:endIndex])                            ,
                               "position": [startIndex + addIndex, endIndex + addIndex-1],
                               "relative": [startIndex           , endIndex-1]
                           }

                       )
                   startIndex = endIndex + 1
                   if param[charNum] in ("(", ")"):
                      statementData.append(
                                {
                                    "word": param[charNum],
                                    "type": "invalidBracket",
                                    "position": [charNum + addIndex, charNum + addIndex],
                                    "relative": [charNum           , charNum]
                                }

                            )
                      startIndex = endIndex + 1
                   elif param[charNum] in arithmetics:
                       statementData.append(
                           {
                               "word": param[charNum],
                               "type": "arithmetic",
                               "position": [charNum + addIndex, charNum + addIndex],
                               "relative": [charNum, charNum]
                           }

                       )

                elif param[charNum] in delimiters:
                     inside = True
                     currentDel = param[charNum]
            else:
                if  charNum == len(param) - 1:
                    endIndex = charNum
                    if charNum == len(param) - 1:
                        endIndex += 1

                    if endIndex != startIndex:
                        statementData.append(
                            {
                                "word": param[startIndex:endIndex],
                                "type": self.getType(param[startIndex:endIndex]),
                                "position": [startIndex + addIndex, endIndex + addIndex-1],
                                "relative": [startIndex, endIndex-1]
                            }

                        )
                    startIndex = endIndex + 1


                elif param[charNum] == currentDel:
                     inside = False
                     currentDel = None

        numberOfCompares = 0
        lastOne          = None
        inValidPairs     = [
            ["arithmetic" , "comprass"   ],
            ["string"     , "variable"   ],
            ["stringConst", "variable"   ],
            ["string"     , "stringConst"]
        ]

        #print("1", statementData)

        for item in statementData:
            if item["type"] == "comprass":
               if numberOfCompares > 0:
                  item["type"] = "error"
                  #print("1")
               numberOfCompares += 1

            if "string" in item["type"] and stringAllowed == False:
                item["type"] = "error"
                #print("2")

            if [item["type"], lastOne]   in inValidPairs or \
               [lastOne, item["type"]]   in inValidPairs or \
               (lastOne == item["type"] and item["type"] not in ("bracket", "invalidBracket")):
               item["type"] = "error"
               #print("3")

            if stringAllowed == True and ((item["type"] == "bracket"     or item["type"] == "comprass" or
                                           item["type"] == "arithmetic") and item["word"] != "+"):
               item["type"] = "error"
               #print("4")

            lastOne = item["type"]

        level     = 0
        #print("2", statementData)

        bracketPairs = []

        for itemNum in range(0, len(statementData)):
            item      = statementData[itemNum]
            compLevel = level
            foundPair = False

            if numberOfCompares == 0 and needComprassion == True:
               item["type"] = "error"
            elif item["type"] == "comprass" and level != 0:
               item["type"] = "error"
            elif item["word"] == "(":
               level += 1
               if   item["type"] == "invalidBracket":
                   foundPair = self.findPairOfBracket(itemNum, len(statementData), 1, statementData, 0, ")")
                   if foundPair != False:
                       item["type"] = "bracket"
                       statementData[foundPair]["type"] = "bracket"
                       bracketPairs.append([itemNum, foundPair])
                   else:
                       item["type"] = "error"
            elif item["word"] == ")" and item["type"] in ["invalidBracket", "bracket"] :
                level -= 1

        #print("3", statementData)

        if lineStructure["lineNum"] == self.__cursorPoz[0]-1:
           for item in bracketPairs:
               if self.__cursorPoz[1] in [statementData[item[0]]["position"][0]  ,
                                          statementData[item[1]]["position"][0]  ,
                                          statementData[item[0]]["position"][0]+1,
                                          statementData[item[1]]["position"][0]+1]:

                  statementData[item[0]]["type"] = "bracketSelected"
                  statementData[item[1]]["type"] = "bracketSelected"


        #print("4", statementData)
        return(statementData)

    def findPairOfBracket(self, itemNum, end, adder, statementData, level, theOneWeNeed):
        compLevel = level

        if theOneWeNeed == "(": compLevel += 1

        for pairNum in range(itemNum, end, adder):
            pair = statementData[pairNum]
            if pair["word"] == "(":
                compLevel += 1
                if level == compLevel and theOneWeNeed == pair["word"]:
                    return pairNum
            elif pair["word"] == ")":
                compLevel -= 1
                if level == compLevel and theOneWeNeed == pair["word"]:
                   return pairNum

        return False

    def getType(self, word):
        writable, readOnly, all, nonSystem = self.__virtualMemory.returnVariablesForBank(self.__currentBank)

        for var in all:
            if var.startswith(word): return("variable")

        import re

        numberRegexes = {"dec": r'^\d{1,3}$',
                         "bin": r'^[b|%][0-1]{1,8}$',
                         "hex": r'^[$|z|h][0-9a-fA-F]{1,2}$'
                         }

        #print(word)
        for key in numberRegexes.keys():
            test = re.findall(numberRegexes[key], word)
            if len(test) > 0:
               return("number")

        delimiters = self.__config.getValueByKey("validStringDelimiters").split(" ")

        if word[0] in delimiters:
           for key in self.__loader.stringConstants.keys():
               if key.startswith(word): return("stringConst")
           return "string"

        comprassDict = self.getComprassionDict()["all"]

        for c in comprassDict:
            if c.startswith(word): return "comprass"

        return "error"

    def getComprassionDict(self):
        comprassionKeys = ["validNotEQ", "validEQ",
                           "validLargerThan", "validSmallerThan",
                           "validLargerThanOrEQ", "validSmallerThanOrEQ"]

        comprassionDict = {"all": []}

        for key in comprassionKeys:
            comprassionDict[key] = self.__config.getValueByKey(key).split(" ")
            for item in comprassionDict[key]:
                comprassionDict["all"].append(item)

        return comprassionDict

    def checkParams(self, param1, param2, param3, currentLineStructure, command, text):

        params, ioMethod = self.returnParamsOfObjects(command)

        returnBack = []
        noneList   = ["None", None, ""]
        ppp        = [param1, param2, param3]

        for paramNum in range(0,3):
            param         = ppp[paramNum][0]
            mustHave      = True
            try:
                paramType = params[paramNum]
                if paramType[0] == "{":
                   paramType = paramType[1:-1]
                   mustHave  = False
            except:
                paramType = None

            if   param in noneList     and paramType in noneList: break
            elif param not in noneList and paramType in noneList:
                 returnBack.append(["error", ppp[paramNum][1]])
            elif param in noneList     and paramType in noneList:
                 returnBack.append(["error", ppp[paramNum][1]])
            else:
                 self.checkIfParamIsOK(paramType, param,
                                         ioMethod, returnBack,
                                         ppp[paramNum][1], mustHave, "param#"+str(paramNum+1), currentLineStructure, text)

        #print(currentLineStructure)

        commandVar = None
        for c in self.__loader.syntaxList.keys():
            if currentLineStructure["command"][0] == c or currentLineStructure["command"][0] in self.__syntaxList[c].alias:
               commandVar = self.__loader.syntaxList[c]
               break

        if command == "const" or command in self.__syntaxList["const"].alias:
           if returnBack[0][0] == "string" and returnBack[1][0] == "number":
              if param1[0] in self.__constants.keys():
                 returnBack[0][0] = "error"
              else:
                 self.__constants[param1[0]] = {
                    "alias": [param1[0].upper(), param1[0].lower()],
                    "value": param2[0]
                 }
           elif returnBack[0][0] == "stringConst":
               returnBack[0][0] = "error"

        elif command == "subroutine" or command in self.__syntaxList["subroutine"].alias:
           if returnBack[0][0] == "string":
              if param1[0] in self.__subroutines:
                 returnBack[0][0] = "error"
              else:
                 self.__subroutines.append(param1[0])

           elif returnBack[0][0] == "subroutine":
                returnBack[0][0] = "error"

        elif command == "call" or command in self.__syntaxList["call"].alias:
            if returnBack[0][0] == "subroutine":
               if param1[0] not in self.__subroutines:
                  returnBack[0][0] = "error"

        elif command == "goto" or command in self.__syntaxList["goto"].alias:
            valid  = False
            number = None
            if returnBack[0][0] == "stringConst":
               number = self.__constants[param1[0].replace("#", "")]
               if int(param1[0].replace("#", "")) > 1 and int(param1[0].replace("#", "")) < 9:
                  valid  = True
            elif returnBack[0][0] == "number":
               if int(param1[0].replace("#", "")) > 1 and int(param1[0].replace("#", "")) < 9:
                   number = param1[0]
                   valid  = True

            if valid == True:
               if self.__virtualMemory.locks["bank"+str(number)] not in (None, "None", ""):
                  #print("#1")
                  returnBack[0][0] = "error"
            else:
                #print("#2")
                returnBack[0][0] = "error"

        elif command == "select" or command in self.__syntaxList["select"].alias:
            if returnBack[0][0] == "stringConst":
               if self.convertStringNumToNumber(self.__constants[param1[0]]["value"]) != 1:
                   returnBack[0][0] = "error"
            elif returnBack[0][0] == "number":
                if self.convertStringNumToNumber(param1[0]) not in [0, 1]:
                   returnBack[0][0] = "error"

        elif command == "case" or command in self.__syntaxList["case"].alias:

            startFound = self.findWahWah("select", currentLineStructure["lineNum"],
                             "up", text, currentLineStructure["level"], "-", 0, None, currentLineStructure)

            if startFound != False:
               selectNum = startFound[0]
               selectLineStructure = self.getLineStructure(selectNum, text, False)

               paramType = self.__syntaxList["select"].params[0]
               temp      = []

               self.checkIfParamIsOK(paramType, selectLineStructure["param#1"][0],
                                       "read", temp, None, True, "param#1", currentLineStructure, text)

               if   temp[0][0] == "variable" and returnBack[0][0] not in ["number", "stringConst", "variable"]:
                    returnBack[0][0] = "error"
               elif temp[0][0] in ["stringConst", "number"]:
                    isThatStatement, filler = self.isThatADamnStatement(currentLineStructure, currentLineStructure["param#1"][1])
                    if isThatStatement == False:
                       for item in returnBack:
                           item[0] = "error"

        elif commandVar.flexSave == True:
             theCommand = self.__loader.syntaxList[command]
             paramMaxNum = len(theCommand.params)

             if returnBack[paramMaxNum - 1][0] != "missing":
                if returnBack[paramMaxNum - 1][0] != "variable": returnBack[paramMaxNum - 1][0] = "error"
             else:
                if returnBack[0][0] != "variable": returnBack[0][0] = "error"

        if "item" in [param1[0], param2[0], param3[0]]:
            returnBack[0][0] = self.isItemAcceptedForWrite(currentLineStructure, text)

        return returnBack

    def isItemAcceptedForWrite(self, currentLineStructure, text):
        startFound = self.findWahWah("do-items", currentLineStructure["lineNum"],
                                     "upAll", text, currentLineStructure["level"], None, None, None,
                                     currentLineStructure)

        if startFound == False:
            #print("#1")
            return "error"
        else:
            doNum = startFound[0]
            doLineStructure = self.getLineStructure(doNum, text, False)

            array = doLineStructure["param#1"][0]
            if array in self.__virtualMemory.arrays.keys():
                readOnly = self.__virtualMemory.hasArrayReadOnly(array)
            else:
                #print("2")
                return "error"

            if readOnly == True:
                endFound = self.findWahWah("end-do", currentLineStructure["lineNum"],
                                           "downAll", text, currentLineStructure["level"], None, None, None,
                                           currentLineStructure)

                if endFound != False:
                    endDoNum = endFound[0]
                    listOfCommands = self.listAllCommandFromTo(None, text, None, doNum, endDoNum + 1)

                    isOneWriting = False
                    for thisLineStructure in listOfCommands:
                        if "item" in [
                            thisLineStructure["param#1"][0],
                            thisLineStructure["param#2"][0],
                            thisLineStructure["param#3"][0]]:
                            c = thisLineStructure["command"][0]

                            for key in self.__syntaxList.keys():
                                if key == c or c in self.__syntaxList[key].alias:
                                    if self.doesItWriteInParam(thisLineStructure, "param#" + \
                                                                                  str([thisLineStructure["param#1"][0],
                                                                                       thisLineStructure["param#2"][0],
                                                                                       thisLineStructure["param#3"][
                                                                                           0]].index("item")+1), "editor" ):
                                        isOneWriting = True
                                        break
                        if isOneWriting == True:
                            #print("3")
                            return "error"
        return "variable"

    def convertStringNumToNumber(self, num):
        if type(num) == int  : return num
        if type(num) == float: return int(num)

        if num.startswith("#"): num = num[1:]
        binSigns = self.__config.getValueByKey("validBinarySigns").split(" ")
        hexSigns = self.__config.getValueByKey("validHexSigns").split(" ")

        mode = 10
        if   num[0] in binSigns:
             mode = 2
             num  = "0b" + num[1:]
        elif num[0] in hexSigns:
             mode = 16
             num  = "0x" + num[1:]

        #print(num, mode)

        return(int(num, mode))

    def findObjects(self, structureItem, firstObjects):
        from copy import deepcopy

        delimiter = "%"
        delimiters = self.__config.getValueByKey("validObjDelimiters").split(" ")

        for d in delimiters:
            if d in structureItem[0]:
               delimiter = d
               break

        listOfPotentialObjects = structureItem[0].split(delimiter)
        objects                = {}
        startIndex             = 0
        lastObj                = None
        listOfNextLevel        = deepcopy(firstObjects)

        maxNum = 3
        if len(listOfPotentialObjects) < maxNum: maxNum = len(listOfPotentialObjects)

        for num in range(0, maxNum):

            currentPossibleObject = listOfPotentialObjects[num]

            if currentPossibleObject in listOfNextLevel:
               objects[currentPossibleObject] = [
                   [startIndex + structureItem[1][0],
                    startIndex + structureItem[1][0] + len(currentPossibleObject) - 1
                    ], self.__objectMaster.returnObjectOrProcess(currentPossibleObject)
               ]

               lastObj         = currentPossibleObject
               startIndex     += len(lastObj) + 1
               listOfNextLevel = self.__objectMaster.returnNextLevel(lastObj)
               for itemNum in range(0, len(listOfNextLevel)):
                   if "(" in listOfNextLevel[itemNum]:
                       listOfNextLevel[itemNum] = listOfNextLevel[itemNum].split("(")[0]

            else:
               break

        return objects

    def getCurrentWord(self, line):
        delimiters = self.__config.getValueByKey("validStringDelimiters").split(" ")
        line = line.replace("\t", " ")

        endPoz = self.__cursorPoz[1]
        startPoz = 0
        inside   = False
        stringD  = None

        for charNum in range(0, endPoz):
            if charNum >= len(line): break

            if inside == True and line[charNum] == stringD:
               stringD = None
               inside  = False
            else:
               if inside == False:
                  if   charNum > len(line) - 1: break
                  if   line[charNum] in delimiters:
                       stringD  = line[charNum]
                       inside   = True
                       startPoz = charNum
                  elif line[charNum] in ("(", ",", " "):
                       startPoz = charNum + 1

        return line[startPoz:endPoz]

    def getLineStructure(self, lineNum, text, checkLevel):
        if lineNum == None: lineNum = self.__cursorPoz[0]-1

        if text == None:
           text = self.__codeBox.get(0.0, END).replace("\t", " ").split("\n")

        if type(text) == str: text = text.replace("\t", " ").split("\n")

        line = text[lineNum].replace("\t", " ")

        lineStructure = {
            "command": [None, [-1, -1]],
            "(":        -1,
            "param#1": [None, [-1, -1]],
            "param#2": [None, [-1, -1]],
            "param#3": [None, [-1, -1]],
            ")":        -1,
            "lineNum":  lineNum,
            "level":    -1,
            "comment": [None, [-1,-1]],
            "commas": [],
            "unreachable": False
        }
        delimiterPoz = self.getFirstValidDelimiterPoz(line)
        validDelimiters = self.__config.getValueByKey("validStringDelimiters").split(" ")

        lineStructure["comment"] = [
            line[(delimiterPoz + 1):], [delimiterPoz + 1, len(line) - 1 ]
        ]

        if delimiterPoz == 0:
           lineStructure["comment"] = [
               line[1:],
               [1, len(line) - 1]
            ]

        if delimiterPoz == len(line):
            lineStructure["comment"][1][0] = len(line)

        if lineStructure["comment"][0] == "" or lineStructure["comment"][1][0] > lineStructure["comment"][1][1]:
           lineStructure["comment"][1][1] = lineStructure["comment"][1][0]

        if len(line) == 0: return  lineStructure

        if line[0] not in ("*", "#"):

            for num in range(0, delimiterPoz):
                if line[num] == "(":
                   lineStructure["("] = num
                   break

            inString   = False
            stringDel  = None


            for num in range(delimiterPoz-1, -1, -1):
                if line[num] in validDelimiters:
                    if inString == False:
                        inString = True
                        stringDel = line[num]
                    elif line[num] == stringDel:
                        inString = False

                if line[num] == ")" and inString == False:
                   lineStructure[")"] = num
                   break

            inside = ""
            if lineStructure["("] != -1:
               if lineStructure[")"] != -1:
                  inside = line[lineStructure["("] + 1 : lineStructure[")"]]
               else:
                  inside = line[lineStructure["("] + 1 : delimiterPoz]

            if lineStructure["("] != -1:
               startX = -1
               endX   = lineStructure["("] - 1
               firstNoneSpace = False
               for num in range(lineStructure["("] - 1, -1, -1):
                   if line[num] == " " and firstNoneSpace == True:
                      startX = num + 1
                      break
                   elif line[num] != " " and firstNoneSpace == False:
                      firstNoneSpace = True
                      endX           = num
                   elif num == 0:
                       startX = 0
                       break

               if startX not in [-1, lineStructure["("]]:
                   lineStructure["command"] = [
                       line[startX : endX + 1],
                       [startX, endX]
                   ]


            else:
                startX = -1
                endX   = -1

                for num in range(0, delimiterPoz + 1):
                    if num == delimiterPoz: break
                    elif line[num] != " ":
                       startX = num
                       break


                for num in range(startX, delimiterPoz + 1):
                    if num == delimiterPoz:
                       if startX != -1: endX = num -1
                       break
                    elif line[num] == " ":
                       endX = num - 1
                       break

                if startX != -1 and endX != -1:
                    lineStructure["command"] = [
                        line[startX: endX+1],
                        [startX, endX]
                    ]


            if lineStructure["("] != -1:
               startX = lineStructure["("] + 1
               endX   = delimiterPoz

               if lineStructure[")"] != -1:
                  endX = lineStructure[")"]

               paramNum   = 0
               paramStart = startX
               paramEnd   = -1
               inString   = False
               stringDel  = None

               for num in range(startX, endX):
                   if line[num] in validDelimiters:
                      if   inString == False:
                           inString  = True
                           stringDel = line[num]
                      elif line[num] == stringDel:
                           inString = False

                   #print(line[num], inString, stringDel)

                   if (line[num] == "," or num == endX - 1) and inString == False:
                      if line[num] == ",":
                         lineStructure["commas"].append(num)

                      paramName = "param#" + str(paramNum + 1)

                      paramEnd = num
                      if line[num] == ",":
                         paramEnd = num - 1

                      lineStructure[paramName] = [
                        line[paramStart : paramEnd + 1],
                        [paramStart, paramEnd]
                      ]

                      paramNum += 1
                      if paramNum > 2: break
                      paramStart = paramEnd + 2

            for key in lineStructure:
                if type(lineStructure[key]) == list and key != "commas":
                   if lineStructure[key][0] != None:
                        cutStart = 0
                        cutEnd   = 0

                        word = lineStructure[key][0]

                        for num in range(0, len(word)):
                            if word[num] == " ":
                               cutStart  += 1
                            else:
                                break

                        for num in range(len(word)-1, -1, -1):
                            if word[num] == " ":
                                cutEnd   += 1
                            else:
                                break

                        lineStructure[key][0] = word[cutStart : len(word) - cutEnd]
                        lineStructure[key][1][0] += cutStart
                        lineStructure[key][1][1] -= cutEnd

            if checkLevel == True and lineStructure["command"][0] != None:
               # lines = self.__codeBox.get(0.0, END).replace("\t", " ").split("\n")
               level     = 0
               for compareLineNum in range(0, lineNum):
                   compareStructure = self.getLineStructure(compareLineNum, text, False)
                   if compareStructure["command"][0] != None:
                       if compareStructure["command"][0].split("-")[0].upper() in ["DO", "PERFORM",
                                                                                   "FOR", "FOREACH",
                                                                                   "SELECT", "SWITCH",
                                                                                   "EVALUATE"]:
                          level += 1
                       elif compareStructure["command"][0].split("-")[0].upper() == "END":
                          level -= 1

               if lineStructure["command"][0].split("-")[0].upper() == "END": level -= 1
               if level < 0: level = 0

               lineStructure["level"] = level

        if lineNum == self.__cursorPoz[0]-1:
            self.__lineStructure = lineStructure

        #print(lineStructure)
        return(lineStructure)

    def updateLineDisplay(self, lineStructure):
        self.createFakeCodeEditorItems(lineStructure, self.__codeEditorItems)
        self.__codeEditorItems["updateRow"].config(state = DISABLED)
        self.__checkEditorItems(lineStructure)

    def __checkEditorItems(self, lineStructure):

        textToPrint = self.__getFakeLine(self.__codeEditorItems)

        selectPosizions = []
        errorPositions  = []

        objectList = self.__objectMaster.getStartingObjects()
        objectList.append("game")

        self.__theNumOfLine = lineStructure["lineNum"]
        self.__lineTinting(textToPrint, objectList, lineStructure["lineNum"], selectPosizions, errorPositions, "lineEditor", None, None)

    def __focusOut(self, event):
        #print(event.type)

        if event.widget in self.__focusOutItems:
           if event.type == "FocusOut":
              self.__focused = None
           else:
              self.__codeEditorItems["updateRow"].config(state = NORMAL)
           textToPrint = self.__getFakeLine(self.__codeEditorItems)

           selectPosizions = []
           errorPositions  = []

           objectList = self.__objectMaster.getStartingObjects()
           #objectList.append("game")

           self.__lineTinting(textToPrint, objectList, self.__theNumOfLine,
                              selectPosizions, errorPositions, "lineEditor", None, None)


    def __getFakeLine(self, source):

        self.reAlignCommandsAndParams()

        if source == None: source = self.__codeEditorItems

        noneList = [None, "None", ""]

        try:
            level = int(source["level"].cget("text"))
        except Exception as e:
            level = 0

        if level == -1:
           lineText = ""
        else:
           lineText = " " * ((level * 4) + 1 )
        dominantObjDelimiter = self.getDominantObjDelimiter()

        if source["command#1"][0].get() not in noneList:
           lineText = lineText + source["command#1"][0].get()

        if source["command#2"][0].get() not in noneList:
           lineText = lineText + dominantObjDelimiter +  source["command#2"][0].get()

        if source["command#3"][0].get() not in noneList:
           lineText = lineText + dominantObjDelimiter +  source["command#3"][0].get()

        if (source["param#1"][0].get() not in noneList or
            source["param#2"][0].get() not in noneList or
            source["param#3"][0].get() not in noneList):
            lineText = lineText + "("

        if source["param#1"][0].get() not in noneList:
           lineText = lineText + source["param#1"][0].get()

        if source["param#2"][0].get() not in noneList:
           lineText = lineText + ", " + source["param#2"][0].get()

        if source["param#3"][0].get() not in noneList:
           lineText = lineText + ", " + source["param#3"][0].get()

        if (source["param#1"][0].get() not in noneList or
            source["param#2"][0].get() not in noneList or
            source["param#3"][0].get() not in noneList):
            lineText = lineText + ")"

        if source["comment"][0].get() not in noneList:
           if source["command#1"][0].get() not in noneList or \
              source["param#1"][0].get() not in noneList:
              lineText = lineText + " " + self.getDominantDelimiter() + "\t" + source["comment"][0].get()
           else:
              lineText = "*" +  source["comment"][0].get()

        return lineText

    def getDominantObjDelimiter(self):
        text = self.__codeBox.get(0.0, END).replace("\t", " ").split("\n")

        delimiterKeys = self.__config.getValueByKey("validObjDelimiters").split(" ")
        delimiters = {}

        for key in delimiterKeys:
            delimiters[key] = 0

        for lineNum in range(0, len(text)):
            line = text[lineNum]
            lineStruct = self.getLineStructure(lineNum, text, False)

            currentDel = None

            if lineStruct["command"][0] == None: continue

            for d in delimiterKeys:
                if d in lineStruct["command"][0]:
                   currentDel = d
                   break

            if currentDel != None:
               delimiters[currentDel] += 1

        largest  = "%"
        largeNum = 0
        for key in delimiterKeys:
            if delimiters[key] > largeNum:
               largeNum = delimiters[key]
               largest  = key

        return largest

    def getDominantDelimiter(self):
        text = self.__codeBox.get(0.0, END).replace("\t", " ").split("\n")

        delimiterKeys = self.__config.getValueByKey("validLineDelimiters").split(" ")

        delimiters = {}

        for key in delimiterKeys:
            delimiters[key] = 0

        for line in text:
            poz = self.getFirstValidDelimiterPoz(line)
            if poz == 0 or poz == len(line): continue
            delimiters[line[poz]] += 1

        largest  = "!"
        largeNum = 0
        for key in delimiterKeys:
            if delimiters[key] > largeNum:
               largeNum = delimiters[key]
               largest  = key

        return largest

    def addTag(self, Y, X1, X2, tag):
#       tagRanges = self.__codeBox.tag_ranges("sel")
        #if tag == "error": raise ValueError

        self.__codeBox.tag_add(tag, str(Y) + "." + str(X1) , str(Y) + "." + str(X2))

        if tag == "error":
           self.__foundError = True

    def removeTag(self, Y, X1, X2, tags):
        if tags == None:
            for tag in self.__codeBox.tag_names():
                if tag == "sel": continue
                self.__codeBox.tag_remove(tag,
                                          str(Y) + "." + str(X1),
                                          str(Y) + "." + str(X2)
                                          )
        elif tags == "nonError":
            for tag in self.__codeBox.tag_names():
                if tag in [ "sel" , "error"]: continue

                self.__codeBox.tag_remove(tag,
                                          str(Y) + "." + str(X1),
                                          str(Y) + "." + str(X2)
                                          )
        elif tags == "background":
            for tag in self.__codeBox.tag_names():
                if "back" in tag.lower():
                    self.__codeBox.tag_remove(tag,
                                              str(Y) + "." + str(X1),
                                              str(Y) + "." + str(X2)
                                              )
        elif type(tags) == str:
            self.__codeBox.tag_remove(tags,
                                      str(Y) + "." + str(X1),
                                      str(Y) + "." + str(X2)
                                      )
        else:
            for tag in tags:
                if tag == "sel": continue

                self.__codeBox.tag_remove(tag,
                                          str(Y) + "." + str(X1),
                                          str(Y) + "." + str(X2)
                                          )

    def getFirstValidDelimiterPoz(self, line):
        if len(line) == 0: return 0
        if line[0] in ("*", "#"): return 0

        level = 0
        validDelimiters = self.__config.getValueByKey("validLineDelimiters").split(" ")
        for charNum in range(0, len(line)):
            if line[charNum] in validDelimiters and level == 0 and\
               (charNum == 0 or line[charNum-1] in (" ", ")", "\t")):
                return charNum

            if line[charNum] == "(": level += 1
            if line[charNum] == ")": level -= 1
            if level < 0           : level  = 0

        return(len(line))

    def __counterEnded(self):
        self.__loader.virtualMemory.codes[self.__currentBank][self.__currentSection].changed = True
        self.__setTinting(self.__cursorPoz[0])

    def clicked(self, event):
        self.__focused2 = event.widget
        self.__counterEnded2()

    def __counterEnded2(self):
        self.setCurzorPoz()
        self.__foundError     = False

        self.__setTinting("whole")

    def __keyPressed(self, event):
        if (event.keysym == "Control_L" or event.keysym == "Control_R"):
            self.__ctrl = True

    def __keyReleased(self, event):
        self.__lastButton = event.keysym
        self.__counter   = 3
        self.__counter2  = 20

        self.setCurzorPoz()

        if (event.keysym == "Control_L" or event.keysym == "Control_R"):
            self.__ctrl = False

    def setCurzorPoz(self):
        __cursorPoz = self.__codeBox.index(INSERT)
        self.__cursorPoz = [int(__cursorPoz.split(".")[0]), int(__cursorPoz.split(".")[1])]

    def __mouseWheel(self, event):
        if self.__ctrl == False: return

        if event.delta > 0 and int(self.__config.getValueByKey("codeBoxFont")) < 36:
            self.__config.setKey("codeBoxFont", str(int(self.__config.getValueByKey("codeBoxFont")) + 1))
            self.__getFont()

        if event.delta < 0 and int(self.__config.getValueByKey("codeBoxFont")) > 12:
            self.__config.setKey("codeBoxFont", str(int(self.__config.getValueByKey("codeBoxFont")) - 1))
            self.__getFont()

    def __getFont(self):
        baseSize = int(self.__config.getValueByKey("codeBoxFont"))
        w = self.__editor.getWindowSize()[0] / 1600
        h = self.__editor.getWindowSize()[1] / 1200

        self.__fontSize = (baseSize * w * h * 1.5)
        self.__normalFont = self.__loader.fontManager.getFont(round(self.__fontSize), False, False, False)
        self.__boldFont = self.__loader.fontManager.getFont(round(self.__fontSize), True, False, False)
        self.__italicFont = self.__loader.fontManager.getFont(round(self.__fontSize), False, True, False)
        self.__undelinedFont = self.__loader.fontManager.getFont(round(self.__fontSize), False, False, True)
        self.__boldItalicFont = self.__loader.fontManager.getFont(round(self.__fontSize), True, True, False)
        self.__boldUnderlinedFont = self.__loader.fontManager.getFont(round(self.__fontSize), True, False, True)
        self.__boldItalicUnderLinedFont = self.__loader.fontManager.getFont(round(self.__fontSize), True, True, True)

        self.__tagSettings = {
            "comment": {
                "foreground": self.__loader.colorPalettes.getColor("comment"),
                "font": self.__italicFont
            },
            "object": {
                "foreground": self.__loader.colorPalettes.getColor("object"),
                "font": self.__boldFont
            },
            "variable": {
                "foreground": self.__loader.colorPalettes.getColor("variable"),
                "font": self.__boldUnderlinedFont
            },
            "array": {
                "foreground": self.__loader.colorPalettes.getColor("array"),
                "font": self.__boldUnderlinedFont
            },
            "number": {
                "foreground": self.__loader.colorPalettes.getColor("number"),
                "font": self.__normalFont
            },
            "command": {
                "foreground": self.__loader.colorPalettes.getColor("command"),
                "font": self.__boldFont
            },
            "process": {
                "foreground": self.__loader.colorPalettes.getColor("command"),
                "font": self.__boldFont
            },
            "error": {
                "foreground": self.__loader.colorPalettes.getColor("boxFontUnSaved"),
                "background": self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                "font": self.__boldFont
            },
            "string": {
                "foreground": self.__loader.colorPalettes.getColor("stringBack"),
                "background": self.__loader.colorPalettes.getColor("stringFont"),
                "font": self.__boldFont
            },
            "stringConst": {
                "foreground": self.__loader.colorPalettes.getColor("constStringBack"),
                "background": self.__loader.colorPalettes.getColor("constStringFont"),
                "font": self.__boldFont
            },

            "bracket": {
                "foreground": self.__loader.colorPalettes.getColor("bracket"),
                "font": self.__boldFont
            },

            "comprass": {
                "foreground": self.__loader.colorPalettes.getColor("bracket"),
                "font": self.__boldFont
            },

            "arithmetic": {
                "foreground": self.__loader.colorPalettes.getColor("bracket"),
                "font": self.__boldFont
            },

            "subroutine": {
                "foreground": self.__loader.colorPalettes.getColor("subroutine"),
                "font": self.__boldUnderlinedFont
            }
        }

        for key in self.__tagSettings:
            if "background" not in self.__tagSettings[key]:
                self.__codeBox.tag_config(key,
                                          foreground = self.__tagSettings[key]["foreground"],
                                          font = self.__tagSettings[key]["font"])
            elif "foreground" not in self.__tagSettings[key]:
                self.__codeBox.tag_config(key,
                                          background = self.__tagSettings[key]["background"],
                                          font = self.__tagSettings[key]["font"])
            else:
                self.__codeBox.tag_config(key,
                                              foreground=self.__tagSettings[key]["foreground"],
                                              background=self.__tagSettings[key]["background"],
                                              font=self.__tagSettings[key]["font"])


        self.__codeBox.tag_config("highLight", background=self.__loader.colorPalettes.getColor("highLight"))

        self.__codeBox.tag_config("unreachable", background=self.__loader.colorPalettes.getColor("unreachable"))

        self.__codeBox.tag_config("commandBack", background=self.__loader.colorPalettes.getColor("commandBack"),
                                                 foreground=self.__loader.colorPalettes.getColor("command"),
                                                 font = self.__boldFont)

        self.__codeBox.tag_config("bracketSelected",
                                  foreground=self.__loader.colorPalettes.getColor("bracket"),
                                  background=self.__loader.colorPalettes.getColor("bracketSelected"),
                                  font=self.__boldFont)


        self.__codeBox.config(font=self.__normalFont)
        self.__codeBox.tag_raise("sel")

    def isPowerOfTwo(self, num):
        return num & (num - 1) == 0