from tkinter import *
from ScreenSetterFrameBase import ScreenSetterFrameBase

class Indicator:

    def __init__(self, loader, baseFrame, data, changeName, changeData, w, h, currentBank, blankAnimation, topLevelWindow, itemNames):
        self.__loader = loader
        self.__baseFrame = baseFrame
        self.__data = data.split(" ")
        self.__w = w
        self.__h = h
        self.__currentBank = currentBank
        self.__changeData = changeData
        self.__topLevelWindow = topLevelWindow

        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs
        self.__fontManager = self.__loader.fontManager
        self.__fontSize = int(self.__screenSize[0] / 1300 * self.__screenSize[1] / 1050 * 14)
        self.__colors = self.__loader.colorPalettes
        self.__colorDict = self.__loader.colorDict

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize * 0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize * 0.65), False, False, False)
        self.__bigFont = self.__fontManager.getFont(int(self.__fontSize * 1.15), False, False, False)
        self.__bigFont2 = self.__fontManager.getFont(int(self.__fontSize * 1.5), False, False, False)

        self.__name = StringVar()
        self.__name.set(self.__data[0])
        self.__lastSelected = None

        self.dead = [False]
        self.stopMe = True
        self.__mode = self.__data[1]
        self.__delay = 0

        self.__setterBase = ScreenSetterFrameBase(loader, baseFrame, data, self.__name, changeName, self.dead, itemNames)
        self.__addElements()

    def __addElements(self):
        self.__uniqueFrame = Frame(self.__baseFrame, width=self.__w,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h)

        self.__uniqueFrame.pack_propagate(False)
        self.__uniqueFrame.pack(side=TOP, anchor=N, fill=X)

        self.__indicators = []
        import os

        groot = os.getcwd() + "\src\View\ScreenElements\Indicators"
        if  self.__mode == "SpecialEffect":
            groot = os.getcwd() + "\src\View\ScreenElements\SpecialEffects"

        #print(groot)
        for root, dirs, files in os.walk(groot):
            for file in files:
                if root == groot and "py" in file:
                    self.__indicators.append(file[:-3])
        #print(indicators)
        self.__indicators.sort()

        self.__label1 = Label(self.__uniqueFrame,
                                   text=self.__dictionaries.getWordFromCurrentLanguage("indicatorTyp")+":",
                                   font=self.__normalFont, fg=self.__colors.getColor("font"),
                                   bg=self.__colors.getColor("window"), justify=CENTER
                                   )

        self.__label1.pack_propagate(False)
        self.__label1.pack(side=TOP, anchor=CENTER, fill=X)

        self.__listFrame = Frame(self.__uniqueFrame, width=self.__w,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 height=round(self.__h // 10 * 2.5))

        self.__listFrame.pack_propagate(False)
        self.__listFrame.pack(side=TOP, anchor=N, fill=X)

        self.__indicatorListScrollBar = Scrollbar(self.__listFrame)
        self.__indicatorListBox = Listbox(self.__listFrame, width=100000,
                                    height=1000,
                                    yscrollcommand=self.__indicatorListScrollBar.set,
                                    selectmode=BROWSE,
                                    exportselection=False,
                                    font=self.__normalFont,
                                    justify=LEFT
                                    )

        self.__indicatorListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__indicatorListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__indicatorListBox.pack_propagate(False)

        self.__indicatorListScrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__indicatorListBox.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__indicatorListScrollBar.config(command=self.__indicatorListBox.yview)
        for var in self.__indicators:
            self.__indicatorListBox.insert(END, var)

        self.__indicatorListBox.select_clear(0, END)

        if self.__mode == "Indicator":
            from FullBar             import FullBar
            from HalfBarWithText     import HalfBarWithText
            from TwoIconsTwoLines    import TwoIconsTwoLines
            from OneIconWithDigits   import OneIconWithDigits
            from SevenDigits         import SevenDigits
            from TwelveIconsOrDigits import TwelveIconsOrDigits
            from DigitClock          import DigitClock

            self.screenSubs = {
                "FullBar"             : [FullBar,             ["#", "255", "$40|$30|$10", "1", "0"]],
                "HalfBarWithText"     : [HalfBarWithText,     ["#", "255", "$40", "1", "$06" ,"Health:", "0", "0"]],
                "TwoIconsTwoLines"    : [TwoIconsTwoLines,    ["#", "$40", "%00000000", "255", "#", "$80", "%00000000", "255", "1", "#", "#", "0", "0", "0"]],
                "OneIconWithDigits"   : [OneIconWithDigits,   ["#", "$16", "%00000000", "2", "#", "#", "default", "1"]],
                "SevenDigits"         : [SevenDigits,         ["#", "#", "#", "#", "#", "#", "#", "7", "0", "1", "$16", "default"]],
                "TwelveIconsOrDigits" : [TwelveIconsOrDigits, ["#", "#", "$06", "#", "1", "1", "%00000000", "0"]],
                "DigitClock"          : [DigitClock,          ["#", "#", "#", "$16", "default", "1", "32", "1"]]
            }
        elif self.__mode == "SpecialEffect":

            from Smoke        import Smoke
            from Fire         import Fire
            from DayTime      import DayTime
            from Space        import Space
            from Gradient     import Gradient
            from WaterWaves   import WaterWaves
            from SnowFlakes   import SnowFlakes
            from _3DLandScape import _3DLandScape
            from Earth        import Earth
            from BlinkingText import BlinkingText

            self.screenSubs = {
                "Smoke"                 : [Smoke,           ["#", "$02", "$74",
                                                             "$0a|$0a|$08|$0a|$0a|$08|$08|$06|$08|$06|$08|$06|$04|$04|$02|$00",
                                                             "$00|$00|$02|$00|$02|$04|$06|$06|$06|$04|$02|$02|$00|$02|$00|$00"
                                                             ]],
                "Fire"                  : [Fire,           ["#", "2", "6",
                                                            "$42|$44|$48|$36|$3a|$18|$1c|$1e|$1e|$1c|$18|$3a|$36|$48|$44|$42|$42|$44|$48|$36|$3a|$18|$1c|$1e|$1e|$1c|$18|$3a|$36|$48|$44|$42"
                                                            ]],
                "DayTime"              : [DayTime,        ["36", "#", "#", "#", "1", "1"
                                                            ]],
                "Space"                : [Space,          ["#", "%01111010"]],
                "Gradient"             : [Gradient,       ["#", "15", "$FF", "#", "1", "1"]],
                "WaterWaves"           : [WaterWaves,     ["#", "$80", "$0E|$0C|$0A|$08|$06|$04", "3"]],
                "SnowFlakes"           : [SnowFlakes,     ["#", "$00|$80", "#", "16", "#"]],
                "_3DLandScape"         : [_3DLandScape,   ["#", "$40", "8", "16", "#", "2"]],
                "Earth"                : [Earth,          ["#", "$D8", "#"]],
                "BlinkingText"         : [BlinkingText,   ["#", "#", "$16", "$42", "2", "#", "#", "0"*512]]
            }


        if self.__data[2]  in ("#", "$"):
           self.__data[2]  = self.__indicators[0]
           self.__indicatorListBox.select_set(0)
           self.__indicatorListBox.yview(0)

           for num in range(0, len(self.screenSubs[self.__indicators[0]][1])):
               self.__data[3 + num] = self.screenSubs[self.__indicators[0]][1][num]
        else:
           for itemNum in range(0, len(self.__indicators)):
               if self.__indicators[itemNum] == self.__data[2]:
                  self.__indicatorListBox.select_set(itemNum)
                  self.__indicatorListBox.yview(itemNum)

        self.__lastSelected = self.__indicatorListBox.curselection()[0]

        self.__subFrame = self.screenSubs[self.__data[2]][0](
            self.__loader, self.__uniqueFrame, self.__data, self.__changeData,
            self.__w, self.__h - round(self.__h // 10 * 2.5), self.__currentBank, self.dead, self.__blankAnimation
        )

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__indicatorListBox, "<ButtonRelease-1>", self.__changedType, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__indicatorListBox, "<KeyRelease-Up>"  , self.__changedType, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__indicatorListBox, "<KeyRelease-Down>", self.__changedType, 1)

        #self.__indicatorListBox.bind("<ButtonRelease-1>", self.__changedType)
        #self.__indicatorListBox.bind("<KeyRelease-Up>", self.__changedType)
        #self.__indicatorListBox.bind("<KeyRelease-Down>", self.__changedType)

    def __changedType(self, evenz):
        if self.__lastSelected != self.__indicatorListBox.curselection()[0]:
            self.stopMe = True
            self.__jumpMan = None
            try:
                self.__subFrame.killAll()
            except:
                print(type(self.__subFrame))
                for item in self.__blackFrame.pack_slaves():
                    item.destroy()
                for item in self.__blackFrame.place_slaves():
                    item.destroy()
                self.__blackFrame.destroy()

            self.__data[2] = self.__indicators[self.__indicatorListBox.curselection()[0]]
            for num in range(0, len(self.screenSubs[self.__indicators[self.__indicatorListBox.curselection()[0]]][1])):
                self.__data[3 + num] = self.screenSubs[self.__indicators[self.__indicatorListBox.curselection()[0]]][1][num]

            self.__lastSelected = self.__indicatorListBox.curselection()[0]

            self.__changeData(self.__data)

            self.__subFrame = self.screenSubs[self.__data[2]][0](
                self.__loader, self.__uniqueFrame, self.__data, self.__changeData,
                self.__w, self.__h - round(self.__h // 10 * 2.5), self.__currentBank, self.dead, self.__blankAnimation
            )

    def __blankAnimation(self, items):
        self.stopMe = False
        self.__blackFrame = Frame(self.__uniqueFrame, width=self.__w,
                                   bg="black",
                                   height=self.__h)
        self.__blackFrame.pack_propagate(False)
        self.__blackFrame.pack(side=TOP, anchor=N, fill=BOTH)


        self.__topFrame = Frame(self.__blackFrame, width=self.__w,
                                   bg="black",
                                   height= self.__loader.jumpman[0].height() )
        self.__topFrame.pack_propagate(False)
        self.__topFrame.pack(side=TOP, anchor=N, fill=X)

        self.__jumpMan = Label(self.__topFrame,
                                   bg="black", image = self.__loader.jumpman[0],
                                   width= self.__loader.jumpman[0].width(),
                                   height=self.__loader.jumpman[0].height()
                                   )

        self.__jumpManX = self.__w // 2 - (self.__loader.jumpman[0].width() // 2)
        self.__jumpMan.place(x=self.__jumpManX, y=0)
        self.__jumpManMirrored = False
        self.__jumpManFrameNum = 0

        txt = self.__dictionaries.getWordFromCurrentLanguage("missingItems")
        for key in items.keys():
            txt = txt.replace("#" + key + "#", items[key])

        self.__bottomFrame = Frame(self.__blackFrame, width=self.__w,
                                   bg="black",
                                   height= self.__loader.jumpman[0].height() )
        self.__bottomFrame.pack_propagate(False)
        self.__bottomFrame.pack(side=BOTTOM, anchor=N, fill=Y)

        self.__textLabel = Label(self.__bottomFrame, bd=0, bg="black",
                                   fg="orangered",
                                   height=10, font=self.__normalFont,
                                   text=txt
                                   )

        self.__textLabel.pack(padx=0, pady=0, fill=X, side=BOTTOM)

        self.__loader.threadLooper.addToThreading(self, self.__loopThem, [], 1)

        #t = Thread(target=self.__loopThem)
        #t.daemon = True
        #t.start()

    def __loopThem(self):
        from mouse import get_position

        self.__textLabel.config(
            fg=self.__loader.mainWindow.getLoopColor()
        )

        if self.__delay > 1:
            self.__delay = 0
        else:
            self.__delay += 1

        # if True:
        try:
            if self.__delay == 0:
                maxW = self.__w - self.__loader.jumpman[0].width() - 5

                jumpManOnScreenX = self.__topLevelWindow.winfo_x() + \
                                   self.__baseFrame.winfo_x() + \
                                   self.__jumpManX

                difference = get_position()[0] - jumpManOnScreenX - self.__loader.jumpman[0].width() // 2

                if abs(difference) < 20:
                    self.__jumpManFrameNum = 0

                else:
                    if self.__jumpManFrameNum > 1:
                        self.__jumpManFrameNum = 0
                    else:
                        self.__jumpManFrameNum += 1

                    if difference > 0:
                        self.__jumpManMirrored = False
                    else:
                        self.__jumpManMirrored = True

                    step = 25

                    if difference < 0 and self.__jumpManX > 5:
                        self.__jumpManX -= step
                    else:
                        if self.__jumpManMirrored == True: self.__jumpManFrameNum = 0

                    if difference > 0 and self.__jumpManX < maxW:
                        self.__jumpManX += step
                    else:
                        if self.__jumpManMirrored == False: self.__jumpManFrameNum = 0

            self.__jumpMan.config(
                image=self.__loader.jumpman[self.__jumpManMirrored * 3 + self.__jumpManFrameNum]
            )
            self.__jumpMan.place(x=self.__jumpManX, y=0)


        except Exception as e:
            print(str(e))

