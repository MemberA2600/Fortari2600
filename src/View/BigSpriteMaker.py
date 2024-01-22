from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from Compiler import Compiler

class BigSpriteMaker:

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

        self.__delay   = 0
        self.__counter = 0

        self.__ctrl = False
        self.__middle = False
        self.__draw = 0

        self.__frameNumMax = 16

        self.__Y = 0
        self.__h = 8
        self.__frameNum = 0
        self.__numOfFrames = 1
        self.__backColor = "$00"
        self.__speed = 0
        self.__lineHeight = 2

        self.__canvasX = 0
        self.__canvasStartX = 0
        self.__canvasY = 0
        self.__width = 1
        self.__direction = 0

        self.__play = False

        # valid: simple, double, overlay
        self.__mode = "overlay"

        self.__activeMode = ""
        self.__finished = False
        self.__finished2 = False

        self.__sizes = [self.__screenSize[0] / 1.5, self.__screenSize[1] / 1.10 - 40]
        self.__window = SubMenu(self.__loader, "bigSprite", self.__sizes[0], self.__sizes[1], None, self.__addElements, 1)

        self.dead = True

    def __closeWindow(self):
        if self.changed == True:
            answer = self.__fileDialogs.askYesNoCancel("notSavedFile", "notSavedFileMessage")
            if answer == "Yes":
                self.__saveSprite()
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

        self.__editorFrame = Frame(self.__topLevelWindow, height=self.__sizes[1],
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0]//2
                                   )
        self.__editorFrame.pack_propagate(False)
        self.__editorFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__controlFrame = Frame(self.__topLevelWindow, height=self.__sizes[1],
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0]//2
                                   )
        self.__controlFrame.pack_propagate(False)
        self.__controlFrame.pack(side=LEFT, anchor=E, fill=BOTH)

        one = Thread(target=self.__oneThread)
        one.daemon = True
        one.start()

        two = Thread(target=self.__twoThread())
        two.daemon = True
        two.start()

        self.__topLevelWindow.bind("<KeyPress-Control_L>", self.shiftON)
        self.__topLevelWindow.bind("<KeyRelease-Control_L>", self.shiftOff)
        self.__topLevelWindow.bind("<KeyPress-Control_R>", self.shiftON)
        self.__topLevelWindow.bind("<KeyRelease-Control_R>", self.shiftOff)
        self.__topLevelWindow.bind("<Button-2>", self.drawMode)

        self.__loader.threadLooper.addToThreading(self, self.__loop, [], 1)

        #t = Thread(target=self.__loop)
        #t.daemon = True
        #t.start()

    def __oneThread(self):
        self.__createData()
        try:
            self.__createEditor()

            self.__frameNumSetter.getEntry().config(state = NORMAL)
            self.__testColorSetter.getEntry().config(state = NORMAL)
            self.__testSpeedSetter.getEntry().config(state = NORMAL)
            self.__heightSetter.getEntry().config(state = NORMAL)
            self.__widthSetter.getEntry().config(state = NORMAL)
            self.__lineHeightSetter.getEntry().config(state = NORMAL)

        except:
            pass

        self.__finished = True

    def __twoThread(self):

        self.__previewLabel = Label(self.__controlFrame,
                                    text=self.__dictionaries.getWordFromCurrentLanguage("preview"),
                                    font=self.__normalFont, fg=self.__colors.getColor("font"),
                                    bg=self.__colors.getColor("window")
                                    )

        self.__previewLabel.pack_propagate(False)
        self.__previewLabel.pack(side=TOP, anchor=N, fill=X)

        self.__canvas = Canvas(self.__controlFrame, bg="black", bd=0,
                               width=self.__sizes[0]//2,
                               height=round(self.__sizes[0]//2 * 3 // 6)
                               )

        self.__canvas.pack_propagate(False)
        self.__canvas.pack(side=TOP, anchor=N, fill=X)

        self.__thePlayer = Frame(self.__controlFrame, bg="red", height=round(self.__sizes[1] // 20))
        self.__thePlayer.config(width=999999)
        self.__thePlayer.pack_propagate(False)
        self.__thePlayer.pack(side=TOP, anchor=N, fill=X)

        self.__indexVal = StringVar()
        self.__indexVal.set("0")

        self.__backImage = self.__loader.io.getImg("backwards", None)
        self.__forImage = self.__loader.io.getImg("forwards", None)
        self.__playImage = self.__loader.io.getImg("play", None)
        self.__stopImage = self.__loader.io.getImg("stop", None)


        self.__backButton = Button(self.__thePlayer, bg=self.__loader.colorPalettes.getColor("window"),
                                   image=self.__backImage,
                                   width= self.__sizes[0] // 8,
                                   state=DISABLED,
                                   command=self.decIndex)

        self.__indexEntryFrame = Frame(self.__thePlayer, bg=self.__loader.colorPalettes.getColor("window"),
                                       width=self.__sizes[0] // 8)

        self.__indexEntry = Entry(self.__indexEntryFrame, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                   width=99,
                                   fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                   textvariable = self.__indexVal, name = "indexEntry",
                                   state=DISABLED, font=self.__bigFont, justify = CENTER,
                                   command=None)

        self.__forButton = Button(self.__thePlayer, bg=self.__loader.colorPalettes.getColor("window"),
                                   image=self.__forImage,
                                   width=self.__sizes[0] // 8,
                                   state=DISABLED,
                                   command=self.incIndex)

        self.__playButton = Button(self.__thePlayer, bg=self.__loader.colorPalettes.getColor("window"),
                                   image=self.__playImage, state = DISABLED,
                                   width=self.__sizes[0] // 8,
                                   command=self.__playing)


        self.__backButton.pack_propagate(False)
        self.__backButton.pack(side=LEFT, anchor=W, fill=Y)
        self.__indexEntryFrame.pack_propagate(False)
        self.__indexEntryFrame.pack(side=LEFT, anchor=W, fill=Y)
        self.__indexEntry.pack_propagate(False)
        self.__indexEntry.pack(side=LEFT, anchor=W, fill=BOTH)
        self.__forButton.pack_propagate(False)
        self.__forButton.pack(side=LEFT, anchor=W, fill=Y)
        self.__playButton.pack_propagate(False)
        self.__playButton.pack(side=LEFT, anchor=W, fill=Y)

        self.__indexEntry.bind("<KeyRelease>", self.__checkIndex)
        self.__indexEntry.bind("<FocusOut>", self.__checkIndex)

        self.__theSetters = Frame(self.__controlFrame, bg=self.__colors.getColor("window"),
                                  height=round(self.__sizes[1] // 32 * 6))
        self.__theSetters.config(width=999999)
        self.__theSetters.pack_propagate(False)
        self.__theSetters.pack(side=TOP, anchor=N, fill=X)

        from VisualEditorFrameWithLabelAndEntry import VisualEditorFrameWithLabelAndEntry


        self.__frameNumSetter = VisualEditorFrameWithLabelAndEntry(
                                self.__loader, "1", self.__theSetters, round(self.__sizes[1] // 32), "frameNum", self.__smallFont,
                                self.checkFrameNumEntry, self.checkFrameNumEntry)

        self.__testColorSetter = VisualEditorFrameWithLabelAndEntry(
                                self.__loader, "", self.__theSetters, round(self.__sizes[1] // 32), "testColor", self.__smallFont,
                                self.checkTestColorEntry, self.checkTestColorEntry)

        self.__testSpeedSetter = VisualEditorFrameWithLabelAndEntry(
                                self.__loader, "", self.__theSetters, round(self.__sizes[1] // 32), "testSpeed", self.__smallFont,
                                self.checkTesSpeedEntry, self.checkTesSpeedEntry)

        self.__heightSetter = VisualEditorFrameWithLabelAndEntry(
                                self.__loader, "8", self.__theSetters, round(self.__sizes[1] // 32), "height", self.__smallFont,
                                self.checkHeightEntry, self.checkHeightEntry)

        self.__widthSetter = VisualEditorFrameWithLabelAndEntry(
                                self.__loader, "1", self.__theSetters, round(self.__sizes[1] // 32), "testWidth", self.__smallFont,
                                self.checkWidthEntry, self.checkWidthEntry)

        self.__lineHeightSetter = VisualEditorFrameWithLabelAndEntry(
                                self.__loader, "2", self.__theSetters, round(self.__sizes[1] // 32), "lineHeight", self.__smallFont,
                                self.checkLineHeight, self.checkLineHeight)

        self.__frameNumSetter.getEntry().config(state = DISABLED)
        self.__testColorSetter.getEntry().config(state = DISABLED)
        self.__testSpeedSetter.getEntry().config(state = DISABLED)
        self.__heightSetter.getEntry().config(state = DISABLED)
        self.__widthSetter.getEntry().config(state = DISABLED)
        self.__lineHeightSetter.getEntry().config(state = DISABLED)

        self.__horMoveFrame = Frame(self.__controlFrame, bg=self.__colors.getColor("window"),
                                  height=round(self.__sizes[1] // 32))
        self.__horMoveFrame.config(width=999999)
        self.__horMoveFrame.pack_propagate(False)
        self.__horMoveFrame.pack(side=TOP, anchor=N, fill=X)

        self.__moveHor = BooleanVar()
        self.__moveHor.set(1)

        self.__horBox = Checkbutton(self.__horMoveFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                    fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                    font=self.__smallFont, text=self.__dictionaries.getWordFromCurrentLanguage("horMove"),
                                    variable=self.__moveHor
                                    )
        self.__horBox.pack(side=LEFT, anchor=N, fill=Y)

        self.__horBox.bind("<Button-1>", self.__redrawCanvasClick)
        self.__redrawCanvas()

        self.__heightIndexF = Frame(self.__controlFrame, bg=self.__colors.getColor("window"),
                                  height=round(self.__sizes[1] // 32 * 2))
        self.__heightIndexF.config(width=999999)
        self.__heightIndexF.pack_propagate(False)
        self.__heightIndexF.pack(side=TOP, anchor=N, fill=X)

        self.__heightIndexLabel = Label(self.__heightIndexF,
                                        bg = self.__colors.getColor("window"),
                                        fg = self.__colors.getColor("font"),
                                        text = self.__dictionaries.getWordFromCurrentLanguage("heightIndex"),
                                        font = self.__smallFont
                                        )
        self.__heightIndexLabel.config(width=999999)
        self.__heightIndexLabel.pack_propagate(False)
        self.__heightIndexLabel.pack(side=TOP, anchor=N, fill=X)

        self.__heightIndexBottom = Frame(self.__heightIndexF, bg=self.__colors.getColor("window"),
                                  height=round(self.__sizes[1] // 32 ))
        self.__heightIndexBottom.config(width=999999)
        self.__heightIndexBottom.pack_propagate(False)
        self.__heightIndexBottom.pack(side=TOP, anchor=N, fill=X)

        self.__heightIndexF1 = Frame(self.__heightIndexBottom, bg=self.__colors.getColor("window"),
                                  height=round(self.__sizes[1] // 32 ))

        while self.__heightIndexF1.winfo_width() < 2:
            self.__heightIndexF1.config(width=self.__heightIndexF.winfo_width()//3)
            self.__heightIndexF1.pack_propagate(False)
            self.__heightIndexF1.pack(side=LEFT, anchor=E, fill=X)

        self.__heightIndexF2 = Frame(self.__heightIndexBottom, bg=self.__colors.getColor("window"),
                                  height=round(self.__sizes[1] // 32 ))
        while self.__heightIndexF2.winfo_width() < 2:
            self.__heightIndexF2.config(width=self.__heightIndexF.winfo_width()//3)
            self.__heightIndexF2.pack_propagate(False)
            self.__heightIndexF2.pack(side=LEFT, anchor=E, fill=X)

        self.__heightIndexF3 = Frame(self.__heightIndexBottom, bg=self.__colors.getColor("window"),
                                  height=round(self.__sizes[1] // 32 * 2))


        while self.__heightIndexF3.winfo_width() < 2:
            self.__heightIndexF3.config(width=self.__heightIndexF.winfo_width()//3)
            self.__heightIndexF3.pack_propagate(False)
            self.__heightIndexF3.pack(side=LEFT, anchor=E, fill=X)


        self.__backYButton = Button(self.__heightIndexF1, bg=self.__loader.colorPalettes.getColor("window"),
                                   image=self.__backImage,
                                   width= self.__sizes[0] // 8,
                                   state=DISABLED,
                                   command=self.decYIndex)

        self.__YNum = StringVar()
        self.__YNum.set("0")
        self.__YNumEntry = Entry(self.__heightIndexF2, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                   width=99,
                                   fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                   textvariable = self.__YNum, name = "yEntry",
                                   state=DISABLED, font=self.__bigFont, justify = CENTER,
                                   command=None)

        self.__forYButton = Button(self.__heightIndexF3, bg=self.__loader.colorPalettes.getColor("window"),
                                   image=self.__forImage,
                                   width=self.__sizes[0] // 8,
                                   state=DISABLED,
                                   command=self.incYIndex)

        self.__backYButton.pack(fill=BOTH)
        self.__YNumEntry.pack(fill=BOTH)
        self.__forYButton.pack(fill=BOTH)

        self.__YNumEntry.bind("<KeyRelease>", self.__setYByEntry)
        self.__YNumEntry.bind("<FocusOut>", self.__setYByEntry)


        self.__spriteType = Frame(self.__controlFrame, bg=self.__colors.getColor("window"),
                                  height=round(self.__sizes[1] // 32 * 4))
        self.__spriteType.config(width=999999)
        self.__spriteType.pack_propagate(False)
        self.__spriteType.pack(side=TOP, anchor=N, fill=X)

        self.__spriteTypeF = Frame(self.__spriteType, bg=self.__colors.getColor("window"),
                                  height=round(self.__sizes[1] // 32))
        self.__spriteTypeF.config(width=999999)
        self.__spriteTypeF.pack_propagate(False)
        self.__spriteTypeF.pack(side=TOP, anchor=N, fill=X)

        self.__spriteTypeLabel = Label(self.__spriteTypeF, bg=self.__colors.getColor("window"),
                                 fg = self.__colors.getColor("font"), text = self.__dictionaries.getWordFromCurrentLanguage("spriteType"),
                                 font = self.__normalFont      )
        self.__spriteTypeLabel.pack_propagate(False)
        self.__spriteTypeLabel.pack(side=LEFT, anchor=E)

        self.__spriteTypeL = Frame(self.__spriteType, bg=self.__colors.getColor("window"),
                                  height=round(self.__sizes[1] // 32))
        self.__spriteTypeL.config(width=999999)
        self.__spriteTypeL.pack_propagate(False)
        self.__spriteTypeL.pack(side=TOP, anchor=N, fill=X)

        self.__spriteTypeL1 = Frame(self.__spriteTypeL, bg=self.__colors.getColor("window"),
                                  width=round(self.__sizes[0] // 8))
        self.__spriteTypeL1.pack_propagate(False)
        self.__spriteTypeL1.pack(side=LEFT, anchor=E, fill=Y)

        self.__spriteTypeL2 = Frame(self.__spriteTypeL, bg=self.__colors.getColor("window"),
                                  width=round(self.__sizes[0] // 8))
        self.__spriteTypeL2.pack_propagate(False)
        self.__spriteTypeL2.pack(side=LEFT, anchor=E, fill=Y)

        self.__spriteTypeL3 = Frame(self.__spriteTypeL, bg=self.__colors.getColor("window"),
                                  width=round(self.__sizes[0] // 8))
        self.__spriteTypeL3.pack_propagate(False)
        self.__spriteTypeL3.pack(side=LEFT, anchor=E, fill=Y)

        self.__spriteT = IntVar()
        self.__spriteT.set(3)

        self.__radio1 = Radiobutton(self.__spriteTypeL1, font = self.__normalFont,
                                    text = self.__dictionaries.getWordFromCurrentLanguage("simple"),
                                    bg=self.__colors.getColor("window"),
                                    fg=self.__colors.getColor("font"),
                                    variable = self.__spriteT, value = 1, command = self.__changeType
                                    )
        self.__radio1.pack(side=LEFT, anchor=E, fill=Y)

        self.__radio2 = Radiobutton(self.__spriteTypeL2, font = self.__normalFont,
                                    text = self.__dictionaries.getWordFromCurrentLanguage("double"),
                                    bg=self.__colors.getColor("window"),
                                    fg=self.__colors.getColor("font"),
                                    variable = self.__spriteT, value = 2, command = self.__changeType
                                    )
        self.__radio2.pack(side=LEFT, anchor=E, fill=Y)

        self.__radio3 = Radiobutton(self.__spriteTypeL3, font = self.__normalFont,
                                    text = self.__dictionaries.getWordFromCurrentLanguage("overlay"),
                                    bg=self.__colors.getColor("window"),
                                    fg=self.__colors.getColor("font"),
                                    variable = self.__spriteT, value = 3, command = self.__changeType
                                    )
        self.__radio3.pack(side=LEFT, anchor=E, fill=Y)

        self.__loading = Frame(self.__controlFrame, bg=self.__colors.getColor("window"),
                                  height=round(self.__sizes[1] // 32 * 3))
        self.__loading.config(width=999999)
        self.__loading.pack_propagate(False)
        self.__loading.pack(side=TOP, anchor=N, fill=X)

        from VisualLoaderFrame import VisualLoaderFrame

        self.__spriteLoader = VisualLoaderFrame(self.__loader, self.__loading, round(self.__sizes[1] // 28),
                                                self.__normalFont, self.__smallFont, None, "Brutal_Big_Sprite",
                                                "spriteName", self.checkIfValidFileName, round(self.__sizes[0] // 4),
                                                self.__openSprite, self.__saveSprite)

        self.__testing = Frame(self.__controlFrame, bg=self.__colors.getColor("window"),
                                  height=round(self.__sizes[1] // 32))
        self.__testing.config(width=999999)
        self.__testing.pack_propagate(False)
        self.__testing.pack(side=TOP, anchor=N, fill=X)

        from EmuTestFrame import EmuTestFrame

        self.__testWithEmulatorFrame = EmuTestFrame(self.__loader, self.__testing, round(self.__sizes[1] // 28),
                                                    self.__normalFont,  round(self.__sizes[0] // 4),
                                                    self.__loadTest, TOP, N)


        self.__setYIndexThings()
        self.__finished2 = True

    def __redrawCanvasClick(self, event):
        self.__redrawCanvas()

    def __clickedBox(self, w, h):
        self.__changed = True
        self.checkIfValidFileName(None)

        if self.__mode != "double":
           self.__canvasStartX = self.__canvas.winfo_width() // 2  - (4 * self.__width * w)
           self.__maxX         = self.__canvas.winfo_width()  - (8 * self.__width * w)
        else:
            self.__canvasStartX = self.__canvas.winfo_width() // 2 - (8 * self.__width * w)
            self.__maxX         = self.__canvas.winfo_width()  - (16 * self.__width * w)

        self.__canvasY = (self.__canvas.winfo_height()) // 2 - (((self.__h + self.__Y) * self.__lineHeight * h) // 2)


        if self.__mode == "double":
            colorMax  = 1
            numOfBits = 16
        elif self.__mode == "overlay":
            colorMax = 2
            numOfBits = 8
        else:
            colorMax = 1
            numOfBits = 8

        if  self.__play == False:
            self.__canvasX   = self.__canvasStartX
            self.__direction = 0
            self.__counter = 0
            self.__tempIndex = self.__frameNum
            self.__delay = 0

        else:

            if self.__speed == 0:
                self.__delay = round(16 / (self.__numOfFrames * 3))
            else:
                self.__delay = round(16 / self.__speed)

            if self.__counter < self.__delay:
                self.__counter += 1
            else:
                self.__counter = 0
                if self.__tempIndex < self.__numOfFrames - 1:
                    self.__tempIndex += 1
                else:
                    self.__tempIndex = 0

                if self.__moveHor.get() == 1:
                    if self.__direction == 0:
                        self.__canvasX -= 5
                        if self.__canvasX < 0:
                            self.__canvasX = 0
                            self.__direction = 1

                    else:
                        self.__canvasX += 5
                        if self.__canvasX > self.__maxX:
                            self.__canvasX = self.__maxX
                            self.__direction = 0
                else:
                    self.__canvasX = self.__canvasStartX

        if True:
            drawY = self.__canvasY
            for theY in range(0, self.__h):
                #for spriteNum in range(0, self.__numOfFrames):
                    self.__canvas.create_rectangle(0, drawY,
                                                   self.__canvas.winfo_width(),
                                                   drawY + self.__lineHeight * h,
                                                   outline="",
                                                   fill=self.__colorDict.getHEXValueFromTIA(
                                                       self.__dataLines[self.__tempIndex][2][theY + self.__Y][
                                                           "color"]
                                                   ))
                    # From 0/1 to 0
                    for colorNum in range(colorMax-1, -1, -1):
                        color = self.__dataLines[self.__tempIndex][colorNum][theY + self.__Y]["color"]

                        drawX = self.__canvasX

                        if self.__direction == 0:
                           fromX = 0
                           toX   = numOfBits
                           stepX = 1
                        else:
                           fromX = numOfBits - 1
                           toX   = -1
                           stepX = -1

                        for bitNum in range(fromX, toX, stepX):
                            if self.__dataLines[self.__tempIndex][colorNum][theY + self.__Y]["pixels"][bitNum] == "1":
                                self.__canvas.create_rectangle(drawX, drawY,
                                                               drawX + self.__width * w,
                                                               drawY + self.__lineHeight * h,
                                                               outline="",
                                                               fill=self.__colorDict.getHEXValueFromTIA(color))
                            drawX += self.__width * w
                    drawY += self.__lineHeight * h

    def incYIndex(self):
        self.__Y += 1
        self.__YNum.set(str(self.__Y))
        self.__setYIndexThings()
        self.__reDesign()

    def decYIndex(self):
        self.__Y -= 1
        self.__YNum.set(str(self.__Y))
        self.__setYIndexThings()
        self.__reDesign()

    def __setYByEntry(self, event):
        num = self.__checkNumeric(self.__YNum.get())
        if num == False:
           self.__YNumEntry.config(bg = self.__colors.getColor("boxBackUnSaved"),
                                    fg = self.__colors.getColor("boxFontUnSaved"))
        else:
            self.__YNumEntry.config(bg=self.__colors.getColor("boxBackNormal"),
                                     fg=self.__colors.getColor("boxFontNormal"))

            self.__setYIndexThings()
            self.__reDesign()


    def __setYIndexThings(self):
        if self.__finished == False:
           self.__Y = 0
        else:
            yMax = self.__h-(len(self.__buttons)-1)
            if yMax < 0:
               yMax = 0

            try:
                self.__Y = int(self.__YNum.get())
            except:
                pass

            if self.__Y < 0: self.__Y = 0
            elif self.__Y > yMax : self.__Y = yMax

            self.__YNum.set(str(self.__Y))

            if yMax == 0:
                self.__YNumEntry.config(state = DISABLED)
            else:
                self.__YNumEntry.config(state=NORMAL)

            if self.__Y == 0:
               self.__backYButton.config(state = DISABLED)
            else:
                self.__backYButton.config(state=NORMAL)

            if self.__Y == yMax:
                self.__forYButton.config(state=DISABLED)
            else:
                self.__forYButton.config(state=NORMAL)

    def __loadTest(self):
        if self.__finished == True and self.__finished2 == True:
            test = Thread(target=self.__testThread)
            test.daemon = True
            test.start()


    def __testThread(self):
        Compiler(self.__loader, self.__loader.virtualMemory.kernel, "testBigSprite",
                              [self.__dataLines, self.__lineHeight, self.__h, self.__activeMode,
                               self.__numOfFrames, "NTSC", "Test_BigSprite", self.__testColorSetter.getValue(),
                               ["Tile1_1", "Tile1_3", "Tile1_5"]])

    def checkIfValidFileName(self, event):
        try:
            name = str(event.widget).split(".")[-1]
        except:
            name = "spriteName"

        try:
            if name == "spriteName":
                widget = self.__spriteLoader.getEntry()
                value = self.__spriteLoader.getValue()

            if self.__loader.io.checkIfValidFileName(value) and (" " not in value):
                widget.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                          fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                          )
                if self.__changed == True and self.__finished == True:
                    self.__spriteLoader.enableSave()
            else:
                widget.config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                                          fg=self.__loader.colorPalettes.getColor("boxFontUnSaved"),
                                          )
                self.__spriteLoader.disableSave()
        except:
            pass


    def __openSprite(self):
        compatibles = {
            "common": ["common"]

        }

        if self.__finished == False or self.__finished2 == False:
            return

        if self.__finished == True:
            if self.changed == True:
                answer = self.__fileDialogs.askYesNoCancel("notSavedFile", "notSavedFileMessage")
                if answer == "Yes":
                    self.__saveSprite()
                elif answer == "Cancel":
                    self.__topLevelWindow.deiconify()
                    self.__topLevelWindow.focus()
                    return
            fpath = self.__fileDialogs.askForFileName("openFile", False, ["a26", "*"],
                                                      self.__loader.mainWindow.projectPath + "bigSprites/")

            if fpath == "":
                return

        #if True:
        try:
            file = open(fpath, "r")
            data = file.readlines()
            file.close()

            if data[0].replace("\n", "").replace("\r", "") not in compatibles[self.__loader.virtualMemory.kernel]:
                if self.__fileDialogs.askYesNoCancel("differentKernel", "differentKernelMessage") == "No":
                    self.__topLevelWindow.deiconify()
                    self.__topLevelWindow.focus()
                    return

            self.__heightSetter.setValue(data[1].replace("\n", "").replace("\r", ""))
            self.__h = int(data[1].replace("\n", "").replace("\r", ""))

            self.__frameNumSetter.setValue(data[2].replace("\n", "").replace("\r", ""))
            self.__numOfFrames = int(data[2].replace("\n", "").replace("\r", ""))
            self.__lineHeightSetter.setValue(data[3].replace("\n", "").replace("\r", ""))
            self.__mode = data[4].replace("\n", "").replace("\r", "")

            modes = ["simple", "double", "overlay"]

            for num in range(0, len(modes)):
                if modes[num] == self.__mode:
                    self.__spriteT.set(num + 1)
                    self.__activeMode == self.__mode

            try:
                self.__lineHeight = int(data[3].replace("\n", "").replace("\r", ""))
            except:
                self.__lineHeight = 1

            trueData = data[5:]

            spriteNum = 0
            colorNum  = 0
            height    = 0

            for lineNum in range(0, len(trueData)):

                lineData = trueData[lineNum].replace("\n", "").replace("\r", "").split(" ")
                line = self.__dataLines[spriteNum][colorNum][height]

                for pixelNum in range(0,16):
                    line["pixels"][pixelNum] = lineData[pixelNum]

                line["color"]  = lineData[16]
                if lineNum // 3 <= len(self.__entries):
                   self.__entryVals[height][colorNum] = lineData[16]
                   self.__entries[height][colorNum].setValue(lineData[16])


                height += 1
                if height == self.__h:
                   height = 0
                   colorNum += 1

                if colorNum == 3:
                   colorNum = 0
                   spriteNum += 1

            for height in range(0,256):
                for spriteNum in range(0, self.__frameNumMax):
                    self.__dataLines[spriteNum][0][height]["color"] = self.__dataLines[0][0][height]["color"]
                    self.__dataLines[spriteNum][1][height]["color"] = self.__dataLines[0][1][height]["color"]
                    self.__dataLines[spriteNum][2][height]["color"] = self.__dataLines[0][2][height]["color"]


            self.__changed = False
            self.__frameNum = 0
            self.__indexVal.set("0")
            self.__Y = 0
            self.__YNum.set("0")
            self.__spriteLoader.setValue(".".join(fpath.replace("\\", "/").split("/")[-1].split(".")[:-1]))

            #if True:
            try:
                for spriteNum in range(0, self.__frameNumMax):
                    if spriteNum != self.__frameNum:
                        continue
                    for theY in range(0, len(self.__buttons)):

                        if theY >= self.__h:
                            self.__entries[theY][0].getEntry().config(state=DISABLED)
                            self.__entries[theY][1].getEntry().config(state=DISABLED)
                            self.__entries[theY][2].getEntry().config(state=DISABLED)
                        else:
                            self.__entries[theY][0].getEntry().config(state=NORMAL)
                            self.__entries[theY][1].getEntry().config(state=NORMAL)
                            self.__entries[theY][2].getEntry().config(state=NORMAL)

                        for theX in range(0, 16):
                            if (self.__mode != "double" and theX > 7) or (theY >= self.__h):
                                self.__buttons[theY][theX].config(state=DISABLED,
                                                                  bg=self.__loader.colorPalettes.getColor(
                                                                      "fontDisabled"))
                            else:

                                self.__buttons[theY][theX].config(state=NORMAL)
                                self.__colorTile(theY, theX, spriteNum)


            except Exception as e:
                print(str(e))

            self.__soundPlayer.playSound("Success")
            self.__redrawCanvas()

        except Exception as e:

            self.__fileDialogs.displayError("unableToOpenFile", "unableToOpenFileMessage", None, str(e))

        self.__topLevelWindow.deiconify()
        self.__topLevelWindow.focus()


    def __saveSprite(self):
        if self.__finished == False or self.__finished2 == False:
            return

        name1 = self.__loader.mainWindow.projectPath + "bigSprites/"+self.__spriteLoader.getValue()+".a26"
        name2 = self.__loader.mainWindow.projectPath + "bigSprites/"+self.__spriteLoader.getValue()+".asm"

        import os
        if os.path.exists(name1):
            answer = self.__fileDialogs.askYesOrNo("fileExists", "overWrite")
            self.__topLevelWindow.deiconify()
            self.__topLevelWindow.focus()

            if answer == "No":
                return


        txt = (self.__loader.virtualMemory.kernel + "\n" +
               str(self.__h) + "\n" + str(self.__numOfFrames) + "\n" +
               str(self.__lineHeight) + "\n"+str(self.__activeMode) + "\n")

        for spriteNum in range(0, self.__numOfFrames):
            for colorNum in range(0,3):
                for height in range(0, self.__h):
                    line = self.__dataLines[spriteNum][colorNum][height]
                    txt += " ".join(line["pixels"]) + " " + line["color"] + "\n"

        file = open(name1, "w")
        file.write(txt)
        file.close()

        spriteData = Compiler(self.__loader, self.__loader.virtualMemory.kernel, "getBigSpriteASM",
                              [self.__dataLines, self.__lineHeight, self.__h, self.__activeMode,
                               self.__numOfFrames, "NTSC", "##NAME##"]).convertedSpite

        file = open(name2, "w")
        file.write(
            "* Height=" + str(self.__h) + "\n" + "* Frames=" +\
            str(self.__numOfFrames) + "\n" + "* LineHeight=" + str(self.__lineHeight) + "\n* Mode="+str(self.__activeMode + "\n" + spriteData)
        )
        file.close()

        self.__soundPlayer.playSound("Success")
        self.__changed = False


    def __changeType(self):
        modes = ["simple", "double", "overlay"]
        self.__mode = modes[self.__spriteT.get() - 1]

    def setValid(self, widget):
        widget.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                      fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                      )

    def setInValid(self, widget):
        widget.config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                      fg=self.__loader.colorPalettes.getColor("boxFontUnSaved"),
                      font=self.__smallFont
                      )

    def checkLineHeight(self, event):
        if self.__lineHeightSetter.getValue() == "":
            self.setInValid(self.__lineHeightSetter.getEntry())
        else:
            try:
                num = int(self.__lineHeightSetter.getValue())
                self.setValid(self.__lineHeightSetter.getEntry())

                if num > 255: num = 255
                elif num < 1: num = 1

                self.__lineHeight = num
                self.__lineHeightSetter.setValue(str(num))

            except:
                self.setInValid(self.__frameNumSetter.getEntry())

        self.__redrawCanvas()

    def checkHeightEntry(self, event):
        maxi = 256 // self.__numOfFrames

        if self.__heightSetter.getValue() == "":
            self.setInValid(self.__heightSetter.getEntry())
        else:
            try:
                num = int(self.__heightSetter.getValue())
                self.setValid(self.__heightSetter.getEntry())

                if num > maxi: num = maxi
                elif num < 1: num = 1

                self.__h = num
                self.__heightSetter.setValue(str(num))
                self.__setYIndexThings()
            except:
                self.setInValid(self.__heightSetter.getEntry())

        self.__reDesign()


    def checkFrameNumEntry(self, event):
        maxi = 256 // self.__h
        if maxi > 16: maxi = 16

        if maxi > self.__frameNumMax: maxi = self.__frameNumMax

        if self.__frameNumSetter.getValue() == "":
            self.setInValid(self.__frameNumSetter.getEntry())
        else:
            try:
                num = int(self.__frameNumSetter.getValue())
                self.setValid(self.__frameNumSetter.getEntry())
                if num < 1:
                   self.__frameNumSetter.setValue("1")
                   self.__numOfFrames = 1
                elif num > maxi:
                    self.__frameNumSetter.setValue(str(maxi))
                    self.__numOfFrames = maxi
                else:
                    self.__numOfFrames = num

            except:
                self.setInValid(self.__frameNumSetter.getEntry())

        self.__reDesign()


    def checkTestColorEntry(self, event):
        if self.__testColorSetter.getValue() == "":
            self.setInValid(self.__testColorSetter.getEntry())
        else:
            try:
                if len(self.__testColorSetter.getValue()) > 3:
                    self.__testColorSetter.setValue(self.__testColorSetter.getValue()[:3])

                self.__testColorSetter.setValue(self.__testColorSetter.getValue().upper())

                self.__colorDict.getHEXValueFromTIA(self.__testColorSetter.getValue().lower())
                self.setValid(self.__testColorSetter.getEntry())

                self.__backColor = self.__testColorSetter.getValue()

                self.__redrawCanvas()

            except:
                self.setInValid(self.__testColorSetter.getEntry())

        self.__redrawCanvas()

    def checkTesSpeedEntry(self, event):
        if self.__testSpeedSetter.getValue() == "":
            self.setInValid(self.__testSpeedSetter.getEntry())
        else:
            try:
                num = int(self.__testSpeedSetter.getValue())
                self.setValid(self.__testSpeedSetter.getEntry())

                if num > 16:
                   num = 16
                elif num < 0:
                   num = 0

                self.__testSpeedSetter.setValue(str(num))
                self.__speed = num

            except:
                self.setInValid(self.__testSpeedSetter.getEntry())

        self.__redrawCanvas()

    def checkWidthEntry(self, event):
        if self.__widthSetter.getValue() == "":
            self.setInValid(self.__widthSetter.getEntry())
        else:
            try:
                num = int(self.__widthSetter.getValue())
                self.setValid(self.__widthSetter.getEntry())

                if num > 4:
                   num = 4
                elif num == 3:
                   num = 4
                elif num < 1:
                   num = 1

                self.__widthSetter.setValue(str(num))
                self.__width = num

            except:
                self.setInValid(self.__widthSetter.getEntry())

        self.__redrawCanvas()

    def __redrawCanvas(self):
        self.__canvas.config(
            bg = self.__colorDict.getHEXValueFromTIA(self.__backColor)
        )
        self.__canvas.clipboard_clear()
        self.__canvas.delete("all")

        w = 1
        while w < 2:
            w = self.__canvas.winfo_width() // 64

        h = 1
        while h < 2:
            h = self.__canvas.winfo_width() // 128

        self.__clickedBox(w, h)


    def incIndex(self):
        if self.__frameNum < self.__numOfFrames-1:
           self.__frameNum += 1
        else:
           self.__frameNum = 0

        self.__indexVal.set(str(self.__frameNum))
        self.__reDesign()


    def decIndex(self):
        if self.__frameNum > 0:
            self.__frameNum -= 1
        else:
            self.__frameNum = self.__numOfFrames-1

        self.__indexVal.set(str(self.__frameNum))
        self.__reDesign()


    def __checkIndex(self, event):
        num = self.__checkNumeric(self.__indexVal.get())
        if num == False:
           self.__indexEntry.config(bg = self.__colors.getColor("boxBackUnSaved"),
                                    fg = self.__colors.getColor("boxFontUnSaved"))
        else:
            self.__indexEntry.config(bg=self.__colors.getColor("boxBackNormal"),
                                     fg=self.__colors.getColor("boxFontNormal"))
            if num > self.__numOfFrames-1:
               num = self.__numOfFrames-1
            elif num < 0:
               num = 0

            self.__indexVal.set(str(num))
            self.__frameNum = num

        self.__reDesign()


    def __checkNumeric(self, val):
        try:
            return(int(val))
        except:
            return(False)

    def __playing(self):
        if self.__play == True:
           self.__play = False
        else:
           self.__play = True

        self.__redrawCanvas()

    def __createData(self):
        colors = ["$0e", "$1e", "$00"]

        self.__dataLines = []

        for num in range(0,self.__frameNumMax):
            self.__dataLines.append([])
            for num2 in range(0,3):

                self.__dataLines[-1].append([])
                for num3 in range(0,256):
                    self.__dataLines[-1][-1].append({})
                    self.__dataLines[-1][-1][-1]["pixels"] = []
                    for num in range(0, 16):
                        self.__dataLines[-1][-1][-1]["pixels"].append("0")
                    self.__dataLines[-1][-1][-1]["color"] = colors[num2]


    def __createEditor(self):
        self.__buttons = []
        self.__entries = []
        self.__entryVals = []

        constant = 16
        s = int(((self.__sizes[0]*0.60) // 32 ))

        for theY in range(0, int(self.__sizes[1] // s)):
            self.__buttons.append([])
            self.__entries.append([])
            self.__entryVals.append(["$0e", "$1e", "$00"])
            self.__soundPlayer.playSound("Pong")

            rowF = Frame(self.__editorFrame,
                      bg=self.__loader.colorPalettes.getColor("window"),
                      width=self.__sizes[0] // 2, height = s
                      )
            rowF.pack_propagate(False)
            rowF.pack(side=TOP, anchor=N, fill=X)

            for theX in range(0, 16):
                name = str(theY) + "_" + str(theX)

                f = Frame(rowF, height = s, width = s,
                            bg = self.__loader.colorPalettes.getColor("boxBackNormal"))
                f.pack_propagate(False)
                f.pack(side=LEFT, anchor=E, fill=Y)

                b = Button(f, height =s, width = s, name = name,
                            bg = self.__loader.colorPalettes.getColor("boxBackNormal"),
                           activebackground = self.__loader.colorPalettes.getColor("highLight"),
                           relief=GROOVE, state = DISABLED
                           )
                b.pack_propagate(False)
                b.pack(side=LEFT, anchor=E, fill = BOTH)
                self.__buttons[-1].append(b)

                b.bind("<Button-1>", self.__clicked)
                b.bind("<Button-3>", self.__clicked)

                b.bind("<Enter>", self.__enter)

            f0 = Frame(rowF, height = s, width = 9999999,
                            bg = self.__loader.colorPalettes.getColor("window"))
            while f0.winfo_width() < 2:
                f0.pack_propagate(False)
                f0.pack(side=LEFT, anchor=E, fill=BOTH)

            f1 = Frame(f0, height = s, width = f0.winfo_width()//3,
                            bg = self.__loader.colorPalettes.getColor("window"))

            while f1.winfo_width() < 2:
                f1.config(width = f0.winfo_width()//3)
                f1.pack_propagate(False)
                f1.pack(side=LEFT, anchor=E, fill=Y)

            f2 = Frame(f0, height = s, width = f0.winfo_width()//3,
                            bg = self.__loader.colorPalettes.getColor("window"))

            while f2.winfo_width() < 2:
                f2.config(width = f0.winfo_width()//3)
                f2.pack_propagate(False)
                f2.pack(side=LEFT, anchor=E, fill=Y)


            f3 = Frame(f0, height = s, width = f0.winfo_width()//3,
                            bg = self.__loader.colorPalettes.getColor("window"))

            while f3.winfo_width() < 2:
                f3.config(width = f0.winfo_width()//3)
                f3.pack_propagate(False)
                f3.pack(side=LEFT, anchor=E, fill=BOTH)

            from HexEntry import HexEntry

            sp1Color = HexEntry(self.__loader, f1, self.__colors,
                       self.__colorDict, self.__smallFont, self.__entryVals[-1], 0, None, self.__setColorData)

            sp2Color = HexEntry(self.__loader, f2, self.__colors,
                       self.__colorDict, self.__smallFont, self.__entryVals[-1], 1, None, self.__setColorData)

            sp3Color = HexEntry(self.__loader, f3, self.__colors,
                       self.__colorDict, self.__smallFont, self.__entryVals[-1], 1, None, self.__setColorData)

            self.__entries[-1].append(sp1Color)
            self.__entries[-1].append(sp2Color)
            self.__entries[-1].append(sp3Color)

            sp1Color.setValue("$0e")
            sp2Color.setValue("$1e")
            sp3Color.setValue("$00")

            sp1Color.changeState(DISABLED)
            sp2Color.changeState(DISABLED)
            sp3Color.changeState(DISABLED)


    def __setColorData(self, event):
        breaking = False

        for yLine in range(0, len(self.__entries)):
            for colorNum in range(0, 3):
                if self.__entries[yLine][colorNum].getEntry() == event.widget:
                    for spriteNum in range(0, 16):
                        val =  self.__entries[yLine][colorNum].getValue()

                        self.__dataLines[spriteNum][colorNum][yLine + self.__Y]["color"] = val
                        self.__entries[yLine][colorNum].setValue(val)
                        breaking = True
                    if breaking == True: break
                if breaking == True: break
            if breaking == True: break

        self.__redrawCanvas()

    def __loop(self):
            try:
                if self.__mode != self.__activeMode and self.__finished == True:

                    self.__activeMode = self.__mode
                    self.__reDesign()

                try:
                    if self.__finished2 == True:
                        self.__playButton.config(state=NORMAL)
                        if self.__numOfFrames < 2:
                            # self.__playButton.config(state = DISABLED)
                            self.__indexEntry.config(state=DISABLED)
                            self.__forButton.config(state=DISABLED)
                            self.__backButton.config(state=DISABLED)
                        else:
                            self.__indexEntry.config(state=NORMAL)
                            self.__forButton.config(state=NORMAL)
                            self.__backButton.config(state=NORMAL)
                except:
                    pass

                if self.__play == True:
                   self.__playButton.config(image = self.__stopImage)
                   play = Thread(target=self.__redrawCanvas())
                   play.daemon = True
                   play.start()
                else:
                   self.__playButton.config(image = self.__playImage)
            except:
                pass

    def __reDesign(self):
        try:
            for theY in range(0, len(self.__buttons)):
                for theX in range(0, len(self.__buttons[theY])):
                    disable = False
                    if self.__mode != "double" and theX > 7:
                        disable = True
                    if theY >= (self.__Y + self.__h):
                        disable = True

                    if disable == True:
                        self.__buttons[theY][theX].config(state = DISABLED,
                                                          bg = self.__loader.colorPalettes.getColor("fontDisabled"))
                    else:
                        self.__buttons[theY][theX].config(state=NORMAL)


                if theY >= (self.__Y + self.__h):
                    self.__entries[theY][0].changeState(DISABLED)
                    self.__entries[theY][1].changeState(DISABLED)
                    self.__entries[theY][2].changeState(DISABLED)

                else:
                    self.__entries[theY][0].changeState(NORMAL)
                    self.__entries[theY][1].changeState(NORMAL)
                    self.__entries[theY][2].changeState(NORMAL)

                if self.__mode != "overlay":
                    self.__entries[theY][1].changeState(DISABLED)
                else:
                    if theY < (self.__Y + self.__h):
                        self.__entries[theY][1].changeState(NORMAL)


        except Exception as e:
            print(str(e))

        try:
            for spriteNum in range(0, self.__frameNumMax):
                if spriteNum != self.__frameNum:
                    continue
                for theY in range(self.__Y, self.__Y + len(self.__buttons)):
                    if theY >= self.__Y + self.__h:
                        break
                    for theX in range(0, 16):
                        if self.__mode != "double" and theX > 7:
                            break
                        self.__colorTile(theY, theX, spriteNum)

        except Exception as e:
            print(str(e))

        self.__redrawCanvas()

    def __colorTile(self, theY, theX, spriteNum):

        thisY = theY - self.__Y

        if self.__frameNum == 0:
            lastFrame = self.__numOfFrames - 1
        else:
            lastFrame = self.__frameNum - 1

        if (self.__dataLines[spriteNum][1][theY]["pixels"][theX] == "1" and
                self.__mode == "overlay"):
            self.__buttons[thisY][theX].config(
                bg=self.__loader.colorPalettes.getColor("boxBackUnSaved")
            )
        elif self.__dataLines[spriteNum][0][theY]["pixels"][theX] == "1":
            self.__buttons[thisY][theX].config(
                bg=self.__loader.colorPalettes.getColor("boxFontNormal")
            )
        elif self.__numOfFrames > 1 and \
                (self.__dataLines[lastFrame][1][theY]["pixels"][theX] == "1" or
                 self.__dataLines[lastFrame][0][theY]["pixels"][theX] == "1"):
            self.__buttons[thisY][theX].config(
                bg=self.__loader.colorPalettes.getColor("boxFontUnSaved")
            )
        else:
            self.__buttons[thisY][theX].config(
                bg=self.__loader.colorPalettes.getColor("boxBackNormal")
            )

    def drawMode(self, event):
        if self.__draw == 1:
            self.__draw = 0
        else:
            self.__draw = 1

    def shiftON(self, event):
        self.__ctrl = True

    def shiftOff(self, event):
        self.__ctrl = False

    def __clicked(self, event):
        button = 0
        if self.__finished == False:
            return

        try:
            button = int(str(event).split(" ")[3].split("=")[1])
        except:
            if self.__ctrl:
                button = 3
            else:
                button = 1

        if self.__ctrl == False and button == 3:
            return

        name = str(event.widget).split(".")[-1]

        Y = int(name.split("_")[0])
        X = int(name.split("_")[1])

        if Y < self.__h:
            if X < 8 or self.__mode == "double":
                self.__changeColor(X, Y, button)
                self.__colorTile(Y+self.__Y, X, self.__frameNum)

                self.__redrawCanvas()

    def __enter(self, event):
        if self.__draw:
            self.__clicked(event)

    def __changeColor(self, theX, theY, button):
        if self.__mode != "overlay":
            if self.__dataLines[self.__frameNum][0][theY + self.__Y]["pixels"][theX] == "0":
                self.__dataLines[self.__frameNum][0][theY + self.__Y]["pixels"][theX] = "1"
            else:
                self.__dataLines[self.__frameNum][0][theY + self.__Y]["pixels"][theX] = "0"
        else:
            if (self.__dataLines[self.__frameNum][0][theY + self.__Y]["pixels"][theX] == "0" and
                self.__dataLines[self.__frameNum][1][theY + self.__Y]["pixels"][theX] == "0"):
                self.__dataLines[self.__frameNum][0][theY + self.__Y]["pixels"][theX] = "1"
                self.__dataLines[self.__frameNum][1][theY + self.__Y]["pixels"][theX] = "0"
            elif (self.__dataLines[self.__frameNum][0][theY + self.__Y]["pixels"][theX] == "1" and
                  self.__dataLines[self.__frameNum][1][theY + self.__Y]["pixels"][theX] == "0"):
                self.__dataLines[self.__frameNum][0][theY + self.__Y]["pixels"][theX] = "0"
                self.__dataLines[self.__frameNum][1][theY + self.__Y]["pixels"][theX] = "1"
            elif (self.__dataLines[self.__frameNum][0][theY + self.__Y]["pixels"][theX] == "0" and
                  self.__dataLines[self.__frameNum][1][theY + self.__Y]["pixels"][theX] == "1"):
                self.__dataLines[self.__frameNum][0][theY + self.__Y]["pixels"][theX] = "0"
                self.__dataLines[self.__frameNum][1][theY + self.__Y]["pixels"][theX] = "0"

