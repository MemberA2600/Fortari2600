from PIL import Image as IMG, ImageTk
from copy import deepcopy
from tkinter import *
from SubMenu import SubMenu

class PictureToCode:

    def __init__(self, loader, kernel, mode, w, changed):
        if mode == "playfield":
            self.__w = 40

            if kernel=="common":
                self.__mirroring = [0,1,1]
                self.__h = 42
        elif mode == "64pxPicture":
            self.__w = 64

        self.__mode = mode

        self.__loader = loader
        self.__mainWindow = self.__loader.mainWindow
        self.dead = False
        self.doThings = False
        self.__ctrl = False

        self.__editPicture = False

        self.__loader.stopThreads.append(self)

        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs
        self.__fontManager = self.__loader.fontManager
        self.__fontSize = int(self.__screenSize[0] / 1300 * self.__screenSize[1] / 1050 * 14)
        self.__colors = self.__loader.colorPalettes
        self.__colorDict = self.__loader.colorDict

        self.__screenSize = self.__loader.screenSize


        formats = [
            "bmp", "dds", "eps", "gif", "dib", "ico", "jpg", "jpeg", "pcx", "png", "tga", "tiff", "pdf"
        ]

        self.answer = self.__fileDialogs.askForFileName("loadPicture",
                                                   False, [formats, "*"], self.__mainWindow.projectPath)
        if self.answer !="":
            image = IMG.open(self.answer, "r")
            if image.mode != "RGB":
                image = image.convert("RGB")

            self.__image = image

            self.__func = None
            self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
            self.__smallFont = self.__fontManager.getFont(int(self.__fontSize * 0.80), False, False, False)
            self.__smallFont2 = self.__fontManager.getFont(int(self.__fontSize * 0.65), False, False, False)
            self.__tinyFont = self.__fontManager.getFont(int(self.__fontSize * 0.45), False, False, False)


            if self.__mode == "playfield":
                self.__window = SubMenu(self.__loader, "loadPicture", self.__screenSize[0] / 1.5,
                                    self.__screenSize[1] / 4 - 45, None, self.__addElements, 2)
            else:
                self.__window = SubMenu(self.__loader, "loadPicture", self.__screenSize[0] / 1.5,
                                    self.__screenSize[1] / 3 - 45, None, self.__addElements, 2)

            self.dead = True

            # Window is dead.
            if self.doThings == True:
                self.generateImage(mode, image, None)

    def generateImage(self, mode, image, testing):
        width, height = image.size
        multi = self.__w / width
        h = round(image.height * multi)

        self.Y = h
        self.__multiH = 1
        if self.Y > 255:
            self.Y = 255
        elif self.__mode == "playfield":
            if self.Y < self.__h:
                self.__multiH = round(self.__h / h)

        w = self.__w
        imageSized = image.resize((w, h), IMG.ANTIALIAS)
        imgColorData = imageSized.load()

        imageClone = deepcopy(imageSized)

        from PIL import ImageOps

        if self.__mode == "playfield":
            if self.__invert.get():
                imageClone = ImageOps.invert(imageClone)

            if self.__right.get():
                imageClone = ImageOps.mirror(imageClone)

        if mode == "playfield":
            fn = lambda x: 255 if x > int(self.__tres.get()) else 0
            altImage = deepcopy(imageClone).convert('L').point(fn, mode='1')
        elif self.__mode == "64pxPicture":
            fn1 = lambda x: 255 if x > int(self.__tres.get()) else 0
            fn2 = lambda x: 255 if x > int(self.__tres.get()) + 128 else 0
            altImage1 = deepcopy(imageClone).convert('L').point(fn1, mode='1')
            altImage2 = deepcopy(imageClone).convert('L').point(fn2, mode='1')

            pixels1 = altImage1.load()
            pixels2 = altImage2.load()

            W, H = altImage1.size

            pixels = []

            for Y in range(0, H):
                for X in range(0, W):
                    value = (pixels1[X, Y] + pixels2[X, Y]) // 2
                    # pixels.append((value, value, value))
                    # data+=chr(value) + chr(value) + chr(value)
                    pixels.append(value)
                    pixels.append(value)
                    pixels.append(value)

            altImage = IMG.frombytes("RGB", (w, h), bytes(pixels))

        # GetColors
        imgPixelData = altImage.load()

        if mode == "playfield":
            self.pixels = []
            self.pfColors = []
            self.bgColors = []

            self.getColorData(w, h, imgColorData, imgPixelData)
            self.getPFData(w, h, imgPixelData)

        elif mode == "64pxPicture":
            self.generateASM(w, h, imgColorData, imgPixelData, testing)


    def __addElementsEditor(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()

        self.__topLevelWindow.bind("<KeyPress-Control_L>", self.ctrlON)
        self.__topLevelWindow.bind("<KeyRelease-Control_L>", self.ctrlOff)
        self.__topLevelWindow.bind("<KeyPress-Control_R>", self.ctrlON)
        self.__topLevelWindow.bind("<KeyRelease-Control_R>", self.ctrlOff)

        self.__canvasFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"),
                                    width=round(self.__topLevel.getTopLevelDimensions()[0]),
                                    height=round(self.__topLevel.getTopLevelDimensions()[1] / 100 * 30))


        self.__canvasFrame.pack_propagate(False)
        self.__canvasFrame.pack(side=TOP, anchor=N, fill=X)

        self.__editorFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"),
                                   width=round(self.__topLevel.getTopLevelDimensions()[0]),
                                   height=round(self.__topLevel.getTopLevelDimensions()[1] / 100 * 70))

        self.__editorFrame.pack_propagate(False)
        self.__editorFrame.pack(side=TOP, anchor=N, fill=X)


        self.__editorButtonsFrame = Frame(self.__editorFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                   width=round(self.__topLevel.getTopLevelDimensions()[0]*0.80),
                                   height=round(self.__topLevel.getTopLevelDimensions()[1] / 100 * 70))

        self.__editorButtonsFrame.pack_propagate(False)
        self.__editorButtonsFrame.pack(side=LEFT, anchor=W, fill=Y)

        self.__editorColorButtonsFrame = Frame(self.__editorFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                   width=round(self.__topLevel.getTopLevelDimensions()[0]*0.20),
                                   height=round(self.__topLevel.getTopLevelDimensions()[1] / 100 * 70))

        self.__editorColorButtonsFrame.pack_propagate(False)
        self.__editorColorButtonsFrame.pack(side=LEFT, anchor=W, fill=Y)

        self.__canvas = Canvas(self.__canvasFrame, bg="black", bd=0,
                               width=round(self.__topLevel.getTopLevelDimensions()[0]*0.80),
                               height=round(self.__topLevel.getTopLevelDimensions()[1] / 100 * 30)
                               )

        self.__canvas.pack_propagate(False)
        self.__canvas.pack(side=LEFT, anchor=W, fill=Y)

        self.__menuFrame = Frame(self.__canvasFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                   width=round(self.__topLevel.getTopLevelDimensions()[0]*0.20),
                                   height=round(self.__topLevel.getTopLevelDimensions()[1] / 100 * 30))

        self.__menuFrame.pack_propagate(False)
        self.__menuFrame.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__controllerFrame = Frame(self.__menuFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                   width=round(self.__topLevel.getTopLevelDimensions()[0]*0.20),
                                   height=round(self.__topLevel.getTopLevelDimensions()[1] / 100 * 4))

        self.__controllerFrame.pack_propagate(False)
        self.__controllerFrame.pack(side=TOP, anchor=N, fill=X)


        self.__subFrame1 = Frame(self.__controllerFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                   width=round((self.__topLevel.getTopLevelDimensions()[0] * 0.20)/3),
                                   height=round(self.__topLevel.getTopLevelDimensions()[1] / 100 * 4))

        self.__subFrame1.pack_propagate(False)
        self.__subFrame1.pack(side=LEFT, anchor=E)

        self.__subFrame2 = Frame(self.__controllerFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                   width=round((self.__topLevel.getTopLevelDimensions()[0] * 0.20)/3),
                                   height=round(self.__topLevel.getTopLevelDimensions()[1] / 100 * 4))

        self.__subFrame2.pack_propagate(False)
        self.__subFrame2.pack(side=LEFT, anchor=E)

        self.__subFrame3 = Frame(self.__controllerFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                   width=round((self.__topLevel.getTopLevelDimensions()[0] * 0.20)/3),
                                   height=round(self.__topLevel.getTopLevelDimensions()[1] / 100 * 4))

        self.__subFrame3.pack_propagate(False)
        self.__subFrame3.pack(side=LEFT, anchor=E)

        self.__button1 = Button(self.__subFrame1, bg=self.__loader.colorPalettes.getColor("window"),
                                font = self.__normalFont, text = "<<",
                                width=9999, height=9999, state = DISABLED, command = self.pozMinus
                                )

        self.__button1.pack_propagate(False)
        self.__button1.pack(side=LEFT, anchor = E, fill=BOTH)

        self.__yPoz = StringVar()
        self.__yPoz.set("0")

        self.__yEntry = Entry(self.__subFrame2,
              bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
              fg=self.__loader.colorPalettes.getColor("boxFontNormal"), justify="center",
              textvariable=self.__yPoz, width=99,
              font=self.__normalFont, state = DISABLED
              )

        self.__yEntry.bind("<KeyRelease>", self.checkYEntry)
        self.__yEntry.bind("<FocusOut>", self.checkYEntry)

        self.__yEntry.pack_propagate(False)
        self.__yEntry.pack(side=LEFT, fill=BOTH, anchor=CENTER)

        self.__button2 = Button(self.__subFrame3, bg=self.__loader.colorPalettes.getColor("window"),
                                font = self.__normalFont, text = ">>",
                                width=9999, height=9999, state = DISABLED, command = self.pozPlus
                                )

        self.__button2.pack_propagate(False)
        self.__button2.pack(side=LEFT, anchor = E, fill=BOTH)

        self.__previewButton = Button(self.__menuFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                   fg = self.__loader.colorPalettes.getColor("font"),
                                   font = self.__normalFont,
                                   text = self.__dictionaries.getWordFromCurrentLanguage("preview")[:-1],
                                   command = self.testingEditor
                                      )

        self.__previewButton.pack_propagate(False)
        self.__previewButton.pack(side=TOP, anchor=N, fill=X)

        self.__saveButton = Button(self.__menuFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                   fg = self.__loader.colorPalettes.getColor("font"),
                                   font = self.__normalFont,
                                   text = self.__dictionaries.getWordFromCurrentLanguage("ok"),
                                   command = self.setAndKill
                                      )

        self.__saveButton.pack_propagate(False)
        self.__saveButton.pack(side=TOP, anchor=N, fill=X)

        self.__cancelButton = Button(self.__menuFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                   fg = self.__loader.colorPalettes.getColor("font"),
                                   font = self.__normalFont,
                                   text = self.__dictionaries.getWordFromCurrentLanguage("cancel"),
                                   command = self.killMe
                                      )

        self.__cancelButton.pack_propagate(False)
        self.__cancelButton.pack(side=TOP, anchor=N, fill=X)

        self.generateEditorButtons()
        self.__redrawCanvas()

        if self.__dataForEditor["h"] > 24:
           self.__yEntry.config(state = NORMAL)
           from threading import Thread
           t = Thread(target=self.__stateButtons)
           t.daemon = True
           t.start()

    def __stateButtons(self):
        from time import sleep
        while self.dead == False:
            if self.__currentY > 0:
                self.__button1.config(state = NORMAL)
            else:
                self.__button1.config(state = DISABLED)

            if self.__currentY < self.__dataForEditor["h"]-24:
                self.__button2.config(state = NORMAL)
            else:
                self.__button2.config(state = DISABLED)

    def pozMinus(self):
        self.__changeState(self.__currentY-1)

    def pozPlus(self):
        self.__changeState(self.__currentY+1)

    def checkYEntry(self, event):
        num = 0

        while len(self.__yPoz.get()) > 3:
            self.__yPoz.set(self.__yPoz.get()[:-1])

        while True:
            try:
                if self.__yPoz.get() == "":
                    break
                num = int(self.__yPoz.get())
                break
            except:
                self.__yPoz.set(self.__yPoz.get()[:-1])

        if self.__yPoz.get() != "":
           if num > self.__dataForEditor["h"]-24:
              num = self.__dataForEditor["h"]-24
           elif num < 0:
               num = 0

           self.__changeState(num)

    def __changeState(self, val):
        self.__yPoz.set(str(val))
        self.__currentY = val

        for buttonName in self.__editorButtons:
            #print(buttonName)

            typ = buttonName.split("_")[0]
            X = int(buttonName.split("_")[1])
            Y = int(buttonName.split("_")[2])

            if self.__dataForEditor["lines"][Y+self.__currentY][typ]["pixels"][X] == "0":
                self.__editorButtons[buttonName].config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
            else:
                if typ == "playfield":
                    self.__editorButtons[buttonName].config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"))
                else:
                    self.__editorButtons[buttonName].config(bg=self.__loader.colorPalettes.getColor("font"))

        for entryName in self.__colorEntries:
            typ = entryName.split("_")[0]
            Y = int(entryName.split("_")[1])

            if typ == "background":
                self.__colorEntries[entryName].setValue(self.__dataForEditor["lines"][Y+self.__currentY]["background"])
            else:
                self.__colorEntries[entryName].setValue(self.__dataForEditor["lines"][Y+self.__currentY][typ]["color"])

        self.__redrawCanvas()

    def generateEditorButtons(self):
        self.__editorButtons = {}
        self.__colorEntries = {}

        self.__currentY = 0

        w = round((self.__topLevel.getTopLevelDimensions()[0]*0.80)/64)
        h = round(self.__topLevel.getTopLevelDimensions()[1] / 100 * 70 / 52)

        for theY in range(0, self.__dataForEditor["h"]):
            if self.__mirrorPF.get() == 1:
                self.__dataForEditor["lines"][theY]["playfield"]["pixels"] = \
                self.__dataForEditor["lines"][theY]["playfield"]["pixels"][::-1]

            if self.__invertPFBG.get() == 1:
               temp =  self.__dataForEditor["lines"][theY]["playfield"]["color"]
               self.__dataForEditor["lines"][theY]["playfield"]["color"] = self.__dataForEditor["lines"][theY]["background"]
               self.__dataForEditor["lines"][theY]["background"] = temp


        for theY in range(0, 24):
            self.__soundPlayer.playSound("Pong")

            for theX in range(0,8):
                frame = Frame(self.__editorButtonsFrame, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                        width=w*8, height=h*2)
                frame.pack_propagate(False)
                frame.place(x =  (theX*w*8), y = (theY*h*2))

                framePX1 = Frame(frame, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                 width=w, height=h)
                framePX1.pack_propagate(False)
                framePX1.place(x = 0, y = 0)

                framePX2 = Frame(frame, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                 width=w, height=h)
                framePX2.pack_propagate(False)
                framePX2.place(x = w, y = 0)

                framePX3 = Frame(frame, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                 width=w, height=h)
                framePX3.pack_propagate(False)
                framePX3.place(x = w*2, y = 0)

                framePX4 = Frame(frame, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                 width=w, height=h)
                framePX4.pack_propagate(False)
                framePX4.place(x = w*3, y = 0)

                framePX5 = Frame(frame, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                 width=w, height=h)
                framePX5.pack_propagate(False)
                framePX5.place(x = w*4, y = 0)

                framePX6 = Frame(frame, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                 width=w, height=h)
                framePX6.pack_propagate(False)
                framePX6.place(x = w*5, y = 0)

                framePX7 = Frame(frame, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                 width=w, height=h)
                framePX7.pack_propagate(False)
                framePX7.place(x = w*6, y = 0)

                framePX8 = Frame(frame, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                 width=w, height=h)
                framePX8.pack_propagate(False)
                framePX8.place(x = w*7, y = 0)

                framePF1 = Frame(frame, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                 width=w*8, height=h)
                framePF1.pack_propagate(False)
                framePF1.place(x = 0, y = h)

                buttonPX1 = Button(framePX1, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                   relief=GROOVE, activebackground=self.__colors.getColor("highLight"),
                                   name = "sprites_" + str((theX*8)) + "_" + str(theY))

                buttonPX2 = Button(framePX2, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                   relief=GROOVE, activebackground=self.__colors.getColor("highLight"),
                                   name = "sprites_" + str((theX*8)+1) + "_" + str(theY))

                buttonPX3 = Button(framePX3, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                   relief=GROOVE, activebackground=self.__colors.getColor("highLight"),
                                   name = "sprites_" + str((theX*8)+2) + "_" + str(theY))

                buttonPX4 = Button(framePX4, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                   relief=GROOVE, activebackground=self.__colors.getColor("highLight"),
                                   name = "sprites_" + str((theX*8)+3) + "_" + str(theY))

                buttonPX5 = Button(framePX5, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                   relief=GROOVE, activebackground=self.__colors.getColor("highLight"),
                                   name = "sprites_" + str((theX*8)+4) + "_" + str(theY))

                buttonPX6 = Button(framePX6, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                   relief=GROOVE, activebackground=self.__colors.getColor("highLight"),
                                   name = "sprites_" + str((theX*8)+5) + "_" + str(theY))

                buttonPX7 = Button(framePX7, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                   relief=GROOVE, activebackground=self.__colors.getColor("highLight"),
                                   name = "sprites_" + str((theX*8)+6) + "_" + str(theY))

                buttonPX8 = Button(framePX8, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                   relief=GROOVE, activebackground=self.__colors.getColor("highLight"),
                                   name = "sprites_" + str((theX*8)+7) + "_" + str(theY))

                buttonPF1 = Button(framePF1, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                   relief=GROOVE, activebackground=self.__colors.getColor("highLight"),
                                   name = "playfield_" + str((theX)) + "_" + str(theY))

                self.buttonSetter(buttonPX1, theY, (theX*8),   "sprites_" + str((theX*8))   + "_" + str(theY))
                self.buttonSetter(buttonPX2, theY, (theX*8)+1, "sprites_" + str((theX*8)+1) + "_" + str(theY))
                self.buttonSetter(buttonPX3, theY, (theX*8)+2, "sprites_" + str((theX*8)+2) + "_" + str(theY))
                self.buttonSetter(buttonPX4, theY, (theX*8)+3, "sprites_" + str((theX*8)+3) + "_" + str(theY))
                self.buttonSetter(buttonPX5, theY, (theX*8)+4, "sprites_" + str((theX*8)+4) + "_" + str(theY))
                self.buttonSetter(buttonPX6, theY, (theX*8)+5, "sprites_" + str((theX*8)+5) + "_" + str(theY))
                self.buttonSetter(buttonPX7, theY, (theX*8)+6, "sprites_" + str((theX*8)+6) + "_" + str(theY))
                self.buttonSetter(buttonPX8, theY, (theX*8)+7, "sprites_" + str((theX*8)+7) + "_" + str(theY))
                self.buttonSetter(buttonPF1, theY, (theX),     "playfield_" + str((theX))   + "_" + str(theY))

            from HexEntry import HexEntry

            colorFrame = Frame(self.__editorColorButtonsFrame,
                                   bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                   width=round(self.__topLevel.getTopLevelDimensions()[0]*0.20),
                                   height=h*2)

            colorFrame.pack_propagate(False)
            colorFrame.pack(side=TOP, fill=X)

            cfW = round((self.__topLevel.getTopLevelDimensions()[0] * 0.20) / 3)

            colorFrame1 = Frame(colorFrame,
                                bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                width=cfW, height=h*2)
            colorFrame1.pack_propagate(False)
            colorFrame1.pack(side=LEFT, fill=Y)

            colorFrame2 = Frame(colorFrame,
                                bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                width=cfW, height=h*2)
            colorFrame2.pack_propagate(False)
            colorFrame2.pack(side=LEFT, fill=Y)

            colorFrame3 = Frame(colorFrame,
                                bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                width=cfW, height=h*2)
            colorFrame3.pack_propagate(False)
            colorFrame3.pack(side=LEFT, fill=Y)

            colorEntry1 = HexEntry(self.__loader, colorFrame1, self.__colors, self.__colorDict, self.__smallFont2,
                                   None, None, None, self.hexFocusOut)
            colorEntry2 = HexEntry(self.__loader, colorFrame2, self.__colors, self.__colorDict, self.__smallFont2,
                                   None, None, None, self.hexFocusOut)
            colorEntry3 = HexEntry(self.__loader, colorFrame3, self.__colors, self.__colorDict, self.__smallFont2,
                                   None, None, None, self.hexFocusOut)

            colorEntry1.setValue(self.__dataForEditor["lines"][theY]["sprites"]["color"])
            colorEntry2.setValue(self.__dataForEditor["lines"][theY]["playfield"]["color"])
            colorEntry3.setValue(self.__dataForEditor["lines"][theY]["background"])

            self.colorEntrySetter(colorEntry1, "sprites", theY)
            self.colorEntrySetter(colorEntry2, "playfield", theY)
            self.colorEntrySetter(colorEntry3, "background", theY)

        self.__invertPFBG.set(0)
        self.__mirrorPF.set(0)
        self.__cutBG.set(0)

    def colorEntrySetter(self, entry, typ, Y):
        self.__colorEntries[typ+"_"+str(Y)] = entry
        if Y-1 > self.__dataForEditor["h"]:
            entry.changeState(DISABLED)


    def buttonSetter(self, button, Y, X, name):
        button.pack_propagate(False)
        button.pack(fill=BOTH)

        button.bind("<Button-1>", self.clicked)
        button.bind("<Button-3>", self.clicked)

        self.__editorButtons[name] = button

        if Y-1 > self.__dataForEditor["h"]:
            button.config(state=DISABLED)
            button.config(bg=self.__loader.colorPalettes.getColor("fontDisabled"))
        else:
            if ("playfield" in name):
                if self.__dataForEditor["lines"][Y+self.__currentY]["playfield"]["pixels"][X] == "1":
                    button.config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"))
            else:
                if self.__dataForEditor["lines"][Y+self.__currentY]["sprites"]["pixels"][X] == "1":
                    button.config(bg=self.__loader.colorPalettes.getColor("font"))

    def getButtonName(self, event, getXY):

        name = str(event.widget).split(".")[-1]

        if getXY == False:
            return(name)
        else:
            bType = name.split("_")[0]
            X = int(name.split("_")[1])
            Y = int(name.split("_")[2])

            return(name, bType, X, Y)

    def hexFocusOut(self, event):

        name = None
        widget = None

        for entryName in self.__colorEntries.keys():
            if self.__colorEntries[entryName].getEntry() == event.widget:
                widget = self.__colorEntries[entryName]
                name = entryName
                break

        typ = name.split("_")[0]
        Y = int(name.split("_")[1])

        if typ == "background":
            self.__dataForEditor["lines"][Y+self.__currentY][typ] = widget.getValue()
        else:
            self.__dataForEditor["lines"][Y+self.__currentY][typ]["color"] = widget.getValue()

        self.__redrawCanvas()

    def clicked(self, event):
        name, bType, X, Y = self.getButtonName(event, True)
        button = int(str(event).split(" ")[3].split("=")[1])

        if self.__ctrl == True:
           if button == 1:
               self.setPixel(Y, bType, X, 1, event.widget)
           else:
               self.setPixel(Y, bType, X, 0, event.widget)

        else:
            self.setPixel(Y, bType, X,
                          1-int(self.__dataForEditor["lines"][Y+self.__currentY][bType]["pixels"][X]), event.widget)

        self.__redrawCanvas()

    def __redrawCanvas(self):
        w = round((self.__topLevel.getTopLevelDimensions()[0]*0.8)/64)
        h = round((self.__topLevel.getTopLevelDimensions()[1] / 100 * 30)/24)

        self.__canvas.clipboard_clear()
        self.__canvas.delete("all")

        for Y in range(self.__currentY, self.__currentY+24, 1):
            drawY = Y - self.__currentY
            colorBG = self.__colorDict.getHEXValueFromTIA(self.__dataForEditor["lines"][Y]["background"])
            colorPF = self.__colorDict.getHEXValueFromTIA(self.__dataForEditor["lines"][Y]["playfield"]["color"])
            colorSprites = self.__colorDict.getHEXValueFromTIA(self.__dataForEditor["lines"][Y]["sprites"]["color"])

            self.__canvas.create_rectangle((0, drawY*h, w*64, (drawY+1)*h),  outline="", fill=colorBG)

            for X in range(0,16,1):
                if X < 8:
                    if self.__dataForEditor["lines"][Y]["playfield"]["pixels"][X] == "1":
                        self.__canvas.create_rectangle((X*w*4, drawY*h, (X+1)*w*4, (drawY+1)*h), outline = "", fill=colorPF)
                else:
                    if self.__dataForEditor["lines"][Y]["playfield"]["pixels"][15-X] == "1":
                        self.__canvas.create_rectangle((X*w*4, drawY*h, (X+1)*w*4, (drawY+1)*h), outline = "", fill=colorPF)

            for X in range(0,64,1):
                if self.__dataForEditor["lines"][Y]["sprites"]["pixels"][X] == "1":
                    self.__canvas.create_rectangle((X * w, drawY * h, (X + 1) * w, (drawY + 1) * h), outline="",
                                                   fill=colorSprites)




    def setPixel(self, Y, bType, X, value, button):
        if X == 0:
            self.__dataForEditor["lines"][Y+self.__currentY][bType]["pixels"] = \
            str(value) + self.__dataForEditor["lines"][Y+self.__currentY][bType]["pixels"][X+1:]
        elif X == len(self.__dataForEditor["lines"][Y+self.__currentY][bType]["pixels"]):
            self.__dataForEditor["lines"][Y+self.__currentY][bType]["pixels"] = \
            self.__dataForEditor["lines"][Y+self.__currentY][bType]["pixels"][:X] + str(value)
        else:
            self.__dataForEditor["lines"][Y+self.__currentY][bType]["pixels"] = \
            self.__dataForEditor["lines"][Y+self.__currentY][bType]["pixels"][:X] + \
            str(value) + self.__dataForEditor["lines"][Y+self.__currentY][bType]["pixels"][X+1:]

        if value == 0:
            button.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        else:
            if bType == "playfield":
                button.config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"))
            else:
                button.config(bg=self.__loader.colorPalettes.getColor("font"))


    def generateASM(self, w, h, imgColorData, imgPixelData, testing):
        #mergedImageData = {}
        mergedByLines = []

        for Y in range(0, h):
            tempLine = []
            """
            lineValues = {
                0: [], 127: [], 255: []
            }
            """
            for X in range(0, w):
                lineDict = {}
                lineDict["pixel"] = imgPixelData[X,Y]
                lineDict["color"] = imgColorData[X,Y]
                #mergedImageData[str(X)+","+str(Y)] = lineDict
                tempLine.append(lineDict)
                #lineValues[lineDict["pixel"][0]].append(lineDict["color"])

            lineStruct = self.decideLineColors(tempLine)
            mergedByLines.append(lineStruct)

        if self.__editPicture == True:
            self.dead = False
            self.doThings = False
            self.__dataForEditor = {
                "lines":  mergedByLines, "h": h}
            self.__window = SubMenu(self.__loader, "editPicture", self.__screenSize[0] / 1.5,
                                    self.__screenSize[1] / 1.35 - 25, None, self.__addElementsEditor, 2)
            self.dead = True


        if self.doThings == True or self.__editPicture == False:
            asm = self.getASM(mergedByLines, h)
            if testing == True:
                from threading import Thread
                t = Thread(target=self.compileThread, args=[asm, h])
                t.daemon=True
                t.start()
            else:
                file = open(self.__loader.mainWindow.projectPath+"/64px/"+self.__name+".asm", "w")
                file.write(asm)
                file.close()
                self.__loader.soundPlayer.playSound("Success")

    def testingEditor(self):
        from threading import Thread

        t = Thread(target=self.testingEditorThread)
        t.daemon = True
        t.start()

    def testingEditorThread(self):
        asm = self.getASM(self.__dataForEditor["lines"], self.__dataForEditor["h"])
        self.compileThread(asm, self.__dataForEditor["h"])


    def compileThread(self, asm, h):
        from Compiler import Compiler
        C = Compiler(self.__loader, "common", "test64px", [asm, h])

    def getASM(self, data, h):
        pic64px_Sprite = [
            "pic64px_00\n",
            "pic64px_01\n",
            "pic64px_02\n",
            "pic64px_03\n",
            "pic64px_04\n",
            "pic64px_05\n",
            "pic64px_06\n",
            "pic64px_07\n"
        ]
        pic64px_Color = "pic64px_Color\n"
        pic64px_PF = "pic64px_PF\n"
        pic64px_PFColor = "pic64px_PFColor\n"
        pic64px_BGColor = "pic64px_BGColor\n"

        #correctBG
        bgColors = {}
        #correctPF

        for Y in range(0, h):
            canCutBG = 0
            if self.__invertPFBG.get() == 1:
                bg = data[Y]["playfield"]["color"]
            else:
                bg = data[Y]["background"]
            bg = bg[1]

            if bg in bgColors.keys():
                bgColors[bg]+=1
            else:
                bgColors[bg]=1

            if self.__mirrorPF.get() == 1:
                pfData = data[Y]["playfield"]["pixels"][::-1]
            else:
                pfData = data[Y]["playfield"]["pixels"]

            pf = []
            for P in pfData:
                pf.append(P)

            spriteData = data[Y]["sprites"]["pixels"]
            for pixelNum in range(0,32,4):
                sprite1 = spriteData[pixelNum:(pixelNum+4)]
                sprite2 = spriteData[(63-pixelNum-4):(63-pixelNum)][::-1]

                if sprite1 == "1111" and sprite2 == "1111":
                    pf[pixelNum//4] = "0"
            data[Y]["playfield"]["pixels"]="".join(pf)

            lineOfPF = ""
            for P in pf:
                lineOfPF+=P*4

            lineOfPF += lineOfPF[::-1]


            for pixelNum in range(0,64):
                if spriteData[pixelNum]=="0" and lineOfPF[pixelNum]=="0":
                    canCutBG +=1

        sorted(bgColors, key=bgColors.get, reverse=True)

        bgMain = list(bgColors.keys())[0]

        for Y in range(0, h):
            Y = h-1-Y
            #print(data[Y])
            spriteData = data[Y]["sprites"]["pixels"]
            spriteColor = data[Y]["sprites"]["color"]
            pfData = data[Y]["playfield"]["pixels"]

            if self.__invertPFBG.get() == 1:
                if self.__reduceBG.get() == 1:
                    bg = "$"+bgMain+data[Y]["playfield"]["color"][2]
                else:
                    bg = data[Y]["playfield"]["color"]

                pfColors = data[Y]["background"]
            else:
                pfColors = data[Y]["playfield"]["color"]
                if self.__reduceBG.get() == 1:
                    bg = "$"+bgMain+data[Y]["background"][2]
                else:
                    bg = data[Y]["background"]


            for pixelNum in range(0,64,8):
                pic64px_Sprite[pixelNum//8] += ("\tBYTE\t#%"+
                                                spriteData[pixelNum:(pixelNum+8)]
                                                +"\n"
                                                )
            pic64px_PF += ("\tBYTE\t#%"+ pfData+"\n")

            pic64px_Color += ("\tBYTE\t#"+ spriteColor+"\n")
            pic64px_PFColor += ("\tBYTE\t#" + pfColors + "\n")

            if canCutBG<24 and self.__cutBG.get()==1:
                pic64px_BGColor += ("\tBYTE\t#"+self.__oneColor.get()+"\n")
            else:
                pic64px_BGColor += ("\tBYTE\t#" + bg + "\n")


        allData = [
            pic64px_Sprite[0], pic64px_Sprite[1], pic64px_Sprite[2], pic64px_Sprite[3], pic64px_Sprite[4],
            pic64px_Sprite[5], pic64px_Sprite[6], pic64px_Sprite[7], pic64px_Color, pic64px_PF,
            pic64px_PFColor, pic64px_BGColor
        ]


        final = "\npic64px_data\n\talign\t256\n"
        bytes = 0
        for data in allData:
            numOfBytes = data.count("BYTE")
            if (bytes+numOfBytes) > 255:
                final+="\n\talign\t256\n" + data[:-1]
                bytes = 0
            else:
                final+=data[:-1]

            bytes+=numOfBytes
            bytes%=256

            final+="\t; "+str(bytes)+"\n\n"

        #print(final)
        return(final)


    def decideLineColors(self, lineValues):
        sums = {
            0: { "colors": [], "pixels": "", "dominantColor": None, "domiTIA": None, "pfError": 0, "allSet": 0},
            127: { "colors": [], "pixels": "", "dominantColor": None, "domiTIA": None, "pfError": 0, "allSet": 0},
            255: {"colors": [], "pixels": "", "dominantColor": None, "domiTIA": None, "pfError": 0, "allSet": 0}
        }

        lineStructure = {
            "background": "",
            "playfield": {"pixels1": "", "color": "", "pixels2": "", "pixels": ""},
            "sprites": {"pixels": "", "color": ""}
        }

        assign = {
            "background": 0,
            "playfield": 0,
            "sprites": 0
        }

        for pixelData in lineValues:
            if pixelData["pixel"][0] == 0:
                sums[0]["pixels"] += "1"
                sums[127]["pixels"] += "0"
                sums[255]["pixels"] += "0"
                sums[0]["colors"].append(pixelData["color"])

            elif pixelData["pixel"][0] == 127:
                sums[0]["pixels"] += "0"
                sums[127]["pixels"] += "1"
                sums[255]["pixels"] += "0"
                sums[127]["colors"].append(pixelData["color"])

            else:
                sums[0]["pixels"] += "0"
                sums[127]["pixels"] += "0"
                sums[255]["pixels"] += "1"
                sums[255]["colors"].append(pixelData["color"])

        for item in [0, 127, 255]:
            sums[item]["dominantColor"] = self.__colorDict.getDominantColor(sums[item]["colors"])
            if sums[item]["dominantColor"] != None:
                try:
                    sums[item]["domiTIA"] = self.__colorDict.getClosestTIAColor(sums[item]["dominantColor"][0],
                                                                             sums[item]["dominantColor"][2],
                                                                             sums[item]["dominantColor"][1])
                except:
                    print(sums[item]["dominantColor"])


            if (sums[item]["domiTIA"]) == None:
                (sums[item]["domiTIA"]) = self.__oneColor.get()

            pfError = 0
            for X in range(0,64,4):
                D = sums[item]["pixels"]
                p1 = int(D[0])
                p2 = int(D[1])
                p3 = int(D[2])
                p4 = int(D[3])

                if (p1+p2+p3+p4 == 4) or (p1+p2+p3+p4 == 0):
                    continue
                elif (p1+p2+p3+p4 == 2):
                    pfError+=2
                else:
                    pfError+=1

                string1 = sums[item]["pixels"][:32]
                string2 = sums[item]["pixels"][32:][::-1]

                for charNum in range(0,32):
                    if string1[charNum] != string2[charNum]:
                        pfError+=1
                sums[item]["allSet"] += (p1+p2+p3+p4)

            sums[item]["pfError"] = pfError

        notUsed = [0, 127, 255]
        hasPF = True
        for key in notUsed:
            if ((sums[key]["pixels"] == "0"*64)
                or (sums[key]["pixels"] == "1"*64)) and hasPF == True:
                notUsed.remove(key)
                hasPF = False

                lineStructure["playfield"]["color"] = self.__oneColor.get()
                lineStructure["playfield"]["pixels1"] = "0"*32
                lineStructure["playfield"]["pixels2"] = "0"*32
                assign["playfield"] = key


        if hasPF == True:
            #playfield
            temp={}
            for item in notUsed:
                temp[item] = sums[item]["pfError"]
            sorted(temp, key=temp.get)
            if sums[notUsed[0]]["pfError"] == sums[notUsed[1]]["pfError"] and sums[notUsed[1]]["pfError"] == sums[notUsed[2]]["pfError"]:
                grrr = {}
                for item in notUsed:
                    grrr[item] = sums[item]["allSet"]
                    sorted(grrr, key=grrr.get, reverse=True)
                if grrr[list(grrr.keys())[0]] == grrr[list(grrr.keys())[1]]:
                    grrr = {}
                    for item in notUsed:
                        grrr[item] = int("0x"+sums[item]["domiTIA"][2], 16)
                        sorted(grrr, key=grrr.get)

                key = list(grrr.keys())[0]
            else:
                if sums[list(temp.keys())[0]]["pfError"] == sums[list(temp.keys())[1]]["pfError"]:
                    grrr = {}
                    grrr[list(temp.keys())[0]] = sums[list(temp.keys())[0]]["allSet"]
                    grrr[list(temp.keys())[1]] = sums[list(temp.keys())[1]]["allSet"]
                    if grrr[list(grrr.keys())[0]] == grrr[list(grrr.keys())[1]]:
                        grrr = {}
                        for item in notUsed:
                            grrr[item] = int("0x" + sums[item]["domiTIA"][2], 16)
                            sorted(grrr, key=grrr.get)

                    sorted(grrr, key=grrr.get, reverse=True)
                    key = list(grrr.keys())[0]
                else:
                    key = list(temp.keys())[0]

            notUsed.remove(key)

            lineStructure["playfield"]["color"] = sums[key]["domiTIA"]
            lineStructure["playfield"]["pixels1"] = sums[key]["pixels"][:32]+sums[key]["pixels"][:32][::-1]
            lineStructure["playfield"]["pixels2"] = sums[key]["pixels"][32:][::-1]+sums[key]["pixels"][32:]
            assign["playfield"] = key

        #background
        temp={}
        for item in notUsed:
            temp[item] = sums[item]["allSet"]
        sorted(temp, key=temp.get)
        notUsed.remove(list(temp.keys())[0])

        lineStructure["background"] = sums[list(temp.keys())[0]]["domiTIA"]
        assign["background"] = list(temp.keys())[0]

        #spite
        lineStructure["sprites"]["color"] = sums[notUsed[0]]["domiTIA"]
        lineStructure["sprites"]["pixels"] = sums[notUsed[0]]["pixels"]
        assign["sprites"] = notUsed[0]

        OK = [0,0]
        for pixelNum in range(0,64):
            if (sums[assign["background"]]["pixels"][pixelNum] == "1"
                    and lineStructure["playfield"]["pixels1"] == "0"
                    and lineStructure["sprites"]["pixels"] == "0"):
                OK[0]+=1
            elif (sums[assign["playfield"]]["pixels"][pixelNum] == "1"
                and lineStructure["playfield"]["pixels1"] == "1"
                  and lineStructure["sprites"]["pixels"] == "0"):
                OK[0]+=1
            elif (sums[assign["sprites"]]["pixels"][pixelNum] == "1"
                and lineStructure["sprites"]["pixels"] == "1"):
                OK[0] += 1

        for pixelNum in range(0,64):
            if (sums[assign["background"]]["pixels"][pixelNum] == "1"
                    and lineStructure["playfield"]["pixels2"] == "0"
                    and lineStructure["sprites"]["pixels"] == "0"):
                OK[1]+=1
            elif (sums[assign["playfield"]]["pixels"][pixelNum] == "1"
                and lineStructure["playfield"]["pixels2"] == "1"
                  and lineStructure["sprites"]["pixels"] == "0"):
                OK[1]+=1
            elif (sums[assign["sprites"]]["pixels"][pixelNum] == "1"
                and lineStructure["sprites"]["pixels"] == "1"):
                OK[1] += 1

        if OK[0] > OK[1]:
            lineStructure["playfield"]["pixels"] = lineStructure["playfield"]["pixels1"][::-1]
            newPF = ""
            newPF2 = ""

            for pixelNum in range(0,32,4):
                part1 = sums[assign["background"]]["pixels"][pixelNum:(pixelNum + 4)]
                part2 = sums[assign["background"]]["pixels"][(63 - pixelNum - 4):(63 - pixelNum)][::-1]

                pfPart = lineStructure["playfield"]["pixels"][pixelNum:(pixelNum + 4)]

                for pixelNum2 in range(0,4):
                    if part1[pixelNum2] == part2[pixelNum2] and part1[pixelNum2] == pfPart[pixelNum2]:
                        newPF+=part1[pixelNum2]
                    elif part1[pixelNum2] == part2[pixelNum2] and part1[pixelNum2] != pfPart[pixelNum2]:
                        newPF += part1[pixelNum2]
                    elif part1[pixelNum2] == pfPart[pixelNum2] and part1[pixelNum2] != pfPart[pixelNum2]:
                        newPF += pfPart[pixelNum2]
                    elif part1[pixelNum2] != pfPart[pixelNum2] and part1[pixelNum2] == pfPart[pixelNum2]:
                        newPF += pfPart[pixelNum2]
                    else:
                        newPF += pfPart[pixelNum2]


            for pixelNum in range(0,32,4):
                p1 = int(newPF[pixelNum])
                p2 = int(newPF[pixelNum + 1])
                p3 = int(newPF[pixelNum + 2])
                p4 = int(newPF[pixelNum + 3])

                if (p1+p2+p3+p4) > 1:
                    newPF2+="1"
                else:
                    newPF2+="0"

            lineStructure["playfield"]["pixels"] = newPF2


        else:
            lineStructure["playfield"]["pixels"] = lineStructure["playfield"]["pixels2"][::-1]
            newPF = ""
            newPF2 = ""

            for pixelNum in range(0, 32, 4):
                part1 = sums[assign["background"]]["pixels"][pixelNum:(pixelNum + 4)]
                part2 = sums[assign["background"]]["pixels"][(63 - pixelNum - 4):(63 - pixelNum)][::-1]

                pfPart = lineStructure["playfield"]["pixels"][pixelNum:(pixelNum + 4)]

                for pixelNum2 in range(0, 4):
                    if part1[pixelNum2] == part2[pixelNum2] and part1[pixelNum2] == pfPart[pixelNum2]:
                        newPF += part1[pixelNum2]
                    elif part1[pixelNum2] == part2[pixelNum2] and part1[pixelNum2] != pfPart[pixelNum2]:
                        newPF += part1[pixelNum2]
                    elif part1[pixelNum2] == pfPart[pixelNum2] and part1[pixelNum2] != pfPart[pixelNum2]:
                        newPF += pfPart[pixelNum2]
                    elif part1[pixelNum2] != pfPart[pixelNum2] and part1[pixelNum2] == pfPart[pixelNum2]:
                        newPF += pfPart[pixelNum2]
                    else:
                        newPF += pfPart[pixelNum2]

            for pixelNum in range(0,32,4):
                p1 = int(newPF[pixelNum])
                p2 = int(newPF[pixelNum + 1])
                p3 = int(newPF[pixelNum + 2])
                p4 = int(newPF[pixelNum + 3])

                if (p1+p2+p3+p4) > 1:
                    newPF2+="1"
                else:
                    newPF2+="0"

            lineStructure["playfield"]["pixels"] = newPF2

            while ((lineStructure["playfield"]["color"] == lineStructure["sprites"]["color"] and
                    lineStructure["sprites"]["color"] != self.__oneColor.get()) or
                   (lineStructure["playfield"]["color"] == lineStructure["background"] and lineStructure[
                       "background"] != self.__oneColor.get()) or
                   (lineStructure["sprites"]["color"] == lineStructure["background"] and lineStructure[
                       "background"] != self.__oneColor.get())):

                lineStructure["playfield"]["color"], lineStructure["sprites"]["color"] = self.colorNoEqual(
                    lineStructure["playfield"]["color"], lineStructure["sprites"]["color"],
                    assign["playfield"], assign["sprites"])

                lineStructure["playfield"]["color"], lineStructure["background"] = self.colorNoEqual(
                    lineStructure["playfield"]["color"], lineStructure["background"],
                    assign["playfield"], assign["background"])

                lineStructure["background"], lineStructure["sprites"]["color"] = self.colorNoEqual(
                    lineStructure["background"], lineStructure["sprites"]["color"],
                    assign["background"], assign["sprites"])

        return (lineStructure)

    def ctrlON(self, event):
        self.__ctrl = True

    def ctrlOff(self, event):
        self.__ctrl = False

    def colorNoEqual(self, color1, color2, assignVal1, assignVal2):
        while (
                color1 == color2 and color1 != self.__oneColor.get()
        ):

            currentVal1 = int("0x" + color1[2], 16)
            currentVal2 = int("0x" + color2[2], 16)

            if currentVal1 > 8:
                if assignVal1 > assignVal2:
                    currentVal2 -= 2
                else:
                    currentVal1 -= 2
            elif currentVal1 < 9:
                if assignVal1 > assignVal2:
                    currentVal1 += 2
                else:
                    currentVal2 += 2
            color1 = color1[:-1] + hex(currentVal1).replace("0x", "")
            color2 = color2[:-1] + hex(currentVal2).replace("0x", "")

        return (color1, color2)

    def getPFData(self, w, h, pixelData):
        for Y in range(0, h):
            row = []
            for X in range(0,40):
                if X < 20:
                    row.append(pixelData[X,Y]//255)
                elif X < 28:
                    if self.__mirroring[2] == 1:
                        row.append(pixelData[20-(X-19), Y] // 255)

                    else:
                        row.append(pixelData[X, Y] // 255)
                elif X < 36:
                    if self.__mirroring[1] == 1:
                        row.append(pixelData[20-(X-19), Y] // 255)

                    else:
                        row.append(pixelData[X, Y] // 255)
                else:
                    if self.__mirroring[0] == 1:
                        row.append(pixelData[20-(X-19), Y] // 255)

                    else:
                        row.append(pixelData[X, Y] // 255)

            for m in range(0, self.__multiH):
                self.pixels.append(deepcopy(row))


    def getColorData(self, w, h, colorData, pixelData):
        for Y in range(0, h):
            #sumPF = [0,0,0]
            #sumBG = [0,0,0]
            PF = [0,0,0]
            BG = [0,0,0]

            pfList = []
            bgList = []

            for X in range(0, w):
                if (pixelData[X,Y] == 255):
                    #for num in range(0,3):
                        #sumPF[num]+=colorData[X,Y][num]
                    try:
                        pfList.append((colorData[X,Y][0], colorData[X,Y][2], colorData[X,Y][1]))
                    except:
                        pfList.append((colorData[X,Y]))
                else:
                    #for num in range(0,3):
                        #sumBG[num]+=colorData[X,Y][num]
                    try:
                        bgList.append((colorData[X,Y][0], colorData[X,Y][2], colorData[X,Y][1]))
                    except:
                        bgList.append((colorData[X,Y]))


            """
            for num in range(0, 3):
                PF[num] = round(sumPF[num]/w)
                BG[num] = round(sumBG[num]/w)

            """
            PF = self.__colorDict.getDominantColor(pfList)
            BG = self.__colorDict.getDominantColor(bgList)



            for m in range(0, self.__multiH):
                if PF != None:
                    pfC = self.__colorDict.getClosestTIAColor(PF[0], PF[1], PF[2])
                else:
                    try:
                        pfC = self.bgColors[-1]
                    except:
                        pfC = self.__oneColor.get()

                pfNum = int(pfC.replace("$", "0x"), 16)


                if BG != None:
                    bgC = self.__colorDict.getClosestTIAColor(BG[0], BG[1], BG[2])
                else:
                    try:
                        bgC = self.pfColors[-1]
                    except:
                        bgC = self.__oneColor.get()

                bgNum = int(bgC.replace("$", "0x"), 16)


                if abs( pfNum - bgNum ) < 4:
                    if (int("0x"+bgC[2], 16))>8:
                        bgC = bgC[:2] + str(hex(int("0x"+bgC[2], 16)-4)).replace("0x", "")
                    else:
                        bgC = bgC[:2] + str(hex(int("0x"+bgC[2], 16)+4)).replace("0x", "")


                self.pfColors.append( bgC )
                self.bgColors.append( pfC )




    def __addElements(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()

        self.__imageFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"))
        self.__imageFrame.config(
            width=round(self.__topLevel.getTopLevelDimensions()[0] /3))
        self.__imageFrame.pack_propagate(False)
        self.__imageFrame.pack(side=LEFT, anchor=W, fill=Y)

        self.__tres=StringVar()

        if self.__mode == "64pxPicture":
            self.__tres.set("84")
        else:
            self.__tres.set("128")

        self.__controllerFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"))
        self.__controllerFrame.config(
            width=round(self.__topLevel.getTopLevelDimensions()[0] /3))
        self.__controllerFrame.pack_propagate(False)
        self.__controllerFrame.pack(side=LEFT, anchor=W, fill=Y)

        self.__titleLabel = Label(self.__controllerFrame, text=self.__dictionaries.getWordFromCurrentLanguage("thresholdSetter"),
                                  bg = self.__loader.colorPalettes.getColor("window"),
                                  fg = self.__loader.colorPalettes.getColor("font"), justify = "center",
                                  font=self.__normalFont
                                  )
        self.__titleLabel.pack(side=TOP, anchor=N, fill=X)

        self.__number = Entry(self.__controllerFrame, text=self.__dictionaries.getWordFromCurrentLanguage("thresholdSetter"),
                                  bg = self.__loader.colorPalettes.getColor("boxBackNormal"),
                                  fg = self.__loader.colorPalettes.getColor("boxFontNormal"), justify = "center",
                                  textvariable=self.__tres, width=999999999,
                                  font=self.__normalFont
                              )

        self.__number.bind("<KeyRelease>", self.__checkNumber)

        self.__number.pack(side=TOP, anchor=N, fill=X)
        self.__minus = self.__loader.io.getImg("negative", None)
        self.__plus = self.__loader.io.getImg("positive", None)


        if self.__mode == "playfield":
            self.__cBoxFrame = Frame(self.__controllerFrame, bg=self.__loader.colorPalettes.getColor("window"))
            self.__cBoxFrame.config(
                width=round(self.__topLevel.getTopLevelDimensions()[0] / 2),
                height=round(self.__topLevel.getTopLevelDimensions()[1] / 6))
            self.__cBoxFrame.pack_propagate(False)
            self.__cBoxFrame.pack(side=TOP, anchor=N, fill=BOTH)


            self.__invert = IntVar()
            self.__invert.set(0)

            self.__check = Checkbutton(self.__cBoxFrame, text=self.__dictionaries.getWordFromCurrentLanguage("invert"),
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       fg=self.__loader.colorPalettes.getColor("font"),
                                       font=self.__smallFont,
                                       variable=self.__invert, command=self.updateBlackAndWhite
                                       )
            self.__check.pack(side=LEFT, anchor=W, fill=X)

            self.__right = IntVar()
            self.__right.set(0)

            self.__rightB = Checkbutton(self.__cBoxFrame,
                                       text=self.__dictionaries.getWordFromCurrentLanguage("preferRight"),
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       fg=self.__loader.colorPalettes.getColor("font"),
                                       font=self.__smallFont,
                                       variable=self.__right, command=self.updateBlackAndWhite
                                       )
            self.__rightB.pack(side=RIGHT, anchor=E, fill=X)
        elif self.__mode == "64pxPicture":
            self.__cBoxFrame = Frame(self.__controllerFrame, bg=self.__loader.colorPalettes.getColor("window"))
            self.__cBoxFrame.config(
                width=round(self.__topLevel.getTopLevelDimensions()[0] / 2),
                height=round(self.__topLevel.getTopLevelDimensions()[1] / 12))
            self.__cBoxFrame.pack_propagate(False)
            self.__cBoxFrame.pack(side=TOP, anchor=N, fill=BOTH)

            self.__cBoxFrame2 = Frame(self.__controllerFrame, bg=self.__loader.colorPalettes.getColor("window"))
            self.__cBoxFrame2.config(
                width=round(self.__topLevel.getTopLevelDimensions()[0] / 2),
                height=round(self.__topLevel.getTopLevelDimensions()[1] / 12))
            self.__cBoxFrame2.pack_propagate(False)
            self.__cBoxFrame2.pack(side=TOP, anchor=N, fill=BOTH)

            self.__mirrorPF = IntVar()
            self.__mirrorPF.set(0)

            self.__mirrorPFCheck = Checkbutton(self.__cBoxFrame,
                                       text=self.__dictionaries.getWordFromCurrentLanguage("invertPF"),
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       fg=self.__loader.colorPalettes.getColor("font"),
                                       font=self.__smallFont2,
                                       variable=self.__mirrorPF
                                       )
            self.__mirrorPFCheck.pack(side=LEFT, anchor=E, fill=X)

            self.__invertPFBG = IntVar()
            self.__invertPFBG.set(0)

            self.__invertPFBGCheck = Checkbutton(self.__cBoxFrame,
                                       text=self.__dictionaries.getWordFromCurrentLanguage("invertColors"),
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       fg=self.__loader.colorPalettes.getColor("font"),
                                       font=self.__smallFont2,
                                       variable=self.__invertPFBG
                                       )
            self.__invertPFBGCheck.pack(side=RIGHT, anchor=E, fill=X)


            self.__reduceBG = IntVar()
            self.__reduceBG.set(0)
            """
            self.__reduceBGCheck = Checkbutton(self.__cBoxFrame2,
                                       text=self.__dictionaries.getWordFromCurrentLanguage("reduceBG"),
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       fg=self.__loader.colorPalettes.getColor("font"),
                                       font=self.__smallFont,
                                       variable=self.__reduceBG
                                       )
            self.__reduceBGCheck.pack(side=LEFT, anchor=E, fill=X)
            """

            self.__cutBG = IntVar()
            self.__cutBG.set(0)

            self.__cutBGCheck = Checkbutton(self.__cBoxFrame2,
                                       text=self.__dictionaries.getWordFromCurrentLanguage("oneColorBG"),
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       fg=self.__loader.colorPalettes.getColor("font"),
                                       font=self.__smallFont2,
                                       variable=self.__cutBG
                                       )
            self.__cutBGCheck.pack(side=LEFT, anchor=E, fill=X)


            self.__imgColor = self.__loader.io.getImg("picker", None)
            self.__oneColor = StringVar()
            self.__oneColor.set("$00")

            self.__oneColorEntry = Entry(self.__cBoxFrame2,
                  bg="#000000",
                  fg="#646464",
                  textvariable=self.__oneColor, width=3,
                  font=self.__smallFont
                  )

            self.__oneColorEntry.pack(side=LEFT, fill=Y)
            self.__oneColorEntry.bind("<KeyRelease>", self.__checkHEX)


            self.__colorButton = Button(
                self.__cBoxFrame2, width=9999999,
                bg="#000000",
                image = self.__imgColor,
                command = self.__getColor,
                )
            self.__colorButton.pack_propagate(False)
            self.__colorButton.pack(side=RIGHT, fill=BOTH)


            self.__EntryFrame = Frame(self.__controllerFrame, bg=self.__loader.colorPalettes.getColor("window"))
            self.__EntryFrame.config(
                width=round(self.__topLevel.getTopLevelDimensions()[0] / 2),
                height=round(self.__topLevel.getTopLevelDimensions()[1] / 8))
            self.__EntryFrame.pack_propagate(False)
            self.__EntryFrame.pack(side=TOP, anchor=N, fill=BOTH)

            self.__thisLabel = Label(self.__EntryFrame, text=self.__dictionaries.getWordFromCurrentLanguage("name"),
                                  bg = self.__loader.colorPalettes.getColor("window"),
                                  fg = self.__loader.colorPalettes.getColor("font"), justify = "center",
                                  font=self.__smallFont
                                  )
            self.__thisLabel.pack(side=LEFT, anchor=E, fill=Y)

            self.__thisFrame = Label(self.__EntryFrame,
                                  bg = self.__loader.colorPalettes.getColor("window"), width=99999999)
            self.__thisFrame.pack_propagate(False)
            self.__thisFrame.pack(side=LEFT, anchor=E, fill=BOTH)


            self.__thisVar = StringVar()
            self.__thisVar.set("Best_Picture_Ever")
            self.__thisEntry = Entry(self.__thisFrame,
                  bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                  fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                  textvariable=self.__thisVar, width=999999999,
                  font=self.__smallFont
                  )

            self.__thisEntry.pack(side=TOP, fill=BOTH)
            self.__thisEntry.bind("<KeyRelease>", self.__checkNumber)



        self.__buttonFrame = Frame(self.__controllerFrame, bg=self.__loader.colorPalettes.getColor("window"))
        if self.__mode == "64pxPicture":
            self.__buttonFrame.config(
            width=round(self.__topLevel.getTopLevelDimensions()[0] / 2), height=round(self.__topLevel.getTopLevelDimensions()[1] / 6))
        else:
            self.__buttonFrame.config(
            width=round(self.__topLevel.getTopLevelDimensions()[0] / 2), height=round(self.__topLevel.getTopLevelDimensions()[1] / 4))
        self.__buttonFrame.pack_propagate(False)
        self.__buttonFrame.pack(side=TOP, anchor=N, fill=BOTH)

        self.__minusButton = Button(self.__buttonFrame, width=round(self.__topLevel.getTopLevelDimensions()[0] / 6),
                                    bg=self.__loader.colorPalettes.getColor("window"),
                                    image=self.__minus, command=self.__neg
                                    )
        self.__minusButton.pack_propagate(False)
        self.__minusButton.pack(side=LEFT, anchor=W, fill=Y)
        self.__positiveButton = Button(self.__buttonFrame, width=round(self.__topLevel.getTopLevelDimensions()[0] / 6),
                                    bg=self.__loader.colorPalettes.getColor("window"),
                                    image=self.__plus, command=self.__pos
                                    )
        self.__positiveButton.pack_propagate(False)
        self.__positiveButton.pack(side=LEFT, anchor=E, fill=Y)


        self.__buttonFrame2 = Frame(self.__controllerFrame, bg=self.__loader.colorPalettes.getColor("window"))
        if self.__mode == "64pxPicture":
            self.__buttonFrame2.config(
            width=round(self.__topLevel.getTopLevelDimensions()[0] / 2),
            height = round(self.__topLevel.getTopLevelDimensions()[1] / 2))
        else:
            self.__buttonFrame2.config(
            width=round(self.__topLevel.getTopLevelDimensions()[0] / 2),
            height = round(self.__topLevel.getTopLevelDimensions()[1] / 3))
        self.__buttonFrame2.pack_propagate(False)
        self.__buttonFrame2.pack(side=TOP, anchor=N, fill=BOTH)

        self.__okButton = Button(self.__buttonFrame2,
                                    bg=self.__loader.colorPalettes.getColor("window"),
                                    fg=self.__loader.colorPalettes.getColor("font"),
                                    text=self.__dictionaries.getWordFromCurrentLanguage("ok"),
                                    font=self.__smallFont, command=self.setAndKill
                                    )
        self.__okButton.pack_propagate(False)
        self.__okButton.pack(side=TOP, anchor=E, fill=X)

        if self.__mode == "64pxPicture":
            self.__okButton.config(text=self.__dictionaries.getWordFromCurrentLanguage("savePicture"))

            self.__bothButtonsFrame = Frame(self.__buttonFrame2, bg=self.__loader.colorPalettes.getColor("window"),
                                            width=round(self.__topLevel.getTopLevelDimensions()[0] / 2),
                                            height = round(self.__topLevel.getTopLevelDimensions()[1] / 8))
            self.__bothButtonsFrame.pack_propagate(False)
            self.__bothButtonsFrame.pack(side=TOP, anchor=E, fill=X)

            self.__bothButtonsFrame1 = Frame(self.__bothButtonsFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                            width=round(self.__topLevel.getTopLevelDimensions()[0] / 6),
                                            height = round(self.__topLevel.getTopLevelDimensions()[1] / 8))
            self.__bothButtonsFrame1.pack_propagate(False)
            self.__bothButtonsFrame1.pack(side=LEFT, anchor=E, fill=Y)

            self.__bothButtonsFrame2 = Frame(self.__bothButtonsFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                            width=round(self.__topLevel.getTopLevelDimensions()[0] / 6),
                                            height = round(self.__topLevel.getTopLevelDimensions()[1] / 8))
            self.__bothButtonsFrame2.pack_propagate(False)
            self.__bothButtonsFrame2.pack(side=LEFT, anchor=E, fill=Y)


            self.__testButton = Button(self.__bothButtonsFrame1,
                                        bg=self.__loader.colorPalettes.getColor("window"),
                                        fg=self.__loader.colorPalettes.getColor("font"), width=99999999,
                                        text=self.__dictionaries.getWordFromCurrentLanguage("preview")[:-1],
                                        font=self.__smallFont, command=self.testingThread
                                        )
            self.__testButton.pack_propagate(False)
            self.__testButton.pack(side=LEFT, anchor=W, fill=BOTH)

            self.__editButton = Button(self.__bothButtonsFrame2,
                                        bg=self.__loader.colorPalettes.getColor("window"),
                                        fg=self.__loader.colorPalettes.getColor("font"), width=99999999,
                                        text=self.__dictionaries.getWordFromCurrentLanguage("editPicture"),
                                        font=self.__smallFont2, command=self.setEditAndKill
                                        )
            self.__editButton.pack_propagate(False)
            self.__editButton.pack(side=LEFT, anchor=W, fill=BOTH)


        self.__cancelButton = Button(self.__buttonFrame2,
                                    bg=self.__loader.colorPalettes.getColor("window"),
                                    fg=self.__loader.colorPalettes.getColor("font"),
                                    text=self.__dictionaries.getWordFromCurrentLanguage("cancel"),
                                    font=self.__smallFont, command=self.killMe
                                    )
        self.__cancelButton.pack_propagate(False)
        self.__cancelButton.pack(side=TOP, anchor=E, fill=X)

        if self.__mode == "64pxPicture":
            self.__okButton.config(font=self.__smallFont2)
            self.__testButton.config(font=self.__smallFont2)
            self.__cancelButton.config(font=self.__smallFont2)

        self.__imageFrame2 = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"))
        self.__imageFrame2.config(
            width=round(self.__topLevel.getTopLevelDimensions()[0] /3))
        self.__imageFrame2.pack_propagate(False)
        self.__imageFrame2.pack(side=LEFT, anchor=W, fill=Y)

        self.blackAndWhite()

    def __checkHEX(self, event):
        if len(self.__oneColor.get()) > 3:
            self.__oneColor.set(self.__oneColor.get()[:3])

        try:
            self.setEntryColor()
        except:
            self.__oneColorEntry.config(
                bg = self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                fg=self.__loader.colorPalettes.getColor("boxFontUnSaved")
            )

    def setEntryColor(self):
        color1 = self.__oneColor.get()
        bg = self.__loader.colorDict.getHEXValueFromTIA(color1)
        if int("0x" + color1[2], 16) > 8:
            color2 = color1[:2] + hex(int("0x" + color1[2], 16) - 4).replace("0x", "")
        else:
            color2 = color1[:2] + hex(int("0x" + color1[2], 16) + 4).replace("0x", "")
        self.__oneColorEntry.config(
            bg=bg,
            fg=self.__loader.colorDict.getHEXValueFromTIA(color2)
        )

    def __getColor(self):
        from tkinter import colorchooser

        color_code = colorchooser.askcolor(title="Choose color")
        self.__colorButton.config(bg=color_code[1].replace("$", "#"))

        self.__oneColor.set(self.__loader.colorDict.getClosestTIAColor(int(color_code[0][0]), int(color_code[0][2]), int(color_code[0][1])))
        self.setEntryColor()

        self.__topLevelWindow.deiconify()
        self.__topLevelWindow.focus()

    def testingThread(self):
        from threading import Thread

        t = Thread(target=self.testing)
        t.daemon = True
        t.start()

    def testing(self):
        self.generateImage(self.__mode, self.__image, True)

    def killMe(self):
        self.__topLevelWindow.destroy()
        self.dead=True

    def setEditAndKill(self):
        self.__editPicture = True
        self.setAndKill()

    def setAndKill(self):
        self.doThings = True
        if self.__mode == "64pxPicture":
            self.__name = self.__thisVar.get()
        self.killMe()

    def __checkNumber(self, event):
        num = 0
        try:
            num = int(self.__tres.get())
        except:
            self.__number.config(
                bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                fg=self.__loader.colorPalettes.getColor("boxFontUnSaved")
            )
        self.__number.config(
            bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
            fg=self.__loader.colorPalettes.getColor("boxFontNormal")
            )

        if num<0:
            num = self.__tres.set("0")
        elif self.__mode == "64pxPicture" and num>128:
            num = self.__tres.set("128")
        elif self.__mode == "playfield" and num>255:
            num = self.__tres.set("255")

        self.updateBlackAndWhite()

    def __pos(self):
        num = int(self.__tres.get())

        if self.__mode == "64pxPicture" and num<117:
            self.__tres.set(str(num + 10))
        elif self.__mode == "playfield" and num<245:
            self.__tres.set(str(num+10))

        self.updateBlackAndWhite()


    def __neg(self):
        num = int(self.__tres.get())

        if num>10:
            self.__tres.set(str(num-10))

        self.updateBlackAndWhite()

    def blackAndWhite(self):

        from copy import deepcopy

        #for slave in self.__imageFrame.pack_slaves():
        #    slave.destroy()

        h = round(self.__topLevel.getTopLevelDimensions()[1])
        image = IMG.open(self.answer, "r")
        width, height = image.size

        multi = h / height
        w = round(image.width * multi)

        imageSized = image.resize((w, h), IMG.ANTIALIAS)


        self.img1 = ImageTk.PhotoImage(imageSized)

        self.label1 = Label(self.__imageFrame,
            height=round(self.__topLevel.getTopLevelDimensions()[1]), image = self.img1
            )
        self.label1.pack(side=LEFT, fill=BOTH)

        self.label2 = Label(self.__imageFrame2,
            height=round(self.__topLevel.getTopLevelDimensions()[1]), image=self.img1
            )
        self.label2.pack(side=RIGHT, fill=BOTH)
        self.updateBlackAndWhite()

    def updateBlackAndWhite(self):
        image = IMG.open(self.answer, "r")
        from PIL import ImageOps
        import numpy as np

        if self.__mode == "playfield":
            try:
                image = ImageOps.invert(image)
                image = ImageOps.invert(image)
            except:
                self.__check.config(state=DISABLED)

            if self.__invert.get():
                image = ImageOps.invert(image)

            if self.__right.get():
                from PIL import ImageOps
                image = ImageOps.mirror(image)

        width, height = image.size
        h = round(self.__topLevel.getTopLevelDimensions()[1])


        multi = h / height
        w = round(image.width * multi)
        imageSized = image.resize((w, h), IMG.ANTIALIAS)

        if self.__mode == "playfield":
            fn = lambda x: 255 if x > int(self.__tres.get()) else 0
            altImage = deepcopy(imageSized).convert('L').point(fn, mode='1')
        elif self.__mode == "64pxPicture":
            fn1 = lambda x: 255 if x > int(self.__tres.get()) else 0
            fn2 = lambda x: 255 if x > int(self.__tres.get())+128 else 0
            altImage1 = deepcopy(imageSized).convert('L').point(fn1, mode='1')
            altImage2 = deepcopy(imageSized).convert('L').point(fn2, mode='1')

            pixels1 = altImage1.load()
            pixels2 = altImage2.load()

            W, H = altImage1.size

            pixels = []

            for Y in range(0, H):
                for X in range(0, W):
                    value = (pixels1[X,Y] + pixels2[X,Y]  )//2
                    #pixels.append((value, value, value))
                    #data+=chr(value) + chr(value) + chr(value)
                    pixels.append(value)
                    pixels.append(value)
                    pixels.append(value)


            altImage = IMG.frombytes("RGB", (w, h), bytes(pixels))

            #altImage1.save("temp/temp.png")
            #altImage = IMG.open("temp/temp.png")

        self.img2 = ImageTk.PhotoImage(altImage)
        self.label2.config(image = self.img2)

if __name__ == "__main__":
    code = PictureToCode("C:\cat.jpg", "common", "playfield", None)
