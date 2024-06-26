from tkinter import *
from SubMenu import SubMenu
from time import sleep

class ScreenTopTester:

    def __init__(self, loader, caller, codeData, boss):

        self.__loader = loader
        self.__mainWindow = self.__loader.mainWindow
        self.dead = False
        self.__caller   = caller
        self.__codeData = codeData
        self.__counter = 0
        self.__lastEvent = None

        self.__bossWindow = boss

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

        self.__sizes = [self.__screenSize[0] // 4, self.__screenSize[1] // 3.75]

        self.__loader.threadLooper.addToThreading(self, self.decrementCounter, [], 2)
        #c = Thread(target = self.decrementCounter)
        #c.daemon = True
        #c.start()

        self.__didOnce = False
        self.__window = SubMenu(self.__loader, "screenTester", self.__sizes[0], self.__sizes[1], None, self.__addElements,
                                2)
        self.dead = True

    def bossFocus(self):
        if self.__didOnce == False:
           self.__didOnce  = True
           self.__bossWindow.deiconify()
           self.__bossWindow.focus()

    def decrementCounter(self):
        #while self.dead == False and self.__mainWindow.dead == False:
            if self.__counter > 0 : self.__counter -= 1
            if self.__counter == 1:
                self.checkEntry(self.__lastEvent)
            sleep(0.01)

    def __closeWindow(self):
        self.dead = True
        self.__topLevelWindow.destroy()
        self.bossFocus()

        self.__loader.topLevels.remove(self.__topLevelWindow)
        self.__caller.answer = "NOPE"

    def __addElements(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()
        self.__topLevelWindow.protocol('WM_DELETE_WINDOW', self.__closeWindow)

        self.__title    = Label(self.__topLevelWindow,
                                text=self.__dictionaries.getWordFromCurrentLanguage("screenTester"),
                                font=self.__normalFont, fg=self.__colors.getColor("font"),
                                bg=self.__colors.getColor("window"), justify=CENTER
                                )

        self.__title.pack_propagate(False)
        self.__title.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__frames = []
        self.__Y      = 0

        YSizes = [6.5, 6.5, 6.5, 6.5, 9, 6]

        for num in range(0, 6):
            self.__frames.append({})

            line    = Frame(self.__topLevelWindow, width=self.__sizes[0],
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = self.__sizes[1] // YSizes[num])
            line.pack_propagate(False)
            line.pack(side=TOP, anchor=N, fill=X)

            self.__frames[num]["lineFrame"] = line

            three = ["leftFrame", "middleFrame", "rightFrame"]
            two   = ["leftFrame", "rightFrame"]

            if num < 4:
                for num2 in range(0, 3):
                    f = Frame(self.__frames[num]["lineFrame"], width=self.__sizes[0]//3,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 6)
                    f.pack_propagate(False)
                    f.pack(side=LEFT, anchor=E, fill=Y)

                    self.__frames[num][three[num2]] = f
            elif num == 4:
                for num2 in range(0, 2):
                    f = Frame(self.__frames[num]["lineFrame"], width=self.__sizes[0]//2,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 7)
                    f.pack_propagate(False)
                    f.pack(side=LEFT, anchor=E, fill=Y)

                    self.__frames[num][two[num2]] = f


        self.__lines      = []

        for num in range(0,4):
            self.__lines.append({})

            label1 = Label(self.__frames[num]["leftFrame"],
                                 text="-",
                                 font=self.__smallFont, fg=self.__colors.getColor("font"),
                                 bg=self.__colors.getColor("window"), justify=CENTER
                                 )

            label1.pack_propagate(False)
            label1.pack(side=TOP, anchor=CENTER, fill=BOTH)

            label2 = Label(self.__frames[num]["middleFrame"],
                                 text="-",
                                 font=self.__normalFont, fg=self.__colors.getColor("font"),
                                 bg=self.__colors.getColor("window"), justify=CENTER
                                 )

            label2.pack_propagate(False)
            label2.pack(side=TOP, anchor=CENTER, fill=BOTH)

            self.__lines[num]["variable"] = label1
            self.__lines[num]["varType"]  = label2

            entryVal = StringVar()

            entry = Entry(self.__frames[num]["rightFrame"], textvariable = entryVal,
                    name = "entry_"+str(num),
                    bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                    fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                    width=99999, font=self.__smallFont, state = DISABLED, justify = CENTER
                    )
            entry.pack_propagate(False)
            entry.pack(side=TOP, anchor=N, fill=BOTH)

            self.__loader.threadLooper.bindingMaster.addBinding(self, entry, "<KeyPress>"  , self.startCounter, 2)
            self.__loader.threadLooper.bindingMaster.addBinding(self, entry, "<KeyRelease>", self.checkEntry  , 2)
            self.__loader.threadLooper.bindingMaster.addBinding(self, entry, "<FocusOut>"  , self.checkEntry  , 2)

            #entry.bind("<KeyPress>", self.startCounter)
            #entry.bind("<KeyRelease>", self.checkEntry)
            #entry.bind("<FocusOut>", self.checkEntry)

            self.__lines[num]["entry"] = entry
            self.__lines[num]["value"] = entryVal
            self.__lines[num]["state"] = DISABLED

        self.__prevButton = Button(self.__frames[4]["leftFrame"], 
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   text = "<<",
                                   width= 99999999, height = 999999999,
                                   state=DISABLED, font = self.__normalFont,
                                   fg = self.__loader.colorPalettes.getColor("font"),
                                   command=self.__prev)

        self.__prevButton.pack_propagate(False)
        self.__prevButton.pack(fill=BOTH, side = LEFT, anchor = E)

        self.__nextButton = Button(self.__frames[4]["rightFrame"],
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   text = ">>",
                                   width= 99999999, height = 999999999,
                                   state=DISABLED, font = self.__normalFont,
                                   fg = self.__loader.colorPalettes.getColor("font"),
                                   command=self.__next)

        self.__nextButton.pack_propagate(False)
        self.__nextButton.pack(fill=BOTH, side = LEFT, anchor = E)

        sai_X = 1253
        sai_Y = 390

        size_Y = self.__sizes[1]//YSizes[5]
        size_X = round(sai_X * (size_Y / sai_Y))

        self.__saitama = self.__loader.io.getImg("saitama", (size_X, int(size_Y)))
        self.__okButton = Button(self.__frames[5]["lineFrame"], activebackground = "black",
                                   bg="black",
                                   image = self.__saitama,
                                   width= 99999999, height = 999999999,
                                   command=self.__OK)

        self.__okButton.pack_propagate(False)
        self.__okButton.pack(fill=BOTH, side = LEFT, anchor = E)

        self.__variableList = {}

        vvv = {}

        counter = self.__loader.virtualMemory.getVariableByName2("counter")
        random  = self.__loader.virtualMemory.getVariableByName2("random")

        for screenPart in self.__codeData.keys():
            for datas in self.__codeData[screenPart]:
                for dataLine in datas[2]:
                    line = dataLine.split(" ")
                    for item in line:
                        variable = self.__loader.virtualMemory.getVariableByName2(item)
                        if variable == counter or variable == random: continue

                        if variable != False:
                           vvv[item] = [variable.type, "0"]

                        try:
                            variable = self.__loader.virtualMemory.getVariableByName2(item.split("::")[1])
                            if variable == counter or variable == random: continue

                            if variable != False:
                               vvv[item] = [variable.type, "0"]
                        except:
                            pass


        keys = list(vvv.keys())
        keys.sort()

        for key in keys:
            self.__variableList[key] = vvv[key]

        self.__fillStuff()
        self.__topLevelWindow.deiconify()
        self.__topLevelWindow.focus()

    def startCounter(self, event):
        self.__lastEvent = event
        self.__counter = 80

    def __fillStuff(self):
        if self.__Y == 0: self.__prevButton.config(state = DISABLED)
        else: self.__prevButton.config(state = NORMAL)

        if self.__Y >= len(self.__variableList) // 4: self.__nextButton.config(state = DISABLED)
        else: self.__nextButton.config(state = NORMAL)

        for lineNum in range(0, 4):
            itemNum = lineNum + self.__Y

            try:
                item = list(self.__variableList.keys())[itemNum]
                self.__lines[lineNum]["variable"].config(text = item)
                self.__lines[lineNum]["varType"].config(text = self.__variableList[item][0])
                self.__lines[lineNum]["value"].set(self.__variableList[item][1])
                self.__lines[lineNum]["entry"].config(state = NORMAL)
                self.__lines[lineNum]["state"] = NORMAL
                self.__lines[lineNum]["entry"].config(bg = self.__loader.colorPalettes.getColor("boxBackNormal"),
                                                      fg = self.__loader.colorPalettes.getColor("boxFontNormal"))

            except Exception as e:
                self.__lines[lineNum]["variable"].config(text = "-")
                self.__lines[lineNum]["variable"].config(text = "-")
                self.__lines[lineNum]["value"].set("")
                self.__lines[lineNum]["entry"].config(state = DISABLED)
                self.__lines[lineNum]["state"] = DISABLED

    def __prev(self):
        self.__Y -= 4
        self.__fillStuff()

    def __next(self):
        self.__Y += 4
        self.__fillStuff()

    def checkEntry(self, event):
        if "KeyRelease" in str(event) and self.__counter > 1:
            self.__lastEvent = event
            return

        num = int(str(event.widget).split(".")[-1].split("_")[-1])
        if self.__lines[num]["state"] == DISABLED: return

        mode = "dec"
        if   self.__lines[num]["value"].get().startswith("$"): mode = "hex"
        elif self.__lines[num]["value"].get().startswith("%"): mode = "bin"
        elif self.__lines[num]["value"].get().startswith("/-"): mode = "decr"
        elif self.__lines[num]["value"].get().startswith("/"): mode = "inc"

        try:
            val = 0
            if   mode == "dec":
                val = int(self.__lines[num]["value"].get())
            elif mode == "hex":
                val = int(self.__lines[num]["value"].get().replace("$", "0x"), 16)
            elif mode in ("inc", "decr"):
                if mode == "inc":
                    val = int(self.__lines[num]["value"].get()[1:])
                else:
                    val = int(self.__lines[num]["value"].get()[2:])

                if val == 0: val = 1
                if val != 1:
                    val -=1
                    val = bin(val).replace("0b", "")
                    while len(val) < 8:
                        val = "0" + val
                    firstOne = 0
                    for num2 in range(0, 8):
                        if val[num2] == "1":
                            firstOne = num2
                            break

                    val = val[:firstOne] + "1" * (8-firstOne)
                    val = int("0b"+val, 2) + 1

            else:
                val = int(self.__lines[num]["value"].get().replace("%", "0b"), 2)

            self.__lines[num]["entry"].config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                              fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        except Exception as e:
            #print(str(e))
            self.__lines[num]["entry"].config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                                              fg=self.__loader.colorPalettes.getColor("boxFontUnSaved"))
            return

        maxValues = { "bit": 1, "doubleBit": 3, "tripleBit": 7, "nibble": 15, "byte": 255 }

        if val < 0: val = 0

        if val > maxValues[self.__lines[num]["varType"].cget("text")]:\
           val = maxValues[self.__lines[num]["varType"].cget("text")]

        if   mode == "dec": self.__lines[num]["value"].set(str(val))
        elif mode == "inc": self.__lines[num]["value"].set("/"+str(val))
        elif mode == "decr": self.__lines[num]["value"].set("/-"+str(val))

        elif mode == "hex":
            temp = hex(val).replace("0x", "")
            if len(temp) == 1: temp = "0" + temp
            self.__lines[num]["value"].set("$"+ temp.upper())
        else:
            temp = bin(val).replace("0b", "")
            while len(temp) < 8: temp = "0" + temp
            self.__lines[num]["value"].set("%"+ temp)

        self.__variableList[self.__lines[num]["variable"].cget("text")][1] = self.__lines[num]["value"].get()

    def __OK(self):
        self.__caller.initCode     = ""
        self.__caller.overScanCode = ""

        xxx = ""
        yyy = ""

        testCounter = 0

        from Compiler import Compiler

        self.bossFocus()

        for variable in self.__variableList.keys():
            if "::" in variable:
                variableName = variable.split("::")[1]
            else:
                variableName = variable

            if self.__variableList[variable][1].startswith("/") == False:
                tempText = "\tLDA\t#" + self.__variableList[variable][1] + "\n"
                theVar = self.__loader.virtualMemory.getVariableByName2(variableName)
                c = Compiler(None, None, "dummy", None)
                tempText += c.convertAnyTo8Bits(theVar.usedBits) + "\tSTA\t" + variableName + "\n"
                yyy += tempText

            else:
                tempText = "\tLDA\tcounter\n"
                incrementer = 0
                if self.__variableList[variable][1].startswith("/-"):
                    incrementer = int(self.__variableList[variable][1][2:])-1
                else:
                    incrementer = int(self.__variableList[variable][1][1:])-1

                if incrementer > 0:
                   tempText += "\tAND\t#"+str(incrementer)+"\n\tCMP\t#"+str(incrementer) + "\n"
                   label = "ThisIsAReallyImportantLabel_"+str(testCounter)
                   testCounter += 1
                   if self.__variableList[variable][1].startswith("/-"):
                       tempText += "\tBNE\t" + label + "\n" + "\tDEC\t" + variableName + "\n" + label + "\n"
                   else:
                       tempText += "\tBNE\t"+label+"\n" + "\tINC\t"+ variableName + "\n" + label + "\n"
                else:
                   if self.__variableList[variable][1].startswith("/-"):
                      tempText += "\tSTA\titem\n\tLDA\t#255\n\tSEC\n\tSBC\titem\n"

                   tempText += "\tSTA\t" + variableName + "\n"

                xxx += tempText

        self.__closeWindow()
        self.__caller.initCode = yyy
        self.__caller.overScanCode = xxx
        self.__soundPlayer.playSound("Okay")
        self.__caller.answer   = "OK"




