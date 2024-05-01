from tkinter import *
from SubMenu import SubMenu
from copy import deepcopy
from time import sleep
from threading import Thread
from FortariMB import FortariMB

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

        self.__pickedColor    = "$0E"
        self.__mouse1         = False
        self.__mouse3         = False

        self.__enteredButton  = None
        self.__drawLayer      = "uniqueLayer"

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

        t2 = Thread(target=self.__createSetterThings)
        t2.daemon = True
        t2.start()

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "<Button-1>", self.mouseClicked, 2)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "<Button-3>", self.mouseClicked, 2)

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "<ButtonRelease-1>", self.mouseReleased, 2)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "<ButtonRelease-3>", self.mouseReleased, 2)

        self.__loader.threadLooper.addToThreading(self, self.__loop, [], 1)

    def mouseClicked(self, event):
        mouseButton = int(str(event).split(" ")[3].split("=")[1])

        if   mouseButton == 1:
             self.__mouse1 = True
        elif mouseButton == 3:
             self.__mouse3 = True

    def mouseReleased(self, event):
        mouseButton = int(str(event).split(" ")[3].split("=")[1])

        if   mouseButton == 1:
             self.__mouse1 = False
        elif mouseButton == 3:
             self.__mouse3 = False

    def enteredFrame(self, event):
        if False in self.__finished: return

        self.__enteredButton = event.widget

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

                self.__loader.threadLooper.bindingMaster.addBinding(self, f, "<Enter>",
                                                                    self.enteredFrame, 2)
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

                b = Button(f,
                          bg=self.__colorDict.getHEXValueFromTIA(self.__bg),
                          text=key, font=self.__miniFont, name=str(y) + "_" + key,
                          relief=GROOVE, activebackground=self.__colors.getColor("highLight"),
                          width=self.__colorsFrame.winfo_width(), height=h)
                b.pack_propagate(False)
                b.pack(side=LEFT, anchor=E, fill=BOTH)

                self.__setColor(b, self.__bg)
                self.__canvasData[-1]["colors"][key][0] = f
                self.__canvasData[-1]["colors"][key][1] = b

                self.__loader.threadLooper.bindingMaster.addBinding(self, b, "<Button-1>", self.__colorPicked, 2)

            self.setLineDataAndColor(y)

        self.__finished[0] = True

    def __createSetterThings(self):
        while self.__setterFrame.winfo_width() < 2: sleep(0.00005)

        self.__colorPickerFrame = Frame(self.__setterFrame,
                                bg=self.__loader.colorPalettes.getColor("window"),
                                width=self.__setterFrame.winfo_width(), height=self.__setterFrame.winfo_height() // 3 * 2)

        self.__colorPickerFrame.pack_propagate(False)
        self.__colorPickerFrame.pack(side=TOP, anchor=N, fill=X)

        while self.__colorPickerFrame.winfo_width() < 2: sleep(0.00005)

        w = self.__colorPickerFrame.winfo_width()  // 8
        h = self.__colorPickerFrame.winfo_height() // 16

        self.__colorPickerButtons = []

        for y in range(0, 16):
            hex1 = hex(y).replace("0x", "$").upper()

            lineFrame = Frame(self.__colorPickerFrame,
                              bg=self.__loader.colorPalettes.getColor("window"),
                              width=self.__colorPickerFrame.winfo_width(), height=h)

            lineFrame.pack_propagate(False)
            lineFrame.pack(side=TOP, anchor=N, fill=X)

            for x in range(0, 16, 2):
                hex2 = hex(x).replace("0x", "").upper()
                name = hex1 + hex2

                f = Frame(lineFrame,
                          bg=self.__loader.colorPalettes.getColor("window"),
                          width = w, height=h,
                          )
                f.pack_propagate(False)
                f.pack(side=LEFT, anchor=E, fill=BOTH)

                b = Button(f,
                           bg=self.__colorDict.getHEXValueFromTIA(name),
                           text=name, font=self.__miniFont, name=name,
                           relief=GROOVE, activebackground=self.__colors.getColor("highLight"),
                           width=w, height=h)
                b.pack_propagate(False)
                b.pack(side=LEFT, anchor=E, fill=BOTH)

                self.__setColor(b, name)
                self.__colorPickerButtons.append(b)

                self.__loader.threadLooper.bindingMaster.addBinding(self, b, "<Button-1>", self.__colorPicked, 2)

        self.__layerPickerFrame = Frame(self.__setterFrame,
                                bg=self.__loader.colorPalettes.getColor("window"),
                                width=self.__setterFrame.winfo_width(), height=self.__setterFrame.winfo_height() // 9 * 2)

        self.__layerPickerFrame.pack_propagate(False)
        self.__layerPickerFrame.pack(side=TOP, anchor=N, fill=X)

        self.__layerPickerLabel = Label(self.__layerPickerFrame,
                                    text=self.__dictionaries.getWordFromCurrentLanguage("drawLayer"),
                                    font=self.__smallFont, fg=self.__colors.getColor("font"),
                                    bg=self.__colors.getColor("window")
                                    )

        self.__layerPickerLabel.pack_propagate(False)
        self.__layerPickerLabel.pack(side=TOP, anchor=N, fill=X)

        self.__selectables = [
            self.__dictionaries.getWordFromCurrentLanguage("uniqueLayer"),
            self.__dictionaries.getWordFromCurrentLanguage("repeatingLayer"),
            self.__dictionaries.getWordFromCurrentLanguage("playfieldLayer")
        ]

        self.__layerPicker = FortariMB(self.__loader, self.__layerPickerFrame, NORMAL,
                                            self.__smallFont, self.__selectables[0], self.__selectables, False, False,
                                            self.layerChanged, [self.__selectables[0]])

        self.__drawLayer = self.__selectables[0]

        self.__finished[1] = True

    def layerChanged(self):
        self.__drawLayer = self.__layerPicker.getSelected()

    def __colorPicked(self, event):
        button = event.widget
        name   = str(button).split(".")[-1]

        if "$" in name:
            self.__pickedColor = name
        else:
            y   = int(name.split("_")[0])
            key = name.split("_")[1]

            self.__pickedColor = self.__canvasData[y]["colors"][key]

            keyNums = {"PF": 2, "PR": 1, "PS": 0}

            self.__layerPicker.deSelect()
            self.__layerPicker.select(
                self.__selectables[keyNums[key]],
                True
            )

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

                #self.__canvasData[y]["colors"][keyPair][1].config(state = NORMAL)

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
                                                               borderwidth=0, relief=GROOVE
                                                               )
                self.__canvasData[y]["colors"][key][1].config(bg=self.__loader.colorPalettes.getColor("fontDisabled"),
                                                               text="",
                                                               state = DISABLED
                                                               )

    def __loop(self):
        try:
            if False in self.__finished:
               return

            if self.__mouse1 or self.__mouse3:
               if self.__enteredButton != None:
                  self.processEnter()
                  self.__enteredButton = None

        except Exception as e:
               print(str(e))
               pass

    def processEnter(self):
        name = str(self.__enteredButton).split(".")[-1]
        y = int(name.split("_")[0])
        x = int(name.split("_")[1])

        pfColor          = self.__canvasData[y]["colors"]["PF"][2]
        repeatColor      = self.__canvasData[y]["colors"]["PR"][2]
        simpleColor      = self.__canvasData[y]["colors"]["PS"][2]

        currentDisplayed = self.__canvasData[y]["pixels"][x][1]

        if self.__mouse1:
           doNothing = {
                "BG": self.__bg, "PF": pfColor, "PR": repeatColor, "PS": simpleColor
           }

           if doNothing[currentDisplayed] == self.__pickedColor: return

           """ 
           editingMode = ""
           if self.__pickedColor in doNothing.values():
              for key in doNothing:
                  if doNothing[key] == self.__pickedColor:
                     editingMode = key
                     break
           else:
              onesNotUsedOnLine = ["PF", "PR", "PS"]
              for theX in range(0, 48):
                  if theX == x: continue
                  item = self.__canvasData[y]["pixels"][theX][1]
                  if item in onesNotUsedOnLine:
                     onesNotUsedOnLine.remove(item)

                  if len(onesNotUsedOnLine) == 0:
                     break

              affectedOtherPixels = 0
              if currentDisplayed == "PF":
                  

              if len(onesNotUsedOnLine) > 0:
                 pass
              """



        elif self.__mouse3:
            pass

    def changeSinglePixel(self, y, x, color, mode):
        pass

    def updateDataFromCanvas(self, y):
        dataY = y + self.__Y


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
