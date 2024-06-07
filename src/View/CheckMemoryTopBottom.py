from tkinter import *
from SubMenu import SubMenu
from time import sleep

class CheckMemoryTopBottom:

    def __init__(self, loader, caller, codeData, boss, bank):

        self.__loader = loader
        self.__mainWindow = self.__loader.mainWindow
        self.dead = False
        self.__caller   = caller
        self.__codeData = codeData
        self.__counter = 0
        self.__lastEvent = None

        self.__bossWindow = boss
        self.__bank       = bank

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
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize * 0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize * 0.65), False, False, False)
        self.__bigFont = self.__fontManager.getFont(int(self.__fontSize * 1.15), False, False, False)
        self.__bigFont2 = self.__fontManager.getFont(int(self.__fontSize * 1.5), False, False, False)

        self.__sizes = [self.__screenSize[0] // 3, self.__screenSize[1] // 2.5]
        self.__didOnce = False

        self.__window = SubMenu(self.__loader, "screenTester", self.__sizes[0], self.__sizes[1], None, self.__addElements,
                                2)
        self.dead = True

    def __closeWindow(self):
        self.dead = True
        self.__topLevelWindow.destroy()
        self.bossFocus()
        try:
            self.__loader.topLevels.remove(self.__topLevelWindow)
        except:
            pass

    def bossFocus(self):
        if self.__didOnce == False:
           self.__didOnce  = True
           self.__bossWindow.deiconify()
           self.__bossWindow.focus()

    def __addElements(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()
        self.__topLevelWindow.protocol('WM_DELETE_WINDOW', self.__closeWindow)
        from tkinter import scrolledtext

        self.__buttons = Frame(self.__topLevelWindow, width= self.__sizes[0],
                                 height=self.__sizes[1] // 10,
                                 bg=self.__colors.getColor("window"))

        self.__buttons.pack_propagate(False)
        self.__buttons.pack(side=BOTTOM, anchor=S, fill=X)


        self.__textFrame = Frame(self.__topLevelWindow, width= self.__sizes[0],
                                 height=self.__sizes[1] // 10 * 9,
                                 bg=self.__colors.getColor("window"))

        self.__textFrame.pack_propagate(False)
        self.__textFrame.pack(side=BOTTOM, anchor=S, fill=BOTH)

        self.__OKButtonFrame = Frame(self.__buttons, width= self.__sizes[0] // 2,
                                 height=self.__sizes[1] // 10,
                                 bg=self.__colors.getColor("window"))

        self.__OKButtonFrame.pack_propagate(False)
        self.__OKButtonFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__CancelButtonFrame = Frame(self.__buttons, width= self.__sizes[0] // 2,
                                 height=self.__sizes[1] // 10,
                                 bg=self.__colors.getColor("window"))

        self.__CancelButtonFrame.pack_propagate(False)
        self.__CancelButtonFrame.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__OKButton = Button(self.__OKButtonFrame, height=9999, width=9999,
               bg=self.__loader.colorPalettes.getColor("window"),
               fg=self.__loader.colorPalettes.getColor("font"),
               text=self.__dictionaries.getWordFromCurrentLanguage("ok"),
               font=self.__normalFont, state=DISABLED, name="ok", command = self.pressedOK
               )
        self.__OKButton.pack_propagate(False)
        self.__OKButton.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__CancelButton = Button(self.__CancelButtonFrame, height=9999, width=9999,
               bg=self.__loader.colorPalettes.getColor("window"),
               fg=self.__loader.colorPalettes.getColor("font"),
               text=self.__dictionaries.getWordFromCurrentLanguage("cancel"),
               font=self.__normalFont, state=DISABLED, name="cancel", command = self.pressedCancel
               )
        self.__CancelButton.pack_propagate(False)
        self.__CancelButton.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__reportBox    = scrolledtext.ScrolledText(self.__textFrame, width=999999, height=self.__sizes[1]//2, wrap=WORD)
        self.__reportBox.pack(fill=BOTH, side=BOTTOM, anchor=S)

        self.__reportBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                fg=self.__loader.colorPalettes.getColor("boxFontNormal"))

        self.__getFont()

        self.__reportBox.bind("<Key>", lambda e: "break")
        self.checkOnMemoryCollision()

        if self.__wasThereAny == False:
           self.__caller.answer = "OK"
           self.__closeWindow()
        else:
           self.__caller.answer = "NOPE"
           self.__CancelButton.config(state = NORMAL)
           if self.__errorCounter == 0:
              self.__OKButton.config(state=NORMAL)

    def pressedOK(self):
        self.__caller.answer = "OK"
        self.__closeWindow()

    def pressedCancel(self):
        self.__closeWindow()

    def addTag(self, Y, X1, X2, tag):
        self.__reportBox.tag_add(tag, str(Y) + "." + str(X1) , str(Y) + "." + str(X2))

    def checkOnMemoryCollision(self):
        self.__varData = {}
        self.__wasThereAny = False
        self.__problems = {"error": 0, "warning": 0}


        mustBeUniqueIndicator = {
        }

        mustBeUniqueSpecial = {
            "Smoke":                [3],
            "Fire":                 [3],
            "DayTime":              [4, 5, 6],
            "Space":                [3],
            "SnowFlakes":           [5],
            "Earth":                [3],
            "BlinkingText":         [3, 4]
        }

        mustBeUnique = {
            "Indicator":            mustBeUniqueIndicator,
            "SpecialEffect":        mustBeUniqueSpecial,
            "SoundBank":            [4,5,6,7]
        }

        for bankNum in range(2, 9):
            bankKey = "Bank" + str(bankNum)
            if self.__bank != "all" and bankKey != self.__bank: continue

            self.__varData = {"Global": {}}

            for screenPart in self.__codeData.keys():
                for item in self.__codeData[screenPart][bankNum-2][2]:
                    item = item.split(" ")

                    itemType         = item[1]
                    startNum         = 2
                    mustBeUniqueList = []

                    if itemType in mustBeUnique:
                        if type(mustBeUnique[itemType]) == list:
                           mustBeUniqueList = mustBeUnique[itemType]
                        else:
                           if item[2] in mustBeUnique[itemType]:
                              mustBeUniqueList = mustBeUnique[itemType][item[2]]
                           startNum = 3

                    for subItemNum in range(startNum, len(item)):
                        subItem = item[subItemNum]
                        if "::" in subItem:
                            subItem = subItem.split("::")[1]

                        var = self.__loader.virtualMemory.getVariableByName2(subItem)
                        if var != False:
                            if var.validity in ["global", "bank1"]:
                                bkey = "Global"
                            else:
                                bkey = bankKey

                            #if bankKey not in self.__varData.keys():
                            #   self.__varData[bankKey] = {}

                            if subItem not in self.__varData[bkey]:
                                self.__varData[bkey][subItem] = [[0, 0, [0, 0, 0, 0, 0, 0, 0]], []]
                                self.__varData[bkey][subItem].append(var.system)
                                self.__varData[bkey][subItem].append(var.iterable)

                            self.__varData[bkey][subItem][0][0] += 1
                            if subItemNum in mustBeUniqueList:
                                if var.system:
                                   self.__varData[bkey][subItem][0][1] += 1
                                self.__varData[bkey][subItem][0][2][bankNum-2] += 1

                            self.__varData[bkey][subItem][1].append(item[0] +" (" + item[1] + ")")

        self.__lastLine    = 0
        self.__lastLineLen = -1
        self.addLineToBox("CheckMemoryTopBottomTitle", {})
        self.addLineToBox(self.generateMinusSighs(self.__lastLineLen), {})
        self.addLineToBox("CheckMemoryTopBottomWarningDef", {"#WARNING#": ["warning", "warning"]})
        self.addLineToBox("CheckMemoryTopBottomErrorDef", {"#ERROR#": ["error", "error"]})

        self.__warningCounter = 0
        self.__errorCounter   = 0

        for validity in self.__varData:
            firstPrint = True
            if len(self.__varData[validity].keys()) > 0:
               for varName in self.__varData[validity]:
                   occurs        =     self.__varData[validity][varName][0][0]
                   duplicates    =     self.__varData[validity][varName][0][1]
                   localDuprMax  = max(self.__varData[validity][varName][0][2])
                   appearances   =     self.__varData[validity][varName][1]
                   system        =     self.__varData[validity][varName][2]
                   iterable      =     self.__varData[validity][varName][3]

                   has2Print   = False
                   error = []

                   if duplicates > 1 or localDuprMax > 1:
                      self.__errorCounter += 1
                      has2Print = True
                      error.append(["duplicateError", {}])
                      error[-1][1]["#VAR#"]     = [varName, "variable"]
                      error[-1][1]["#NUM#"]     = ["#" + str(self.__errorCounter), "error"]
                      error[-1][1]["#LIST#"]    = [", ".join(appearances) , None]
                      error[-1][1]["#ERROR#"] = ["error", "error"]
                      self.__problems["error"] += 1

                   if system and iterable == False:
                      self.__warningCounter += 1
                      has2Print = True
                      error.append(["readOnlyWarning", {}])
                      error[-1][1]["#VAR#"] = [varName, "variable"]
                      error[-1][1]["#NUM#"]     = ["#" + str(self.__warningCounter), "warning"]
                      error[-1][1]["#LIST#"] = [", ".join(appearances), None]
                      error[-1][1]["#WARNING#"] = ["warning", "warning"]
                      self.__problems["warning"] += 1

                   if has2Print:
                      if firstPrint:
                        firstPrint         = False
                        self.__wasThereAny = True
                        self.addLineToBox("", {})
                        self.addLineToBox(self.generateMinusSighs(len(validity)), {})
                        self.addLineToBox(validity.upper(), {})
                        self.addLineToBox(self.generateMinusSighs(len(validity)), {})

                      for e in error:
                          self.addLineToBox(e[0], e[1])

        if self.__errorCounter > 0 or self.__warningCounter + 0:
           self.addLineToBox("", {})
           self.addLineToBox(self.generateMinusSighs(25), {})

           if self.__errorCounter > 0:
              text = self.__dictionaries.getWordFromCurrentLanguage("totalNumberOfErrors").replace("#NUM#", str(self.__errorCounter))
              self.addLineToBox(text, {text: [text, "error"]})

           if self.__warningCounter > 0:
              text = self.__dictionaries.getWordFromCurrentLanguage("totalNumberOfWarnings").replace("#NUM#", str(self.__warningCounter))
              self.addLineToBox(text, {text: [text, "warning"]})
           self.addLineToBox(self.generateMinusSighs(25), {})

    def generateMinusSighs(self, num):
        return("-" * (round(num * 1.5) + 5))

    def addLineToBox(self, key, changerDict):
        try:
            text = self.__dictionaries.getWordFromCurrentLanguage(key)
        except:
            text = key

        self.__lastLine += 1

        if changerDict not in [None, {}]:
           for k in changerDict:
               try:
                   changerDict[k][0] = self.__dictionaries.getWordFromCurrentLanguage(changerDict[k][0])
               except:
                   pass

               text = text.replace(k, changerDict[k][0])

        self.__lastLineLen = len(text)
        self.__reportBox.insert(END, text + "\n")
        self.__reportBox.see(str(self.__lastLineLen) + ".0")

        if changerDict not in [None, {}]:
           for k in changerDict:
               word = changerDict[k][0]
               tag  = changerDict[k][1]

               if tag == None: continue

               lastStart = 0
               while (True):
                   returnVal = text.find(word, lastStart)
                   if returnVal == -1: break

                   self.addTag(self.__lastLine, returnVal, returnVal + len(word), tag)
                   lastStart = returnVal + len(word)

    def __getFont(self):
        baseSize = int(self.__config.getValueByKey("codeBoxFont"))
        w = self.__loader.mainWindow.getWindowSize()[0] / 1600
        h = self.__loader.mainWindow.getWindowSize()[1] / 1200

        self.__fontSize = (baseSize * w * h)
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
            "warning": {
                "background": self.__loader.colorPalettes.getColor("highLight"),
                "font": self.__normalFont
            },
            "variable": {
                "foreground": self.__loader.colorPalettes.getColor("variable"),
                "font": self.__boldUnderlinedFont
            },
            "error": {
                "foreground": self.__loader.colorPalettes.getColor("boxFontUnSaved"),
                "background": self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                "font": self.__boldFont
           }
        }

        for key in self.__tagSettings:
            if "background" not in self.__tagSettings[key]:
                self.__reportBox.tag_config(key,
                                          foreground = self.__tagSettings[key]["foreground"],
                                          font = self.__tagSettings[key]["font"])
            elif "foreground" not in self.__tagSettings[key]:
                self.__reportBox.tag_config(key,
                                          background = self.__tagSettings[key]["background"],
                                          font = self.__tagSettings[key]["font"])
            else:
                self.__reportBox.tag_config(key,
                                              foreground=self.__tagSettings[key]["foreground"],
                                              background=self.__tagSettings[key]["background"],
                                              font=self.__tagSettings[key]["font"])

        self.__reportBox.config(font=self.__normalFont)
        self.__reportBox.tag_raise("sel")