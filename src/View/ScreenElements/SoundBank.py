from tkinter import *
from ScreenSetterFrameBase import ScreenSetterFrameBase
import os
from time import sleep

class SoundBank:

    def __init__(self, loader, baseFrame, data, changeName, changeData, w, h, currentBank, blankAnimation,
                 topLevelWindow, itemNames):
        self.__loader = loader
        self.__baseFrame = baseFrame
        self.__data = data.split(" ")
        self.__w = w
        self.__h = h
        self.__currentBank = currentBank

        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs
        self.__fontManager = self.__loader.fontManager
        self.__fontSize = int(self.__screenSize[0] / 1300 * self.__screenSize[1] / 1050 * 14)
        self.__colors = self.__loader.colorPalettes
        self.__colorDict = self.__loader.colorDict

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize * 0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize * 0.65), False, False, False)
        self.__bigFont = self.__fontManager.getFont(int(self.__fontSize * 1.15), False, False, False)
        self.__bigFont2 = self.__fontManager.getFont(int(self.__fontSize * 1.5), False, False, False)

        self.__name = StringVar()
        self.__name.set(self.__data[0])
        self.dead = [False]
        self.__changeData = changeData

        self.__otherKeys = {
            "usedSound"     : "availableSound",
            "availableSound": "usedSound"
        }

        self.__soundList = []
        self.collectSound()

        if len(self.__soundList) != 0:
            wasHash = False
            if self.__data[2] == "#":
               wasHash = True
            self.__setterBase = ScreenSetterFrameBase(loader, baseFrame, data, self.__name, changeName, self.dead, itemNames)
            self.__addElements(wasHash)
        else:
            blankAnimation(["missing", {
                               "item": "soundFx", "folder": self.__loader.mainWindow.projectPath.split("/")[-2]+"/soundFx"
                           }])

    def collectSound(self):
        folder = self.__loader.mainWindow.projectPath + "soundFx"
        self.__sizes = {}

        self.__soundList = []
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith(".asm"):
                    self.__soundList.append(file[:-4])

                    f     = open(root + "/" + file)
                    lines = f.read().replace("\r", "").split("\n")
                    f.close()

                    for line in lines:
                        if "Bytes=" in line:
                            self.__sizes[file[:-4]] = int(line.split("Bytes=")[1])
                            break
        self.__soundList.sort()

    def wouldItFit(self, key):
        itemSize   = self.__sizes[key]
        sizeOfUsed = 0

        for k in self.__usedSounds:
            sizeOfUsed += self.__sizes[k]

        return sizeOfUsed + itemSize < 257

    def __addElements(self, wasHash):
        self.__setterBase.registerError("noSoundFx")

        self.__uniqueFrame = Frame(self.__baseFrame, width=self.__w,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h)

        self.__uniqueFrame.pack_propagate(False)
        self.__uniqueFrame.pack(side=TOP, anchor=N, fill=X)

        self.__errorText = StringVar()

        self.__errorLine = Label(self.__uniqueFrame, width=self.__w,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   fg=self.__loader.colorPalettes.getColor("font"),
                                   height=1,
                                   font = self.__smallFont,
                                   textvariable = self.__errorText
                                 )

        self.__errorLine.pack_propagate(False)
        self.__errorLine.pack(side=TOP, anchor=N, fill=X)

        self.__variables = []
        for address in self.__loader.virtualMemory.memory.keys():
            for variable in self.__loader.virtualMemory.memory[address].variables.keys():
                var = self.__loader.virtualMemory.memory[address].variables[variable]
                if (    (var.validity == "global" or
                         var.validity == self.__currentBank) and
                        (var.system == False or
                         var.iterable == True
                        ) and
                         var.type == "byte"):
                    self.__variables.append(address + "::" + variable)

        if self.__data[2]   == "#":
           self.__usedSounds = []
           self.__data[2]    = "||"
        else:
           self.__usedSounds = []
           usedSounds = self.__data[2][1:-1].split("|")

           for s in usedSounds:
               if s in self.__soundList:
                  self.__usedSounds.append(s)

        self.__availableSounds = []
        for s in self.__soundList:
            if s not in self.__usedSounds:
               self.__availableSounds.append(s)

        self.__bankFrame = Frame(self.__uniqueFrame, width=self.__w // 5 * 2,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h)

        self.__bankFrame.pack_propagate(False)
        self.__bankFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__varFrame = Frame(self.__uniqueFrame, width=self.__w // 5 * 3,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h)

        self.__varFrame.pack_propagate(False)
        self.__varFrame.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__keysAndListBoxes = {"usedSound": [self.__usedSounds, ">>"], "availableSound": [self.__availableSounds, "<<"]}

        self.__framesAndOtherNotNeeded = []

        self.__soundListBoxes   = {}
        for key in self.__keysAndListBoxes:
            f = Frame(self.__bankFrame, width=self.__w // 5,
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       height=self.__h)

            f.pack_propagate(False)
            f.pack(side=LEFT, anchor=E, fill=Y)

            fLabel = Frame(f, width=self.__w // 5,
                      bg=self.__loader.colorPalettes.getColor("window"),
                      height=self.__h // 20)

            fLabel.pack_propagate(False)
            fLabel.pack(side=TOP, anchor=N, fill=X)

            fListBox = Frame(f, width=self.__w // 5,
                      bg=self.__loader.colorPalettes.getColor("window"),
                      height=self.__h // 20 * 15)

            fListBox.pack_propagate(False)
            fListBox.pack(side=TOP, anchor=N, fill=X)

            fButton = Frame(f, width=self.__w // 5,
                      bg=self.__loader.colorPalettes.getColor("window"),
                      height=self.__h // 20 * 3)

            fButton.pack_propagate(False)
            fButton.pack(side=TOP, anchor=N, fill=BOTH)

            self.__framesAndOtherNotNeeded.append(f)
            self.__framesAndOtherNotNeeded.append(fLabel)
            self.__framesAndOtherNotNeeded.append(fListBox)
            self.__framesAndOtherNotNeeded.append(fButton)

            l = Label(fLabel, width=self.__w // 5,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              fg=self.__loader.colorPalettes.getColor("font"),
                              font = self.__normalFont,
                              text = self.__dictionaries.getWordFromCurrentLanguage(key),
                              height=self.__h)

            l.pack_propagate(False)
            l.pack(side=LEFT, anchor=E, fill=BOTH)

            sBar = Scrollbar(fListBox)
            lBox = Listbox(fListBox, width=100000,
                            name="listBox_" + key, height=1000,
                            yscrollcommand=sBar.set, selectmode=BROWSE,
                            exportselection=False, font=self.__smallFont,
                            justify=LEFT)

            lBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
            lBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
            lBox.pack_propagate(False)

            sBar.pack(side=RIGHT, anchor=W, fill=Y)
            lBox.pack(side=LEFT, anchor=W, fill=BOTH)

            sBar.config(command=lBox.yview)

            self.__framesAndOtherNotNeeded.append(sBar)
            self.__soundListBoxes[key]                 = {}
            self.__soundListBoxes[key]["listBox"]      = lBox
            self.__soundListBoxes[key]["varList"]      = self.__keysAndListBoxes[key][0]

            for item in self.__keysAndListBoxes[key][0]:
                lBox.insert(END, item)

            self.__soundListBoxes[key]["listBox"].select_clear(0, END)
            self.__soundListBoxes[key]["listBox"].select_set(0)

            b = Button(fButton,   width=self.__w // 5, name = "button_" + key,
                                  bg=self.__loader.colorPalettes.getColor("window"),
                                  fg=self.__loader.colorPalettes.getColor("font"),
                                  font = self.__bigFont,
                                  text = self.__keysAndListBoxes[key][1],
                                  height=self.__h)
            b.pack_propagate(False)
            b.pack(fill=BOTH)

            self.__soundListBoxes[key]["button"] = b

            self.__loader.threadLooper.bindingMaster.addBinding(self, b   , "<Button-1>"       , self.__listBoxChange, 1)
            self.__loader.threadLooper.bindingMaster.addBinding(self, lBox, "<Double-Button-1>", self.__listBoxChange, 1)

        self.__secondKeyList      = []
        self.__labelNames         = {}
        self.__numberOfCheckBoxes = int(self.__data[3])

        self.__secondOther        = {}

        for num in range (0, 2):
            self.__secondKeyList.append("channelß".replace("ß", str(num)))
            self.__labelNames["channelß".replace("ß", str(num))] = \
                  self.__dictionaries.getWordFromCurrentLanguage("channelß").replace("ß", str(num))
            self.__secondOther["channelß".replace("ß", str(num))] = "channelß".replace("ß", str(1 - num))

        self.__varSetters = {}
        for key in self.__secondKeyList:
            self.__varSetters[key] = {}

            f = Frame(self.__varFrame, width=round(self.__w // 5 * 1.5),
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       height=self.__h)
            f.pack_propagate(False)
            f.pack(side=LEFT, anchor=E, fill=Y)

            fLabel = Frame(f, width=self.__w // 5,
                      bg=self.__loader.colorPalettes.getColor("window"),
                      height=self.__h // 20)

            fLabel.pack_propagate(False)
            fLabel.pack(side=TOP, anchor=N, fill=X)

            l = Label(fLabel, width=round(self.__w // 5 * 1.5),
                              bg=self.__loader.colorPalettes.getColor("window"),
                              fg=self.__loader.colorPalettes.getColor("font"),
                              font = self.__normalFont,
                              text = self.__labelNames[key],
                              height=self.__h)

            l.pack_propagate(False)
            l.pack(side=LEFT, anchor=E, fill=BOTH)

            self.__framesAndOtherNotNeeded.append(f)
            self.__framesAndOtherNotNeeded.append(fLabel)
            self.__framesAndOtherNotNeeded.append(l)

            fCheckBox = Frame(f, width=round(self.__w // 5 * 1.5),
                                  bg=self.__loader.colorPalettes.getColor("window"),
                                  height=self.__h // 20)

            fCheckBox.pack_propagate(False)
            fCheckBox.pack(side=TOP, anchor=N, fill=X)

            self.__framesAndOtherNotNeeded.append(fCheckBox)

            cButtonVal = IntVar()
            cButton = Checkbutton(fCheckBox,
                                  name="checkBox_"+key,
                                  text=self.__dictionaries.getWordFromCurrentLanguage("enabled"),
                                  bg=self.__colors.getColor("window"),
                                  fg=self.__colors.getColor("font"),
                                  justify=LEFT, font=self.__normalFont,
                                  variable=cButtonVal,
                                  activebackground=self.__colors.getColor("highLight"),
                                  activeforeground=self.__loader.colorPalettes.getColor("font"),
                                  )

            cButton.pack_propagate(False)
            cButton.pack(fill=BOTH, side=TOP, anchor=CENTER)

            self.__varSetters[key]["enabledVar"] = cButtonVal
            self.__varSetters[key]["enabled"]    = cButton

            fListBoxes = Frame(f, width=round(self.__w // 5 * 1.5),
                                  bg=self.__loader.colorPalettes.getColor("window"),
                                  height=self.__h)
            fListBoxes.pack_propagate(False)
            fListBoxes.pack(side=TOP, anchor=N, fill=BOTH)

            fListBoxes_1 = Frame(fListBoxes, width=round(self.__w // 5 * 1.5) // 2,
                                  bg=self.__loader.colorPalettes.getColor("window"),
                                  height=self.__h)
            fListBoxes_1.pack_propagate(False)
            fListBoxes_1.pack(side=LEFT, anchor=E, fill=Y)

            fListBoxes_2 = Frame(fListBoxes, width=round(self.__w // 5 * 1.5) // 2,
                                  bg=self.__loader.colorPalettes.getColor("window"),
                                  height=self.__h)
            fListBoxes_2.pack_propagate(False)
            fListBoxes_2.pack(side=LEFT, anchor=E, fill=Y)

            self.__framesAndOtherNotNeeded.append(fListBoxes)
            self.__framesAndOtherNotNeeded.append(fListBoxes_1)
            self.__framesAndOtherNotNeeded.append(fListBoxes_2)

            f1        = Label(fListBoxes_1, width=round(self.__w // 5 * 1.5) // 2,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              fg=self.__loader.colorPalettes.getColor("font"),
                              font = self.__smallFont,
                              text = self.__dictionaries.getWordFromCurrentLanguage("byteSound"),
                              height=1)

            f1.pack_propagate(False)
            f1.pack(side=TOP, anchor=N, fill=X)

            f2        = Label(fListBoxes_2, width=round(self.__w // 5 * 1.5) // 2,
                                  bg=self.__loader.colorPalettes.getColor("window"),
                                  fg=self.__loader.colorPalettes.getColor("font"),
                                  font = self.__smallFont,
                                  text = self.__dictionaries.getWordFromCurrentLanguage("bytePointer"),
                                  height=1)

            f2.pack_propagate(False)
            f2.pack(side=TOP, anchor=N, fill=X)

            self.__framesAndOtherNotNeeded.append(f1)
            self.__framesAndOtherNotNeeded.append(f2)

            fListBoxes_1BoxF = Frame(fListBoxes_1, width=round(self.__w // 5 * 1.5) // 2,
                                  bg=self.__loader.colorPalettes.getColor("window"),
                                  height=self.__h)
            fListBoxes_1BoxF.pack_propagate(False)
            fListBoxes_1BoxF.pack(side=TOP, anchor=N, fill=BOTH)

            fListBoxes_2BoxF = Frame(fListBoxes_2, width=round(self.__w // 5 * 1.5) // 2,
                                  bg=self.__loader.colorPalettes.getColor("window"),
                                  height=self.__h)
            fListBoxes_2BoxF.pack_propagate(False)
            fListBoxes_2BoxF.pack(side=TOP, anchor=N, fill=BOTH)

            self.__framesAndOtherNotNeeded.append(fListBoxes_1BoxF)
            self.__framesAndOtherNotNeeded.append(fListBoxes_2BoxF)

            sBar1 = Scrollbar(fListBoxes_1BoxF)
            lBox1 = Listbox(fListBoxes_1BoxF, width=100000,
                           name="listBox_Sound_" + key, height=1000,
                           yscrollcommand=sBar1.set, selectmode=BROWSE,
                           exportselection=False, font=self.__smallFont,
                           justify=LEFT)

            lBox1.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
            lBox1.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
            lBox1.pack_propagate(False)

            sBar1.pack(side=RIGHT, anchor=W, fill=Y)
            lBox1.pack(side=LEFT, anchor=W, fill=BOTH)
            sBar1.config(command=lBox1.yview)

            sBar2 = Scrollbar(fListBoxes_2BoxF)
            lBox2 = Listbox(fListBoxes_2BoxF, width=100000,
                           name="listBox_Pointer_" + key, height=1000,
                           yscrollcommand=sBar2.set, selectmode=BROWSE,
                           exportselection=False, font=self.__smallFont,
                           justify=LEFT)

            lBox2.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
            lBox2.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
            lBox2.pack_propagate(False)

            sBar2.pack(side=RIGHT, anchor=W, fill=Y)
            lBox2.pack(side=LEFT, anchor=W, fill=BOTH)
            sBar2.config(command=lBox2.yview)

            self.__framesAndOtherNotNeeded.append(sBar1)
            self.__framesAndOtherNotNeeded.append(sBar2)

            self.__varSetters[key]["listBox_Sound"]        = lBox1
            self.__varSetters[key]["listBox_Pointer"]      = lBox2

            self.__varSetters[key]["lastSelected_Sound"]   = 0
            self.__varSetters[key]["lastSelected_Pointer"] = 0

            for item in self.__variables:
                lBox1.insert(END, item)
                lBox2.insert(END, item)

            theNum = int(key[-1])
            kkk = ["lastSelected_Sound", "lastSelected_Pointer"]

            for kNum in range(0, 2):
                dataNum = 4 + (theNum * 2) + kNum

                if self.__data[dataNum] == "#":
                   self.__data[dataNum] = self.__variables[0]
                else:
                   for varNum in range(0, len(self.__variables)):
                       if self.__variables[varNum] == self.__data[dataNum]:
                           self.__varSetters[key][kkk[kNum]] = varNum
                           break

            if self.__numberOfCheckBoxes in (theNum, 2):
               self.__varSetters[key]["enabledVar"].set(1)
               self.__varSetters[key]["enabledVarWas"] = 1
            else:
               self.__varSetters[key]["listBox_Sound"]  .config(state = DISABLED)
               self.__varSetters[key]["listBox_Pointer"].config(state = DISABLED)
               self.__varSetters[key]["enabledVarWas"] = 0

            self.__varSetters[key]["listBox_Sound"]  .select_clear(0, END)
            self.__varSetters[key]["listBox_Pointer"].select_clear(0, END)

            self.__varSetters[key]["listBox_Sound"]  .select_set(self.__varSetters[key]["lastSelected_Sound"]  )
            self.__varSetters[key]["listBox_Pointer"].select_set(self.__varSetters[key]["lastSelected_Pointer"])

            self.addListBoxBindings(lBox1, self.lBoxChanged)
            self.addListBoxBindings(lBox2, self.lBoxChanged)

            self.__loader.threadLooper.bindingMaster.addBinding(self, cButton, "<ButtonRelease-1>",
                                                                self.optionChanged, 1)

        self.__loader.threadLooper.addToThreading(self, self.loop, [], 1)
        self.setErrorLabel()

    def setErrorLabel(self):
        if self.__usedSounds == []:
            self.__errorLine.config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                                    fg=self.__loader.colorPalettes.getColor("boxFontUnSaved"))
            self.__errorText.set(self.__dictionaries.getWordFromCurrentLanguage("soundBankError"))
        else:
            counting = []
            activeOnes = int(self.__data[3])

            duplicate  = False
            for itemNum in range(4, 8):
                sectorNum = (itemNum - 4) // 2
                if sectorNum != activeOnes and activeOnes != 2:
                   continue

                if self.__data[itemNum] not in counting:
                   counting.append(self.__data[itemNum])
                else:
                   duplicate = True
                   break

            if duplicate:
                self.__errorLine.config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                                        fg=self.__loader.colorPalettes.getColor("boxFontUnSaved"))
                self.__errorText.set(self.__dictionaries.getWordFromCurrentLanguage("soundBankError2"))
            else:
                self.__errorLine.config(bg=self.__loader.colorPalettes.getColor("window"),
                                        fg=self.__loader.colorPalettes.getColor("font"))
                self.__errorText.set("")


    def optionChanged(self, event):
        button  = event.widget
        key    = str(button).split(".")[-1].split("_")[-1]

        if button["state"] == DISABLED: return

        self.__varSetters[key]["enabledVarWas"] = 1 - self.__varSetters[key]["enabledVarWas"]

        if self.__varSetters[key]["enabledVarWas"] == 0:
           self.__data[3] = str(1 - self.__secondKeyList.index(key))
        else:
           self.__data[3] = "2"

        valKeys  = ["lastSelected_Sound", "lastSelected_Pointer"]
        boxNames = ["listBox_Sound"     , "listBox_Pointer"]

        if self.__varSetters[key]["enabledVarWas"] == 1:
           for subKeyNum in range(0, 2):
               self.__varSetters[key][boxNames[subKeyNum]].select_clear(0, END)
               self.__varSetters[key][boxNames[subKeyNum]].select_set(self.__varSetters[key][valKeys[subKeyNum]])

               dataNum = 4 + (self.__secondKeyList.index(key) * 2) + subKeyNum
               self.__data[dataNum] = self.__variables[self.__varSetters[key][valKeys[subKeyNum]]]

        self.__changeData(self.__data)

    def lBoxChanged(self, event):
        lbox   = event.widget
        key    = str(lbox).split(".")[-1].split("_")[-1]
        typ    = str(lbox).split(".")[-1].split("_")[-2]

        if lbox["state"] == DISABLED: return

        valKeys  = ["lastSelected_Sound", "lastSelected_Pointer"]
        boxNames = ["listBox_Sound"     , "listBox_Pointer"]

        typs     = ["Sound", "Pointer"]

        typNum   = typs.index(typ)
        dataNum  = 4 + (self.__secondKeyList.index(key) * 2) + typNum

        self.__varSetters[key][valKeys[typNum]] = self.__varSetters[key][boxNames[typNum]].curselection()[0]

        self.__data[dataNum] = self.__variables[self.__varSetters[key][valKeys[typNum]]]
        self.__changeData(self.__data)
        self.setErrorLabel()

    def addListBoxBindings(self, lBox, func):
        for txt in ["<ButtonRelease-1>", "<KeyRelease-Up>", "<KeyRelease-Down>"]:
            self.__loader.threadLooper.bindingMaster.addBinding(self, lBox, txt,
                                                                func, 1)

    def loop(self):
        for key in self.__soundListBoxes:
            if len(self.__soundListBoxes[key]["varList"]) == 0:
               state = DISABLED
            else:
               state = NORMAL

            if key == "availableSound":
               if len(self.__soundListBoxes["usedSound"]["varList"]) > 31: state = DISABLED

               try:
                   selectNum = self.__soundListBoxes[key]["listBox"].curselection()[0]
               except:
                   selectNum = 0

               theOne = self.__soundListBoxes[key]["varList"][selectNum]
               if self.wouldItFit(theOne) == False: state = DISABLED

            try:
                #self.__soundListBoxes[key]["listBox"].config(state = state)
                self.__soundListBoxes[key]["button"] .config(state = state)
            except:
                pass

            try:
                for key in self.__secondKeyList:
                    if self.__varSetters[key]["enabledVar"].get() == 0:
                       self.__varSetters[self.__secondOther[key]]["enabledVar"].set(1)
                       state      = DISABLED
                       otherState = NORMAL
                    else:
                       state      = NORMAL
                       otherState = None

                    self.__varSetters[self.__secondOther[key]]["enabled"]        .config(state=state)
                    self.__varSetters[key]["listBox_Sound"]                      .config(state=state)
                    self.__varSetters[key]["listBox_Pointer"]                    .config(state=state)
                    if otherState != None:
                       self.__varSetters[self.__secondOther[key]]["listBox_Sound"]  .config(state=otherState)
                       self.__varSetters[self.__secondOther[key]]["listBox_Pointer"].config(state=otherState)
            except:
                pass

    def __listBoxChange(self, event):
        entry  = event.widget
        key    = str(entry).split(".")[-1].split("_")[-1]

        if type(entry) == Listbox and len(self.__soundListBoxes[key]["varList"]) == 0: return

        otherKey = self.__otherKeys[key]

        try:
            selectNum = self.__soundListBoxes[key]["listBox"].curselection()[0]
        except:
            selectNum = 0

        theOne = self.__soundListBoxes[key]["varList"][selectNum]
        if key == "availableSound":
           if len(self.__soundListBoxes["usedSound"]["varList"]) > 31: return
           if self.wouldItFit(theOne) == False: return

        self.__soundListBoxes[key]["varList"].remove(theOne)
        self.__soundListBoxes[key]["listBox"].select_clear(0, END)
        self.__soundListBoxes[key]["listBox"].delete(selectNum)

        if len(self.__soundListBoxes[key]["varList"]) > 0:
            try:
                self.__soundListBoxes[key]["listBox"].select_set(theOne)
            except:
                try:
                    self.__soundListBoxes[key]["listBox"].select_set(theOne - 1)
                except:
                    try:
                        self.__soundListBoxes[key]["listBox"].select_set(theOne + 1)
                    except:
                        self.__soundListBoxes[key]["listBox"].select_set(0)

        self.__soundListBoxes[otherKey]["varList"].append(theOne)
        self.__soundListBoxes[otherKey]["varList"].sort()
        self.__soundListBoxes[otherKey]["listBox"].select_clear(0, END)

        self.__soundListBoxes[otherKey]["listBox"].delete(0, END)
        for item in self.__soundListBoxes[otherKey]["varList"]:
            self.__soundListBoxes[otherKey]["listBox"].insert(END, item)

        index = self.__soundListBoxes[otherKey]["varList"].index(theOne)
        self.__soundListBoxes[otherKey]["listBox"].select_set(index)
        self.__soundListBoxes[otherKey]["listBox"].see(index)
        self.__soundListBoxes[otherKey]["listBox"].yview(index)

        theseAre = "|" + "|".join(self.__usedSounds) + "|"
        if self.__data[2] != theseAre:
           self.__data[2]  = theseAre
           self.__changeData(self.__data)
           self.setErrorLabel()





