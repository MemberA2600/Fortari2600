from SubMenu import SubMenu
from SubMenuLabel import SubMenuLabel
from SubMenuFrame import SubMenuFrame
from tkinter import *
import re
from time import sleep
from threading import Thread

class PlayfieldEditor:

    def __init__(self, loader, mainWindow):
        self.__loader = loader
        self.__mainWindow = mainWindow

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


        if self.__loader.virtualMemory.kernel == "common":
            self.__func = self.__addElementsCommon

        self.__ctrl = False
        self.__middle = False
        self.__draw = 0

        self.__sizes = {
            "common": [self.__screenSize[0] / 1.20, self.__screenSize[1]/1.10  - 45]
        }


        self.__window = SubMenu(self.__loader, "playfieldEditor", self.__sizes["common"][0],
                                self.__sizes["common"][1], None, self.__func)

        self.dead = True


    def checker(self):
        from time import sleep
        while(self.dead==False and self.__loader.mainWindow.dead == False):
            try:
                if self.changed == False:
                    self.__saveButton.config(state=DISABLED)
                    self.__saveButtonBG.config(state=DISABLED)
                else:
                    self.__saveButton.config(state=NORMAL)
                    self.__saveButtonBG.config(state=NORMAL)

            except Exception as e:
                self.__loader.logger.errorLog(e)


            sleep(0.4)

    def __addElementsCommon(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()

        self.__piff = 1
        self.__puff = 0.55
        self.__Y = 42
        self.__index = 0


        self.__playfieldFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"))
        self.__playfieldFrame.config(height=round(self.__topLevel.getTopLevelDimensions()[1]/self.__Y*self.__piff)*self.__Y)
        self.__playfieldFrame.pack_propagate(False)
        self.__playfieldFrame.pack(side=TOP, anchor=N, fill=X)

        self.__theField = Frame(self.__playfieldFrame, bg=self.__loader.colorPalettes.getColor("window"))

        calc = round(self.__topLevel.getTopLevelDimensions()[0]/40*self.__puff)*40
        self.__theField.config(width=calc)
        self.__theField.pack_propagate(False)
        self.__theField.pack(side=LEFT, anchor=W, fill=Y)

        self.__topLevelWindow.bind("<KeyPress-Control_L>", self.shiftON)
        self.__topLevelWindow.bind("<KeyRelease-Control_L>", self.shiftOff)
        self.__topLevelWindow.bind("<KeyPress-Control_R>", self.shiftON)
        self.__topLevelWindow.bind("<KeyRelease-Control_R>", self.shiftOff)
        self.__topLevelWindow.bind("<Button-2>", self.drawMode)

        calc2 = round(self.__topLevel.getTopLevelDimensions()[0]/40*self.__puff)*15

        self.__intTheMiddle = Frame(self.__playfieldFrame, bg=self.__loader.colorPalettes.getColor("window"))
        self.__intTheMiddle.config(width=calc2)
        self.__intTheMiddle.pack_propagate(False)
        self.__intTheMiddle.pack(side=LEFT, anchor=W, fill=Y)

        self.__colorTable = []
        for num in range(0,255):
            self.__colorTable.append(["$0E", "$00"])

        self.__colorFrames = {}
        self.__colorEntries = {}
        self.__colorEntryVar = {}
        self.__buttons = {}

        self.__fieldOnTheRight = Frame(self.__playfieldFrame, width=self.__topLevel.getTopLevelDimensions()[0]-calc-calc2,
                                       bg=self.__loader.colorPalettes.getColor("window")
                                       )
        self.__fieldOnTheRight.pack(side=LEFT, anchor=E, fill=Y)

        self.__previewLabel=Label(self.__fieldOnTheRight, text=self.__dictionaries.getWordFromCurrentLanguage("preview"),
                                  font=self.__normalFont, fg=self.__colors.getColor("font"),
                                  bg=self.__colors.getColor("window")
                                  )

        self.__previewLabel.pack_propagate(False)
        self.__previewLabel.pack(side=TOP, anchor=N, fill=X)

        self.__canvas = Canvas(self.__fieldOnTheRight, bg="black", bd=0,
                               width=self.__topLevel.getTopLevelDimensions()[0]-calc,
                               height=round(self.__topLevel.getTopLevelDimensions()[1]/5)
                               )

        self.__canvas.pack_propagate(False)
        self.__canvas.pack(side=TOP, anchor=N, fill=X)


        self.__theController = Frame(self.__fieldOnTheRight, bg=self.__loader.colorPalettes.getColor("window"), height=round(self.__topLevel.getTopLevelDimensions()[1]/5*4))
        self.__theController.config(width=self.__topLevel.getTopLevelDimensions()[0]-calc-calc2)
        self.__theController.pack_propagate(False)
        self.__theController.pack(side=TOP, anchor=N, fill=X)

        self.__height=StringVar()
        self.__height.set("42")
        ten = round(self.__topLevel.getTopLevelDimensions()[1]/25)

        self.__heightSetter = Frame(self.__theController, height = ten, bg=self.__loader.colorPalettes.getColor("window"))
        self.__heightSetter.pack_propagate(False)

        self.__heightSetter.pack(side=TOP, anchor=N, fill=X)
        self.__heightLabel = Label(self.__heightSetter, text=self.__dictionaries.getWordFromCurrentLanguage("height"),
                                   font=self.__smallFont,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   fg=self.__loader.colorPalettes.getColor("font")
                                   )
        self.__heightLabel.pack(side=LEFT, anchor=W, fill=Y)

        self.__heightEntry = Entry(self.__heightSetter, textvariable=self.__height, name="heightEntry")
        self.__heightEntry.config(width=99999, bg = self.__loader.colorPalettes.getColor("boxBackNormal"),
                                  fg = self.__loader.colorPalettes.getColor("boxFontNormal"),
                                  font=self.__smallFont
                                  )

        self.__heightEntry.bind("<KeyRelease>", self.checkHeightEntry)
        self.__heightEntry.bind("<FocusOut>", self.checkHeightEntry2)
        self.__heightEntry.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__indexVal = StringVar()
        self.__indexVal.set("0")

        self.__indexSetter = Frame(self.__theController, height = ten, bg=self.__loader.colorPalettes.getColor("window"))
        self.__indexSetter.pack_propagate(False)

        self.__indexSetter.pack(side=TOP, anchor=N, fill=X)
        self.__indexLabel = Label(self.__indexSetter, text=self.__dictionaries.getWordFromCurrentLanguage("index"),
                                   font=self.__smallFont,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   fg=self.__loader.colorPalettes.getColor("font")
                                   )
        self.__indexLabel.pack(side=LEFT, anchor=W, fill=Y)

        self.__indexEntry = Entry(self.__indexSetter, textvariable=self.__indexVal, name="indexEntry")
        self.__indexEntry.config(width=99999, bg = self.__loader.colorPalettes.getColor("boxBackNormal"),
                                  fg = self.__loader.colorPalettes.getColor("boxFontNormal"),
                                  font=self.__smallFont
                                  )

        self.__indexEntry.bind("<KeyRelease>", self.checkIndexEntry)
        self.__indexEntry.bind("<FocusOut>", self.checkIndexEntry2)
        self.__indexEntry.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__playfieldFrame = Frame(self.__theController, height=ten*3, bg=self.__loader.colorPalettes.getColor("window"))
        self.__playfieldFrame.pack_propagate(False)

        self.__playfieldFrame.pack(side=TOP, anchor=N, fill=X)

        self.__playfieldLabel = Label(self.__playfieldFrame, text=self.__dictionaries.getWordFromCurrentLanguage("playfield"),
                                   font=self.__normalFont,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   fg=self.__loader.colorPalettes.getColor("font")
                                   )
        self.__playfieldLabel.pack(side=TOP, anchor=W, fill=X)

        self.__playfieldSetter = Frame(self.__playfieldFrame, height=ten*2, bg=self.__loader.colorPalettes.getColor("window"))
        self.__playfieldSetter.pack_propagate(False)
        self.__playfieldSetter.pack(side=TOP, anchor=N, fill=X)

        self.__playfieldNameFrame = Frame(self.__playfieldSetter, height=ten, bg=self.__loader.colorPalettes.getColor("window"))
        self.__playfieldNameFrame.pack_propagate(False)
        self.__playfieldNameFrame.pack(side=TOP, anchor=N, fill=X)

        self.__playfieldNameLabel = Label(self.__playfieldNameFrame, text=self.__dictionaries.getWordFromCurrentLanguage("name"),
                                  font=self.__smallFont,
                                  bg=self.__loader.colorPalettes.getColor("window"),
                                  fg=self.__loader.colorPalettes.getColor("font")
                                  )
        self.__playfieldNameLabel.pack(side=LEFT, anchor=W, fill=Y)

        self.__pfName = StringVar()
        self.__pfName.set("Awesome_Playfield")

        self.__playfieldNameEntry = Entry(self.__playfieldNameFrame, textvariable=self.__pfName, name="pfName")
        self.__playfieldNameEntry.config(width=99999, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                 fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                 font=self.__smallFont
                                 )

        self.__playfieldNameEntry.pack(side=LEFT, anchor=E, fill=BOTH)
        self.__playfieldNameEntry.bind("<KeyRelease>", self.checkIfValidFileName)

        self.__playfieldButtonsFrame = Frame(self.__playfieldSetter, height=ten, bg=self.__loader.colorPalettes.getColor("window"))
        self.__playfieldButtonsFrame.pack_propagate(False)
        self.__playfieldButtonsFrame.pack(side=TOP, anchor=N, fill=X)

        self.__openPic = self.__loader.io.getImg("open", None)
        self.__savePic = self.__loader.io.getImg("save", None)

        self.__openButton = Button(self.__playfieldButtonsFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                   image = self.__openPic, width=(self.__topLevel.getTopLevelDimensions()[0]-calc-calc2)/2,
                                   command = self.__openPlayfield)

        self.__openButton.pack(side = LEFT, anchor = W, fill=Y)

        self.__saveButton = Button(self.__playfieldButtonsFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                   image = self.__savePic, width=(self.__topLevel.getTopLevelDimensions()[0]-calc-calc2)/2,
                                   state=DISABLED, command=self.__savePlayfield)

        self.__saveButton.pack(side = LEFT, anchor = W, fill=Y)


        self.__backgroundFrame = Frame(self.__theController, height=ten*3, bg=self.__loader.colorPalettes.getColor("window"))
        self.__backgroundFrame.pack_propagate(False)

        self.__backgroundFrame.pack(side=TOP, anchor=N, fill=X)

        self.__backgroundLabel = Label(self.__backgroundFrame, text=self.__dictionaries.getWordFromCurrentLanguage("background"),
                                   font=self.__normalFont,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   fg=self.__loader.colorPalettes.getColor("font")
                                   )
        self.__backgroundLabel.pack(side=TOP, anchor=W, fill=X)

        self.__backgroundSetter = Frame(self.__backgroundFrame, height=ten*2, bg=self.__loader.colorPalettes.getColor("window"))
        self.__backgroundSetter.pack_propagate(False)
        self.__backgroundSetter.pack(side=TOP, anchor=N, fill=X)

        self.__backgroundNameFrame = Frame(self.__backgroundSetter, height=ten, bg=self.__loader.colorPalettes.getColor("window"))
        self.__backgroundNameFrame.pack_propagate(False)
        self.__backgroundNameFrame.pack(side=TOP, anchor=N, fill=X)

        self.__backgroundNameLabel = Label(self.__backgroundNameFrame, text=self.__dictionaries.getWordFromCurrentLanguage("name"),
                                  font=self.__smallFont,
                                  bg=self.__loader.colorPalettes.getColor("window"),
                                  fg=self.__loader.colorPalettes.getColor("font")
                                  )
        self.__backgroundNameLabel.pack(side=LEFT, anchor=W, fill=Y)

        self.__bgName = StringVar()
        self.__bgName.set("Wonderful_Background")

        self.__backgroundNameEntry = Entry(self.__backgroundNameFrame, textvariable=self.__bgName, name="bgName")
        self.__backgroundNameEntry.config(width=99999, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                 fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                 font=self.__smallFont
                                 )

        self.__backgroundNameEntry.pack(side=LEFT, anchor=E, fill=BOTH)
        self.__backgroundNameEntry.bind("<KeyRelease>", self.checkIfValidFileName)

        self.__backgroundButtonsFrame = Frame(self.__backgroundSetter, height=ten, bg=self.__loader.colorPalettes.getColor("window"))
        self.__backgroundButtonsFrame.pack_propagate(False)
        self.__backgroundButtonsFrame.pack(side=TOP, anchor=N, fill=X)

        self.__openButtonBG = Button(self.__backgroundButtonsFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                   image = self.__openPic, width=(self.__topLevel.getTopLevelDimensions()[0]-calc-calc2)/2,
                                   command = self.__openBackground)

        self.__openButtonBG.pack(side = LEFT, anchor = W, fill=Y)

        self.__saveButtonBG = Button(self.__backgroundButtonsFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                   image = self.__savePic, width=(self.__topLevel.getTopLevelDimensions()[0]-calc-calc2)/2,
                                   state=DISABLED, command=self.__saveBackground)

        self.__saveButtonBG.pack(side = LEFT, anchor = W, fill=Y)


        #This is were the fun begins.
        ############################

        self.alreadyDone = False
        self.__frames = {}
        self.__table = []
        row = []
        self.__logicalX=[
            [4,35], [5,34], [6,33],
            [7,32], [8,31], [9,30],
            [10,29], [11,28], [12,27],
            [13,26], [14,25], [15,24],
            [16,23], [17,22], [18,21],
            [19,20]
            ]

        #print(self.__logicalX)
        from copy import deepcopy

        for num in range(0,40):
            row.append("0")

        for num in range(0,256):
            self.__table.append(deepcopy(row))

        e = Thread(target=self.generateTableCommon)
        e.daemon=True
        e.start()

        t = Thread(target=self.checker)
        t.daemon = True
        t.start()


    def __openPlayfield(self):
        import os

        if self.changed == True:
            answer = self.__fileDialogs.askYesNoCancel("notSavedFile", "notSavedFileMessage")
            if answer == "Yes":
                self.__savePlayfield()
            elif answer == "Cancel":
                return

        fpath = self.__fileDialogs.askForFileName("openFile", False, ["a26", "*"],
                                                  self.__loader.mainWindow.projectPath + "playfields/")

        if fpath == "":
            return

        try:
            file = open(fpath, "r")
            data = file.readlines()
            file.close()

            if self.__loader.virtualMemory.kernel != data[0].replace("\n","").replace("\r",""):
                if self.__fileDialogs.askYesNoCancel("differentKernel", "differentKernelMessage") == "No":
                    return

            self.__pfName.set(".".join(fpath.split(os.sep)[-1].split(".")[:-1]))

            self.__height.set(data[1].replace("\n","").replace("\r",""))
            maxY = int(self.__height.get())
            data.pop(0)
            data.pop(0)

            for Y in range(0, maxY):
                line = data[Y].replace("\n","").replace("\r","").split(" ")
                self.__colorTable[Y][0] = line[-1]
                for X in range(0,40):
                    self.__table[Y][X] = line[X]

            self.__soundPlayer.playSound("Success")
            self.changed=False

            self.__topLevelWindow.deiconify()
            self.__topLevelWindow.focus()
            self.alreadyDone = True
            self.firstLoad = True

            self.generateTableCommon()

        except Exception as e:
            self.__fileDialogs.displayError("unableToOpenFile", "unableToOpenFileMessage",None, str(e))
            self.__topLevelWindow.deiconify()
            self.__topLevelWindow.focus()



    def __savePlayfield(self):
        import os

        fileName = self.__loader.mainWindow.projectPath + "playfields/"+self.__pfName.get()+".a26"
        if os.path.exists(fileName):
            answer=self.__fileDialogs.askYesOrNo("fileExists", "overWrite")
            if answer == "No":
                return
        fileLines = []
        fileLines.append(self.__loader.virtualMemory.kernel)
        fileLines.append(self.__height.get())
        for Y in range(0, int(self.__height.get())):
            fileLines.append(" ".join(self.__table[Y])+" "+self.__colorTable[Y][0])

        file = open(fileName, "w")
        file.write("\n".join(fileLines))
        file.close()
        self.__soundPlayer.playSound("Success")
        self.changed=False

    def __openBackground(self):
        import os

        if self.changed == True:
            answer = self.__fileDialogs.askYesNoCancel("notSavedFile", "notSavedFileMessage")
            if answer == "Yes":
                self.__saveBackground()
            elif answer == "Cancel":
                return

        fpath = self.__fileDialogs.askForFileName("openFile", False, ["a26", "*"],
                                                  self.__loader.mainWindow.projectPath + "backgrounds/")

        if fpath == "":
            return

        try:
            file = open(fpath, "r")
            data = file.readlines()
            file.close()

            if self.__loader.virtualMemory.kernel != data[0].replace("\n", "").replace("\r", ""):
                if self.__fileDialogs.askYesNoCancel("differentKernel", "differentKernelMessage") == "No":
                    return

            self.__bgName.set(".".join(fpath.split(os.sep)[-1].split(".")[:-1]))

            self.__height.set(data[1].replace("\n", "").replace("\r", ""))
            maxY = int(self.__height.get())

            line = data[-1].replace("\n", "").replace("\r", "").split(" ")

            for Y in range(0, maxY):
                self.__colorTable[Y][1] = line[Y]

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

    def __saveBackground(self):
        import os

        fileName = self.__loader.mainWindow.projectPath + "backgrounds/" + self.__bgName.get() + ".a26"
        if os.path.exists(fileName):
            answer = self.__fileDialogs.askYesOrNo("fileExists", "overWrite")
            if answer == "No":
                return
        fileLines = []
        fileLines.append(self.__loader.virtualMemory.kernel)
        fileLines.append(self.__height.get())

        lastLine = ""

        for Y in range(0, int(self.__height.get())):
            lastLine += " " + self.__colorTable[Y][1]
        fileLines.append(lastLine[1:])

        file = open(fileName, "w")
        file.write("\n".join(fileLines))
        file.close()
        self.__soundPlayer.playSound("Success")
        self.changed = False

    def checkIfValidFileName(self, event):

        name = str(event.widget).split(".")[-1]

        if name == "pfName":
            widget = self.__playfieldNameEntry
            value = self.__pfName
        elif name == "bgName":
            widget = self.__backgroundNameEntry
            value = self.__bgName

        if self.__loader.io.checkIfValidFileName(value.get()):
            widget.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                      fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                      )

        else:
            widget.config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                                      fg=self.__loader.colorPalettes.getColor("boxFontUnSaved"),
                                      font=self.__smallFont
                                      )


    def checkHeightEntry(self, event):
        num = 0

        try:
            num = int(self.__height.get())
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
            num = int(self.__height.get())
            if num<42:
                self.__height.set("42")


            if num>256:
                self.__height.set("256")

        except:
            return
        self.checkIndexEntry2(event)

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

            """
            if num>256-int(self.__height.get()):
                self.__indexVal.set(str(256-int(self.__height.get())))

            """

            if num>int(self.__height.get())-self.__Y:
                self.__indexVal.set(str(int(self.__height.get())-self.__Y))

        except Exception as e:
            pass

        self.__index = int(self.__indexVal.get())
        self.generateTableCommon()

    def shiftON(self, event):
        self.__ctrl = True

    def shiftOff(self, event):
        self.__ctrl = False

    def drawMode(self, event):
        if self.__draw == 1:
            self.__draw = 0
        else:
            self.__draw = 1


    def generateTableCommon(self):
        w = round(self.__topLevel.getTopLevelDimensions()[0]/40*self.__puff)
        h = round(self.__topLevel.getTopLevelDimensions()[1]/self.__Y*self.__piff)

        w2 = round(self.__topLevel.getTopLevelDimensions()[0]/40*self.__puff)*7.5


        for Y in range(self.__index ,self.__Y+self.__index):
            f1 = None
            f2 = None
            e1 = None
            e2 = None


            self.__topLevelWindow.bind("<KeyRelease>", self.checkEntry)

            if self.alreadyDone == False:
                self.__soundPlayer.playSound("Pong")
                f1 = Frame(self.__intTheMiddle, width=w2, height=h, bg=self.__colors.getColor("boxBackNormal"))
                f1.pack_propagate(False)
                f1.place(x=0, y=h * (Y - self.__index))

                f2 = Frame(self.__intTheMiddle, width=w2, height=h, bg=self.__colors.getColor("boxBackNormal"))
                f2.pack_propagate(False)
                f2.place(x=w2, y=h * (Y - self.__index))

                self.__colorFrames[str(Y-self.__index)] = [f1, f2]
                eV1 = StringVar()
                eV2 = StringVar()
                e1 = Entry(f1, name=(str(Y-self.__index)+",0"), textvariable = eV1, font=self.__smallFont, justify = "center")
                e1.pack(fill=BOTH)
                e2 = Entry(f2, name=(str(Y-self.__index)+",1"), textvariable = eV2, font=self.__smallFont, justify = "center")
                e2.pack(fill=BOTH)
                self.__colorEntries[str(Y-self.__index)] = [e1, e2]
                self.__colorEntryVar[str(Y-self.__index)] = [eV1, eV2]

            else:
                f1 = self.__colorFrames[str(Y-self.__index)][0]
                f2 = self.__colorFrames[str(Y-self.__index)][1]
                eV1 = self.__colorEntryVar[str(Y-self.__index)][0]
                eV2 = self.__colorEntryVar[str(Y-self.__index)][1]
                e1 = self.__colorEntries[str(Y-self.__index)][0]
                e2 = self.__colorEntries[str(Y-self.__index)][1]

            eV1.set(self.__colorTable[Y][0])
            eV2.set(self.__colorTable[Y][1])
            self.colorEntry(e1, eV1.get())
            self.colorEntry(e2, eV2.get())

            for X in range(0,40):
                f = None
                b = None

                if self.alreadyDone == False:
                    if (X<4 or X>35):
                        f = Frame(self.__theField, width=w, height=h, bg=self.__colors.getColor("fontDisabled"))
                    else:
                        f = Frame(self.__theField, width=w, height=h, bg=self.__colors.getColor("boxBackNormal"))
                    f.pack_propagate(False)
                    f.place(x=w*X, y=h*(Y-self.__index))
                    self.__motion = False
                    self.__frames[str(X) + "," + str(Y-self.__index)] = f

                    b = Button(f, name=(str(X) + "," + str(Y)),
                               relief=GROOVE, activebackground=self.__colors.getColor("highLight"))

                    b.bind("<Button-1>", self.clickedCommon)
                    b.bind("<Button-3>", self.clickedCommon)

                    b.bind("<Enter>", self.enterCommon)
                    b.pack_propagate(False)
                    b.pack(fill=BOTH)

                    self.__buttons[str(X) + "," + str(Y-self.__index)] = b
                else:
                    f = self.__frames[str(X) + "," + str(Y-self.__index)]
                    b = self.__buttons[str(X) + "," + str(Y-self.__index)]
                    #b.config(name=(str(X) + "," + str(Y)))

                if self.__table[Y][X] == "1":
                    b.config(bg=self.__colors.getColor("boxFontNormal"))
                else:
                    if (X<4 or X>35):
                        b.config(bg=self.__colors.getColor("fontDisabled"))
                    else:
                        b.config(bg=self.__colors.getColor("boxBackNormal"))



        self.alreadyDone = True
        self.redrawCanvas()

    def checkEntry(self, event):
        name = str(event.widget).split(".")[-1]
        if name in ["heightEntry", "indexEntry", "pfName"]:
            return

        Y = int(name.split(",")[0])
        X = int(name.split(",")[1])
        realY=Y+self.__index

        self.__colorEntryVar[str(Y)][X].set(self.__colorEntryVar[str(Y)][X].get().upper())

        if (len(self.__colorEntryVar[str(Y)][X].get())>3):
            self.__colorEntryVar[str(Y)][X].set(self.__colorEntryVar[str(Y)][X].get()[:3])
            return

        entry = event.widget
        if (len(self.__colorEntryVar[str(Y)][X].get())<3):
            entry.config(bg=self.__colors.getColor("boxBackUnSaved"), fg=self.__colors.getColor("boxFontUnSaved"))
            return

        try:
            num = int(self.__colorEntryVar[str(Y)][X].get().replace("$", "0x"), 16)
        except:
            entry.config(bg=self.__colors.getColor("boxBackUnSaved"), fg=self.__colors.getColor("boxFontUnSaved"))
            return

        num = int("0x"+self.__colorEntryVar[str(Y)][X].get()[2], 16)
        if (num%2 == 1):
            self.__colorEntryVar[str(Y)][X].set(self.__colorEntryVar[str(Y)][X].get()[:2]+hex(num-1).replace("0x","").upper())

        self.colorEntry(event.widget, self.__colorEntryVar[str(Y)][X].get())
        self.__colorTable[realY][X] = self.__colorEntryVar[str(Y)][X].get()

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

    def enterCommon(self, event):
        if self.__draw:
            self.clickedCommon(event)

    def redrawCanvas(self):
        if self.firstLoad == True:
            self.firstLoad = False
        else:
            self.changed = True

        if self.alreadyDone == True:
            w = round(self.__canvas.winfo_width()/40)
            h = round(self.__canvas.winfo_height()/42)

            self.__canvas.clipboard_clear()
            for Y in range(0,42):
                colorPF = self.__colorTable[Y+self.__index][0]
                colorBK = self.__colorTable[Y+self.__index][1]
                #canvas.create_rectangle(x1, y1, x2, y2, **kwargs)
                self.__canvas.create_rectangle(0, Y*h, self.__canvas.winfo_width(), (Y+1)*h, outline = "",
                                               fill=self.__colorDict.getHEXValueFromTIA(colorBK))

                for X in range(0,40):
                    if self.__table[Y+self.__index][X] == "1":
                        self.__canvas.create_rectangle(X*w, Y * h, (X+1)*w, (Y + 1) * h, outline="",
                                                       fill=self.__colorDict.getHEXValueFromTIA(colorPF))



    def clickedCommon(self, event):
        button = 0
        try:
            button = int(str(event).split(" ")[3].split("=")[1])
        except:
            if self.__ctrl:
                button = 3
            else:
                button = 1

        if self.__ctrl==False and button == 3:
            return

        name = str(event.widget).split(".")[-1]
        X = int(name.split(",")[0])
        Y = int(name.split(",")[1])+self.__index

        self.changeColor(X,Y, button)

        if (X>3 and X<36):
            for pair in self.__logicalX:
                from copy import deepcopy
                if (X in pair):
                    pairCopy = deepcopy(pair)
                    pairCopy.remove(X)
                    self.changeColor(pairCopy[0], Y, button)

    def changeColor(self, X, Y, button):
        color = ""

        if self.__draw == True:
            if self.__ctrl == False:
                self.__table[Y][X] = "1"
                color = self.__colors.getColor("boxFontNormal")
            else:
                self.__table[Y][X] = "0"
                if (X < 4 or X > 35):
                    color = self.__colors.getColor("fontDisabled")
                else:
                    color = self.__colors.getColor("boxBackNormal")


        else:
            if self.__ctrl:
                if button == 1:
                    self.__table[Y][X] = "1"
                    color = self.__colors.getColor("boxFontNormal")
                else:
                    self.__table[Y][X] = "0"
                    if (X < 4 or X > 35):
                        color = self.__colors.getColor("fontDisabled")
                    else:
                        color = self.__colors.getColor("boxBackNormal")
            else:
                if (self.__table[Y][X] == "0"):
                    self.__table[Y][X] = "1"
                    color = self.__colors.getColor("boxFontNormal")
                else:
                    self.__table[Y][X] = "0"
                    if (X < 4 or X > 35):
                        color = self.__colors.getColor("fontDisabled")
                    else:
                        color = self.__colors.getColor("boxBackNormal")

        self.__buttons[str(X)+","+str(Y-self.__index)].config(bg=color)
        self.redrawCanvas()

    def focusIn(self, event):
        self.focused = event.widget

    def focusOut(self, event):
        self.focused = None