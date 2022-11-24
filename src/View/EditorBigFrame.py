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
        self.__counter    = 0
        self.__cursorPoz  = [1,0]

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
        self.__highLightWord       = None
        self.__highLightIgnoreCase = True

        from threading import Thread
        self.__ctrl = False

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

            if self.__counter > 0:
               self.__counter -= 1

            if self.__counter == 1: self.__counterEnded()
            sleep(0.005)

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

        self.__codeBox.bind("<Key>", self.__keyPressed)
        self.__codeBox.bind("<KeyRelease>", self.__keyReleased)
        self.__codeBox.bind("<MouseWheel>", self.__mouseWheel)
        self.__codeBox.bind("<FocusIn>", self.__loader.mainWindow.focusIn)
        self.__codeBox.bind("<FocusOut>", self.__loader.mainWindow.focusOut)

        self.__currentBank    = "bank2"
        self.__currentSection = "overscan"

        self.__loadFromMemory(self.__currentBank, self.__currentSection)

        self.__validKeys = [
            "enter", "leave", "overscan", "vblank", "subroutines"
        ]

        self.__getFont()

    def __loadFromMemory(self, bank, section):
        if self.__loader.virtualMemory.codes[self.__currentBank][self.__currentSection].changed == True:
           pass

        self.__codeBox.delete(0.0, END)
        text = self.__loader.virtualMemory.codes[bank][section].code
        self.__codeBox.insert(0.0, text)
        self.__setTinting("whole")

    def __setTinting(self, mode):
        from threading import Thread

        t = Thread(target=self.__tintingThread, args=[mode])
        t.daemon = True
        t.start()

    def __tintingThread(self, mode):
        text = self.__codeBox.get(0.0, END).split("\n")
        if mode == "whole":
           for num in range (1, len(text)+1):
               self.__lineTinting(num, text[num-1])
        else:
            self.__lineTinting(mode, text[mode-1])

    def __lineTinting(self, lineNum, line):
        for tag in self.__codeBox.tag_names():
            self.__codeBox.tag_remove(tag,
                                      str(lineNum)+".0",
                                      str(lineNum) + "." + str(len(line))
                                      )

        if line.startswith("*") or line.startswith("#"):
           self.__codeBox.tag_add("comment", str(lineNum) + ".0", str(lineNum) + "." + str(len(line)))

        xxx = self.getFirstValidDelimiterPoz(line)
        if xxx != None:
           self.__codeBox.tag_add("comment", str(lineNum) + "."+ str(xxx), str(lineNum) + "." + str(len(line)))

        if self.__highLightWord != None:
            highLightPositions = self.stringInLine(line, self.__highLightWord)
            for dim in highLightPositions:
                self.__codeBox.tag_add("highLight",
                                       str(lineNum) + "." + str(dim[0]),
                                       str(lineNum) + "." + str(dim[1])
                                       )

    def stringInLine(self, line, word):
        positions = []

        for startIndex in range(0, len(line)-len(word)):
            tempW = line[startIndex:startIndex+len(word)]
            if self.__highLightIgnoreCase == True:
               if tempW.upper() == word.upper(): positions.append((startIndex, startIndex+len(word)))
            else:
               if tempW == word: positions.append((startIndex, startIndex + len(word)))

        return(positions)

    def __getFont(self):
        baseSize = int(self.__config.getValueByKey("codeBoxFont"))
        w = self.__editor.getWindowSize()[0] / 1600
        h = self.__editor.getWindowSize()[1] / 1200

        self.__fontSize = (baseSize * w * h * 1.5)
        self.__normalFont = self.__loader.fontManager.getFont(round(self.__fontSize), False, False, False)
        self.__boldFont = self.__loader.fontManager.getFont(round(self.__fontSize), True, False, False)
        self.__italicFont = self.__loader.fontManager.getFont(round(self.__fontSize), False, True, False)
        self.__undelinedFont = self.__loader.fontManager.getFont(round(self.__fontSize), False, False, True)
        self.__boldItalicFont = self.__loader.fontManager.getFont(round(self.__fontSize), True, True, False)
        self.__boldUnderlinedFont = self.__loader.fontManager.getFont(round(self.__fontSize), True, False, True)
        self.__boldItalicUnderLinedFont = self.__loader.fontManager.getFont(round(self.__fontSize), True, True, True)

        self.__codeBox.tag_config("comment",
                                  foreground=self.__loader.colorPalettes.getColor("comment"),
                                  font=self.__italicFont)

        self.__codeBox.tag_config("highLight", background=self.__loader.colorPalettes.getColor("highLight"))


        self.__codeBox.config(font=self.__normalFont)

    def getFirstValidDelimiterPoz(self, line):
        level = 0
        validDelimiters = self.__config.getValueByKey("validLineDelimiters").split(" ")
        for charNum in range(0, len(line)):
            if line[charNum] in validDelimiters and level == 0: return charNum

            if line[charNum] == "(": level += 1
            if line[charNum] == ")": level -= 1
            if level < 0     : level = 0

    def __counterEnded(self):
        self.__loader.virtualMemory.codes[self.__currentBank][self.__currentSection].changed = True
        self.__setTinting(self.__cursorPoz[0])

    def __keyPressed(self, event):
        if (event.keysym == "Control_L" or event.keysym == "Control_R"):
            self.__ctrl = True

    def __keyReleased(self, event):
        self.__counter   = 100
        __cursorPoz = self.__codeBox.index(INSERT)
        self.__cursorPoz = [int(__cursorPoz.split(".")[0]), int(__cursorPoz.split(".")[1])]

        if (event.keysym == "Control_L" or event.keysym == "Control_R"):
            self.__ctrl = False

    def __mouseWheel(self, event):
        if event.delta > 0 and int(self.__config.getValueByKey("codeBoxFont")) < 36:
            self.__config.setKey("codeBoxFont", str(int(self.__config.getValueByKey("codeBoxFont")) + 1))
            self.__getFont()

        if event.delta < 0 and int(self.__config.getValueByKey("codeBoxFont")) > 12:
            self.__config.setKey("codeBoxFont", str(int(self.__config.getValueByKey("codeBoxFont")) - 1))
            self.__getFont()
