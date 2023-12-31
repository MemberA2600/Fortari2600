from tkinter import *
from SubMenu import SubMenu
from threading import Thread

class ConstantWindow:

    def __init__(self, loader):
        self.__loader = loader

        self.dead = False
        self.notInitAnymore = False

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

        self.__bigFont = self.__fontManager.getFont(self.__fontSize, True, False, False)
        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize*0.65), False, False, False)
        self.__tinyFont = self.__fontManager.getFont(int(self.__fontSize*0.45), False, False, False)
        self.__numberOfLines = 20
        self.__countDownPageNum = 0
        self.__stopUs = False

        self.__sizes = {
            "common": [self.__screenSize[0] // 2.25, self.__screenSize[1]//2]
        }

        self.__listOfColumnNames = ["constantName", "constantValue", "constantValidityType", "constantValidityBank", "constantValiditySection"]

        self.__buffer = self.__loader.tapeFrames
        self.__imgIndex = 0
        self.__mode = ""
        self.__finished = True
        self.__archivedDone = False
        self.__selectedPage     = 1
        self.__maxNumberOfPages = 1
        self.__countDown        = 0

        self.__data = []
        self.__window = SubMenu(self.__loader, "constant", self.__sizes["common"][0],
                                self.__sizes["common"][1], None, self.__addElements, 1)

        self.__loader.collector.restoreSystemPath()
        self.dead = True
        self.changed = False


    def __closeWindow(self):
        if self.__finished == True:
            self.dead = True
            self.__topLevelWindow.destroy()
            self.__loader.topLevels.remove(self.__topLevelWindow)

    def __addElements(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()
        self.__topLevelWindow.protocol('WM_DELETE_WINDOW', self.__closeWindow)

        self.__labels              = []
        self.__entries             = {}
        self.__lineFrames          = []
        self.__listBoxes           = {}
        self.__entryVars           = {}

        self.__types               = ["global", "bank", "section"]

        self.__upperFrame = Frame(self.__topLevelWindow,
                                  width= self.__sizes[self.__loader.virtualMemory.kernel][0],
                                  height=self.__sizes[self.__loader.virtualMemory.kernel][1] // 10 * 9,
                                  bg=self.__colors.getColor("window"))
        self.__upperFrame.pack_propagate(False)
        self.__upperFrame.pack(side=TOP, anchor = N, fill=X)

        self.__controllerFrame = Frame(self.__topLevelWindow,
                                  width= self.__sizes[self.__loader.virtualMemory.kernel][0],
                                  height=self.__sizes[self.__loader.virtualMemory.kernel][1] // 6,
                                  bg=self.__colors.getColor("window"))
        self.__controllerFrame.pack_propagate(False)
        self.__controllerFrame.pack(side=TOP, anchor = N, fill=BOTH)

        self.__frameOfSettings = Frame(self.__upperFrame,
                                  width= self.__sizes[self.__loader.virtualMemory.kernel][0] // 5 * 4,
                                  height=self.__sizes[self.__loader.virtualMemory.kernel][1] // 10 * 9,
                                  bg=self.__colors.getColor("window"))
        self.__frameOfSettings.pack_propagate(False)
        self.__frameOfSettings.pack(side=LEFT, anchor = E, fill=Y)

        self.__spaceFrame = Frame(self.__upperFrame,
                            width= self.__sizes[self.__loader.virtualMemory.kernel][0] // 5,
                            height=self.__sizes[self.__loader.virtualMemory.kernel][1] // 10 * 9,
                            bg="black")
        self.__spaceFrame.pack_propagate(False)
        self.__spaceFrame.pack(side=LEFT, anchor = E, fill=Y)

        from CosmicCommuter import CosmicCommuter
        self.__cosmicCommuter = CosmicCommuter(self.__spaceFrame, self.__loader, [
            self.__sizes[self.__loader.virtualMemory.kernel][0] // 5,
            self.__sizes[self.__loader.virtualMemory.kernel][1] // 10 * 9],
            self.__topLevelWindow, self)

        for num in range(0, self.__numberOfLines):
            w = self.__sizes[self.__loader.virtualMemory.kernel][0] // 5 // 5 * 4

            f = Frame(self.__frameOfSettings,
                      width=self.__sizes[self.__loader.virtualMemory.kernel][0] // 5 * 4,
                      height=self.__sizes[self.__loader.virtualMemory.kernel][1] // 10 * 9 // self.__numberOfLines,
                      bg=self.__colors.getColor("window"))
            f.pack_propagate(False)
            f.pack(side=TOP, anchor=N, fill=X)

            self.__lineFrames.append(f)
            self.__soundPlayer.playSound("Pong")

            for subNum in range(0, 5):
                name = str(num-1) + "_" + str(subNum)

                f2 = Frame(f,
                          width=w,
                          height=self.__sizes[self.__loader.virtualMemory.kernel][1] // 10 * 9 // self.__numberOfLines,
                          bg=self.__colors.getColor("window"),)
                f2.pack_propagate(False)
                f2.pack(side=LEFT, anchor=S, fill=Y)

                if num == 0:
                   text = self.__dictionaries.getWordFromCurrentLanguage(self.__listOfColumnNames[subNum])

                   l = Label(f2, text=text,
                             font=self.__miniFont, fg=self.__colors.getColor("font"),
                             bg=self.__colors.getColor("window"), justify=CENTER
                             )

                   l.pack_propagate(False)
                   l.pack(side=TOP, anchor=CENTER, fill=BOTH)

                   self.__labels.append(l)

                else:
                    if subNum < 2:
                       eVar = StringVar()
                       e    = Entry(f2,
                                    bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                    width=99,
                                    fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                    textvariable=eVar, name=name,
                                    state=DISABLED, font=self.__miniFont, justify=CENTER,
                                    command=None)

                       e.pack_propagate(False)
                       e.pack(side=TOP, anchor=CENTER, fill=BOTH)

                       self.__entries[name]   = e
                       self.__entryVars[name] = eVar
                       e.bind("<FocusOut>"  , self.callChanger)
                       e.bind("<KeyRelease>", self.callChangerDelayed)

                    else:
                       text = self.__dictionaries.getWordFromCurrentLanguage(self.__listOfColumnNames[subNum])

                       from FortariMB import FortariMB
                       if subNum == 2:
                          items     = ["global", "bank", "section"]
                          multi     = False
                          translate = True
                          default   = [self.__dictionaries.getWordFromCurrentLanguage("global")]
                       else:
                          multi     = True
                          translate = False
                          default   = []

                          if subNum == 3:
                             items = []
                             for bankNum in range(1, 9):
                                 bankNum = "Bank" + str(bankNum)
                                 items.append(bankNum)
                          else:
                             from copy import deepcopy
                             items = deepcopy(self.__loader.sections)
                             for item in items:
                                 if item not in self.__loader.mainWindow.validSections:
                                    items.remove(item)

                       self.__listBoxes[name] = FortariMB(self.__loader, f2, DISABLED, self.__miniFont, text, items, multi, translate, self.selectedChanged, default)

        self.__controllers = {}

        for num in range(0, 5):
            f = Frame(self.__controllerFrame,
                      width=self.__sizes[self.__loader.virtualMemory.kernel][0] // 5,
                      height=self.__sizes[self.__loader.virtualMemory.kernel][1] // 6,
                      bg=self.__colors.getColor("window"))
            f.pack_propagate(False)
            f.pack(side=LEFT, anchor=W, fill=Y)

            if num != 1:
               data = {
                   0: ["<<",
                       self.pageBefore,
                       self.__bigFont, "prev"
                       ],
                   2: [">>",
                       self.pageAfter,
                       self.__bigFont, "next"
                       ],
                   3: [self.__dictionaries.getWordFromCurrentLanguage("ok"),
                       self.__saveData,
                       self.__normalFont, "ok"],
                   4: [self.__dictionaries.getWordFromCurrentLanguage("cancel"),
                       self.__closeWindow,
                       self.__normalFont, "cancel"]
               }

               b = Button(f, width=999999999,
                          bg=self.__colors.getColor("window"),
                          fg=self.__colors.getColor("font"),
                          font=data[num][2], state=DISABLED,
                          command=data[num][1],
                          text=   data[num][0]
                          )
               b.pack_propagate(False)
               b.pack(side=LEFT, anchor=W, fill=BOTH)

               self.__controllers[data[num][3]] = b

            else:
                self.__pageNum = StringVar()
                self.__pageNum.set("1")
                self.__pageNumE = Entry(  f,
                                          bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                          width=99,
                                          fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                          textvariable=self.__pageNum,
                                          state=DISABLED, font=self.__normalFont, justify=CENTER,
                                          )

                self.__pageNumE.pack_propagate(False)
                self.__pageNumE.pack(side=LEFT, anchor=W, fill=BOTH)
                self.__pageNumE.bind("<FocusOut>", self.pageNumChanged)
                self.__pageNumE.bind("<KeyRelease>", self.pageNumChanged)

        for key in self.__entries:
            self.__entries[key].config(state = NORMAL)

        for key in self.__listBoxes:
            if self.__listBoxes[key].multiSelect == False:
               self.__listBoxes[key].changeState(NORMAL)

        #for key in self.__controllers:
        #    self.__controllers[key].config(state = NORMAL)

        self.__controllers["cancel"].config(state=NORMAL)

        self.__loadData()
        self.pageNumChangedThing(None)

        t = Thread(target=self.loop)
        t.daemon = True
        t.start()

        self.notInitAnymore = True

    def pageNumChanged(self, event):
        self.__countDownPageNum = 40

    def pageNumChangedThing(self, event):
        self.__maxNumberOfPages = (len(self.__data) - 1) // self.__numberOfLines + 1

        self.__pageNumE.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                               fg=self.__loader.colorPalettes.getColor("boxFontNormal")
                               )
        try:
            num = int(self.__pageNum.get())
        except:
            if self.__pageNum.get() != "":
                self.__pageNumE.config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                                       fg=self.__loader.colorPalettes.getColor("boxFontUnSaved")
                                       )
            return

        if num < 1: num = 1
        if num > self.__maxNumberOfPages: num = self.__maxNumberOfPages

        self.__pageNum.set(str(num))
        self.__selectedPage = num

        if num == 1:
           self.__controllers["prev"].config(state = DISABLED)
        else:
           self.__controllers["prev"].config(state = NORMAL)


        if num >= self.__maxNumberOfPages:
           self.__controllers["next"].config(state = DISABLED)
        else:
           self.__controllers["next"].config(state = NORMAL)

        self.__removeAndFill(num)
        self.selectedChanged()
        self.__stopUs = False

    def __removeAndFill(self, page):
        offset = (self.__numberOfLines - 1) * (page - 1)

        for lineNum in range(0, self.__numberOfLines - 1):
            #print(lineNum, offset, len(self.__data))
            try:
                dataLine = self.__data[lineNum + offset]
            except:
                self.__data.append(["", "", "", "[]", "[]"])
                dataLine = self.__data[lineNum + offset]

            for subNum in range(0,5):
                name = str(lineNum) + "_" + str(subNum)

                if subNum < 2:
                   self.__entryVars[name].set(dataLine[subNum])
                else:
                   if dataLine[subNum] in ["", "[]"]:
                      self.__listBoxes[name].selectDefault()
                   else:
                      self.__listBoxes[name].deSelect()
                      self.__listBoxes[name].select(dataLine[subNum], True)

    def pageBefore(self):
        if self.__stopUs: return
        self.__stopUs = True
        self.__selectedPage -= 1
        #self.__countDownPageNum = 5
        #self.selectedChanged()
        #self.__pageNum.set(str(self.__selectedPage))

        self.__pageNum.set(str(self.__selectedPage))
        self.pageNumChangedThing(None)

    def pageAfter(self):
        if self.__stopUs: return
        self.__stopUs = True
        self.__selectedPage += 1
        #self.__countDownPageNum = 5
        #self.selectedChanged()
        #self.__pageNum.set(str(self.__selectedPage))

        self.__pageNum.set(str(self.__selectedPage))
        self.pageNumChangedThing(None)

    def callChangerDelayed(self, event):
        self.__countDown = 120

    def loop(self):
        from time import sleep
        while self.dead == False and self.__loader.mainWindow.dead == False:
            try:
               if self.__countDown > 0: self.__countDown -= 1
               if self.__countDown == 1:
                  self.callChanger(None)

               if self.__countDownPageNum > 0: self.__countDownPageNum -= 1
               if self.__countDownPageNum == 1:
                  if self.__stopUs: return
                  self.__stopUs = True
                  self.pageNumChangedThing(None)

            except Exception as e:
                #print(str(e))
                pass
            sleep(0.005)


    def callChanger(self, event):
        self.selectedChanged()

    def selectedChanged(self):
        if self.notInitAnymore: self.__controllers["ok"].config(state=NORMAL)

        multi  = self.__numberOfLines - 1
        offset = multi * (self.__selectedPage - 1)

        #allTheLines = []

        for num in range(0, self.__numberOfLines - 1):
            currentLine        = {}
            currentLinesHolder = {}
            entries            = {}
            for subNum in range(0, 5):
                name = str(num) + "_" + str(subNum)
                key  = self.__listOfColumnNames[subNum]

                if subNum in range(0, 2):
                   currentLinesHolder[key] = self.__entryVars[name]
                   entries[key]            = self.__entries[name]
                   currentLine[key]        = self.__entryVars[name].get()
                else:
                   currentLinesHolder[key] = self.__listBoxes[name]
                   currentLine[key]        = self.__listBoxes[name].getSelected()

                   if type(currentLine[key]) == list:
                      currentLine[key] = "[" + ",".join(currentLine[key]) + "]"

            lineNum = num + offset

            self.__checkCurrentLine(currentLine, currentLinesHolder, entries, lineNum)
            #allTheLines.append([currentLine, currentLinesHolder])

        if self.__maxNumberOfPages > 1:
           self.__pageNumE.config(state = NORMAL)
        else:
           self.__pageNumE.config(state = DISABLED)

    def __checkCurrentLine(self, currentLine, currentLinesHolder, entries, lineNum):
        keyOfName     = self.__listOfColumnNames[0]
        keyOfValue    = self.__listOfColumnNames[1]
        keyOfType     = self.__listOfColumnNames[2]
        keyOfBank     = self.__listOfColumnNames[3]
        keyOfSection  = self.__listOfColumnNames[4]

        nameOfName    = str(lineNum % 19) + "_0"
        nameOfValue   = str(lineNum % 19) + "_1"
        nameOfType    = str(lineNum % 19) + "_2"
        nameOfBank    = str(lineNum % 19) + "_3"
        nameOfSection = str(lineNum % 19) + "_4"

        stringDelimiters = self.__loader.config.getValueByKey("validStringDelimiters").split(" ")

        isThereValidValue = False
        for key in [keyOfName, keyOfValue, keyOfType, keyOfBank, keyOfSection]:
            if type(currentLinesHolder[key]) == StringVar:
               if currentLinesHolder[key].get() != "":
                  isThereValidValue = True
                  break

        if isThereValidValue == False:
           for key in (nameOfType, nameOfBank, nameOfSection):
               self.__listBoxes[key].selectDefault()
               self.__listBoxes[key].changeState(DISABLED)
           return

        self.__listBoxes[nameOfType].changeState(NORMAL)

        if type(currentLinesHolder[keyOfName]) == StringVar:
           name = currentLinesHolder[keyOfName].get()
        else:
           name = currentLinesHolder[keyOfName].getSelected()

        #if name == "": raise ValueError

        invalidName = False
        import re
        if len(re.findall(r'^[a-zA-Z][a-zA-Z0-9_-]+$', name)) == 0: invalidName = True
        if len(name) < 3: invalidName = True

        itsAlreadyThere = False
        for lineNum2 in range(0, len(self.__data)):
            if lineNum == lineNum2: continue

            if self.__data[lineNum2][0] == name:
               itsAlreadyThere = True
               break

        hasDelimiters = 0
        for d in stringDelimiters:
            if name[0] == d and name[-1] == d: name = name[1:-1]
            if d in name: hasDelimiters += 1

        if itsAlreadyThere == True or hasDelimiters == 3 or invalidName:
           entries[keyOfName].config(bg = self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                                      fg = self.__loader.colorPalettes.getColor("boxFontUnSaved")
                                      )
        else:
           entries[keyOfName].config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                      fg=self.__loader.colorPalettes.getColor("boxFontNormal")
                                      )

           if currentLinesHolder[keyOfName].get() != "":
              currentLine[keyOfName] = name
              currentLinesHolder[keyOfName].set(name)
              entries[keyOfName].icursor(len(name))


        if type(currentLinesHolder[keyOfValue]) == StringVar:
           value = currentLinesHolder[keyOfValue].get()
        else:
           value = currentLinesHolder[keyOfValue].getSelected()

        for d in stringDelimiters:
            if value.startswith(d) and value.endswith(d):
               value = value[1:-1]
               break

        if value.startswith("#"): value = value[1:]

        isNumOk = True
        if   value.startswith("%"):
             try:
                 number = int(value.replace("%", "0b"), 2)
                 if   number > 255:
                      number = number%256
                 elif number < 0:
                      number = 0

                 numberString = bin(number).replace("0b", "")
                 value        = "%" + ((8-len(numberString)) * "0") + numberString
             except:
                 isNumOk = False
        elif value.startswith("$"):
            try:
                number = int(value.replace("$", "0x"), 16)
                if number > 255:
                    number = number%256
                elif number < 0:
                    number = 0

                numberString = hex(number).replace("0x", "")
                value = "$" + ((2 - len(numberString)) * "0") + numberString
            except:
                isNumOk = False
        else:
            try:
                number = int(value)
                if number > 255:
                    number = 255
                elif number < 0:
                    number = 0

                value = str(number)
            except:
                isNumOk = False

        if isNumOk == False and currentLinesHolder[keyOfValue].get() != "":
           entries[keyOfValue].config(bg = self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                                      fg = self.__loader.colorPalettes.getColor("boxFontUnSaved")
                                      )
        else:
           entries[keyOfValue].config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                      fg=self.__loader.colorPalettes.getColor("boxFontNormal")
                                      )
           if currentLinesHolder[keyOfValue].get() != "":
              currentLine[keyOfValue] = value
              currentLinesHolder[keyOfValue].set(value)
              entries[keyOfValue].icursor(len(value))

        errorInAny = False
        keysAndValuesOfTypes = {}
        for key in self.__types:
            keysAndValuesOfTypes[key] = self.__loader.dictionaries.getWordFromCurrentLanguage(key)

        if   currentLine[keyOfType]                        == keysAndValuesOfTypes["global"]:
             currentLine[keyOfBank]                         = "[]"
             currentLine[keyOfSection]                      = "[]"
             self.__listBoxes[nameOfBank].changeState(   DISABLED)
             self.__listBoxes[nameOfSection].changeState(DISABLED)
        elif currentLine[keyOfType]                        == keysAndValuesOfTypes["bank"]:
             currentLine[keyOfSection]                      = "[]"
             self.__listBoxes[nameOfBank].changeState(   NORMAL)
             self.__listBoxes[nameOfSection].changeState(DISABLED)
        else:
             self.__listBoxes[nameOfBank].changeState(   NORMAL)
             self.__listBoxes[nameOfSection].changeState(NORMAL)

        #for key in [keyOfBank, keyOfSection]:
        #    if type(currentLine[key]) == str:
        #       currentLine[key] = currentLine[key][1:-1].split(",")

        if   currentLine[keyOfType]    == keysAndValuesOfTypes["bank"]\
        and  currentLine[keyOfBank]    ==  "[]"                         :
             errorInAny                 =  True

        elif currentLine[keyOfType]    == keysAndValuesOfTypes["section"] \
        and (currentLine[keyOfBank]    == "[]"
         or  currentLine[keyOfSection] == "[]"                            ):
             errorInAny                 = True

        #print(currentLine[keyOfType], keysAndValuesOfTypes["section"], currentLine[keyOfBank]  )

        if   currentLine[keyOfType]    == keysAndValuesOfTypes["section"] \
        and  currentLine[keyOfBank]    == "[Bank1]":
             newSections                = []
             for section in currentLine[keyOfSection][1:-1].split(","):
                 if section in self.__loader.bank1Sections:
                    newSections.append(section)
             currentLine[keyOfSection]  = "[" + ",".join(newSections) + "]"

        for key in [[nameOfBank, keyOfBank],[nameOfSection, keyOfSection]]:
            self.__listBoxes[key[0]].deSelect()
            if type(currentLine[key[1]]) == list:
                for item in currentLine[key[1]]:
                    self.__listBoxes[key[0]].select(item, True)
            else:
                self.__listBoxes[key[0]].select(currentLine[key[1]], True)

        if errorInAny == False and isNumOk and itsAlreadyThere == False and hasDelimiters < 3 and invalidName == False:

           #while len(self.__data) < self.__maxNumberOfPages * 19:
           #    self.__data.append(["", "", "", "[]", "[]"])

           self.__data[lineNum] = list(currentLine.values())
           for itemNum in range(3, 5):
               if type(self.__data[lineNum][itemNum]) == list:
                  self.__data[lineNum][itemNum] = "[" + ",".join(self.__data[lineNum][itemNum]) + "]"

           self.__controllers["ok"].config(state = NORMAL)
        else:
           self.__controllers["ok"].config(state = DISABLED)


    def __loadPage(self):
        multi  = self.__numberOfLines - 1
        offset = multi * (self.__selectedPage - 1)

        for num in range(0, multi):
            dataLineNum = num + offset

            for subNum in range(0, 5):
                name = str(num) + "_" + str(subNum)
                if subNum < 2:
                    self.__entryVars[name].set(self.__data[dataLineNum][subNum])
                else:
                    self.__listBoxes[name].deSelect()
                    self.__listBoxes[name].select(self.__data[dataLineNum][subNum])

        self.selectedChanged()

    def __saveData(self):
        path = self.__loader.mainWindow.projectPath + "bank1/constants.a26"
        f = open(path, "w")
        f.write('*** This is the location of user-defined constants.\n')
        for line in self.__data:
            if line != []:
               if line[0] != "":
                  for lNum in range(0, len(line)):
                      line[lNum] = line[lNum].replace(",", " ")

                  dictWord = line[2]
                  for typ in self.__types:
                      if self.__dictionaries.getWordFromCurrentLanguage(typ) == dictWord:
                         line[2] = typ
                         break

                  f.write(line[0] + "=" + ",".join(line[1:]) + "\n")
        f.close()

        self.__closeWindow()
        self.__loader.soundPlayer.playSound("success")

    def __loadData(self):
        path = self.__loader.mainWindow.projectPath + "bank1/constants.a26"
        f = open(path, "r")
        lines = f.read().replace("\r", "").split("\n")
        f.close()

        index         = -1
        for line in lines:
            if len(line) > 0:
                if line[0] not in ["*", "#"]:
                  index += 1
                  itemName = line.split("=")[0]
                  params   = line.split("=")[1].split(",")

                  for pNum in range(0, len(params)):
                      params[pNum] = params[pNum].replace(" ", ",")

                  self.__data.append([])
                  last = self.__data[-1]
                  last.append(itemName)

                  for item in params:
                      if item in self.__types:
                         last.append(self.__dictionaries.getWordFromCurrentLanguage(item))
                         params[params.index(item)] = self.__dictionaries.getWordFromCurrentLanguage(item)
                      else:
                         last.append(item)

                  if index < self.__numberOfLines - 1:
                     for subNum in range(0, 5):
                         name = str(index) + "_" + str(subNum)
                         if   subNum == 0:
                              self.__entryVars[name].set(itemName)
                         elif subNum == 1:
                              self.__entryVars[name].set(params[0])
                         else:
                              self.__listBoxes[name].deSelect()
                              self.__listBoxes[name].select(params[subNum - 1], True)
        self.selectedChanged()
        #for line in self.__data:
        #    print(line)