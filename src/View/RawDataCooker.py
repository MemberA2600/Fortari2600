from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from time import sleep
from copy import deepcopy

class RawDataCooker:

    def __init__(self, loader):
        self.__loader = loader
        self.__mainWindow = self.__loader.mainWindow

        self.dead = False
        self.__changed = False
        self.__loader.stopThreads.append(self)
        self.__done = False

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
        self.__finished2 = False

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize*0.65), False, False, False)
        self.__bigFont = self.__fontManager.getFont(int(self.__fontSize*1.15), False, False, False)

        #self.__delay   = 0
        #self.__counter = 0
        self.__changed = 0

        self.__ctrl = False
        self.__middle = False
        self.__draw = 0
        self.__enabled    = False

        self.__numberOfLines = 20
        self.__Y             = 0

        self.__counterNumber = [0, None]
        self.__counterLabel  = [0, None]
        self.__labelErrors   = []
        self.__labelsInText  = {}

        self.__errorLineNum  = -1

        for num in range(0, 20):
            self.__labelErrors.append({})

        self.__sizes = [self.__screenSize[0] / 1.25, self.__screenSize[1] / 1.20 - 40]
        self.__window = SubMenu(self.__loader, "rawData", self.__sizes[0], self.__sizes[1], None, self.__addElements, 1)

        self.dead = True

    def __closeWindow(self):
        if self.__changed == True:
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

    def __collectLabels(self):
        keys = ["enter", "leave", "overscan",
                "screenroutines", "subroutines", "vblank"]

        self.__dummyFirstCompiler = None

        kernelText = self.__loader.io.loadKernelElement(
            self.__loader.virtualMemory.kernel, "main_kernel"
        )

        for line in kernelText.split("\n"):
            self.addLabelIfCan(line, "bank1", "kernel", None, None, "kernelCode")

        for bankNum in range(1, 9):
            bank = "bank" + str(bankNum)

            for section in keys:
                if section in self.__loader.virtualMemory.codes[bank].keys():
                    lines = self.__loader.virtualMemory.codes[bank][section].code.split("\n")

                    for line in lines:
                        if len(line) == 0: continue
                        if line[0] in ("#", "*", ";"): continue

                        lineStructure = self.getLineStructure(line)
                        objTextLines  = ""

                        if   self.isCommandInLineThat(lineStructure, "asm"):
                             self.addLabelIfCan(lineStructure["param#1"][0], bank, section, None, None, "asmCommand")

                        elif self.isCommandInLineThat(lineStructure, "mLoad"):
                             folder = lineStructure["param#1"][0]
                             fName  = lineStructure["param#2"][0]

                             path   = self.__loader.mainWindow.projectPath + folder + "/" + fName + ".asm"
                             f      = open(path, "r")
                             data   = f.read()
                             f.close()

                             for dLine in data.split("\n"):
                                 self.addLabelIfCan(dLine, bank, section, folder, fName, "mLoadCode")
                        else:
                            command = None
                            obj     = False

                            for c in self.__loader.syntaxList.keys():
                                if lineStructure["command"][0] == c or lineStructure["command"][0] in self.__loader.syntaxList[c].alias:
                                   command = self.__loader.syntaxList[c]
                                   break

                            if command == None:
                               objectThings = self.__loader.virtualMemory.objectMaster.returnAllAboutTheObject(lineStructure["command"][0])
                               command = self.__loader.virtualMemory.objectMaster.createFakeCommandOnObjectProcess(objectThings)
                               obj     = True

                            for paramNum in range(1, 4):
                                pNameInStruct = "param#" + str(paramNum)
                                pInCommand    = command.params[paramNum - 1]

                                if pNameInStruct in lineStructure.keys():
                                   if pInCommand.startswith("{"): pInCommand = pInCommand[1:-1]

                                   if pInCommand == "data":
                                      if obj:
                                         folder = objectThings["folder"]
                                         fName  = lineStructure[pNameInStruct][0]

                                         if self.__dummyFirstCompiler == None:
                                            from FirstCompiler import FirstCompiler

                                            self.__dummyFirstCompiler = FirstCompiler(self.__loader, 0, self.__loader.bigFrame,
                                                                                      "", False, "dummy",
                                                                                      bank, section, 0, "", True, {}
                                                                                      )

                                            #template, optionalText, objectThings = self.__dummyFirstCompiler.getObjTemplate(
                                            #                                                        lineStructure,
                                            #                                                        None, objectThings)

                                            lineStructure["fullLine"] = line
                                            lineStructure["labelsBefore"] = []
                                            lineStructure["labelsAfter"] = []
                                            lineStructure["commentsBefore"] = ""
                                            lineStructure["compiled"] = ""
                                            lineStructure["compiledBefore"] = ""
                                            lineStructure["magicNumber"] = -1
                                            lineStructure["error"] = False

                                            self.__dummyFirstCompiler.processLine(lineStructure, [lineStructure], command, objectThings)

                                            for word in self.__dummyFirstCompiler.importantWords:
                                                try:
                                                    objTextLines = lineStructure[word].split("\n")
                                                except:
                                                    objTextLines = lineStructure[word]

                                                for line in objTextLines:
                                                    self.addLabelIfCan(line, bank, section, folder, fName, "objectCommand")
                                            break

                                      else:
                                          # Currently, there is no command besides mLoad that would load data directly.

                                          for root, dirs, files in self.__loader.mainWindow.projectPath:
                                              for dir in dirs:
                                                  for subRoot, subDirs, subFiles in self.__loader.mainWindow.projectPath + "/" + dir:
                                                      for subFile in subFiles:
                                                          if "asm" in subFile and ".".join(subFile.split(".")[:-1]) == pInCommand:
                                                              subPath = self.__loader.mainWindow.projectPath + "/" + dir + "/" + subFile
                                                              f = open(subFile, "r")
                                                              subText = f.read()
                                                              f.close()

                                                              for grrrrrrrrr in subText.split("\n"):
                                                                  self.addLabelIfCan(grrrrrrrrr, bank, section, dir, subFile, "unknownCommand")

    def addLabelIfCan(self, possibleLabel, bank, section, folder, fName, where):
        if len(possibleLabel) > 0:
            replacedTags = self.replaceTags(possibleLabel, bank, section, folder, fName)

            if replacedTags[0] not in ["#", "*", " ", "\t"]:
                if possibleLabel not in self.__labelsInText.keys():
                    self.__labelsInText[possibleLabel] = self.__loader.dictionaries.getWordFromCurrentLanguage(where)

                    if possibleLabel != replacedTags:
                       self.__labelsInText[replacedTags] = self.replaceTags(self.__loader.dictionaries.getWordFromCurrentLanguage(where),
                                                                            bank, section, folder, fName)


    def isCommandInLineThat(self, line, command):
        if line["command"][0] == command or line["command"][0] in self.__loader.syntaxList[command].alias:
           return True
        return False

    def replaceTags(self, label, bank, section, folder, fName):
        label = label.replace("##", "#")

        tags = {
            "#BANK#": bank, "#SECTION#": section, "#FULL#": bank + "_" + section
        }

        if folder != None and fName != None:
           tags["#NAME#"] = bank + "_" + fName + "_" + folder

        for tag in tags:
            label = label.replace(tag, tags[tag])

        return label

    def getLineStructure(self, line):
        return self.__loader.bigFrame.getLineStructure(0, [line], False)

    def __addElements(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()
        self.__topLevelWindow.protocol('WM_DELETE_WINDOW', self.__closeWindow)

        self.__collectLabels()

        self.__errorFrame = Frame(self.__topLevelWindow,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0], height = self.__sizes[1] // 48 )

        self.__errorFrame.pack_propagate(False)
        self.__errorFrame.pack(side=TOP, anchor=N, fill=BOTH)

        self.__errorString = StringVar()
        self.__errorLabel  = Label(self.__errorFrame,
                   textvariable = self.__errorString,
                   font=self.__smallFont, fg=self.__colors.getColor("font"),
                   bg=self.__colors.getColor("window")
                   )

        self.__errorLabel.pack_propagate(False)
        self.__errorLabel.pack(side=TOP, anchor=N, fill=BOTH)

        self.__editorFrame = Frame(self.__topLevelWindow,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0], height = self.__sizes[1] // 6 * 4
                                   )
        self.__editorFrame.pack_propagate(False)
        self.__editorFrame.pack(side=TOP, anchor=N, fill=X)

        self.__errorStack = []

        self.__controllerFrame = Frame(self.__topLevelWindow,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0], height = round(self.__sizes[1] // 6 * 1.875)
                                   )
        self.__controllerFrame.pack_propagate(False)
        self.__controllerFrame.pack(side=TOP, anchor=N, fill=BOTH)

        while self.__controllerFrame.winfo_width() < 2: sleep(0.0000001)

        self.__loaderFrame = Frame(self.__controllerFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0] // 3, height = self.__controllerFrame.winfo_height())

        self.__loaderFrame.pack_propagate(False)
        self.__loaderFrame.pack(side=LEFT, anchor=W, fill=Y)

        self.__othersFrame = Frame(self.__controllerFrame,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   width=self.__sizes[0] // 3 * 2, height=self.__controllerFrame.winfo_height())

        self.__othersFrame.pack_propagate(False)
        self.__othersFrame.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__running  = 0

        t = Thread(target = self.__createEditorLines)
        t.daemon = True
        t.start()

        t = Thread(target = self.createLoaderFrame)
        t.daemon = True
        t.start()

        self.__loader.threadLooper.addToThreading(self, self.__loop, [], 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "<KeyPress-Control_L>" , self.shiftON, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "<KeyRelease-Control_L>", self.shiftOff, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "<KeyPress-Control_R>" , self.shiftON, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "<KeyRelease-Control_R>", self.shiftOff, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "Button-2>"             , self.drawMode, 1)

    def createLoaderFrame(self):
        self.__running += 1
        from VisualLoaderFrame import VisualLoaderFrame

        while self.__loaderFrame.winfo_height() < 2: sleep(0.000001)

        self.__enableThem = []
        self.__enabled    = False

        self.__visualLFrame = Frame(self.__loaderFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__loaderFrame.winfo_width(), height = self.__loaderFrame.winfo_height() // 3.5)

        self.__visualLFrame.pack_propagate(False)
        self.__visualLFrame.pack(side=TOP, anchor=N, fill=X)

        self.__rawLoader = VisualLoaderFrame(self.__loader, self.__visualLFrame, self.__loaderFrame.winfo_height() // 8,
                                                self.__normalFont, self.__smallFont, None, "Smelly_Raw_Meet",
                                                "rawName", self.__checkIfValidFileName, self.__loaderFrame.winfo_width() // 2,
                                                self.__open, self.__save)

        per = 8

        self.__numOfLinesFrame = Frame(self.__loaderFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__loaderFrame.winfo_width(), height = self.__loaderFrame.winfo_height() // per)

        self.__numOfLinesFrame.pack_propagate(False)
        self.__numOfLinesFrame.pack(side=TOP, anchor=N, fill=X)

        self.__yIndexFrame = Frame(self.__loaderFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__loaderFrame.winfo_width(), height = self.__loaderFrame.winfo_height() // per)

        self.__yIndexFrame.pack_propagate(False)
        self.__yIndexFrame.pack(side=TOP, anchor=N, fill=X)

        self.__indexButtonsFrame = Frame(self.__loaderFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__loaderFrame.winfo_width(), height = self.__loaderFrame.winfo_height() // per)

        self.__indexButtonsFrame.pack_propagate(False)
        self.__indexButtonsFrame.pack(side=TOP, anchor=N, fill=X)

        self.__numOfLinesLabelFrame = Frame(self.__numOfLinesFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__loaderFrame.winfo_width() // 2, height = self.__loaderFrame.winfo_height() // per)

        self.__numOfLinesLabelFrame.pack_propagate(False)
        self.__numOfLinesLabelFrame.pack(side=LEFT, anchor=W, fill=Y)

        self.__numOfLinesEntryFrame = Frame(self.__numOfLinesFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__loaderFrame.winfo_width() // 2, height = self.__loaderFrame.winfo_height() // per)

        self.__numOfLinesEntryFrame.pack_propagate(False)
        self.__numOfLinesEntryFrame.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__numOfLinesLabel = Label(self.__numOfLinesLabelFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   fg = self.__loader.colorPalettes.getColor("font"), justify = LEFT,
                                   font = self.__smallFont, text = self.__loader.dictionaries.getWordFromCurrentLanguage("numOfLines") + ":",
                                   height = 1)

        self.__numOfLinesLabel.pack_propagate(False)
        self.__numOfLinesLabel.pack(side=LEFT, anchor=E, fill=Y)

        self.__numOfLinesEntryVal = StringVar()
        self.__numOfLinesEntryVal.set(str(self.__numberOfLines))
        self.__numOfLinesEntry    = Entry(self.__numOfLinesEntryFrame,
                                             name="entry_numOfLines",
                                             bg=self.__colors.getColor("boxBackNormal"),
                                             fg=self.__colors.getColor("boxFontNormal"),
                                             width=9999, justify=CENTER, state=DISABLED,
                                             textvariable=self.__numOfLinesEntryVal,
                                             font=self.__normalFont
                                             )

        self.__numOfLinesEntry.pack_propagate(False)
        self.__numOfLinesEntry.pack(fill=X, side=TOP, anchor=N)

        self.__enableThem.append(self.__numOfLinesEntry)

        self.__yIndexLabelFrame = Frame(self.__yIndexFrame,
                                        bg=self.__loader.colorPalettes.getColor("window"),
                                        width=self.__loaderFrame.winfo_width() // 2,
                                        height=self.__loaderFrame.winfo_height() // per)

        self.__yIndexLabelFrame.pack_propagate(False)
        self.__yIndexLabelFrame.pack(side=LEFT, anchor=W, fill=Y)

        self.__yIndexEntryFrame = Frame(self.__yIndexFrame,
                                        bg=self.__loader.colorPalettes.getColor("window"),
                                        width=self.__loaderFrame.winfo_width() // 2,
                                        height=self.__loaderFrame.winfo_height() // per)

        self.__yIndexEntryFrame.pack_propagate(False)
        self.__yIndexEntryFrame.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__yIndexLabel = Label(self.__yIndexLabelFrame,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   fg=self.__loader.colorPalettes.getColor("font"), justify=LEFT,
                                   font=self.__smallFont,
                                   text=self.__loader.dictionaries.getWordFromCurrentLanguage("yOffset") + ":",
                                   height=1)

        self.__yIndexLabel.pack_propagate(False)
        self.__yIndexLabel.pack(side=LEFT, anchor=E, fill=Y)

        self.__yIndexEntryVal = StringVar()
        self.__yIndexEntryVal.set(str(self.__Y))
        self.__yIndexEntry = Entry(self.__yIndexEntryFrame,
                                   name="entry_yIndex",
                                   bg=self.__colors.getColor("boxBackNormal"),
                                   fg=self.__colors.getColor("boxFontNormal"),
                                   width=9999, justify=CENTER, state=DISABLED,
                                   textvariable=self.__yIndexEntryVal,
                                   font=self.__normalFont
                                   )

        self.__yIndexEntry.pack_propagate(False)
        self.__yIndexEntry.pack(fill=X, side=TOP, anchor=N)

        #self.__enableThem.append(self.__yIndexEntry)

        self.__indexButtonsFrame1 = Frame(self.__indexButtonsFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__loaderFrame.winfo_width() // 2, height = self.__loaderFrame.winfo_height() // per)

        self.__indexButtonsFrame1.pack_propagate(False)
        self.__indexButtonsFrame1.pack(side=LEFT, anchor=W, fill=Y)

        self.__indexButtonsFrame2 = Frame(self.__indexButtonsFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__loaderFrame.winfo_width() // 2, height = self.__loaderFrame.winfo_height() // per)

        self.__indexButtonsFrame2.pack_propagate(False)
        self.__indexButtonsFrame2.pack(side=LEFT, anchor=W, fill=Y)

        self.__indexButton1 = Button(self.__indexButtonsFrame1, height=self.__loaderFrame.winfo_height() // per,
                                       width=self.__loaderFrame.winfo_width() // 2,
                                       name="indexButtonUp",
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       fg=self.__loader.colorPalettes.getColor("font"),
                                       text = "<<", font = self.__normalFont,
                                       activebackground=self.__loader.colorPalettes.getColor("highLight"),
                                       state=DISABLED, command=None
                                       )
        self.__indexButton1.pack_propagate(False)
        self.__indexButton1.pack(side=TOP, anchor=N, fill=BOTH)

        self.__indexButton2 = Button(self.__indexButtonsFrame2, height=self.__loaderFrame.winfo_height() // per,
                                       width=self.__loaderFrame.winfo_width() // 2,
                                       name="indexButtonDown",
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       fg=self.__loader.colorPalettes.getColor("font"),
                                       text = ">>", font = self.__normalFont,
                                       activebackground=self.__loader.colorPalettes.getColor("highLight"),
                                       state=DISABLED, command=None
                                       )
        self.__indexButton2.pack_propagate(False)
        self.__indexButton2.pack(side=TOP, anchor=N, fill=BOTH)

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__numOfLinesEntry, "<KeyRelease>",
                                                            self.__checkEntry, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__numOfLinesEntry, "<FocusOut>",
                                                            self.__checkEntry, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__yIndexEntry, "<KeyRelease>",
                                                            self.__checkEntry, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__yIndexEntry, "<FocusOut>",
                                                            self.__checkEntry, 1)

        self.__running -= 1

    def __checkEntry(self, event):
        entry = event.widget
        name = str(entry).split(".")[-1].split("_")[-1]

        if entry.cget("state") == DISABLED: return

        maxIndex    = self.__numberOfLines - len(self.__lineData)
        if maxIndex < 0: maxIndex = 0

        valuesOnName = {
            "numOfLines": [[1, 256]     , self.__numOfLinesEntryVal],
            "yIndex"    : [[0, maxIndex], self.__yIndexEntryVal    ]
        }

        entryVal = valuesOnName[name][1]
        value    = entryVal.get()

    def __checkIfValidFileName(self, event):

        name = str(event.widget).split(".")[-1]

        value  = None
        widget = None
        if name == "rawName":
            widget = self.__rawLoader.getEntry()
            value = self.__rawLoader.getValue()


        if self.__loader.io.checkIfValidFileName(value) and (" " not in value):
            widget.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                      fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                      )

        else:
            widget.config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                                      fg=self.__loader.colorPalettes.getColor("boxFontUnSaved"),
                                      )

    def __open(self):
        pass

    def __save(self):
        pass

    def __loop(self):
        if self.__running == 0:
            try:
                if self.__enabled    == False:
                   self.__enabled     = True
                   for item in self.__enableThem:
                       item.config(state = NORMAL)


                if self.__counterNumber[0] > 0:
                   if self.__counterNumber[0] == 1:
                      self.checkNumber(self.__counterNumber[1])

                   self.__counterNumber[0] -= 1

                if self.__counterLabel[0] > 0:
                   if self.__counterLabel[0] == 1:
                      self.checkLabel(self.__counterLabel[1])

                   self.__counterLabel[0] -= 1

                if self.__numberOfLines <= len(self.__lineData):
                   self.__indexButton1.config(state = DISABLED)
                   self.__indexButton2.config(state = DISABLED)
                   self.__yIndexEntry .config(state = DISABLED)
                else:
                   self.__yIndexEntry .config(state = NORMAL)
                   if self.__Y > 0:
                      self.__indexButton1.config(state = NORMAL)
                   else:
                      self.__indexButton1.config(state = DISABLED)

                   if self.__Y < self.__numberOfLines - len(self.__lineData):
                      self.__indexButton2.config(state = NORMAL)
                   else:
                      self.__indexButton2.config(state = DISABLED)

            except Exception as e:
                print(str(e))

    def fillLineDataEnd(self):

        schema = {
            "bits": [0,0,0,0,0,0,0,0], "entry": "", "label": ""
        }

        if len(self.__allData) < self.__numberOfLines:
           for num in range(0, self.__numberOfLines - len(self.__allData)):
               self.__allData.append(deepcopy(schema))

        self.fillTheEditor()

    def fillTheEditor(self):

        for lineNum in range(self.__Y, self.__Y + len(self.__lineData)):
            lineNumOnEditor = lineNum - self.__Y
            #print(lineNumOnEditor, lineNum, len(self.__lineData), len(self.__allData))

            if lineNumOnEditor >= self.__numberOfLines:
               for bitNum in range(0, 8):
                   self.__lineData[lineNumOnEditor]["bitVals"]   [bitNum] = 0
                   self.__lineData[lineNumOnEditor]["bitButtons"][bitNum].config(
                       state = DISABLED,
                       bg = self.__colors.getColor("fontDisabled")
                   )

               self.__lineData[lineNumOnEditor]["entryVal"].set("")
               self.__lineData[lineNumOnEditor]["labelVal"].set("")

               self.__lineData[lineNumOnEditor]["entry"]     .config(state = DISABLED)
               self.__lineData[lineNumOnEditor]["labelEntry"].config(state = DISABLED)

               self.__lineData[lineNumOnEditor]["select"]    .config(state = DISABLED)

            else:
               for bitNum in range(0, 8):
                   self.__lineData[lineNumOnEditor]["bitVals"][bitNum] = self.__allData[lineNum]["bits"][bitNum]
                   if self.__lineData[lineNumOnEditor]["bitVals"][bitNum] == 1:
                      self.__lineData[lineNumOnEditor]["bitButtons"][bitNum].config(
                           state = NORMAL,
                           bg=self.__colors.getColor("boxFontNormal")
                       )

                   else:
                       self.__lineData[lineNumOnEditor]["bitButtons"][bitNum].config(
                           state=NORMAL,
                           bg=self.__colors.getColor("boxBackNormal")
                       )

                   self.__lineData[lineNumOnEditor]["entryVal"].set(self.__allData[lineNum]["entry"])
                   self.__lineData[lineNumOnEditor]["labelVal"].set(self.__allData[lineNum]["label"])

                   self.__lineData[lineNumOnEditor]["entry"]     .config(state = NORMAL)
                   self.__lineData[lineNumOnEditor]["labelEntry"].config(state = NORMAL)

                   if self.__allData[lineNum]["label"] == "":
                      self.__lineData[lineNumOnEditor]["select"].config(state=DISABLED)
                   else:
                      self.__lineData[lineNumOnEditor]["select"].config(state=NORMAL)

    def clicked(self, event):
        if self.__running > 0: return

        button = event.widget
        name  = str(button).split(".")[-1]

        if button.cget("state") == DISABLED: return

        lineNum     = int(name.split("_")[-2])
        bitNum      = int(name.split("_")[-1])

        try:
            mouseButton = int(str(event).split(" ")[3].split("=")[1])
        except:
            if self.__ctrl:
                mouseButton = 3
            else:
                mouseButton = 1

        if self.__ctrl == False and mouseButton == 3:
           return

        value = self.__lineData[lineNum]["bitVals"][bitNum]

        if self.__ctrl == False:
            value = 1 - value
        else:
            if button == 1:
               value = 1
            else:
               value = 0

        self.__lineData[lineNum]["bitVals"][bitNum] = value

        if value == 1:
           self.__lineData[lineNum]["bitButtons"][bitNum].config(bg = self.__colors.getColor("boxFontNormal"))
        else:
           self.__lineData[lineNum]["bitButtons"][bitNum].config(bg = self.__colors.getColor("boxBackNormal"))

        theNumber = self.__lineData[lineNum]["entryVal"].get()
        if theNumber.startswith("#"): vtheNumber = theNumber[1:]

        if   theNumber.startswith("%"):
             mode = "bin"
        elif theNumber.startswith("$"):
             mode = "hex"
        else:
             mode = "dec"

        binString = "0b"
        for bitNum2 in range(7, -1, -1): binString += str(self.__lineData[lineNum]["bitVals"][bitNum2])

        theNumber = int(binString, 2)

        if   mode == "bin":
             theNumber = bin(theNumber).replace("0b", "")
             theNumber = "%" + ((8 - len(theNumber)) * "0") + theNumber
        elif mode == "hex":
             theNumber = hex(theNumber).replace("0x", "")
             theNumber = "$" + ((2 - len(theNumber)) * "0") + theNumber
        else:
             theNumber = str(theNumber)

        self.__lineData[lineNum]["entryVal"].set(theNumber)
        self.__changed = True

        self.__lineData[lineNum]["entry"].config(bg=self.__colors.getColor("boxBackNormal"),
                                                 fg=self.__colors.getColor("boxFontNormal"))

        self.__allData[lineNum + self.__Y]["entry"] = value
        self.__allData[lineNum + self.__Y]["bits"] = deepcopy(self.__lineData[lineNum]["bitVals"])
        self.__changed = True

    def shiftON(self, event):
        self.__ctrl = True

    def shiftOff(self, event):
        self.__ctrl = False

    def drawMode(self, event):
        if self.__draw == 1:
           self.__draw = 0
        else:
           self.__draw = 1

    def checkNumber(self, event):
        entry = event.widget
        name  = str(entry).split(".")[-1]

        if entry.cget("state") == DISABLED: return

        self.__counterNumber =  [0, None]

        lineNum = int(name.split("_")[-1])

        value = self.__lineData[lineNum]["entryVal"].get()
        if value == "":
           entry.config(bg=self.__colors.getColor("boxBackNormal"),
                         fg=self.__colors.getColor("boxFontNormal"))
           return

        if value.startswith("#"): value = value[1:]

        try:
            if   value.startswith("%"):
                 mode = "bin"
                 value  = int(value.replace("%", "0b"), 2)
            elif value.startswith("$"):
                 mode = "hex"
                 value  = int(value.replace("$", "0x"), 16)
            else:
                 mode = "dec"
                 value  = int(value)
        except:
            entry.config(bg = self.__colors.getColor("boxBackUnSaved"),
                         fg = self.__colors.getColor("boxFontUnSaved"))
            return

        entry.config(bg=self.__colors.getColor("boxBackNormal"),
                     fg=self.__colors.getColor("boxFontNormal"))

        if   value < 0:   value = 0
        elif value > 255: value = 255

        binVal = bin(value).replace("0b", "")
        binVal = ((8-len(binVal)) * "0") + binVal

        if   mode == "dec":
             value = str(value)
        elif mode == "bin":
             value = "%" + binVal
        else:
             value = hex(value).replace("0x", "")
             if len(value) == 1: value = "0" + value
             value = "$" + value

        self.__lineData[lineNum]["entryVal"].set(str(value))
        self.__allData [lineNum + self.__Y]["entry"] = str(value)

        for bitNum in range(0, 8):
            val = binVal[7-bitNum]

            self.__lineData[lineNum]["bitVals"][bitNum] = int(val)

            colors = {
                "0": [self.__colors.getColor("boxBackNormal")],
                "1": [self.__colors.getColor("boxFontNormal")],
            }

            self.__lineData[lineNum]["bitButtons"][bitNum].config(
                   bg = colors[val])

        self.__changed = True
        entry.icursor = len(str(value))
        self.__allData [lineNum + self.__Y]["bits"] = deepcopy(self.__lineData[lineNum]["bitVals"])

    def __createEditorLines(self):
        self.__running += 1

        self.__frames   = []
        self.__lineData = []
        self.__labels   = []

        schema =  {
            "bitButtons"   : [],
            "bitVals"      : [],
            "entry"        : None,
            "entryVal"     : None,
            "labelEntry"   : None,
            "selectVal"    : None,
            "select"       : None
        }

        while self.__editorFrame.winfo_width() < 2: sleep(0.000000001)

        for lineNum in range(-1, 20):
            f = Frame(self.__editorFrame,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  width=self.__sizes[0], height=self.__editorFrame.winfo_height() // 21
                  )
            f.pack_propagate(False)
            f.pack(side=TOP, anchor=N, fill=X)

            f8bits = Frame(f,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  width=self.__sizes[0] // 10 * 2, height=self.__editorFrame.winfo_height() // 21
                  )
            f8bits.pack_propagate(False)
            f8bits.pack(side=LEFT, anchor=E, fill=Y)

            fValEntry = Frame(f,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  width=self.__sizes[0] // 10 , height=self.__editorFrame.winfo_height() // 21
                  )
            fValEntry.pack_propagate(False)
            fValEntry.pack(side=LEFT, anchor=E, fill=Y)

            fLabelEntry = Frame(f,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  width=self.__sizes[0] // 10 * 6, height=self.__editorFrame.winfo_height() // 21
                  )
            fLabelEntry.pack_propagate(False)
            fLabelEntry.pack(side=LEFT, anchor=E, fill=Y)

            fSelectEntry = Frame(f,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  width=self.__sizes[0] // 10 * 6, height=self.__editorFrame.winfo_height() // 21
                  )
            fSelectEntry.pack_propagate(False)
            fSelectEntry.pack(side=LEFT, anchor=E, fill=BOTH)

            self.__frames.append(f)
            self.__frames.append(f8bits)
            self.__frames.append(fValEntry)
            self.__frames.append(fLabelEntry)
            self.__frames.append(fSelectEntry)

            if lineNum == -1:
                l1 = Label(f8bits,
                           text = self.__loader.dictionaries.getWordFromCurrentLanguage("displayedAsBits"),
                           font=self.__smallFont, fg=self.__colors.getColor("font"),
                           bg=self.__colors.getColor("window")
                           )

                l1.pack_propagate(False)
                l1.pack(side=TOP, anchor=N, fill=BOTH)

                l2 = Label(fValEntry,
                           text = self.__loader.dictionaries.getWordFromCurrentLanguage("displayedAsVal"),
                           font=self.__smallFont, fg=self.__colors.getColor("font"),
                           bg=self.__colors.getColor("window")
                           )

                l2.pack_propagate(False)
                l2.pack(side=TOP, anchor=N, fill=BOTH)

                l3 = Label(fLabelEntry,
                           text = self.__loader.dictionaries.getWordFromCurrentLanguage("labelBefore"),
                           font=self.__smallFont, fg=self.__colors.getColor("font"),
                           bg=self.__colors.getColor("window")
                           )

                l3.pack_propagate(False)
                l3.pack(side=TOP, anchor=N, fill=BOTH)

                l4 = Label(fSelectEntry,
                           text = self.__loader.dictionaries.getWordFromCurrentLanguage("selectLabel"),
                           font=self.__smallFont, fg=self.__colors.getColor("font"),
                           bg=self.__colors.getColor("window")
                           )

                l4.pack_propagate(False)
                l4.pack(side=TOP, anchor=N, fill=BOTH)

                self.__labels = [l1, l2, l3, l4]

            else:
                self.__lineData.append(deepcopy(schema))
                self.__soundPlayer.playSound("Pong")

                for bitNum in range(0, 8):
                    bitFrame = Frame(f8bits,
                      bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                      width=(self.__sizes[0] // 10 * 2) // 8, height=self.__editorFrame.winfo_height() // 21
                      )
                    bitFrame.pack_propagate(False)
                    bitFrame.pack(side=RIGHT, anchor=W, fill=Y)

                    while bitFrame.winfo_width() < 2: sleep(0.000000000001)

                    b = Button(bitFrame, height=bitFrame.winfo_height(),
                                         width=bitFrame.winfo_width(),
                                         name="bit_" + str(lineNum) + "_" + str(bitNum),
                                         bg=self.__loader.colorPalettes.getColor("fontDisabled"),
                                         activebackground=self.__loader.colorPalettes.getColor("highLight"),
                                         state=DISABLED, command=None
                                         )
                    b.pack_propagate(False)
                    b.pack(side=TOP, anchor=N, fill=BOTH)

                    self.__frames.append(bitFrame)
                    self.__lineData[-1]["bitVals"].append(0)
                    self.__lineData[-1]["bitButtons"].append(b)

                    self.__loader.threadLooper.bindingMaster.addBinding(self, b, "<Button-1>",
                                                                        self.clicked, 1)
                    self.__loader.threadLooper.bindingMaster.addBinding(self, b, "<Button-3>",
                                                                        self.clicked, 1)

                self.__lineData[-1]["entryVal"] = StringVar()
                self.__lineData[-1]["entry"]    = Entry(fValEntry,
                                                          name="entry_" + str(lineNum),
                                                          bg=self.__colors.getColor("boxBackNormal"),
                                                          fg=self.__colors.getColor("boxFontNormal"),
                                                          width=9999, justify=CENTER, state = DISABLED,
                                                          textvariable=self.__lineData[-1]["entryVal"],
                                                          font=self.__normalFont
                                                          )

                self.__lineData[-1]["entry"].pack_propagate(False)
                self.__lineData[-1]["entry"].pack(fill=X, side=TOP, anchor=N)


                self.__lineData[-1]["labelVal"] = StringVar()
                self.__lineData[-1]["labelEntry"]    = Entry(fLabelEntry,
                                                          name="labelEntry_" + str(lineNum),
                                                          bg=self.__colors.getColor("boxBackNormal"),
                                                          fg=self.__colors.getColor("boxFontNormal"),
                                                          width=9999, justify=LEFT, state = DISABLED,
                                                          textvariable=self.__lineData[-1]["labelVal"],
                                                          font=self.__normalFont
                                                          )

                self.__lineData[-1]["labelEntry"].pack_propagate(False)
                self.__lineData[-1]["labelEntry"].pack(fill=X, side=TOP, anchor=N)

                self.__lineData[-1]["selectVal"] = IntVar()
                self.__lineData[-1]["select"] = Checkbutton(fSelectEntry, width=fSelectEntry.winfo_width(),
                                                bg=self.__colors.getColor("window"),
                                                justify=CENTER,
                                                variable=self.__lineData[-1]["selectVal"],
                                                activebackground=self.__colors.getColor("highLight"),
                                                command=None
                                                )

                self.__lineData[-1]["select"].pack_propagate(False)
                self.__lineData[-1]["select"].pack(fill=Y, side=LEFT, anchor=E)

                self.__loader.threadLooper.bindingMaster.addBinding(self, self.__lineData[-1]["entry"], "<KeyRelease>",
                                                                    self.setCounterNumber, 1)
                self.__loader.threadLooper.bindingMaster.addBinding(self, self.__lineData[-1]["entry"], "<FocusOut>",
                                                                    self.checkNumber, 1)
                self.__loader.threadLooper.bindingMaster.addBinding(self, self.__lineData[-1]["labelEntry"], "<KeyRelease>",
                                                                    self.setCounterNumber2, 1)
                self.__loader.threadLooper.bindingMaster.addBinding(self, self.__lineData[-1]["labelEntry"], "<FocusOut>",
                                                                    self.checkLabel, 1)


        self.__allData = []
        self.fillLineDataEnd()
        self.__running -= 1

    def checkLabel(self, event):
        entry = event.widget
        name  = str(entry).split(".")[-1]

        if entry.cget("state") == DISABLED: return

        self.__counterLabel =  [0, None]

        lineNum = int(name.split("_")[-1])

        value = self.__lineData[lineNum]["labelVal"].get()

        if value == "":
           self.__changed = True
           self.removeError(lineNum, "all")
           self.__allData[lineNum + self.__Y]["label"] = ""
        else:
           if len(value) > 0:
              if value in self.__labelsInText.keys():
                 self.addError("duplicateLabel", {
                     "#LABEL#": value, "#SECONDONE#": self.__loader.dictionaries.getWordFromCurrentLanguage(self.__labelsInText[value]),
                 }, lineNum)
              else:
                 self.removeError(lineNum, "duplicateLabel")

              if self.glen(value) < 8 or len(value) < 8:
                 self.addError("labelTooShort", {"#LABEL#": value} , lineNum)
              else:
                 self.removeError(lineNum, "labelTooShort")

              currentLineNum = lineNum + self.__Y

              for lNum in range(0, self.__numberOfLines):
                  if lNum == currentLineNum: continue

                  if self.__allData[lNum]["label"] == value:
                     self.addError("duplicateOnData", {"#LABEL#": value} , lineNum)
                     #self.addError("duplicateOnData", {"#LABEL#": value} , lNum)
                  else:
                     self.removeError(lineNum, "duplicateOnData")

              illegals = self.getIllegals(value)

              if len(illegals["chars"]) > 0:
                 self.addError("illegalCharacter", {"#LABEL#"   : value,
                                                    "#ILLEGALS#": ", ".join(illegals["chars"])}, lineNum)
              else:
                 self.removeError(lineNum, "illegalCharacter")

              if len(illegals["tags"]) > 0:
                 self.addError("illegalTag", {"#LABEL#": value,
                                                    "#ILLEGALS#": ", ".join(illegals["tags"])}, lineNum)
              else:
                 self.removeError(lineNum, "illegalTag")

        if wasError      == False:
           self.__changed = True
           self.__allData[lineNum + self.__Y]["label"] = value

        self.colorLabels(lineNum)

    def glen(self, label):
        tags, label = self.getTagsReturnLabelWithoutThem(label)

        #Have to set to get the name!

        l = 0

        tagValGuess = {"#BANK#": 5, "#NAME#": len(self.__rawLoader.getValue()), "#FOLDER#": 3}
        tagValGuess["#FULL#"] = sum(tagValGuess.values())

        for tag in tags:
            if tag in tagValGuess:
               l += tagValGuess[tag]

        return l + len(label)

    def getTagsReturnLabelWithoutThem(self, label):
        tagStart = -1
        tagEnd = -1
        searchForEnd = False

        tags = []

        while True:
            if searchForEnd == False:
               tagStart += 1
               if tagStart >= len(label): break

               if label[tagStart] == "#":
                  searchForEnd = True
                  tagEnd       = tagStart

            else:
               tagEnd   += 1
               if tagEnd >= len(label): break

               if label[tagEnd] == "#":
                  tags.append(label[tagStart:tagEnd + 1])
                  label        = label[:tagStart] + label[tagEnd + 1:]
                  tagStart     = -1
                  tagEnd       = -1
                  searchForEnd = False

        return tags, label

    def getIllegals(self, label):
        illegals = {
            "chars": [], "tags": []
        }

        allowedTags = ["#BANK#", "#NAME#", "#FOLDER#", "#FULL#"]

        tags, label = self.getTagsReturnLabelWithoutThem(label)

        for tag in tags:
            if tag not in allowedTags:
                illegals["tags"].append(tag)

        ranges = {
               "letters": [ord("a"), ord("z")],
               "LETTERS": [ord("A"), ord("Z")],
               "numbers": [ord("0"), ord("9")],
               "_"      : [ord("_"), ord("_")],
               "-"      : [ord("-"), ord("-")]
           }

        for c in label:
            val   = ord(c)
            found = False
            for r in ranges.keys():
                if val <= ranges[r][1] and val >= ranges[r][0]:
                   found = True
                   break

            if found == False: illegals["chars"].append(c)

        return illegals

    def colorLabels(self, lineNum):
        errorText = ""

        for num in range(0, 20):
            if self.__labelErrors[num] == {}:
               self.__lineData[num]["labelEntry"].config(bg = self.__colors.getColor("boxBackNormal"),
                                                         fg = self.__colors.getColor("boxFontNormal"))

               self.__allData[self.__Y + num]["label"] = self.__lineData[num]["labelVal"].get()
               if self.__lineData[num]["labelVal"].get() == "":
                  self.__lineData[num]["selectVal"].set(0)
                  self.__lineData[num]["select"].config(state = DISABLED)
               else:
                  self.__lineData[num]["select"].config(state = NORMAL)

            else:
               self.__lineData[num]["labelEntry"].config(bg=self.__colors.getColor("boxBackUnSaved"),
                                                         fg=self.__colors.getColor("boxFontUnSaved"))

               if lineNum == num or errorText == "":
                  key = ""
                  for key in self.__labelErrors[num].keys():
                      pass

                  self.__errorLineNum = num
                  errorText = self.__labelErrors[num][key]

        if errorText == "":
           self.__errorString.set("")
           self.__errorLabel.config(bg = self.__colors.getColor("window"))
        else:
           self.__errorString.set(errorText)
           self.__errorLabel.config(bg=self.__colors.getColor("boxBackUnSaved"),
                                    fg=self.__colors.getColor("boxFontUnSaved"))

    def addError(self, errorKey, replacers, lineNum):
        #lineNum -= 1
        txt = self.__loader.dictionaries.getWordFromCurrentLanguage(errorKey)

        for key in replacers:
            txt = txt.replace(key, replacers[key])

        if errorKey in  self.__labelErrors[lineNum].keys():
           self.removeError(lineNum, errorKey)

        self.__labelErrors[lineNum][errorKey] = txt

    def removeError(self, lineNum, errorKey):
        #lineNum -= 1

        if errorKey in ("all", "", None):
           self.__labelErrors[lineNum] = {}
        else:
           if errorKey in self.__labelErrors[lineNum]: self.__labelErrors[lineNum].pop(errorKey)

    def setCounterNumber(self, event):
        self.__counterNumber[0] = 10
        self.__counterNumber[1] = event

    def setCounterNumber2(self, event):
        self.__counterLabel[0] = 10
        self.__counterLabel[1] = event
