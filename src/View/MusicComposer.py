from SubMenu import SubMenu
from SubMenuLabel import SubMenuLabel
from SubMenuFrame import SubMenuFrame
from tkinter import *
import re
from time import sleep
from threading import Thread

class MusicComposer:

    def __init__(self, loader, mainWindow, tiaScreens):
        self.__loader = loader
        self.__mainWindow = mainWindow

        self.firstLoad = True
        self.dead = False
        self.changed = False
        self.__loader.stopThreads.append(self)

        self.__caller = 0

        self.__pressed = {"1": False, "3": False}

        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs
        self.__fontManager = self.__loader.fontManager
        self.__fontSize = int(self.__screenSize[0]/1300 * self.__screenSize[1]/1050*14)
        self.__colors = self.__loader.colorPalettes
        self.__colorDict = self.__loader.colorDict
        self.__piaNotes = self.__loader.piaNotes

        self.__focused = None
        self.__screenSize = self.__loader.screenSize

        self.__func = None
        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__bigFont = self.__fontManager.getFont(int(self.__fontSize*1.10), False, False, False)
        self.__tinyFont = self.__fontManager.getFont(int(self.__fontSize*0.35), False, False, False)
        self.__tinyFont2 = self.__fontManager.getFont(int(self.__fontSize*0.50), False, False, False)

        if tiaScreens == None:
            from TiaScreens import TiaScreens
            self.__tiaScreens = TiaScreens(self.__loader)

        if self.__loader.virtualMemory.kernel == "common":
            self.__func = self.__addElementsCommon

        self.__ctrl = False
        self.__draw = 0

        self.__sizes = {
            "common": [self.__screenSize[0] / 1.10, self.__screenSize[1]/1.10  - 35]
        }

        self.__alreadyDone = False

        self.__window = SubMenu(self.__loader, "music", self.__sizes["common"][0],
                                self.__sizes["common"][1], None, self.__func, 1)

        self.dead = True


    def checker(self):
        from time import sleep
        while(self.dead==False and self.__loader.mainWindow.dead == False):
            try:
               if self.__channelNum[0] != self.__tiaScreens.currentChannel:
                   self.__tiaScreens.currentChannel = self.__channelNum[0]


            except Exception as e:
                self.__loader.logger.errorLog(e)


            sleep(0.4)

    def __addElementsCommon(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()

        self.__editorFrame = Frame(self.__topLevelWindow,
                                   height=round(self.__topLevel.getTopLevelDimensions()[1]),
                                   bg=self.__colors.getColor("window"))
        self.__editorFrame.pack_propagate(False)
        self.__editorFrame.pack(side=TOP, fill=X)

        self.__selectedChannelFrame = Frame(self.__editorFrame,
                                   height=round(self.__topLevel.getTopLevelDimensions()[1]*0.05),
                                   bg=self.__colors.getColor("window"))
        self.__selectedChannelFrame.pack_propagate(False)
        self.__selectedChannelFrame.pack(side=TOP, fill=X)

        self.__selectorForReal = Frame(self.__selectedChannelFrame,
                                   width=round(self.__topLevel.getTopLevelDimensions()[0]*0.5),
                                   bg=self.__colors.getColor("window"))
        self.__selectorForReal.pack_propagate(False)
        self.__selectorForReal.pack(side=LEFT, fill=Y)

        self.__selectorLabel = Label(self.__selectorForReal,
                                     width=len(self.__dictionaries.getWordFromCurrentLanguage("selectChannel"))+1,
                                     bg = self.__colors.getColor("window"),
                                     fg = self.__colors.getColor("font"),
                                     text = self.__dictionaries.getWordFromCurrentLanguage("selectChannel"),
                                     font = self.__normalFont,
                                     justify=LEFT
                                     )
        self.__selectorLabel.pack(side=LEFT, fill=Y, anchor=W)

        self.__selectorButtons = Frame(self.__selectorForReal,
                                   width=round(self.__topLevel.getTopLevelDimensions()[0]*0.25),
                                   bg=self.__colors.getColor("window"))
        self.__selectorButtons.pack_propagate(False)
        self.__selectorButtons.pack(side=LEFT, fill=Y)

        self.__channelNum = [1]
        from ChannelChangerButton import ChannelChangerButton

        for num in range(1,5):
            self.__channel1Button = ChannelChangerButton(self.__loader, self.__bigFont, num,
                                           self.__channelNum,
                                           round(self.__topLevel.getTopLevelDimensions()[0]*0.002),
                                           self.__selectorButtons)


        self.__channelFrame = Frame(self.__editorFrame, height=round(self.__topLevel.getTopLevelDimensions()[1]*0.75),
                                    bg = self.__colors.getColor("window"),
                                    width=self.__topLevel.getTopLevelDimensions()[0])
        self.__channelFrame.pack_propagate(False)
        self.__channelFrame.pack(side=TOP, anchor=N, fill=X)

        self.__h = round(self.__topLevel.getTopLevelDimensions()[1]*0.60*0.66)

        self.__trembleChannel = Frame(self.__channelFrame, height=self.__h,
                                    bg = self.__colors.getColor("window"),
                                      width=self.__topLevel.getTopLevelDimensions()[0]
                                      )
        self.__trembleChannel.pack_propagate(False)
        self.__trembleChannel.pack(side=TOP, anchor=N, fill=X)

        """
        self.__XXX = Frame(self.__channelFrame, height=round(self.__h*0.01),
                                    bg = self.__colors.getColor("window"))
        self.__XXX.pack_propagate(False)
        self.__XXX.pack(side=TOP, anchor=N, fill=X)
        """

        self.__bassNUM = 0.7

        self.__bassChannel = Frame(self.__channelFrame, height=round(self.__h*self.__bassNUM),
                                    bg = self.__colors.getColor("window"),
                                   width=self.__topLevel.getTopLevelDimensions()[0])
        self.__bassChannel.pack_propagate(False)
        self.__bassChannel.pack(side=TOP, anchor=N, fill=X)

        self.__drumNUM = 0.35

        self.__drumChannel = Frame(self.__channelFrame, height=round(self.__h*self.__drumNUM),
                                    bg = self.__colors.getColor("window"),
                                   width=self.__topLevel.getTopLevelDimensions()[0])
        self.__drumChannel.pack_propagate(False)
        self.__drumChannel.pack(side=TOP, anchor=N, fill=X)

        #self.__bass = True
        self.__buzz = False
        self.__correctNotes = 0 # Can be 0-2
        self.__fadeOutLen = 0
        self.__dividerLen = 4   # Has effect over 2
        self.__vibratio = False

        self.__piaNoteTable = {}

        self.__patterns = {}
        self.createPattenrs()

        self.__runningThreads = 3

        t1 = Thread(target=self.__drawField, args=(self.__trembleChannel, self.__h,
                                                   69, 31, self.__patterns["tremble"],
                                                   "tremble"))
        t1.daemon = True
        t1.start()

        t2 = Thread(target=self.__drawField, args=(self.__bassChannel, round(self.__h*self.__bassNUM),
                                                   30, 2, self.__patterns["bass"],
                                                   "bass"))
        t2.daemon = True
        t2.start()

        t3 = Thread(target=self.__drawDrums, args=(self.__drumChannel, round(self.__h*self.__drumNUM)))
        t3.daemon = True
        t3.start()


        t99 = Thread(target=self.checker)
        t99.daemon = True
        t99.start()

        self.__topLevelWindow.bind("<KeyPress-Control_L>", self.shiftON)
        self.__topLevelWindow.bind("<KeyRelease-Control_L>", self.shiftOff)
        self.__topLevelWindow.bind("<KeyPress-Control_R>", self.shiftON)
        self.__topLevelWindow.bind("<KeyRelease-Control_R>", self.shiftOff)
        #self.__topLevelWindow.bind('<ButtonPress-1>', self.pressed)
        #self.__topLevelWindow.bind('<ButtonRelease-1>', self.released)
        #self.__topLevelWindow.bind('<ButtonPress-3>', self.pressed)
        #self.__topLevelWindow.bind('<ButtonRelease-3>', self.released)
        self.__topLevelWindow.bind("<Button-2>", self.button2)

        """
    def pressed(self, event):
        self.__pressed[str(event.num)] = True

    def released(self, event):
        self.__pressed[str(event.num)] = False
        """

    def button2(self, event):
        self.__draw = 1 - self.__draw

    def createPattenrs(self):
        from copy import deepcopy

        pattern = []
        octave = [0,1,0,1,0,0,1,0,1,0,1,0]
        for num in range(0, 3):
            pattern.extend(deepcopy(octave))
        pattern.append(0)
        self.__patterns["tremble"] = pattern

        pattern = []
        octave = [0,1,0,1,0,0,1,0,1,0,1,0]
        for num in range(0, 2):
            pattern.extend(deepcopy(octave))
        pattern.extend([0,1,0,1,0])
        self.__patterns["bass"] = pattern


    def __drawDrums(self, frame, frameH):
        numofFieldsW = self.__tiaScreens.numOfFieldsW
        numofFieldsH = 3

        listenButtons = Frame(frame, bg = self.__colors.getColor("window"),
                              width=round(self.__topLevel.getTopLevelDimensions()[0]*0.05))
        listenButtons.pack_propagate(False)
        listenButtons.pack(side=LEFT, anchor=W, fill=Y)

        setPanel = Frame(frame, bg = self.__colors.getColor("window"),
                         width=round(self.__topLevel.getTopLevelDimensions()[0]*0.95))
        setPanel.pack_propagate(False)
        setPanel.pack(side=LEFT, anchor=W, fill=BOTH)

        baseW = round(round(self.__topLevel.getTopLevelDimensions()[0] * 0.85) / numofFieldsW)
        baseH = round(frameH*self.__drumNUM / numofFieldsH * 0.6)

        self.drumSetNames = ["15,20", "8,0", "15,2", "8,8", "2,0", "3,0", "3,1"]

        self.drumButton(self.drumSetNames[0], self.__dictionaries.getWordFromCurrentLanguage("drum"), 0, listenButtons, baseW, baseH)
        self.drumButton(self.drumSetNames[1], self.__dictionaries.getWordFromCurrentLanguage("hat")+"-1", 1, listenButtons, baseW, baseH)
        self.drumButton(self.drumSetNames[2], self.__dictionaries.getWordFromCurrentLanguage("hat")+"-2", 2, listenButtons, baseW, baseH)
        self.drumButton(self.drumSetNames[3], self.__dictionaries.getWordFromCurrentLanguage("snare"), 3, listenButtons, baseW, baseH)
        self.drumButton(self.drumSetNames[4], self.__dictionaries.getWordFromCurrentLanguage("horn"), 4, listenButtons, baseW, baseH)
        self.drumButton(self.drumSetNames[5], self.__dictionaries.getWordFromCurrentLanguage("buzz")+"-1", 5, listenButtons, baseW, baseH)
        self.drumButton(self.drumSetNames[6], self.__dictionaries.getWordFromCurrentLanguage("buzz")+"-2", 6, listenButtons, baseW, baseH)

        theY = 0
        for yY in range(0,7):
            color1 = "white"
            color2 = "black"
            if yY % 2 == 1:
                color1 = "black"
                color2 = "white"
            theX = 0
            for counter in range(0, numofFieldsW):
                if self.__dividerLen > 1 and (counter + 1) % self.__dividerLen == 0:
                    theW = round(baseW*0.95)
                else:
                    theW = baseW

                f = Frame(setPanel, width=theW, height=baseH, bg=color1)
                f.pack_propagate(False)
                f.place(x=theX, y=theY)

                b = Button(f, width=theW, height=baseH, bg=color1,
                           fg=color2,
                           font=self.__tinyFont2,
                           name=str(counter) + "," + str(yY+89),
                           activebackground=self.__colors.getColor("highLight"))

                self.__tiaScreens.setColorValue(counter, yY+89, color1)
                self.colorButton(counter, yY+89, b)
                b.pack_propagate(False)
                b.pack(fill=BOTH)
                self.__piaNoteTable[str(counter) + "," + str(yY+89)] = b

                b.bind("<ButtonPress-1>", self.clickedButton)
                b.bind("<MouseWheel>", self.mouseWheel)
                b.bind("<Enter>", self.enterCommon)

                theX+=baseW
            theY+=baseH
        self.__runningThreads-=1

    def drumButton(self, name, text, multi, frame, baseW, baseH):
        f = Frame(frame, width=baseW*3, height=baseH, bg="white")
        f.pack_propagate(False)
        f.place(x=0, y=baseH*multi)

        if multi % 2 == 0:
            color1 = "white"
            color2 = "black"
        else:
            color2 = "white"
            color1 = "black"

        b = Button(f, width=baseW*3, height=baseH, bg=color1, fg=color2,
                    font=self.__tinyFont, name=name,
                   text = text,
                   activebackground=self.__colors.getColor("highLight")
                   )
        b.pack_propagate(False)
        b.pack(fill=BOTH)
        b.bind("<ButtonPress-1>", self.playNote1)


    def __drawField(self, frame, frameH, start, end, pattern, key):

        if key == "bass":
            frameH * self.__bassNUM

        numofFieldsH = start-end
        numofFieldsW = self.__tiaScreens.numOfFieldsW

        listenButtons = Frame(frame, bg = self.__colors.getColor("window"),
                              width=round(self.__topLevel.getTopLevelDimensions()[0]*0.05))
        listenButtons.pack_propagate(False)
        listenButtons.pack(side=LEFT, anchor=W, fill=Y)

        setPanel = Frame(frame, bg = self.__colors.getColor("window"),
                         width=round(self.__topLevel.getTopLevelDimensions()[0]*0.95))
        setPanel.pack_propagate(False)
        setPanel.pack(side=LEFT, anchor=W, fill=BOTH)

        YPoz = 0
        counter = 0

        for theY in range(start-1, end, -1):
            baseH = round(frameH / numofFieldsH)
            H = baseH
            baseW = round(round(self.__topLevel.getTopLevelDimensions()[0]*0.85) / numofFieldsW)
            color1 = "white"
            color2 = "black"
            if pattern[counter] == 1:
                color1 = "black"
                color2 = "white"

            notes = self.__piaNotes.getTiaValue(theY, None)
            if (key == "tremble"):
                self.__soundPlayer.playSound("Pong")

                self.deleteKey(notes, "1")
                self.deleteKey(notes, "6")
            elif (key == "bass"):
                self.deleteKey(notes, "4")
                self.deleteKey(notes, "12")

            X = baseW*counter

            self.createPianoButtons(listenButtons, notes, baseW, H, YPoz, color1, color2)
            self.createEditorButtons(setPanel, baseW, H, YPoz, color1, color2, theY)

            #print(start, end-1, theY)
            counter+=1
            YPoz+=H
        self.__runningThreads-=1

    def createEditorButtons(self, frame, W, H, Y, colorBack, colorFont, theY):
        counter = 0
        for X in range(0, self.__tiaScreens.numOfFieldsW, 1):
            theX = X
            X = counter * W

            if self.__dividerLen > 1 and (counter + 1) % self.__dividerLen == 0:
                theW = round(W*0.95)
            else:
                theW = W

            f = Frame(frame, width=theW, height=H, bg=colorBack)
            f.pack_propagate(False)
            f.place(x=X, y=Y)

            self.__tiaScreens.setColorValue(theX, theY, colorBack)

            b = Button(f, width=theW, height=H, bg=colorBack,
                       fg=colorFont,
                       font=self.__tinyFont2,
                       name=str(counter) + "," + str(theY),
                       activebackground=self.__colors.getColor("highLight"))

            self.colorButton(theX, theY, b)
            b.pack_propagate(False)
            b.pack(fill=BOTH)
            self.__piaNoteTable[str(counter) + "," + str(theY)] = b
            counter+=1

            b.bind("<ButtonPress-1>", self.clickedButton)
            b.bind("<MouseWheel>", self.mouseWheel)
            b.bind("<Enter>", self.enterCommon)


    def clickedButton(self, event):
        if self.__runningThreads>0:
            return

        name = str(event.widget).split(".")[-1]
        Y, X = self.getXYfromName(name)

        buttonValues = self.__tiaScreens.getTileValue(X,Y)
        buttonValues["enabled"] = 1 - buttonValues["enabled"]

        if buttonValues["enabled"] == 0:
            self.__tiaScreens.setTileValue(X, Y, 0, 0, 0, 0)
            self.colorButton(X,Y,event.widget)
        else:
            self.eraseRow(X)
            self.setValues(X, Y)
            self.colorButton(X,Y,event.widget)

    def setValues(self, X, Y):
        notes = self.__piaNotes.getTiaValue(Y, None)

        if (Y > 31):
            self.deleteKey(notes, "1")
            self.deleteKey(notes, "6")
        elif (Y < 32):
            self.deleteKey(notes, "4")
            self.deleteKey(notes, "12")

        if Y > 88:
            note = self.drumSetNames[Y-89]
            C = int(note.split(",")[0])
            F = int(note.split(",")[1])

        elif len(notes) == 1:
            if type(notes[list(notes.keys())[0]]) == list:
                from random import randint
                num = randint(0, len(notes[list(notes.keys())[0]])-1)

                C = int(list(notes.keys())[0])
                F = int(notes[list(notes.keys())[0]][num])

            else:
                C = int(list(notes.keys())[0])
                F = int(notes[list(notes.keys())[0]])
        else:
            dominants = self.__tiaScreens.getDomimantChannel()

            C = None
            for num in dominants:
                if num in notes.keys():
                    C = num
                    F = notes[num]

            if C == None:
                C = int(list(notes.keys())[0])
                F = int(notes[list(notes.keys())[0]])

        self.__tiaScreens.setTileValue(X, Y, 8, C, F, 1)
        if self.__buzz == True and C == 6:
            C = 7
        self.__piaNotes.playTia(8, C, F)

    def eraseRow(self, X):
        for Y in range(0,100):
            try:
                self.__tiaScreens.setTileValue(X, Y, 0, 0, 0, 0)
                self.colorButton(X,Y,self.__piaNoteTable[str(X)+","+str(Y)])
            except:
                pass

    def colorButton(self, X, Y, button):
        buttonValues = self.__tiaScreens.getTileValue(X, Y)

        if buttonValues["enabled"] == 0:

            if buttonValues["color"] == "white":
                color2 = "black"
            else:
                color2 = "white"
            button.config(bg = buttonValues["color"], fg = color2, text = "")
        else:

            button.config(bg = self.__colors.getColor("boxBackUnSaved"),
                          fg = self.__colors.getColor("boxFontUnSaved"),
                          text = str(buttonValues["volume"]))



    def createPianoButtons(self, frame, notes, W, H, Y, colorBack, colorFont):
        counter = 0
        for channel in notes.keys():
            if type(notes[channel]) != list:
                X = counter * W
                #print(Y*H)
                f = Frame(frame, width=W, height=H, bg = colorBack)
                f.pack_propagate(False)
                f.place(x=X, y=Y)

                b = Button(f, width=W, height=H, bg = colorBack,
                           fg = colorFont, text=str(channel) + ": " + str(notes[channel]),
                           font=self.__tinyFont,
                           name = str(channel) + "," + str(notes[channel]),
                           activebackground=self.__colors.getColor("highLight")
                           )

                #self.__piaNoteTable[str(channel) + "," + str(notes[channel])] = b

                b.bind("<ButtonPress-1>", self.playNote1)
                #b.bind("<ButtonPress-1>", self.released())

                b.pack_propagate(False)
                b.pack(fill=BOTH)

                if channel == "6":
                    counter+=1
                    X = counter * W

                    f = Frame(frame, width=W, height=H, bg=colorBack)
                    f.pack_propagate(False)
                    f.place(x=X, y=Y)

                    b = Button(f, width=W, height=H, bg=colorBack,
                               fg=colorFont, text = "7: " + str(notes[channel]),
                               font=self.__tinyFont,
                               name="7," + str(notes[channel]),
                               activebackground=self.__colors.getColor("highLight")
                               )

                    b.bind("<ButtonPress-1>", self.playNote1)
                    # b.bind("<ButtonPress-1>", self.released())

                    b.pack_propagate(False)
                    b.pack(fill=BOTH)

            #self.__piaNoteTable
            counter +=1

    def playNote1(self, event):
        name = str(event.widget).split(".")[-1]
        note, channel = self.getXYfromName(name)
        self.__piaNotes.playTia(8, int(channel), int(note))


    def deleteKey(self, d, key):
        try:
            del d[key]
        except:
            pass

    def mouseWheel(self, event):
        if self.__runningThreads>0:
            return

        name = str(event.widget).split(".")[-1]
        Y, X = self.getXYfromName(name)
        buttonValues = self.__tiaScreens.getTileValue(X, Y)

        if buttonValues["volume"] == 0:
            return
        elif event.delta == 120:
            if buttonValues["volume"] == 15:
                V = 1
            else:
                V = buttonValues["volume"] + 1
        else:
            if buttonValues["volume"] == 1:
                V = 15
            else:
                V = buttonValues["volume"] - 1


        event.widget.config(text=str(V))
        self.__tiaScreens.setTileValue(X, Y,
                                    V ,
                                    buttonValues["channel"],
                                    buttonValues["freq"],
                                    1)

    def enterCommon(self, event):
        if self.__runningThreads > 0:
            return

        if self.__draw == 1:
            name = str(event.widget).split(".")[-1]
            Y, X = self.getXYfromName(name)
            buttonValues = self.__tiaScreens.getTileValue(X, Y)

            if self.__ctrl == False:
                if buttonValues["enabled"] == 1:
                    self.__tiaScreens.setTileValue(X, Y, 0, 0, 0, 0)
                    self.colorButton(X, Y, event.widget)
            else:
                if buttonValues["enabled"] == 0:
                    self.eraseRow(X)
                    self.setValues(X, Y)
                    self.colorButton(X, Y, event.widget)

        """
        if self.__ctrl == True:
            name = str(event.widget).split(".")[-1]
            Y, X = self.getXYfromName(name)
            buttonValues = self.__tiaScreens.getTileValue(X, Y)

            if buttonValues["enabled"] == 1 and self.__pressed["3"] == True:
                self.__tiaScreens.setTileValue(X, Y, 0, 0, 0, 0)
                self.colorButton(X, Y, event.widget)
            if buttonValues["enabled"] == 0 and self.__pressed["1"] == True:
                self.eraseRow(X)
                self.setValues(X, Y)
                self.colorButton(X, Y, event.widget)
        """

    def focusIn(self, event):
        self.focused = event.widget

    def focusOut(self, event):
        self.focused = None

    def shiftON(self, event):
        self.__ctrl = True

    def shiftOff(self, event):
        self.__ctrl = False

    def getXYfromName(self, w):
        name = str(w).split(".")[-1]
        try:
            Y = int(name.split(",")[0])
            X = int(name.split(",")[1])
            return X,Y
        except:
            return