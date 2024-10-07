from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from time import sleep
from copy import deepcopy
from tkinter import scrolledtext
from PIL import ImageTk, Image as IMAGE

class Oven:

    def __init__(self, loader, blocks, code):
        self.__loader = loader
        self.__mainWindow = self.__loader.mainWindow

        self.__blocks = blocks
        self.__code   = code

        self.dead = False
        self.__changed = False
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

        self.__running  = 0
        self.__focused = None
        self.__screenSize = self.__loader.screenSize
        self.__picIndex = 0

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize*0.65), False, False, False)
        self.__bigFont = self.__fontManager.getFont(int(self.__fontSize*1.15), False, False, False)

        self.__sizes = [self.__screenSize[0] / 1.25, self.__screenSize[1] / 1.25 - 40]
        self.__window = SubMenu(self.__loader, "rawData", self.__sizes[0], self.__sizes[1], None, self.__addElements, 2)

        self.dead = True

    def __closeWindow(self):
        self.dead = True
        self.__topLevelWindow.destroy()
        self.__loader.topLevels.remove(self.__topLevelWindow)

    def __addElements(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()
        self.__topLevelWindow.protocol('WM_DELETE_WINDOW', self.__closeWindow)

        self.__narrowFtame = Frame(self.__topLevelWindow,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0] // 4, height = self.__sizes[1] )

        self.__narrowFtame.pack_propagate(False)
        self.__narrowFtame.pack(side=LEFT, anchor=W, fill=Y)

        self.__mostFrame = Frame(self.__topLevelWindow,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0] // 4 * 3, height = self.__sizes[1] )

        self.__mostFrame.pack_propagate(False)
        self.__mostFrame.pack(side=LEFT, anchor=W, fill=BOTH)

        t1 = Thread(target = self.__loadNarrow)
        t1.daemon = True
        t1.start()

        self.__loader.threadLooper.addToThreading(self, self.loop, [], 1)

    def loop(self):
        if self.__running == 0:
           self.__picIndex += 1
           if self.__picIndex > 15: self.__picIndex = 0

           self.__thatPic = self.__canvas.create_image(
               0, 0, image=self.__buffer[self.__picIndex // 4], anchor=NW
           )


    def __loadNarrow(self):
        self.__running += 1

        while self.__narrowFtame.winfo_width() < 2: sleep(0.00000001)

        # 325 x 115

        w = round(self.__narrowFtame.winfo_width())
        h = round(115 * (self.__narrowFtame.winfo_width() / 325))


        self.__narrowFtameUpper = Frame(self.__narrowFtame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0] // 10, height = h )

        self.__narrowFtameUpper.pack_propagate(False)
        self.__narrowFtameUpper.pack(side=TOP, anchor=N, fill=X)

        self.__canvas = Canvas(self.__narrowFtameUpper, bg = self.__loader.colorPalettes.getColor("window"),
                               height=h, width=w)
        self.__canvas.pack_propagate(False)
        self.__canvas.pack(side=TOP, fill=BOTH, anchor=CENTER)

        self.__buffer = []

        for num in range(0, 4):
            #self.__buffer.append(IMAGE.open(str("others/img/cooker/0" + str(num) + ".png")).resize(w, h, IMAGE.ANTIALIAS))

            self.__buffer.append(
                ImageTk.PhotoImage(IMAGE.open("others/img/cooker/0" + str(num) + ".png").resize((w, h), IMAGE.ANTIALIAS)))

        self.__thatPic = self.__canvas.create_image(
            0, 0, image=self.__buffer[0], anchor=NW
        )

        self.__asmBox    = scrolledtext.ScrolledText(self.__narrowFtame, width=999999, height=self.__sizes[1]//2, wrap=WORD)
        self.__asmBox.pack(fill=BOTH, side=BOTTOM, anchor=S)

        self.__asmBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                fg=self.__loader.colorPalettes.getColor("boxFontNormal"))


        self.__getFont()

        self.__asmBox.insert(END, self.__code)
        self.__formatting()

        self.__asmBox.bind("<Key>", lambda e: "break")
        self.__running -= 1

    def __formatting(self):
        y = 0
        for line in self.__code.split("\n"):
            y = y + 1
            if len(line) == 0: continue

            if line[0] in (" ", "\t"):
               wasNonSpace = False
               for poz in range(0, len(line)):
                   if line[poz] in (" ", "\t"):
                      if wasNonSpace: break
                   else:
                      wasNonSpace = True

               self.addTag(y, 0  , poz      , "command")

               if ";" in line:
                  self.addTag(y, poz, line.index(";")      , "number")
                  self.addTag(y, line.index(";"), len(line), "comment")
               else:
                  self.addTag(y, poz, len(line), "number" )

            else:
               if line[0] in ["#", "*"] and line[1:5] not in ("NAME", "BANK"):
                  self.addTag(y, 0, len(line), "comment")
               else:
                  self.addTag(y, 0, len(line), "label")


    def addTag(self, Y, X1, X2, tag):
        self.__asmBox.tag_add(tag, str(Y) + "." + str(X1) , str(Y) + "." + str(X2))

    def __getFont(self):
        baseSize = int(self.__config.getValueByKey("codeBoxFont"))
        w = self.__loader.mainWindow.getWindowSize()[0] / 1600
        h = self.__loader.mainWindow.getWindowSize()[1] / 1200

        self.__fontSize = (baseSize * w * h)
        self.__normalFont = self.__loader.fontManager.getFont(round(self.__fontSize), False, False, False)
        self.__boldFont = self.__loader.fontManager.getFont(round(self.__fontSize), True, False, False)
        self.__italicFont = self.__loader.fontManager.getFont(round(self.__fontSize), False, True, False)
        self.__undelinedFont = self.__loader.fontManager.getFont(round(self.__fontSize), False, False, True)
        self.__boldItalicFont = self.__loader.fontManager.getFont(round(self.__fontSize), True, True, False)
        self.__boldUnderlinedFont = self.__loader.fontManager.getFont(round(self.__fontSize), True, False, True)
        self.__boldItalicUnderLinedFont = self.__loader.fontManager.getFont(round(self.__fontSize), True, True, True)

        self.__tagSettings = {
            "comment": {
                "foreground": self.__loader.colorPalettes.getColor("comment"),
                "font": self.__italicFont
            },
            "number": {
                "foreground": self.__loader.colorPalettes.getColor("number"),
                "font": self.__normalFont
            },
            "command": {
                "foreground": self.__loader.colorPalettes.getColor("command"),
                "font": self.__boldFont
            },
            "label": {
                "foreground": self.__loader.colorPalettes.getColor("portState"),
                "font": self.__boldUnderlinedFont
            }
        }

        for key in self.__tagSettings:
            if "background" not in self.__tagSettings[key]:
                self.__asmBox.tag_config(key,
                                            foreground=self.__tagSettings[key]["foreground"],
                                            font=self.__tagSettings[key]["font"])
            elif "foreground" not in self.__tagSettings[key]:
                self.__asmBox.tag_config(key,
                                            background=self.__tagSettings[key]["background"],
                                            font=self.__tagSettings[key]["font"])
            else:
                self.__asmBox.tag_config(key,
                                            foreground=self.__tagSettings[key]["foreground"],
                                            background=self.__tagSettings[key]["background"],
                                            font=self.__tagSettings[key]["font"])

        self.__asmBox.config(font=self.__normalFont)
        self.__asmBox.tag_raise("sel")

