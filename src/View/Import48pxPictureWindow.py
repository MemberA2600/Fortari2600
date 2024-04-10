from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from time import sleep
from PIL import Image as IMG, ImageTk, ImageOps
import os

class Import48pxPictureWindow:

    def __init__(self, loader, initMode, numOfLines, repeatingOnTop, pattern, patterns):
        self.__loader = loader

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

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize*0.65), False, False, False)
        self.__bigFont = self.__fontManager.getFont(int(self.__fontSize*1.15), False, False, False)
        self.__bigFont2 = self.__fontManager.getFont(int(self.__fontSize*1.5), False, False, False)

        self.__sizes = [self.__screenSize[0] // 2.25, self.__screenSize[1] // 1.40]

        self.__initMode       = initMode
        self.__wasInit        = initMode
        self.__auto           = initMode
        self.__oneColorBG     = False

        self.__numOfLines     = numOfLines
        self.__repeatingOnTop = repeatingOnTop
        self.__patterns       = patterns
        self.__pattern        = pattern
        self.__w              = 48
        self.__tolerance      = 4
        self.__segmentMethod  = "AVG"
        self.__segmentMethods = ["AND", "OR", "AVG"]

        self.__tresConst      = 42

        formats = ["bmp", "dds", "eps", "gif", "dib", "ico", "jpg", "jpeg", "pcx", "png", "tga", "tiff", "pdf"]

        self.answer = self.__fileDialogs.askForFileName("loadPicture",
                                                        False, [formats, "*"], self.__mainWindow.projectPath)

        self.result = None

        if self.answer != "" or os.path.exists(self.answer) == False:
           self.__imageBackUp = IMG.open(self.answer, "r")
           if self.__imageBackUp.mode != "RGB":
              self.__imageBackUp       = self.__imageBackUp.convert("RGB")

           w, h     = self.__imageBackUp.size
           self.__h = round((self.__w / w) * h)
           if self.__h > 255: self.__h = 255

           #self.__imageBackUp = self.__imageBackUp.resize((self.__w, self.__h), IMG.ANTIALIAS)

           self.__window = SubMenu(self.__loader, "loadPicture", self.__sizes[0], self.__sizes[1], None, self.__addElements,
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
                                 height=round(self.__sizes[1] / 3 * 2), width = self.__sizes[0])
        self.__canvasFrame.pack_propagate(False)
        self.__canvasFrame.pack(side=TOP, anchor=N, fill=X)

        between = 50

        self.__subFrame0 = Frame(self.__canvasFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 3 * 2, width = (between // 3))
        self.__subFrame0.pack_propagate(False)
        self.__subFrame0.pack(side=LEFT, anchor=E, fill=Y)

        self.__subFrame1 = Frame(self.__canvasFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 3 * 2, width = self.__sizes[0] // 2 - (between // 2))
        self.__subFrame1.pack_propagate(False)
        self.__subFrame1.pack(side=LEFT, anchor=E, fill=Y)

        self.__subFrame2 = Frame(self.__canvasFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 3 * 2, width = (between // 3))
        self.__subFrame2.pack_propagate(False)
        self.__subFrame2.pack(side=LEFT, anchor=E, fill=Y)

        self.__subFrame3 = Frame(self.__canvasFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 3 * 2, width = self.__sizes[0] // 2 - (between // 2))
        self.__subFrame3.pack_propagate(False)
        self.__subFrame3.pack(side=LEFT, anchor=E, fill=Y)

        self.__subFrame4 = Frame(self.__canvasFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 3 * 2, width = (between // 3))
        self.__subFrame4.pack_propagate(False)
        self.__subFrame4.pack(side=LEFT, anchor=E, fill=Y)

        self.__canvas = Canvas(self.__subFrame3, bg="black", bd=0,
                               width  = self.__sizes[0],
                               height = self.__sizes[1] // 3 * 2
                               )

        self.__canvas.pack_propagate(False)
        self.__canvas.pack(side=TOP, anchor=N, fill=Y)

        self.__imgLabel = Label(self.__subFrame1, bg="black",
                                width  = round(self.__sizes[0]),
                                height = round(self.__sizes[1] // 3 * 2)
                                )
        self.__imgLabel.pack_propagate(False)
        self.__imgLabel.pack(side=TOP, anchor=N, fill=BOTH)

        self.__thresholdFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 25, width = self.__sizes[0])
        self.__thresholdFrame.pack_propagate(False)
        self.__thresholdFrame.pack(side=TOP, anchor=N, fill=X)

        self.__tresLabel = Label(self.__thresholdFrame, text=self.__dictionaries.getWordFromCurrentLanguage("thresholdSetter"),
                                  bg = self.__loader.colorPalettes.getColor("window"),
                                  fg = self.__loader.colorPalettes.getColor("font"), justify = "center",
                                  font=self.__normalFont
                                  )
        self.__tresLabel.pack(side=TOP, anchor=N, fill=X)

        self.__thresholdEntryFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 25, width = self.__sizes[0])
        self.__thresholdEntryFrame.pack_propagate(False)
        self.__thresholdEntryFrame.pack(side=TOP, anchor=N, fill=X)

        self.__thresholdEntryFrame1 = Frame(self.__thresholdEntryFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 10, width = self.__sizes[0] // 10 * 4)
        self.__thresholdEntryFrame1.pack_propagate(False)
        self.__thresholdEntryFrame1.pack(side=LEFT, anchor=E, fill=Y)

        self.__thresholdEntryFrame2 = Frame(self.__thresholdEntryFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 10, width = self.__sizes[0] // 10 * 2)
        self.__thresholdEntryFrame2.pack_propagate(False)
        self.__thresholdEntryFrame2.pack(side=LEFT, anchor=E, fill=Y)

        self.__thresholdEntryFrame3 = Frame(self.__thresholdEntryFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 10, width = self.__sizes[0] // 10 * 4)
        self.__thresholdEntryFrame3.pack_propagate(False)
        self.__thresholdEntryFrame3.pack(side=LEFT, anchor=E, fill=Y)

        self.__tres      = StringVar()
        self.__tres.set(str(self.__tresConst))
        self.__tresEntry = Entry(self.__thresholdEntryFrame2, text=self.__dictionaries.getWordFromCurrentLanguage("thresholdSetter"),
                                  bg = self.__loader.colorPalettes.getColor("boxBackNormal"),
                                  fg = self.__loader.colorPalettes.getColor("boxFontNormal"), justify = "center",
                                  textvariable=self.__tres, width=999999999,
                                  font=self.__normalFont
                              )
        self.__tresEntry.pack(side=TOP, anchor=N, fill=X)

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__tresEntry, "<FocusOut>"  , self.__tresChanged, 2)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__tresEntry, "<KeyRelease>", self.__tresChanged, 2)

        self.__boxButtonVal = IntVar()
        self.__boxButtonVal.set(self.__initMode)

        self.__boxButton = Checkbutton(self.__thresholdEntryFrame1, bg=self.__loader.colorPalettes.getColor("window"),
                                    fg=self.__loader.colorPalettes.getColor("boxFontNormal"), state = NORMAL,
                                    font=self.__smallFont, text=self.__dictionaries.getWordFromCurrentLanguage("initMode"),
                                    variable=self.__boxButtonVal
                                    )
        self.__boxButton.pack(side=BOTTOM, anchor=W, fill=X)

        self.__boxButtonVal2 = IntVar()
        self.__boxButtonVal2.set(self.__auto)

        self.__boxButton2 = Checkbutton(self.__thresholdEntryFrame3, bg=self.__loader.colorPalettes.getColor("window"),
                                    fg=self.__loader.colorPalettes.getColor("boxFontNormal"), state = NORMAL,
                                    font=self.__smallFont, text=self.__dictionaries.getWordFromCurrentLanguage("autoDetect"),
                                    variable=self.__boxButtonVal2
                                    )
        self.__boxButton2.pack(side=BOTTOM, anchor=W, fill=X)

        if self.__boxButtonVal.get() == False: self.__boxButton2.config(state = DISABLED)

        self.__setterFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 10, width = self.__sizes[0])
        self.__setterFrame.pack_propagate(False)
        self.__setterFrame.pack(side=TOP, anchor=N, fill=X)

        self.__setterFrame1 = Frame(self.__setterFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 10, width = self.__sizes[0] // 3)
        self.__setterFrame1.pack_propagate(False)
        self.__setterFrame1.pack(side=LEFT, anchor=E, fill=Y)

        self.__setterFrame2 = Frame(self.__setterFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 10, width = self.__sizes[0] // 3)
        self.__setterFrame2.pack_propagate(False)
        self.__setterFrame2.pack(side=LEFT, anchor=E, fill=Y)

        self.__setterFrame3 = Frame(self.__setterFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 10, width = self.__sizes[0] // 3)
        self.__setterFrame3.pack_propagate(False)
        self.__setterFrame3.pack(side=LEFT, anchor=E, fill=Y)

        self.__numLinesLabel = Label(self.__setterFrame1, text=self.__dictionaries.getWordFromCurrentLanguage("numOfLines"),
                                  bg = self.__loader.colorPalettes.getColor("window"),
                                  fg = self.__loader.colorPalettes.getColor("font"), justify = "center",
                                  font=self.__normalFont
                                  )
        self.__numLinesLabel.pack(side=TOP, anchor=N, fill=X)

        self.__numOfLinesVar      = StringVar()
        self.__numOfLinesVar.set(str(self.__numOfLines))
        self.__numOfLinesEntry    = Entry(self.__setterFrame1, text=self.__dictionaries.getWordFromCurrentLanguage("thresholdSetter"),
                                  bg = self.__loader.colorPalettes.getColor("boxBackNormal"),
                                  fg = self.__loader.colorPalettes.getColor("boxFontNormal"), justify = "center",
                                  textvariable=self.__numOfLinesVar, width=999999999,
                                  font=self.__normalFont
                              )
        self.__numOfLinesEntry.pack(side=TOP, anchor=N, fill=X)

        if self.__auto:
           self.__numOfLinesEntry.config(state = DISABLED)

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__numOfLinesEntry, "<FocusOut>"  , self.__tresChanged, 2)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__numOfLinesEntry, "<KeyRelease>", self.__tresChanged, 2)

        self.__boxButtonVal3 = IntVar()
        self.__boxButtonVal3.set(self.__repeatingOnTop)

        self.__boxButton3 = Checkbutton(self.__setterFrame2, bg=self.__loader.colorPalettes.getColor("window"),
                                    fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                    font=self.__normalFont, text=self.__dictionaries.getWordFromCurrentLanguage("repeatingIsOnTop2").replace("\\n", "\n"),
                                    variable=self.__boxButtonVal3
                                    )
        self.__boxButton3.pack(side=TOP, anchor=N, fill=Y)

        self.__pattenLabel = Label(self.__setterFrame3, text=self.__dictionaries.getWordFromCurrentLanguage("repeatingPattern"),
                                  bg = self.__loader.colorPalettes.getColor("window"),
                                  fg = self.__loader.colorPalettes.getColor("font"), justify = "center",
                                  font=self.__normalFont
                                  )
        self.__pattenLabel.pack(side=TOP, anchor=N, fill=X)

        from FortariMB import FortariMB

        if self.__auto:
           status = DISABLED
        else:
           status = NORMAL

        self.__repeatingPattern = FortariMB(self.__loader, self.__setterFrame3, status,
                                            self.__smallFont, self.__pattern, self.__patterns, False, False,
                                            self.selectedChanged, [self.__pattern])

        if self.__auto:
           self.__boxButton3.config(state = DISABLED)

        t1 = Thread(target=self.imageThread)
        t1.daemon = True
        t1.start()

        self.__loader.threadLooper.addToThreading(self, self.__loop, [], 2)

    def selectedChanged(self, event):
        if self.__pattern != self.__repeatingPattern.getValue():
           self.__pattern  = self.__repeatingPattern.getValue()
           self.generate2600Picture()

    def __numOfLinesChanged(self, event):
        val = self.__numOfLinesVar.get()
        entry = self.__numOfLinesEntry

        try:
            num = int(val)
        except:
            entry.config(bg=self.__colors.getColor("boxBackUnSaved"), fg=self.__colors.getColor("boxFontUnSaved"))
            return

        entry.config(bg=self.__colors.getColor("boxBackNormal"), fg=self.__colors.getColor("boxFontNormal"))

        if   num < 1  : num = 1
        elif num > 255: num = 255

        if self.__numOfLines != num:
           self.__numOfLines  = num
           self.generate2600Picture()

        self.__numOfLinesVar.set(str(num))
        entry.icursor(len(str(num)))

    def __loop(self):
        boxChange = False
        update    = False

        if self.__initMode != self.__boxButtonVal.get():
           self.__initMode  = self.__boxButtonVal.get()
           boxChange        = True

        if self.__auto     != self.__boxButtonVal2.get():
           self.__auto      = self.__boxButtonVal2.get()
           boxChange        = True

        if self.__repeatingOnTop != self.__boxButtonVal3.get():
           self.__repeatingOnTop  = self.__boxButtonVal3.get()
           boxChange        = True

        if boxChange:
           #print(self.__initMode, self.__auto, False == 0)
           if self.__initMode and self.__auto:
              self.__boxButton3.config(state      = DISABLED)
              self.__numOfLinesEntry.config(state = DISABLED)
              self.__repeatingPattern.changeState(DISABLED)

           elif self.__initMode and self.__auto == False:
              self.__boxButton2.config(state=NORMAL)
              self.__boxButton3.config(state=NORMAL)
              self.__numOfLinesEntry.config(state=NORMAL)
              self.__repeatingPattern.changeState(NORMAL)

           else:
              self.__auto = False
              self.__boxButtonVal2.set(0)
              self.__boxButton2.config(state      = DISABLED)
              self.__boxButton2.config(state      = DISABLED)
              self.__boxButton3.config(state      = DISABLED)
              self.__numOfLinesEntry.config(state = DISABLED)
              self.__repeatingPattern.changeState(DISABLED)

           update = True
           self.generate2600Picture()

    def __tresChanged(self, event):
        val = self.__tres.get()
        entry = self.__tresEntry

        try:
            num = int(val)
        except:
            entry.config(bg=self.__colors.getColor("boxBackUnSaved"), fg=self.__colors.getColor("boxFontUnSaved"))
            return

        entry.config(bg=self.__colors.getColor("boxBackNormal"), fg=self.__colors.getColor("boxFontNormal"))
        if num < 0:
            num = 0
        elif num > 85:
            num = 85

        if self.__tresConst != num:
            self.__tresConst = num
            self.convertImageAndReDrawCanvas()

        self.__tres.set(str(num))
        entry.icursor(len(str(num)))

    def imageThread(self):
        while(self.__imgLabel.winfo_width() < 2): sleep(0.00005)
        self.convertImageAndReDrawCanvas()

    def convertImageAndReDrawCanvas(self):
        self.__canvas.clipboard_clear()
        self.__canvas.delete("all")

        #self.__imageColors = self.__imageBackUp.load()
        i    = deepcopy(self.__imageBackUp)
        newH = round(self.__imgLabel.winfo_width() / i.width * i.height)
        i    = i.resize((self.__imgLabel.winfo_width(), newH), IMG.ANTIALIAS)

        self.__iConvertedLabel = ImageTk.PhotoImage(self.imageTo4Colors(i, self.__tresConst))
        self.__imgLabel.config(image = self.__iConvertedLabel)

        self.generate2600Picture()
        self.drawCanvas()

    def drawCanvas(self):
        self.__canvas.clipboard_clear()
        self.__canvas.delete("all")

        xUnit = self.__canvas.winfo_width()  // 48
        yUnit = self.__canvas.winfo_height() // self.__numOfLines

        start = (len(self.__colorData) - self.__numOfLines) // 2
        end   =  len(self.__colorData) - start

        order = ["BG", "PF", "P1", "P0"]
        for y in range(start, end):
            for item in order:
                colorLine = None
                for num in self.__colorData[y].keys():
                    if self.__colorData[y][num][3] == item:
                       colorLine = self.__colorData[y][num]
                       break

                if colorLine == None: continue

                c =  self.__colorDict.getHEXValueFromTIA(colorLine[2])

                if   item == "BG":
                     self.__canvas.create_rectangle(0, y * yUnit,
                                                   self.__canvas.winfo_width(), (y + 1) * yUnit,
                                                   outline="", fill=c)
                elif item == "PF":
                     for x in range(0, 12):
                         if colorLine[0][x] == 1:
                            self.__canvas.create_rectangle(x * 4 * xUnit, y * yUnit,
                                                        (x + 1) * 4 * xUnit, (y + 1) * yUnit,
                                                        outline="", fill=c)
                elif item in ["P0", "P1"]:
                     for x in range(0, 48):
                         if colorLine[0][x] == 1:
                             self.__canvas.create_rectangle(x * xUnit, y * yUnit,
                                                            (x + 1) * xUnit, (y + 1) * yUnit,
                                                            outline="", fill=c)


    def __drawTemp(self):
        xUnit = self.__canvas.winfo_width()  // 48
        yUnit = self.__canvas.winfo_height() // self.__numOfLines

        start = (len(self.__colorData) - self.__numOfLines) // 2
        end   =  len(self.__colorData) - start

        for y in range(start, end):
            for x in range(0, 48):
                for val in self.__colorData[y]:
                    if self.__colorData[y][val][0][x] == 1:
                       c = self.__colorDict.getHEXValueFromTIA(self.__colorData[y][val][2])
                       self.__canvas.create_rectangle(x * xUnit, y * yUnit,
                                                      (x + 1) * xUnit, (y + 1) * yUnit,
                                                      outline="", fill=c)
                       break

    def __setRulesAndReArrange(self):
        if self.__repeatingOnTop:
           repeating = "P0"
           simple    = "P1"
        else:
           repeating = "P1"
           simple    = "P0"

        for y in range(0, self.__h):
            elements            = ["P0", "P1", "PF", "BG"]
            values              = [0, 85, 170, 255]
            onesRepeating       = []
            onesBulky           = []

            rules = {}

            lineSettings = {}
            for val in values:
                if self.__colorData[y][val][0].count(1) == 0:
                   values.remove(val)

            for val in values:
                couldBeRepeatingPattern = deepcopy(self.__colorData[y][val][0])
                couldBePlayfield        = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

                step = 16
                for x in range(0, step):
                    vals = [self.__colorData[y][val][0][x             ],
                            self.__colorData[y][val][0][x +  step     ],
                            self.__colorData[y][val][0][x + (step * 2)]]

                    same =  []
                    for charNum in range(0, 3):
                        if self.__pattern[charNum] == "1":
                           same.append(vals[charNum])

                    newVal = 0
                    if same.count(1) == 0 or same.count(0) == 0:
                       newVal = same[0]
                    else:
                       if   self.__segmentMethod == "AND":
                            newVal = 0
                       elif self.__segmentMethod == "OR":
                            newVal = 1
                       elif self.__segmentMethod == "AVG":
                            newVal = round(sum(same) / len(same))

                    for charNum in range(0, 3):
                        if self.__pattern[charNum] == "1":
                            couldBeRepeatingPattern[(step * charNum) + x] = newVal
                        else:
                            couldBeRepeatingPattern[(step * charNum) + x] = 0

                step = 4
                for start in range(0, 48, step):
                    segment = self.__colorData[y][val][0][start: start + step]
                    if segment.count(1) == 0 or segment.count(0) == 0:
                       newVal = segment[0]
                    else:
                       if   self.__segmentMethod == "AND":
                           newVal = 0
                       elif self.__segmentMethod == "OR":
                           newVal = 1
                       elif self.__segmentMethod == "AVG":
                           newVal = round(sum(segment) / len(segment))

                    couldBePlayfield[start // step] = newVal

                lineSettings[val] = {}
                lineSettings[val]['couldBePlayfield']        = deepcopy(couldBePlayfield)
                lineSettings[val]['couldBeRepeatingPattern'] = deepcopy(couldBeRepeatingPattern)

                lineSettings[val]['bulky']     = False
                lineSettings[val]['repeating'] = False

                samePixelAsRepeated  = 0
                samePixelAsPlayfield = 0

                for x in range(0, 48):
                    pixel = self.__colorData[y][val][0][x]

                    if lineSettings[val]['couldBeRepeatingPattern'][x]  == pixel:
                       samePixelAsRepeated  += 1

                    if lineSettings[val]['couldBePlayfield'][x // 4]    == pixel:
                       samePixelAsPlayfield += 1

                if 48 - samePixelAsPlayfield <= self.__tolerance:
                   onesBulky.append(val)
                   lineSettings[val]['bulky'] = True

                if 48 - samePixelAsRepeated <= self.__tolerance:
                   onesRepeating.append(val)
                   lineSettings[val]['repeating'] = True

                lineSettings[val]["samePixelAsRepeated"]  = samePixelAsRepeated
                lineSettings[val]["samePixelAsPlayfield"] = samePixelAsPlayfield

            #print(onesBulky, onesRepeating, values)
                #print(y, val, samePixelAsRepeated, samePixelAsPlayfield)

            if len(onesRepeating) > 0 and len(values) > 1:
               largest    = 0
               largestOne = ""

               for val in onesRepeating:
                   if lineSettings[val]["samePixelAsRepeated"] > largest:
                      largest    = lineSettings[val]["samePixelAsRepeated"]
                      largestOne = val

               values.remove(largestOne)
               elements.remove(repeating)

               self.__colorData[y][largestOne][3] = repeating
               self.__colorData[y][largestOne][4] = True
               self.__colorData[y][largestOne][0] = deepcopy(lineSettings[largestOne]["couldBeRepeatingPattern"])
               rules[repeating] = largestOne

               if largestOne in onesBulky:
                  onesBulky.remove(largestOne)

            if len(onesBulky) > 0 and len(values) > 1:
               largest = 0
               largestOne = ""

               for val in onesBulky:
                    if lineSettings[val]["samePixelAsPlayfield"] > largest:
                        largest = lineSettings[val]["samePixelAsPlayfield"]
                        largestOne = val

               values.remove(largestOne)
               elements.remove("PF")
               self.__colorData[y][largestOne][3] = "PF"
               self.__colorData[y][largestOne][0] = deepcopy(lineSettings[largestOne]["couldBePlayfield"])
               rules["PF"] = largestOne

            if len(values) > 0:
               if len(values) > 1 and simple in elements:
                  largest = 0
                  largestOne = ""

                  for val in values:
                      colorAmp  = int("0x" + self.__colorData[y][val][2][2], 16) + 1
                      numberOf1 = self.__colorData[y][val][0].count(1)
                      errorNum  = 96 - (lineSettings[val]["samePixelAsRepeated"] + lineSettings[val]["samePixelAsPlayfield"])

                      thisVal   = (numberOf1 + errorNum) * (colorAmp / 2)

                      if thisVal > largest:
                         largest    = thisVal
                         largestOne = val

                  #print(largestOne, values)
                  values.remove(largestOne)
                  elements.remove(simple)
                  self.__colorData[y][largestOne][3] = simple
                  rules[simple] = largestOne

               if len(values) > 1 and repeating in elements:
                  if self.__repeatingOnTop == False:
                     largest = 0
                     largestOne = ""

                     for val in values:
                         overlapping = 0
                         for x in range(0, 48):
                             if lineSettings[val]["couldBeRepeatingPattern"][x] == self.__colorData[y][rules[simple]][0][x]:
                                overlapping += 1

                         if overlapping > largest:
                            largest    = overlapping
                            largestOne = val

                     if 48 - largest <= self.__tolerance:
                        elements.remove(repeating)
                        self.__colorData[y][largestOne][3] = repeating
                        self.__colorData[y][largestOne][4] = True
                        rules[repeating] = largestOne
                        self.__colorData[y][largestOne][0] = deepcopy(lineSettings[largestOne]["couldBeRepeatingPattern"])
                        values.remove(largestOne)

               else:
                   if repeating in elements:
                      elements.remove(repeating)

               if len(values) > 1 and "PF" in elements:
                   largest = 0
                   largestOne = ""

                   otherList = [simple, repeating]
                   if repeating not in rules.keys(): otherList.remove(repeating)
                   #print(rules, elements)

                   for val in values:
                       overlapping = 0
                       for x in range(0, 48):
                           for other in otherList:
                               if lineSettings[val]["couldBePlayfield"][x // 4] == self.__colorData[y][rules[other]][0][x]:
                                  overlapping += 1
                                  break

                       if overlapping > largest:
                           largest = overlapping
                           largestOne = val

                   if 48 - largest <= self.__tolerance:
                       elements.remove("PF")
                       values.remove(largestOne)
                       self.__colorData[y][largestOne][3] = "PF"
                       self.__colorData[y][largestOne][4] = True
                       rules["PF"] = largestOne
                       self.__colorData[y][largestOne][0] = deepcopy(lineSettings[largestOne]["couldBePlayfield"])

               if len(values) > 0 and len(elements) > 0:
                  self.__colorData[y][values[0]][3] = elements[0]
                  if elements[0] == "PF":
                     self.__colorData[y][values[0]][0] = deepcopy(lineSettings[values[0]]["couldBePlayfield"])

    def generate2600Picture(self):
        i                  = deepcopy(self.__imageBackUp)
        i                  = i.resize((self.__w, self.__h), IMG.ANTIALIAS)
        iConverted48Colors = i.load()
        iConverted48       = self.imageTo4Colors(i, self.__tresConst).load()

        self.__colorData = []

        if self.__auto:
           self.__numOfLines          = self.__h
           self.__numOfLinesVar.set(str(self.__h))

           self.__repeatingOnTop = False
           self.__boxButtonVal3.set(0)

           patternsFound = {}
           for y in range(0, self.__h):
               colorData = {
                   0: [],
                   85: [],
                   170: [],
                   255: []
               }

               for x in range(0, self.__w):
                   # if self.__iConverted48[x, y]   == 0
                   val = iConverted48[x, y][0]

                   for key in colorData:
                       if key == val:
                           colorData[key].append(1)
                       else:
                           colorData[key].append(0)

               for val in colorData.keys():
                   sections = [colorData[val][0:16], colorData[val][16:32], colorData[val][32:48]]

                   for pattern in self.__patterns:
                       test = [[], [], []]
                       numOfValids = 0
                       for charNum in range(0, 3):
                           if pattern[charNum] == '1':
                               test[charNum] = sections[charNum]
                               numOfValids += 1

                       nope = False

                       if numOfValids > 1:
                           firstNonEmpty = []
                           for sectionNum in range(0, 3):
                               if test[sectionNum] != []:
                                   firstNonEmpty = test[sectionNum]
                                   break

                           for sectionNum in range(0, 3):
                               if test[sectionNum] != firstNonEmpty and test[sectionNum] != []:
                                   nope = True
                                   break

                       for sectionNum in range(0, 3):
                           if test[sectionNum] == [] and sections[sectionNum].count(1) > 0:
                               nope = True
                               break

                       if nope: continue

                       for charNum in range(0, 3):
                           if pattern[charNum] == '0' and test[charNum] != []:
                               nope = True
                               break

                       if nope == False:
                           if pattern in patternsFound.keys():
                               patternsFound[pattern] += 1
                           else:
                               patternsFound[pattern] = 1

           # sorted(patternsFound, key=patternsFound.get)
           # print(patternsFound)

           strongest = ""
           strongestVal = 0

           for key in patternsFound:
               if patternsFound[key] > strongestVal:
                   strongest = key
                   strongestVal = patternsFound[key]
               elif patternsFound[key] == strongestVal:
                   if key[0] == key[2]:
                       strongest = key
                       strongestVal = patternsFound[key]

           self.__pattern = strongest
           self.__repeatingPattern.deSelect()
           self.__repeatingPattern.select(self.__pattern, True)

        else:
           pass

        for y in range(0, self.__h):
            colorData = {
                0  : [[], [], "", "", False],
                85 : [[], [], "", "", False],
                170: [[], [], "", "", False],
                255: [[], [], "", "", False]
            }

            for x in range(0, self.__w):
                #if self.__iConverted48[x, y]   == 0
                val = iConverted48[x, y][0]

                for key in colorData:
                    if key == val:
                       colorData[key][0].append(1)
                    else:
                       colorData[key][0].append(0)

                colorData[val][1].append(iConverted48Colors[x, y])

            for val in colorData:
                if len(colorData[val][1]) > 0:
                    dominant = self.__colorDict.getDominantColor(colorData[val][1])
                    try:
                        colorData[val][2] = self.__colorDict.getClosestTIAColor(dominant[0],
                                                                           dominant[2],
                                                                           dominant[1])
                    except:
                        print(colorData[val][1])
                else:
                    colorData[val][2] = "$00"

                    #print(colorData[val][2])
            #self.__setRulesOfLines(colorData)
            #self.__rearrengePatterns(colorData)
            self.__colorData.append(deepcopy(colorData))

        #self.__drawTemp()
        self.__setRulesAndReArrange()

        #self.__oneColorBG = False
        if self.__oneColorBG:
           bgColorsAmp  = []
           bgColorsBase = {}
           for line in self.__colorData:
               for val in line.keys():
                   if line[val][3] == "BG" and line[val][0].count(1) > 0:
                      #bgColorsBase.append(line[val][2][1])
                      if line[val][2][1] not in bgColorsBase.keys():
                         bgColorsBase[line[val][2][1]]  = 1
                      else:
                         bgColorsBase[line[val][2][1]] += 1

                      bgColorsAmp.append(int("0x" + line[val][2][2], 16))

           largest    = 0
           largestOne = ""
           #sorted(bgColorsBase, key = bgColorsBase.get)
           for key in bgColorsBase.keys():
               if bgColorsBase[key] > largest:
                  largest    = bgColorsBase[key]
                  largestOne = key

           avg = round(sum(bgColorsAmp) / len(bgColorsAmp))

           thatColor = "$" + largestOne + hex(avg).replace("0x","").upper()
           for line in self.__colorData:
               for val in line.keys():
                   if line[val][3] == "BG":
                      line[val][2]  = thatColor


    def imageTo4Colors(self, image, tres):
        i = deepcopy(image)

        fn1 = lambda x: 255 if x > tres       else 0
        fn2 = lambda x: 255 if x > tres + 85  else 0
        fn3 = lambda x: 255 if x > tres + 170 else 0

        altImage1 = deepcopy(i).convert('L').point(fn1, mode='1')
        altImage2 = deepcopy(i).convert('L').point(fn2, mode='1')
        altImage3 = deepcopy(i).convert('L').point(fn3, mode='1')

        pixels1 = altImage1.load()
        pixels2 = altImage2.load()
        pixels3 = altImage3.load()

        w, h = i.size

        pixels  = []

        for y in range(0, h):
            for x in range(0, w):
                value = (pixels1[x, y] + pixels2[x, y]+ pixels3[x, y]) // 3
                pixels.append(value)
                pixels.append(value)
                pixels.append(value)

        return IMG.frombytes("RGB", (w, h), bytes(pixels))