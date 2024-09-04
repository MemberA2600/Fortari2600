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

        self.__ctrl = False
        self.__draw = 0

        #self.__delay   = 0
        #self.__counter = 0
        self.__changed = 0

        self.__ctrl = False
        self.__middle = False
        self.__draw = 0

        self.__numberOfLines = 20
        self.__Y             = 0

        self.__counterNumber = [0, None]
        self.__counterLabel  = [0, None]
        self.__labelErrors   = []
        self.__labelsInText  = []

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

        for bankNum in range(1, 9):
            bank = "bank" + str(bankNum)

            for section in keys:
                if section in self.__loader.virtualMemory.codes[bank].keys():
                    lines = self.__loader.virtualMemory.codes[bank][section].code.split("\n")

                    for line in lines:
                        lineStructure = self.getLineStructure(line)

                        if   self.isCommandInLineThat(lineStructure, "asm"):
                             self.addLabelIfCan(lineStructure["param#1"][0], bank, section, None, None)

                        elif self.isCommandInLineThat(lineStructure, "mLoad"):
                             folder = lineStructure["param#1"][0]
                             fName  = lineStructure["param#2"][0]

                             path   = self.__loader.mainWindow.projectPath + folder + "/" + fName + ".asm"
                             f      = open(path, "r")
                             data   = f.read()
                             f.close()

                             for dLine in data.split("\n"):
                                 self.addLabelIfCan(dLine, bank, section, folder, fName)
                        else:
                            command = None
                            obj     = False

                            for c in self.__loader.syntaxList.keys():
                                if lineStructure["command"][0] == c or lineStructure["command"][0] in self.__loader.syntaxList[c].alias:
                                   command = self.__loader.syntaxList[c]
                                   break

                            if command == None:
                               objectThings = self.__loader.objectMaster.returnAllAboutTheObject(lineStructure["command"][0])
                               command = self.__loader.objectMaster.createFakeCommandOnObjectProcess(objectThings)
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

                                         #for dLine in objectThings["template"]:
                                         #    self.addLabelIfCan(dLine, bank, section, folder, fName)
                                      else:
                                          # Currently, there is no command besides mLoad that would load data directly.
                                          pass

    def addLabelIfCan(self, possibleLabel, bank, section, folder, fName):
        if len(possibleLabel) > 0:
            replacedTags = self.replaceTags(possibleLabel, bank, section, folder, fName)

            if replacedTags[0] not in ["#", "*", " ", "\t"]:
                if possibleLabel not in self.__labels:
                    self.__labelsInText.append(possibleLabel)
                    if possibleLabel != replacedTags:
                        self.__labelsInText.append(replacedTags)

    def isCommandInLineThat(self, line, command):
        if line["command"][0] == command or line["command"][0] in self.__loader.syntaxList[command].alias:
           return True
        return False

    def replaceTags(self, label, bank, section, folder, fName):
        label = label.replace("##", "#")

        tags = {
            "#BANK#": bank, "#SECTION#": section
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

        self.__running  = 0

        t = Thread(target = self.__createEditorLines)
        t.daemon = True
        t.start()

        self.__loader.threadLooper.addToThreading(self, self.__loop, [], 1)

    def __loop(self):
        try:
            if self.__counterNumber[0] > 0:
               if self.__counterNumber[0] == 1:
                  self.checkNumber(self.__counterNumber[1])

               self.__counterNumber[0] -= 1.

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

        for lineNum in range(self.__Y, self.__Y + 20):
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

    def checkNumber(self, event):
        entry = event.widget
        name  = str(entry).split(".")[-1]

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

        self.__allData = []
        self.fillLineDataEnd()
        self.__running -= 1

    def checkLabel(self, event):
        entry = event.widget
        name  = str(entry).split(".")[-1]

        self.__counterLabel =  [0, None]

        lineNum = int(name.split("_")[-1])

        value = self.__lineData[lineNum]["labelVal"].get()

        if value == "":
           entry.config(bg=self.__colors.getColor("boxBackNormal"),
                         fg=self.__colors.getColor("boxFontNormal"))
           return





        """                       if self.__fullTextLabels.count(line[0]) > 1:
                           if printError: print("OHNO Duplicate", line[0])
                           self.addToErrorList(lineStructure["lineNum"],
                                              self.prepareErrorASM("compilerErrorASMDuplicateLabel",
                                                                    "", line[0],
                                                                    lineStructure["lineNum"], lineStructure))

                       if self.__labelsOfMainKenrel.count(line[0]) > 0:
                           if printError: print("OHNO KernelLabel", line[0])
                           self.addToErrorList(lineStructure["lineNum"],
                                              self.prepareErrorASM("compilerErrorASMDKernelLabel",
                                                                    "", line[0],
                                                                    lineStructure["lineNum"], lineStructure))

                       if len(line[0]) < 8:
                           if printError: print("OHNO Too Short", line[0])
                           self.addToErrorList(lineStructure["lineNum"],
                                               self.prepareErrorASM("compilerErrorASMKernelLabelShort",
                                                                    "", line[0],
                                                                    lineStructure["lineNum"], lineStructure))
        """



    def setCounterNumber(self, event):
        self.__counterNumber[0] = 10
        self.__counterNumber[1] = event