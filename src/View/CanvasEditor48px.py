from tkinter import *
from SubMenu import SubMenu
from copy import deepcopy
from time import sleep
from threading import Thread

class CanvasEditor48px:

    def __init__(self, loader, numOfLines, repeatingOnTop, pattern, data, colorData, bg, keys):
        self.__loader = loader

        self.__loader = loader
        self.__mainWindow = self.__loader.mainWindow

        self.dead = False
        self.changed = False
        self.__loader.stopThreads.append(self)
        self.__first = True

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

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize*0.65), False, False, False)
        self.__bigFont = self.__fontManager.getFont(int(self.__fontSize*1.15), False, False, False)
        self.__bigFont2 = self.__fontManager.getFont(int(self.__fontSize*1.5), False, False, False)

        self.__sizes = [self.__screenSize[0] // 1.5, self.__screenSize[1] // 1.40]

        self.__numOfLines     = numOfLines
        self.__repeatingOnTop = repeatingOnTop
        self.__pattern        = pattern

        self.__data           = deepcopy(data)
        self.__colorData      = deepcopy(colorData)

        self.__finished       = [False, False]
        self.__bg             = bg

        self.__w              = 48
        self.__h              = 48
        self.__Y              = 0

        self.__keyPairs       = {
            "PS": keys[0], "PR": keys[1], "PF": keys[2]
        }

        self.__window = SubMenu(self.__loader, "48pxCanvas", self.__sizes[0], self.__sizes[1], None,
                                self.__addElements,
                                2)
        self.dead   = True

    def __closeWindow(self):
        self.dead = True
        self.__topLevelWindow.destroy()
        self.__loader.topLevels.remove(self.__topLevelWindow)


    def __addElements(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()
        self.__topLevelWindow.protocol('WM_DELETE_WINDOW', self.__closeWindow)

        self.__canvasFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__sizes[1], width=self.__sizes[0] // 20 * 10)
        self.__canvasFrame.pack_propagate(False)
        self.__canvasFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__colorsFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__sizes[1], width=self.__sizes[0] // 20 * 5)
        self.__colorsFrame.pack_propagate(False)
        self.__colorsFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__setterFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__sizes[1], width=self.__sizes[0] // 20 * 5)
        self.__setterFrame.pack_propagate(False)
        self.__setterFrame.pack(side=LEFT, anchor=E, fill=BOTH)

        t1 = Thread(target=self.__createCanvasFrameButtons)
        t1.daemon = True
        t1.start()

        self.__loader.threadLooper.addToThreading(self, self.__loop, [], 1)

    def __createCanvasFrameButtons(self):
        while self.__canvasFrame.winfo_width() < 2: sleep(0.00005)
        while self.__colorsFrame.winfo_width() < 2: sleep(0.00005)

        w = self.__canvasFrame.winfo_width()  // self.__w
        h = self.__canvasFrame.winfo_height() // self.__h

        self.__canvasData    = []
        self.__lineFrames        = []

        for y in range (0, self.__h):
            self.__canvasData.append({
                "enabled"    : True,
                "pixels"     : [],
                "colors"     : {"PF": [None, None, self.__bg],
                                "PR": [None, None, self.__bg],
                                "PS": [None, None, self.__bg]}
            })

            lineFrame = Frame(self.__canvasFrame,
                                bg=self.__loader.colorPalettes.getColor("window"),
                                width=self.__canvasFrame.winfo_width(), height=h)

            lineFrame.pack_propagate(False)
            lineFrame.pack(side=TOP, anchor=N, fill=X)
            self.__soundPlayer.playSound("Pong")
            self.__lineFrames.append(lineFrame)

            for x in range(0, self.__w):
                f = Frame(lineFrame,
                          bg=self.__colorDict.getHEXValueFromTIA(self.__bg),
                          borderwidth=1, relief=RIDGE, name = str(y) + "_" + str(x),
                          width=w, height=h)
                f.pack_propagate(False)
                f.pack(side=LEFT, anchor=E, fill=Y)

                self.__canvasData[-1]["pixels"].append([f, "BG"])

            clineFrame = Frame(self.__colorsFrame,
                                bg=self.__loader.colorPalettes.getColor("window"),
                                width=self.__colorsFrame.winfo_width(), height=h)

            clineFrame.pack_propagate(False)
            clineFrame.pack(side=TOP, anchor=N, fill=X)
            self.__lineFrames.append(clineFrame)

            for key in self.__canvasData[-1]["colors"].keys():
                f = Frame(clineFrame,
                          bg=self.__colorDict.getHEXValueFromTIA(self.__bg),
                          width=self.__colorsFrame.winfo_width() // 3, height=h,
                          borderwidth=1, relief=RIDGE)
                f.pack_propagate(False)
                f.pack(side=LEFT, anchor=E, fill=BOTH)

                l = Label(f,
                          bg=self.__colorDict.getHEXValueFromTIA(self.__bg),
                          text=key, font=self.__miniFont, name=str(y) + "_" + key,
                          width=self.__colorsFrame.winfo_width(), height=h)
                l.pack_propagate(False)
                l.pack(side=LEFT, anchor=E, fill=BOTH)

                self.__setColor(l, self.__bg)
                self.__canvasData[-1]["colors"][key][0] = f
                self.__canvasData[-1]["colors"][key][1] = l

            self.setLineDataAndColor(y)

        self.__finished[0] = True

    def setLineDataAndColor(self, y):
        yWithOffset = y + self.__Y

        if yWithOffset < self.__numOfLines:
            self.__canvasData[y]["enabled"] = True
            for key in self.__colorData[yWithOffset].keys():
                keyPair = ""
                for keyPair in self.__keyPairs:
                    if self.__keyPairs[keyPair] == key:
                        break

                self.__canvasData[y]["colors"][keyPair][2] = self.__colorData[yWithOffset][key]
                self.__setColor(self.__canvasData[y]["colors"][keyPair][1],
                                self.__canvasData[y]["colors"][keyPair][2])

            for x in range(0, self.__w):
                simplePixel    = self.__data[yWithOffset][self.__keyPairs["PS"]][x]
                repeatPixel    = self.__data[yWithOffset][self.__keyPairs["PR"]][x]
                playfieldPixel = self.__data[yWithOffset][self.__keyPairs["PF"]][x // 4]

                pixel = "BG"
                if playfieldPixel == 1:
                    pixel = "PF"

                if self.__repeatingOnTop:
                    if simplePixel == 1:
                        pixel = "PS"

                    if repeatPixel == 1:
                        pixel = "PR"

                else:
                    if repeatPixel == 1:
                        pixel = "PR"

                    if simplePixel == 1:
                        pixel = "PS"

                #print(pixel, simplePixel, repeatPixel, playfieldPixel)

                self.__canvasData[y]["pixels"][x][1] = pixel
                if pixel == "BG":
                   self.__setColor(self.__canvasData[y]["pixels"][x][0], self.__bg)
                else:
                   self.__setColor(self.__canvasData[y]["pixels"][x][0],
                                   self.__canvasData[y]["colors"][pixel][2])

        else:
            self.__canvasData[y]["enabled"] = False
            for item in self.__canvasData[y]["pixels"]:
                item[0].config(bg=self.__loader.colorPalettes.getColor("fontDisabled"),
                               borderwidth=0, relief=GROOVE
                               )
            for key in self.__canvasData[y]["colors"].keys():
                self.__canvasData[y]["colors"][key][0].config(bg=self.__loader.colorPalettes.getColor("fontDisabled"),
                                                               # borderwidth=0, relief=GROOVE
                                                               )
                self.__canvasData[y]["colors"][key][1].config(bg=self.__loader.colorPalettes.getColor("fontDisabled"),
                                                               text=""
                                                               )
    def __loop(self):
        try:
            if False in self.__finished:
               return

        except Exception as e:
               print(str(e))
               pass


    def __setColor(self, frame, color):
        try:
            t = int("0x"+color[-1], 16)
            if t % 2 == 1:
               t = t-1
               color = color[:-1]+hex(t).replace("0x","")

            color1 = self.__colorDict.getHEXValueFromTIA(color)

            num = int("0x"+color[2], 16)
            if num>8:
                num = color[:2]+hex(num-6).replace("0x","")
            else:
                num = color[:2]+hex(num+6).replace("0x","")

            color2 = self.__colorDict.getHEXValueFromTIA(num)
            frame.config(bg=color1, fg=color2)
        except Exception as e:
            frame.config(bg=self.__colorDict.getHEXValueFromTIA(color))
