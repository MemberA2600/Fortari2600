from tkinter import *
from SubMenu import SubMenu
from threading import Thread

class MenuMaker:

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

        self.__validFName = True

        self.__ctrl = False
        self.__middle = False
        self.__draw = 0
        self.__selected = 0
        self.__current  = 0
        self.__selectedSegment = 0

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize*0.65), False, False, False)
        self.__bigFont = self.__fontManager.getFont(int(self.__fontSize*1.15), False, False, False)
        self.__bigFont2 = self.__fontManager.getFont(int(self.__fontSize*1.5), False, False, False)

        self.__maxWidth = 48
        self.__maxNumberOfItems = 31

        self.__invalids = {}

        self.__items = 1

        self.__segments = [[0, self.__items-1]]
        self.__lineHeight = 1

        self.__colorValues = [
            ["$02", "$04", "$06", "$08", "$08", "$06", "$04", "$02"],
            ["$16", "$18", "$1a", "$1c", "$1c", "$1a", "$18", "$16"],
            ["$42", "$44", "$46", "$48", "$48", "$46", "$44", "$42"],
        ]


        self.__sizes = [self.__screenSize[0] / 2, self.__screenSize[1] //1.25 - 55]
        self.__window = SubMenu(self.__loader, "menuMaker", self.__sizes[0], self.__sizes[1], None, self.__addElements,
                                1)
        self.dead = True

    def __closeWindow(self):
        if self.changed == True:
            answer = self.__fileDialogs.askYesNoCancel("notSavedFile", "notSavedFileMessage")
            if answer == "Yes":
                self.__saveMenu()
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

        self.__finishedThem = [False, False, False, False]

        self.__canvasFrame = Frame(self.__topLevelWindow, width=self.__sizes[0],
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = round(self.__sizes[1]//2)
                                   )
        self.__canvasFrame.pack_propagate(False)
        self.__canvasFrame.pack(side=TOP, anchor=N, fill=X)

        self.__canvas = Canvas(self.__canvasFrame, bg="black", bd=0,
                               width=99999,
                               height=99999
                               )
        while self.__canvas.winfo_width() < 2:
            self.__canvas.pack_propagate(False)
            self.__canvas.pack(side=TOP, anchor=N, fill=BOTH)

        divider = 6

        self.__editorFrame = Frame(self.__topLevelWindow, width=self.__sizes[0],
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = round(self.__sizes[1]//divider*1.5)
                                   )
        self.__editorFrame.pack_propagate(False)
        self.__editorFrame.pack(side=TOP, anchor=N, fill=X)

        self.__editorPixelsFrame = Frame(self.__editorFrame, width=round(self.__sizes[0]*0.8),
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = round(self.__sizes[1]//divider)
                                   )

        while self.__editorPixelsFrame.winfo_width() < 2:
            self.__editorPixelsFrame.pack_propagate(False)
            self.__editorPixelsFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__editorColorsFrame = Frame(self.__editorFrame, width=round(self.__sizes[0]*0.8),
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = round(self.__sizes[1]//divider)
                                   )
        while self.__editorColorsFrame.winfo_width() < 2:
            self.__editorColorsFrame.pack_propagate(False)
            self.__editorColorsFrame.pack(side=LEFT, anchor=E, fill=BOTH)

        t1 = Thread(target=self.createEditorFrame)
        t1.daemon = True
        t1.start()

        t2 = Thread(target=self.createColorsFrame)
        t2.daemon = True
        t2.start()

        self.__editorItemSetterFrame = Frame(self.__topLevelWindow, width=round(self.__sizes[0]),
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = round(self.__sizes[1]//16)
                                   )

        while self.__editorItemSetterFrame.winfo_width() < 2:
            self.__editorItemSetterFrame.pack_propagate(False)
            self.__editorItemSetterFrame.pack(side=TOP, anchor=N, fill=X)

        self.__backImage = self.__loader.io.getImg("backwards", None)
        self.__forImage = self.__loader.io.getImg("forwards", None)

        """
        t3 = Thread(target=self.createSetterMenu)
        t3.daemon = True
        t3.start()
        """

        divider2 = 14
        self.createSetterMenu()

        self.__bottomFrame = Frame(self.__topLevelWindow, width=round(self.__sizes[0]),
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = round(self.__sizes[1]//(divider2+2))
                                   )
        while self.__bottomFrame.winfo_width() < 2:
            self.__bottomFrame.pack_propagate(False)
            self.__bottomFrame.pack(side=TOP, anchor=N, fill=X)

        self.__segmentsFrame = Frame(self.__topLevelWindow, width=round(self.__sizes[0]),
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = round(self.__sizes[1]//divider2//2)
                                   )
        while self.__segmentsFrame.winfo_width() < 2:
            self.__segmentsFrame.pack_propagate(False)
            self.__segmentsFrame.pack(side=TOP, anchor=N, fill=X)

        self.__createSegmentsFrame()

        """
        t4 = Thread(target=self.createBottomElements)
        t4.daemon = True
        t4.start()
        """

        self.__buttonFrame = Frame(self.__topLevelWindow, width=round(self.__sizes[0]),
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = round(self.__sizes[1])
                                   )
        while self.__buttonFrame.winfo_width() < 2:
            self.__buttonFrame.pack_propagate(False)
            self.__buttonFrame.pack(side=TOP, anchor=N, fill=BOTH)

        self.createBottomElements()
        self.createBottomButtons()

        loop = Thread(target=self.__loop)
        loop.daemon = True
        loop.start()

        self.__topLevelWindow.bind("<KeyPress-Control_L>", self.shiftON)
        self.__topLevelWindow.bind("<KeyRelease-Control_L>", self.shiftOff)
        self.__topLevelWindow.bind("<KeyPress-Control_R>", self.shiftON)
        self.__topLevelWindow.bind("<KeyRelease-Control_R>", self.shiftOff)
        self.__topLevelWindow.bind("<Button-2>", self.drawMode)

        self.__topLevelWindow.bind("<KeyPress-Up>", self.up)
        self.__topLevelWindow.bind("<KeyPress-Down>", self.down)

    def up(self, event):
        self.__selected -=1
        if self.__selected < 0:
           self.__selected = self.__items - 1

        self.__redrawCanvas()

    def down(self, event):
        self.__selected += 1
        if self.__selected > self.__items - 1:
            self.__selected = 0

        self.__redrawCanvas()


    def __createSegmentsFrame(self):
        self.__segmentsLabel = Label(self.__segmentsFrame,
                                     text=self.__dictionaries.getWordFromCurrentLanguage("segments") + " ",
                                     font=self.__smallFont, fg=self.__colors.getColor("font"),
                                     bg=self.__colors.getColor("window"), justify=CENTER
                                     )

        self.__segmentsLabel.pack_propagate(False)
        self.__segmentsLabel.pack(side=LEFT, anchor=E, fill=Y)

        self.__segmentsText = StringVar()
        self.__segmentsText.set("0-0;")

        self.__segmentsEntry = Entry(self.__segmentsFrame, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                 width=999999,
                                 fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                 textvariable=self.__segmentsText, name="segmentEntry",
                                 font=self.__smallFont)
        self.__segmentsEntry.pack_propagate(False)
        self.__segmentsEntry.pack(side=LEFT, fill=BOTH)

        self.__segmentsEntry.bind("<KeyRelease>", self.checkIfBullShit)
        self.__segmentsEntry.bind("<FocusOut>", self.checkIfBullShit)
        self.__invalids[self.__segmentsEntry] = False

    def checkIfBullShit(self, event):
        import re
        regex1 = r";{0,1}[0-9]{1,2}\-[0-9]{1,2};{0,1}"
        regex2 = r"[0-9]{1,2}\-[0-9]{1,2}"
        regex3 = r"[a-zA-Z]"

        self.__segmentsText.set(self.__segmentsText.get().replace(" ", ""))
        self.__segmentsText.set(re.sub(regex3, "", self.__segmentsText.get()))

        all = re.findall(regex1, self.__segmentsText.get())
        if len(all) == 0:
            self.setSegmentsInvalid()
            return

        all = self.__segmentsText.get().split(";")
        number = 0
        temp = []
        for item in all:
            if item != "" :
                if len(re.findall(regex2, item)) == 0:
                    self.setSegmentsInvalid()
                    return
                else:
                    item = item.split("-")
                    temp.append([int(item[0]), int(item[1])])
                    number+=1

        if number > 6:
           self.setSegmentsInvalid()
           return

        if "FocusOut" in str(event) or event == False or event == None:
            counter = -1
            for item in temp:
                counter += 1
                if len(temp) == 1:
                    item[0] = 0
                    item[1] = self.__items-1
                elif item == temp[0]:
                    item[0] = 0
                elif item == temp[-1]:
                    item[-1] = self.__items-1
                    if item[0] != temp[-2][1] + 1:
                       item[0] = temp[-2][1] + 1

                else:
                    if item[0] != temp[counter-1][1] + 1:
                       item[0] =  temp[counter-1][1] + 1

                    if item[1] != temp[counter+1][0] - 1:
                       item[1] =  temp[counter+1][0] - 1

        if temp[0][0] != 0:
            self.setSegmentsInvalid()
            return
        elif temp[-1][1] != self.__items - 1:
            self.setSegmentsInvalid()
            return

        counter = 0
        for item in temp[1:-1]:
            counter+=1
            if item[0] != temp[counter-1][1] + 1 or item[1] != temp[counter+1][0] - 1:
                self.setSegmentsInvalid()
                return

            if item[0] < 1 or item[1] > self.__items - 2:
                self.setSegmentsInvalid()
                return

        self.__segmentsEntry.config(
            bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
            fg=self.__loader.colorPalettes.getColor("boxFontNormal")
        )

        from copy import deepcopy

        self.__segments = deepcopy(temp)
        txtTemp = []

        for item in temp:
            txtTemp.append(str(item[0])+"-"+str(item[1]))

        txt = ';'.join(txtTemp)
        if len(temp) == 1:
           txt+=";"

        self.__segmentsText.set(txt)
        if event != False:
            self.__redrawCanvas()
            if event != None:
                self.changed = True

    def setSegmentsInvalid(self):
        self.__segmentsEntry.config(
            bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
            fg=self.__loader.colorPalettes.getColor("boxFontUnSaved")
        )

    def createBottomButtons(self):
        self.__topFrame = Frame(self.__buttonFrame, width=round(self.__sizes[0]),
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = self.__buttonFrame.winfo_height() // 3)

        while self.__topFrame.winfo_width() < 2:
            self.__topFrame.pack_propagate(False)
            self.__topFrame.pack(side=TOP, anchor=N, fill=X)

        self.__botFrame = Frame(self.__buttonFrame, width=round(self.__sizes[0]),
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = self.__buttonFrame.winfo_height() // 3 * 2)

        while self.__botFrame.winfo_width() < 2:
            self.__botFrame.pack_propagate(False)
            self.__botFrame.pack(side=TOP, anchor=N, fill=X)


        self.Button1Frame = Frame(self.__botFrame, width=round(self.__sizes[0]*0.33),
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = self.__bottomFrame.winfo_height())

        while self.Button1Frame.winfo_width() < 2:
            self.Button1Frame.pack_propagate(False)
            self.Button1Frame.pack(side=LEFT, anchor=E, fill=Y)

        self.Button2Frame = Frame(self.__botFrame, width=round(self.__sizes[0]*0.33),
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = self.__bottomFrame.winfo_height())

        while self.Button2Frame.winfo_width() < 2:
            self.Button2Frame.pack_propagate(False)
            self.Button2Frame.pack(side=LEFT, anchor=E, fill=Y)

        self.Button3Frame = Frame(self.__botFrame, width=round(self.__sizes[0]),
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = self.__bottomFrame.winfo_height())

        while self.Button3Frame.winfo_width() < 2:
            self.Button3Frame.pack_propagate(False)
            self.Button3Frame.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__openImage = self.__loader.io.getImg("open", None)
        self.__saveImage = self.__loader.io.getImg("save", None)
        self.__testImage = self.__loader.io.getImg("stella", None)

        self.__openImageButton = Button(self.Button1Frame, height=9999, width=9999,
                   bg=self.__loader.colorPalettes.getColor("window"),
                   image = self.__openImage,
                   state=DISABLED, command = self.__openMenu
                   )
        self.__openImageButton.pack_propagate(False)
        self.__openImageButton.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__saveImageButton = Button(self.Button2Frame, height=9999, width=9999,
                   bg=self.__loader.colorPalettes.getColor("window"),
                   image = self.__saveImage,
                   state=DISABLED, command = self.__saveMenu
                   )
        self.__saveImageButton.pack_propagate(False)
        self.__saveImageButton.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__testImageButton = Button(self.Button3Frame, height=9999, width=9999,
                   bg=self.__loader.colorPalettes.getColor("window"),
                   image = self.__testImage,
                   state=DISABLED, command = self.__testMenu
                   )
        self.__testImageButton.pack_propagate(False)
        self.__testImageButton.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__frameNumLabel = Label(self.__topFrame,
                                   text=self.__dictionaries.getWordFromCurrentLanguage("name")+" ",
                                   font=self.__smallFont, fg=self.__colors.getColor("font"),
                                   bg=self.__colors.getColor("window"), justify=CENTER
                                   )

        self.__frameNumLabel.pack_propagate(False)
        self.__frameNumLabel.pack(side=LEFT, anchor=E, fill=Y)

        self.__nameVal = StringVar()
        self.__nameVal.set("Serve_The_Hive")

        self.__nameEntry = Entry(self.__topFrame, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                   width=999999,
                                   fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                   textvariable = self.__nameVal, name = "nameEntry",
                                   font=self.__smallFont)
        self.__nameEntry.pack_propagate(False)
        self.__nameEntry.pack(side=LEFT, fill=BOTH)

        self.__nameEntry.bind("<KeyRelease>", self.checkIfValidFileName)
        self.__nameEntry.bind("<FocusOut>", self.checkIfValidFileName)
        self.__invalids[self.__nameEntry] = False


    def checkIfValidFileName(self, event):
        try:
            name = str(event.widget).split(".")[-1]
        except:
            name = "landscape"

        if self.__loader.io.checkIfValidFileName(self.__nameVal.get()) == False or (" " in self.__nameVal.get()):
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

    def __openMenu(self):
        compatibles = {
            "common": ["common"]
        }

        if self.changed == True:
            answer = self.__fileDialogs.askYesNoCancel("notSavedFile", "notSavedFileMessage")
            if answer == "Yes":
                self.__saveMenu()
            elif answer == "Cancel":
                self.__topLevelWindow.deiconify()
                self.__topLevelWindow.focus()
                return
        fpath = self.__fileDialogs.askForFileName("openFile", False, ["a26", "*"],
                                                  self.__loader.mainWindow.projectPath + "menus/")

        if fpath == "":
            return


        try:
        #if True:
            f = open(fpath, "r")
            lines = f.read().replace("\r", "").split("\n")
            f.close()

            if lines[0].replace("\n", "").replace("\r", "") not in compatibles[self.__loader.virtualMemory.kernel]:
                if self.__fileDialogs.askYesNoCancel("differentKernel", "differentKernelMessage") == "No":
                    self.__topLevelWindow.deiconify()
                    self.__topLevelWindow.focus()
                    return


            self.__items = int(lines[1])
            self.__frameNum.set(lines[1])

            self.__lineHeight = int(lines[2])
            self.__lineHeightNum.set(lines[2])

            self.__backColor[0] = lines[3]
            self.__backColorEntry.setValue(lines[3])

            self.__itemNum.set("0")

            self.__segmentsText.set(lines[4])
            segmentSource = lines[4].split(";")
            self.__segments = []
            for item in segmentSource:
                if item != '':
                   item = item.replace("\r","").split("-")
                   self.__segments.append([int(item[0]), int(item[1])])

            from copy import deepcopy

            for lineNum in range(5, 8):
                line = lines[lineNum].split(" ")
                self.__colorValues[lineNum-5] = deepcopy(line)

            for lineNum in range(8, 8 + self.__maxNumberOfItems*8):
                line = lines[lineNum]
                trueLineNum = lineNum - 8
                itemNum = trueLineNum // 8
                lineNumInItem = trueLineNum%8
                for charNum in range(0, len(line)):
                    self.__dataLines[itemNum][lineNumInItem][charNum] = int(line[charNum])

            self.__soundPlayer.playSound("Success")
            self.redrawAllButtons()
            self.changed = False
            self.checkIfBullShit(None)

            self.__nameVal.set(".".join(fpath.split("/")[-1].split(".")[:-1]))

        except Exception as e:
            self.__fileDialogs.displayError("unableToOpenFile", "unableToOpenFileMessage", None, str(e))

        self.__topLevelWindow.deiconify()
        self.__topLevelWindow.focus()

    def __saveMenu(self):
        name1 = self.__loader.mainWindow.projectPath+"menus/"+self.__nameVal.get()+".a26"
        name2 = self.__loader.mainWindow.projectPath+"menus/"+self.__nameVal.get()+".asm"

        text =  self.__loader.virtualMemory.kernel  + "\n" +\
                str(self.__items)                   + "\n" +\
                str(self.__lineHeight)              + "\n" +\
                str(self.__backColor[0])            + "\n"

        for item in self.__segments:
            text += str(item[0])+"-"+str(item[1])+";"

        text = text[:-1]+"\n"
        for line in self.__colorValues:
            text += " ".join(line) + "\n"

        bigText = ""
        for YLine in self.__dataLines:
            for Xline in YLine:
                for item in Xline:
                    text    += str(item)
                    bigText += str(item)
                text    += "\n"
                bigText += "\n"
        f = open(name1, "w")
        f.write(text)
        f.close()

        self.__topLevelWindow.deiconify()
        self.__topLevelWindow.focus()

        largest = 0
        for item in self.__segments:
            diff = item[1] - item[0]
            if diff > largest: largest = diff

        #comments = "* Items="+str(self.__items)+"\n* Largest="+str(largest)+"\n* LineHeight=" + str(self.__lineHeight)+"\n"
        comments = "* Items=" + str(self.__items) + "\n* Largest=" + str(largest) + "\n"

        from Compiler import Compiler

        f = open(name2, "w")
        f.write(
            comments +\
            Compiler(
                self.__loader, self.__loader.virtualMemory.kernel, "menuASM", [
                    bigText,
                    self.__colorValues,
                    self.__items,
                    self.__segmentsText.get(),
                    self.__segments,
                    "NTSC", "##NAME##"
                ]
            ).converted
        )
        f.close()

        self.__soundPlayer.playSound("Success")
        self.changed = False

    def __testMenu(self):
        t = Thread(target=self.__testThread)
        t.daemon = True
        t.start()

    def __testThread(self):
        from Compiler import Compiler

        bigText = ""
        for YLine in self.__dataLines:
            for Xline in YLine:
                for item in Xline:
                    bigText += str(item)
                bigText += "\n"

        largest = 0
        for item in self.__segments:
            diff = item[1] - item[0]
            if diff > largest: largest = diff

        Compiler(
            self.__loader, self.__loader.virtualMemory.kernel, "testMenu", [
                bigText,
                self.__colorValues,
                self.__items,
                self.__segmentsText.get(),
                self.__segments,
                "NTSC", "TestMenu", ["Tile1_1"],
                [self.__items, largest]
            ])

    def createBottomElements(self):
        self.theFirstEntryFrame = Frame(self.__bottomFrame, width=round(self.__sizes[0]*0.5),
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = self.__bottomFrame.winfo_height())

        while self.theFirstEntryFrame.winfo_width() < 2:
            self.theFirstEntryFrame.pack_propagate(False)
            self.theFirstEntryFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__frameNumLabel = Label(self.theFirstEntryFrame,
                                   text=self.__dictionaries.getWordFromCurrentLanguage("numItem")+": ",
                                   font=self.__smallFont, fg=self.__colors.getColor("font"),
                                   bg=self.__colors.getColor("window"), justify=CENTER
                                   )

        self.__frameNumLabel.pack_propagate(False)
        self.__frameNumLabel.pack(side=LEFT, anchor=E, fill=Y)

        self.__frameNum = StringVar()
        self.__frameNum.set("1")

        self.__frameNumEntry = Entry(self.theFirstEntryFrame, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                 width=99999999,
                                 fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                 textvariable=self.__frameNum, name="frameNum",
                                 state=DISABLED, font=self.__bigFont, justify=CENTER,
                                 command=None)
        self.__frameNumEntry.pack_propagate(False)
        self.__frameNumEntry.pack(fill=BOTH, side=TOP, anchor=N)

        self.__frameNumEntry.bind("<KeyRelease>", self.__frameEntryCheck)
        self.__frameNumEntry.bind("<FocusOut>", self.__frameEntryCheck)
        self.__invalids[self.__frameNumEntry] = False


        self.theSecondEntryFrame = Frame(self.__bottomFrame, width=round(self.__sizes[0]*0.5),
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = self.__bottomFrame.winfo_height())

        while self.theSecondEntryFrame.winfo_width() < 2:
            self.theSecondEntryFrame.pack_propagate(False)
            self.theSecondEntryFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__backColorLabel = Label(self.theSecondEntryFrame,
                                   text=self.__dictionaries.getWordFromCurrentLanguage("frameColor")+" ",
                                   font=self.__smallFont, fg=self.__colors.getColor("font"),
                                   bg=self.__colors.getColor("window"), justify=CENTER
                                   )

        self.__backColorLabel.pack_propagate(False)
        self.__backColorLabel.pack(side=LEFT, anchor=E, fill=Y)

        from HexEntry import HexEntry


        self.__backColor = ["$00"]
        self.__backColorEntry = HexEntry(self.__loader, self.theSecondEntryFrame, self.__colors,
                            self.__colorDict, self.__normalFont, self.__backColor, 0, None, self.justReDraw)

        self.theThirdEntryFrame = Frame(self.__bottomFrame, width=round(self.__sizes[0]*0.3),
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = self.__bottomFrame.winfo_height())

        self.__invalids[self.__backColorEntry.getEntry()] = False


        """
        while self.theThirdEntryFrame.winfo_width() < 2:
            self.theThirdEntryFrame.pack_propagate(False)
            self.theThirdEntryFrame.pack(side=LEFT, anchor=E, fill=BOTH)
        """

        self.__lineHeightLabel = Label(self.theThirdEntryFrame,
                                   text=self.__dictionaries.getWordFromCurrentLanguage("lineHeight")+" ",
                                   font=self.__smallFont, fg=self.__colors.getColor("font"),
                                   bg=self.__colors.getColor("window"), justify=CENTER
                                   )

        self.__lineHeightLabel.pack_propagate(False)
        self.__lineHeightLabel.pack(side=LEFT, anchor=E, fill=Y)

        self.__lineHeightNum = StringVar()
        self.__lineHeightNum.set("1")

        self.__lineHeightNumEntry = Entry(self.theThirdEntryFrame, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                 width=99999999,
                                 fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                 textvariable=self.__lineHeightNum, name="lineHeight",
                                 state=DISABLED, font=self.__bigFont, justify=CENTER,
                                 command=None)
        self.__lineHeightNumEntry.pack_propagate(False)
        self.__lineHeightNumEntry.pack(fill=BOTH, side=TOP, anchor=N)

        self.__lineHeightNumEntry.bind("<KeyRelease>", self.__lineHCheck)
        self.__lineHeightNumEntry.bind("<FocusOut>", self.__lineHCheck)

        self.__finishedThem[3] = True

    def __lineHCheck(self, event):
        if self.__checkIfNumeric(self.__lineHeightNum.get()) == False:
            self.__lineHeightNumEntry.config(
                bg = self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                fg=self.__loader.colorPalettes.getColor("boxFontUnSaved")
            )
        else:
            self.__lineHeightNumEntry.config(
                bg = self.__loader.colorPalettes.getColor("boxBackNormal"),
                fg=self.__loader.colorPalettes.getColor("boxFontNormal")
            )

            num = int(self.__lineHeightNum.get())
            if num < 1: num = 1
            elif num > 6: num = 6

            self.__lineHeight = num
            self.__lineHeightNum.set(str(self.__lineHeight))

            if self.__items > self.__maxNumberOfItems // self.__lineHeight:
               self.__items = self.__maxNumberOfItems // self.__lineHeight
               self.__itemNum.set(str(self.__maxNumberOfItems // self.__lineHeight))

               if self.__current > self.__items - 1:
                  self.__current = self.__items - 1
                  self.__itemNum.set(str(self.__current))

            self.redrawAllButtons()
            self.changed = True


    def justReDraw(self, event):
        self.__redrawCanvas()

    def __frameEntryCheck(self, event):
        if self.__checkIfNumeric(self.__frameNum.get()) == False:
            self.__frameNumEntry.config(
                bg = self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                fg=self.__loader.colorPalettes.getColor("boxFontUnSaved")
            )
        else:
            self.__frameNumEntry.config(
                bg = self.__loader.colorPalettes.getColor("boxBackNormal"),
                fg=self.__loader.colorPalettes.getColor("boxFontNormal")
            )

            num = int(self.__frameNum.get())
            if   num < 1: num = 1
            elif num > self.__maxNumberOfItems // self.__lineHeight:
                num = self.__maxNumberOfItems // self.__lineHeight

            self.__frameNum.set(str(num))
            self.__items = num

            if self.__current > num-1:
               self.__current = num-1
               self.__itemNum.set(str(num-1))

            self.redrawAllButtons()
            self.changed = True

    def __loop(self):

        from time import sleep

        while self.dead == False and self.__loader.mainWindow.dead == False:
            try:
                if self.__theyAreDisabled == True:
                    doIt = True

                    for item in self.__finishedThem:
                        if item == False: doIt == False

                    if doIt == True:
                        for theY in range(0,8):
                            for button in self.__buttons[theY]:
                                button.config(state = NORMAL)
                            for entry in self.__entries[theY]:
                                entry.changeState(NORMAL)


                        self.__textEntry.config(state = NORMAL)
                        self.__generateTB.config(state = NORMAL)
                        self.__frameNumEntry.config(state = NORMAL)
                        self.__lineHeightNumEntry.config(state = NORMAL)
                        self.__openImageButton.config(state = NORMAL)
                        self.__testImageButton.config(state = NORMAL)
                        self.__theyAreDisabled = False
                        #self.__redrawCanvas()
                else:
                    if self.__items > 1:
                       self.__itemEntry.config(state  = NORMAL)
                       self.__buttonFor.config(state  = NORMAL)
                       self.__buttonPrev.config(state = NORMAL)
                    else:
                       self.__itemEntry.config(state  = DISABLED)
                       self.__buttonFor.config(state  = DISABLED)
                       self.__buttonPrev.config(state = DISABLED)

                    if self.changed == True and self.__validFName == True:
                       self.__saveImageButton.config(state = NORMAL)
                    else:
                       self.__saveImageButton.config(state = DISABLED)

            except Exception as e:
                #print(str(e))
                pass

            sleep(0.05)

    def createEditorFrame(self):

        self.__dataLines = []
        for num in range(0,self.__maxNumberOfItems):
            self.__dataLines.append([])
            for theY in range(0,8):
                self.__dataLines[-1].append([])
                for theX in range(0,self.__maxWidth):
                    self.__dataLines[-1][-1].append(0)

        w = self.__editorPixelsFrame.winfo_width() // self.__maxWidth
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

            for theX in range(0,self.__maxWidth):
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

        self.__finishedThem[0] = True

    def createColorsFrame(self):
        from HexEntry import HexEntry

        w = self.__editorColorsFrame.winfo_width() // 3
        h = self.__editorColorsFrame.winfo_height() // 8

        self.__entries = []
        self.__entryVals = []

        for theY in range(0,8):
            self.__entries.append([])
            self.__entryVals.append([self.__colorValues[0][theY],
                                     self.__colorValues[1][theY],
                                     self.__colorValues[2][theY]])

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
                f0.pack(side=LEFT, anchor=E, fill=Y)

            f1 = Frame(rowF, height = h, width = w,
                            bg = self.__loader.colorPalettes.getColor("window"))
            while f1.winfo_width() < 2:
                f1.pack_propagate(False)
                f1.pack(side=LEFT, anchor=E, fill=Y)

            f2 = Frame(rowF, height = h, width = w,
                            bg = self.__loader.colorPalettes.getColor("window"))
            while f2.winfo_width() < 2:
                f2.pack_propagate(False)
                f2.pack(side=LEFT, anchor=E, fill=BOTH)

            sp1Color = HexEntry(self.__loader, f0, self.__colors,
                       self.__colorDict, self.__miniFont, self.__entryVals[-1], 0, None, self.__setColorData)

            sp2Color = HexEntry(self.__loader, f1, self.__colors,
                       self.__colorDict, self.__miniFont, self.__entryVals[-1], 1, None, self.__setColorData)

            sp3Color = HexEntry(self.__loader, f2, self.__colors,
                       self.__colorDict, self.__miniFont, self.__entryVals[-1], 2, None, self.__setColorData)


            self.__entries[-1].append(sp1Color)
            self.__entries[-1].append(sp2Color)
            self.__entries[-1].append(sp3Color)

            sp1Color.setValue(self.__colorValues[0][theY])
            sp2Color.setValue(self.__colorValues[1][theY])
            sp3Color.setValue(self.__colorValues[2][theY])

            sp1Color.changeState(DISABLED)
            sp2Color.changeState(DISABLED)
            sp3Color.changeState(DISABLED)

        self.__finishedThem[1] = True

    def createSetterMenu(self):

        self.__editorItemSetterFirstFrame = Frame(self.__editorItemSetterFrame, width=round(self.__sizes[0]*0.3),
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = round(self.__sizes[1]//11)
                                   )

        while self.__editorItemSetterFirstFrame.winfo_width() < 2:
            self.__editorItemSetterFirstFrame.pack_propagate(False)
            self.__editorItemSetterFirstFrame.pack(side=LEFT, anchor=E, fill=Y)

        f1 = Frame(self.__editorItemSetterFirstFrame, width=round(self.__sizes[0]*0.3*0.33),
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = round(self.__sizes[1]//11)
                                   )
        while f1.winfo_width() < 2:
            f1.pack_propagate(False)
            f1.pack(side=LEFT, anchor=E, fill=Y)

        f2 = Frame(self.__editorItemSetterFirstFrame, width=round(self.__sizes[0]*0.3*0.33),
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = round(self.__sizes[1]//11)
                                   )
        while f2.winfo_width() < 2:
            f2.pack_propagate(False)
            f2.pack(side=LEFT, anchor=E, fill=Y)

        f3 = Frame(self.__editorItemSetterFirstFrame, width=round(self.__sizes[0]*0.3*0.33),
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = round(self.__sizes[1]//11)
                                   )
        while f3.winfo_width() < 2:
            f3.pack_propagate(False)
            f3.pack(side=LEFT, anchor=E, fill=Y)

        self.__buttonPrev = Button(f1, bg=self.__loader.colorPalettes.getColor("window"),
                                   image=self.__backImage,
                                   width= f1.winfo_width(),
                                   state=DISABLED,
                                   command=self.__decNum)

        self.__buttonPrev.pack_propagate(False)
        self.__buttonPrev.pack(fill=BOTH, side = TOP, anchor = N)

        self.__buttonFor = Button(f3, bg=self.__loader.colorPalettes.getColor("window"),
                                   image=self.__forImage,
                                   width= f3.winfo_width(),
                                   state=DISABLED,
                                   command=self.__nextNum)

        self.__buttonFor.pack_propagate(False)
        self.__buttonFor.pack(fill=BOTH, side = TOP, anchor = N)

        self.__itemNum = StringVar()
        self.__itemNum.set("0")

        self.__itemEntry = Entry(f2, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                   width=99999999,
                                   fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                   textvariable = self.__itemNum, name = "itemNum",
                                   state=DISABLED, font=self.__bigFont, justify = CENTER,
                                   command=None)
        self.__itemEntry.pack_propagate(False)
        self.__itemEntry.pack(fill=BOTH, side = TOP, anchor = N)

        self.__itemEntry.bind("<KeyRelease>", self.__itemEntyCheck)
        self.__itemEntry.bind("<FocusOut>", self.__itemEntyCheck)

        self.__editorItemSetterTextFrame = Frame(self.__editorItemSetterFrame, width=round(self.__sizes[0]*0.35),
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = round(self.__sizes[1]//11)
                                   )

        while self.__editorItemSetterTextFrame.winfo_width() < 2:
            self.__editorItemSetterTextFrame.pack_propagate(False)
            self.__editorItemSetterTextFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__text = StringVar()
        self.__text.set("Zergling")
        self.__textEntry = Entry(self.__editorItemSetterTextFrame, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                   width=99999999,
                                   fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                   textvariable = self.__text, name = "text",
                                   state=DISABLED, font=self.__bigFont,
                                   command=None)
        self.__textEntry.pack_propagate(False)
        self.__textEntry.pack(fill=BOTH, side = TOP, anchor = N)

        self.__lastFrameForButton = Frame(self.__editorItemSetterFrame, width=round(self.__sizes[0]),
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = round(self.__sizes[1]//11)
                                   )

        while self.__lastFrameForButton.winfo_width() < 2:
            self.__lastFrameForButton.pack_propagate(False)
            self.__lastFrameForButton.pack(side=LEFT, anchor=E, fill=Y)


        self.__generateTB = Button(self.__lastFrameForButton, bg=self.__loader.colorPalettes.getColor("window"),
                                   text=self.__dictionaries.getWordFromCurrentLanguage("generateText"),
                                   fg=self.__loader.colorPalettes.getColor("font"),
                                   width= 999999,
                                   state=DISABLED, font = self.__smallFont,
                                   command=self.__generateTXT)

        self.__generateTB.pack_propagate(False)
        self.__generateTB.pack(fill=BOTH, side = TOP, anchor = N)

        self.__textEntry.bind("<KeyRelease>", self.checkTXT)
        self.__textEntry.bind("<FocusOut>", self.checkTXT)

        self.__finishedThem[2] = True

    def checkTXT(self, event):
        txt = self.__text.get()

        if "FocusOut" in str(event):
            while txt[0] == " ":
                print("fuck")
                txt = txt[1:]
            while txt[-1] == " ":
                txt = txt[:-1]

        if len(txt) > self.__maxWidth // 6:
           newLen = self.__maxWidth // 6
           txt = txt[:newLen]

        self.__text.set(txt)

    def __generateTXT(self):
        for theY in range(0,8):
            for theX in range(0,self.__maxWidth):
                self.__dataLines[self.__current][theY][theX] = 0

        txt = self.__text.get().upper()

        tempData = []
        for theY in range(0,8):
            tempData.append([])
            for theX in range(0,self.__maxWidth):
                tempData[-1].append(0)

        index = 0
        for char in txt:

            charData = self.__fontManager.getAtariChar(char)
            if charData == None:
               charData = self.__fontManager.getAtariChar(" ")

            for Y in range(0,8):
                for X in range(0,5):
                    tempData[Y][index+X] = int(charData[Y][X])
            index+=6

        lastOne = self.__maxWidth
        for theX in range(self.__maxWidth-1,-1,-1):
            allOfThemAreSpaces = True
            for theY in range(0, 8):
                if tempData[theY][theX] != 0:
                   allOfThemAreSpaces = False
                   break
            if allOfThemAreSpaces == True:
               lastOne = theX
            else:
                break

        offset = (self.__maxWidth - lastOne) // 2

        for theY in range(0,8):

            for num in range(0, offset):
                tempData[theY].pop(-1)
                tempData[theY].insert(0, 0)

            for theX in range(0,self.__maxWidth):
                self.__dataLines[self.__current][theY][theX] = tempData[theY][theX]

        self.redrawAllButtons()
        self.changed = True

    def redrawAllButtons(self):

        for theY in range(0,8):
            for theX in range(0, self.__maxWidth):
                self.colorTile(theY, theX, self.__dataLines[self.__current][theY][theX])

        self.__redrawCanvas()

    def __decNum(self):
        self.__current -= 1
        if self.__current < 0:
           self.__current = self.__items

        self.__itemNum.set(str(self.__current))

    def __nextNum(self):
        self.__current += 1
        if self.__current > self.__items-1:
           self.__current = 0

        self.__itemNum.set(str(self.__current))


    def __itemEntyCheck(self, event):
        if self.__checkIfNumeric(self.__itemNum.get()) == False:
            self.__itemEntry.config(
                bg = self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                fg=self.__loader.colorPalettes.getColor("boxFontUnSaved")
            )
        else:
            self.__itemEntry.config(
                bg = self.__loader.colorPalettes.getColor("boxBackNormal"),
                fg=self.__loader.colorPalettes.getColor("boxFontNormal")
            )

            if self.__current < 0:
                self.__current = 0
            elif self.__current > self.__items-1:
                self.__current = self.__items-1

            self.__itemNum.set(str(self.__current))

        self.redrawAllButtons()
        self.changed = True


    def __checkIfNumeric(self, val):
        try:
            teszt = int(val)
            return True
        except:
            return False

    def __clicked(self, event):
        for item in self.__finishedThem:
            if item == False: return

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
                self.__dataLines[self.__current][Y][X] = 1 - self.__dataLines[self.__current][Y][X]
            else:
                if   button == 1:
                    self.__dataLines[self.__current][Y][X] = 1
                elif button == 3:
                    self.__dataLines[self.__current][Y][X] = 0
        else:
            if self.__ctrl == False:
                self.__dataLines[self.__current][Y][X] = 1
            else:
                self.__dataLines[self.__current][Y][X] = 0

        self.colorTile(Y, X,  self.__dataLines[self.__current][Y][X])
        self.__redrawCanvas()
        self.changed = True

    def colorTile(self, Y, X, value):
        button = self.__buttons[Y][X]

        if value == 1:
           button.config(bg = self.__loader.colorPalettes.getColor("boxFontNormal"))
        else:
           button.config(bg = self.__loader.colorPalettes.getColor("boxBackNormal"))

    def __enter(self, event):
        for item in self.__finishedThem:
            if item == False: return

        if self.__draw:
            self.__clicked(event)

    def __setColorData(self, event):
        for item in self.__finishedThem:
            if item == False: return

        breaking = False
        for theY in range(0,8):
            for colorNum in range(0,2):
                if self.__entries[theY][colorNum].getEntry() == event.widget:
                    self.__colorValues[colorNum][theY] = self.__entries[theY][colorNum].getValue()
                    self.__entryVals[colorNum][theY]   = self.__entries[theY][colorNum].getValue()
                    breaking = True
                    break
            if breaking == True: break

        self.__redrawCanvas()
        self.changed = True

    def __redrawCanvas(self):
        self.__canvas.clipboard_clear()
        self.__canvas.delete("all")
        self.checkIfBullShit(False)

        backColor = self.__colorDict.getHEXValueFromTIA(self.__backColor[0])
        self.__canvas.config(bg = backColor)

        h = self.__lineHeight * 4

        whyNot = self.__canvas.winfo_height()

        if self.__selected > self.__items - 1:
           self.__selected = self.__items - 1

        counter = -1
        for item in self.__segments:
            counter += 1
            if self.__selected >= item[0] and self.__selected <= item[1]:
               self.__selectedSegment = counter
               break

        if self.__segments[self.__selectedSegment][1] > self.__items:
           subtract = self.__items
        else:
           subtract = self.__segments[self.__selectedSegment][1]

        numOfItem = subtract-self.__segments[self.__selectedSegment][0]

        startY = (whyNot // 2) -(numOfItem * h * 8) // 2
        startX = self.__canvas.winfo_width() // 2 -(4 * self.__maxWidth // 2)

        for itemNum in range(self.__segments[self.__selectedSegment][0], self.__segments[self.__selectedSegment][1]+1):
            for theY in range(0,8):

                if self.__selected == itemNum:
                    thatColor = self.__colorDict.getHEXValueFromTIA(self.__colorValues[1][theY])
                    self.__canvas.create_rectangle(0, startY+(theY * h),
                                                   self.__canvas.winfo_width(),
                                                   startY + ((theY + 1)* h),
                                                   outline="",
                                                   fill=self.__colorDict.getHEXValueFromTIA(
                                                       self.__colorValues[2][theY]
                                                   ))
                else:
                    thatColor = self.__colorDict.getHEXValueFromTIA(self.__colorValues[0][theY])

                for theX in range(0, self.__maxWidth):
                    if self.__dataLines[itemNum][theY][theX] == 1:
                        self.__canvas.create_rectangle(startX + (theX * 4),
                                                       startY + (theY * h),
                                                       startX + ((theX+1) * 4),
                                                       startY + ((theY + 1) * h),
                                                       outline="",
                                                       fill=thatColor)
            startY += ((theY + 1) * h) + 2


    def drawMode(self, event):
        self.__draw = 1 - self.__draw

    def shiftON(self, event):
        self.__ctrl = True

    def shiftOff(self, event):
        self.__ctrl = False