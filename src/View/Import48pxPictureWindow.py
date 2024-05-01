from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from time import sleep
from PIL import Image as IMG, ImageTk, ImageOps
import os

class Import48pxPictureWindow:

    def __init__(self, loader, frameNum, numOfLines, repeatingOnTop, pattern, patterns):
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

        self.__sizes = [self.__screenSize[0] // 2.25, self.__screenSize[1] // 1.40]

        if frameNum == 1:
           initMode = True
        else:
           initMode = False

        self.__initMode       = initMode
        self.__wasInit        = initMode
        self.__auto           = initMode
        self.__oneColorBG     = False

        self.__numOfLines     = numOfLines
        self.__repeatingOnTop = repeatingOnTop
        self.__patterns       = patterns
        self.__pattern        = pattern
        self.__w              = 48
        self.__tolerance      = 8
        self.__segmentMethod  = "AVG"
        self.__segmentMethods = ["AND", "OR", "AVG"]
        self.__finished       = True
        self.__invert         = False
        self.__forceBlack     = False

        self.__tresConst      = 42
        self.__doHole         = True
        #self.__holers         = (4, 5, 6, 7)
        self.__holers = (0, 1, 10, 11)

        self.__skipNum = 0

        formats = ["bmp", "dds", "eps", "gif", "dib", "ico", "jpg", "jpeg", "pcx", "png", "tga", "tiff", "pdf"]

        self.answer = self.__fileDialogs.askForFileName("loadPicture",
                                                        False, [formats, "*"], self.__mainWindow.projectPath)

        self.result = None

        if self.answer != "" and os.path.exists(self.answer) == True:
           self.__imageBackUp = IMG.open(self.answer, "r")
           if self.__imageBackUp.mode != "RGB":
              self.__imageBackUp       = self.__imageBackUp.convert("RGB")

           w, h     = self.__imageBackUp.size
           self.__h = round((self.__w / w) * h)
           if self.__h > 255: self.__h = 255

           #self.__imageBackUp = self.__imageBackUp.resize((self.__w, self.__h), IMG.ANTIALIAS)

           self.__window = SubMenu(self.__loader, "loadPicture", self.__sizes[0], self.__sizes[1], None, self.__addElements,
                                2)
        else:
           self.__loader.mainWindow.editor.attributes('-disabled', True)
           self.__loader.topLevels[-1].focus_force()

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
                                 height=self.__sizes[1] // 12, width = self.__sizes[0])
        self.__setterFrame.pack_propagate(False)
        self.__setterFrame.pack(side=TOP, anchor=N, fill=X)

        self.__setterFrame1 = Frame(self.__setterFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 12, width = self.__sizes[0] // 3)
        self.__setterFrame1.pack_propagate(False)
        self.__setterFrame1.pack(side=LEFT, anchor=E, fill=Y)

        self.__setterFrame2 = Frame(self.__setterFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 12, width = self.__sizes[0] // 3)
        self.__setterFrame2.pack_propagate(False)
        self.__setterFrame2.pack(side=LEFT, anchor=E, fill=Y)

        self.__setterFrame3 = Frame(self.__setterFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 12, width = self.__sizes[0] // 3)
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

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__numOfLinesEntry, "<FocusOut>"  , self.__numOfLinesChanged, 2)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__numOfLinesEntry, "<KeyRelease>", self.__numOfLinesChanged, 2)

        self.__boxButtonVal3 = IntVar()
        self.__boxButtonVal3.set(self.__repeatingOnTop)

        self.__boxButton3 = Checkbutton(self.__setterFrame2, bg=self.__loader.colorPalettes.getColor("window"),
                                    fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                    font=self.__normalFont, text=self.__dictionaries.getWordFromCurrentLanguage("repeatingIsOnTop2").replace("\\n", "\n"),
                                    variable=self.__boxButtonVal3
                                    )
        self.__boxButton3.pack(side=TOP, anchor=CENTER, fill=Y)

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

        self.__setterFrame_ = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 12, width = self.__sizes[0])
        self.__setterFrame_.pack_propagate(False)
        self.__setterFrame_.pack(side=TOP, anchor=N, fill=X)

        self.__setterFrame4 = Frame(self.__setterFrame_, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 12, width = self.__sizes[0] // 3)
        self.__setterFrame4.pack_propagate(False)
        self.__setterFrame4.pack(side=LEFT, anchor=E, fill=Y)

        self.__setterFrame5 = Frame(self.__setterFrame_, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 12, width = self.__sizes[0] // 3)
        self.__setterFrame5.pack_propagate(False)
        self.__setterFrame5.pack(side=LEFT, anchor=E, fill=Y)

        self.__setterFrame6 = Frame(self.__setterFrame_, bg=self.__loader.colorPalettes.getColor("window"),
                                 height=self.__sizes[1] // 12, width = self.__sizes[0] // 3)
        self.__setterFrame6.pack_propagate(False)
        self.__setterFrame6.pack(side=LEFT, anchor=E, fill=Y)

        self.__toleranceVar  = StringVar()
        self.__boxButtonVal4 = IntVar()

        #self.__boxButtonVal4.set(self.__oneColorBG)
        self.__toleranceVar.set(str(self.__tolerance))

        """
        self.__boxButton4 = Checkbutton(self.__setterFrame5, bg=self.__loader.colorPalettes.getColor("window"),
                                    fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                    font=self.__normalFont, text=self.__dictionaries.getWordFromCurrentLanguage("oneColor2").replace("\\n", "\n"),
                                    variable=self.__boxButtonVal4
                                    )
        self.__boxButton4.pack(side=TOP, anchor=CENTER, fill=Y)
        """

        self.__errorToleranceLabel = Label(self.__setterFrame4, text=self.__dictionaries.getWordFromCurrentLanguage("eTolerance"),
                                  bg = self.__loader.colorPalettes.getColor("window"),
                                  fg = self.__loader.colorPalettes.getColor("font"), justify = "center",
                                  font=self.__normalFont
                                  )
        self.__errorToleranceLabel.pack(side=TOP, anchor=N, fill=X)

        self.__errorToleranceEntry    = Entry(self.__setterFrame4, text=self.__dictionaries.getWordFromCurrentLanguage("thresholdSetter"),
                                  bg = self.__loader.colorPalettes.getColor("boxBackNormal"),
                                  fg = self.__loader.colorPalettes.getColor("boxFontNormal"), justify = "center",
                                  textvariable=self.__toleranceVar, width=999999999,
                                  font=self.__normalFont
                              )
        self.__errorToleranceEntry.pack(side=TOP, anchor=N, fill=X)

        if self.__auto:
           self.__numOfLinesEntry.config(state = DISABLED)
           #self.__boxButton4.config(state = DISABLED)

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__errorToleranceEntry, "<FocusOut>"  , self.__eTorChanged, 2)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__errorToleranceEntry, "<KeyRelease>", self.__eTorChanged, 2)

        self.__segmentLabel = Label(self.__setterFrame6, text=self.__dictionaries.getWordFromCurrentLanguage("segmentMethod"),
                                  bg = self.__loader.colorPalettes.getColor("window"),
                                  fg = self.__loader.colorPalettes.getColor("font"), justify = "center",
                                  font=self.__normalFont
                                  )
        self.__segmentLabel.pack(side=TOP, anchor=N, fill=X)

        self.__segmentSetter = FortariMB(self.__loader, self.__setterFrame6, status,
                                            self.__smallFont, self.__segmentMethod, self.__segmentMethods, False, False,
                                            self.selectedChanged2, [self.__segmentMethod])

        self.__setterFrame__ = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"),
                                    height=self.__sizes[1] // 12, width=self.__sizes[0])
        self.__setterFrame__.pack_propagate(False)
        self.__setterFrame__.pack(side=TOP, anchor=N, fill=BOTH)

        self.__setterFrame7 = Frame(self.__setterFrame__, bg=self.__loader.colorPalettes.getColor("window"),
                                    height=self.__sizes[1] // 12, width=self.__sizes[0] // 3)
        self.__setterFrame7.pack_propagate(False)
        self.__setterFrame7.pack(side=LEFT, anchor=E, fill=Y)

        self.__setterFrame8 = Frame(self.__setterFrame__, bg=self.__loader.colorPalettes.getColor("window"),
                                    height=self.__sizes[1] // 12, width=self.__sizes[0] // 3)
        self.__setterFrame8.pack_propagate(False)
        self.__setterFrame8.pack(side=LEFT, anchor=E, fill=Y)

        self.__setterFrame9 = Frame(self.__setterFrame__, bg=self.__loader.colorPalettes.getColor("window"),
                                    height=self.__sizes[1] // 12, width=self.__sizes[0] // 3)
        self.__setterFrame9.pack_propagate(False)
        self.__setterFrame9.pack(side=LEFT, anchor=E, fill=Y)

        self.__okButton = Button(self.__setterFrame8,
                                    bg=self.__loader.colorPalettes.getColor("window"),
                                    fg=self.__loader.colorPalettes.getColor("font"),
                                    activebackground=self.__loader.colorPalettes.getColor("highLight"),
                                    activeforeground=self.__loader.colorPalettes.getColor("font"),
                                    text=self.__dictionaries.getWordFromCurrentLanguage("ok"),
                                    font=self.__normalFont, command=self.saveToData
                                    )
        self.__okButton.pack_propagate(False)
        self.__okButton.pack(side=BOTTOM, anchor=S, fill=BOTH)

        """
        self.__boxButtonVal5 = IntVar()
        self.__boxButtonVal6 = IntVar()

        self.__boxButtonVal5.set(self.__invert)
        self.__boxButtonVal5.set(self.__forceBlack)

        self.__boxButton5 = Checkbutton(self.__setterFrame7, bg=self.__loader.colorPalettes.getColor("window"),
                                        fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                        font=self.__normalFont,
                                        text=self.__dictionaries.getWordFromCurrentLanguage("invertColors").replace("\\n",
                                                                                                                 "\n"),
                                        variable=self.__boxButtonVal5
                                        )
        self.__boxButton5.pack(side=TOP, anchor=CENTER, fill=Y)

        self.__boxButton6 = Checkbutton(self.__setterFrame9, bg=self.__loader.colorPalettes.getColor("window"),
                                        fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                        font=self.__normalFont,
                                        text=self.__dictionaries.getWordFromCurrentLanguage("forceBlack").replace("\\n",
                                                                                                                 "\n"),
                                        variable=self.__boxButtonVal6
                                        )
        self.__boxButton6.pack(side=TOP, anchor=CENTER, fill=Y)


        if self.__auto:
           self.__boxButton5.config(state = DISABLED)
           self.__boxButton6.config(state = DISABLED)

        """

        t1 = Thread(target=self.imageThread)
        t1.daemon = True
        t1.start()

        self.__loader.threadLooper.addToThreading(self, self.__loop, [], 2)

    def saveToData(self):
        start = (len(self.__colorData) - self.__numOfLines) // 2
        end   =  len(self.__colorData) - start

        data = deepcopy(self.__colorData[start:end])

        self.result = {
            "numberOfLines"   : self.__numOfLines,
            "data"            : data,
            "repeatingOnTop"  : self.__repeatingOnTop,
            "repeatPattern"   : self.__pattern
        }

        self.__closeWindow()

    def selectedChanged2(self):
        if self.__segmentMethod != self.__segmentSetter.getSelected():
           self.__segmentMethod  = self.__segmentSetter.getSelected()
           self.gen2600()

    def __eTorChanged(self, event):
        val = self.__toleranceVar.get()
        entry = self.__errorToleranceEntry

        try:
            num = int(val)
        except:
            entry.config(bg=self.__colors.getColor("boxBackUnSaved"), fg=self.__colors.getColor("boxFontUnSaved"))
            return

        entry.config(bg=self.__colors.getColor("boxBackNormal"), fg=self.__colors.getColor("boxFontNormal"))
        if num < 0:
            num = 0
        elif num > 48:
            num = 48

        if self.__tolerance != num:
            self.__tolerance = num
            self.gen2600()

        self.__toleranceVar.set(str(num))
        entry.icursor(len(str(num)))

    def selectedChanged(self):
        if self.__pattern != self.__repeatingPattern.getSelected():
           self.__pattern  = self.__repeatingPattern.getSelected()
           self.gen2600()

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
        elif num > self.__h: num = self.__h

        if self.__numOfLines != num:
           self.__numOfLines  = num
           self.gen2600()

        self.__numOfLinesVar.set(str(num))
        entry.icursor(len(str(num)))

    def __loop(self):
        boxChange = False
        update    = False

        try:
            if self.__finished:
               self.__okButton.config(state = NORMAL)
            else:
               self.__okButton.config(state = DISABLED)

            if self.__initMode != self.__boxButtonVal.get():
               self.__initMode  = self.__boxButtonVal.get()
               boxChange        = True

            if self.__auto     != self.__boxButtonVal2.get():
               self.__auto      = self.__boxButtonVal2.get()
               boxChange        = True

            if self.__repeatingOnTop != self.__boxButtonVal3.get():
               self.__repeatingOnTop  = self.__boxButtonVal3.get()
               boxChange        = True

            if self.__oneColorBG != self.__boxButtonVal4.get():
               self.__oneColorBG  = self.__boxButtonVal4.get()
               boxChange        = True

            #if self.__invert != self.__boxButtonVal5.get():
            #   self.__invert  = self.__boxButtonVal5.get()
            #   boxChange        = True

            #if self.__forceBlack != self.__boxButtonVal6.get():
            #   self.__forceBlack  = self.__boxButtonVal6.get()
            #   boxChange        = True

            if boxChange:
               #print(self.__initMode, self.__auto, False == 0)
               if self.__initMode and self.__auto:
                  self.__boxButton3.config(state      = DISABLED)
                  self.__numOfLinesEntry.config(state = DISABLED)
                  self.__repeatingPattern.changeState(DISABLED)
                 # self.__boxButton5.config(state      = DISABLED)
                 # self.__boxButton6.config(state      = DISABLED)
                  self.__segmentSetter.changeState(DISABLED)

               elif self.__initMode and self.__auto == False:
                  self.__boxButton2.config(state=NORMAL)
                  self.__boxButton3.config(state=NORMAL)
                  self.__numOfLinesEntry.config(state=NORMAL)
                  self.__repeatingPattern.changeState(NORMAL)
                #  self.__boxButton5.config(state      = NORMAL)
                #  self.__boxButton6.config(state      = NORMAL)
                  self.__segmentSetter.changeState(NORMAL)
               else:
                  self.__auto = False
                  self.__boxButtonVal2.set(0)
                  self.__boxButton2.config(state      = DISABLED)
                  self.__boxButton3.config(state      = DISABLED)
                  self.__numOfLinesEntry.config(state = DISABLED)
                  self.__repeatingPattern.changeState(DISABLED)
                #  self.__boxButton5.config(state      = DISABLED)
                #  self.__boxButton6.config(state      = DISABLED)
                  self.__segmentSetter.changeState(DISABLED)

               update = True
               self.gen2600()
        except Exception as e:
            print(str(e))

    def gen2600(self):
        t = Thread(target=self.generate2600Pic)
        t.daemon = True
        t.start()

    def generate2600Pic(self):
        while (self.__finished == False): sleep(0.0005)
        self.__finished = False
        self.__okButton.config(state=DISABLED)

        self.generate2600Picture()
        self.drawCanvas()

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

            t1 = Thread(target=self.imageThread)
            t1.daemon = True
            t1.start()

        self.__tres.set(str(num))
        entry.icursor(len(str(num)))

    def imageThread(self):
        while (self.__finished == False): sleep(0.0005)
        self.__finished = False
        self.__okButton.config(state=DISABLED)

        while(self.__imgLabel.winfo_width() < 2): sleep(0.0005)

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
        #print(self.__oneColorBG, self.__forceBlack)

        self.drawCanvas()

    def drawCanvas(self):
        self.__canvas.clipboard_clear()
        self.__canvas.delete("all")

        xUnit = self.__canvas.winfo_width()  // 48
        yUnit = self.__canvas.winfo_height() // self.__numOfLines

        start = (len(self.__colorData) - self.__numOfLines) // 2
        end   =  len(self.__colorData) - start

        #order   = ["BG", "PF", "P1", "P0"]
        order = ["PF", "P1", "P0"]
        actualY = -1
        for y in range(start, end):
            actualY += 1
            for item in order:
                colorLine = None
                for num in self.__colorData[y].keys():
                    if self.__colorData[y][num][3] == item:
                       colorLine = self.__colorData[y][num]
                       break

                if colorLine == None: continue

                c =  self.__colorDict.getHEXValueFromTIA(colorLine[2])

                if   item == "BG":
                     self.__canvas.create_rectangle(0, actualY * yUnit,
                                                   self.__canvas.winfo_width(), (actualY + 1) * yUnit,
                                                   outline="", fill=c)
                elif item == "PF":
                     for x in range(0, 12):
                         if x in self.__holers and self.__doHole: continue

                         if colorLine[0][x] == 1:
                            self.__canvas.create_rectangle(x * 4 * xUnit, actualY * yUnit,
                                                        (x + 1) * 4 * xUnit, (actualY + 1) * yUnit,
                                                        outline="", fill=c)
                elif item in ["P0", "P1"]:
                     for x in range(0, 48):
                         if colorLine[0][x] == 1:
                             self.__canvas.create_rectangle(x * xUnit, actualY * yUnit,
                                                            (x + 1) * xUnit, (actualY + 1) * yUnit,
                                                            outline="", fill=c)

        self.__finished = True
        self.__okButton.config(state=NORMAL)

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
            hasHolers           = []
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
                
                countInHoles = 0

                for index in self.__holers:
                    if self.__colorData[y][val][0][index] == 1: countInHoles += 1
                
                lineSettings[val]['hasHole']  =  countInHoles <= self.__tolerance // 4
                lineSettings[val]['holeVal']  = self.__colorData[y][val][0][20:28].count(1)

                if lineSettings[val]['hasHole']: hasHolers.append(val)
                #print(lineSettings[val]['hasHole'])

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

            becamePF = False

            if len(hasHolers) > 0 and len(values) > 1 and self.__doHole:
               least    = 8
               leastOne = ""
               bulky    = False
               rep      = False

               for val in hasHolers:
                   if lineSettings[val]["holeVal"] < least:
                      least    = lineSettings[val]["holeVal"]
                      bulky    = val in onesBulky
                      rep      = val in onesRepeating
                      leastOne = val


               if leastOne != "":
                   values.remove(leastOne)
                   elements.remove("PF")
                   hasHolers.remove(leastOne)
                   if bulky: onesBulky    .remove(leastOne)
                   if rep  : onesRepeating.remove(leastOne)

                   self.__colorData[y][leastOne][3] = "PF"
                   self.__colorData[y][leastOne][0] = deepcopy(lineSettings[leastOne]["couldBePlayfield"])
                   rules["PF"] = leastOne
                   becamePF = leastOne
                   xXx      = 0

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

            if len(onesBulky) > 0 and len(values) > 1 and "PF" in elements:
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
               becamePF = largestOne
               xXx      = 1

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
                       becamePF = largestOne
                       xXx      = 2

               if len(values) > 0 and len(elements) > 0:
                  self.__colorData[y][values[0]][3] = elements[0]
                  if elements[0] == "PF":
                     self.__colorData[y][values[0]][0] = deepcopy(lineSettings[values[0]]["couldBePlayfield"])
                     becamePF = values[0]
                     xXx = 3

            if self.__doHole:
                for key in self.__colorData[y].keys():
                   if self.__colorData[y][key][3] == "PF":
                      for index in self.__holers:
                          self.__colorData[y][key][0][index] = 0
               #else:
               #   print("OK", xXx)

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

        wasFirst = False
        if self.__first or self.__auto:
            if self.__first:
               self.__first = False
               wasFirst     = True
            self.__setAutoMergeMethodAndBackground()

        self.__setRulesAndReArrange()
        if self.__forceBlack or self.__invert or self.__auto or wasFirst:
           self.__swapPFBG()

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

    def __swapPFBG(self):
        if self.__auto:
           self.__invert     = False
           self.__forceBlack = False

           swappable = 0
           black     = 0
           all       = 0
           for y in range(0, self.__h):
               BG = None
               PF = None
               for val in self.__colorData[y].keys():
                   if self.__colorData[y][val][3] == "PF":
                       PF = self.__colorData[y][val]
                   elif self.__colorData[y][val][3] == "BG":
                       BG = self.__colorData[y][val]

                   if PF != None and BG != None:
                       break

               if PF != None and BG != None:
                   bgColor = PF[2]
                   pfColor = BG[2]
                   pfData  = PF[0]
                   all    += 1

                   if (pfColor != "$00" and bgColor == "$00"):
                       black += 1
                       continue

                   if pfData.count(0) > len(pfData) // 2:
                      swappable += 1
                      continue

           if swappable > all // 2:
              self.__invert = True
           if black > all // 2:
              self.__forceBlack = True

           #self.__boxButtonVal5.set(self.__invert)
           #self.__boxButtonVal6.set(self.__forceBlack)


        if self.__auto == False and self.__forceBlack == False:
           return

        for y in range(0, self.__h):
            BG = None
            PF = None
            for val in self.__colorData[y].keys():
                if   self.__colorData[y][val][3] == "PF":
                     PF = self.__colorData[y][val]
                elif self.__colorData[y][val][3] == "BG":
                     BG = self.__colorData[y][val]

                if PF != None and BG != None:
                   break

            if PF != None and BG != None:
               bgColor = PF[2]
               pfColor = BG[2]
               pfData  = PF[0]

               if (pfColor != "$00" and bgColor == "$00" and self.__forceBlack) or self.__invert:
                  PF[2]   = pfColor
                  BG[2]   = bgColor

                  for x in range(0, len(pfData)):
                      pfData[x] = 1 - pfData[x]


    def __setAutoMergeMethodAndBackground(self):
        colors     = {}
        forMerging = [0, 0, 0]

        for y in range(0, self.__h):
            for val in self.__colorData[y].keys():
                if self.__colorData[y][val][0].count(1) > 1:
                   if val not in colors:
                      colors[val]     = []

                   if self.__colorData[y][val][0].count(1) > 0:
                      colors[val].append(self.__colorData[y][val][2])

                   for methodNum in range(0, len(self.__segmentMethods)):
                       method = self.__segmentMethods[methodNum]
                       segmentsRepeat = []
                       #    self.__colorData[y][val][0][0 :16],
                       #    self.__colorData[y][val][0][16:32],
                       #    self.__colorData[y][val][0][32:48]
                       #]

                       for number in range(0, 3):
                           if self.__pattern[number] == "1":
                              segmentsRepeat.append(self.__colorData[y][val][0][number * 16 : (number + 1) + 16])

                       segmentsPF = []
                       for startX in range(0, 48, 4):
                           segmentsPF.append(self.__colorData[y][val][0][startX : startX + 4])

                       if len(segmentsRepeat) > 1:
                          for x in range(0, 16):
                              pixels = []
                              for segment in segmentsRepeat:
                                  pixels.append(segment[x])

                              if pixels.count(1) > 1 and pixels.count(0) > 1:
                                 value = 0
                                 if   method == "AVG":
                                      value = round(sum(pixels) / len(pixels))
                                 elif method == "AND":
                                      if pixels.count(0) == 0:
                                         value = 1
                                      else:
                                         value = 0
                                 elif method == "OR":
                                      if pixels.count(1) == 0:
                                         value = 0
                                      else:
                                         value = 1

                                 forMerging[methodNum] += pixels.count(value)

                       for segmentNum in range(0, 12):
                           pixels = segmentsPF[segmentNum]
                           if pixels.count(1) > 1 and pixels.count(0) > 1:
                               value = 0
                               if method == "AVG":
                                   value = round(sum(pixels) / len(pixels))
                               elif method == "AND":
                                   if pixels.count(0) == 0:
                                       value = 1
                                   else:
                                       value = 0
                               elif method == "OR":
                                   if pixels.count(1) == 0:
                                       value = 0
                                   else:
                                       value = 1

                               forMerging[methodNum] += pixels.count(value)

        largest    = 0
        largestOne = ""
        for methodNum in range(0, len(self.__segmentMethods)):
            method = self.__segmentMethods[methodNum]

            if forMerging[methodNum] > largest:
               forMerging[methodNum] = largest
               largestOne            = method

        self.__segmentMethod = largestOne
        self.__segmentSetter.deSelect()
        self.__segmentSetter.select(self.__segmentMethod, True)
        #print(self.__segmentMethod)


        """"

        self.__oneColorBG = False
        for val in colors.keys():
            temp = {}
            numOfKeys = 0
            for c in colors[val]:
                key = c[1] + hex(int("0x" + c[2], 16) // (self.__tolerance // 2 + 1)).replace("0x", "").upper()
                if key not in temp.keys():
                   temp[key]  = 1
                   numOfKeys += 1
                else:
                   temp[key] += 1

            largest    = 0
            largestOne = ""

            for key in temp:
                if temp[key] > largest:
                   largest    = temp[key]
                   largestOne = key

            if numOfKeys == 0: continue

            #print(largest, numOfKeys, temp.keys())
            if largest / numOfKeys > 0.9:
              self.__oneColorBG = True
              break

        #print(self.__oneColorBG, self.__segmentMethod)

        self.__boxButtonVal4.set(self.__oneColorBG)
        """

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