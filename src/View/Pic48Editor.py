from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from Compiler import Compiler
from HexEntry import HexEntry
from time import sleep

class Pic48Editor:

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
        self.__theyAreDisabled = True

        self.__ctrl = False
        self.__middle = False
        self.__draw = 0

        self.__Y            = 0
        self.__frames       = []
        self.__finished     = [False, False]
        self.__enabledThem  = False
        self.__disabledOnes = []

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize*0.65), False, False, False)
        self.__bigFont = self.__fontManager.getFont(int(self.__fontSize*1.15), False, False, False)
        self.__bigFont2 = self.__fontManager.getFont(int(self.__fontSize*1.5), False, False, False)

        self.__dataLines = []
        self.__xSize  = [48, 48, 12]
        self.__ySize  = 48
        self.__keys   = ["layerUnique", "layerRepeating" , "layerPlayfield", "background"]

        self.__numOfLines = self.__ySize // len(self.__xSize)

        self.__sizes = [self.__screenSize[0] // 1.65 // self.__xSize[0] * self.__xSize[0],
                        (self.__screenSize[1] //1.20 - 55) // self.__ySize * self.__ySize]
        self.__window = SubMenu(self.__loader, "48pxPicture", self.__sizes[0], self.__sizes[1], None, self.__addElements,
                                1)
        self.dead = True

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

        self.__editorFrame = Frame(self.__topLevelWindow,
                  bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                  width=self.__sizes[0] // 20 * 12, height=self.__sizes[1]
                  )
        self.__editorFrame.pack_propagate(False)
        self.__editorFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__colorFrame = Frame(self.__topLevelWindow,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  width=self.__sizes[0] // 20 * 3, height=self.__sizes[1]
                  )
        self.__colorFrame.pack_propagate(False)
        self.__colorFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__setterFrame = Frame(self.__topLevelWindow,
                  bg=self.__loader.colorPalettes.getColor("window"),
                  width=self.__sizes[0], height=self.__sizes[1]
                  )
        self.__setterFrame.pack_propagate(False)
        self.__setterFrame.pack(side=LEFT, anchor=E, fill=BOTH)

        t1 = Thread(target=self.generateEditor)
        t1.daemon = True
        t1.start()

        t2 = Thread(target=self.generateColorFields)
        t2.daemon = True
        t2.start()

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "<KeyPress-Control_L>",
                                                           self.shiftON, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "<KeyRelease-Control_L>",
                                                           self.shiftOff, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "<KeyPress-Control_R>",
                                                           self.shiftON, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "<KeyRelease-Control_R>",
                                                           self.shiftOff, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "<Button-2>", self.drawMode, 1)

        self.__loader.threadLooper.addToThreading(self, self.__loop, [], 1)

    def __loop(self):
        try:
            if False in self.__finished:
               return

            if self.__enabledThem == False:
               self.__enabledThem = True

               for item in self.__disabledOnes:
                   if type(item) == HexEntry:
                      item.changeState(NORMAL)
                   else:
                      item.config(state = NORMAL)

               self.__disabledOnes = []

        except Exception as e:
             #print(str(e))
             pass

    def generateColorFields(self):
        while (self.__colorFrame.winfo_width() < 2): sleep(0.000005)

        sizeY = self.__colorFrame.winfo_height() // self.__ySize * len(self.__xSize)
        sizeX = self.__colorFrame.winfo_width()

        self.__colorDataLines = []

        for y in range(0, self.__ySize // (len(self.__xSize))):
            fBig      = Frame(self.__colorFrame,
                              bg    = self.__loader.colorPalettes.getColor("boxBackNormal"),
                              width = sizeX, height= sizeY
                              )
            fBig.pack_propagate(False)
            fBig.pack(side=TOP, anchor=N, fill=X)

            self.__frames.append(fBig)

            self.__colorDataLines.append(
                {
                    "colors":  {self.__keys[0]: ["$1E"], self.__keys[1]: ["$44"], self.__keys[2]: ["$0E"], self.__keys[3]: ["$00"]},
                    "entries": {self.__keys[0]:  None  , self.__keys[1]:  None  , self.__keys[2]:  None  , self.__keys[3]:  None  }
                }
            )

            fBig1      = Frame(fBig,
                              bg    = self.__loader.colorPalettes.getColor("window"),
                              width = sizeX // 2, height= sizeY
                              )
            fBig1.pack_propagate(False)
            fBig1.pack(side=LEFT, anchor=E, fill=Y)
            self.__frames.append(fBig1)

            fBig2      = Frame(fBig,
                              bg    = self.__loader.colorPalettes.getColor("window"),
                              width = sizeX // 2, height= sizeY
                              )
            fBig2.pack_propagate(False)
            fBig2.pack(side=LEFT, anchor=E, fill=BOTH)
            self.__frames.append(fBig2)

            self.__colorDataLines[-1]["entries"][self.__keys[3]] = HexEntry(self.__loader, fBig2, self.__colors,
                                                                   self.__colorDict, self.__bigFont,
                                                                   self.__colorDataLines[-1]["colors"][self.__keys[3]],
                                                                   0, None, self.reDrawCanvas)
            self.__colorDataLines[-1]["entries"][self.__keys[3]].changeState(DISABLED)
            self.__disabledOnes.append(self.__colorDataLines[-1]["entries"][self.__keys[3]])

            for subNum in range(0, len(self.__xSize)):
                fSub = Frame(fBig1,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              width=sizeX // 2, height=sizeY // len(self.__xSize)
                              )
                fSub.pack_propagate(False)
                fSub.pack(side=TOP, anchor=N, fill=X)
                self.__frames.append(fSub)

                self.__colorDataLines[-1]["entries"][self.__keys[subNum]] = HexEntry(self.__loader, fSub, self.__colors,
                                                                                self.__colorDict, self.__smallFont,
                                                                                self.__colorDataLines[-1]["colors"][
                                                                                    self.__keys[subNum]],
                                                                                0, None, self.reDrawCanvas)
                self.__colorDataLines[-1]["entries"][self.__keys[subNum]].changeState(DISABLED)
                self.__disabledOnes.append(self.__colorDataLines[-1]["entries"][self.__keys[subNum]])


        self.__finished[1] = True

    def reDrawCanvas(self):
        pass

    def generateEditor(self):
        #sizeY  = self.__sizes[1] // self.__ySize
        #sizeX  = self.__sizes[0] // 3 * 2

        while (self.__editorFrame.winfo_width() < 2): sleep(0.000005)

        sizeY = self.__editorFrame.winfo_height() // self.__ySize * len(self.__xSize)
        sizeX = self.__editorFrame.winfo_width()

        for y in range(0, self.__ySize // (len(self.__xSize))):
            fBig      = Frame(self.__editorFrame,
                              bg    = self.__loader.colorPalettes.getColor("boxBackNormal"),
                              width = sizeX, height= sizeY
                              )
            fBig.pack_propagate(False)
            fBig.pack(side=TOP, anchor=N, fill=X)

            self.__frames.append(fBig)

            self.__dataLines.append({
                self.__keys[0]: {
                    "buttons": [],
                    "values": []
                },
                self.__keys[1]: {
                    "buttons": [],
                    "values": []
                },
                self.__keys[2]: {
                    "buttons": [],
                    "values": []
                }
            })
            self.__soundPlayer.playSound("Pong")

            for xBig in range(0, self.__xSize[2]):
                fBigHor = Frame(fBig,
                             bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                             width=sizeX // self.__xSize[2], height=sizeY
                             )
                fBigHor.pack_propagate(False)
                fBigHor.pack(side=LEFT, anchor=E, fill=Y)

                self.__frames.append(fBigHor)

                for sub in range(0, len(self.__xSize)):
                    fSub = Frame(fBigHor,
                                 bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                 width=sizeX // self.__xSize[2], height=sizeY // len(self.__xSize)
                                 )
                    fSub.pack_propagate(False)
                    fSub.pack(side=TOP, anchor=N, fill=Y)

                    self.__frames.append(fSub)

                    nextLen = self.__xSize[sub] // self.__xSize[2]

                    for subSub in range(0, nextLen):
                        xNum = str(xBig * nextLen + subSub)
                        #print(xNum, str(y))

                        fSubSub = Frame(fSub,
                                     bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                     width=sizeX // self.__xSize[2] // nextLen, height=sizeY // len(self.__xSize)
                                     )
                        fSubSub.pack_propagate(False)
                        fSubSub.pack(side=LEFT, anchor=E, fill=Y)

                        self.__frames.append(fSubSub)

                        b = Button(fSubSub, name=(self.__keys[sub] + "_" + xNum + "," + str(y)),
                                   bg=self.__loader.colorPalettes.getColor("boxBackNormal"), state = DISABLED,
                                   relief=GROOVE, activebackground=self.__colors.getColor("highLight"))
                        b.pack_propagate(False)
                        b.pack(fill=BOTH)

                        self.__dataLines[-1][self.__keys[sub]]["buttons"].append(b)
                        self.__dataLines[-1][self.__keys[sub]]["values"] .append(0)
                        self.__disabledOnes.append(b)

                        self.__loader.threadLooper.bindingMaster.addBinding(self, b, "<Button-1>", self.__clicked, 1)
                        self.__loader.threadLooper.bindingMaster.addBinding(self, b, "<Button-3>", self.__clicked, 1)
                        self.__loader.threadLooper.bindingMaster.addBinding(self, b, "<Enter>", self.__enter, 1)

        self.__finished[0] = True

    def __clicked(self, event):
        button = event.widget
        if button.cget("state") == DISABLED or\
           False in self.__finished: return

        name   = str(button).split(".")[-1]
        try:
            mouseButton = int(str(event).split(" ")[3].split("=")[1])
        except:
            if self.__ctrl:
                mouseButton = 3
            else:
                mouseButton = 1

        if self.__ctrl == False and mouseButton == 3:
           return

        levelKey = name.split("_")[0]
        theX     = int(name.split("_")[1].split(",")[0])
        theY     = int(name.split("_")[1].split(",")[1])

        if self.__draw == True:
           if self.__ctrl == False:
              self.__dataLines[theY][levelKey]["values"][theX] = 1
           else:
              self.__dataLines[theY][levelKey]["values"][theX] = 0
        else:
            if self.__ctrl:
               if mouseButton == 1:
                  self.__dataLines[theY][levelKey]["values"][theX] = 1
               else:
                  self.__dataLines[theY][levelKey]["values"][theX] = 0
            else:
                self.__dataLines[theY][levelKey]["values"][theX] = 1 - self.__dataLines[theY][levelKey]["values"][theX]

        self.colorTile(button, self.__dataLines[theY][levelKey]["values"][theX])
        self.reDrawCanvas()
        self.changed = True

    def colorTile(self, button, value):
        colors = ["boxBackNormal", "boxFontNormal"]

        button.config(bg = self.__colors.getColor(colors[value]))

    def __enter(self, event):
        if self.__draw: self.__clicked(event)

    def drawMode(self, event):
        self.__draw = 1 - self.__draw

    def shiftON(self, event):
        self.__ctrl = True

    def shiftOff(self, event):
        self.__ctrl = False

    def __save(self):
        pass

