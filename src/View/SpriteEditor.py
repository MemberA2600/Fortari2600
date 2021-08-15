from SubMenu import SubMenu
from SubMenuLabel import SubMenuLabel
from SubMenuFrame import SubMenuFrame
from tkinter import *
import re
from time import sleep
from threading import Thread

class SpriteEditor:

    def __init__(self, loader, mainWindow):
        self.__loader = loader
        self.__mainWindow = mainWindow

        self.__counter = 0
        self.__tempIndex = 0

        self.firstLoad = True
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

        self.__func = None
        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize*0.65), False, False, False)

        self.__bigFont = self.__fontManager.getFont(int(self.__fontSize*1.15), False, False, False)

        self.__moveDirection = [False,False]

        if self.__loader.virtualMemory.kernel == "common":
            self.__func = self.__addElementsCommon

        self.__ctrl = False
        self.__middle = False
        self.__draw = 0

        self.__sizes = {
            "common": [self.__screenSize[0] / 2, self.__screenSize[1]/1.10  - 40]
        }


        self.__window = SubMenu(self.__loader, "spriteEditor", self.__sizes["common"][0],
                                self.__sizes["common"][1], None, self.__func, 1)

        self.dead = True

    def checker(self):
        from time import sleep
        while(self.dead==False and self.__loader.mainWindow.dead == False):
            try:
                if self.__numOfFrames>1:
                    self.__backButton.config(state=NORMAL)
                    self.__forButton.config(state=NORMAL)
                    self.__indexEntry.config(state=NORMAL)
                else:
                    self.__backButton.config(state=DISABLED)
                    self.__forButton.config(state=DISABLED)
                    self.__indexEntry.config(state=DISABLED)
                    self.__isPlaying = False




                if self.__tileSetMode.get() == 1:
                    self.__playButton.config(state = DISABLED)
                    self.__horBox.config(state = DISABLED)
                    self.__verBox.config(state = DISABLED)
                    self.__p1Box.config(state = DISABLED)
                    self.__p1Mode.set(0)

                    self.__isPlaying = False

                    if self.__heightSetter.getValue() != "8":
                        self.__heightSetter.setValue("8")
                        self.__height = 8
                        self.generateTableCommon()
                else:
                    self.__playButton.config(state=NORMAL)
                    self.__horBox.config(state = NORMAL)
                    self.__verBox.config(state = NORMAL)
                    self.__p1Box.config(state = NORMAL)


                if self.__isPlaying:
                    self.__playButton.config(image=self.__stopImage)
                    play = Thread(target=self.redrawCanvas)
                    play.daemon=True
                    play.start()
                else:
                    self.__playButton.config(image=self.__playImage)

                if self.changed == False:
                    self.__spriteLoader.disableSave()

                else:
                    self.__spriteLoader.enableSave()

            except Exception as e:
                self.__loader.logger.errorLog(e)


            sleep(0.04)

    def shiftON(self, event):
        self.__ctrl = True

    def shiftOff(self, event):
        self.__ctrl = False

    def drawMode(self, event):
        if self.__draw == 1:
            self.__draw = 0
        else:
            self.__draw = 1

    def __addElementsCommon(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()

        self.__puff = 0.50
        self.__height = 8
        self.__heightMax=42

        self.__isPlaying = False
        self.__index = 0
        self.__numOfFrames = 1

        self.__topLevelWindow.bind("<KeyPress-Control_L>", self.shiftON)
        self.__topLevelWindow.bind("<KeyRelease-Control_L>", self.shiftOff)
        self.__topLevelWindow.bind("<KeyPress-Control_R>", self.shiftON)
        self.__topLevelWindow.bind("<KeyRelease-Control_R>", self.shiftOff)
        self.__topLevelWindow.bind("<Button-2>", self.drawMode)

        self.__mainFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=
                                     self.__topLevel.getTopLevelDimensions()[1])
        self.__mainFrame.pack_propagate(False)
        self.__mainFrame.pack(side=TOP, anchor=N, fill=BOTH)

        calc = round(self.__topLevel.getTopLevelDimensions()[0]/8*self.__puff)*4
        calc2 = round(self.__topLevel.getTopLevelDimensions()[0]/8*self.__puff)*2

        self.__theField = Frame(self.__mainFrame, bg=self.__loader.colorPalettes.getColor("window"))
        self.__theField.config(width=calc)
        self.__theField.pack_propagate(False)
        self.__theField.pack(side=LEFT, anchor=W, fill=Y)

        self.__intTheMiddle = Frame(self.__mainFrame, bg=self.__loader.colorPalettes.getColor("window"))
        self.__intTheMiddle.config(width=calc2)
        self.__intTheMiddle.pack_propagate(False)
        self.__intTheMiddle.pack(side=LEFT, anchor=W, fill=Y)

        self.__colorTable = []
        for num in range(0,self.__heightMax):
            self.__colorTable.append("$0E")

        self.__colorFrames = {}
        self.__colorEntries = {}
        self.__colorEntryVar = {}
        self.__buttons = {}

        self.__fieldOnTheRight = Frame(self.__mainFrame, width=self.__topLevel.getTopLevelDimensions()[0]-calc-calc2,
                                       bg=self.__loader.colorPalettes.getColor("window")
                                       )
        self.__fieldOnTheRight.pack(side=LEFT, anchor=E, fill=Y)

        self.__previewLabel = Label(self.__fieldOnTheRight,
                                    text=self.__dictionaries.getWordFromCurrentLanguage("preview"),
                                    font=self.__normalFont, fg=self.__colors.getColor("font"),
                                    bg=self.__colors.getColor("window")
                                    )

        self.__previewLabel.pack_propagate(False)
        self.__previewLabel.pack(side=TOP, anchor=N, fill=X)

        self.__canvas = Canvas(self.__fieldOnTheRight, bg="black", bd=0,
                               width=self.__topLevel.getTopLevelDimensions()[0] - calc,
                               height=round(self.__topLevel.getTopLevelDimensions()[1] / 5)
                               )

        self.__canvas.pack_propagate(False)
        self.__canvas.pack(side=TOP, anchor=N, fill=X)


        self.__thePlayer = Frame(self.__fieldOnTheRight, bg="red", height=round(self.__topLevel.getTopLevelDimensions()[1]/20))
        self.__thePlayer.config(width=self.__topLevel.getTopLevelDimensions()[0]-calc-calc2)
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
                                   width=round((self.__topLevel.getTopLevelDimensions()[0] - calc - calc2) / 4),
                                   state=DISABLED,
                                   command=self.decIndex)

        self.__indexEntryFrame = Frame(self.__thePlayer, bg=self.__loader.colorPalettes.getColor("window"),
                                       width=round((self.__topLevel.getTopLevelDimensions()[0] - calc - calc2) / 4))

        self.__indexEntry = Entry(self.__indexEntryFrame, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                   width=99,
                                   fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                   textvariable = self.__indexVal, name = "indexEntry",
                                   state=DISABLED, font=self.__bigFont, justify = CENTER,
                                   command=None)

        self.__forButton = Button(self.__thePlayer, bg=self.__loader.colorPalettes.getColor("window"),
                                   image=self.__forImage,
                                   width=round((self.__topLevel.getTopLevelDimensions()[0] - calc - calc2) / 4),
                                   state=DISABLED,
                                   command=self.incIndex)

        self.__playButton = Button(self.__thePlayer, bg=self.__loader.colorPalettes.getColor("window"),
                                   image=self.__playImage,
                                   width=round((self.__topLevel.getTopLevelDimensions()[0] - calc - calc2) / 4),
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


        self.__theController = Frame(self.__fieldOnTheRight, bg=self.__loader.colorPalettes.getColor("window"), height=round(self.__topLevel.getTopLevelDimensions()[1]/5*4))
        self.__theController.config(width=self.__topLevel.getTopLevelDimensions()[0]-calc-calc2)
        self.__theController.pack_propagate(False)
        self.__theController.pack(side=TOP, anchor=N, fill=X)

        ten = round(self.__topLevel.getTopLevelDimensions()[1] / 25)

        from VisualEditorFrameWithLabelAndEntry import VisualEditorFrameWithLabelAndEntry

        self.__widthSetter = VisualEditorFrameWithLabelAndEntry(
            self.__loader, "1", self.__theController, ten, "testWidth", self.__smallFont,
            self.checkWidthEntry, None)

        self.__moveHor = BooleanVar()
        self.__moveHor.set(1)
        self.__moveVer = BooleanVar()
        self.__moveVer.set(1)

        self.__testerBoxesFrame = Frame(self.__theController, height=ten, bg=self.__loader.colorPalettes.getColor("window"))
        self.__testerBoxesFrame.pack_propagate(False)
        self.__testerBoxesFrame.pack(side=TOP, anchor=N, fill=X)

        self.__horBox = Checkbutton(self.__testerBoxesFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                    fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                    font=self.__smallFont, text=self.__dictionaries.getWordFromCurrentLanguage("horMove"),
                                    variable=self.__moveHor
                                    )
        self.__horBox.pack(side=LEFT, anchor=N, fill=X)

        self.__verBox = Checkbutton(self.__testerBoxesFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                    fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                    font=self.__smallFont, text=self.__dictionaries.getWordFromCurrentLanguage("verMove"),
                                    variable=self.__moveVer
                                    )
        self.__verBox.pack(side=LEFT, anchor=N, fill=X)

        self.__tileSetMode = BooleanVar()
        self.__tileSetMode.set(0)

        self.__tileSetBoxFrame = Frame(self.__theController, height=ten, bg=self.__loader.colorPalettes.getColor("window"))
        self.__tileSetBoxFrame.pack_propagate(False)
        self.__tileSetBoxFrame.pack(side=TOP, anchor=N, fill=X)

        self.__tileBox = Checkbutton(self.__tileSetBoxFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                    fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                    font=self.__smallFont, text=self.__dictionaries.getWordFromCurrentLanguage("tileSetMode"),
                                    variable=self.__tileSetMode, command = self.generateTableCommon
                                    )
        self.__tileBox.pack(side=LEFT, anchor=N, fill=X)

        self.__p1Mode = BooleanVar()
        self.__p1Mode.set(0)

        self.__p1Box = Checkbutton(self.__tileSetBoxFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                    fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                    font=self.__smallFont, text=self.__dictionaries.getWordFromCurrentLanguage("testAsP1"),
                                    variable=self.__p1Mode, command = self.generateTableCommon
                                    )
        self.__p1Box.pack(side=LEFT, anchor=N, fill=X)

        self.__testColorSetter = VisualEditorFrameWithLabelAndEntry(
            self.__loader, "", self.__theController, ten, "testColor", self.__smallFont,
            self.checkColorEntry, None)

        self.__testSpeedSetter = VisualEditorFrameWithLabelAndEntry(
            self.__loader, "", self.__theController, ten, "testSpeed", self.__smallFont,
            self.checkSpeedEntry, None)

        self.__frameNumSetter = VisualEditorFrameWithLabelAndEntry(
            self.__loader, "1", self.__theController, ten, "frameNum", self.__smallFont,
            self.checkFrameNumEntry, self.checkFrameNumEntry2)

        self.__heightSetter = VisualEditorFrameWithLabelAndEntry(
            self.__loader, "8", self.__theController, ten, "height", self.__smallFont,
            self.checkHeightEntry, self.checkHeightEntry2)

        from VisualLoaderFrame import VisualLoaderFrame

        self.__spriteLoader = VisualLoaderFrame(self.__loader, self.__theController, ten, self.__normalFont, self.__smallFont,
                                                   None, "MasterPiece_Sprite", "spriteName", self.checkIfValidFileName,
                                                   round((self.__topLevel.getTopLevelDimensions()[0] - calc - calc2) / 2),
                                                   self.__openSprite, self.__saveSprite)


        self.__bigFatFrame = Frame(self.__theController, height=99999999, bg=self.__loader.colorPalettes.getColor("window"))
        self.__bigFatFrame.pack_propagate(False)
        self.__bigFatFrame.pack(side=TOP, anchor=N, fill=BOTH)

        self.__fatTitle = Label(self.__bigFatFrame,
                                    text=self.__dictionaries.getWordFromCurrentLanguage("testPlayfield"),
                                    font=self.__normalFont, fg=self.__colors.getColor("font"),
                                    bg=self.__colors.getColor("window")
                                    )

        self.__fatTitle.pack_propagate(False)
        self.__fatTitle.pack(side=TOP, anchor=N, fill=X)


        self.__refresher = Button(self.__bigFatFrame, font=self.__smallFont, width=99,
                                  text=self.__dictionaries.getWordFromCurrentLanguage("refreshList"),
                                  bg = self.__colors.getColor("window"), fg = self.__colors.getColor("font"),
                                  command = self.fillBoth)
        self.__refresher.pack_propagate(False)

        from EmuTestFrame import EmuTestFrame

        self.__testWithEmulatorFrame = EmuTestFrame(self.__loader, self.__bigFatFrame, ten, self.__normalFont,
                                                    round((self.__topLevel.getTopLevelDimensions()[
                                                               0] - calc - calc2) / 2), self.__loadTest, BOTTOM, S)

        self.__refresher.pack(side=BOTTOM, anchor = S, fill=X)

        self.__listBoxFrame = Frame(self.__bigFatFrame, height=99999999, bg=self.__loader.colorPalettes.getColor("window"),
                                    )
        self.__listBoxFrame.pack_propagate(False)
        self.__listBoxFrame.pack(side=TOP, anchor=N, fill=BOTH)

        from SpriteEditorListBox import SpriteEditorListBox

        self.__pfBox = SpriteEditorListBox(self.__loader, self.__listBoxFrame, self.__miniFont)
        self.__bgBox = SpriteEditorListBox(self.__loader, self.__listBoxFrame, self.__miniFont)

        self.__pfBox.getListBox().bind("<Double-Button-1>", self.checkIfOther1)
        self.__bgBox.getListBox().bind("<Double-Button-1>", self.checkIfOther2)

        self.fillBoth()

        #This is were the fun begins.
        ############################

        self.alreadyDone = False

        self.__frames = {}
        self.__table = {}
        row = []

        from copy import deepcopy

        row = ["0","0","0","0","0","0","0","0"]

        for index in range(0,16):
            self.__table[index] = []
            for num in range(0,self.__heightMax):
                self.__table[index].append(deepcopy(row))

        e = Thread(target=self.generateTableCommon)
        e.daemon = True
        e.start()

        t = Thread(target=self.checker)
        t.daemon = True
        t.start()

    def checkIfOther1(self, event):
        self.checkIfOther(self.__pfBox.getSelected(), self.__listItems2, self.__bgBox.getListBox())

    def checkIfOther2(self, event):
        self.checkIfOther(self.__bgBox.getSelected(), self.__listItems1, self.__pfBox.getListBox())

    def checkIfOther(self, toFind, listItems, listBox):
        for num in range(0, len(listItems)):
            if listItems[num] == toFind:
                listBox.selection_clear(0,END)
                listBox.selection_set(num)
                return


    def __loadTest(self):
        t = Thread(target=self.__testThread)
        t.daemon = True
        t.start()

    def __testThread(self):

        from Compiler import Compiler

        if self.__tileSetMode.get() == 1 :
            c = Compiler(self.__loader, self.__loader.virtualMemory.kernel, "tileSetTest",
                         [self.__table, self.__colorTable, self.__height, self.__numOfFrames, "NTSC",
                          self.__pfBox.getSelected(),
                          self.__bgBox.getSelected(),
                          self.__colorDict.getTIAfromRGB([self.getDom()[0], self.getDom()[2], self.getDom()[1]]),
                          0
                          ])

        else:
            c = Compiler(self.__loader, self.__loader.virtualMemory.kernel, "spriteTest",
                         [self.__table, self.__colorTable, self.__height, self.__numOfFrames, "NTSC",
                          self.__pfBox.getSelected(),
                          self.__bgBox.getSelected(),
                          self.__colorDict.getTIAfromRGB([self.getDom()[0], self.getDom()[2], self.getDom()[1]]),
                          self.__p1Mode.get()
                          ])

    def fillBoth(self):
        self.fillListBox1()
        self.fillListBox2()


    def fillListBox1(self):
        self.__listItems1 = [self.__dictionaries.getWordFromCurrentLanguage("blank")]
        self.fillListBox(self.__pfBox.getListBox(), "playfields/", self.__listItems1)

    def fillListBox2(self):
        self.__listItems2 = [self.__dictionaries.getWordFromCurrentLanguage("blank")]
        self.fillListBox(self.__bgBox.getListBox(), "backgrounds/", self.__listItems2)

    def fillListBox(self, listbox, folder, listitems):
        import os
        listbox.selection_clear(0, END)
        listbox.delete(0, END)
        for root, dirs, files in os.walk(self.__loader.mainWindow.projectPath + folder):
            for file in files:
                listitems.append(
                    ".".join(file.split(".")[:-1]).split("/")[-1]
                )
        for item in listitems:
            listbox.insert(END, item)
        listbox.selection_set(0)


    def __playing(self):
        if self.__isPlaying == False:
            self.__isPlaying = True
        else:
            self.__isPlaying = False
        self.redrawCanvas()

    def checkWidthEntry(self, event):
        if self.__widthSetter.getValue() == "":
            self.setValid(self.__widthSetter.getEntry())
        else:

            self.__widthSetter.setValue(self.__widthSetter.getValue().upper())

            if len(self.__widthSetter.getValue()) > 1:
                self.__widthSetter.setValue(self.__widthSetter.getValue()[:1])

            try:
                num = int(self.__widthSetter.getValue().lower())
                self.setValid(self.__widthSetter.getEntry())

                self.redrawCanvas()
                if num<1:
                    self.__widthSetter.setValue("1")
                elif num == 3 or num>4:
                    self.__widthSetter.setValue("4")


            except:
                self.setInValid(self.__widthSetter.getEntry())

                self.redrawCanvas()

    def setValid(self, widget):
        widget.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                      fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                      )

    def setInValid(self, widget):
        widget.config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                      fg=self.__loader.colorPalettes.getColor("boxFontUnSaved"),
                      font=self.__smallFont
                      )


    def checkColorEntry(self, event):
        if self.__testColorSetter.getValue() == "":
            self.setValid(self.__testColorSetter.getEntry())

        else:

            self.__testColorSetter.setValue(self.__testColorSetter.getValue().upper())

            if len(self.__testColorSetter.getValue()) > 3:
                self.__testColorSetter.setValue(self.__testColorSetter.getValue()[:3])

            try:
                self.__colorDict.getHEXValueFromTIA(self.__testColorSetter.getValue().lower())
                self.setValid(self.__testColorSetter.getEntry())

                self.redrawCanvas()

            except:
                self.setInValid(self.__testColorSetter.getEntry())

                self.redrawCanvas()


    def checkSpeedEntry(self, event):
        if self.__testSpeedSetter.getValue() == "":
            self.setValid(self.__testSpeedSetter.getEntry())

        else:

            while True:
                try:
                    if self.__testSpeedSetter.getValue() == "":
                        break
                    test = int(self.__testSpeedSetter.getValue())
                    break
                except:
                    self.__testSpeedSetter.setValue(self.__testSpeedSetter.getValue()[:-1])

            try:
                test = int(self.__testSpeedSetter.getValue())
                self.setValid(self.__testSpeedSetter.getEntry())

                if test > 16:
                    self.__testSpeedSetter.setValue("16")
                elif test<1:
                    self.__testSpeedSetter.setValue("1")


            except:
                self.setInValid(self.__testSpeedSetter.getEntry())

    def decIndex(self):
        if self.__index == 0:
            self.__index = self.__numOfFrames-1
        else:
            self.__index -= 1

        self.__indexVal.set(str(self.__index))
        self.generateTableCommon()

    def incIndex(self):
        if self.__index > self.__numOfFrames - 2:
            self.__index = 0
        else:
            self.__index += 1

        self.__indexVal.set(str(self.__index))
        self.generateTableCommon()

    def checkHeightEntry(self, event):
        num = 0

        try:
            num = int(self.__heightSetter.getValue())
        except:
            self.setInValid(self.__heightSetter.getEntry())

            return

        self.setValid(self.__heightSetter.getEntry())

    def checkHeightEntry2(self, event):
        try:
            num = int(self.__heightSetter.getValue())
            if num<1:
                self.__heightSetter.setValue("1")


            if num>self.__heightMax:
                self.__heightSetter.setValue(str(self.__heightMax))

            self.__height = int(self.__heightSetter.getValue())

        except:
            return
        self.checkIndexEntry2(event)
        self.checkFrameNumEntry2(event)


    def checkIndexEntry(self, event):
        num = 0

        try:
            num = int(self.__indexVal.get())
        except:
            self.setInValid(self.__indexEntry.getEntry())

            return

        self.setValid(self.__indexEntry.getEntry())

    def checkIndexEntry2(self, event):
        try:
            num = int(self.__indexVal.get())
            if num<0:
                self.__indexVal.set("0")

            if num>self.__numOfFrames:
                self.__indexVal.set(str(self.__numOfFrames-1))

        except Exception as e:
            pass

        self.__index = int(self.__indexVal.get())
        self.generateTableCommon()

    def checkFrameNumEntry(self, event):
        num = 0

        try:
            num = int(self.__indexVal.get())
        except:
            self.setInValid(self.__frameNumSetter.getEntry())

            return

        self.setValid(self.__frameNumSetter.getEntry())

    def checkFrameNumEntry2(self, event):
        max = 256 // self.__height
        if max>16:
            max = 16

        try:
            num = int(self.__frameNumSetter.getValue())
            if num<1:
                self.__frameNumSetter.setValue("1")

            if num>max:
                self.__frameNumSetter.setValue(str(max))

        except Exception as e:
            pass

        self.__numOfFrames = int(self.__frameNumSetter.getValue())
        self.checkIndexEntry2(event)

    def generateTableCommon(self):
        w = round(self.__topLevel.getTopLevelDimensions()[0]/16*self.__puff)
        h = round(self.__topLevel.getTopLevelDimensions()[1]/self.__heightMax)

        for Y in range(0, self.__heightMax):
            f1 = None
            f2 = None
            e1 = None
            e2 = None


            self.__topLevelWindow.bind("<KeyRelease>", self.checkEntry)

            if self.alreadyDone == False:
                self.__soundPlayer.playSound("Pong")
                f1 = Frame(self.__intTheMiddle, width=self.__intTheMiddle.winfo_width(), height=h, bg=self.__colors.getColor("boxBackNormal"))
                f1.pack_propagate(False)
                f1.place(x=0, y=h * (Y))

                self.__colorFrames[str(Y)] = f1
                eV1 = StringVar()
                e1 = Entry(f1, name=(str(Y)), textvariable = eV1, font=self.__smallFont, justify = "center")
                e1.pack(fill=BOTH)
                self.__colorEntries[str(Y)] = e1
                self.__colorEntryVar[str(Y)] = eV1

            else:
                f1 = self.__colorFrames[str(Y)]
                eV1 = self.__colorEntryVar[str(Y)]
                e1 = self.__colorEntries[str(Y)]

            e1.bind("<FocusOut>", self.forceReDraw)
            eV1.set(self.__colorTable[Y])
            self.colorEntry(e1, eV1.get())

            for X in range(0,8):
                f = None
                b = None

                if self.alreadyDone == False:
                    f = Frame(self.__theField, width=w, height=h, bg=self.__colors.getColor("boxBackNormal"))
                    f.pack_propagate(False)
                    f.place(x=w*X, y=h*(Y))
                    self.__motion = False
                    self.__frames[str(X) + "," + str(Y)] = f

                    b = Button(f, name=(str(X) + "," + str(Y)),
                               relief=GROOVE, activebackground=self.__colors.getColor("highLight"))

                    b.bind("<Button-1>", self.clickedCommon)
                    b.bind("<Button-3>", self.clickedCommon)

                    b.bind("<Enter>", self.enterCommon)
                    b.pack_propagate(False)
                    b.pack(fill=BOTH)

                    self.__buttons[str(X) + "," + str(Y)] = b
                else:
                    f = self.__frames[str(X) + "," + str(Y)]
                    b = self.__buttons[str(X) + "," + str(Y)]
                    #b.config(name=(str(X) + "," + str(Y)))

                e1.config(state=NORMAL)
                b.config(state=NORMAL)

                if Y>self.__height-1:
                    b.config(state=DISABLED, bg = self.__colors.getColor("fontDisabled"))
                    e1.config(state=DISABLED, bg = self.__colors.getColor("fontDisabled"), fg = self.__colors.getColor("fontDisabled"))


                elif self.__table[self.__index][Y][X] == "1":
                    b.config(bg=self.__colors.getColor("boxFontNormal"))
                    """
                    if self.__numOfFrames > 1:
                        if self.__index == 0:
                            if self.__table[self.__numOfFrames-1][Y][X] == "0":
                                b.config(bg=self.__colors.getColor("highLight"))
                        else:
                            if self.__table[self.__index-1][Y][X] == "0":
                                b.config(bg=self.__colors.getColor("highLight"))
                    """
                else:
                    b.config(bg=self.__colors.getColor("boxBackNormal"))
                    if self.__numOfFrames > 1:
                        if self.__index == 0:
                            if self.__table[self.__numOfFrames - 1][Y][X] == "1" and self.__tileSetMode.get() == 0:
                                b.config(bg=self.__colors.getColor("highLight"))
                        else:
                            if self.__table[self.__index - 1][Y][X] == "1" and self.__tileSetMode.get() == 0:
                                b.config(bg=self.__colors.getColor("highLight"))


        self.alreadyDone = True
        self.redrawCanvas()

    def forceReDraw(self, event):
        self.redrawCanvas()

    def getDom(self):
        dom = None
        try:
            dom = self.__colorDict.getRGBValueFromTIA(self.__testColorSetter.getValue().lower())

        except:
            temp = []
            for num in range(0, self.__height):
                temp.append(self.__colorDict.getRGBValueFromTIA(self.__colorTable[num]))

            dom = list(self.__colorDict.getDominantColor(temp))
            for num in range(0, 3):
                dom[num] = 255 - dom[num]
        return(dom)

    def redrawCanvas(self):

        nusiz = 0
        try:
            nusiz = int(self.__widthSetter.getValue())
        except:
            nusiz = 1

        if self.firstLoad == True:
            self.firstLoad = False
        else:
            self.changed = True

        if self.alreadyDone == True:
            w = round(self.__canvas.winfo_width() / 80)
            h = round(self.__canvas.winfo_height() / self.__heightMax)

            dom = self.getDom()

            self.__canvas.config(
                bg = self.__colorDict.getHEXValue(dom[0], dom[1], dom[2])
            )

            if self.__isPlaying == False:
                self.__moveDirection = [False, False]

                self.__counter = 0
                self.__Hor = 38
                self.__Ver = round(24-(self.__height))
                self.__mirrored = False
                self.__tempIndex = self.__index
            else:
                speed = 0
                if self.__testSpeedSetter.getValue() != "":
                    try:
                        speed = int(self.__testSpeedSetter.getValue())
                    except:
                        speed = 0

                if speed == 0:
                    self.__delay = round(16/(self.__numOfFrames*3))
                else:
                    self.__delay = round(16/speed)

                if self.__counter < self.__delay:
                    self.__counter+=1
                else:
                    self.__counter = 0
                    if self.__tempIndex<self.__numOfFrames-1:
                        self.__tempIndex+=1
                    else:
                        self.__tempIndex = 0

                    if self.__moveHor.get()==1:
                        if self.__moveDirection[0] == False:
                            if self.__Hor < 83 - (8*nusiz):
                                self.__Hor+=1
                            else:
                                self.__mirrored = True
                                self.__moveDirection[0] = True
                        else:
                            if self.__Hor > 0:
                                self.__Hor-=1
                            else:
                                self.__mirrored = False
                                self.__moveDirection[0] = False
                    else:
                        self.__Hor = 38

                    if self.__moveVer.get()==1:
                        if self.__moveDirection[1] == False:
                            if self.__Ver < 42 - self.__height:
                                self.__Ver+=1
                            else:
                                self.__moveDirection[1] = True
                        else:
                            if self.__Ver > 0:
                                self.__Ver-=1
                            else:
                                self.__moveDirection[1] = False
                    else:
                        self.__Ver = round(24 - (self.__height))



            self.__canvas.clipboard_clear()
            self.__canvas.delete("all")




            for Y in range(0, self.__height):
                # canvas.create_rectangle(x1, y1, x2, y2, **kwargs)
                #self.__canvas.create_rectangle(0, Y * h, self.__canvas.winfo_width(), (Y + 1) * h, outline="",
                #                               fill=self.__colorDict.getHEXValueFromTIA(self.__colorTable[Y]))
                if self.__mirrored == False:
                    for X in range(0, 8):
                        nusizNum = (nusiz - 1)*X

                        if self.__table[self.__tempIndex][Y][X] == "1":
                            self.__canvas.create_rectangle((X + self.__Hor + nusizNum) * w, (Y + self.__Ver) * h,
                                                           (X + self.__Hor + nusiz + nusizNum) * w, (Y + 1 + self.__Ver) * h, outline="",
                                                           fill=self.__colorDict.getHEXValueFromTIA(self.__colorTable[Y]))
                else:
                    for X in range(0, 8):
                        nusizNum = (nusiz - 1)*(X)

                        if self.__table[self.__tempIndex][Y][7-X] == "1":
                            self.__canvas.create_rectangle((X + self.__Hor + nusizNum) * w, (Y + self.__Ver) * h,
                                                           (X + self.__Hor + +nusiz + nusizNum) * w, (Y + 1 + self.__Ver) * h, outline="",
                                                           fill=self.__colorDict.getHEXValueFromTIA(self.__colorTable[Y]))

    def clickedCommon(self, event):
        button = 0
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
        X = int(name.split(",")[0])
        Y = int(name.split(",")[1])


        if Y < self.__height:
            self.changeColor(X, Y, button)


    def enterCommon(self, event):
        if self.__draw:
            self.clickedCommon(event)


    def changeColor(self, X, Y, button):
        color = ""

        if Y>self.__height-1:
            return

        b = self.__buttons[str(X) + "," + str(Y)]

        if self.__draw == True:
            if self.__ctrl == False:
                self.__table[self.__index][Y][X] = "1"
                color = self.__colors.getColor("boxFontNormal")
                """
                if self.__numOfFrames > 1:
                    if self.__index == 0:
                        if self.__table[self.__numOfFrames - 1][Y][X] == "0":
                            b.config(bg=self.__colors.getColor("highLight"))
                            color = self.__colors.getColor("highLight")

                    else:
                        if self.__table[self.__index - 1][Y][X] == "0":
                            b.config(bg=self.__colors.getColor("highLight"))
                            color = self.__colors.getColor("highLight")
                """

            else:
                self.__table[self.__index][Y][X] = "0"
                color = self.__colors.getColor("boxBackNormal")
                if self.__numOfFrames > 1:
                    if self.__index == 0:
                        if self.__table[self.__numOfFrames - 1][Y][X] == "1" and self.__tileSetMode.get() == 0:
                            b.config(bg=self.__colors.getColor("highLight"))
                            color = self.__colors.getColor("highLight")

                    else:
                        if self.__table[self.__index - 1][Y][X] == "1" and self.__tileSetMode.get() == 0:
                            b.config(bg=self.__colors.getColor("highLight"))
                            color = self.__colors.getColor("highLight")



        else:
            if self.__ctrl:
                if button == 1:
                    self.__table[self.__index][Y][X] = "1"
                    color = self.__colors.getColor("boxFontNormal")
                    """
                    if self.__numOfFrames > 1:
                        #print("1")
                        if self.__index == 0:
                            if self.__table[self.__numOfFrames - 1][Y][X] == "0":
                                b.config(bg=self.__colors.getColor("highLight"))
                                color = self.__colors.getColor("highLight")
                        else:
                            if self.__table[self.__index - 1][Y][X] == "0":
                                b.config(bg=self.__colors.getColor("highLight"))
                                color = self.__colors.getColor("highLight")
                    """
                else:
                    self.__table[self.__index][Y][X] = "0"
                    color = self.__colors.getColor("boxBackNormal")
                    if self.__numOfFrames > 1:
                        #print("2")
                        if self.__index == 0:
                            if self.__table[self.__numOfFrames - 1][Y][X] == "1" and self.__tileSetMode.get() == 0:
                                b.config(bg=self.__colors.getColor("highLight"))
                                color = self.__colors.getColor("highLight")

                        else:
                            if self.__table[self.__index - 1][Y][X] == "1" and self.__tileSetMode.get() == 0:
                                b.config(bg=self.__colors.getColor("highLight"))
                                color = self.__colors.getColor("highLight")

            else:
                if (self.__table[self.__index][Y][X] == "0"):
                    self.__table[self.__index][Y][X] = "1"
                    color = self.__colors.getColor("boxFontNormal")
                    """
                    if self.__numOfFrames > 1:
                        #print("3")
                        if self.__index == 0:
                            if self.__table[self.__numOfFrames - 1][Y][X] == "0":
                                b.config(bg=self.__colors.getColor("highLight"))
                                color = self.__colors.getColor("highLight")
                        else:
                            if self.__table[self.__index - 1][Y][X] == "0":
                                b.config(bg=self.__colors.getColor("highLight"))
                                color = self.__colors.getColor("highLight")
                    """
                else:
                    self.__table[self.__index][Y][X] = "0"
                    color = self.__colors.getColor("boxBackNormal")
                    if self.__numOfFrames > 1:
                        #print("4")
                        if self.__index == 0:
                            if self.__table[self.__numOfFrames - 1][Y][X] == "1" and self.__tileSetMode.get() == 0:
                                b.config(bg=self.__colors.getColor("highLight"))
                                color = self.__colors.getColor("highLight")
                        else:
                            if self.__table[self.__index - 1][Y][X] == "1" and self.__tileSetMode.get() == 0:
                                b.config(bg=self.__colors.getColor("highLight"))
                                color = self.__colors.getColor("highLight")


        self.__buttons[str(X) + "," + str(Y)].config(bg=color)
        self.redrawCanvas()

    def checkEntry(self, event):
        name = str(event.widget).split(".")[-1]
        if name == "nope":
            return

        Y = 0

        try:
            Y = int(name)
        except:
            return
        self.__colorEntryVar[str(Y)].set(self.__colorEntryVar[str(Y)].get().upper())

        if (len(self.__colorEntryVar[str(Y)].get())>3):
            self.__colorEntryVar[str(Y)].set(self.__colorEntryVar[str(Y)].get()[:3])
            return

        entry = event.widget
        if (len(self.__colorEntryVar[str(Y)].get())<3):
            entry.config(bg=self.__colors.getColor("boxBackUnSaved"), fg=self.__colors.getColor("boxFontUnSaved"))
            return


        try:
            num = int(self.__colorEntryVar[str(Y)].get().replace("$", "0x"), 16)
        except:
            entry.config(bg=self.__colors.getColor("boxBackUnSaved"), fg=self.__colors.getColor("boxFontUnSaved"))
            return


        num = int("0x"+self.__colorEntryVar[str(Y)].get()[2], 16)
        if (num%2 == 1):
            self.__colorEntryVar[str(Y)].set(self.__colorEntryVar[str(Y)].get()[:2]+hex(num-1).replace("0x","").upper())

        self.colorEntry(event.widget, self.__colorEntryVar[str(Y)].get())
        self.__colorTable[Y] = self.__colorEntryVar[str(Y)].get()


        self.generateTableCommon()

    def colorEntry(self, entry, value):
        color1 = self.__colorDict.getHEXValueFromTIA(value)

        num = int("0x"+value[2], 16)
        if num>8:
            num =value[:2]+hex(num-6).replace("0x","")
        else:
            num =value[:2]+hex(num+6).replace("0x","")

        color2 = self.__colorDict.getHEXValueFromTIA(num)
        entry.config(bg=color1, fg=color2)

    def focusIn(self, event):
        self.focused = event.widget
    def focusOut(self, event):
        self.focused = None

    def checkIfValidFileName(self, event):

        name = str(event.widget).split(".")[-1]

        if name == "spriteName":
            widget = self.__spriteLoader.getEntry()
            value = self.__spriteLoader.getValue()


        if self.__loader.io.checkIfValidFileName(value):
            widget.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                      fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                      )

        else:
            widget.config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                                      fg=self.__loader.colorPalettes.getColor("boxFontUnSaved"),
                                      )

    def __openSprite(self):
        import os

        if self.changed == True:
            answer = self.__fileDialogs.askYesNoCancel("notSavedFile", "notSavedFileMessage")
            if answer == "Yes":
                self.__saveSprite()
            elif answer == "Cancel":
                return

        fpath = self.__fileDialogs.askForFileName("openFile", False, ["a26", "*"],
                                                  self.__loader.mainWindow.projectPath + "sprites/")

        if fpath == "":
            return

        try:
            file = open(fpath, "r")
            data = file.readlines()
            file.close()

            compatibles = {
                "common": ["common"]

            }

            if data[0].replace("\n", "").replace("\r", "") not in compatibles[self.__loader.virtualMemory.kernel]:
                if self.__fileDialogs.askYesNoCancel("differentKernel", "differentKernelMessage") == "No":
                    return

            self.__spriteLoader.setValue(".".join(fpath.split("/")[-1].split(".")[:-1]))

            self.__heightSetter.setValue(data[1].replace("\n", "").replace("\r", ""))
            self.__height = int(self.__heightSetter.getValue())
            self.__indexVal.set("0")
            self.__index = 0

            self.__frameNumSetter.setValue(data[2].replace("\n", "").replace("\r", ""))
            self.__numOfFrames = int(self.__frameNumSetter.getValue())

            data.pop(0)
            data.pop(0)
            data.pop(0)

            for index in range(0, self.__numOfFrames):
                for Y in range(index*self.__height, self.__height+(index*self.__height)):
                    line = data[Y].replace("\n", "").replace("\r", "").split(" ")

                    relY= Y - (index*self.__height)

                    self.__colorTable[relY] = line[-1]
                    for X in range(0, 8):
                        self.__table[index][relY][X] = line[X]

            self.__soundPlayer.playSound("Success")
            self.changed = False

            self.__topLevelWindow.deiconify()
            self.__topLevelWindow.focus()
            self.alreadyDone = True
            self.firstLoad = True

            self.generateTableCommon()

        except Exception as e:
            self.__fileDialogs.displayError("unableToOpenFile", "unableToOpenFileMessage", None, str(e))
            self.__topLevelWindow.deiconify()
            self.__topLevelWindow.focus()

    def __saveSprite(self):
        import os

        fileName = self.__loader.mainWindow.projectPath + "sprites/"+self.__spriteLoader.getValue()+".a26"
        if os.path.exists(fileName):
            answer=self.__fileDialogs.askYesOrNo("fileExists", "overWrite")
            if answer == "No":
                return
        fileLines = []
        fileLines.append(self.__loader.virtualMemory.kernel)
        fileLines.append(str(self.__height))
        fileLines.append(str(self.__numOfFrames))

        for index in range(0, self.__numOfFrames):
            for Y in range(0, int(self.__height)):
                fileLines.append(" ".join(self.__table[index][Y])+" "+self.__colorTable[Y])

        file = open(fileName, "w")
        file.write("\n".join(fileLines))
        file.close()
        self.__soundPlayer.playSound("Success")
        self.changed=False

        self.__topLevelWindow.deiconify()
        self.__topLevelWindow.focus()