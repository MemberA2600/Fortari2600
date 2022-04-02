from tkinter import *
from SubMenu import SubMenu
from threading import Thread

class LandScapeEditor:

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
        self.__chars = {}
        self.__play = False
        self.__counter = 0
        self.__validFName = True

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize*0.65), False, False, False)
        self.__bigFont = self.__fontManager.getFont(int(self.__fontSize*1.15), False, False, False)
        self.__bigFont2 = self.__fontManager.getFont(int(self.__fontSize*1.5), False, False, False)


        self.__offset     = 0
        self.__width      = 80      # Two screens
        self.__maxWidth   = 232
        self.__lineHeight = 1
        self.__play = False

        self.__sizes = [self.__screenSize[0] / 1.15, self.__screenSize[1] / 2 - 55]
        self.__window = SubMenu(self.__loader, "landscape", self.__sizes[0], self.__sizes[1], None, self.__addElements, 1)

        self.dead = True

    def __closeWindow(self):
        if self.changed == True:
            answer = self.__fileDialogs.askYesNoCancel("notSavedFile", "notSavedFileMessage")
            if answer == "Yes":
                self.__saveLS()
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

        self.__editorFrame = Frame(self.__topLevelWindow, width=self.__sizes[0],
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = round(self.__sizes[1]//5*1.75)
                                   )
        self.__editorFrame.pack_propagate(False)
        self.__editorFrame.pack(side=TOP, anchor=N, fill=X)

        self.__editorControlFrame = Frame(self.__topLevelWindow, width=self.__sizes[0],
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = round(self.__sizes[1]//5*0.25)
                                   )
        self.__editorControlFrame.pack_propagate(False)
        self.__editorControlFrame.pack(side=TOP, anchor=N, fill=X)

        self.__displayFrame = Frame(self.__topLevelWindow, width=self.__sizes[0],
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = self.__sizes[1]//5*2
                                   )
        self.__displayFrame.pack_propagate(False)
        self.__displayFrame.pack(side=TOP, anchor=N, fill=X)

        self.__controlFrame = Frame(self.__topLevelWindow, width=self.__sizes[0],
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = round(self.__sizes[1]//5*2)
                                   )
        self.__controlFrame.pack_propagate(False)
        self.__controlFrame.pack(side=TOP, anchor=N, fill=BOTH)

        self.__editorPixelsFrame = Frame(self.__editorFrame, width=self.__sizes[0]*0.85,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = self.__sizes[1]//5*2
                                   )
        while self.__editorPixelsFrame.winfo_width() < 2:
            self.__editorPixelsFrame.config(width=self.__sizes[0]*0.85,
                                            height = self.__sizes[1]//5*2)
            self.__editorPixelsFrame.pack_propagate(False)
            self.__editorPixelsFrame.pack(side=LEFT, anchor=E, fill=Y)


        self.__editorColorsFrame = Frame(self.__editorFrame, width=self.__sizes[0]*0.15,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = self.__sizes[1]//5*2
                                   )
        while self.__editorColorsFrame.winfo_width() < 2:
            self.__editorColorsFrame.config(width=self.__sizes[0]*0.15,
                                            height = self.__sizes[1]//5*2)
            self.__editorColorsFrame.pack_propagate(False)
            self.__editorColorsFrame.pack(side=LEFT, anchor=E, fill=Y)

        from threading import Thread

        self.__finished = [False, False, False, False, False, False]

        t1 = Thread(target=self.__createData)
        t1.daemon = True
        t1.start()

        t2 = Thread(target=self.__createEditorPixelsFrame)
        t2.daemon = True
        t2.start()

        t3 = Thread(target=self.__createEditorColorsFrame)
        t3.daemon = True
        t3.start()

        t4 = Thread(target=self.__createDataHandler)
        t4.daemon = True
        t4.start()

        t5 = Thread(target=self.__createCanvas())
        t5.daemon = True
        t5.start()

        t6 = Thread(target=self.__createBottom())
        t6.daemon = True
        t6.start()

        L = Thread(target=self.__loop)
        L.daemon = True
        L.start()

        self.__topLevelWindow.bind("<KeyPress-Control_L>", self.shiftON)
        self.__topLevelWindow.bind("<KeyRelease-Control_L>", self.shiftOff)
        self.__topLevelWindow.bind("<KeyPress-Control_R>", self.shiftON)
        self.__topLevelWindow.bind("<KeyRelease-Control_R>", self.shiftOff)
        self.__topLevelWindow.bind("<Button-2>", self.drawMode)

    def __createBottom(self):
        self.__theFuck = Frame(self.__controlFrame, bg=self.__loader.colorPalettes.getColor("window"), height=9999, width = self.__sizes[0]//5*2)
        self.__theFuck.pack_propagate(False)
        self.__theFuck.pack(side=LEFT, anchor=E, fill=Y)

        self.__offsetLabel = Label(self.__theFuck,
                                    text=self.__dictionaries.getWordFromCurrentLanguage("xOffset")+":",
                                    font=self.__bigFont, fg=self.__colors.getColor("font"),
                                    bg=self.__colors.getColor("window"), justify = CENTER
                                    )

        self.__offsetLabel.pack_propagate(False)
        self.__offsetLabel.pack(side=TOP, anchor=N, fill=X)

        self.__thePlayer = Frame(self.__theFuck, bg=self.__loader.colorPalettes.getColor("window"), height=99999, width = self.__sizes[0]//5*2)
        self.__thePlayer.pack_propagate(False)
        self.__thePlayer.pack(side=TOP, anchor=N, fill=BOTH)

        self.__offsetVal = StringVar()
        self.__offsetVal.set("0")

        self.__backImage = self.__loader.io.getImg("backwards", None)
        self.__forImage = self.__loader.io.getImg("forwards", None)
        self.__playImage = self.__loader.io.getImg("play", None)
        self.__stopImage = self.__loader.io.getImg("stop", None)

        self.__backButton = Button(self.__thePlayer, bg=self.__loader.colorPalettes.getColor("window"),
                                   image=self.__backImage,
                                   width= self.__thePlayer.winfo_width() // 4,
                                   state=DISABLED,
                                   command=self.__decOffSet)

        self.__offsetEntryFrame = Frame(self.__thePlayer, bg=self.__loader.colorPalettes.getColor("window"),
                                       width=self.__thePlayer.winfo_width() - (self.__thePlayer.winfo_width() // 4 * 3))

        self.__entryFrame = Entry(self.__offsetEntryFrame, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                   width=self.__thePlayer.winfo_width() - (self.__thePlayer.winfo_width() // 4 * 3),
                                   fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                   textvariable = self.__offsetVal, name = "offsetEntry",
                                   state=DISABLED, font=self.__bigFont2, justify = CENTER,
                                   command=None)

        self.__forButton = Button(self.__thePlayer, bg=self.__loader.colorPalettes.getColor("window"),
                                   image=self.__forImage,
                                   width=self.__thePlayer.winfo_width() // 4,
                                   state=DISABLED,
                                   command=self.incOffSet)

        self.__playButton = Button(self.__thePlayer, bg=self.__loader.colorPalettes.getColor("window"),
                                   image=self.__playImage, state = DISABLED,
                                   width=self.__thePlayer.winfo_width() // 4,
                                   command=self.__moveIt)

        self.__backButton.pack_propagate(False)
        self.__backButton.pack(side=LEFT, anchor=W, fill=Y)
        self.__offsetEntryFrame.pack_propagate(False)
        self.__offsetEntryFrame.pack(side=LEFT, anchor=W, fill=Y)
        self.__entryFrame.pack_propagate(False)
        self.__entryFrame.pack(side=LEFT, anchor=W, fill=BOTH)
        self.__forButton.pack_propagate(False)
        self.__forButton.pack(side=LEFT, anchor=W, fill=Y)
        self.__playButton.pack_propagate(False)
        self.__playButton.pack(side=LEFT, anchor=W, fill=Y)

        self.__entryFrame.bind("<KeyRelease>", self.__checkOffEntry)
        self.__entryFrame.bind("<FocusOut>", self.__checkOffEntry)

        self.__theFuck2 = Frame(self.__controlFrame, bg=self.__loader.colorPalettes.getColor("window"), height=9999, width = self.__sizes[0]//7)
        self.__theFuck2.pack_propagate(False)
        self.__theFuck2.pack(side=LEFT, anchor=E, fill=Y)

        self.__widthLabel = Label(self.__theFuck2,
                                    text=self.__dictionaries.getWordFromCurrentLanguage("width")+":",
                                    font=self.__bigFont, fg=self.__colors.getColor("font"),
                                    bg=self.__colors.getColor("window"), justify = CENTER
                                    )

        self.__widthLabel.pack_propagate(False)
        self.__widthLabel.pack(side=TOP, anchor=N, fill=X)

        self.__theSetter = Frame(self.__theFuck2, bg=self.__loader.colorPalettes.getColor("window"), height=99999, width = self.__sizes[0]//5*2)
        self.__theSetter.pack_propagate(False)
        self.__theSetter.pack(side=TOP, anchor=N, fill=BOTH)

        self.__theSetter2 = Frame(self.__theSetter, bg=self.__loader.colorPalettes.getColor("window"), height=99999, width = self.__sizes[0]//5*2)
        self.__theSetter2.pack_propagate(False)
        self.__theSetter2.pack(side=TOP, anchor=N, fill=BOTH)

        self.__widthVal = StringVar()
        self.__widthVal.set("80")

        self.__widthEntry = Entry(self.__theSetter2, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                   width=999999,
                                   fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                   textvariable = self.__widthVal, name = "widthEntry",
                                   state=DISABLED, font=self.__bigFont2, justify = CENTER,
                                   command=None)
        self.__widthEntry.pack_propagate(False)
        self.__widthEntry.pack(side=LEFT, fill=BOTH)

        self.__widthEntry.bind("<KeyRelease>", self.__checkWidthEntry)
        self.__widthEntry.bind("<FocusOut>", self.__checkWidthEntry)

        self.__theFuck3 = Frame(self.__controlFrame, bg=self.__loader.colorPalettes.getColor("window"), height=9999, width = 999999)
        self.__theFuck3.pack_propagate(False)
        self.__theFuck3.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__nameLabel = Label(self.__theFuck3,
                                    text=self.__dictionaries.getWordFromCurrentLanguage("name"),
                                    font=self.__bigFont, fg=self.__colors.getColor("font"),
                                    bg=self.__colors.getColor("window"), justify = CENTER
                                    )

        self.__nameLabel.pack_propagate(False)
        self.__nameLabel.pack(side=TOP, anchor=N, fill=X)

        self.__theFuck4 = Frame(self.__theFuck3, bg=self.__loader.colorPalettes.getColor("window"), height=9999, width = 999999)
        while self.__theFuck4.winfo_width() < 2:
            self.__theFuck4.pack_propagate(False)
            self.__theFuck4.pack(side=TOP, anchor=N, fill=BOTH)

        self.__nameEntryFrame = Frame(self.__theFuck4, bg=self.__loader.colorPalettes.getColor("window"), height=9999,
                                      width = round(self.__theFuck4.winfo_width()//1.5))
        self.__nameEntryFrame.pack_propagate(False)
        self.__nameEntryFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__nameVal = StringVar()
        self.__nameVal.set("Fatherland")

        self.__nameEntry = Entry(self.__nameEntryFrame, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                   width=999999,
                                   fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                   textvariable = self.__nameVal, name = "nameEntry",
                                   font=self.__bigFont)
        self.__nameEntry.pack_propagate(False)
        self.__nameEntry.pack(side=LEFT, fill=BOTH)

        self.__theFuck5 = Frame(self.__theFuck4, bg=self.__loader.colorPalettes.getColor("window"), height=9999, width = 999999)
        while self.__theFuck5.winfo_width() < 2:
            self.__theFuck5.pack_propagate(False)
            self.__theFuck5.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__nameEntry.bind("<KeyRelease>", self.checkIfValidFileName)
        self.__nameEntry.bind("<FocusOut>", self.checkIfValidFileName)

        self.__openFrame = Frame(self.__theFuck5, bg=self.__loader.colorPalettes.getColor("window"), height=9999,
                                 width = self.__theFuck5.winfo_width() // 3)
        self.__openFrame.pack_propagate(False)
        self.__openFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__saveFrame = Frame(self.__theFuck5, bg=self.__loader.colorPalettes.getColor("window"), height=9999,
                                 width = self.__theFuck5.winfo_width() // 3)
        self.__saveFrame.pack_propagate(False)
        self.__saveFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__testFrame = Frame(self.__theFuck5, bg=self.__loader.colorPalettes.getColor("window"), height=9999,
                                 width = self.__theFuck5.winfo_width() // 3)
        self.__testFrame.pack_propagate(False)
        self.__testFrame.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__openImage = self.__loader.io.getImg("open", None)
        self.__saveImage = self.__loader.io.getImg("save", None)
        self.__testImage = self.__loader.io.getImg("stella", None)


        self.__openImageButton = Button(self.__openFrame, height=9999, width=9999,
                   bg=self.__loader.colorPalettes.getColor("window"),
                   image = self.__openImage,
                   state=DISABLED, command = self.__openLS
                   )
        self.__openImageButton.pack_propagate(False)
        self.__openImageButton.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__saveImageButton = Button(self.__saveFrame, height=9999, width=9999,
                   bg=self.__loader.colorPalettes.getColor("window"),
                   image = self.__saveImage,
                   state=DISABLED, command = self.__saveLS
                   )
        self.__saveImageButton.pack_propagate(False)
        self.__saveImageButton.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__testImageButton = Button(self.__testFrame, height=9999, width=9999,
                   bg=self.__loader.colorPalettes.getColor("window"),
                   image = self.__testImage,
                   state=DISABLED, command = self.__testLS
                   )
        self.__testImageButton.pack_propagate(False)
        self.__testImageButton.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__finished[5] = True

    def __testLS(self):
        pass

    def __openLS(self):
        compatibles = {
            "common": ["common"]
        }

        if self.changed == True:
            answer = self.__fileDialogs.askYesNoCancel("notSavedFile", "notSavedFileMessage")
            if answer == "Yes":
                self.__saveLS()
            elif answer == "Cancel":
                self.__topLevelWindow.deiconify()
                self.__topLevelWindow.focus()
                return
        fpath = self.__fileDialogs.askForFileName("openFile", False, ["a26", "*"],
                                                  self.__loader.mainWindow.projectPath + "landscapes/")

        if fpath == "":
            return

        try:
        #if True:
            file = open(fpath, "r")
            data = file.readlines()
            file.close()

            if data[0].replace("\n", "").replace("\r", "") not in compatibles[self.__loader.virtualMemory.kernel]:
                if self.__fileDialogs.askYesNoCancel("differentKernel", "differentKernelMessage") == "No":
                    self.__topLevelWindow.deiconify()
                    self.__topLevelWindow.focus()
                    return


            self.__width = int(data[1])
            self.__widthVal.set(data[1])

            for lineNum in range(2,10):
                line = data[lineNum].replace("\r", "").replace("\n","").split(" ")
                trueLineNum = lineNum - 2
                self.__entries[trueLineNum][0].setValue(line[0])
                self.__entries[trueLineNum][1].setValue(line[1])

                self.__dataLines[trueLineNum]["colors"][0] = line[0]
                self.__dataLines[trueLineNum]["colors"][1] = line[1]


            for lineNum in range(10, 18):
                line = data[lineNum].replace("\r", "").replace("\n","").split(" ")
                trueLineNum = lineNum - 10
                for X in range(0, len(line)):
                    self.__dataLines[trueLineNum]["pixels"][X] = int(line[X])

            self.__soundPlayer.playSound("Success")
            self.redrawAllButtons()
        except Exception as e:
            self.__fileDialogs.displayError("unableToOpenFile", "unableToOpenFileMessage", None, str(e))

        self.__topLevelWindow.deiconify()
        self.__topLevelWindow.focus()


    def __saveLS(self):

        name1 = self.__loader.mainWindow.projectPath+"landscapes/"+self.__nameVal.get()+".a26"
        name2 = self.__loader.mainWindow.projectPath+"landscapes/"+self.__nameVal.get()+".asm"

        import os
        if os.path.exists(name1):
            answer = self.__fileDialogs.askYesOrNo("fileExists", "overWrite")
            self.__topLevelWindow.deiconify()
            self.__topLevelWindow.focus()

            if answer == "No":
                return

        txt = (self.__loader.virtualMemory.kernel   + "\n" +
               str(self.__width)                    + "\n")

        for theY in range(0,8):
            txt += self.__dataLines[theY]["colors"][0] +\
                   " " + self.__dataLines[theY]["colors"][1] + "\n"

        for theY in range(0,8):
            for theX in range(0, self.__maxWidth):
                txt += str(self.__dataLines[theY]["pixels"][theX])
                if theX == (self.__maxWidth-1):
                    txt += "\n"
                else:
                    txt += " "

        f = open(name1, "w")
        f.write(txt)
        f.close()

        trueWidth = self.__getTrueWidth()

        from Compiler import Compiler

        converted = Compiler(self.__loader, self.__loader.virtualMemory.kernel, "getLSASM",
                              [self.__dataLines, trueWidth, "NTSC", "##NAME##"]).converted

        f = open(name2, "w")
        f.write(
            "* Width=" + str(trueWidth+40) + "\n" + converted+ "\n")
        f.close()

        self.__soundPlayer.playSound("Success")
        self.changed = False

    def __getTrueWidth(self):
        for startX in range(self.__width-6, 0, -6):
            allZero = True
            for X in range(startX, startX+5, 1):
                for Y in range(0,8):
                    if self.__dataLines[Y]["pixels"][X] == 1:
                        allZero = False
                        break

                if allZero == False:
                   return X+6


    def checkIfValidFileName(self, event):
        try:
            name = str(event.widget).split(".")[-1]
        except:
            name = "landscape"

        if self.__loader.io.checkIfValidFileName(self.__nameVal.get()) == False:
           self.__nameEntry.config(
               bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
               fg=self.__loader.colorPalettes.getColor("boxFontUnSaved")
           )
           self.__validFName = False
        else:
            self.__nameEntry.config(
                bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                fg=self.__loader.colorPalettes.getColor("boxFontNormal")
            )
            self.__validFName = True

    def __decOffSet(self):
        if self.__offset <= 0:
           self.__offset = self.__width - 40
        else:
           self.__offset -= 1

        self.__offsetVal.set(str(self.__offset))
        self.redrawAllButtons()


    def incOffSet(self):
        if self.__offset >= self.__width - 40:
            self.__offset = 0
        else:
            self.__offset += 1

        self.__offsetVal.set(str(self.__offset))
        self.redrawAllButtons()

    def __checkWidthEntry(self, event):
        if self.__checkIfValid(self.__widthVal.get()) == False:
            self.__widthEntry.config(
                bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                fg=self.__loader.colorPalettes.getColor("boxFontUnSaved")
            )
        else:
            self.__widthEntry.config(
                bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                fg=self.__loader.colorPalettes.getColor("boxFontNormal")
            )

            self.__width = int(self.__widthVal.get())
            if self.__width < 40:
                self.__width = 40
            elif self.__width > self.__maxWidth:
                self.__width = self.__maxWidth

            self.__widthVal.set(str(self.__width))

        self.__checkOffEntry(event)
        self.changed = True


    def __checkOffEntry(self, event):
        if self.__checkIfValid(self.__offsetVal.get()) == False:
            self.__entryFrame.config(
                bg = self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                fg=self.__loader.colorPalettes.getColor("boxFontUnSaved")
            )
        else:
            self.__entryFrame.config(
                bg = self.__loader.colorPalettes.getColor("boxBackNormal"),
                fg=self.__loader.colorPalettes.getColor("boxFontNormal")
            )

            self.__offset = int(self.__offsetVal.get())
            if self.__offset < 0:
               self.__offset = 0
            elif self.__offset > self.__width - 40:
                if self.__play == True:
                    self.__offset = 0
                else:
                    self.__offset = self.__width - 40

            self.__offsetVal.set(str(self.__offset))

        self.redrawAllButtons()

    def __checkIfValid(self, val):
        try:
            teszt = int(val)
            return True
        except:
            return False

    def __moveIt(self):
        self.__play = 1 - self.__play

    def __createCanvas(self):
        self.__canvas = Canvas(self.__displayFrame, bg="black", bd=0,
                               width=99999,
                               height=99999
                               )
        while self.__canvas.winfo_width() < 2:
            self.__canvas.pack_propagate(False)
            self.__canvas.pack(side=TOP, anchor=N, fill=BOTH)

        self.__canvasW = self.__canvas.winfo_width() // 39
        self.__canvasH = self.__canvas.winfo_height() // 8

        self.__redrawCanvas()
        self.__finished[4] = True

    def __redrawCanvas(self):
        self.__canvas.clipboard_clear()
        self.__canvas.delete("all")

        for theY in range(0,8):
            self.__canvas.create_rectangle(0,
                                           theY*self.__canvasH,
                                           self.__canvas.winfo_width(),
                                           (theY+1) * self.__canvasH,
                                           outline="",
                                           fill=self.__colorDict.getHEXValueFromTIA(
                                               self.__dataLines[theY]["colors"][1]
                                           ))

            for theX in range(0,40):
                if self.__dataLines[theY]["pixels"][theX+self.__offset] == 1:
                    self.__canvas.create_rectangle(theX * self.__canvasW,
                                                   theY * self.__canvasH,
                                                   (theX + 1) * self.__canvasW,
                                                   (theY + 1) * self.__canvasH,
                                                   outline="",
                                                   fill=self.__colorDict.getHEXValueFromTIA(
                                                       self.__dataLines[theY]["colors"][0]
                                                   ))


    def __createDataHandler(self):
        self.__randomF = Frame(self.__editorControlFrame, width=round(self.__sizes[0]*0.20), height=9999,
                  bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__randomF.pack_propagate(False)
        self.__randomF.pack(side=LEFT, anchor=E, fill=Y)

        self.__randomB = Button(self.__randomF, height=9999, width=9999,
                   bg=self.__loader.colorPalettes.getColor("window"),
                   fg=self.__loader.colorPalettes.getColor("font"),
                   text = self.__dictionaries.getWordFromCurrentLanguage("generateRandom"),
                   state=DISABLED, font = self.__smallFont, command = self.__generateRandom
                   )
        self.__randomB.pack_propagate(False)
        self.__randomB.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__textFrame = Frame(self.__editorControlFrame, width=round(self.__sizes[0]*0.60), height=9999,
                  bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__textFrame.pack_propagate(False)
        self.__textFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__textToConvert = StringVar()
        self.__textToConvert.set("...and then i noticed that she was a gargoyle!")
        self.__textEntry = Entry(self.__textFrame, textvariable=self.__textToConvert, font=self.__smallFont, state=DISABLED)
        self.__textEntry.pack_propagate(False)
        self.__textEntry.pack(fill=BOTH)

        self.__finished[3] = True

        self.randomTG = Frame(self.__editorControlFrame, width=round(self.__sizes[0]*0.20), height=9999,
                  bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.randomTG.pack_propagate(False)
        self.randomTG.pack(side=LEFT, anchor=E, fill=Y)

        self.__generateTB = Button(self.randomTG, height=9999, width=9999,
                   bg=self.__loader.colorPalettes.getColor("window"),
                   fg=self.__loader.colorPalettes.getColor("font"),
                   text = self.__dictionaries.getWordFromCurrentLanguage("generateText"),
                   state=DISABLED, font = self.__smallFont, command = self.__generateTXT
                   )
        self.__generateTB.pack_propagate(False)
        self.__generateTB.pack(side=LEFT, anchor=E, fill=BOTH)

    def __generateTXT(self):
        for theY in range(0,8):
            for theX in range(0,self.__maxWidth):
                self.__dataLines[theY]["pixels"][theX] = 0

        text = self.__textToConvert.get().upper()
        index = 0

        for char in text:
            if index > self.__maxWidth - 6:
               break

            if char not in self.__chars.keys():
               char = " "

            for Y in range(0,8):
                for X in range(0,5):
                    self.__dataLines[Y]["pixels"][index+X] = int(self.__chars[char][Y][X])

            index+=6

        self.redrawAllButtons()
        self.changed = True


    def __generateRandom(self):
        from random import randint, seed
        from datetime import datetime

        seed(int(str(datetime.now()).split(".")[-1]))

        number = randint(1,9)
        self.setThem(number, 0)

        for theX in range(1, self.__maxWidth):
            neeeeew = 0
            while neeeeew == 0:
                neeeeew = randint(-2,2)
                if number + neeeeew > 8 or number + neeeeew < 1:
                   neeeeew *= -1

            number += neeeeew
            self.setThem(number, theX)

        self.redrawAllButtons()
        self.changed = True


    def setThem(self, num, X):
        binary = "0"*(8-num) + "1"*num
        for Y in range(0,8):
            self.__dataLines[Y]["pixels"][X] = int(binary[Y])

    def redrawAllButtons(self):

        for theY in range(0,8):
            for theX in range(self.__offset, self.__offset+40):
                self.colorTile(theY, theX - self.__offset, self.__dataLines[theY]["pixels"][theX])

        self.__redrawCanvas()

    def __createData(self):
        self.__dataLines = []
        for theY in range(0,8):
            self.__dataLines.append(
                {
                    "pixels": [], "colors": ["$0e", "$00"]
                }
            )
            for theX in range(0, self.__maxWidth):
                self.__dataLines[-1]["pixels"].append(0)


        f = open("config/letters.txt")
        txt = f.readlines()
        f.close()

        lastChar = None
        for line in txt:
            line = line.replace("\n", "").replace("\r", "")
            if line != "":
               if len(line) == 1:
                  lastChar = line[0]
                  self.__chars[lastChar] = []
               else:
                  self.__chars[lastChar].append(line)

        self.__finished[0] = True

    def __createEditorPixelsFrame(self):
        w = self.__editorPixelsFrame.winfo_width() // 40
        h = self.__editorPixelsFrame.winfo_height() // 8

        self.__buttons = []

        for theY in range(0,8):
            self.__soundPlayer.playSound("Pong")
            self.__buttons.append([])
            rowF = Frame(self.__editorPixelsFrame,
                      bg=self.__loader.colorPalettes.getColor("window"),
                      width=self.__editorPixelsFrame.winfo_width(), height = h
                      )
            rowF.pack_propagate(False)
            rowF.pack(side=TOP, anchor=N, fill=X)

            while rowF.winfo_width() < 2:
                rowF.config(width=self.__editorPixelsFrame.winfo_width(), height = h)
                rowF.pack_propagate(False)
                rowF.pack(side=TOP, anchor=N, fill=X)

            for theX in range(0,40):
                name = str(theY) + "_" + str(theX)

                f = Frame(rowF, height = h, width = w,
                            bg = self.__loader.colorPalettes.getColor("boxBackNormal"))
                f.pack_propagate(False)
                f.pack(side=LEFT, anchor=E, fill=Y)

                b = Button(f, height = h, width = w, name = name,
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

        self.__finished[1] = True


    def __createEditorColorsFrame(self):

        from HexEntry import HexEntry

        w = self.__editorColorsFrame.winfo_width() // 2
        h = self.__editorColorsFrame.winfo_height() // 8

        self.__entries = []
        self.__entryVals = []

        for theY in range(0,8):
            self.__entries.append([])
            self.__entryVals.append(["$0e", "$00"])

            rowF = Frame(self.__editorColorsFrame,
                         bg=self.__loader.colorPalettes.getColor("window"),
                         width=self.__editorColorsFrame.winfo_width(), height=h
                         )
            rowF.pack_propagate(False)
            rowF.pack(side=TOP, anchor=N, fill=X)

            f0 = Frame(rowF, height = h, width = w,
                            bg = self.__loader.colorPalettes.getColor("window"))
            while f0.winfo_width() < 2:
                f0.pack_propagate(False)
                f0.pack(side=LEFT, anchor=E, fill=BOTH)

            f1 = Frame(rowF, height = h, width = w,
                            bg = self.__loader.colorPalettes.getColor("window"))
            while f1.winfo_width() < 2:
                f1.pack_propagate(False)
                f1.pack(side=LEFT, anchor=E, fill=BOTH)

            sp1Color = HexEntry(self.__loader, f0, self.__colors,
                       self.__colorDict, self.__smallFont, self.__entryVals[-1], 0, None, self.__setColorData)

            sp2Color = HexEntry(self.__loader, f1, self.__colors,
                       self.__colorDict, self.__smallFont, self.__entryVals[-1], 1, None, self.__setColorData)

            self.__entries[-1].append(sp1Color)
            self.__entries[-1].append(sp2Color)

            sp1Color.setValue("$0e")
            sp2Color.setValue("$00")

            sp1Color.changeState(DISABLED)
            sp2Color.changeState(DISABLED)

        self.__finished[2] = True

    def __clicked(self, event):
        for item in self.__finished:
            if item == False: return

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

        Y = int(name.split("_")[0])
        X = int(name.split("_")[1])

        if self.__draw == False:
            if self.__ctrl == False:
                self.__dataLines[Y]["pixels"][X + self.__offset] = 1 - self.__dataLines[Y]["pixels"][X + self.__offset]
            else:
                if   button == 1:
                    self.__dataLines[Y]["pixels"][X + self.__offset] = 1
                elif button == 3:
                    self.__dataLines[Y]["pixels"][X + self.__offset] = 3
        else:
            if self.__ctrl == False:
                self.__dataLines[Y]["pixels"][X + self.__offset] = 1
            else:
                self.__dataLines[Y]["pixels"][X + self.__offset] = 3

        self.colorTile(Y, X, self.__dataLines[Y]["pixels"][X + self.__offset])
        self.__redrawCanvas()
        self.changed = True


    def colorTile(self, Y, X, value):
        button = self.__buttons[Y][X]

        if value == 1:
           button.config(bg = self.__loader.colorPalettes.getColor("boxFontNormal"))
        else:
           button.config(bg = self.__loader.colorPalettes.getColor("boxBackNormal"))

    def __enter(self, event):
        for item in self.__finished:
            if item == False: return

        if self.__draw:
            self.__clicked(event)

    def __setColorData(self, event):
        for item in self.__finished:
            if item == False: return

        breaking = False
        for theY in range(0,8):
            for colorNum in range(0,2):
                if self.__entries[theY][colorNum].getEntry() == event.widget:
                    self.__dataLines[theY]["colors"][colorNum] = self.__entries[theY][colorNum].getValue()
                    breaking = True
                    break
            if breaking == True: break

        self.__redrawCanvas()
        self.changed = True


    def __loop(self):
        from time import sleep

        while self.dead == False and self.__mainWindow.dead == False:
            try:
                noLoop = False

                for item in self.__finished:
                    if item == False: noLoop = True

                if noLoop == False:
                    if self.__theyAreDisabled == True:
                        for yLine in self.__buttons:
                            for button in yLine:
                                button.config(state = NORMAL)

                        for yLine in self.__entries:
                            for entry in yLine:
                                entry.changeState(NORMAL)
                        self.__theyAreDisabled = False
                        self.__randomB.config(state=NORMAL)
                        self.__textEntry.config(state=NORMAL)
                        self.__generateTB.config(state=NORMAL)
                        self.__playButton.config(state=NORMAL)
                        self.__entryFrame.config(state=NORMAL)
                        self.__forButton.config(state=NORMAL)
                        self.__backButton.config(state=NORMAL)
                        self.__widthEntry.config(state=NORMAL)
                        self.__openImageButton.config(state=NORMAL)
                        self.__testImageButton.config(state=NORMAL)


                    else:
                        if self.__width == 40:
                            self.__playButton.config(state=DISABLED)
                            self.__entryFrame.config(state=DISABLED)
                            self.__forButton.config(state=DISABLED)
                            self.__backButton.config(state=DISABLED)
                            self.__play = False
                        else:
                            self.__playButton.config(state=NORMAL)
                            self.__entryFrame.config(state=NORMAL)
                            self.__forButton.config(state=NORMAL)
                            self.__backButton.config(state=NORMAL)

                        if self.__play == False:
                           self.__playButton.config(image = self.__playImage)
                           self.__counter = 0
                        else:
                            self.__playButton.config(image=self.__stopImage)
                            if self.__counter > 2:
                               self.__counter = 0

                               self.__offsetVal.set(str(self.__offset+1))
                               self.__checkOffEntry(None)
                            else:
                               self.__counter+=1

                        if self.changed == True and self.__validFName == True:
                           self.__saveImageButton.config(state=NORMAL)
                        else:
                           self.__saveImageButton.config(state=DISABLED)

            except:
                pass

            sleep(0.025)

    def drawMode(self, event):
        self.__draw = 1 - self.__draw

    def shiftON(self, event):
        self.__ctrl = True

    def shiftOff(self, event):
        self.__ctrl = False