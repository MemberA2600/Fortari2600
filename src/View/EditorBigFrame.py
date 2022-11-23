from tkinter import *

class EditorBigFrame:

    def __init__(self, loader, frame):

        self.__loader = loader
        self.__editor = self.__loader.mainWindow

        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs
        self.__fontManager = self.__loader.fontManager
        self.__fontSize = int(self.__screenSize[0]/1300 * self.__screenSize[1]/1050*14)
        self.__colors = self.__loader.colorPalettes
        self.__colorDict = self.__loader.colorDict
        self.__memory = self.__loader.virtualMemory.memory
        self.__arrays = self.__loader.virtualMemory.arrays
        self.__virtualMemory = self.__loader.virtualMemory

        self.__focused = None
        self.__screenSize = self.__loader.screenSize

        self.__destroyables = {}

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize*0.65), False, False, False)
        self.__tinyFont = self.__fontManager.getFont(int(self.__fontSize*0.45), False, False, False)
        self.__halfFont = self.__fontManager.getFont(int(self.__fontSize*0.57), False, False, False)

        self.__changed = False
        self.__frame = Frame(frame, width=self.__editor.getWindowSize()[0],
                                   height=self.__editor.getWindowSize()[1],
                                   bg=self.__colors.getColor("window"))
        self.__frame.pack_propagate(False)
        self.__frame.pack(side=TOP, anchor = N, fill=BOTH)

        sizes = (0.20, 0.60, 0.20)

        self.__leftFrame = Frame(self.__frame, width=round(self.__editor.getWindowSize()[0]*sizes[0]),
                                   height=self.__editor.getWindowSize()[1],
                                   bg=self.__colors.getColor("window"))
        self.__leftFrame.pack_propagate(False)
        self.__leftFrame.pack(side=LEFT, anchor = E, fill=Y)

        self.__mainFrame = Frame(self.__frame, width=round(self.__editor.getWindowSize()[0]*sizes[1]),
                                   height=self.__editor.getWindowSize()[1],
                                   bg=self.__colors.getColor("window"))
        self.__mainFrame.pack_propagate(False)
        self.__mainFrame.pack(side=LEFT, anchor = E, fill=Y)

        self.__rightFrame = Frame(self.__frame, width=round(self.__editor.getWindowSize()[0]*sizes[2]),
                                   height=self.__editor.getWindowSize()[1],
                                   bg=self.__colors.getColor("window"))
        self.__rightFrame.pack_propagate(False)
        self.__rightFrame.pack(side=LEFT, anchor = E, fill=Y)

        self.activeMode = None
        # Valid modes: intro, editor, locked, empty
        self.__selectedMode = "intro"

        self.__bankButtons    = self.__editor.changerButtons
        self.__sectionButtons = self.__editor.sectionButtons

        from threading import Thread


        t = Thread(target=self.loop)
        t.daemon = True
        t.start()


    def loop(self):
        from time import sleep

        while self.__editor.dead == False:
            if self.activeMode != self.__selectedMode:
               if self.activeMode != None:
                   self.__removeSlaves()

               self.activeMode = self.__selectedMode

               if self.__selectedMode == "intro":
                  self.__createIntroScreen()
               elif  self.__selectedMode == "empty":
                  pass
               elif  self.__selectedMode == "job":
                  self.__createJobWindows()


            sleep(0.0005)

    def __removeSlaves(self):
        self.__mainFrame.config(bg = self.__loader.colorPalettes.getColor("window"))
        self.__leftFrame.config(bg = self.__loader.colorPalettes.getColor("window"))
        self.__rightFrame.config(bg = self.__loader.colorPalettes.getColor("window"))

        self.__destroyables = {}

        for slave in self.__leftFrame.pack_slaves():
            slave.destroy()

        for slave in self.__mainFrame.pack_slaves():
            slave.destroy()

        for slave in self.__rightFrame.pack_slaves():
            slave.destroy()

    def __createIntroScreen(self):
        from AtariLogo import AtariLogo

        self.__mainFrame.config(bg = "black")
        self.__leftFrame.config(bg = "black")
        self.__rightFrame.config(bg = "black")

        atariLogo = AtariLogo(self.__loader, self.__mainFrame, self.__leftFrame, self.__rightFrame)

        self.__destroyables["AtariLogo"] = atariLogo

    def setMode(self, mode):
        self.__selectedMode = mode

    def getMode(self):
        return self.activeMode

    def __createJobWindows(self):
        from tkinter import scrolledtext

        self.__codeBox = scrolledtext.ScrolledText(self.__mainFrame, width=999999, height=9999999, wrap=WORD)
        self.__codeBox.pack(fill=BOTH)
        self.__codeBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                        fg=self.__loader.colorPalettes.getColor("boxFontNormal"))