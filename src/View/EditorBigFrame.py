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

        self.__words = ["lineNum", "level", "command", "param#1", "param#2", "param#3", "comment", "updateRow"]


        self.__focused = None
        self.__screenSize = self.__loader.screenSize
        self.__counter    = 0
        self.__counter2    = 0
        self.firstTry = True

        self.__cursorPoz  = [1,0]

        self.__destroyables = {}
        self.__lastButton   = None

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize*0.65), False, False, False)
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

        self.__bankButtons    = self.__editor.changerButtons
        self.__sectionButtons = self.__editor.sectionButtons
        self.__highLightWord       = None
        self.__highLightIgnoreCase = True

        from threading import Thread
        self.__ctrl = False

        t = Thread(target=self.loop)
        t.daemon = True
        t.start()

    def __insertPressed(self, event):
        self.__insertSelectedFromBox()

    def __insertSelectedFromBox(self):
        pass

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

            if self.__counter == 1: self.__counterEnded()
            if self.__counter2 == 1: self.__counterEnded2()

            sleep(0.005)

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

        self.__codeBox = scrolledtext.ScrolledText(self.__mainFrame, width=999999, height=self.__mainFrame.winfo_height(), wrap=WORD)
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

        bannerItems = [[self.__dictionaries.getWordFromCurrentLanguage("number")        , 1.5, Label,  None],
                       [self.__dictionaries.getWordFromCurrentLanguage("level")         , 1.5, Label,  None],
                       [self.__dictionaries.getWordFromCurrentLanguage("command")       , 2,   Entry,  NORMAL],
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
        xUnit = self.__mainFrame.winfo_width() // sumItems
        self.__labelFrames       = []
        self.__headerLabels      = []
        self.__codeEditoritems   = {}

        for item in bannerItems:
            bannerItemLens.append(
                int(len(item[0])  * xUnit * item[1])
            )

            f = Frame(self.__codeFrameHeader, width=bannerItemLens[-1],
                                         height=99999999,
                                         bg=self.__colors.getColor("window"))
            f.pack_propagate(False)
            f.pack(side=LEFT, anchor = E, fill=Y)

            self.__labelFrames.append(f)

            num = bannerItems.index(item)
            c = colors[num%2]

            label = Label(f, text=item[0],
                      font=self.__miniFont, fg=c[0], bg=c[1], justify=CENTER
                      )

            label.pack_propagate(False)
            label.pack(side=TOP, anchor=N, fill=BOTH)

            self.__headerLabels.append(label)

            f2 = Frame(self.__codeFrameEditor, width=bannerItemLens[-1],
                                         height=99999999,
                                         bg=self.__colors.getColor("window"))
            f2.pack_propagate(False)
            f2.pack(side=LEFT, anchor = E, fill=Y)

            self.__labelFrames.append(f2)

            if   bannerItems[num][2] == Label:
                label = Label(f2, text="-",
                              font=self.__miniFont,
                              fg=self.__colors.getColor("font"),
                              bg=self.__colors.getColor("window"),
                              justify=CENTER
                              )

                label.pack_propagate(False)
                label.pack(side=TOP, anchor=N, fill=BOTH)
                self.__codeEditoritems[self.__words[num]] = label

            elif bannerItems[num][2] == Entry:
                entryVar = StringVar()

                entry = Entry(f2, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                   width=99999,
                                   fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                   textvariable=entryVar, name=self.__words[num],
                                   font=self.__miniFont, justify=CENTER,
                                   )
                entry.pack_propagate()
                entry.pack(side=TOP, anchor=N, fill=BOTH)

                entry.bind("<KeyRelease>", self.checker)
                entry.bind("<FocusOut>", self.checker)

                self.__codeEditoritems[self.__words[num]] = [entryVar, entry]


            elif bannerItems[num][2] == Button:
                button = Button(f2,      width=9999999,
                                         command=bannerItems[num][3],
                                         state=DISABLED,
                                         font=self.__tinyFont, fg=self.__colors.getColor("font"),
                                         bg=self.__colors.getColor("window"),
                                         text=bannerItems[num][0])
                button.pack_propagate(False)
                button.pack(fill=X)

                self.__codeEditoritems[self.__words[num]] = button


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

        self.__scrollBarOnTheRight = s
        self.__listBoxOnTheRight   = l
        self.firstTry = True

        self.getLineStructure(None, None, True)
        self.__loadFromMemory(self.__currentBank, self.__currentSection)

    def updateTextFromDisplay(self):
        pass

    def checker(self, event):
        pass

    def focusOut(self, event):
        self.__setTinting("whole")
        self.__loader.mainWindow.focusOut(event)

    def __loadFromMemory(self, bank, section):
        if self.__loader.virtualMemory.codes[self.__currentBank][self.__currentSection].changed == True:
           pass

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

        if self.__lastButton == "Enter": mode = "whole"

        #objectList, processList = self.__objectMaster.getObjectsAndProcessesValidForGlobalAndBank()
        objectList = self.__objectMaster.getStartingObjects()
        objectList.append("game")

        selectPosizions = []
        errorPositions  = []

        from copy import deepcopy
        self.__constants = deepcopy(self.__loader.stringConstants)

        if mode == "whole":

           for num in range (1, len(text)+1):
               self.__lineTinting(text[num-1], objectList, num-1, selectPosizions, errorPositions)

               for item in selectPosizions:
                   self.removeTag(item[2] + 1, item[0], item[1] + 1, "background")
                   self.addTag(item[2] + 1, item[0], item[1] + 1, "commandBack")

               for item in errorPositions:
                   self.removeTag(item[2] + 1, item[0], item[1] + 1, None)
                   self.addTag(item[2] + 1, item[0], item[1] + 1, "error")

        else:
            self.__lineTinting(text[mode-1], objectList, mode-1, selectPosizions, errorPositions)

    def __lineTinting(self, line, objects, lineNum, selectPosizions, errorPositions):
        if len(line) == 0: return

        delimiterPoz = self.getFirstValidDelimiterPoz(line)
        yOnTextBox = lineNum + 1
        line = line.replace("\t", " ")

        self.removeTag(yOnTextBox, 0, len(line), None)
        text = self.__codeBox.get(0.0, END).replace("\t", " ").split("\n")

        currentLineStructure = self.getLineStructure(lineNum, text, True)

        if line[0] in ("*", "#"): delimiterPoz = 0

        if delimiterPoz != len(line):
           self.addTag(yOnTextBox, delimiterPoz, len(line), "comment")

        hasValidCommand = False
        addError        = False
        commandParams   = []

        if currentLineStructure["command"][0] in self.__syntaxList.keys():
           self.addTag(yOnTextBox, currentLineStructure["command"][1][0],
                                   currentLineStructure["command"][1][1]+1, "command")

           hasValidCommand = True
           commandParams   = self.__syntaxList[currentLineStructure["command"][0]].params

           if self.__syntaxList[currentLineStructure["command"][0]].endNeeded == True:
                endFound = self.__findEnd(currentLineStructure, lineNum, text)
                if endFound == False: addError = True
                else:
                    if self.__cursorPoz[0] == yOnTextBox:

                       self.addToPosizions(selectPosizions, self.convertToX1X2Y(endFound))
                       self.addToPosizions(selectPosizions,
                                                 self.convertToX1X2Y(self.getXYfromCommand(currentLineStructure)))


           elif currentLineStructure["command"][0].startswith("end-") == True:
               startFound = self.__findStart(currentLineStructure, lineNum, text)
               if startFound == False: addError = True
               else:
                   if self.__cursorPoz[0] == yOnTextBox:

                      self.addToPosizions(selectPosizions, self.convertToX1X2Y(startFound))
                      self.addToPosizions(selectPosizions,
                                                self.convertToX1X2Y(self.getXYfromCommand(currentLineStructure)))


           elif currentLineStructure["command"][0] == "case" or currentLineStructure["command"][0] in\
                self.__syntaxList["case"].alias:

                foundAllRelatedForCaseDefault = self.__foundAllRelatedForCaseDefault(currentLineStructure, lineNum, text, False)
                if foundAllRelatedForCaseDefault["select"] == False or foundAllRelatedForCaseDefault["end-select"] == False: addError = True

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

               foundAllRelatedForCaseDefault = self.__foundAllRelatedForCaseDefault(currentLineStructure, lineNum, text,
                                                                                    False)

               if foundAllRelatedForCaseDefault["select"] == False or foundAllRelatedForCaseDefault[
                   "end-select"] == False or foundAllRelatedForCaseDefault["numOfDefaults"] > 1 or \
                       foundAllRelatedForCaseDefault["numOfCases"] == 0: addError = True

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

                if foundAllRelatedForDoAndEndDo["start"] == False or foundAllRelatedForDoAndEndDo["end"] == False: addError = True

                if addError == False and self.__cursorPoz[0] == yOnTextBox:
                    self.addToPosizions(selectPosizions,
                                              self.convertToX1X2Y(foundAllRelatedForDoAndEndDo["start"]))
                    self.addToPosizions(selectPosizions,
                                              self.convertToX1X2Y(foundAllRelatedForDoAndEndDo["end"]))
                    self.addToPosizions(selectPosizions,
                                              self.convertToX1X2Y(self.getXYfromCommand(currentLineStructure)))

           if currentLineStructure["command"][0] == "do-items" or\
              currentLineStructure["command"][0] in self.__syntaxList["do-items"].alias:

              firstPoz  = []
              lastPoz   = []

              if currentLineStructure["level"] == 0:
                 firstPoz = lineNum
                 lastPoz  = self.__findEnd(currentLineStructure, lineNum, text)

              else:
                 from copy import deepcopy

                 copied = deepcopy(currentLineStructure)
                 copied["level"] = 0

                 xyz = self.__foundAllRelatedForDoAndEndDo(copied, lineNum, text, "do-items")

                 firstPoz = xyz["start"]
                 lastPoz  = xyz["end"]

              if firstPoz != False and type(firstPoz) != int: firstPoz = firstPoz[0]
              if lastPoz  != False:                           lastPoz  = lastPoz[0]

              listOfDoItems = self.__listAllCommandFromTo("do-items", text, None, firstPoz, lastPoz + 1)
              if len(listOfDoItems) > 1:
                 for item in listOfDoItems:
                     self.addToPosizions(errorPositions,
                                         self.convertToX1X2Y(self.getXYfromCommand(item)))

           if  ((currentLineStructure["("] == -1 or currentLineStructure[")"] == -1) and
                self.__syntaxList[currentLineStructure["command"][0]].bracketNeeded == True or
               (currentLineStructure["("] != -1 or currentLineStructure[")"] != -1) and
               self.__syntaxList[currentLineStructure["command"][0]].bracketNeeded == False):
                    addError = True

           if self.__currentSection not in self.__syntaxList[currentLineStructure["command"][0]].sectionsAllowed:
              addError = True


           if addError == True:
               self.removeTag(yOnTextBox, currentLineStructure["command"][1][0],
                              currentLineStructure["command"][1][1] + 1, None)
               self.addTag(yOnTextBox, currentLineStructure["command"][1][0],
                           currentLineStructure["command"][1][1] + 1, "error")

        elif currentLineStructure["command"][0] not in (None, "None", ""):
           foundObjects = self.findObjects(currentLineStructure["command"], objects)

           self.addTag(yOnTextBox, currentLineStructure["command"][1][0],
                        currentLineStructure["command"][1][1] + 1, "error")

           asList = list(foundObjects.keys())
           for keyNum in range(0, len(asList)):
              key = asList[keyNum]

              adder = 1
              if key == asList[-1]: adder = 0
              self.removeTag(yOnTextBox, foundObjects[key][0][0],
                          foundObjects[key][0][1] + 1 + adder,
                          None)

              self.addTag(yOnTextBox, foundObjects[key][0][0],
                          foundObjects[key][0][1] + 1,
                          foundObjects[key][1])

              if foundObjects[key][1] == "process":
                 hasValidCommand = True

                 commandNum      = len(self.__objectMaster.returnParamsForProcess(currentLineStructure["command"][0]))
                 for num in range(0, commandNum):
                     commandParams.append("variable")


        if   currentLineStructure["("] != -1 and currentLineStructure[")"] == -1:
             self.addTag(yOnTextBox, currentLineStructure["("],
                                     currentLineStructure["("] + 1,
                                     "error")
        elif currentLineStructure["("] == -1 and currentLineStructure[")"] != -1:
             self.addTag(yOnTextBox, currentLineStructure[")"],
                                     currentLineStructure[")"] + 1,
                                     "error")
        elif currentLineStructure["("] != -1 and currentLineStructure[")"] != -1:
            self.addTag(yOnTextBox, currentLineStructure[")"],
                        currentLineStructure[")"] + 1,
                        "bracket")

            self.addTag(yOnTextBox, currentLineStructure["("],
                        currentLineStructure["("] + 1,
                        "bracket")

        if  currentLineStructure["("] != -1 and currentLineStructure["param#1"] not in [None, "None", ""]\
        and hasValidCommand == True:
            paramColoring = self.checkParams(currentLineStructure["param#1"],
                                               currentLineStructure["param#2"],
                                               currentLineStructure["param#3"],
                                               currentLineStructure, currentLineStructure["command"][0])

            for item in paramColoring:
                if item[1][0] != -1:
                   self.removeTag(yOnTextBox, item[1][0],
                                              item[1][1] + 1,
                                              None)
                   self.addTag(   yOnTextBox, item[1][0],
                                              item[1][1] + 1,
                                              item[0])

        for ind in range(0, len(currentLineStructure["commas"])):
            if ind > len(commandParams) - 2:
               self.addTag(yOnTextBox, currentLineStructure["commas"][ind],
                                       currentLineStructure["commas"][ind] + 1,
                                       "error")

        if yOnTextBox == self.__cursorPoz[0]:
           currentWord = self.getCurrentWord(text[lineNum])
           self.updateLineDisplay(currentLineStructure)
           self.__updateListBoxFromCodeEditor(currentWord, currentLineStructure, commandParams, line)


    def __updateListBoxFromCodeEditor(self, currentWord, lineStructure, paramTypes, line):
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
                cursorIn = "param#1"

                for commaNum in range(0, len(lineStructure["commas"])):
                    if self.__cursorPoz[1] > lineStructure["commas"][commaNum]:
                        param = commaNum + 1
                    else:
                        cursorIn = "param#" + str(param)
                        break

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
                  thisParam = params[paramNum]

                  paramType = params[paramNum]
                  dimension = lineStructure[cursorIn][1]

                  mustHave = True
                  if paramType[0] == "{":
                      paramType = paramType[1:-1]
                      mustHave = False

                  foundIt, paramTypeAndDimension = self.__checkIfParamIsOK(paramType, thisParam,
                                                                            ioMethod, None,
                                                                            dimension, mustHave)
                  if foundIt == True:
                     listType = paramTypeAndDimension[0]
                  else:
                     listType = paramType.split("|")[0]



        wordsForList.sort()
        print(listType, lineStructure)
        # print(cursorIn, currentWord, lineStructure)


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
            sendBack["start"] = self.__findWahWah(word, lineNum,
                                                   "up", text, currentLineStructure["level"], "-", 0, None,
                                                   currentLineStructure)

            if sendBack["start"] != False:
                ender = "end-"+word.split("-")[0]
                break

        if ender != None:
            sendBack["end"] = self.__findWahWah(ender, lineNum,
                                                   "down", text, currentLineStructure["level"], None, None, None,
                                                   currentLineStructure)

        return sendBack


    def __foundAllRelatedForCaseDefault(self, currentLineStructure, lineNum, text, isDefault):
        sendBack = {
            "select"         : False,
            "end-select"     : False,
            "numOfDefaults"  : 0,
            "numOfCases"     : 0,
            "defaults"        : [],
            "cases"          : []
        }

        sendBack["select"] = self.__findWahWah("select", lineNum,
                             "up", text, currentLineStructure["level"], "-", 0, None, currentLineStructure)

        if sendBack["select"] != False:
           sendBack["end-select"] = self.__findWahWah("end-select", lineNum,
                               "down", text, currentLineStructure["level"], None, None, None, currentLineStructure)

        if sendBack["end-select"] != False:
           sendBack["cases"] = self.__listAllCommandFromTo("case", text, currentLineStructure["level"],
                              sendBack["select"][0], sendBack["end-select"][0] + 1
                                                          )
           sendBack["defaults"] = self.__listAllCommandFromTo("default", text, currentLineStructure["level"],
                              sendBack["select"][0], sendBack["end-select"][0] + 1
                                                          )
           sendBack["numOfCases"] = len(sendBack["cases"])
           sendBack["numOfDefaults"] = len(sendBack["defaults"])

        return sendBack

    def __listAllCommandFromTo(self, searchWord, text, level, fromY, toY):
        sendBack = []

        commandList = [searchWord]
        commandList.extend(self.__syntaxList[searchWord].alias)

        for lineNum in range(fromY, toY):
            lineStruct = self.getLineStructure(lineNum, text, True)

            if lineStruct["command"][0] in commandList and (lineStruct["level"] == level or level == None):
                sendBack.append(lineStruct)

        return sendBack

    def __findWahWah(self, key, startPoz, direction, text, level, splitBy, splitPoz, forceEndPoz, currentLineStructure):

        send = False
        searchItems = [key]
        searchItems.extend(self.__syntaxList[searchItems[0]].alias)


        for item in searchItems:
            if send != False: return send

            send = self.__finderLoop(currentLineStructure, startPoz, text, direction, item,
                              level - 1, splitBy, splitPoz, forceEndPoz, False)

        return False



    def __findEnd(self, currentLineStructure, lineNum, text):
        endCommand = "end-" + currentLineStructure["command"][0].split("-")[0]

        return self.__finderLoop(currentLineStructure,
                                 lineNum, text, "down", endCommand,
                                 currentLineStructure["level"],
                                 None, None, None, False
                                 )

    def __findStart(self, currentLineStructure, lineNum, text):
        startCommand = currentLineStructure["command"][0].split("-")[1]

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
            if d in command:
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
            paramNum = len(self.__objectMaster.returnParamsForProcess(command))
            for num in range(0, paramNum):
                params.append("variable")
                ioMethod.append("read")

        return params, ioMethod

    def __checkIfParamIsOK(self, paramType, param, ioMethod, returnBack, dimension, mustHave):
        foundIt = False
        noneList   = ["None", None, ""]

        sendBack   = False
        if returnBack == None:
           returnBack  = []
           sendBack    = True

        paramTypeList = paramType.split("|")

        for pType in paramTypeList:
            if foundIt == True: break

            if param in noneList: continue

            if pType == "variable":
                writable, readOnly, all, nonSystem = self.__virtualMemory.returnVariablesForBank(self.__currentBank)

                if param in all:
                    foundIt = True

                    if ioMethod == "write" and (param in readOnly):
                       returnBack.append(["error", dimension])
                    else:
                       returnBack.append(["variable", dimension])
                    break
            elif pType == "number":
                import re

                numberRegexes = {"dec": r'\d{1,3}',
                                 "bin": r'[b|%][0-1]{1,8}',
                                 "hex": r'[$|z|h][0-9a-f]{1,2}'
                                 }

                for key in numberRegexes.keys():
                    test = re.findall(numberRegexes[key], param)
                    if len(test) > 0:
                       foundIt = True
                       returnBack.append(["number", dimension])


            elif pType == "array":
                if foundIt == True: break

                writable, readOnly, all = self.__virtualMemory.returnArraysOnValidity(self.__currentBank)
                if param in all:
                    foundIt = True

                    if ioMethod == "write" and (param in readOnly):
                       returnBack.append(["error", dimension])
                    else:
                       returnBack.append(["variable", dimension])
                    break

            elif pType == "string" or "stringConst":
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

        # TODO should add the other types!

        if foundIt == False:
           if mustHave == False and param in noneList:
              returnBack.append(["missing", dimension])
           else:
              returnBack.append(["error", dimension])

        if sendBack: return foundIt, returnBack[-1]

    def checkParams(self, param1, param2, param3, currentLineStructure, command):

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
                 self.__checkIfParamIsOK(paramType, param,
                                         ioMethod, returnBack,
                                         ppp[paramNum][1], mustHave)

        #print("fuck", params, returnBack)

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

        elif command == "select" or command in self.__syntaxList["select"].alias:
            if returnBack[0][0] == "stringConst" and\
               self.convertStringNumToNumber(self.__constants[param1[0]]["value"]) not in [0, 1]:
               returnBack[0][0] = "error"
            elif returnBack[0][0] == "number" and self.convertStringNumToNumber(param1[0]) not in [0, 1]:
               returnBack[0][0] = "error"

        return returnBack

    def convertStringNumToNumber(self, num):
        if type(num) == int  : return num
        if type(num) == float: return int(num)

        binSigns = self.__config.getValueByKey("validBinarySigns").split(" ")
        hexSigns = self.__config.getValueByKey("validHexSigns").split(" ")

        mode = 10
        if   num[0] in binSigns:
             mode = 2
             num  = "0b" + num[1:]
        elif num[0] in hexSigns:
             mode = 16
             num  = "0x" + num[1:]

        print(num, mode)

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
                    ], self.__objectMaster.returnOcjectOrProcess(currentPossibleObject)
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

        startPoz = self.__cursorPoz[1]
        endPoz   = startPoz

        try:
            for num in range(startPoz-1, -1, -1):
                if line[num] == " ":
                   endPoz = num + 1
                   break
        except:
            pass

        return line[endPoz:startPoz]


    def getLineStructure(self, lineNum, text, checkLevel):
        if lineNum == None: lineNum = self.__cursorPoz[0]-1

        if text == None:
           text = self.__codeBox.get(0.0, END).replace("\t", " ").split("\n")

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
            "commas": []
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
        for key in lineStructure:
            if key in self.__words:
               item = self.__codeEditoritems[key]

               if type(item)  == Label:
                  item.config(text = str(lineStructure[key]))

               elif type(item) == list:
                  if type(item[0]) == StringVar:
                     item[0].set(lineStructure[key][0])

        self.__checkEditorItems()

    def __checkEditorItems(self):
        pass

    def addTag(self, Y, X1, X2, tag):
        self.__codeBox.tag_add(tag, str(Y) + "." + str(X1) , str(Y) + "." + str(X2))

    def removeTag(self, Y, X1, X2, tags):
        if tags == None:
            for tag in self.__codeBox.tag_names():
                self.__codeBox.tag_remove(tag,
                                          str(Y) + "." + str(X1),
                                          str(Y) + "." + str(X2)
                                          )
        elif tags == "nonError":
            for tag in self.__codeBox.tag_names():
                if tag == "error":
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
               (charNum == 0 or line[charNum-1] in (" ", ")", "\t")): return charNum

            if line[charNum] == "(": level += 1
            if line[charNum] == ")": level -= 1
            if level < 0           : level  = 0

        return(len(line))

    def __counterEnded(self):
        self.__loader.virtualMemory.codes[self.__currentBank][self.__currentSection].changed = True
        self.__setTinting(self.__cursorPoz[0])

    def clicked(self, event):
        self.__counterEnded2()

    def __counterEnded2(self):
        self.setCurzorPoz()
        self.__setTinting("whole")

    def __keyPressed(self, event):
        if (event.keysym == "Control_L" or event.keysym == "Control_R"):
            self.__ctrl = True

    def __keyReleased(self, event):
        self.__lastButton = event.keysym
        self.__counter   = 25
        self.__counter2   = 250

        self.setCurzorPoz()

        if (event.keysym == "Control_L" or event.keysym == "Control_R"):
            self.__ctrl = False

    def setCurzorPoz(self):
        __cursorPoz = self.__codeBox.index(INSERT)
        self.__cursorPoz = [int(__cursorPoz.split(".")[0]), int(__cursorPoz.split(".")[1])]

    def __mouseWheel(self, event):
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

        self.__codeBox.tag_config("comment",
                                  foreground=self.__loader.colorPalettes.getColor("comment"),
                                  font=self.__italicFont)

        self.__codeBox.tag_config("object",
                                  foreground=self.__loader.colorPalettes.getColor("object"),
                                  font=self.__boldFont)

        self.__codeBox.tag_config("variable",
                                  foreground=self.__loader.colorPalettes.getColor("variable"),
                                  font=self.__boldUnderlinedFont)

        self.__codeBox.tag_config("array",
                                  foreground=self.__loader.colorPalettes.getColor("array"),
                                  font=self.__boldUnderlinedFont)

        self.__codeBox.tag_config("number",
                                  foreground=self.__loader.colorPalettes.getColor("number"),
                                  font=self.__italicFont)

       # self.__codeBox.tag_config("process",
       #                           foreground=self.__loader.colorPalettes.getColor("process"),
       #                           font=self.__boldFont)

        self.__codeBox.tag_config("highLight", background=self.__loader.colorPalettes.getColor("highLight"))

        self.__codeBox.tag_config("command",
                                  foreground=self.__loader.colorPalettes.getColor("command"),
                                  font=self.__boldFont)

        self.__codeBox.tag_config("process",
                                  foreground=self.__loader.colorPalettes.getColor("command"),
                                  font=self.__boldFont)

        self.__codeBox.tag_config("commandBack", background=self.__loader.colorPalettes.getColor("commandBack"),
                                                 foreground=self.__loader.colorPalettes.getColor("command"),
                                                 font = self.__boldFont)

        self.__codeBox.tag_config("error", background=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                                           foreground=self.__loader.colorPalettes.getColor("boxFontUnSaved"))

        self.__codeBox.tag_config("string", background=self.__loader.colorPalettes.getColor("stringBack"),
                                            foreground=self.__loader.colorPalettes.getColor("stringFont")
                                           )

        self.__codeBox.tag_config("stringConst", background=self.__loader.colorPalettes.getColor("constStringBack"),
                                            foreground=self.__loader.colorPalettes.getColor("constStringFont")
                                           )

        self.__codeBox.tag_config("bracket",
                                  foreground=self.__loader.colorPalettes.getColor("bracket"),
                                  font=self.__boldFont)


        self.__codeBox.config(font=self.__normalFont)