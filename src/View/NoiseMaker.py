from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from Compiler import Compiler
from time import sleep
from VisualEditorFrameWithLabelAndEntry import VisualEditorFrameWithLabelAndEntry
from FortariMB import FortariMB
import os
from PIL import ImageTk, Image as IMAGE
from TiaTone import TiaTone
from VisualLoaderFrame import VisualLoaderFrame

class NoiseMaker:

    def __init__(self, loader):
        self.__loader = loader
        self.__mainWindow = self.__loader.mainWindow

        self.dead = False
        self.changed = False
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

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize*0.65), False, False, False)
        self.__bigFont = self.__fontManager.getFont(int(self.__fontSize*1.15), False, False, False)
        self.__bigFont2 = self.__fontManager.getFont(int(self.__fontSize*1.5), False, False, False)

        self.__finished   = [False, False, False]
        self.__sawRising  = 89
        self.__sawIndex   = 0
        self.__firstSound = True
        self.__lastIndex  = -1
        self.__saws       = [None, None]
        self.__saveIndex  = 1
        self.__tia        = TiaTone()

        self.__playingSawAttackSound = 0
        self.__playingAnySawSound    = 0
        self.__onSaw = False
        self.__dont  = False
        self.__channelSkip = [0, 11, 5, 10, 9, 13]

        self.__wWw = 32

        self.__sizes = [self.__screenSize[0]  // 1.60,
                        (self.__screenSize[1] // 1.15 - 55)]

        self.__sawClicked       = False
        self.__sawBindingsAdded = False
        self.__validOnes = {
            "volume": range(0,16), "channel": [1,2,3,4,6,7,8,12,14,15], "frequency": range(0,32), "duration": range(1,8)

            }

        self.__window = SubMenu(self.__loader, "noiseMaker", self.__sizes[0], self.__sizes[1], None, self.__addElements,
                                1)
        self.dead   = True

    def __closeWindow(self):
        if self.changed == True:
            answer = self.__fileDialogs.askYesNoCancel("notSavedFile", "notSavedFileMessage")
            if answer == "Yes":
                self.__save()
            elif answer == "Cancel":
                self.__topLevelWindow.deiconify()
                self.__topLevelWindow.focus()
                return

        self.dead = True
        self.__topLevelWindow.destroy()
        self.__loader.topLevels.remove(self.__topLevelWindow)

    def __addElements(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()
        self.__topLevelWindow.protocol('WM_DELETE_WINDOW', self.__closeWindow)
        self.__savePoz = [self.__topLevelWindow.winfo_x(), self.__topLevelWindow.winfo_y()]

        self.__editorSizeY = self.__sizes[1] // 20 * 16
        self.__editorFrame = Frame(self.__topLevelWindow,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  width=self.__sizes[0], height=self.__editorSizeY
                  )
        self.__editorFrame.pack_propagate(False)
        self.__editorFrame.pack(side=TOP, anchor=N, fill=X)

        self.__sawFrame = Frame(self.__topLevelWindow,
                  bg=self.__loader.colorPalettes.getColor("highLight"),
                  width=self.__sizes[0], height=self.__sizes[1] - self.__editorSizeY
                  )
        self.__sawFrame.pack_propagate(False)
        self.__sawFrame.pack(side=TOP, anchor=N, fill=BOTH)

        t1 = Thread(target=self.createSawThings)
        t1.daemon = True
        t1.start()

        t2 = Thread(target=self.createEditorThings)
        t2.daemon = True
        t2.start()

        self.__loader.threadLooper.addToThreading(self, self.__loop, [], 1)

    def createEditorThings(self):
        while self.__editorFrame.winfo_width() < 2: sleep(0.00005)

        self.__buttonsFrame = Frame(self.__editorFrame,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  width=self.__sizes[0] // 5 *  3, height=self.__editorSizeY
                  )

        self.__buttonsFrame.pack_propagate(False)
        self.__buttonsFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__interfaceFrame = Frame(self.__editorFrame,
                                    bg=self.__loader.colorPalettes.getColor("window"),
                                    width=self.__sizes[0] // 5 * 2, height=self.__editorSizeY
                                    )

        self.__interfaceFrame.pack_propagate(False)
        self.__interfaceFrame.pack(side=LEFT, anchor=E, fill=BOTH)

        labelTexts = [
            self.__dictionaries.getWordFromCurrentLanguage("volume"),
            self.__dictionaries.getWordFromCurrentLanguage("channel"),
            self.__dictionaries.getWordFromCurrentLanguage("frequency"),
            self.__dictionaries.getWordFromCurrentLanguage("duration"),
            None
        ]

        while self.__buttonsFrame.winfo_width() < 2: sleep(0.00005)

        self.__dataLines = {}
        self.__keys = [
            "volume", "channel", "frequency", "duration"
        ]

        keys = self.__keys
        hList    = [16, 16, 32, 0]
        multi    = [2, 1.35, 4, 1]
        defaults = [6, 4, 0, 1]

        self.__framesAndLabels = []
        #testColors = ["red", "yellow"]

        backColor = [
            self.__loader.colorPalettes.getColor("boxBackNormal"),
            self.__loader.colorPalettes.getColor("boxBackNormal"),
            self.__loader.colorPalettes.getColor("boxBackNormal"),
            self.__loader.colorPalettes.getColor("window")

        ]

        for y in range(0, 4):
            self.__dataLines[keys[y]] = {
                "entries": [], "entryVals": [], "buttons": []
            }

            h = round(self.__editorSizeY / sum(multi) * multi[y])

            f = Frame(self.__buttonsFrame, bg=self.__colors.getColor("window"),
                      width=self.__sizes[0], height=h
                     )

            f.pack_propagate(False)
            f.pack(side=TOP, anchor=N, fill=X)

            self.__framesAndLabels.append(f)

            h2 = round(h / 5 / multi[y])

            fL = Frame(f, bg=backColor[y], width=self.__sizes[0], height = h2)
            fL.pack_propagate(False)
            fL.pack(side=TOP, anchor=N, fill=X)

            l = Label(fL,
                      fg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                      bg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                      font = self.__smallFont,
                      text = labelTexts[y],
                      width=1
                      )

            l.pack_propagate(False)
            l.pack(side=TOP, anchor=N, fill=BOTH)

            w = self.__wWw
            self.__framesAndLabels.append(fL)
            self.__framesAndLabels.append(l)

            for x in range(0, w):
                fX = Frame(f, bg=backColor[y],
                      width=self.__sizes[0] // 5 *  3 // w, height=h
                     )

                fX.pack_propagate(False)
                fX.pack(side=LEFT, anchor=E, fill=Y)

                fX1 = Frame(fX, bg=backColor[y],
                          width=self.__sizes[0] // 5 *  3, height=h2
                          )

                fX1.pack_propagate(False)
                fX1.pack(side=TOP, anchor=N, fill=X)

                self.__framesAndLabels.append(fX)
                self.__framesAndLabels.append(fX1)

                eVal = StringVar()
                eVal.set(str(defaults[y]))

                e = Entry(fX1, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                          width=99,
                                          fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                          textvariable=eVal, name=keys[y] + "_" + str(x),
                                          font=self.__miniFont, justify=CENTER,
                                          command=None)

                e.pack_propagate(False)
                e.pack(side=LEFT, anchor=W, fill=BOTH)

                self.__loader.threadLooper.bindingMaster.addBinding(self, e, "<KeyRelease>",
                                                                    self.__edited, 1)
                self.__loader.threadLooper.bindingMaster.addBinding(self, e, "<FocusOut>",
                                                                    self.__edited, 1)


                self.__dataLines[keys[y]]["entryVals"].append(eVal)
                self.__dataLines[keys[y]]["entries"].append(e)
                self.__dataLines[keys[y]]["buttons"].append([])

                for subY in range(0, hList[y]):


                    if keys[y] != "channel": self.__h3 = round((h - (h2 * 3)) / hList[y])

                    fSub = Frame(fX, bg=backColor[y],
                               width=self.__sizes[0] // w, height=self.__h3
                               )

                    fSub.pack_propagate(False)

                    if keys[y] == "channel" and subY in self.__channelSkip:
                       pass
                    else:
                        if keys[y] == "volume":
                           fSub.pack(side=BOTTOM, anchor=S, fill=X)
                        else:
                           fSub.pack(side=TOP, anchor=N, fill=X)

                    self.__framesAndLabels.append(fSub)

                    b = Button(fSub, name = keys[y] + "_" + str(x) + "_" + str(subY),
                               bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                               relief=GROOVE, activebackground=self.__colors.getColor("highLight"))
                    b.pack_propagate(False)

                    if keys[y] == "channel" and subY in self.__channelSkip:
                       pass
                    else:
                       b.pack(fill=BOTH)

                    self.__dataLines[keys[y]]["buttons"][-1].append(b)

                    self.__loader.threadLooper.bindingMaster.addBinding(self, b, "<Button-1>",
                                                                        self.__clicked, 1)
        self.fillButtons()

        t3 = Thread(target=self.createInterface)
        t3.daemon = True
        t3.start()

        self.__finished[1] = True

    def fillButtons(self):
        for key in self.__keys:
            for x in range(0, 32):
                if len(self.__dataLines[key]["buttons"][0]) > 0:
                   if key != "duration":
                      self.setButtonOnKeyAndX(key, x)

    def setButtonOnKeyAndX(self, key, x):
        if key == "duration": return

        if x >= self.__wWw:
            if key == "frequency":
               h = 32
            else:
               h = 16

            self.__dataLines["duration"]["entries"][x].config(state = DISABLED)
            self.__dataLines[key]       ["entries"][x].config(state = DISABLED)
            for y in range(0, h):
                self.__dataLines[key]["buttons"][x][y].config(bg = self.__colors.getColor("fontDisabled"), state = DISABLED)

        else:
            self.__dataLines["duration"]["entries"][x].config(state = NORMAL)
            self.__dataLines[key]       ["entries"][x].config(state = NORMAL)

            val = int(self.__dataLines[key]["entryVals"][x].get())

            if key == "frequency":
               h = 32
            else:
               h = 16

            for y in range(0, h):
                colors = {
                    True:  self.__colors.getColor("boxFontNormal"),
                    False: self.__colors.getColor("boxBackNormal")
                }

                try:
                    self.__dataLines[key]["buttons"][x][y].config(
                        bg = colors[y == val], state = NORMAL
                    )
                except:
                    print(key, x, y)

    def __edited(self, event):
        if False in self.__finished or self.__dont: return

        if type(event) == Entry:
            entry = event
        else:
            entry = event.widget

        name   = str(entry).split(".")[-1]

        key = name.split("_")[0]
        x   = int(name.split("_")[1])

        entryVal = self.__dataLines[key]["entryVals"][x]

        if len(entryVal.get()) > 2:
            entryVal.set(entryVal.get()[:2])

        try:
            num = int(entryVal.get())
        except:
            entry.config(bg = self.__colors.getColor("boxBackUnSaved"),
                         fg = self.__colors.getColor("boxFontUnSaved")
                         )
            return False

        if   num < min(self.__validOnes[key]): num   = min(self.__validOnes[key])
        elif num > max(self.__validOnes[key]): num   = max(self.__validOnes[key])
        elif num not in self.__validOnes[key]:
             diff = 99
             num2 = -1
             for n in self.__validOnes[key]:
                 d = abs(num - n)
                 if d < diff:
                    diff = d
                    num2 = n

             num = num2

        entry.config(bg = self.__colors.getColor("boxBackNormal"),
                     fg = self.__colors.getColor("boxFontNormal")
                         )
        entryVal.set(str(num))
        entry.icursor(len(str(num)))

        if key != "duration":
           self.setButtonOnKeyAndX(key, x)
        self.changed = True
        return True


    def __clicked(self, event):
        if False in self.__finished or self.__dont: return

        button = event.widget
        name   = str(button).split(".")[-1]
        #print(name)

        key = name.split("_")[0]
        x   = int(name.split("_")[1])
        y   = int(name.split("_")[2])

        self.__dataLines[key]["entryVals"][x].set(str(y))
        self.__dataLines[key]["entries"][x].config(bg = self.__colors.getColor("boxBackNormal"), fg = self.__colors.getColor("boxFontNormal"))

        if key != "duration":
           self.setButtonOnKeyAndX(key, x)

        self.__tia.setAndPlay(int(self.__dataLines["volume"]["entryVals"][x].get()),
                              int(self.__dataLines["channel"]["entryVals"][x].get()),
                              int(self.__dataLines["frequency"]["entryVals"][x].get()),
                              "NTSC",
                              int(self.__dataLines["duration"]["entryVals"][x].get()))
        self.changed = True


    def createInterface(self):
        while self.__interfaceFrame.winfo_width() < 2: sleep(0.00005)

        self.__affectedValuesLabel = Label(self.__interfaceFrame,
                                           fg=self.__loader.colorPalettes.getColor("font"),
                                           bg=self.__loader.colorPalettes.getColor("window"),
                                           font=self.__normalFont,
                                           text=self.__dictionaries.getWordFromCurrentLanguage("affectedValues")+":",
                                           width=1
                                           )

        self.__affectedValuesLabel.pack_propagate(False)
        self.__affectedValuesLabel.pack(side=TOP, anchor=N, fill=BOTH)

        fSiez = self.__sizes[1] // 25

        self.__fortariThings = Frame(self.__interfaceFrame,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  width=self.__sizes[0], height=fSiez
                  )
        self.__fortariThings.pack_propagate(False)
        self.__fortariThings.pack(side=TOP, anchor=N, fill=X)

        self.__affecteds = FortariMB(self.__loader, self.__fortariThings, NORMAL,
                                            self.__smallFont, self.__dictionaries.getWordFromCurrentLanguage("tiaRegisters"),
                                            self.__keys[:-1], True, False,
                                            self.selectedChanged, self.__keys[:-1])

        #for item in self.__keys[:-1]: self.__affecteds.select(item, True)

        self.__actionLabel = Label(self.__interfaceFrame,
                                   fg=self.__loader.colorPalettes.getColor("font"),
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   font=self.__normalFont,
                                   text=self.__dictionaries.getWordFromCurrentLanguage("action")+":",
                                   width=1
                                   )

        self.__actionLabel.pack_propagate(False)
        self.__actionLabel.pack(side=TOP, anchor=N, fill=BOTH)

        self.__iFaceFrames  = []
        self.__iFaceButtons = {}

        self.__lenghtF = Frame(self.__interfaceFrame,
                               bg=self.__loader.colorPalettes.getColor("window"),
                               width=self.__interfaceFrame.winfo_width(),
                               height=self.__interfaceFrame.winfo_height() // 20
                               )

        self.__lenghtF.pack_propagate(False)
        self.__lenghtF.pack(side=TOP, anchor=N, fill=BOTH)

        self.__lenght = VisualEditorFrameWithLabelAndEntry(
            self.__loader, str(self.__wWw), self.__lenghtF, self.__interfaceFrame.winfo_width(), "toneLen", self.__smallFont,
            self.changeLenght, self.changeLenght)

        commandList = {
            "copyFirstToAll": self.copyFirstToAll,
            "genSawUp"      : self.genSawUp,
            "genSawDown"    : self.genSawDown,
            "genTriUp"      : self.genTriUp,
            "genTriDown"    : self.genTriDown,
            "genSinewave"   : self.genSine,
            "randomNoise"   : self.randomNoise

        }

        for word in commandList.keys():
            f = Frame(self.__interfaceFrame,
                      bg=self.__loader.colorPalettes.getColor("window"),
                      width=self.__sizes[0], height=fSiez
                      )
            f.pack_propagate(False)
            f.pack(side=TOP, anchor=N, fill=X)

            b = Button(f, name = word,
                       bg=self.__loader.colorPalettes.getColor("window"),
                       fg=self.__loader.colorPalettes.getColor("font"),
                       text = self.__dictionaries.getWordFromCurrentLanguage(word),
                       activebackground=self.__colors.getColor("highLight"),
                       command = commandList[word], font = self.__smallFont)
            b.pack_propagate(False)
            b.pack(fill=BOTH)

            self.__iFaceButtons[word] = b
            self.__iFaceFrames.append(f)

        self.__backImage = self.__loader.io.getImg("backwards", None)
        self.__forImage = self.__loader.io.getImg("forwards", None)

        self.__arrowsFrame = Frame(self.__interfaceFrame,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  width=self.__sizes[0], height=fSiez
                  )
        self.__arrowsFrame.pack_propagate(False)
        self.__arrowsFrame.pack(side=TOP, anchor=N, fill=X)

        self.__arrowsFrame1 = Frame(self.__arrowsFrame,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  width=self.__interfaceFrame.winfo_width()//2, height=fSiez
                  )
        self.__arrowsFrame1.pack_propagate(False)
        self.__arrowsFrame1.pack(side=LEFT, anchor=E, fill=Y)

        self.__arrowsFrame2 = Frame(self.__arrowsFrame,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  width=self.__interfaceFrame.winfo_width()//2, height=fSiez
                  )
        self.__arrowsFrame2.pack_propagate(False)
        self.__arrowsFrame2.pack(side=LEFT, anchor=E, fill=Y)

        self.__backButton = Button(self.__arrowsFrame1, bg=self.__loader.colorPalettes.getColor("window"),
                                   image=self.__backImage,
                                   width=self.__sizes[0], state=DISABLED, command=self.__decIndex)


        self.__forButton = Button(self.__arrowsFrame2, bg=self.__loader.colorPalettes.getColor("window"),
                                   image=self.__forImage,
                                   width=self.__sizes[0], state=DISABLED, command=self.__incIndex)

        self.__forButton.pack_propagate(False)
        self.__forButton.pack(side=LEFT, anchor=W, fill=Y)
        self.__backButton.pack_propagate(False)
        self.__backButton.pack(side=LEFT, anchor=W, fill=Y)

        self.__loaderFrame = Frame(self.__interfaceFrame,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  width=self.__sizes[0], height=fSiez * 2
                  )
        self.__loaderFrame.pack_propagate(False)
        self.__loaderFrame.pack(side=TOP, anchor=N, fill=X)

        self.__testerFrame = Frame(self.__interfaceFrame,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  width=self.__sizes[0], height=fSiez
                  )
        self.__testerFrame.pack_propagate(False)
        self.__testerFrame.pack(side=TOP, anchor=N, fill=X)

        while self.__loaderFrame.winfo_width() < 2: sleep(0.000005)

        self.__spriteLoader = VisualLoaderFrame(self.__loader, self.__loaderFrame, self.__loaderFrame.winfo_height() // 2, self.__smallFont, self.__miniFont,
                                                None, "PixelFarts", "openSoundFx", self.checkIfValidFileName,
                                                self.__interfaceFrame.winfo_width() // 2, self.__open, self.__save)

        while (self.__testerFrame.winfo_width() < 2): sleep(0.00001)

        from EmuTestFrame import EmuTestFrame

        self.__testWithEmulatorFrame = EmuTestFrame(self.__loader, self.__testerFrame,
                                                    self.__testerFrame.winfo_height()     , self.__normalFont,
                                                    self.__testerFrame.winfo_width()  // 2, self.__loadTest, BOTTOM, S)


        self.__finished[2] = True

    def __decIndex(self):
        self.__changeIndex(-1)

    def __incIndex(self):
        self.__changeIndex(1)

    def __changeIndex(self, num):
        copied = {}
        for key in self.__dataLines.keys():
            copied[key] = []

            for x in range(num, self.__wWw + num):
                if x >=   self.__wWw:
                   x  = x%self.__wWw

                copied[key].append(self.__dataLines[key]["entryVals"][x].get())

            for x in range(0, self.__wWw):
                self.__dataLines[key]["entryVals"][x].set(copied[key][x])
                self.__edited(self.__dataLines[key]["entries"][x])
                if key != "duration":
                   self.setButtonOnKeyAndX(key, x)

    def __loadTest(self):
        t = Thread(target=self.__testThread)
        t.daemon = True
        t.start()

    def __testThread(self):
        Compiler(self.__loader, self.__loader.virtualMemory.kernel, "soundFxTest",
                 [self.__dataLines, self.__wWw, "NTSC", "#NAME#", "bank2"])

    def checkIfValidFileName(self, event):
        name = str(event.widget).split(".")[-1]

        widget = self.__spriteLoader.getEntry()
        value = self.__spriteLoader.getValue()


        if self.__loader.io.checkIfValidFileName(value) and (" " not in value):
            widget.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                      fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                      )

        else:
            widget.config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                                      fg=self.__loader.colorPalettes.getColor("boxFontUnSaved"),
                                      )


    def changeLenght(self, event):
        if False in self.__finished or self.__dont: return

        entry    = event.widget
        val      = self.__lenght.getValue()

        if len(val) > 2:
           self.__lenght.setValue(val[:-2])

        try:
            num = int(val)
        except:
            entry.config(bg=self.__colors.getColor("boxBackUnSaved"),
                         fg=self.__colors.getColor("boxFontUnSaved")
                         )
            return

        entry.config(bg=self.__colors.getColor("boxBackNormal"),
                     fg=self.__colors.getColor("boxFontNormal")
                     )

        if num > 32: num = 32
        if num < 1 : num = 1

        self.__wWw = num
        self.__lenght.setValue(str(num))
        entry.icursor(len(str(num)))
        self.changed = True

        self.fillButtons()

    def randomNoise(self):
        from random import randint

        if False in self.__finished or self.__dont: return

        for key in self.__affecteds.getSelected():
            minI = min(self.__validOnes[key])
            maxI = max(self.__validOnes[key])
            array = []

            for num in range(0, self.__wWw):
                item = randint(minI, maxI)

                if item not in self.__validOnes[key]:
                    closest = ""
                    diff = 99

                    for one in self.__validOnes[key]:
                        d = abs(item - one)
                        if d < diff:
                            diff = d
                            closest = one
                    item = closest

                array.append(item)
            self.generatePattern(1, array, key)

    def genSine(self):
        if False in self.__finished or self.__dont: return

        for key in self.__affecteds.getSelected():
            table = self.generateSinTable(len(self.__validOnes[key]))

            if key == "volume": table = table[::-1]

            ord   = list(self.__validOnes[key])
            if key == "volume":
               ord.sort(reverse=True)
            else:
               ord.sort()

            middleOne = max(ord) // 2

            newTable = []
            for itemNum in range(0, len(table)):
                item = table[itemNum]

                item = round(item * middleOne)

                if item > max(ord): item = max(ord)
                if item < min(ord): item = min(ord)

                if item not in self.__validOnes[key]:
                   closest = ""
                   diff    = 99

                   for one in self.__validOnes[key]:
                       d = abs(item - one)
                       if d < diff:
                          diff = d
                          closest = one
                   item = closest

                newTable.append(item)

            step = len(newTable) / self.__wWw
            self.generatePattern(step, newTable, key)

    def generateSinTable(self, l):
        from math import sin, radians

        vals = []

        for num in range(0, 360):
            vals.append(sin(radians(num)) + 1)

        step = 360 / l

        index = 0

        newVals = []
        while index < 360:
              newVals.append(vals[int(index)])
              index += step

        secondIndex = 1
        indexVals = [l // 4, l // 4 * 3]

        while len(newVals) < l:
              secondIndex = 1 - secondIndex
              newVals.insert(indexVals[secondIndex], newVals[indexVals[secondIndex]])

        return newVals

    def genTriUp(self):
        if False in self.__finished or self.__dont: return

        for key in self.__affecteds.getSelected():
            step = len(self.__validOnes[key]) * 2 / self.__wWw

            array1 = list(deepcopy(self.__validOnes[key]))
            array2 = list(deepcopy(self.__validOnes[key][::-1]))

            #if key != "volume": array = array[::-1]
            if key != "volume":
               array2.extend(array1)
               array = array2
            else:
               array1.extend(array2)
               array = array1

            self.generatePattern(step, array, key)


    def genTriDown(self):
        if False in self.__finished or self.__dont: return

        for key in self.__affecteds.getSelected():
            step = len(self.__validOnes[key]) * 2 / self.__wWw

            array1 = list(deepcopy(self.__validOnes[key][::-1]))
            array2 = list(deepcopy(self.__validOnes[key]))

            if key != "volume":
               array2.extend(array1)
               array = array2
            else:
               array1.extend(array2)
               array = array1

            self.generatePattern(step, array, key)

    def genSawUp(self):
        if False in self.__finished or self.__dont: return

        for key in self.__affecteds.getSelected():
            step = len(self.__validOnes[key]) / self.__wWw

            array = deepcopy(self.__validOnes[key])
            if key != "volume": array = array[::-1]

            self.generatePattern(step, array, key)


    def genSawDown(self):
        if False in self.__finished or self.__dont: return

        for key in self.__affecteds.getSelected():
            step = len(self.__validOnes[key]) / self.__wWw

            array = deepcopy(self.__validOnes[key])
            if key == "volume": array = array[::-1]

            self.generatePattern(step, array, key)

    def generatePattern(self, step, array, key):
        index = -1
        for x in range(0, self.__wWw):
            index += step
            noDec = int(index)

            if noDec >= len(array):
                index = 0
                noDec = 0

            self.__dataLines[key]["entryVals"][x].set(str(array[noDec]))
            self.setButtonOnKeyAndX(key, x)

        self.changed = True

    def copyFirstToAll(self):
        if False in self.__finished or self.__dont: return

        for key in self.__affecteds.getSelected():
            val = self.__dataLines[key]["entryVals"][0].get()
            for x in range(1, self.__wWw):
                self.__dataLines[key]["entryVals"][x].set(val)
                self.setButtonOnKeyAndX(key, x)

    def selectedChanged(self):
        pass

    def createSawThings(self):
        while self.__sawFrame.winfo_width() < 2: sleep(0.00005)

        self.__sawCanvas = Canvas(self.__sawFrame, bg=self.__loader.colorPalettes.getColor("window"), bd=0,
                               width=self.__sizes[0], height = self.__sizes[1]
                               )

        self.__sawCanvas.pack_propagate(False)
        self.__sawCanvas.pack(side=TOP, anchor=N, fill=BOTH)

        import os
        self.__sawFrames   = []

        constant         = self.__sawFrame.winfo_height() / 89
        self.__sawSize   = [round(154 * constant), round(self.__sawFrame.winfo_height())]
        self.__sawRising = self.__sawFrame.winfo_height()
        self.__sawRisingSteps =  self.__sawFrame.winfo_height() // 20

        for root, folders, files in os.walk("others/img/doom"):
            for file in files:
                self.__sawFrames.append(ImageTk.PhotoImage(IMAGE.open(root + "/" + file).resize((
                     self.__sawSize[0], self.__sawSize[1]), IMAGE.ANTIALIAS)))

        self.__finished[0] = True

    def __save(self):
        if False not in self.__finished:
           pass

        if self.changed == True:
            fileName = self.__loader.mainWindow.projectPath + "soundFx/" + self.__spriteLoader.getValue() + ".a26"
            if os.path.exists(fileName):
                answer = self.__fileDialogs.askYesOrNo("fileExists", "overWrite")
                if answer == "No":
                    return

            self.__dont = True

            firstLine = self.__loader.virtualMemory.kernel + " " + str(self.__wWw) + "\n"
            for key in self.__keys:
                datas = []
                for num in range(0, self.__wWw):
                    datas.append(self.__dataLines[key]["entryVals"][num].get())
                firstLine += " ".join(datas) + "\n"

            file = open(fileName, "w")
            file.write(firstLine)
            file.close()
            self.__soundPlayer.playSound("Success")

            fileName = self.__loader.mainWindow.projectPath + "soundFx/" + self.__spriteLoader.getValue() + ".asm"

            data = Compiler(self.__loader, self.__loader.virtualMemory.kernel, "soundFxData",
                            [self.__dataLines, self.__wWw, "NTSC", "#NAME#", "bank2"]).converted

            file = open(fileName, "w")
            file.write(data)
            file.close()

            self.__topLevelWindow.deiconify()
            self.__topLevelWindow.focus()

            self.__dont = False


    def __open(self):
        if False not in self.__finished:

            if self.changed == True:
                answer = self.__fileDialogs.askYesNoCancel("notSavedFile", "notSavedFileMessage")
                if answer == "Yes":
                    self.__save()
                elif answer == "Cancel":
                    self.__topLevelWindow.deiconify()
                    self.__topLevelWindow.focus()
                    return

            fpath = self.__fileDialogs.askForFileName("openFile", False, ["a26", "*"],
                                                      self.__loader.mainWindow.projectPath + "soundFx/")

            if fpath == "":
               return

            self.__dont = True

            try:
                file = open(fpath, "r")
                data = file.read().replace("\r", "").split("\n")
                file.close()

                compatibles = {
                    "common": ["common"]
                }

                self.__spriteLoader.setValue(".".join(fpath.split("/")[-1].split(".")[:-1]))
                if data[0].split(" ")[0] not in compatibles[self.__loader.virtualMemory.kernel]:
                    if self.__fileDialogs.askYesNoCancel("differentKernel", "differentKernelMessage") == "No":
                        self.__topLevelWindow.deiconify()
                        self.__topLevelWindow.focus()
                        self.__dont = False
                        return

                self.__wWw = int(data[0].split(" ")[1])
                self.__lenght.setValue(str(self.__wWw))

                index = 0
                for key in self.__keys:
                    index += 1
                    datas = data[index].split(" ")

                    for x in range(0, 32):
                        if x < self.__wWw:
                           self.__dataLines[key]["entryVals"][x].set(datas[x])
                        if key != "duration": self.setButtonOnKeyAndX(key, x)

            except Exception as e:
                self.__fileDialogs.displayError("unableToOpenFile", "unableToOpenFileMessage", None, str(e))

            self.__soundPlayer.playSound("Success")
            self.__dont = False

            self.__topLevelWindow.deiconify()
            self.__topLevelWindow.focus()

    def __loop(self):
        try:
            if False in self.__finished:
               return

            if self.__firstSound:
               self.__firstSound = False
               self.__soundPlayer.playOnlyOneAtTime("sawStart")
               self.__playingAnySawSound = 20

               self.__loader.threadLooper.addToThreading(self, self.__drawSawCanvas, [], 1)

            if self.changed == False:
               self.__spriteLoader.disableSave()
            else:
               self.__spriteLoader.enableSave()

            if self.__wWw == 1:
               self.__forButton.config(state = DISABLED)
               self.__backButton.config(state = DISABLED)
            else:
               self.__forButton.config(state=NORMAL)
               self.__backButton.config(state=NORMAL)

        except Exception as e:
             print(str(e))
             pass

    def __sawEnter(self, event):
        if len(self.__sawFrames) > 1:
           self.__onSaw = True

    def __sawLeave(self, event):
        self.__onSaw = False

    def __clickedSaw(self, event):
        if len(self.__sawFrames) == 4:
           self.__sawClicked = True
           self.__savePoz = [self.__topLevelWindow.winfo_x(), self.__topLevelWindow.winfo_y()]

    def __releaseSaw(self, event):
        self.__sawClicked = False
        self.setXY(self.__savePoz[0], self.__savePoz[1])

    def setXY(self, x, y):
        self.__topLevelWindow.geometry(
            str(round(self.__sizes[0])) + "x" + str(round(self.__sizes[1])) + "+" + str(x) + "+" + str(y)
        )

    def __drawSawCanvas(self):
        from random import randint

        if self.__playingAnySawSound > 0   : self.__playingAnySawSound    -= 1
        if self.__playingSawAttackSound > 0: self.__playingSawAttackSound -= 1

        if self.__playingAnySawSound == 0 and self.__playingSawAttackSound == 0 and self.__onSaw:
           self.__soundPlayer.playOnlyOneAtTime("sawIdle")
           self.__playingAnySawSound = 7

        if self.__playingSawAttackSound == 0 and self.__sawClicked:
           self.__soundPlayer.playOnlyOneAtTime("sawAttack")
           self.__playingSawAttackSound = 3

        if self.__sawClicked:
           self.setXY(self.__savePoz[0] + randint(-9, 9), self.__savePoz[1])

        if self.__sawBindingsAdded == False:
           self.__sawBindingsAdded = True
           self.__loader.threadLooper.bindingMaster.addBinding(self, self.__sawCanvas, "<Enter>", self.__sawEnter, 1)
           self.__loader.threadLooper.bindingMaster.addBinding(self, self.__sawCanvas, "<Leave>", self.__sawLeave, 1)

           self.__loader.threadLooper.bindingMaster.addBinding(self, self.__sawCanvas, "<Button-1>"       , self.__clickedSaw, 1)
           self.__loader.threadLooper.bindingMaster.addBinding(self, self.__sawCanvas, "<ButtonRelease-1>", self.__releaseSaw, 1)


        index = self.__sawIndex // 5
        if self.__sawClicked:
           index += 2

        if self.__sawIndex > 8:
            self.__sawIndex = 0
        else:
            self.__sawIndex += 1

        if index != self.__lastIndex or self.__sawRising > 0:
           self.__lastIndex = index
        else:
           return

        #self.__sawCanvas.clipboard_clear()
        #self.__sawCanvas.delete("all")
        self.__saveIndex = 1 - self.__saveIndex

        self.__saws[self.__saveIndex] = self.__sawCanvas.create_image(
                                 self.__sawFrame.winfo_width() // 2 - self.__sawSize[0] // 2, self.__sawRising
                                 , image=self.__sawFrames[index], anchor=NW
                                 )

        if self.__saws[1 - self.__saveIndex] != None:
            try:
                self.__sawCanvas.delete(self.__saws[1 - self.__saveIndex])
                self.__saws[1 - self.__saveIndex] = None
            except:
                pass

        if self.__sawRising > 0:
           self.__sawRising -= self.__sawRisingSteps

        if self.__sawRising < 0:
           self.__sawRising = 0

