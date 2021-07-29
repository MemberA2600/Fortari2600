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

                if self.__isPlaying:
                    self.__playButton.config(image=self.__stopImage)
                    self.redrawCanvas()
                else:
                    self.__playButton.config(image=self.__playImage)



                if self.changed == False:
                    self.__saveButton.config(state=DISABLED)
                    self.__saveButtonBG.config(state=DISABLED)
                else:
                    self.__saveButton.config(state=NORMAL)
                    self.__saveButtonBG.config(state=NORMAL)
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


        self.__frameNumVal = StringVar()
        self.__frameNumVal.set("1")

        self.__frameNumSetter = Frame(self.__theController, height=ten, bg=self.__loader.colorPalettes.getColor("window"))
        self.__frameNumSetter.pack_propagate(False)

        self.__frameNumSetter.pack(side=TOP, anchor=N, fill=X)
        self.__frameNumLabel = Label(self.__frameNumSetter, text=self.__dictionaries.getWordFromCurrentLanguage("frameNum")+" ",
                                   font=self.__smallFont,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   fg=self.__loader.colorPalettes.getColor("font")
                                   )
        self.__frameNumLabel.pack(side=LEFT, anchor=W, fill=Y)

        self.__frameNumEntry = Entry(self.__frameNumSetter, textvariable=self.__frameNumVal, name="frameNumEntry")
        self.__frameNumEntry.config(width=99999, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                  fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                  font=self.__smallFont
                                  )

        self.__frameNumEntry.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__heightVal = StringVar()
        self.__heightVal.set("8")

        self.__heightSetter = Frame(self.__theController, height=ten, bg=self.__loader.colorPalettes.getColor("window"))
        self.__heightSetter.pack_propagate(False)

        self.__heightSetter.pack(side=TOP, anchor=N, fill=X)
        self.__heightLabel = Label(self.__heightSetter, text=self.__dictionaries.getWordFromCurrentLanguage("height")+" ",
                                   font=self.__smallFont,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   fg=self.__loader.colorPalettes.getColor("font")
                                   )
        self.__heightLabel.pack(side=LEFT, anchor=W, fill=Y)

        self.__heightEntry = Entry(self.__heightSetter, textvariable=self.__heightVal, name="heightEntry")
        self.__heightEntry.config(width=99999, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                  fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                  font=self.__smallFont
                                  )

        self.__testColorVar = StringVar()

        self.__testColorSetter = Frame(self.__theController, height=ten, bg=self.__loader.colorPalettes.getColor("window"))
        self.__testColorSetter.pack_propagate(False)
        self.__testColorSetter.pack(side=TOP, anchor=N, fill=X)

        self.__testColorLabel = Label(self.__testColorSetter, text=self.__dictionaries.getWordFromCurrentLanguage("testColor")+" ",
                                   font=self.__smallFont,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   fg=self.__loader.colorPalettes.getColor("font")
                                   )
        self.__testColorLabel.pack(side=LEFT, anchor=W, fill=Y)

        self.__testColorEntry = Entry(self.__testColorSetter, textvariable=self.__testColorVar, name="testColor")
        self.__testColorEntry.config(width=99999, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                  fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                  font=self.__smallFont
                                  )

        self.__testColorEntry.bind("<KeyRelease>", self.checkColorEntry)

        self.__testSpeedVar = StringVar()

        self.__testSpeedSetter = Frame(self.__theController, height=ten, bg=self.__loader.colorPalettes.getColor("window"))
        self.__testSpeedSetter.pack_propagate(False)
        self.__testSpeedSetter.pack(side=TOP, anchor=N, fill=X)

        self.__testSpeedLabel = Label(self.__testSpeedSetter, text=self.__dictionaries.getWordFromCurrentLanguage("testSpeed")+" ",
                                   font=self.__smallFont,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   fg=self.__loader.colorPalettes.getColor("font")
                                   )
        self.__testSpeedLabel.pack(side=LEFT, anchor=W, fill=Y)

        self.__testSpeedEntry = Entry(self.__testSpeedSetter, textvariable=self.__testSpeedVar, name="testSpeed")
        self.__testSpeedEntry.config(width=99999, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                  fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                  font=self.__smallFont
                                  )

        self.__testColorEntry.pack(side=LEFT, anchor=E, fill=BOTH)
        self.__testSpeedEntry.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__testSpeedEntry.bind("<KeyRelease>", self.checkSpeedEntry)

        self.__indexEntry.bind("<KeyRelease>", self.checkIndexEntry)
        self.__indexEntry.bind("<FocusOut>", self.checkIndexEntry2)

        self.__frameNumEntry.bind("<KeyRelease>", self.checkFrameNumEntry)
        self.__frameNumEntry.bind("<FocusOut>", self.checkFrameNumEntry2)

        self.__heightEntry.bind("<KeyRelease>", self.checkHeightEntry)
        self.__heightEntry.bind("<FocusOut>", self.checkHeightEntry2)
        self.__heightEntry.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__nusizVar = StringVar()
        self.__nusizVar.set("1")
        self.__moveHor = BooleanVar()
        self.__moveHor.set(1)
        self.__moveVer = BooleanVar()
        self.__moveVer.set(1)




        self.__spriteSetter = Frame(self.__theController, height=ten*2, bg=self.__loader.colorPalettes.getColor("window"))
        self.__spriteSetter.pack_propagate(False)
        self.__spriteSetter.pack(side=TOP, anchor=N, fill=X)

        self.__spriteNameFrame = Frame(self.__spriteSetter, height=ten, bg=self.__loader.colorPalettes.getColor("window"))
        self.__spriteNameFrame.pack_propagate(False)
        self.__spriteNameFrame.pack(side=TOP, anchor=N, fill=X)

        self.__spriteNameLabel = Label(self.__spriteNameFrame, text=self.__dictionaries.getWordFromCurrentLanguage("name"),
                                  font=self.__smallFont,
                                  bg=self.__loader.colorPalettes.getColor("window"),
                                  fg=self.__loader.colorPalettes.getColor("font")
                                  )
        self.__spriteNameLabel.pack(side=LEFT, anchor=W, fill=Y)

        self.__spriteName = StringVar()
        self.__spriteName.set("MasterPiece_Sprite")

        self.__spriteNameEntry = Entry(self.__spriteNameFrame, textvariable=self.__spriteName, name="spriteName")
        self.__spriteNameEntry.config(width=99999, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                 fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                 font=self.__smallFont
                                 )

        self.__spriteNameEntry.pack(side=LEFT, anchor=E, fill=BOTH)
        self.__spriteNameEntry.bind("<KeyRelease>", self.checkIfValidFileName)

        self.__spriteButtonsFrame = Frame(self.__spriteSetter, height=ten, bg=self.__loader.colorPalettes.getColor("window"))
        self.__spriteButtonsFrame.pack_propagate(False)
        self.__spriteButtonsFrame.pack(side=TOP, anchor=N, fill=X)

        self.__openPic = self.__loader.io.getImg("open", None)
        self.__savePic = self.__loader.io.getImg("save", None)

        self.__openButton = Button(self.__spriteButtonsFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                   image = self.__openPic, width=round((self.__topLevel.getTopLevelDimensions()[0] - calc - calc2) / 2),
                                   command = self.__openSprite)

        self.__openButton.pack(side = LEFT, anchor = W, fill=Y)

        self.__saveButton = Button(self.__spriteButtonsFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                   image = self.__savePic, width=round((self.__topLevel.getTopLevelDimensions()[0] - calc - calc2) / 2),
                                   state=DISABLED, command=self.__saveSprite)

        self.__saveButton.pack(side = LEFT, anchor = W, fill=Y)


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

    def __playing(self):
        if self.__isPlaying == False:
            self.__isPlaying = True
        else:
            self.__isPlaying = False
        self.redrawCanvas()

    def checkColorEntry(self, event):
        if self.__testColorVar.get() == "":
            self.__testColorEntry.config(
                bg = self.__loader.colorPalettes.getColor("boxBackNormal"),
                fg = self.__loader.colorPalettes.getColor("boxFontNormal"))
        else:

            self.__testColorVar.set(self.__testColorVar.get().upper())

            if len(self.__testColorVar.get()) > 3:
                self.__testColorVar.set(self.__testColorVar.get()[:3])

            try:
                self.__colorDict.getHEXValueFromTIA(self.__testColorVar.get().lower())
                self.__testColorEntry.config(
                    bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                    fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
                self.redrawCanvas()

            except:
                self.__testColorEntry.config(
                    bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                    fg=self.__loader.colorPalettes.getColor("boxFontUnSaved"))
                self.redrawCanvas()


    def checkSpeedEntry(self, event):
        if self.__testSpeedVar.get() == "":
            self.__testSpeedEntry.config(
                bg = self.__loader.colorPalettes.getColor("boxBackNormal"),
                fg = self.__loader.colorPalettes.getColor("boxFontNormal"))
        else:

            while True:
                try:
                    if self.__testSpeedVar.get() == "":
                        break
                    test = int(self.__testSpeedVar.get())
                    break
                except:
                    self.__testSpeedVar.set(self.__testSpeedVar.get()[:-1])

            try:
                test = int(self.__testSpeedVar.get())
                self.__testSpeedEntry.config(
                    bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                    fg=self.__loader.colorPalettes.getColor("boxFontNormal"))

                if test > 15:
                    self.__testSpeedVar.set("15")
                elif test<1:
                    self.__testSpeedVar.set("1")


            except:
                self.__testSpeedEntry.config(
                    bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                    fg=self.__loader.colorPalettes.getColor("boxFontUnSaved"))



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
            num = int(self.__heightVal.get())
        except:
            self.__heightEntry.config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                                      fg=self.__loader.colorPalettes.getColor("boxFontUnSaved"),
                                      font=self.__smallFont
                                      )
            return

        self.__heightEntry.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                              fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                              )

    def checkHeightEntry2(self, event):
        try:
            num = int(self.__heightVal.get())
            if num<1:
                self.__heightVal.set("1")


            if num>self.__heightMax:
                self.__heightVal.set(str(self.__heightMax))

            self.__height = int(self.__heightVal.get())

        except:
            return
        self.checkIndexEntry2(event)
        self.checkFrameNumEntry2(event)


    def checkIndexEntry(self, event):
        num = 0

        try:
            num = int(self.__indexVal.get())
        except:
            self.__indexEntry.config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                                      fg=self.__loader.colorPalettes.getColor("boxFontUnSaved"),
                                      font=self.__smallFont
                                      )
            return

        self.__indexEntry.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                              fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                              )

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
            self.__frameNumEntry.config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                                      fg=self.__loader.colorPalettes.getColor("boxFontUnSaved"),
                                      font=self.__smallFont
                                      )
            return

        self.__frameNumEntry.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                              fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                              )

    def checkFrameNumEntry2(self, event):
        max = 256 // self.__height
        if max>15:
            max = 15

        try:
            num = int(self.__frameNumVal.get())
            if num<1:
                self.__frameNumVal.set("1")

            if num>max:
                self.__frameNumVal.set(str(max))

        except Exception as e:
            pass

        self.__numOfFrames = int(self.__frameNumVal.get())
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

                if Y>self.__height-1:
                    b.config(state=DISABLED, bg = self.__colors.getColor("fontDisabled"))
                    e1.config(state=DISABLED, bg = self.__colors.getColor("fontDisabled"), fg = self.__colors.getColor("fontDisabled"))


                elif self.__table[self.__index][Y][X] == "1":
                    b.config(bg=self.__colors.getColor("boxFontNormal"))
                    """
                    if self.__numOfFrames > 1:
                        if self.__index == 0:
                            if self.__table[self.__numOfFrames-1][Y][X] == "0":
                                b.config(bg=self.__colors.getColor("comment"))
                        else:
                            if self.__table[self.__index-1][Y][X] == "0":
                                b.config(bg=self.__colors.getColor("comment"))
                    """
                else:
                    b.config(bg=self.__colors.getColor("boxBackNormal"))
                    if self.__numOfFrames > 1:
                        if self.__index == 0:
                            if self.__table[self.__numOfFrames - 1][Y][X] == "1":
                                b.config(bg=self.__colors.getColor("fontDisabled"))
                        else:
                            if self.__table[self.__index - 1][Y][X] == "1":
                                b.config(bg=self.__colors.getColor("fontDisabled"))


        self.alreadyDone = True
        self.redrawCanvas()

    def redrawCanvas(self):

        nusiz = 0
        try:
            nusiz = int(self.__nusizVar.get())
        except:
            nusiz = 1

        if self.firstLoad == True:
            self.firstLoad = False
        else:
            self.changed = True

        if self.alreadyDone == True:
            w = round(self.__canvas.winfo_width() / 80)
            h = round(self.__canvas.winfo_height() / self.__heightMax)
            dom = None

            try:
                dom = self.__colorDict.getRGBValueFromTIA(self.__testColorVar.get().lower())

            except:
                temp = []
                for num in range(0, self.__height):
                    temp.append(self.__colorDict.getRGBValueFromTIA(self.__colorTable[num]))

                dom = list(self.__colorDict.getDominantColor(temp))
                for num in range(0,3):
                    dom[num] = 255-dom[num]

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
                if self.__testSpeedVar.get() != "":
                    try:
                        speed = int(self.__testSpeedVar.get())
                    except:
                        speed = 0

                if speed == 0:
                    self.__delay = round(7/self.__numOfFrames)
                else:
                    self.__delay = round(7/speed)

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
                            b.config(bg=self.__colors.getColor("comment"))
                            color = self.__colors.getColor("comment")

                    else:
                        if self.__table[self.__index - 1][Y][X] == "0":
                            b.config(bg=self.__colors.getColor("comment"))
                            color = self.__colors.getColor("comment")
                """

            else:
                self.__table[self.__index][Y][X] = "0"
                color = self.__colors.getColor("boxBackNormal")
                if self.__numOfFrames > 1:
                    if self.__index == 0:
                        if self.__table[self.__numOfFrames - 1][Y][X] == "1":
                            b.config(bg=self.__colors.getColor("fontDisabled"))
                            color = self.__colors.getColor("fontDisabled")

                    else:
                        if self.__table[self.__index - 1][Y][X] == "1":
                            b.config(bg=self.__colors.getColor("fontDisabled"))
                            color = self.__colors.getColor("fontDisabled")



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
                                b.config(bg=self.__colors.getColor("comment"))
                                color = self.__colors.getColor("comment")
                        else:
                            if self.__table[self.__index - 1][Y][X] == "0":
                                b.config(bg=self.__colors.getColor("comment"))
                                color = self.__colors.getColor("comment")
                    """
                else:
                    self.__table[self.__index][Y][X] = "0"
                    color = self.__colors.getColor("boxBackNormal")
                    if self.__numOfFrames > 1:
                        #print("2")
                        if self.__index == 0:
                            if self.__table[self.__numOfFrames - 1][Y][X] == "1":
                                b.config(bg=self.__colors.getColor("fontDisabled"))
                                color = self.__colors.getColor("fontDisabled")

                        else:
                            if self.__table[self.__index - 1][Y][X] == "1":
                                b.config(bg=self.__colors.getColor("fontDisabled"))
                                color = self.__colors.getColor("fontDisabled")

            else:
                if (self.__table[self.__index][Y][X] == "0"):
                    self.__table[self.__index][Y][X] = "1"
                    color = self.__colors.getColor("boxFontNormal")
                    """
                    if self.__numOfFrames > 1:
                        #print("3")
                        if self.__index == 0:
                            if self.__table[self.__numOfFrames - 1][Y][X] == "0":
                                b.config(bg=self.__colors.getColor("comment"))
                                color = self.__colors.getColor("comment")
                        else:
                            if self.__table[self.__index - 1][Y][X] == "0":
                                b.config(bg=self.__colors.getColor("comment"))
                                color = self.__colors.getColor("comment")
                    """
                else:
                    self.__table[self.__index][Y][X] = "0"
                    color = self.__colors.getColor("boxBackNormal")
                    if self.__numOfFrames > 1:
                        #print("4")
                        if self.__index == 0:
                            if self.__table[self.__numOfFrames - 1][Y][X] == "1":
                                b.config(bg=self.__colors.getColor("fontDisabled"))
                                color = self.__colors.getColor("fontDisabled")
                        else:
                            if self.__table[self.__index - 1][Y][X] == "1":
                                b.config(bg=self.__colors.getColor("fontDisabled"))
                                color = self.__colors.getColor("fontDisabled")


        self.__buttons[str(X) + "," + str(Y)].config(bg=color)
        self.redrawCanvas()

    def checkEntry(self, event):
        name = str(event.widget).split(".")[-1]
        if name in ["heightEntry", "indexEntry", "spriteName", "frameNumEntry", "testColor", "testSpeed"]:
            return

        Y = int(name)
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
            widget = self.__playfieldNameEntry
            value = self.__pfName


        if self.__loader.io.checkIfValidFileName(value.get()):
            widget.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                      fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                      )

        else:
            widget.config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                                      fg=self.__loader.colorPalettes.getColor("boxFontUnSaved"),
                                      font=self.__smallFont
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

            self.__spriteName.set(".".join(fpath.split(os.sep)[-1].split(".")[:-1]))

            self.__heightVal.set(data[1].replace("\n", "").replace("\r", ""))
            self.__height = int(self.__heightVal.get())
            self.__indexVal.set("0")
            self.__index = 0

            self.__frameNumVal.set(data[2].replace("\n", "").replace("\r", ""))
            self.__numOfFrames = int(self.__frameNumVal.get())

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

        fileName = self.__loader.mainWindow.projectPath + "sprites/"+self.__spriteName.get()+".a26"
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