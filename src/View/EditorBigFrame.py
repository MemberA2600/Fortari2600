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

        self.__focused = None
        self.__screenSize = self.__loader.screenSize
        self.__counter    = 0
        self.__counter2    = 0

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

        self.__codeBox = scrolledtext.ScrolledText(self.__mainFrame, width=999999, height=9999999, wrap=WORD)
        self.__codeBox.pack(fill=BOTH)
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

        self.__loadFromMemory(self.__currentBank, self.__currentSection)

        self.__validKeys = [
            "enter", "leave", "overscan", "vblank", "subroutines"
        ]

        self.__getFont()
        sizes = (0.20, 0.60, 0.20)

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
        text = self.__codeBox.get(0.0, END).split("\n")
        if self.__lastButton == "Enter": mode = "whole"

        objectList, processList = self.__objectMaster.getObjectsAndProcessesValidForGlobalAndBank()
        objectList.append("game")

        if mode == "whole":
           for num in range (1, len(text)+1):
               self.__lineTinting(num, text[num-1], objectList, processList)
        else:
            self.__lineTinting(mode, text[mode-1], objectList, processList)

        for bracket in (")", "("):
            if bracket in text[self.__cursorPoz[0]-1][self.__cursorPoz[1]-1:self.__cursorPoz[1]+1]:
               index = text[self.__cursorPoz[0]-1][self.__cursorPoz[1]-1:self.__cursorPoz[1]+1].index(bracket)
               #nextBracketPoz = self.__findBracketPairs(bracket, self.__cursorPoz[1]-1+index, self.__cursorPoz[0]-1, text)

               error = True
               bracketPairs = self.__getBracketPairs(text)
               thePairs = []

               for pair in bracketPairs:
                   if str(self.__cursorPoz[0]) + "." + str(self.__cursorPoz[1] - (1-index)) in pair:
                       if len(pair) == 2:
                          thePairs = pair
                          error    = False
                       break

               if error != True:
                   theY1  = int(thePairs[0].split(".")[0])
                   theX1  = int(thePairs[0].split(".")[1])
                   theY2  = int(thePairs[1].split(".")[0])
                   theX2  = int(thePairs[1].split(".")[1])

                   self.removeTag(theY1, theX1, theX1+1, "error")
                   self.removeTag(theY2, theX2, theX2+1, "error")

                   self.__codeBox.tag_add("bracketSelected",     str(theY1) + "." + str(theX1),
                                                                 str(theY1) + "." + str(theX1 + 1))

                   self.__codeBox.tag_add("bracketSelected",     str(theY2) + "." + str(theX2),
                                                                 str(theY2) + "." + str(theX2 + 1))
               else:

                   poz = [
                       str(self.__cursorPoz[0]), str(self.__cursorPoz[1] - (1-index)),
                       str(self.__cursorPoz[1] - (1-index) + 1)
                   ]

                   self.removeTag(poz[0], poz[1], poz[2], None)
                   self.__codeBox.tag_add("error",     str(poz[0]) + "." + str(poz[1]),
                                                       str(poz[0]) + "." + str(poz[2]))

        delimiterPairs = self.getStringDelimiterPair(text)

        for pair in delimiterPairs:

            if len(pair) == 1:
                poz = [
                    pair[0].split(".")[0], pair[0].split(".")[1],
                ]

                self.removeTag(poz[0], poz[1], str(int(poz[1]) + 1), None)
                self.__codeBox.tag_add("error", str(poz[0]) + "." + str(poz[1]),
                                       str(poz[0]) + "." + str(int(poz[1]) + 1))
            else:
                theY1 = int(pair[0].split(".")[0])
                theX1 = int(pair[0].split(".")[1])
                theY2 = int(pair[1].split(".")[0])
                theX2 = int(pair[1].split(".")[1])

                self.removeTag(theY1, theX1, theX1 + 1, "error")
                self.removeTag(theY2, theX2, theX2 + 1, "error")

                self.__codeBox.tag_add("string", str(theY1) + "." + str(theX1),
                                       str(theY2) + "." + str(theX2 + 1))

        commandPairs = self.getCommandPairs(text)

        line = text[self.__cursorPoz[0]-1].replace("\t", " ")
        xxx = self.getFirstValidDelimiterPoz(line)

        words = line[:xxx].split(" ")
        index = 0

        for word in words:
            found = False
            if commandPairs == None: break

            for compWord in commandPairs.keys():
                if found: break

                try:
                    compWord2 = compWord
                    if compWord2.endswith("("): compWord2 = compWord2[:-1]
                    commandText, commandEndText, commandLen, commandVal = self.commandPrepare(compWord2)
                except Exception as e:
                    #print(str(e))
                    continue

                if commandEndText == None: break
                if (self.__currentSection in commandVal.sectionsAllowed) == False: break

                theList = commandPairs[compWord]
                # wordStartPoz = str(self.__cursorPoz[0]) + "." + str(index)
                # wordEndPoz = str(self.__cursorPoz[0]) + "." + str(index + len(word) + 1)

                if word in (commandText, commandEndText):
                   for pair in theList:
                       if len(pair) > 1:
                           theY1    = int(pair[0].split(".")[0])
                           theY2    = int(pair[1].split(".")[0])

                           theX1    = int(pair[0].split(".")[1])
                           theX2    = int(pair[1].split(".")[1])

                           theX1End = int(pair[0].split(".")[2])
                           theX2End = int(pair[1].split(".")[2])

                           if (theY1 == self.__cursorPoz[0]              and\
                                       self.__cursorPoz[1] >= theX1      and \
                                       self.__cursorPoz[1] <= theX1End   and \
                                       word == commandText)\
                               or (theY2 == self.__cursorPoz[0]          and\
                                       self.__cursorPoz[1] >= theX2      and \
                                       self.__cursorPoz[1] <= theX2End   and \
                                       word == commandEndText):
                                       found = True

                                       if  commandText.endswith("(")\
                                       and word == commandText: theX1End -= 1

                                       self.removeTag(theY1, theX1, theX1End, None)
                                       self.removeTag(theY2, theX2, theX2End, None)

                                       self.__codeBox.tag_add("commandBack", str(theY1) + "." + str(theX1),
                                                                                str(theY1) + "." + str(theX1End + 1))
                                       self.__codeBox.tag_add("commandBack", str(theY2) + "." + str(theX2),
                                                                                str(theY2) + "." + str(theX2End + 1))

                       elif len(pair) == 1:
                           theY1    = int(pair[0].split(".")[0])
                           theX1    = int(pair[0].split(".")[1])
                           theX1End = int(pair[0].split(".")[2])
                           if commandText.endswith("(") \
                                   and word == commandText: theX1End -= 1

                           self.removeTag(theY1, theX1, theX1End, None)
                           found = True
                           self.__codeBox.tag_add("error", str(theY1) + "." + str(theX1),
                                                   str(theY1) + "." + str(theX1End + 1))
            index += (len(word) + 1)

        try:
            self.__setListBoxOnTheRight(text)
        except Exception as e:
           # print(str(e))
           pass

    def __setListBoxOnTheRight(self, text):
        selector = 0
        try:
            selector = self.__listBoxOnTheRight.curselection()[0]
        except:
            pass

        self.__listBoxOnTheRight.select_clear(0, END)
        self.__listBoxOnTheRight.delete(0, END)

        line = text[self.__cursorPoz[0]-1]
        xxx = self.getFirstValidDelimiterPoz(line)
        line = line[:xxx]

        words = line.split(" ")

        index = 0
        currentWord = ""

        for word in words:
            endPoz = index + len(word)
            if self.__cursorPoz[1] == endPoz:
                currentWord = word
                break
            else:
                index += endPoz + 1

        if currentWord == "": return

        forTheList = {}

        typ = None

        delimiter = ""
        for d in self.__config.getValueByKey("validObjDelimiters"):
            if d in currentWord:
               delimiter = d
               typ = "object"
               break

        if typ == None:
            for command in self.__syntaxList.keys():
                if command.startswith(currentWord): forTheList[command] = "command"

            # Object stuff are callable with call / exec, while using variables depends on if the command writes or reads.

        elif typ == "object":
            if currentWord[-1] == delimiter:
                lastOne = currentWord.split(delimiter)[-2]

                if lastOne.upper() == "game".upper():
                    firstLevel = self.__objectMaster.objects.keys()
                    for item in firstLevel:
                        if item.startswith("bank") == False:
                            forTheList[item] = "object"
                else:
                    nextLevel = self.__objectMaster.returnNextLevel(lastOne)
                    for item in nextLevel:
                        askName = item
                        if "(" in item:
                            askName = item.split("(")[0]

                        forTheList[askName] = self.__objectMaster.returnOcjectOrProcess(item)


            """
            writable, readOnly, all = self.__virtualMemory.returnVariablesForBank(self.__currentBank)
            for var in writable:
                if var.startswith(currentWord): forTheList[var] = "variable"
            """

        keys = list(forTheList.keys())
        keys.sort()

        for item in keys:
            self.__listBoxOnTheRight.insert(END, item)
            self.__listBoxOnTheRight.itemconfig(END, fg = self.__loader.colorPalettes.getColor(forTheList[item]))

        if len(list(forTheList.keys())) - 1 < selector: selector = len(list(forTheList.keys())) - 1
        self.__listBoxOnTheRight.select_set(selector)
        self.__listBoxOnTheRight.yview(selector)

    def commandPrepare(self, command):
        commandVal = self.__loader.syntaxList[command]
        commandText = command
        commandLen = len(command)
        commandEndText = None

        if commandVal.endNeeded == True:
            commandEndText = "end-" + command.split("-")[0]

        if commandVal.bracketNeeded == True:
            commandText += "("
            commandLen += 1

        return commandText, commandEndText, commandLen, commandVal

    def getCommandPairs(self, text):
        pairs = {}
        commandStack = []

        for theY in range(0, len(text)):
            line = text[theY]
            xxx = self.getFirstValidDelimiterPoz(line)
            line = line[:xxx]

            if line.startswith("*") or line.startswith("#"): continue
            lenght = len(line)
            delimiterLen = self.getFirstValidDelimiterPoz(line)
            if delimiterLen != None:
                lenght = delimiterLen

            words = line[:lenght].replace("\t", " ").split(" ")
            index = 0
            for word in words:
                found = False
                for command in self.__loader.syntaxList.keys():
                    if found == True: break
                    #print(command)

                    if command in line:
                        commandText, commandEndText, commandLen, commandVal = self.commandPrepare(command)

                        if commandEndText != None:
                            compareText = commandText
                            if commandVal.bracketNeeded == True and compareText.endswith("(") == False:
                                compareText += "("


                            if word == compareText:
                               commandStack.append(commandText)
                               if commandText not in pairs.keys():
                                  pairs[commandText] = []
                               pairs[commandText].append([
                                   str(theY + 1) + "." + str(index) + "." + str(index + len(word))

                               ])
                               found = True

                            elif word == commandEndText:
                                lastCommand = commandStack[-1]
                                commandStack.pop(-1)
                                for pairNum in range(len(pairs[lastCommand])-1, -1, -1):
                                    if len(pairs[lastCommand][pairNum]) == 1:
                                       pairs[lastCommand][pairNum].append(
                                           str(theY + 1) + "." + str(index) + "." + str(index + len(word))
                                       )
                                       found = True
                                       break

                index += 1 + len(word)
        # print(pairs)
        return pairs

    def getStringDelimiterPair(self, text):
        pairs = []
        open = True
        delimiters = self.__loader.config.getValueByKey("validStringDelimiters").split(" ")

        validDelimiter = None

        for theY in range(0, len(text)):
            line = text[theY]
            if line.startswith("*") or line.startswith("#"): continue

            lenght = len(line)
            delimiterLen = self.getFirstValidDelimiterPoz(line)
            if delimiterLen != None:
               lenght = delimiterLen

            for theX in range(0, lenght):
               if line[theX] in delimiters:
                  if open == True:
                     open = False
                     validDelimiter = line[theX]
                     pairs.append(
                         [
                             str(theY + 1) + "." + str(theX)
                         ]
                     )
                  elif open == False and line[theX] == validDelimiter:
                      validDelimiter = None
                      open = True
                      pairs[-1].append(str(theY + 1) + "." + str(theX))

        return pairs


    def removeTag(self, Y, X1, X2, tags):
        if tags == None:
            for tag in self.__codeBox.tag_names():
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

    def __getBracketPairs(self, text):
        pairs = []
        level = 0

        for theY in range(0, len(text)):
            line = text[theY]
            xxx  = self.getFirstValidDelimiterPoz(line)
            line = line[:xxx]

            if line.startswith("*") or line.startswith("#"): continue

            lenght = len(line)
            delimiterLen = self.getFirstValidDelimiterPoz(line)
            if delimiterLen != None:
               lenght = delimiterLen

            for theX in range(0, lenght):
                if line[theX] == "(":
                   pairs.append(
                       [
                            str(theY + 1) + "." + str(theX)
                       ]
                   )
                   level += 1
                elif line[theX] == ")":
                    if level > 0:
                       index = 0-level
                       pairs[index].append(str(theY + 1) + "." + str(theX))
                       level -= 1

        return pairs

    def __lineTinting(self, lineNum, line, objectList, processList):

        for tag in self.__codeBox.tag_names():
            self.__codeBox.tag_remove(tag,
                                      str(lineNum)+".0",
                                      str(lineNum) + "." + str(len(line)+1)
                                      )

        if line.startswith("*") or line.startswith("#"):
           self.__codeBox.tag_add("comment", str(lineNum) + ".0", str(lineNum) + "." + str(len(line)))

        else:
            xxx = self.getFirstValidDelimiterPoz(line)
            if xxx != None:
               self.__codeBox.tag_add("comment", str(lineNum) + "."+ str(xxx), str(lineNum) + "." + str(len(line)))

            for key in self.__syntaxList.keys():
                command = self.__syntaxList[key]

                theString = key
                if command.bracketNeeded == True:
                   theString += "("

                for startIndex in range(0, len(line[:xxx]) - len(theString)+1):
                    if line[startIndex:startIndex+len(theString)] == theString:
                        endIndex = startIndex + len(theString)
                        if command.bracketNeeded == True: endIndex -= 1

                        if self.__currentSection in command.sectionsAllowed:
                            self.__codeBox.tag_add("command", str(lineNum) + "." + str(startIndex),
                                               str(lineNum) + "." + str(endIndex))
                        else:
                            self.__codeBox.tag_add("error", str(lineNum) + "." + str(startIndex),
                                               str(lineNum) + "." + str(endIndex))

            for index in range(0, len(line[:xxx])):
                if line[index] in ("(", ")"):
                   self.__codeBox.tag_add("bracket", str(lineNum) + "." + str(index),
                                          str(lineNum) + "." + str(index+1))


            words = line[:xxx].split(" ")
            index = 0
            for word in words:
                delimiter = "%"
                foundOne = False
                for d in self.__config.getValueByKey("validObjDelimiters").split(" "):
                    if d in word:
                       delimiter = d
                       foundOne  = True
                       break

                if foundOne == True:
                   subIndex = 0
                   subLine  = word.split(delimiter)

                   for subWord in subLine:
                       if subWord in objectList:
                           self.__codeBox.tag_add("object", str(lineNum) + "." + str(subIndex + index),
                                                            str(lineNum) + "." + str(subIndex + index + len(subWord)))
                       elif subWord in processList:
                           self.__codeBox.tag_add("process", str(lineNum) + "." + str(subIndex + index),
                                                             str(lineNum) + "." + str(subIndex + index + len(subWord)))

                       subIndex += (len(subWord) + 1)

                index += (len(word) + 1)

            listOfNumbers = self.findNumbersInALine(line, lineNum)
            for pair in listOfNumbers:
                X1 = int(pair[0].split(".")[1])
                X2 = int(pair[1].split(".")[1])

                self.removeTag(lineNum, X1, X2, None)
                self.__codeBox.tag_add("number", pair[0], pair[1])

            writable, readOnly, all = self.__virtualMemory.returnVariablesForBank(self.__currentBank)

            for variable in all:
                for startIndex in range(0, len(line[:xxx])-len(variable)+1):
                    endIndex = startIndex + len(variable)

                    if line[startIndex:endIndex].upper() == variable.upper():
                       self.removeTag(lineNum, startIndex, endIndex+1, None)
                       self.__codeBox.tag_add("variable", str(lineNum) + "." + str(startIndex),
                                         str(lineNum) + "." + str(endIndex))

            for array in self.__virtualMemory.arrays.keys():
                for startIndex in range(0, len(line[:xxx])-len(array)+1):
                    endIndex = startIndex + len(array)

                    if line[startIndex:endIndex].upper() == array.upper():
                       self.removeTag(lineNum, startIndex, endIndex+1, None)
                       self.__codeBox.tag_add("array", str(lineNum) + "." + str(startIndex),
                                         str(lineNum) + "." + str(endIndex))

        if self.__highLightWord != None:
            highLightPositions = self.stringInLine(line, self.__highLightWord)
            for dim in highLightPositions:
                self.__codeBox.tag_add("highLight",
                                       str(lineNum) + "." + str(dim[0]),
                                       str(lineNum) + "." + str(dim[1])
                                       )

    def stringInLine(self, line, word):
        positions = []

        for startIndex in range(0, len(line)-len(word)):
            tempW = line[startIndex:startIndex+len(word)]
            if self.__highLightIgnoreCase == True:
               if tempW.upper() == word.upper(): positions.append((startIndex, startIndex+len(word)))
            else:
               if tempW == word: positions.append((startIndex, startIndex + len(word)))

        return(positions)

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

        self.__codeBox.tag_config("process",
                                  foreground=self.__loader.colorPalettes.getColor("process"),
                                  font=self.__boldFont)

        self.__codeBox.tag_config("highLight", background=self.__loader.colorPalettes.getColor("highLight"))

        self.__codeBox.tag_config("command",
                                  foreground=self.__loader.colorPalettes.getColor("command"),
                                  font=self.__boldFont)

        self.__codeBox.tag_config("commandBack", background=self.__loader.colorPalettes.getColor("commandBack"),
                                                 foreground=self.__loader.colorPalettes.getColor("command"),
                                                 font = self.__boldFont)

        self.__codeBox.tag_config("bracketSelected", background=self.__loader.colorPalettes.getColor("bracketSelected"))
        self.__codeBox.tag_config("error", background=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                                           foreground=self.__loader.colorPalettes.getColor("boxFontUnSaved"))

        self.__codeBox.tag_config("string", background=self.__loader.colorPalettes.getColor("stringBack"),
                                            foreground=self.__loader.colorPalettes.getColor("stringFont"),
                                           )

        self.__codeBox.tag_config("bracket",
                                  foreground=self.__loader.colorPalettes.getColor("bracket"),
                                  font=self.__boldFont)


        self.__codeBox.config(font=self.__normalFont)

    def findNumbersInALine(self, line, lineNum):
        import re

        numberPozisions = []
        numberRegexes = {"dec": r'\d{1,3}',
                         "bin": r'[b|%][0-1]{1,8}',
                         "hex": r'[$|z|h][0-9a-f]{1,2}'
                         }

        listOfRegex  = [[],[],[]]

        listOfRegex[0] = re.findall(numberRegexes["dec"], line, re.IGNORECASE)
        listOfRegex[1] = re.findall(numberRegexes["bin"], line, re.IGNORECASE)
        listOfRegex[2] = re.findall(numberRegexes["hex"], line, re.IGNORECASE)

        xxx = self.getFirstValidDelimiterPoz(line)
        line = line[:xxx]

        for listNum in range(0, 3):
            for item in listOfRegex[listNum]:
                for startIndex in range(0, len(line) - len(item) +1):
                    endIndex = startIndex + len(item)

                    if line[startIndex:endIndex].upper() == item.upper():

                       val = 256
                       if item[0] in self.__config.getValueByKey("validBinarySigns").split(" "):
                          val = int("0b" + item[1:],2)
                       elif item[0] in self.__config.getValueByKey("validHexSigns").split(" "):
                          val = int("0x" + item[1:], 16)
                       else:
                          val = int(item, 10)

                       if val > 255: continue

                       newItem = []
                       newItem.append(
                           str(lineNum) + "." + str(startIndex)
                       )
                       newItem.append(
                           str(lineNum) + "." + str(endIndex)
                       )

                       numberPozisions.append(newItem)

        return numberPozisions


    def getFirstValidDelimiterPoz(self, line):
        level = 0
        validDelimiters = self.__config.getValueByKey("validLineDelimiters").split(" ")
        for charNum in range(0, len(line)):
            if line[charNum] in validDelimiters and level == 0 and\
               (charNum == 0 or line[charNum-1] in (" ", ")", "\t")): return charNum

            if line[charNum] == "(": level += 1
            if line[charNum] == ")": level -= 1
            if level < 0     : level = 0

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
