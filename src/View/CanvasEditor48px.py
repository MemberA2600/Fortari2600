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

        self.__dataP          = data
        self.__colorDataP     = colorData

        self.__finished       = [False, False]
        self.__bg             = bg

        self.__w              = 48
        self.__h              = 48
        self.__Y              = 0

        self.__savedPoz = [-1, -1]
        self.__altButton = None

        self.__ctrl           = False
        self.__alt           = False

        self.__middle         = False
        self.__draw           = 0

        self.__pickedColor    = "$0E"
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

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "<KeyPress-Alt_L>",
                                                            self.altOn, 2)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "<KeyRelease-Alt_L>",
                                                            self.altOff, 2)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "<KeyPress-Alt_R>",
                                                            self.altOn, 2)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "<KeyRelease-Alt_R>",
                                                            self.altOff, 2)

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "<KeyPress-Control_L>",
                                                            self.shiftON, 2)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "<KeyRelease-Control_L>",
                                                            self.shiftOff, 2)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "<KeyPress-Control_R>",
                                                            self.shiftON, 2)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "<KeyRelease-Control_R>",
                                                            self.shiftOff, 2)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "<Button-2>", self.drawMode, 2)

        #self.__loader.threadLooper.addToThreading(self, self.__loop, [], 2)


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
                                                                    self.__enter, 2)
                self.__loader.threadLooper.bindingMaster.addBinding(self, f, "<Button-1>",
                                                                    self.__clicked, 2)
                self.__loader.threadLooper.bindingMaster.addBinding(self, f, "<Button-3>",
                                                                    self.__clicked, 2)

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

            self.__pickedColor = self.__canvasData[y]["colors"][key][2]

            keyNums = {"PF": 2, "PR": 1, "PS": 0}

            self.__layerPicker.deSelect()
            self.__layerPicker.select(
                self.__selectables[keyNums[key]],
                True
            )

    def setLineDataAndColor(self, y):
        yWithOffset = y + self.__Y

        repeatingValids = [0, 1, 2]
        for num in range(0, 3):
            if self.__pattern[num] == "0": repeatingValids.remove(num)

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

                self.__canvasData[y]["colors"][keyPair][1].config(
                    text = keyPair + " (" + self.__canvasData[y]["colors"][keyPair][2] + ")"
                )

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

                    if repeatPixel == 1 and x // 16 in repeatingValids:
                        pixel = "PR"

                else:
                    if repeatPixel == 1 and x // 16 in repeatingValids:
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
        #if True:
            if False in self.__finished:
               return

        except Exception as e:
               print(str(e))
               pass

    def changeSinglePixel(self, y, x, color, layer):
        if layer == "removeLayer":
           pixelName = "BG"
        else:
           p = {
               self.__selectables[0]: "PS",
               self.__selectables[1]: "PR",
               self.__selectables[2]: "PF"
           }

           found = False
           for key in p.keys():
               val = p[key]
               if self.__pickedColor == self.__canvasData[y]["colors"][val][2]:
                  found     = True
                  pixelName = val
                  self.__layerPicker.deSelect()
                  self.__layerPicker.select(key, True)
                  layer = key

                  break

           if found == False:
              pixelName = p[layer]

        if pixelName == "PF" and (x < 8 or x > 39)             : return
        if pixelName == "PR" and self.__pattern[x // 16] == "0": return

        itWas = self.__canvasData[y]["pixels"][x][1]
        self.__canvasData[y]["pixels"][x][1] = pixelName

        repPozStart = x // 16
        otherPoz = [0, 1, 2]

        for num in range(0, 3):
            if self.__pattern[num] == "0":
               otherPoz.remove(num)

        try:
            otherPoz.remove(repPozStart)
        except:
            pass

        updateThese = {
            False: ["PF", "BG"],
            True:  ["PF", "BG", "PS"]
        }

        updateList = updateThese[self.__repeatingOnTop]

        for refX in range(repPozStart * 16, (repPozStart + 1) * 16):
            if self.__canvasData[y]["pixels"][refX][1] == "PR":
               for base in otherPoz:
                   base *= 16
                   updatePoz = base + (refX % 16)
                   if self.__canvasData[y]["pixels"][updatePoz][1] in updateList:
                      self.__canvasData[y]["pixels"][updatePoz][1] = "PR"

            if self.__canvasData[y]["pixels"][refX][1] in updateList:
               for base in otherPoz:
                   base *= 16
                   updatePoz = base + (refX % 16)
                   if self.__canvasData[y]["pixels"][updatePoz][1] == "PR":
                      self.__canvasData[y]["pixels"][updatePoz][1] = "BG"

        for x4 in range(2, 10):
            numOfBGs = 0
            numOfPFs = 0

            for subX in range(x4 * 4, (x4 + 1) * 4):
                if self.__canvasData[y]["pixels"][subX][1] == "PF": numOfPFs += 1
                if self.__canvasData[y]["pixels"][subX][1] == "BG": numOfBGs += 1

            if numOfPFs > 0 and numOfBGs > 0:
                for subX in range(x4 * 4, (x4 + 1) * 4):
                    if   pixelName == "PF" or (pixelName == "BG" and itWas in ("PR", "PS")):
                         if self.__canvasData[y]["pixels"][subX][1] == "BG":
                            self.__canvasData[y]["pixels"][subX][1]  = "PF"
                    elif pixelName == "BG":
                        if self.__canvasData[y]["pixels"][subX][1] == "PF":
                            self.__canvasData[y]["pixels"][subX][1] = "BG"

        if layer != "removeLayer":
           self.__canvasData[y]["colors"][pixelName][2] = color
           self.__canvasData[y]["colors"][pixelName][1].config(
                text=pixelName + " (" + color + ")")
           self.__setColor(self.__canvasData[y]["colors"][pixelName][1], color)

        for subX in range(0, 48):
            if self.__canvasData[y]["pixels"][subX][1] != "BG":
                saveColor = self.__canvasData[y]["colors"][self.__canvasData[y]["pixels"][subX][1]][2]
            else:
                saveColor = self.__bg

            self.__setColor(self.__canvasData[y]["pixels"][subX][0], saveColor
                            )

        self.updateDataFromCanvas(y)

    def updateDataFromCanvas(self, y):
        dataY = y + self.__Y

        for key in self.__colorData[dataY].keys():
            for keyPair in self.__keyPairs:
                if self.__keyPairs[keyPair] == key:
                   break

            self.__colorData[dataY][key] = self.__canvasData[y]["colors"][keyPair][2]

        ones = [0, 1, 2]
        values = [
            self.__keyPairs["PS"], self.__keyPairs["PR"], self.__keyPairs["PF"]
        ]

        for x in range(0, 48):
            pfX = x // 4
            pfInit = x % 4

            relX = x % 16

            self.__data[dataY][values[0]][x] = 0
            for num in ones:
                thatX = (num * 16) + relX
                self.__data[dataY][values[1]][thatX] = 0

            if pfInit == 0:
               self.__data[dataY][values[2]][pfX] = 0

            val = self.__canvasData[y]["pixels"][x][1]
            if val == "PS":
                self.__data[dataY][values[0]][x] = 1
            elif val == "PF":
                self.__data[dataY][values[2]][pfX] = 1
            elif val == "PR":
                for num in ones:
                    thatX = (num * 16) + relX
                    self.__data[dataY][values[1]][thatX] = 1

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

    def drawMode(self, event):
        self.__draw = 1 - self.__draw

    def shiftON(self, event):
        self.__ctrl = True

    def shiftOff(self, event):
        self.__ctrl = False

    def altOn(self, event):
        if self.__altButton != None:
           name = str(self.__altButton).split(".")[-1]
           x = int(name.split("_")[1])
           y = int(name.split("_")[0])

           self.__savedPoz = [x, y]

        self.__alt = True

    def altOff(self, event):
        self.__alt = False

    def __enter(self, event):
        if self.__alt == False:
           self.__altButton = event.widget

        if self.__draw: self.__clicked(event)

    def __clicked(self, event):
        button = event.widget
        name = str(button).split(".")[-1]
        try:
            mouseButton = int(str(event).split(" ")[3].split("=")[1])
        except:
            if self.__ctrl:
                mouseButton = 3
            else:
                mouseButton = 1

        y = int(name.split("_")[0])
        x = int(name.split("_")[1])

        if y >= self.__numOfLines -  self.__Y: return

        if self.__alt:
           if self.__savedPoz[0] != x and self.__savedPoz[1] != y:
              return

        if self.__draw:
            if self.__ctrl:
               layer = "removeLayer"
            else:
               layer = self.__layerPicker.getSelected()
        else:
            if self.__ctrl:
               if mouseButton == 3:
                  layer = "removeLayer"
               else:
                  layer = self.__layerPicker.getSelected()
            else:
                val   = self.__canvasData[y]["pixels"][x][1]
                layer = self.__layerPicker.getSelected()

                p = {
                    self.__selectables[0]: "PS",
                    self.__selectables[1]: "PR",
                    self.__selectables[2]: "PF"
                }

                for key in p:
                    if p[key] == val:
                       if key == layer:
                          layer = "removeLayer"
                       break

        self.changeSinglePixel(y, x, self.__pickedColor, layer)