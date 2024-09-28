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
        self.__allDataReady = False

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

        self.__counterNumber  = [0, None]
        self.__counterLabel   = [0, None]
        self.__counterEntries = [0, None]
        self.__labelErrors   = []
        self.__labelsInText  = {}
        self.__maskByte      = "$00"
        self.__numberOfSelecteds = 0

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

                                          import os

                                          for root, dirs, files in os.walk(self.__loader.mainWindow.projectPath):
                                              for dir in dirs:
                                                  for subRoot, subDirs, subFiles in os.walk(self.__loader.mainWindow.projectPath + "/" + dir):
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
            if " = " in possibleLabel:
                possibleLabel = possibleLabel.split(" = ")[0]

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

        if folder == "raw":
            tags = {
                "#BANK#": bank
            }

            if fName  != None: tags["#NAME#"] = fName
            tags["#FOLDER#"] = "raw"

            if folder != None and fName != None:
                tags["#FULL#"] = bank + "_" + fName + "_raw"
        else:
            tags = {
                "#BANK#": bank, "#FULL#": bank + "_" + section
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

        t = Thread(target = self.createOthersFrame)
        t.daemon = True
        t.start()

        self.__loader.threadLooper.addToThreading(self, self.__loop, [], 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "<KeyPress-Control_L>" , self.shiftON, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "<KeyRelease-Control_L>", self.shiftOff, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "<KeyPress-Control_R>" , self.shiftON, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "<KeyRelease-Control_R>", self.shiftOff, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "Button-2>"             , self.drawMode, 1)

    def createOthersFrame(self):
        self.__running += 1

        while self.__othersFrame.winfo_height() < 2: sleep(0.000001)

        per = 9

        self.__removerFrame = Frame(self.__othersFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__loaderFrame.winfo_width(), height = self.__othersFrame.winfo_height() // per)

        self.__removerFrame.pack_propagate(False)
        self.__removerFrame.pack(side=TOP, anchor=N, fill=X)

        self.__removeButton = Button(self.__removerFrame, height=self.__loaderFrame.winfo_height() // per,
                                       width=self.__othersFrame.winfo_width() ,
                                       name="removeGaps",
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       fg=self.__loader.colorPalettes.getColor("font"),
                                       text = self.__dictionaries.getWordFromCurrentLanguage("removeGaps"),
                                       font = self.__smallFont,
                                       activebackground=self.__loader.colorPalettes.getColor("highLight"),
                                       command=None
                                       )
        self.__removeButton.pack_propagate(False)
        self.__removeButton.pack(side=TOP, anchor=N, fill=BOTH)

        self.__generatorTitleFrame = Frame(self.__othersFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__loaderFrame.winfo_width(), height = self.__othersFrame.winfo_height() // per)

        self.__generatorTitleFrame.pack_propagate(False)
        self.__generatorTitleFrame.pack(side=TOP, anchor=N, fill=X)

        self.__generatorTitleLabel = Label(self.__generatorTitleFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   fg = self.__loader.colorPalettes.getColor("font"), justify = LEFT,
                                   font = self.__smallFont, text = self.__loader.dictionaries.getWordFromCurrentLanguage("alterSelectedData") + ":",
                                   height = 1)

        self.__generatorTitleLabel.pack_propagate(False)
        self.__generatorTitleLabel.pack(side=TOP, anchor=N, fill=BOTH)

        self.__moveFrames = Frame(self.__othersFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__loaderFrame.winfo_width(), height = self.__othersFrame.winfo_height() // per)

        self.__moveFrames.pack_propagate(False)
        self.__moveFrames.pack(side=TOP, anchor=N, fill=X)

        self.__mirroringFrames = Frame(self.__othersFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__loaderFrame.winfo_width(), height = self.__othersFrame.winfo_height() // per)

        self.__mirroringFrames.pack_propagate(False)
        self.__mirroringFrames.pack(side=TOP, anchor=N, fill=X)

        while self.__mirroringFrames.winfo_height() < 2: sleep(0.000001)

        self.__mirroringFrame1 = Frame(self.__mirroringFrames,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__othersFrame.winfo_width() // 2,
                                   height = self.__othersFrame.winfo_height() // per)

        self.__mirroringFrame1.pack_propagate(False)
        self.__mirroringFrame1.pack(side=LEFT, anchor=W, fill=Y)

        self.__mirroringFrame2 = Frame(self.__mirroringFrames,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__othersFrame.winfo_width() // 2,
                                   height = self.__othersFrame.winfo_height() // per)

        self.__mirroringFrame2.pack_propagate(False)
        self.__mirroringFrame2.pack(side=LEFT, anchor=W, fill=Y)

        self.__mirroringButton1 = Button(self.__mirroringFrame1, height=self.__loaderFrame.winfo_height() // per,
                                       width=self.__othersFrame.winfo_width() // 2,
                                       name="mirrorHorizontally",
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       fg=self.__loader.colorPalettes.getColor("font"),
                                       text = self.__dictionaries.getWordFromCurrentLanguage("mirrorHorizontally"),
                                       font = self.__smallFont,
                                       activebackground=self.__loader.colorPalettes.getColor("highLight"),
                                       state=DISABLED, command=None
                                       )
        self.__mirroringButton1.pack_propagate(False)
        self.__mirroringButton1.pack(side=TOP, anchor=N, fill=BOTH)

        self.__mirroringButton2 = Button(self.__mirroringFrame2, height=self.__loaderFrame.winfo_height() // per,
                                       width=self.__othersFrame.winfo_width() // 2,
                                       name="mirrorVertically",
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       fg=self.__loader.colorPalettes.getColor("font"),
                                       text = self.__dictionaries.getWordFromCurrentLanguage("mirrorVertically"),
                                       font = self.__smallFont,
                                       activebackground=self.__loader.colorPalettes.getColor("highLight"),
                                       state=DISABLED, command=None
                                       )
        self.__mirroringButton2.pack_propagate(False)
        self.__mirroringButton2.pack(side=TOP, anchor=N, fill=BOTH)

        self.__maskingFrames = Frame(self.__othersFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__loaderFrame.winfo_width(), height = self.__othersFrame.winfo_height() // per)

        self.__maskingFrames.pack_propagate(False)
        self.__maskingFrames.pack(side=TOP, anchor=N, fill=X)

        self.__maskingFrames1 = Frame(self.__maskingFrames,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__othersFrame.winfo_width() // 3,
                                   height = self.__othersFrame.winfo_height() // per)

        self.__maskingFrames1.pack_propagate(False)
        self.__maskingFrames1.pack(side=LEFT, anchor=W, fill=Y)

        self.__maskingFrames2 = Frame(self.__maskingFrames,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__othersFrame.winfo_width() // 3,
                                   height = self.__othersFrame.winfo_height() // per)

        self.__maskingFrames2.pack_propagate(False)
        self.__maskingFrames2.pack(side=LEFT, anchor=W, fill=Y)

        self.__maskingFrames3 = Frame(self.__maskingFrames,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__othersFrame.winfo_width() // 3,
                                   height = self.__othersFrame.winfo_height() // per)

        self.__maskingFrames3.pack_propagate(False)
        self.__maskingFrames3.pack(side=LEFT, anchor=W, fill=Y)

        self.__maskingButton = Button(self.__maskingFrames3, height=self.__loaderFrame.winfo_height() // per,
                                       width=self.__othersFrame.winfo_width() // 2,
                                       name="maskData",
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       fg=self.__loader.colorPalettes.getColor("font"),
                                       text = self.__dictionaries.getWordFromCurrentLanguage("maskData"),
                                       font = self.__smallFont,
                                       activebackground=self.__loader.colorPalettes.getColor("highLight"),
                                       state=DISABLED, command=None
                                       )
        self.__maskingButton.pack_propagate(False)
        self.__maskingButton.pack(side=TOP, anchor=N, fill=BOTH)

        self.__radioButtonVar2 = IntVar()
        self.__radioButtonThings2 = [{}, {}, {}, {}]

        self.__wordKeyList2 = ["NOT", "AND" , "OR", "EOR"]
        self.__radioButtonVar2.set(1)

        self.__changeIfSelected = [self.__mirroringButton1, self.__mirroringButton2]

        while self.__maskingFrames1.winfo_width() < 2: sleep(0.000000001)

        for num in range(0, 4):
            self.__radioButtonThings2[num]["frame"] = Frame(self.__maskingFrames1,
                                                            bg=self.__loader.colorPalettes.getColor("window"),
                                                            width=self.__maskingFrames1.winfo_width() // 4,
                                                            height=self.__maskingFrames1.winfo_height() // per)

            self.__radioButtonThings2[num]["frame"].pack_propagate(False)
            self.__radioButtonThings2[num]["frame"].pack(side=LEFT, anchor=W, fill=Y)

            self.__radioButtonThings2[num]["button"] = Radiobutton(self.__radioButtonThings2[num]["frame"],
                                                  text=self.__wordKeyList2[num],
                                                  name="radio2_" + self.__wordKeyList2[num],
                                                  bg=self.__colors.getColor("window"),
                                                  fg=self.__colors.getColor("font"),
                                                  justify=LEFT, font=self.__miniFont,
                                                  variable=self.__radioButtonVar2, state = DISABLED,
                                                  activebackground=self.__colors.getColor("highLight"),
                                                  activeforeground=self.__loader.colorPalettes.getColor("font"),
                                                  value = num + 1, command=None
                                                  )

            self.__radioButtonThings2[num]["button"].pack_propagate(False)
            self.__radioButtonThings2[num]["button"].pack(side=LEFT, anchor=W)

            self.__loader.threadLooper.bindingMaster.addBinding(self, self.__radioButtonThings2[num]["button"],
                                                                "<Button-1>",
                                                                self.radioClicked, 1)

            self.__changeIfSelected.append(self.__radioButtonThings2[num]["button"])

        self.__maskNumberVar = StringVar()
        self.__maskNumberVar.set(self.__maskByte)
        self.__maskNumberEntry = Entry(self.__maskingFrames2,
                                            name="entry_MaskByte",
                                            bg=self.__colors.getColor("boxBackNormal"),
                                            fg=self.__colors.getColor("boxFontNormal"),
                                            width=9999, justify=CENTER, state=DISABLED,
                                            textvariable=self.__maskNumberVar,
                                            font=self.__normalFont
                                            )

        self.__maskNumberEntry.pack_propagate(False)
        self.__maskNumberEntry.pack(fill=X, side=TOP, anchor=N)

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__maskNumberEntry,
                                                            "<KeyRelease>",
                                                            self.setCounterNumber, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__maskNumberEntry,
                                                            "<FocusOut>",
                                                            self.checkNumber, 1)

        self.__moveFrames1 = Frame(self.__moveFrames,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__loaderFrame.winfo_width() , height = self.__othersFrame.winfo_height() // per)

        self.__moveFrames1.pack_propagate(False)
        self.__moveFrames1.pack(side=LEFT, anchor=W, fill=Y)

        self.__moveFrames2 = Frame(self.__moveFrames,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__loaderFrame.winfo_width() , height = self.__othersFrame.winfo_height() // per)

        self.__moveFrames2.pack_propagate(False)
        self.__moveFrames2.pack(side=LEFT, anchor=W, fill=Y)

        self.__moveButton1 = Button(self.__moveFrames1, height=self.__loaderFrame.winfo_height() // per,
                                       width=self.__othersFrame.winfo_width() ,
                                       name="moveUp",
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       fg=self.__loader.colorPalettes.getColor("font"),
                                       text = "/\/\ " + self.__dictionaries.getWordFromCurrentLanguage("moveUp"),
                                       font = self.__smallFont,
                                       activebackground=self.__loader.colorPalettes.getColor("highLight"),
                                       state=DISABLED, command=None
                                       )
        self.__moveButton1.pack_propagate(False)
        self.__moveButton1.pack(side=TOP, anchor=N, fill=BOTH)

        self.__moveButton2 = Button(self.__moveFrames2, height=self.__loaderFrame.winfo_height() // per,
                                       width=self.__othersFrame.winfo_width() ,
                                       name="modeDown",
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       fg=self.__loader.colorPalettes.getColor("font"),
                                       text = "\/\/ " + self.__dictionaries.getWordFromCurrentLanguage("moveDown"),
                                       font = self.__smallFont,
                                       activebackground=self.__loader.colorPalettes.getColor("highLight"),
                                       state=DISABLED, command=None
                                       )
        self.__moveButton2.pack_propagate(False)
        self.__moveButton2.pack(side=TOP, anchor=N, fill=BOTH)

        self.__rangeFrames = Frame(self.__othersFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__loaderFrame.winfo_width(), height = self.__othersFrame.winfo_height() // per)

        self.__rangeFrames.pack_propagate(False)
        self.__rangeFrames.pack(side=TOP, anchor=N, fill=X)

        self.__rangeFrame1 = Frame(self.__rangeFrames,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__othersFrame.winfo_width() // 3 * 2,
                                   height = self.__othersFrame.winfo_height() // per)

        self.__rangeFrame1.pack_propagate(False)
        self.__rangeFrame1.pack(side=LEFT, anchor=W, fill=Y)

        self.__rangeFrame3 = Frame(self.__rangeFrames,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__othersFrame.winfo_width() // 3,
                                   height = self.__othersFrame.winfo_height() // per)

        self.__rangeFrame3.pack_propagate(False)
        self.__rangeFrame3.pack(side=LEFT, anchor=W, fill=Y)

        self.__rangeButton = Button(self.__rangeFrame3, height=self.__loaderFrame.winfo_height() // per,
                                       width=self.__othersFrame.winfo_width() // 3,
                                       name="generateRange",
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       fg=self.__loader.colorPalettes.getColor("font"),
                                       text = self.__dictionaries.getWordFromCurrentLanguage("generateRange"),
                                       font = self.__smallFont,
                                       activebackground=self.__loader.colorPalettes.getColor("highLight"),
                                       state=DISABLED, command=None
                                       )
        self.__rangeButton.pack_propagate(False)
        self.__rangeButton.pack(side=TOP, anchor=N, fill=BOTH)

        while self.__rangeFrame1.winfo_width() < 2: sleep(0.00000001)

        self.__rangeFrame1_1 = Frame(self.__rangeFrame1,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__rangeFrame1.winfo_width() // 3.5,
                                   height = self.__rangeFrame1.winfo_height() // per)

        self.__rangeFrame1_1.pack_propagate(False)
        self.__rangeFrame1_1.pack(side=LEFT, anchor=W, fill=Y)

        self.__rangeFrame1_2 = Frame(self.__rangeFrame1,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__rangeFrame1.winfo_width() // 50,
                                   height = self.__rangeFrame1.winfo_height() // per)

        self.__rangeFrame1_2.pack_propagate(False)
        self.__rangeFrame1_2.pack(side=LEFT, anchor=W, fill=Y)

        self.__rangeFrame1_3 = Frame(self.__rangeFrame1,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__rangeFrame1.winfo_width() // 3.5,
                                   height = self.__rangeFrame1.winfo_height() // per)

        self.__rangeFrame1_3.pack_propagate(False)
        self.__rangeFrame1_3.pack(side=LEFT, anchor=W, fill=Y)

        self.__rangeFrame1_4 = Frame(self.__rangeFrame1,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__rangeFrame1.winfo_width() // 6,
                                   height = self.__rangeFrame1.winfo_height() // per)

        self.__rangeFrame1_4.pack_propagate(False)
        self.__rangeFrame1_4.pack(side=LEFT, anchor=W, fill=Y)

        self.__rangeFrame1_5 = Frame(self.__rangeFrame1,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__rangeFrame1.winfo_width() // 3.5,
                                   height = self.__rangeFrame1.winfo_height() // per)

        self.__rangeFrame1_5.pack_propagate(False)
        self.__rangeFrame1_5.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__lineLabel = Label(self.__rangeFrame1_2, width = self.__rangeFrame1_2.winfo_width(),
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   fg = self.__loader.colorPalettes.getColor("font"), justify = CENTER,
                                   font = self.__smallFont, text = "-",
                                   height = 1)

        self.__lineLabel.pack_propagate(False)
        self.__lineLabel.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__lenTextLabel = Label(self.__rangeFrame1_4, width = len(self.__dictionaries.getWordFromCurrentLanguage("len") + ": "),
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   fg = self.__loader.colorPalettes.getColor("font"), justify = RIGHT,
                                   font = self.__smallFont, text = self.__dictionaries.getWordFromCurrentLanguage("len") + ": ",
                                   height = 1)

        self.__lenTextLabel.pack_propagate(False)
        self.__lenTextLabel.pack(side=RIGHT, anchor=E, fill=BOTH)


        self.__rangeSmallerVar   = StringVar()
        self.__rangeSmallerVar.set("$00")
        self.__rangeSmallerEntry = Entry(self.__rangeFrame1_1,
                                             name="entry_rangeSmaller",
                                             bg=self.__colors.getColor("boxBackNormal"),
                                             fg=self.__colors.getColor("boxFontNormal"),
                                             width=9999, justify=CENTER, state=DISABLED,
                                             textvariable=self.__rangeSmallerVar,
                                             font=self.__normalFont
                                             )

        self.__rangeSmallerEntry.pack_propagate(False)
        self.__rangeSmallerEntry.pack(fill=X, side=TOP, anchor=N)

        self.__rangeLargerVar   = StringVar()
        self.__rangeLargerVar.set("$FF")
        self.__rangeLargerEntry = Entry(self.__rangeFrame1_3,
                                             name="entry_rangeLarger",
                                             bg=self.__colors.getColor("boxBackNormal"),
                                             fg=self.__colors.getColor("boxFontNormal"),
                                             width=9999, justify=CENTER, state=DISABLED,
                                             textvariable=self.__rangeLargerVar,
                                             font=self.__normalFont
                                             )

        self.__rangeLargerEntry.pack_propagate(False)
        self.__rangeLargerEntry.pack(fill=X, side=TOP, anchor=N)

        self.__rangeLenVar   = StringVar()
        self.__rangeLenVar.set("16")
        self.__rangeLen      =  16
        self.__rangeLenEntry = Entry(self.__rangeFrame1_5,
                                             name="entry_rangeLen",
                                             bg=self.__colors.getColor("boxBackNormal"),
                                             fg=self.__colors.getColor("boxFontNormal"),
                                             width=9999, justify=CENTER, state=DISABLED,
                                             textvariable=self.__rangeLenVar,
                                             font=self.__normalFont
                                             )

        self.__rangeLenEntry.pack_propagate(False)
        self.__rangeLenEntry.pack(fill=X, side=TOP, anchor=N)

        self.__ranges = ["$00", "$FF"]

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__rangeSmallerEntry, "<KeyRelease>", self.setCounterNumber, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__rangeSmallerEntry, "<FocusOut>"  , self.checkNumber,      1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__rangeLargerEntry , "<KeyRelease>", self.setCounterNumber, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__rangeLargerEntry , "<FocusOut>"  , self.checkNumber,      1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__rangeLenEntry    , "<KeyRelease>", self.setCounterNumber, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__rangeLenEntry    , "<FocusOut>"  , self.checkNumber,      1)

        self.__changeIfSelected.append(self.__maskingButton)
        self.__changeIfSelected.append(self.__moveButton1)
        self.__changeIfSelected.append(self.__moveButton2)
        self.__changeIfSelected.append(self.__rangeButton)
        self.__changeIfSelected.append(self.__rangeSmallerEntry)
        self.__changeIfSelected.append(self.__rangeLargerEntry)
        self.__changeIfSelected.append(self.__rangeLenEntry)

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__mirroringButton1, "<Button-1>", self.simpleButtonsStuff, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__mirroringButton2, "<Button-1>", self.simpleButtonsStuff, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__maskingButton   , "<Button-1>", self.simpleButtonsStuff, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__rangeButton     , "<Button-1>", self.simpleButtonsStuff, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__moveButton1     , "<Button-1>", self.moveUpDown        , 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__moveButton2     , "<Button-1>", self.moveUpDown        , 1)

        self.__running -= 1

    def simpleButtonsStuff(self, event):
        button = event.widget
        name  = str(button).split(".")[-1].split("_")[-1]

        if button.cget("state") == DISABLED: return

        selectors, numOfSelecteds, inARow = self.getLabelsAndSelecteds()

        keyList = list(selectors.keys())
        keyList.sort()

        index = -1
        first = True

        for lineNum in keyList:
            index += 1
            item = selectors[lineNum]
            if item[1]:
               try:
                   nextLineNum = keyList[index + 1]
                   lastOne     = False
               except:
                   nextLineNum = len(self.__allData)
                   lastOne     = True

               if   name == "mirrorHorizontally":
                    for lNum in range(lineNum, nextLineNum):
                        if self.__allData[lNum]["entry"].startswith("#"):
                           self.__allData[lNum]["entry"] = self.__allData[lNum]["entry"][1:]

                        if self.__allData[lNum]["entry"] != "":
                           value, mode  = self.convertEntryToNum(self.__allData[lNum]["entry"])
                           value, dummy = self.convertEntryToNum("%" + self.formatNum(value, "bin")[1:][::-1])
                           self.__allData[lNum]["entry"] = self.formatNum(value, mode)
                           self.doTheBitsFromVal(lNum, True)

               elif name == "mirrorVertically":
                    items = item[2][::-1]
                    index = -1

                    removed = 0

                    while "" in items:
                        items.remove("")
                        removed += 1

                    for n in range(0, removed):
                        items.append("")

                    for lNum in range(lineNum, nextLineNum):
                        if index < len(items):
                            index += 1
                            val    = items[index]
                        else:
                            val   = ""

                        self.__allData[lNum]["entry"] = val
                        self.doTheBitsFromVal(lNum, True)

               elif name == "maskData":
                    if first:
                       method             = self.__wordKeyList2[self.__radioButtonVar2.get() - 1]
                       if method         != "NOT":
                          maskData, dummy = self.convertEntryToNum(self.__maskByte)
                          maskBin         = self.formatNum(maskData, "bin")[1:]
                       first = False

                    for lNum in range(lineNum, nextLineNum):
                        if self.__allData[lNum]["entry"].startswith("#"):
                           self.__allData[lNum]["entry"] = self.__allData[lNum]["entry"][1:]

                        if self.__allData[lNum]["entry"] != "":
                           lineData, mode = self.convertEntryToNum(self.__allData[lNum]["entry"])
                           lineDataBin    = self.formatNum(lineData, "bin")[1:]

                           newBinary = ""
                           for cNum in range(0, 8):
                               c1        = lineDataBin[cNum]

                               if method == "NOT":
                                  newBinary += str(1 - int(c1))
                               else:
                                  c2 = maskBin[cNum]
                                  if   method == "AND":
                                       if "0" in [c1, c2]:
                                          newBinary += "0"
                                       else:
                                          newBinary += "1"
                                  elif method == "OR":
                                      if "1" in [c1, c2]:
                                          newBinary += "1"
                                      else:
                                          newBinary += "0"

                                  elif method == "EOR":
                                      if  c1 != c2:
                                          newBinary += "1"
                                      else:
                                          newBinary += "0"

                           newValue, dummy               = self.convertEntryToNum("%" + newBinary)
                           self.__allData[lNum]["entry"] = self.formatNum(newValue, mode)
                           self.doTheBitsFromVal(lNum, True)

               elif name == "generateRange":
                    if first:
                       fromR = self.__ranges[0]
                       toR   = self.__ranges[1]

                       length  = self.__rangeLen
                       l2      = nextLineNum - lineNum
                       if l2   < length: length = l2

                       if fromR.startswith("#"):
                          fromR = fromR[1:]

                       if toR.startswith("#"):
                          toR   = toR  [1:]

                       fromRData, mode  = self.convertEntryToNum(fromR)
                       toRData  , dummy = self.convertEntryToNum(toR)

                       step    = (toRData - fromRData) / length

                       newList = []

                       xxx = fromRData
                       for num in range(0, length):
                           diff = xxx - int(xxx)

                           if diff > 0.49999999999999999:
                              newList.append(round(xxx))
                           else:
                              newList.append(int  (xxx))

                           xxx += step

                       newList[-1] = toRData

                       for num in range(0, length):
                           self.__allData[num + lineNum]["entry"] = self.formatNum(newList[num], mode)
                           self.doTheBitsFromVal(num + lineNum, True)

        self.__changed = True
        self.fillTheEditor()

    def moveUpDown(self, event):
        button = event.widget
        name = str(button).split(".")[-1].split("_")[-1][4:]

        if button.cget("state") == DISABLED: return

        selectors, numOfSelecteds, inARow = self.getLabelsAndSelecteds()

        selectedOnes = []
        for lineNum in selectors:
            if selectors[lineNum][1] == True:
               selectedOnes.append(lineNum)

        keyList = list(selectors.keys())
        keyList.sort()

        smallest = keyList[ 0]
        largest  = keyList[-1]

        if smallest == largest: return

        index = -1
        while True:
            index +=1
            if index  == len(keyList) or (index == len(keyList) - 1 and name == "Down"): break
            if (index == 0 and name == "Up"): continue

            lineNum = keyList[index]
            if lineNum in selectedOnes:
               selectedOnes.remove(lineNum)

               self.doTheMove(index, keyList, lineNum, name)
               index = -1

        newList = []
        for n in range(0, smallest):
            newList.append(self.__schema)

        for key in keyList:
            for lineNum in range(key, len(self.__allData)):
                if lineNum  > key and self.__allData[lineNum]["label"] != "":
                   break
                if key == largest and self.__allData[lineNum]["entry"] == "":
                   break

                newList.append(deepcopy(self.__allData[lineNum]))



        for n in range(largest, len(self.__allData)):
            newList.append(self.__schema)

        self.__allData = newList
        self.__changed = True
        self.fillTheEditor()

        self.enableDisableOthers()
        self.colorLabels(None)

    def doTheMove(self, index, keyList, theNum, dir):
        if index == None:
           index = keyList.index(theNum)

           if dir == "Up"   and index == 0              : return
           if dir == "Down" and index == len(keyList) -1: return

        keyList.pop(index)

        if dir == "Up":
           keyList.insert(index - 1, theNum)
        else:
           keyList.insert(index + 1, theNum)

    def convertEntryToNum(self, num):
        if num.startswith("%"):
            mode = "bin"
            value = int(num.replace("%", "0b"), 2)
        elif num.startswith("$"):
            mode = "hex"
            value = int(num.replace("$", "0x"), 16)
        else:
            mode = "dec"
            value = int(num)

        return value, mode


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

        per = 9

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
                                       name="indexButton-",
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
                                       name="indexButton+",
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       fg=self.__loader.colorPalettes.getColor("font"),
                                       text = ">>", font = self.__normalFont,
                                       activebackground=self.__loader.colorPalettes.getColor("highLight"),
                                       state=DISABLED, command=None
                                       )
        self.__indexButton2.pack_propagate(False)
        self.__indexButton2.pack(side=TOP, anchor=N, fill=BOTH)

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__numOfLinesEntry, "<KeyRelease>",
                                                            self.entryCounter, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__numOfLinesEntry, "<FocusOut>",
                                                            self.__checkEntry, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__yIndexEntry, "<KeyRelease>",
                                                            self.entryCounter, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__yIndexEntry, "<FocusOut>",
                                                            self.__checkEntry, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__indexButton1, "<Button-1>",
                                                            self.addSub, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__indexButton2, "<Button-1>",
                                                            self.addSub, 1)

        self.__lastBigFrame = Frame(self.__loaderFrame,
                                        bg=self.__loader.colorPalettes.getColor("window"),
                                        width=self.__loaderFrame.winfo_width(),
                                        height=self.__loaderFrame.winfo_height())

        self.__lastBigFrame.pack_propagate(False)
        self.__lastBigFrame.pack(side=TOP, anchor=N, fill=BOTH)

        self.__lastBigFrame1 = Frame(self.__lastBigFrame,
                                        bg=self.__loader.colorPalettes.getColor("window"),
                                        width=self.__loaderFrame.winfo_width() // 3,
                                        height=self.__loaderFrame.winfo_height())

        self.__lastBigFrame1.pack_propagate(False)
        self.__lastBigFrame1.pack(side=LEFT, anchor=W, fill=Y)

        self.__lastBigFrame2 = Frame(self.__lastBigFrame,
                                        bg=self.__loader.colorPalettes.getColor("window"),
                                        width=self.__loaderFrame.winfo_width() // 3 * 2,
                                        height=self.__loaderFrame.winfo_height())

        self.__lastBigFrame2.pack_propagate(False)
        self.__lastBigFrame2.pack(side=LEFT, anchor=W, fill=BOTH)

        while self.__lastBigFrame.winfo_width() < 2: sleep(0.00000001)

        self.__endLabelFrame = Frame(self.__lastBigFrame1,
                                        bg=self.__loader.colorPalettes.getColor("window"),
                                        width=self.__loaderFrame.winfo_width() // 3,
                                        height=self.__loaderFrame.winfo_height() // per // 2)

        self.__endLabelFrame.pack_propagate(False)
        self.__endLabelFrame.pack(side=TOP, anchor=N, fill=X)

        self.__endLabel = Label(self.__endLabelFrame,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   fg=self.__loader.colorPalettes.getColor("font"), justify=LEFT,
                                   font=self.__miniFont,
                                   text=self.__loader.dictionaries.getWordFromCurrentLanguage("endByteType") + " >>",
                                   height=1)

        self.__endLabel.pack_propagate(False)
        self.__endLabel.pack(side=LEFT, anchor=W)

        self.__radioButtonVar = IntVar()
        self.__radioButtonThings = [{}, {}, {}]

        self.__wordKeyList = ["autoWhole" , "autoLayer", "manualWhole"]
        self.__radioButtonVar.set(1)

        for num in range(0, 3):
            self.__radioButtonThings[num]["frame"] = Frame(self.__lastBigFrame2,
                                                            bg=self.__loader.colorPalettes.getColor("window"),
                                                            width=self.__loaderFrame.winfo_width() // 3 * 2,
                                                            height=self.__loaderFrame.winfo_height() // per)

            self.__radioButtonThings[num]["frame"].pack_propagate(False)
            self.__radioButtonThings[num]["frame"].pack(side=TOP, anchor=N, fill=X)

            self.__radioButtonThings[num]["button"] = Radiobutton(self.__radioButtonThings[num]["frame"],
                                                  text=self.__dictionaries.getWordFromCurrentLanguage(self.__wordKeyList[num]),
                                                  name="radio1_" + self.__wordKeyList[num],
                                                  bg=self.__colors.getColor("window"),
                                                  fg=self.__colors.getColor("font"),
                                                  justify=LEFT, font=self.__miniFont,
                                                  variable=self.__radioButtonVar,
                                                  activebackground=self.__colors.getColor("highLight"),
                                                  activeforeground=self.__loader.colorPalettes.getColor("font"),
                                                  value = num + 1, command=None
                                                  )

            self.__radioButtonThings[num]["button"].pack_propagate(False)
            self.__radioButtonThings[num]["button"].pack(side=LEFT, anchor=W)

            self.__loader.threadLooper.bindingMaster.addBinding(self, self.__radioButtonThings[num]["button"],
                                                                "<Button-1>",
                                                                self.radioClicked, 1)

            if self.__wordKeyList[num] == "manualWhole":
               self.__radioButtonThings[num]["entryFrame"] = Frame(self.__radioButtonThings[num]["frame"],
                                                               bg=self.__loader.colorPalettes.getColor("window"),
                                                               width=self.__loaderFrame.winfo_width() // 3 * 2,
                                                               height=self.__loaderFrame.winfo_height() // per)

               self.__radioButtonThings[num]["entryFrame"].pack_propagate(False)
               self.__radioButtonThings[num]["entryFrame"].pack(side=LEFT, anchor=W, fill=BOTH)

               self.__radioButtonThings[num]["endVarVar"]   = StringVar()
               self.__radioButtonThings[num]["endVarEntry"] = Entry(self.__radioButtonThings[num]["entryFrame"],
                                                                    name="entry_ManualEndByte",
                                                                    bg=self.__colors.getColor("boxBackNormal"),
                                                                    fg=self.__colors.getColor("boxFontNormal"),
                                                                    width=9999, justify=CENTER, state=DISABLED,
                                                                    textvariable=self.__radioButtonThings[num]["endVarVar"],
                                                                    font=self.__normalFont
                                                                    )

               self.__radioButtonThings[num]["endVarEntry"].pack_propagate(False)
               self.__radioButtonThings[num]["endVarEntry"].pack(fill=X, side=TOP, anchor=N)

               self.__loader.threadLooper.bindingMaster.addBinding(self, self.__radioButtonThings[num]["endVarEntry"], "<KeyRelease>",
                                                                    self.setCounterNumber, 1)
               self.__loader.threadLooper.bindingMaster.addBinding(self, self.__radioButtonThings[num]["endVarEntry"], "<FocusOut>",
                                                                    self.checkNumber, 1)
        self.__getTheEndByte(None)
        self.__running -= 1

    def radioClicked(self, event):
        button = event.widget
        name  = str(button).split(".")[-1].split("_")[-1]
        group = int(str(button).split(".")[-1].split("_")[0][-1])

        if button.cget("state") == DISABLED: return

        if   group == 1:
             num = self.__wordKeyList.index(name)
             self.__radioButtonVar.set(num+1)

             if name == "manualWhole":
                self.__radioButtonThings[2]["endVarEntry"].config(state = NORMAL)
             else:
                self.__radioButtonThings[2]["endVarEntry"].config(state = DISABLED)
                self.__radioButtonThings[2]["endVarVar"]  .set("")

             self.__getTheEndByte(None)
        elif group == 2:
             num = self.__wordKeyList2.index(name)
             self.__radioButtonVar2.set(num+1)

             self.enableDisableOthers()

    def __getTheEndByte(self, label):
       num = self.__radioButtonVar.get()

       if   num == 1:
            return self.formatNum(self.__getPossibeValidEndBytes(None)[-1], "hex")
       elif num == 2:
            return self.formatNum(self.__getPossibeValidEndBytes(label)[-1], "hex")
       else:
            possibleOnes = self.__getPossibeValidEndBytes(None)[0]

            try:
               theNumber = self.__radioButtonThings[2]["endVarVar"].get()

               if theNumber.startswith("#"): theNumber = theNumber[1:]

               valOfEntry, mode = self.convertEntryToNum(theNumber)

               """
               valOfEntry = self.getInt(theNumber)

               if theNumber.startswith("%"):
                   mode = "bin"
               elif theNumber.startswith("$"):
                   mode = "hex"
               else:
                   mode = "dec"
               """
               found = False
               for num in possibleOnes:
                   if num == valOfEntry:
                      found = True
                      break

               if found == False:
                  returnMe = self.formatNum(self.getClosest(valOfEntry, possibleOnes), mode)
               else:
                  returnMe = theNumber
            except:
               returnMe = "$FF"

            self.__radioButtonThings[2]["endVarVar"].set(returnMe)
            self.__radioButtonThings[2]["endVarEntry"].config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                                              fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
            return returnMe

    def getClosest(self, val, array):
        diff = 9999
        num  = -1

        for n in array:
            d = abs(val - n)

            if d < diff:
               diff   = d
               num    = n

        return num

    def getInt(self, theNumber):
        if   theNumber.startswith("%"):
             return int(theNumber.replace("%", "0b"), 2)

        elif theNumber.startswith("$"):
             return int(theNumber.replace("$", "0x"), 16)

        else:
             return int(theNumber)

    def __getPossibeValidEndBytes(self, label):
        numbers = list(range(0, 256))
        foundLabel = False

        while self.__allDataReady == False: sleep(0.000001)

        for line in self.__allData:
            if label not in [None, "", "None"]:
               if line["label"] != "":
                  if foundLabel == False:
                     if label == line["label"]: foundLabel = True
                  else:
                     if line["entry"] != "": break

               if foundLabel == False: continue

            if line["entry"] == "": continue
            v = self.getInt(line["entry"])
            if v in numbers: numbers.remove(v)

        return numbers

    def addSub(self, event):
        button = event.widget
        name = str(button).split(".")[-1].split("_")[-1]

        if button.cget("state") == DISABLED: return

        self.__checkEntry(event)

    def entryCounter(self, event):
        self.__counterEntries = [5, event]

    def __checkEntry(self, event):
        entry = event.widget
        name = str(entry).split(".")[-1].split("_")[-1]

        if entry.cget("state") == DISABLED: return

        self.__counterEntries = [0, None]

        maxIndex    = self.__numberOfLines - len(self.__lineData)
        if maxIndex < 0: maxIndex = 0

        wasButton = False
        if "indexButton" in name:
            changers = {"+": 1, "-": -1}
            self.__yIndexEntryVal.set(str(self.__Y + changers[name[-1]]))
            name = "yIndex"
            wasButton = True

        valuesOnName = {
            "numOfLines": [[1, 256]     , self.__numOfLinesEntryVal],
            "yIndex"    : [[0, maxIndex], self.__yIndexEntryVal    ]
        }

        entryVal = valuesOnName[name][1]
        value    = entryVal.get()

        try:
            num     = int(value)
        except:
            entry.config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                        fg=self.__loader.colorPalettes.getColor("boxFontUnSaved"),
                        )

        if wasButton == False:
           entry.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                        fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                        )
        else:
           self.__yIndexEntry.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                         fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                         )

        if   num < valuesOnName[name][0][0]: num = valuesOnName[name][0][0]
        elif num > valuesOnName[name][0][1]: num = valuesOnName[name][0][1]

        entryVal.set(str(num))

        if   name == "numOfLines":
             origNum = self.__numberOfLines
             self.__numberOfLines = num

             maxIndex    = self.__numberOfLines - len(self.__lineData)
             if self.__Y > maxIndex:
                self.__Y = maxIndex
                self.__yIndexEntryVal.set(str(maxIndex))

        elif name == "yIndex":
             origNum = self.__Y
             self.__Y = num

        if origNum != num:
           self.fillLineDataEnd()
           self.__changed = True

        self.deleteErrors()
        self.fillTheEditor()
        self.colorLabels(None)

    def deleteErrors(self):
        for num in range(0, len(self.__lineData)):
            self.__labelErrors[num] = {}

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

                if self.__counterEntries[0] > 0:
                   if self.__counterEntries[0] == 1:
                      self.__checkEntry(self.__counterEntries[1])

                   self.__counterEntries[0] -= 1

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

        self.__schema = {
            "bits": [0,0,0,0,0,0,0,0], "entry": "", "label": "", "addEndByte": 0, "wasSelected": 0, "color": 0
        }

        if len(self.__allData) < self.__numberOfLines:
           for num in range(0, self.__numberOfLines - len(self.__allData)):
               self.__allData.append(deepcopy(self.__schema))

        self.__allDataReady = True
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
               self.__lineData[lineNumOnEditor]["endVar"]    .config(state = DISABLED)

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

               """ 
               disable = False
               #print("---------------------------")
               if self.__allData[lineNum]["label"] == "":
                  disable = True
               else:
                  #print("fos")
                  if lineNum < len(self.__allData) - 1:
                     #print(self.__allData[lineNum + 1]["label"], self.__allData[lineNum]["entry"])
                     if self.__allData[lineNum + 1]["label"] != "" and self.__allData[lineNum]["entry"] == "":
                        disable = True
               """

               if self.checkIfDisable(lineNumOnEditor):
                  self.__lineData[lineNumOnEditor]["select"].config(state=DISABLED)
                  self.__lineData[lineNumOnEditor]["endVar"].config(state=DISABLED)
                  self.__lineData[lineNumOnEditor]["colorData"].config(state=DISABLED)

                  self.__lineData[lineNumOnEditor]["endVarVar"].set(0)
                  self.__lineData[lineNumOnEditor]["selectVal"].set(0)
                  self.__lineData[lineNumOnEditor]["colorDataVar"].set(0)

               else:
                  self.__lineData[lineNumOnEditor]["select"].config(state=NORMAL)
                  self.__lineData[lineNumOnEditor]["endVar"].config(state=NORMAL)
                  self.__lineData[lineNumOnEditor]["colorData"].config(state=NORMAL)

                  self.__lineData[lineNumOnEditor]["endVarVar"].set(self.__allData[lineNum]["addEndByte"])
                  self.__lineData[lineNumOnEditor]["selectVal"].set(self.__allData[lineNum]["wasSelected"])
                  self.__lineData[lineNumOnEditor]["colorDataVar"].set(self.__allData[lineNum]["wasSelected"])


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

        dummy, mode = self.convertEntryToNum(theNumber)

        binString = "0b"
        for bitNum2 in range(7, -1, -1): binString += str(self.__lineData[lineNum]["bitVals"][bitNum2])

        theNumber = self.formatNum(int(binString, 2), mode)

        self.__lineData[lineNum]["entryVal"].set(theNumber)
        self.__changed = True

        self.__lineData[lineNum]["entry"].config(bg=self.__colors.getColor("boxBackNormal"),
                                                 fg=self.__colors.getColor("boxFontNormal"))

        self.__allData[lineNum + self.__Y]["entry"] = value
        self.__allData[lineNum + self.__Y]["bits"] = deepcopy(self.__lineData[lineNum]["bitVals"])
        self.__changed = True

    def formatNum(self, theNumber, mode):
        if   mode == "bin":
             theNumber = bin(theNumber).replace("0b", "")
             return "%" + ((8 - len(theNumber)) * "0") + theNumber
        elif mode == "hex":
             theNumber = hex(theNumber).replace("0x", "")
             return ("$" + ((2 - len(theNumber)) * "0") + theNumber).upper()
        else:
             return str(theNumber)

    def shiftON(self, event):
        self.__ctrl = True

    def shiftOff(self, event):
        self.__ctrl = False

    def drawMode(self, event):
        if self.__draw == 1:
           self.__draw = 0
        else:
           self.__draw = 1

    def doTheBitsFromVal(self, lineNum, allData):
        try:
            teszt   = int(lineNum)
        except:
            try:
                lineNum = int(lineNum.split("_")[-1])
            except:
                f = False

                for n in range(0, len(self.__lineData)):
                    if self.__lineData[n]["entry"] == lineNum:
                       lineNum = int(lineNum.cget("name").split("_")[-1])
                       f = True
                       break
                if f == False: return

        if allData:
           stringVal = self.__allData[lineNum]["entry"]
           lineNum   = lineNum - self.__Y
        else:
           stringVal = self.__lineData[lineNum]["entryVal"].get()

        if stringVal != "":
           value, mode = self.convertEntryToNum(stringVal)
           if mode == "bin":
               binVal = stringVal[1:]
           else:
               binVal = self.formatNum(value, "bin")[1:]
        else:
           binVal = "0" * 8

        for bitNum in range(0, 8):
            val = binVal[7 - bitNum]

            self.__lineData[lineNum]["bitVals"][bitNum] = int(val)

            colors = {
                "0": [self.__colors.getColor("boxBackNormal")],
                "1": [self.__colors.getColor("boxFontNormal")],
            }

            self.__lineData[lineNum]["bitButtons"][bitNum].config(
                bg=colors[val])

        self.__changed = True
        self.__allData[lineNum + self.__Y]["bits"] = deepcopy(self.__lineData[lineNum]["bitVals"])
        self.colorLabels(None)

    def checkNumber(self, event):
        entry = event.widget
        name  = str(entry).split(".")[-1]

        if entry.cget("state") == DISABLED: return

        self.__counterNumber =  [0, None]

        subName = name.split("_")[-1]

        hardcoded = {
            "ManualEndByte": self.__radioButtonThings[2]["endVarVar"],
            "MaskByte"     : self.__maskNumberVar,
            "rangeSmaller" : self.__rangeSmallerVar,
            "rangeLarger"  : self.__rangeLargerVar,
            "rangeLen"     : self.__rangeLenVar
        }

        varHolder = None

        if   subName in hardcoded:
             varHolder = hardcoded[subName]
             value     = hardcoded[subName].get()
        else:
             lineNum   = int(subName)
             varHolder = self.__lineData[lineNum]["entryVal"]

        value = varHolder.get()

        if value == "":
           entry.config(bg=self.__colors.getColor("boxBackNormal"),
                         fg=self.__colors.getColor("boxFontNormal"))

           if subName == "ManualEndByte": self.__getTheEndByte(None)
           if subName not in hardcoded:
               for bitNum in range(0, 8):
                   self.__lineData[lineNum]["bitButtons"][bitNum].config(bg=self.__colors.getColor("boxBackNormal"))

               self.__changed = True
               self.__lineData[lineNum]           ["entryVal"].set("")
               self.__allData [lineNum + self.__Y]["entry"   ] = ""
               self.__lineData[lineNum]           ["bitVals" ] = [0,0,0,0,0,0,0,0]
               self.__allData [lineNum + self.__Y]["bits"    ] = [0,0,0,0,0,0,0,0]
               self.colorLabels(None)

           return

        if value.startswith("#"): value = value[1:]

        try:
            value, mode = self.convertEntryToNum(value)
            """
            if   value.startswith("%"):
                 mode = "bin"
                 value  = int(value.replace("%", "0b"), 2)
            elif value.startswith("$"):
                 mode = "hex"
                 value  = int(value.replace("$", "0x"), 16)
            else:
                 mode = "dec"
                 value  = int(value)
            """
        except:
            entry.config(bg = self.__colors.getColor("boxBackUnSaved"),
                         fg = self.__colors.getColor("boxFontUnSaved"))

            if subName == "ManualEndByte": self.__getTheEndByte(None)

            return

        entry.config(bg=self.__colors.getColor("boxBackNormal"),
                     fg=self.__colors.getColor("boxFontNormal"))

        if subName == "rangeLen": base = 1
        else                    : base = 0

        if   value < base      : value = base
        elif value > 255 + base: value = 255 + base

        binVal = bin(value).replace("0b", "")
        binVal = ((8-len(binVal)) * "0") + binVal

        value = self.formatNum(value, mode)

        """
        if   mode == "dec":
             value = str(value)
        elif mode == "bin":
             value = "%" + binVal
        else:
             value = hex(value).replace("0x", "")
             if len(value) == 1: value = "0" + value
             value = "$" + value

        """

        if   subName in ["rangeSmaller", "rangeLarger"]: pass
        elif subName in hardcoded                      : varHolder.set(str(value))
        else:
             varHolder.set(str(value))
             self.__allData [lineNum + self.__Y]["entry"] = str(value)

        entry.icursor = len(str(value))

        if  subName not in hardcoded:
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
            self.__allData [lineNum + self.__Y]["bits"] = deepcopy(self.__lineData[lineNum]["bitVals"])
            self.colorLabels(None)

        elif subName == "ManualEndByte":
            self.__getTheEndByte(None)

        elif subName == "MaskByte":
             self.__maskByte = str(value)

        elif subName == "rangeLen":
            self.__rangeLen, dummy = self.convertEntryToNum(str(value))

        elif subName in ["rangeSmaller", "rangeLarger"]:
           modeNum = 0

           if "Smaller" in subName:
              self.__rangeSmallerVar.set(value)
              modeNum = 0
           else:
              self.__rangeLargerVar.set(value)
              modeNum = 1

           self.__ranges[modeNum] = value
           values  = [-1, -1]
           mode    = ""
           for n in range(0, 2):
               if modeNum == n:
                  values[n], mode  = self.convertEntryToNum(self.__ranges[n])
               else:
                  values[n], dummy = self.convertEntryToNum(self.__ranges[n])

           for n in range(0, 2):
               self.__ranges[n] = self.formatNum(values[n], mode)

               if n == 0:
                  self.__rangeSmallerVar.set(self.__ranges[0])
               else:
                  self.__rangeLargerVar.set(self.__ranges[1])

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
            "select"       : None,
            "endVarVal"    : None,
            "endVar"       : None,
            "colorData"    : None,
            "colorDataVar" : None
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
                  width=self.__sizes[0] // 10 * 4, height=self.__editorFrame.winfo_height() // 21
                  )
            fLabelEntry.pack_propagate(False)
            fLabelEntry.pack(side=LEFT, anchor=E, fill=Y)

            fAddEndByte = Frame(f,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  width=self.__sizes[0] // 10, height=self.__editorFrame.winfo_height() // 21
                  )
            fAddEndByte.pack_propagate(False)
            fAddEndByte.pack(side=LEFT, anchor=E, fill=Y)

            fColorData = Frame(f,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  width=self.__sizes[0] // 10, height=self.__editorFrame.winfo_height() // 21
                  )
            fColorData.pack_propagate(False)
            fColorData.pack(side=LEFT, anchor=E, fill=Y)

            fSelectEntry = Frame(f,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  width=self.__sizes[0] // 10, height=self.__editorFrame.winfo_height() // 21
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

                l4 = Label(fAddEndByte,
                           text = self.__loader.dictionaries.getWordFromCurrentLanguage("addEndByte"),
                           font=self.__smallFont, fg=self.__colors.getColor("font"),
                           bg=self.__colors.getColor("window")
                           )

                l4.pack_propagate(False)
                l4.pack(side=TOP, anchor=N, fill=BOTH)

                l5 = Label(fColorData,
                           text = self.__loader.dictionaries.getWordFromCurrentLanguage("colorData"),
                           font=self.__smallFont, fg=self.__colors.getColor("font"),
                           bg=self.__colors.getColor("window")
                           )

                l5.pack_propagate(False)
                l5.pack(side=TOP, anchor=N, fill=BOTH)


                lLast = Label(fSelectEntry,
                           text = self.__loader.dictionaries.getWordFromCurrentLanguage("selectLabel"),
                           font=self.__smallFont, fg=self.__colors.getColor("font"),
                           bg=self.__colors.getColor("window")
                           )

                lLast.pack_propagate(False)
                lLast.pack(side=TOP, anchor=N, fill=BOTH)

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

                self.__lineData[-1]["endVarVar"] = IntVar()
                self.__lineData[-1]["endVar"] = Checkbutton(fAddEndByte, width=fSelectEntry.winfo_width(),
                                                bg=self.__colors.getColor("window"),
                                                name="endVar_" + str(lineNum),
                                                justify=CENTER,
                                                variable=self.__lineData[-1]["endVarVar"],
                                                activebackground=self.__colors.getColor("highLight"),
                                                command=None
                                                )

                self.__lineData[-1]["endVar"].pack_propagate(False)
                self.__lineData[-1]["endVar"].pack(fill=Y, side=LEFT, anchor=E)

                self.__lineData[-1]["colorDataVar"] = IntVar()
                self.__lineData[-1]["colorData"] = Checkbutton(fColorData, width=fSelectEntry.winfo_width(),
                                                bg=self.__colors.getColor("window"),
                                                name = "colorData_" + str(lineNum),
                                                justify=CENTER, state = DISABLED,
                                                variable=self.__lineData[-1]["colorData"],
                                                activebackground=self.__colors.getColor("highLight"),
                                                command=None
                                                )

                self.__lineData[-1]["colorData"].pack_propagate(False)
                self.__lineData[-1]["colorData"].pack(fill=Y, side=LEFT, anchor=E)

                self.__lineData[-1]["selectVal"] = IntVar()
                self.__lineData[-1]["select"] = Checkbutton(fSelectEntry, width=fSelectEntry.winfo_width(),
                                                bg=self.__colors.getColor("window"),
                                                name = "select_" + str(lineNum),
                                                justify=CENTER,
                                                variable=self.__lineData[-1]["selectVal"],
                                                activebackground=self.__colors.getColor("highLight"),
                                                command=None
                                                )

                self.__lineData[-1]["select"].pack_propagate(False)
                self.__lineData[-1]["select"].pack(fill=Y, side=LEFT, anchor=E)

                self.__loader.threadLooper.bindingMaster.addBinding(self, self.__lineData[-1]["entry"]     , "<KeyRelease>",
                                                                    self.setCounterNumber, 1)
                self.__loader.threadLooper.bindingMaster.addBinding(self, self.__lineData[-1]["entry"]     , "<FocusOut>",
                                                                    self.checkNumber, 1)
                self.__loader.threadLooper.bindingMaster.addBinding(self, self.__lineData[-1]["labelEntry"], "<KeyRelease>",
                                                                    self.setCounterNumber2, 1)
                self.__loader.threadLooper.bindingMaster.addBinding(self, self.__lineData[-1]["labelEntry"], "<FocusOut>",
                                                                    self.checkLabel, 1)
                self.__loader.threadLooper.bindingMaster.addBinding(self, self.__lineData[-1]["select"]    , "<Button-1>",
                                                                    self.clickedButton, 1)
                self.__loader.threadLooper.bindingMaster.addBinding(self, self.__lineData[-1]["endVar"]    , "<Button-1>",
                                                                    self.clickedButton, 1)
                self.__loader.threadLooper.bindingMaster.addBinding(self, self.__lineData[-1]["colorData"]  , "<Button-1>",
                                                                    self.clickedButton, 1)

        self.__allData = []
        self.fillLineDataEnd()
        self.__running -= 1

    def clickedButton(self, event):
        button = event.widget
        name  = str(button).split(".")[-1]

        if button.cget("state") == DISABLED: return

        typ     = name.split("_")[0]
        lineNum = int(name.split("_")[1])

        keys = {"select": "wasSelected", "endVar": "addEndByte", "colorData": "colorDataVar"}

        self.__allData[lineNum + self.__Y][keys[typ]] = 1 - self.__allData[lineNum + self.__Y][keys[typ]]

        if typ == "select":
           if self.__allData[lineNum + self.__Y][keys[typ]] == 1:
              self.__numberOfSelecteds += 1
           else:
              self.__numberOfSelecteds -= 1

           self.enableDisableOthers()
           self.colorLabels(None)

        #print(self.__lineData[lineNum]["endVarVar"].get(), lineNum )

    def enableDisableOthers(self):
        if self.__numberOfSelecteds == 0:
           for item in self.__changeIfSelected:
               item.config(state = DISABLED)

           self.__maskNumberEntry.config(state = DISABLED)
        else:
           for item in self.__changeIfSelected:
               item.config(state=NORMAL)

           if self.__radioButtonVar2.get() > 1:
               self.__maskNumberEntry.config(state = NORMAL)
           else:
               self.__maskNumberEntry.config(state = DISABLED)

           selectors, numOfSelecteds, inARow = self.getLabelsAndSelecteds()

           if len(selectors.keys()) < 2:
              self.__moveButton1.config(state = DISABLED)
              self.__moveButton2.config(state = DISABLED)
           else:
              firstKey = -1
              lastKey  = -1
              for lastKey in selectors.keys():
                  if firstKey == -1: firstKey = lastKey

              if selectors[firstKey][1] == True:
                 self.__moveButton1.config(state=DISABLED)
              else:
                 self.__moveButton1.config(state=NORMAL)

              if selectors[lastKey][1] == True:
                 self.__moveButton2.config(state=DISABLED)
              else:
                 self.__moveButton2.config(state=NORMAL)

    def getLabelsAndSelecteds(self):
        selectors = {}
        lastItem  = None
        numOfSelecred = 0

        inARow        = False
        firstSelected = True

        for lineNum in range(0, len(self.__allData)):
            label    = self.__allData[lineNum]["label"]
            selected = self.__allData[lineNum]["wasSelected"]
            entry    = self.__allData[lineNum]["entry"]

            if label != "":
               selectors[lineNum] = [label, selected, [entry]]
               lastItem           = selectors[lineNum]
               if selected == True: numOfSelecred += 1

               if firstSelected == False and selected == False:
                  inARow        =  False

               if firstSelected == True and selected:
                  firstSelected =  False
                  inARow        =  True
            else:
               if lastItem != None: lastItem[2].append(entry)

        return selectors, numOfSelecred, inARow


    def checkLabel(self, event):
        entry = event.widget
        name  = str(entry).split(".")[-1]

        if entry.cget("state") == DISABLED: return

        self.__counterLabel =  [0, None]

        lineNum = int(name.split("_")[-1])

        value = self.__lineData[lineNum]["labelVal"].get()
        wasError = False

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
                 wasError = True
              else:
                 self.removeError(lineNum, "duplicateLabel")

              if self.glen(value) < 8 or len(value) < 8:
                 self.addError("labelTooShort", {"#LABEL#": value} , lineNum)
                 wasError = True
              else:
                 self.removeError(lineNum, "labelTooShort")

              collectLabelNums = {}

              for lNum in range(0, self.__numberOfLines):
                  #if lNum == lineNum: continue

                  """  
                  if self.__lineData[lNum]["labelVal"].get() == value:
                     self.addError("duplicateOnData", {"#LABEL#": value} , lineNum)
                     if "duplicateOnData" not in self.__labelErrors[lNum].keys():
                         self.addError("duplicateOnData", {"#LABEL#": value} , lNum)
                     wasError = True
                  else:
                     self.removeError(lineNum, "duplicateOnData")
                  """
                  if self.__lineData[lNum]["labelVal"].get() == "":
                     self.removeError(lNum, "duplicateOnData")
                  else:
                      if self.__lineData[lNum]["labelVal"].get() not in collectLabelNums:
                         collectLabelNums[self.__lineData[lNum]["labelVal"].get()]  = [1, [lNum]]
                      else:
                         collectLabelNums[self.__lineData[lNum]["labelVal"].get()][0] += 1
                         collectLabelNums[self.__lineData[lNum]["labelVal"].get()][1].append(lNum)

              for key in collectLabelNums:
                  if collectLabelNums[key][0] > 1:
                     for lNum in collectLabelNums[key][1]:
                         if lNum == lineNum: wasError = True

                         self.addError("duplicateOnData", {"#LABEL#": value}, lNum)
                  else:
                      self.removeError(collectLabelNums[key][1][0], "duplicateOnData")


              illegals = self.getIllegals(value)

              if len(illegals["chars"]) > 0:
                 self.addError("illegalCharacter", {"#LABEL#"   : value,
                                                    "#ILLEGALS#": ", ".join(illegals["chars"])}, lineNum)
                 wasError = True

              else:
                 self.removeError(lineNum, "illegalCharacter")

              if len(illegals["tags"]) > 0:
                 self.addError("illegalTag", {"#LABEL#": value,
                                                    "#ILLEGALS#": ", ".join(illegals["tags"])}, lineNum)
                 wasError = True

              else:
                 self.removeError(lineNum, "illegalTag")

              if value.endswith("_ENDBYTE"):
                 self.addError("endsEnd", {"#LABEL#": value}, lineNum)
                 wasError = True

              else:
                 self.removeError(lineNum, "endsEnd")

              if value.startswith("#BANK#") == False and value.startswith("#NAME#") == False:
                 self.addError("startTag", {"#LABEL#": value}, lineNum)
                 wasError = True

              else:
                 self.removeError(lineNum, "startTag")

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

    def checkIfDisable(self, num):
        num += self.__Y

        if self.__allData[num]["label"] == "":
            return True

        if num < len(self.__allData) - 1:
            #print(self.__allData[num + 1]["label"], "|" , self.__allData[num]["entry"])
            if self.__allData[num + 1]["label"] != "" and self.__allData[num]["entry"] == "":
               return True

        return False

    def colorLabels(self, lineNum):
        errorText = ""

        for num in range(0, 20):
            if self.__labelErrors[num] == {}:
               self.__lineData[num]["labelEntry"].config(bg = self.__colors.getColor("boxBackNormal"),
                                                         fg = self.__colors.getColor("boxFontNormal"))

               self.__allData[self.__Y + num]["label"] = self.__lineData[num]["labelVal"].get()

               if self.checkIfDisable(num):
                  self.__lineData[num]["selectVal"].set(0)
                  self.__lineData[num]["select"].config(state    = DISABLED)
                  self.__lineData[num]["endVarVar"].set(0)
                  self.__lineData[num]["endVar"].config(state    = DISABLED)
                  self.__lineData[num]["colorData"].config(state = DISABLED)
                  self.__allData[num + self.__Y]["addEndByte"]  = 0
                  self.__allData[num + self.__Y]["wasSelected"] = 0
                  self.__allData[num + self.__Y]["color"]       = 0

               else:
                  self.__lineData[num]["select"].config(state = NORMAL)
                  self.__lineData[num]["endVar"].config(state = NORMAL)
                  self.__lineData[num]["colorData"].config(state = NORMAL)

            else:
               self.__lineData[num]["labelEntry"].config(bg=self.__colors.getColor("boxBackUnSaved"),
                                                         fg=self.__colors.getColor("boxFontUnSaved"))
               if lineNum != None:
                   if lineNum == num or errorText == "":
                      #
                      #  Get the last key
                      #
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
