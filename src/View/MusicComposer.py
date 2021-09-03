from SubMenu import SubMenu
from SubMenuLabel import SubMenuLabel
from SubMenuFrame import SubMenuFrame
from tkinter import *
import re
from time import sleep
from threading import Thread

class MusicComposer:

    def __init__(self, loader, mainWindow):
        self.__loader = loader
        self.__mainWindow = mainWindow

        self.__pianoLabel = None

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
               pass

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
                                    bg = self.__colors.getColor("window"))
        self.__channelFrame.pack_propagate(False)
        self.__channelFrame.pack(side=TOP, anchor=N, fill=X)

        self.__h = round(self.__topLevel.getTopLevelDimensions()[1]*0.60*0.66)

        self.__trembleChannel = Frame(self.__channelFrame, height=self.__h,
                                    bg = self.__colors.getColor("window"))
        self.__trembleChannel.pack_propagate(False)
        self.__trembleChannel.pack(side=TOP, anchor=N, fill=X)

        self.__XXX = Frame(self.__channelFrame, height=round(self.__h*0.01),
                                    bg = self.__colors.getColor("font"))
        self.__XXX.pack_propagate(False)
        self.__XXX.pack(side=TOP, anchor=N, fill=X)

        self.__bassNUM = 0.7

        self.__bassChannel = Frame(self.__channelFrame, height=round(self.__h*self.__bassNUM),
                                    bg = self.__colors.getColor("window"))
        self.__bassChannel.pack_propagate(False)
        self.__bassChannel.pack(side=TOP, anchor=N, fill=X)

        #self.__bass = True
        self.__buzz = False
        self.__correctNotes = 0 # Can be 0-2
        self.__fadeOutLen = 0
        self.__dividerLen = 4   # Has effect over 2
        self.__vibratio = False

        self.__topLevelWindow.bind("<KeyPress-Control_L>", self.shiftON)
        self.__topLevelWindow.bind("<KeyRelease-Control_L>", self.shiftOff)
        self.__topLevelWindow.bind("<KeyPress-Control_R>", self.shiftON)
        self.__topLevelWindow.bind("<KeyRelease-Control_R>", self.shiftOff)
        self.__topLevelWindow.bind('<ButtonPress-1>', self.pressed)
        self.__topLevelWindow.bind('<ButtonRelease-1>', self.released)
        self.__topLevelWindow.bind('<ButtonPress-3>', self.pressed)
        self.__topLevelWindow.bind('<ButtonRelease-3>', self.released)

        self.__table = {}
        self.__patterns = {}
        self.__noteButtons = []

        from NoteTable import NoteTable
        self.numOfFieldsW = 48

        self.__noteTable= NoteTable(self.__loader, self.numOfFieldsW)

        self.__runningThreads = 2

        t1 = Thread(target=self.__drawTrembleField)
        t1.daemon = True
        t1.start()

        t2 = Thread(target=self.__drawBassField)
        t2.daemon = True
        t2.start()

        t99 = Thread(target=self.checker)
        t99.daemon = True
        t99.start()



    def pressed(self, event):
        try:
            for item in str(event).split(" "):
                if "num" in item:
                    self.__pressed[item.split("=")[1]] = True
        except:
            return

    def released(self, event):
        try:
            for item in str(event).split(" "):
                if "num" in item:
                    self.__pressed[item.split("=")[1]] = False
        except:
            return


    def __drawBassField(self):
        from PIL import Image, ImageTk

        self._pianoImgBass = Image.open("others/img/bassPiano.png")

        while True:
            try:
                piano_w = self.__saveW
                break
            except:
                pass


        piano_h = round(self.__h*self.__bassNUM)

        self._pianoImgBass = self._pianoImgBass.resize((piano_w, piano_h), Image.ANTIALIAS)
        self._pianoImgBassTK = ImageTk.PhotoImage(self._pianoImgBass)

        self.__pianoFrameB = Frame(self.__bassChannel, width=round(piano_w*1.5), height=piano_h, bg = self.__colors.getColor("window"))
        self.__pianoFrameB.pack_propagate(False)
        self.__pianoFrameB.pack(side=LEFT, anchor = W, fill = Y)

        self.__pianoLabelB = Label(self.__pianoFrameB, image=self._pianoImgBassTK, width=round(piano_w / 3 * 2), height=piano_h)
        self.__pianoLabelB.pack_propagate(False)
        self.__pianoLabelB.pack(side=LEFT, anchor=W, fill=Y)

        self.__bbbB = Frame(self.__pianoFrameB, width=9999, height=piano_h, bg = "white")
        self.__bbbB.pack_propagate(False)
        self.__bbbB.pack(side=LEFT, anchor = W, fill = BOTH)

        self.__remainingB = self.__topLevel.getTopLevelDimensions()[0]-(piano_w*1.5)

        self.__fieldFrameB = Frame(self.__bassChannel, bg = self.__colors.getColor("window"), width=self.__remainingB)
        self.__fieldFrameB.pack_propagate(False)
        self.__fieldFrameB.pack(side=LEFT, anchor = W, fill = BOTH)

        self.__drawBassFields()
        self.__runningThreads-=1

    def __drawTrembleField(self):
        from copy import deepcopy
        from PIL import Image, ImageTk

        self._pianoImgTremble = Image.open("others/img/tremblePiano.png")

        piano_h = round(self.__h)
        piano_w = round((self.__h/1280*150)*2)
        self.__saveW = piano_w

        self._pianoImgTremble = self._pianoImgTremble.resize((piano_w, piano_h), Image.ANTIALIAS)
        self._pianoImgTrembleTK = ImageTk.PhotoImage(self._pianoImgTremble)


        self.__pianoFrame = Frame(self.__trembleChannel, width=round(piano_w*1.5), height=piano_h, bg = self.__colors.getColor("window"))
        self.__pianoFrame.pack_propagate(False)
        self.__pianoFrame.pack(side=LEFT, anchor = W, fill = Y)

        self.__pianoLabel = Label(self.__pianoFrame, image=self._pianoImgTrembleTK, width=round(piano_w / 3 * 2), height=piano_h)
        self.__pianoLabel.pack_propagate(False)
        self.__pianoLabel.pack(side=LEFT, anchor=W, fill=Y)

        self.__bbb = Frame(self.__pianoFrame, width=9999, height=piano_h, bg = "white")
        self.__bbb.pack_propagate(False)
        self.__bbb.pack(side=LEFT, anchor = W, fill = BOTH)

        self.__remaining = self.__topLevel.getTopLevelDimensions()[0]-(piano_w*1.5)

        self.__fieldFrame = Frame(self.__trembleChannel, bg = self.__colors.getColor("window"), width=self.__remaining)
        self.__fieldFrame.pack_propagate(False)
        self.__fieldFrame.pack(side=LEFT, anchor = W, fill = BOTH)

        self.__drawTrembleFields()
        self.__runningThreads-=1

    def __drawFields(self, start, end, numOfFieldsH, pattern, key, w, h, fieldFrame, bbb, numOfFieldsW):

        from PianoButton import PianoButton

        theY = 0
        theH = 0
        self.__table[key] = []

        pfffff = 0
        for counter in range(0, numOfFieldsH):

            Y=end-counter

            self.__table[key].append([])
            self.__soundPlayer.playSound("Pong")

            theY += theH
            for X in range(0, numOfFieldsW):

                self.__table[key][counter].append({})
                theW = 0

                if self.__dividerLen > 1 and (X + 1) % self.__dividerLen == 0:
                    theW = round(w * (0.85))
                else:
                    theW = w

                F = None
                if pattern[counter] == 0:
                    theH = round(h * (1.35 + pfffff))
                    try:
                        if pattern[counter + 1] == 1:
                            theH = round(h+(1*pfffff))

                    except:
                        pass
                    try:
                        if pattern[counter - 1] == 1:
                            theH = round(h * (1.12 + pfffff))

                    except:
                        pass

                    try:
                        if pattern[counter + 1] == 1 and pattern[counter - 1] == 1:
                            theH = round(h * (0.9 + pfffff))

                    except:
                        pass

                    F = Frame(fieldFrame, bg=self.__colors.getColor("boxBackNormal"), width=theW, height=theH)
                else:
                    theH = h

                    F = Frame(fieldFrame, bg=self.__colors.getColor("boxFontNormal"), width=theW, height=theH)

                # F.config(borderwidth = 1, relief=RIDGE)
                F.pack_propagate(False)
                F.place(x=X * w, y=theY)
                self.__table[key][counter][X]["frame"] = F
                self.__table[key][counter][X]["value"] = 0

                if self.__dividerLen > 1 and (X + 1) % self.__dividerLen == 0:
                    divider = Frame(fieldFrame, bg=self.__colors.getColor("fontDisabled"), width=round(w * 0.1),
                                    height=theH)
                    divider.pack_propagate(False)
                    divider.place(x=(X * w) + theW, y=theY)

                B = Button(F, name=str(X) + "," + str(Y), bg=self.__table[key][counter][X]["frame"]["bg"],
                           relief=GROOVE, activebackground=self.__colors.getColor("highLight"))

                if self.__table[key][counter][X]["value"] == True:
                    B.config(bg=self.__colors.getColor("boxBackUnSaved"))

                B.pack_propagate(False)
                B.pack(fill=BOTH)
                B.bind("<Button-1>", self.clickedCommon)
                B.bind("<Button-3>", self.clickedCommon)
                B.bind("<Enter>", self.enterCommon)

                self.__table[key][counter][X]["button"] = B
                #self.__table[key][counter][X]["volume"] = 8

            theW = round((self.__h / 1280 * 150) * 2 / 4)

            notes = self.__piaNotes.getTiaValue(str(Y), None)

            if key == "bass":
                try:
                    del notes["4"]
                except:
                    pass
                try:
                    del notes["12"]
                except:
                    pass
            else:
                try:
                    del notes["1"]
                except:
                    pass
                try:
                    del notes["6"]
                except:
                    pass
            if notes != None:
                num = 0
                for channel in notes.keys():

                    color = "white"
                    if pattern[counter] == 1:
                        color = "black"

                    note = notes[channel]
                    if type(note) == list:
                        continue


                    if channel == "6":
                        b = PianoButton(self.__loader, color, bbb, theW, note, "6",
                                        self.__tinyFont, theW * num, theY, theH)

                        self.__noteButtons.append(b)
                        num += 1
                        b = PianoButton(self.__loader, color, bbb, theW, note, "7",
                                        self.__tinyFont, theW * num, theY, theH)

                        self.__noteButtons.append(b)
                        num += 1
                    else:
                        b = PianoButton(self.__loader, color, bbb, theW, note, channel,
                                        self.__tinyFont, theW * num, theY, theH)

                        self.__noteButtons.append(b)
                        num += 1


    def __drawBassFields(self):

        from copy import deepcopy

        numOfFieldsW = 48
        numofFieldsH = 27
        start=2
        end=30
        w = round(self.__remainingB / numOfFieldsW)
        h = round(self.__topLevel.getTopLevelDimensions()[1] * 0.4 / numofFieldsH)

        pattern = []
        octave = [0,1,0,1,0,0,1,0,1,0,1,0]
        for num in range(0, 2):
            pattern.extend(deepcopy(octave))
        pattern.extend([0,1,0,1,0])

        self.__patterns["bass"] = pattern
        self.__drawFields(start, end, numofFieldsH, pattern, "bass", w, round(h*self.__bassNUM), self.__fieldFrameB, self.__bbbB, numOfFieldsW)

    def __drawTrembleFields(self):
        from copy import deepcopy

        numOfFieldsW = 48
        numofFieldsH = 38
        start=31
        end=69
        w = round(self.__remaining / numOfFieldsW)
        h = round(self.__topLevel.getTopLevelDimensions()[1] * 0.4 / numofFieldsH)

        pattern = [0]
        octave = [0,1,0,1,0,0,1,0,1,0,1,0]
        for num in range(0, 3):
            pattern.extend(deepcopy(octave))
        pattern.append(0)

        self.__patterns["tremble"] = pattern
        self.__drawFields(start, end, numofFieldsH, pattern, "tremble", w, h, self.__fieldFrame, self.__bbb, numOfFieldsW)



    def clickedCommon(self, event):
        if self.__runningThreads>0:
            return

        button = 0

        if self.__ctrl == False:
            try:
                for item in str(event).split(" "):
                    if "num" in item:
                        item = item.split("=")
                        button = int(item[1])
            except:
                return
        else:
            if self.__pressed["1"] == True:
                button = 1
            else:
                if self.__pressed["3"] == True:
                    button = 3
                else:
                    return

        name = str(event.widget).split(".")[-1]
        X = 0
        Y = 0

        try:
            Y = int(name.split(",")[0])
            X = int(name.split(",")[1])
        except:
            return
        if X>30:
            self.__flipButton(X, Y, "tremble")
        if X<32 and X>3:
            print(X)
            self.__flipButton(X, Y, "bass")


    def __flipButton(self, Y, X, key):
        pattern = self.__patterns[key]

        realY = Y


        if key == "tremble":
            Y = 69-Y
            #noteTable = self.__noteTableTremble
        elif key == "bass":
            Y = 30-Y
            #noteTable = self.__noteTableBass

        #print(Y, X)
        self.__table[key][Y][X]["value"] = 1-self.__table[key][Y][X]["value"]

        normalColor = self.__colors.getColor("boxBackNormal")
        if pattern[Y] == 1:
            normalColor = self.__colors.getColor("font")

        if self.__table[key][Y][X]["value"] == 1:

            self.__clearColumns(X)

            self.__noteTable.flipField(X,Y)
            self.__table[key][Y][X]["button"].config(bg = self.__colors.getColor("boxBackUnSaved"),
                                                fg = self.__colors.getColor("boxFontUnSaved"),
                                                font = self.__tinyFont2)

            self.__table[key][Y][X]["button"].config(text = self.__noteTable.getValue(X,Y))
            dominants = self.__noteTable.getDominantChannelsOfScreen(key)


            notes = self.__piaNotes.getTiaValue(str(realY), None)
            #print(realY)

            channel = None
            freq = None


            if type(notes[list(notes.keys())[0]]) == list:
                from random import randint

                num = randint(0, len(notes[list(notes.keys())[0]])-1)
                #print(len(notes[list(notes.keys())[0]]), num)


                self.__piaNotes.playTia(
                    notes[list(notes.keys())[0]][num],
                    list(notes.keys())[0]
                )

            elif len(notes) == 1:
                self.__piaNotes.playTia(notes[list(notes.keys())[0]],
                                        list(notes.keys())[0])
            elif len(notes) > 1:
                reversedDict, orderedList = self.reversedAndOrdered(notes, dominants)
                #print(reversedDict)
                #print(orderedList)
                #print(notes)

                self.__piaNotes.playTia(notes[str(reversedDict[orderedList[0]])],
                                        reversedDict[orderedList[0]])

        else:
            self.__noteTable.flipField(X,Y)
            self.__table[key][Y][X]["button"].config(bg = normalColor, text = "")

    def __clearColumns(self, X):

        # 38, 27
        for Y in range(0,38):
            self.clearButton("tremble", X, Y)

        for Y in range(0, 27):
            self.clearButton("bass", X, Y)

    def clearButton(self, key, X, Y):
        if self.__patterns[key][Y] == 1:
            color = "black"
        else:
            color = "white"

        self.__noteTable.clearField(X, Y)
        self.__table[key][Y][X]["button"].config(bg=color, text="")
        self.__table[key][Y][X]["value"] = 0

    def reversedAndOrdered(self, notes, dominants):
        reversedDict = {}
        orderedList = []

        for item in notes.keys():
            reversedDict[dominants[int(item)]] = item
            orderedList.append(dominants[int(item)])

        orderedList.sort(reverse=True)
        return(reversedDict, orderedList)


    def enterCommon(self, event):
        if self.__ctrl == True:
            self.clickedCommon(event)

    def focusIn(self, event):
        self.focused = event.widget

    def focusOut(self, event):
        self.focused = None

    def shiftON(self, event):
        self.__ctrl = True

    def shiftOff(self, event):
        self.__ctrl = False