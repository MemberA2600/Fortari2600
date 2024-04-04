from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from Compiler import Compiler
from HexEntry import HexEntry
from time import sleep
from VisualEditorFrameWithLabelAndEntry import VisualEditorFrameWithLabelAndEntry
from FortariMB import FortariMB

class Pic48Editor:

    def __init__(self, loader):
        self.__loader = loader
        self.__mainWindow = self.__loader.mainWindow

        self.dead = False
        self.changed = False
        self.__loader.stopThreads.append(self)
        self.__isPlaying = False

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

        self.__ctrl           = False
        self.__middle         = False
        self.__draw           = 0
        self.__repeatingOnTop = False

        self.__Y            = 0
        self.__frameNum     = 1
        self.__frameIndex   = 0
        self.__frames       = []
        self.__finished     = [False, False, False]
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
        self.ignore   = False

        self.__data      = [[]]
        self.__colorData = [[]]

        self.__numOfLines = self.__ySize // len(self.__xSize)

        self.__temp = {self.__keys[0]: [], self.__keys[1]: [], self.__keys[2]: []}
        for num in range(0, max(self.__xSize)):
           for index in range(0, 3):
               if len(self.__temp[self.__keys[index]]) < self.__xSize[index]: self.__temp[self.__keys[index]].append(0)

        for num in range(0, self.__numOfLines):
            self.__data[0].append(deepcopy(self.__temp))

        #print(self.__data[0])

        self.__patterns = ["100", "010", "001", "110", "011", "101", "111"]
        self.__pattern = "010"

        self.__sizes = [self.__screenSize[0] // 1.65 // self.__xSize[0] * self.__xSize[0],
                        (self.__screenSize[1] //1.20 - 55) // self.__ySize * self.__ySize]
        self.__window = SubMenu(self.__loader, "48pxPicture", self.__sizes[0], self.__sizes[1], None, self.__addElements,
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

        self.__editorFrame = Frame(self.__topLevelWindow,
                  bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                  width=self.__sizes[0] // 20 * 11, height=self.__sizes[1]
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
                  width=self.__sizes[0] * 6, height=self.__sizes[1]
                  )
        self.__setterFrame.pack_propagate(False)
        self.__setterFrame.pack(side=LEFT, anchor=E, fill=BOTH)

        t1 = Thread(target=self.generateEditor)
        t1.daemon = True
        t1.start()

        t2 = Thread(target=self.generateColorFields)
        t2.daemon = True
        t2.start()

        self.__canvas = Canvas(self.__setterFrame, bg="black", bd=0,
                               width=self.__sizes[0] * 5, height = self.__sizes[1] // 3
                               )

        self.__canvas.pack_propagate(False)
        self.__canvas.pack(side=TOP, anchor=N, fill=X)

        t3 = Thread(target=self.generateMenu)
        t3.daemon = True
        t3.start()

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
                   if type(item) in (HexEntry, FortariMB):
                      item.changeState(NORMAL)
                   else:
                      item.config(state = NORMAL)

               self.__disabledOnes = []
            else:
               if   self.__frameIndex >= self.__frameNum:
                    self.__changeIndex(self.__frameNum - 1)

               if     self.__isPlaying == False:
                 self.__playButton.config(image=self.__playImage)

                 if   self.__frameNum == 1 and self.__indexEntry.cget("state") == NORMAL:
                      self.__indexEntry.config(state = DISABLED)
                      self.__playButton.config(state = DISABLED)
                      self.__backButton.config(state = DISABLED)
                      self.__forButton.config(state = DISABLED)
                 elif self.__frameNum > 1 and self.__indexEntry.cget("state") == DISABLED:
                      self.__indexEntry.config(state=NORMAL)
                      self.__playButton.config(state=NORMAL)
                      self.__backButton.config(state=NORMAL)
                      self.__forButton.config(state=NORMAL)
               else:
                  self.__playButton.config(image=self.__stopImage)
                  if self.__frameNum == 1:
                      self.__isPlaying = False

                  elif self.__frameNum > 1:
                       self.__indexEntry.config(state=DISABLED)
                       self.__backButton.config(state=DISABLED)
                       self.__forButton.config(state=DISABLED)

               if self.__repeatingOnTop != self.__boxButtonVal.get():
                  self.__repeatingOnTop = self.__boxButtonVal.get()
                  self.reDrawCanvas(None)

               if self.__Y > 0 and self.__numOfLines > self.__ySize // len(self.__xSize):
                  self.__backYIndexButton.config(state = NORMAL)
               else:
                  self.__backYIndexButton.config(state=DISABLED)

               if self.__Y < self.__numOfLines - (self.__ySize // len(self.__xSize)) and self.__numOfLines > self.__ySize // len(self.__xSize):
                  self.__forYIndexButton.config(state = NORMAL)
               else:
                  self.__forYIndexButton.config(state=DISABLED)

        except Exception as e:
             #print(str(e))
             pass

    def generateMenu(self):
        while (self.__setterFrame.winfo_width() < 2
           or  self.__canvas.winfo_width()      < 2): sleep(0.000005)

        self.__backColor = "$00"

        self.__backImage = self.__loader.io.getImg("backwards", None)
        self.__forImage = self.__loader.io.getImg("forwards", None)
        self.__playImage = self.__loader.io.getImg("play", None)
        self.__stopImage = self.__loader.io.getImg("stop", None)

        self.__thePlayer = Frame(self.__setterFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 16, width = self.__setterFrame.winfo_width())
        self.__thePlayer.pack_propagate(False)
        self.__thePlayer.pack(side=TOP, anchor=N, fill=X)

        f1 = Frame(self.__thePlayer, bg=self.__loader.colorPalettes.getColor("window"),
                   height=self.__sizes[1] // 12, width = self.__setterFrame.winfo_width() // 4)
        f1.pack_propagate(False)
        f1.pack(side=LEFT, anchor=E, fill=Y)

        f2 = Frame(self.__thePlayer, bg=self.__loader.colorPalettes.getColor("window"),
                   height=self.__sizes[1] // 12, width = self.__setterFrame.winfo_width() // 4)
        f2.pack_propagate(False)
        f2.pack(side=LEFT, anchor=E, fill=Y)

        f3 = Frame(self.__thePlayer, bg=self.__loader.colorPalettes.getColor("window"),
                   height=self.__sizes[1] // 12, width = self.__setterFrame.winfo_width() // 4)
        f3.pack_propagate(False)
        f3.pack(side=LEFT, anchor=E, fill=Y)

        f4 = Frame(self.__thePlayer, bg=self.__loader.colorPalettes.getColor("window"),
                   height=self.__sizes[1] // 12, width = self.__setterFrame.winfo_width() // 4)
        f4.pack_propagate(False)
        f4.pack(side=LEFT, anchor=E, fill=Y)

        self.__frames.append(f1)
        self.__frames.append(f2)
        self.__frames.append(f3)
        self.__frames.append(f4)

        self.__backButton = Button(f1, bg=self.__loader.colorPalettes.getColor("window"),
                                   image=self.__backImage,
                                   width=self.__sizes[0], state=DISABLED, command=self.__decIndex)




        self.__forButton = Button(f3, bg=self.__loader.colorPalettes.getColor("window"),
                                   image=self.__forImage,
                                   width=self.__sizes[0], state=DISABLED, command=self.__incIndex)

        self.__playButton = Button(f4, bg=self.__loader.colorPalettes.getColor("window"),
                                   image=self.__playImage,
                                   width=self.__sizes[0], state=DISABLED, command=self.__play)

        self.__backButton.pack_propagate(False)
        self.__backButton.pack(side=LEFT, anchor=W, fill=Y)
        self.__forButton.pack_propagate(False)
        self.__forButton.pack(side=LEFT, anchor=W, fill=Y)
        self.__playButton.pack_propagate(False)
        self.__playButton.pack(side=LEFT, anchor=W, fill=Y)

        self.__indexVal = StringVar()
        self.__indexVal.set("0")

        self.__indexEntry = Entry(f2, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                   width=99,
                                   fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                   textvariable = self.__indexVal, name = "indexEntry",
                                   state=DISABLED, font=self.__bigFont, justify = CENTER,
                                   command=None)

        self.__indexEntry.pack_propagate(False)
        self.__indexEntry.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__indexEntry, "<FocusOut>", self.__checkIndexEntry, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__indexEntry, "<KeyRelease>", self.__checkIndexEntry, 1)

        self.__backSetter = VisualEditorFrameWithLabelAndEntry(
            self.__loader, "$00", self.__setterFrame, self.__sizes[1] // 25, "testColor", self.__smallFont,
            self.checkBGColorEntry, self.checkBGColorEntry)

        self.checkBGColorEntry(None)

        self.__speedSetter = VisualEditorFrameWithLabelAndEntry(
            self.__loader, "1", self.__setterFrame, self.__sizes[1] // 25, "testSpeed", self.__smallFont,
            self.checkSpeedEntry, self.checkSpeedEntry)

        self.__linesSetter = VisualEditorFrameWithLabelAndEntry(
            self.__loader, str(self.__numOfLines), self.__setterFrame, self.__sizes[1] // 25, "numOfLines", self.__smallFont,
            self.checkLineNumEntry, self.checkLineNumEntry)

        self.__linesSetter.setLabelText(self.__dictionaries.getWordFromCurrentLanguage("numOfLines") + ":")

        self.__frameNumSetter = VisualEditorFrameWithLabelAndEntry(
            self.__loader, "1", self.__setterFrame, self.__sizes[1] // 25, "frameNum", self.__smallFont,
            self.checkFrameNum, self.checkFrameNum)

        self.__indexSetter = VisualEditorFrameWithLabelAndEntry(
            self.__loader, "0", self.__setterFrame, self.__sizes[1] // 25, "index", self.__smallFont,
            self.checkYIndex, self.checkYIndex)

        self.__speed = 1

        self.__backSetter.getEntry().config(state     = DISABLED)
        self.__linesSetter.getEntry().config(state    = DISABLED)
        self.__speedSetter.getEntry().config(state    = DISABLED)
        self.__frameNumSetter.getEntry().config(state = DISABLED)
        self.__indexSetter.getEntry().config(state    = DISABLED)

        self.__disabledOnes.append(self.__backSetter.getEntry())
        self.__disabledOnes.append(self.__linesSetter.getEntry())
        self.__disabledOnes.append(self.__speedSetter.getEntry())
        self.__disabledOnes.append(self.__frameNumSetter.getEntry())
        self.__disabledOnes.append(self.__indexSetter.getEntry())

        self.__indexButtons = Frame(self.__setterFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 20, width = self.__setterFrame.winfo_width())
        self.__indexButtons.pack_propagate(False)
        self.__indexButtons.pack(side=TOP, anchor=N, fill=X)

        self.__indexButtonLeft = Frame(self.__indexButtons, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 20, width = self.__setterFrame.winfo_width() // 2)
        self.__indexButtonLeft.pack_propagate(False)
        self.__indexButtonLeft.pack(side=LEFT, anchor=E, fill=Y)

        self.__indexButtonRight = Frame(self.__indexButtons, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 20, width = self.__setterFrame.winfo_width() // 2)
        self.__indexButtonRight.pack_propagate(False)
        self.__indexButtonRight.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__backYIndexButton = Button(self.__indexButtonLeft, bg=self.__loader.colorPalettes.getColor("window"),
                                   image=self.__backImage,
                                   width=self.__sizes[0], state=DISABLED, command=self.__decYIndex)

        self.__forYIndexButton = Button(self.__indexButtonRight, bg=self.__loader.colorPalettes.getColor("window"),
                                   image=self.__forImage,
                                   width=self.__sizes[0], state=DISABLED, command=self.__incYIndex)

        self.__backYIndexButton.pack_propagate(False)
        self.__backYIndexButton.pack(side=TOP, anchor=N, fill=BOTH)

        self.__forYIndexButton.pack_propagate(False)
        self.__forYIndexButton.pack(side=TOP, anchor=N, fill=BOTH)

        self.__boxFrame = Frame(self.__setterFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 22, width = self.__setterFrame.winfo_width())
        self.__boxFrame.pack_propagate(False)
        self.__boxFrame.pack(side=TOP, anchor=N, fill=X)

        self.__boxButtonVal = IntVar()
        self.__boxButton = Checkbutton(self.__boxFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                    fg=self.__loader.colorPalettes.getColor("boxFontNormal"), state = DISABLED,
                                    font=self.__miniFont, text=self.__dictionaries.getWordFromCurrentLanguage("repeatingIsOnTop"),
                                    variable=self.__boxButtonVal
                                    )
        self.__boxButton.pack(side=LEFT, anchor=N, fill=X)

        self.__boxFrame2 = Frame(self.__setterFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 22, width = self.__setterFrame.winfo_width())
        self.__boxFrame2.pack_propagate(False)
        self.__boxFrame2.pack(side=TOP, anchor=N, fill=X)

        self.__boxButtonVal2 = IntVar()
        self.__boxButton2 = Checkbutton(self.__boxFrame2, bg=self.__loader.colorPalettes.getColor("window"),
                                    fg=self.__loader.colorPalettes.getColor("boxFontNormal"), state = DISABLED,
                                    font=self.__miniFont, text=self.__dictionaries.getWordFromCurrentLanguage("addBorders"),
                                    variable=self.__boxButtonVal2
                                    )
        self.__boxButton2.pack(side=LEFT, anchor=N, fill=X)

        self.__patternMainFrame = Frame(self.__setterFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 18, width = self.__setterFrame.winfo_width())
        self.__patternMainFrame.pack_propagate(False)
        self.__patternMainFrame.pack(side=TOP, anchor=N, fill=X)

        self.__patternLabelFrame = Frame(self.__patternMainFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 18, width = self.__setterFrame.winfo_width() // 4 * 3)
        self.__patternLabelFrame.pack_propagate(False)
        self.__patternLabelFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__patternButtonFrame = Frame(self.__patternMainFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 18, width = self.__setterFrame.winfo_width() // 4)
        self.__patternButtonFrame.pack_propagate(False)
        self.__patternButtonFrame.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__patternLabel = Label(self.__patternLabelFrame,
                                    text=self.__dictionaries.getWordFromCurrentLanguage("repeatingPattern"),
                                    font=self.__smallFont, fg=self.__colors.getColor("font"),
                                    bg=self.__colors.getColor("window")
                                    )

        self.__patternLabel.pack_propagate(False)
        self.__patternLabel.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__repeatingPattern = FortariMB(self.__loader, self.__patternButtonFrame, DISABLED,
                                            self.__smallFont, self.__pattern, self.__patterns, False, False,
                                            self.selectedChanged, [self.__pattern])

        self.__disabledOnes.append(self.__boxButton)
        self.__disabledOnes.append(self.__boxButton2)
        self.__disabledOnes.append(self.__repeatingPattern)

        from VisualLoaderFrame import VisualLoaderFrame

        self.__loaderFrame = Frame(self.__setterFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] //12, width = self.__setterFrame.winfo_width())
        self.__loaderFrame.pack_propagate(False)
        self.__loaderFrame.pack(side=TOP, anchor=N, fill=X)

        self.__testerFrame = Frame(self.__setterFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 20, width = self.__setterFrame.winfo_width())
        self.__testerFrame.pack_propagate(False)
        self.__testerFrame.pack(side=TOP, anchor=N, fill=X)

        self.__importFrame = Frame(self.__setterFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 20, width = self.__setterFrame.winfo_width())
        self.__importFrame.pack_propagate(False)
        self.__importFrame.pack(side=TOP, anchor=N, fill=X)

        while (self.__loaderFrame.winfo_width() < 2): sleep(0.00001)

        self.__spriteLoader = VisualLoaderFrame(self.__loader, self.__loaderFrame, self.__loaderFrame.winfo_height()//2, self.__smallFont, self.__miniFont,
                                                None, "Better_Than_AI", "loadPicture", self.checkIfValidFileName,
                                                self.__setterFrame.winfo_width() // 2, self.__open, self.__save)

        while (self.__testerFrame.winfo_width() < 2): sleep(0.00001)

        from EmuTestFrame import EmuTestFrame

        self.__testWithEmulatorFrame = EmuTestFrame(self.__loader, self.__testerFrame, self.__testerFrame.winfo_height(), self.__normalFont,
                                                    self.__setterFrame.winfo_width() // 2, self.__loadTest, BOTTOM, S)

        while (self.__importFrame.winfo_width() < 2): sleep(0.00001)

        from ConvertFromImageFrame import ConvertFromImageFrame

        self.__convertFromImage = ConvertFromImageFrame(self.__loader, self.__importFrame, self.__importFrame.winfo_height(), self.__normalFont,
                                                        self.__setterFrame.winfo_width() // 2, self.__importImage,
                                                        TOP, N)

        self.__finished[2] = True

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

    def __importImage(self):
        pass

    def __loadTest(self):
        pass

    def __open(self):
        pass

    def __save(self):
        pass

    def __decYIndex(self):
        self.checkYIndex(-1)

    def __incYIndex(self):
        self.checkYIndex(1)

    def selectedChanged(self):
        self.__pattern = self.__repeatingPattern.getSelected()
        self.reDrawCanvas(None)

    def checkYIndex(self, event):
        if type(event) != int:
           val   = self.__indexSetter.getValue()
        else:
           val   = self.__Y + event

        entry = self.__indexSetter.getEntry()

        try:
            num = int(val)
        except:
            entry.config(bg=self.__colors.getColor("boxBackUnSaved"), fg=self.__colors.getColor("boxFontUnSaved"))
            return

        entry.config(bg=self.__colors.getColor("boxBackNormal"), fg=self.__colors.getColor("boxFontNormal"))

        if   num > self.__numOfLines - (self.__ySize // len(self.__xSize)):
             num = self.__numOfLines - (self.__ySize // len(self.__xSize))

        if   num < 0:
             num = 0

        if num != self.__Y:
            self.__Y = num
            self.fillEditorEntries()
            self.reDrawCanvas(None)

        self.__indexSetter.setValue(str(num))
        entry.icursor(len(str(num)))

    def checkIfThereIsSomethingOnThePrev(self, y, key, x, button):
        prevFrame = self.__frameIndex - 1
        if prevFrame < 0: prevFrame = self.__frameNum - 1

        if self.__data[prevFrame][y][key][x] == 1:
           self.colorTile(button, 2, key)


    def fillEditorEntries(self):
        for y in range(self.__Y, self.__Y + (self.__ySize // len(self.__xSize))):
            for key in self.__data[self.__frameIndex][y]:
                for x in range(0, len(self.__data[self.__frameIndex][y][key])):
                    self.__dataLines[y-self.__Y][key]["values"][x] = self.__data[self.__frameIndex][y][key][x]
                    self.colorTile(
                        self.__dataLines[y - self.__Y][key]["buttons"][x],
                        self.__dataLines[y - self.__Y][key]["values"][x],
                        key)

                    if self.__frameNum > 1 and self.__data[self.__frameIndex][y][key][x] == 0:
                        self.checkIfThereIsSomethingOnThePrev(y, key, x, self.__dataLines[y - self.__Y][key]["buttons"][x])

            for key in self.__colorData[self.__frameIndex][y]:
                self.__colorDataLines[y-self.__Y]["entries"][key].setValue(
                    self.__colorData[self.__frameIndex][y][key]
                )
                self.__colorDataLines[y - self.__Y]["colors"][key][0] = self.__colorData[self.__frameIndex][y][key]


    def checkLineNumEntry(self, event):
        val   = self.__linesSetter.getValue()
        entry = self.__linesSetter.getEntry()

        try:
            num = int(val)
        except:
            entry.config(bg=self.__colors.getColor("boxBackUnSaved"), fg=self.__colors.getColor("boxFontUnSaved"))
            return

        entry.config(bg=self.__colors.getColor("boxBackNormal"), fg=self.__colors.getColor("boxFontNormal"))
        if   num < 1:   num = 1
        elif num > 255: num = 255

        if self.__numOfLines != num:
            self.numOfLinesChanged(num)
            self.__numOfLines = num
            self.checkFrameNum(None)
            self.checkYIndex(None)
            self.reDrawCanvas(None)

        self.__linesSetter.setValue(str(num))
        entry.icursor(len(str(num)))

    def numOfLinesChanged(self, newNum):
        for y in range(0, self.__ySize // len(self.__xSize), 1):
               for key in self.__keys:
                   if key in self.__dataLines[y]:
                       index = -1
                       for button in self.__dataLines[y][key]["buttons"]:
                           index += 1
                           if y < newNum:
                              button.config(state = NORMAL)
                              self.colorTile(button,
                                             self.__dataLines[y][key]["values"][index], key
                                             )
                              if self.__frameNum > 1 and self.__data[self.__frameIndex][y + self.__Y][key][index] == 0:
                                 self.checkIfThereIsSomethingOnThePrev(y + self.__Y, key, index, button)

                           else:
                              button.config(state = DISABLED, bg = self.__colors.getColor("fontDisabled"))

                   if y < newNum:
                      self.__colorDataLines[y]["entries"][key].changeState(NORMAL)
                   else:
                      self.__colorDataLines[y]["entries"][key].changeState(DISABLED)

        if len(self.__data[0]) < newNum:
           for indexNum in range(0, len(self.__data)):
               while (len(self.__data[indexNum]) < newNum):
                      self.__data[indexNum]     .append(deepcopy(self.__temp     ))
                      self.__colorData[indexNum].append(deepcopy(self.__colorTemp))

    def checkSpeedEntry(self, event):
        val   = self.__speedSetter.getValue()
        entry = event.widget

        try:
            num = int(val)
        except:
            entry.config(bg=self.__colors.getColor("boxBackUnSaved"), fg=self.__colors.getColor("boxFontUnSaved"))
            return

        entry.config(bg=self.__colors.getColor("boxBackNormal"), fg=self.__colors.getColor("boxFontNormal"))
        if   num < 1  : num = 1
        elif num > 16 : num = 16

        self.__speed = num
        self.__speedSetter.setValue(str(num))

        entry.icursor(len(str(num)))

    def checkFrameNum(self, event):
        val   = self.__frameNumSetter.getValue()
        entry = self.__frameNumSetter.getEntry()

        try:
            num = int(val)
        except:
            entry.config(bg=self.__colors.getColor("boxBackUnSaved"), fg=self.__colors.getColor("boxFontUnSaved"))
            return

        entry.config(bg=self.__colors.getColor("boxBackNormal"), fg=self.__colors.getColor("boxFontNormal"))
        if   num < 1                       : num = 1
        if   num > 256 // self.__numOfLines: num = 256 // self.__numOfLines
        if   num > 16                      : num = 16

        if num != self.__frameNum:
           self.__frameNum = num
           self.addNewInitData(num)

           self.__checkIndexEntry(None)
           self.reDrawCanvas(None)

        self.__frameNumSetter.setValue(str(num))
        entry.icursor(len(str(num)))

    def addNewInitData(self, numOfFrames):
        if numOfFrames > len(self.__data):
           for num in range(0, (numOfFrames - len(self.__data))):
               self.__data     .append([])
               self.__colorData.append([])
               for num2 in range(0, self.__numOfLines):
                  self.__data     [-1].append(deepcopy(self.__temp     ))
                  self.__colorData[-1].append(deepcopy(self.__colorTemp))

    def checkBGColorEntry(self, event):
        if (len(self.__backSetter.getValue()))<3:
            self.__backSetter.getEntry().config(
                bg=self.__colors.getColor("boxBackUnSaved"), fg=self.__colors.getColor("boxFontUnSaved"))
            return
        elif (len(self.__backSetter.getValue()))>3:
            self.__backSetter.setValue(self.__backSetter.getValue()[:3])

        if self.__backSetter.getValue()[0]!="$":
            self.__backSetter.getEntry().config(
                bg=self.__colors.getColor("boxBackUnSaved"), fg=self.__colors.getColor("boxFontUnSaved"))
            return
        try:
            num = int(self.__backSetter.getValue().replace("$", "0x"), 16)
        except:
            self.__backSetter.getEntry().config(
                bg=self.__colors.getColor("boxBackUnSaved"), fg=self.__colors.getColor("boxFontUnSaved"))
            return
        try:
            t = int("0x"+self.__backSetter.getValue()[-1], 16)
            if t % 2 == 1:
                t = t-1
                self.__backSetter.setValue(self.__backSetter.getValue()[:-1]+hex(t).replace("0x",""))

            color1 = self.__colorDict.getHEXValueFromTIA(self.__backSetter.getValue())

            num = int("0x"+self.__backSetter.getValue()[2], 16)
            if num>8:
                num = self.__backSetter.getValue()[:2]+hex(num-6).replace("0x","")
            else:
                num = self.__backSetter.getValue()[:2]+hex(num+6).replace("0x","")

            color2 = self.__colorDict.getHEXValueFromTIA(num)
            self.__backSetter.getEntry().config(bg=color1, fg=color2)
        except:
            pass

        self.__backSetter.getEntry().icursor(len(self.__backSetter.getValue()))
        self.__backColor = self.__backSetter.getValue()
        self.reDrawCanvas(None)

    def __checkIndexEntry(self, event):
        val   = self.__indexEntry.get()
        entry = self.__indexEntry

        try:
            num = int(val)
        except:
            entry.config(bg=self.__colors.getColor("boxBackUnSaved"), fg=self.__colors.getColor("boxFontUnSaved"))
            return

        if    num < 0                  : num = 0
        elif  num > self.__frameNum - 1: num = self.__frameNum - 1

        entry.config(bg=self.__colors.getColor("boxBackNormal"), fg=self.__colors.getColor("boxFontNormal"))
        self.__changeIndex(num, False, True)
        entry.icursor(len(str(num)))
        self.fillEditorEntries()
        self.reDrawCanvas(None)

    def __decIndex(self):
        self.__changeIndex(-1, True, True)

    def __incIndex(self):
        self.__changeIndex(1, True, True)

    def __play(self):
        self.__isPlaying = 1 - self.__isPlaying

        if self.__isPlaying:
           p = Thread(target = self.__playThread)
           p.daemon = True
           p.start()

    def __playThread(self):
        while (self.__isPlaying and self.dead == False and self.__loader.mainWindow.dead == False):
            self.__changeIndex(1, True, True)
            sleep(1 / (self.__speed // 2) )

    def __changeIndex(self, val, relative, update):
        old = self.__frameIndex

        if relative:
           self.__frameIndex += val
        else:
           self.__frameIndex = val

        if   self.__frameIndex < 0: self.__frameIndex = self.__frameNum - 1
        elif self.__frameIndex >= self.__frameNum: self.__frameIndex = 0

        if update: self.__indexVal.set(str(self.__frameIndex))

        if old != self.__frameIndex:
           self.fillEditorEntries()
           self.reDrawCanvas(None)

    def generateColorFields(self):
        while (self.__colorFrame.winfo_width() < 2): sleep(0.000005)

        sizeY = self.__colorFrame.winfo_height() // self.__ySize * len(self.__xSize)
        sizeX = self.__colorFrame.winfo_width()

        self.__colorDataLines = []
        self.__colorTemp      = {self.__keys[0]: "$1E",
                                 self.__keys[1]: "$44",
                                 self.__keys[2]: "$0E",
                                 self.__keys[3]: "$00"}


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
                    "colors":  {self.__keys[0]: [self.__colorTemp[self.__keys[0]]],
                                self.__keys[1]: [self.__colorTemp[self.__keys[1]]],
                                self.__keys[2]: [self.__colorTemp[self.__keys[2]]],
                                self.__keys[3]: [self.__colorTemp[self.__keys[3]]]},
                    "entries": {self.__keys[0]:  None  , self.__keys[1]:  None  , self.__keys[2]:  None  , self.__keys[3]:  None  }
                }
            )

            self.__colorData[0].append(deepcopy(self.__colorTemp))

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
                                                                   0, None, self.changedColorValie)
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
                                                                                0, None, self.changedColorValie)
                self.__colorDataLines[-1]["entries"][self.__keys[subNum]].changeState(DISABLED)
                self.__disabledOnes.append(self.__colorDataLines[-1]["entries"][self.__keys[subNum]])

        self.__finished[1] = True

    def changedColorValie(self, event):
        for y in range(0, len(self.__colorDataLines)):
            for key in self.__colorDataLines[y]["entries"]:
                if self.__colorDataLines[y]["entries"][key].getEntry() == event.widget:
                   self.__colorData[self.__frameIndex][y + self.__Y][key] = self.__colorDataLines[y]["entries"][key].getValue()
                   break

        self.reDrawCanvas(None)

    def reDrawCanvas(self, dummy):
        if False in self.__finished:
           return

        if dummy != "noSave": self.changed = True

        self.__canvas.clipboard_clear()
        self.__canvas.delete("all")
        #self.__canvas.config(bg = self.__colorDict.getHEXValueFromTIA(self.__backColor))

        xUnit = self.__canvas.winfo_width()  // self.__xSize[0]
        yUnit = self.__canvas.winfo_height() // self.__numOfLines

        order = {
            False: [self.__keys[3], self.__keys[2], self.__keys[1], self.__keys[0]],
            True:  [self.__keys[3], self.__keys[2], self.__keys[0], self.__keys[1]]
        }

        lenghts = {
            self.__keys[0]: max(self.__xSize) // self.__xSize[0],
            self.__keys[1]: max(self.__xSize) // self.__xSize[1],
            self.__keys[2]: max(self.__xSize) // self.__xSize[2]
        }

        for y in range(0, len(self.__dataLines)):
            for key in order[self.__repeatingOnTop]:
                c = self.__colorDict.getHEXValueFromTIA(self.__colorDataLines[y]["colors"][key][0])
                if key not in self.__dataLines[y].keys():
                   self.__canvas.create_rectangle(0                          , y      * yUnit,
                                                  self.__canvas.winfo_width(),(y + 1) * yUnit,
                                                  outline = "", fill = c)

                else:
                    for x in range(0, len(self.__dataLines[y][key]["values"])):
                        val    = self.__dataLines[y][key]["values"][x]
                        lenght = lenghts[key]

                        if key == "layerRepeating":
                           segmentNum = x // (self.__xSize[1] // 3)
                           if self.__pattern[segmentNum] == "0": val = 0

                        if val != 0:
                           self.__canvas.create_rectangle( x    * lenght * xUnit,  y      * yUnit,
                                                          (x+1) * lenght * xUnit, (y + 1) * yUnit,
                                                          outline="", fill=c)


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

                        colors = ["boxBackNormal", "fontDisabled"]

                        b = Button(fSubSub, name=(self.__keys[sub] + "_" + xNum + "," + str(y)),
                                   bg=self.__loader.colorPalettes.getColor(colors[sub%2]), state = DISABLED,
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

        self.colorTile(button, self.__dataLines[theY][levelKey]["values"][theX], levelKey)

        self.__data[self.__frameIndex][theY + self.__Y][levelKey][theX] = self.__dataLines[theY][levelKey]["values"][theX]

        if self.__frameNum > 1 and self.__dataLines[theY][levelKey]["values"][theX] == 0:
           self.checkIfThereIsSomethingOnThePrev(theY + self.__Y, levelkey, theX, button)

        if self.ignore == False:
           if levelKey == "layerRepeating":
               others = self.getOtherTwoX(theX)
               self.ignore = True

               #self.__dataLines[theY][levelKey]["values"][others[0]] = self.__dataLines[theY][levelKey]["values"][theX]
               #self.__dataLines[theY][levelKey]["values"][others[1]] = self.__dataLines[theY][levelKey]["values"][theX]
               for num in others:
                   event.widget = self.__dataLines[theY][levelKey]["buttons"][num]
                   self.__clicked(event)
               self.ignore = False

           self.reDrawCanvas(None)
           self.changed = True

    def getOtherTwoX(self, x):
        currentBigPoz = x // 16
        currentOffset = x %  16

        nums     = [0, 1, 2]
        returnMe = []

        for num in nums:
            if currentBigPoz == num: continue
            returnMe.append(num * 16 + currentOffset)

        return returnMe

    def colorTile(self, button, value, levelKey):
        colors = {self.__keys[0]: ["boxBackNormal", "boxFontNormal", "highLight"],
                  self.__keys[1]: ["fontDisabled" , "boxFontNormal", "highLight"],
                  self.__keys[2]: ["boxBackNormal", "boxFontNormal", "highLight"],
                  }
        button.config(bg = self.__colors.getColor(colors[levelKey][value]))

    def __enter(self, event):
        if self.__draw: self.__clicked(event)

    def drawMode(self, event):
        self.__draw = 1 - self.__draw

    def shiftON(self, event):
        self.__ctrl = True

    def shiftOff(self, event):
        self.__ctrl = False


