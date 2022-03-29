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

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize*0.65), False, False, False)
        self.__bigFont = self.__fontManager.getFont(int(self.__fontSize*1.15), False, False, False)

        self.__offset = 0
        self.__width      = 80      # Two screens
        self.__maxWidth   = 160     # Has to be recalculated!
        self.__lineHeight = 1
        self.__play = False

        self.__sizes = [self.__screenSize[0] / 1.15, self.__screenSize[1] / 2 - 55]
        self.__window = SubMenu(self.__loader, "landscape", self.__sizes[0], self.__sizes[1], None, self.__addElements, 1)

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

        self.__editorFrame = Frame(self.__topLevelWindow, width=self.__sizes[0],
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = round(self.__sizes[1]//5*1.75)
                                   )
        self.__editorFrame.pack_propagate(False)
        self.__editorFrame.pack(side=TOP, anchor=N, fill=X)

        self.__displayFrame = Frame(self.__topLevelWindow, width=self.__sizes[0],
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = self.__sizes[1]//5*2
                                   )
        self.__displayFrame.pack_propagate(False)
        self.__displayFrame.pack(side=TOP, anchor=N, fill=X)

        self.__controlFrame = Frame(self.__topLevelWindow, width=self.__sizes[0],
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = round(self.__sizes[1]//5*2.25)
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

        self.__finished = [False, False, False]

        t1 = Thread(target=self.__createData)
        t1.daemon = True
        t1.start()

        t2 = Thread(target=self.__createEditorPixelsFrame)
        t2.daemon = True
        t2.start()

        t3 = Thread(target=self.__createEditorColorsFrame)
        t3.daemon = True
        t3.start()

        L = Thread(target=self.__loop)
        L.daemon = True
        L.start()

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
            self.__buttons.append([])
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

    def __enter(self, event):
        for item in self.__finished:
            if item == False: return

    def __setColorData(self, event):
        for item in self.__finished:
            if item == False: return

        breaking = False

    def __loop(self):
        from time import sleep

        while self.dead == False and self.__mainWindow.dead == False:
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

            sleep(0.0005)