from SubMenu import SubMenu
from SubMenuLabel import SubMenuLabel
from SubMenuFrame import SubMenuFrame
from tkinter import *
import re
from time import sleep
from threading import Thread

class PlayfieldEditor:

    def __init__(self, loader, mainWindow):
        self.__loader = loader
        self.__mainWindow = mainWindow

        self.dead = False
        self.__loader.stopThreads.append(self)

        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs
        self.__fontManager = self.__loader.fontManager
        self.__fontSize = int(self.__screenSize[0]/1300 * self.__screenSize[1]/1050*14)
        self.__colors = self.__loader.colorPalettes

        self.__focused = None
        self.__screenSize = self.__loader.screenSize

        self.__func = None
        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)


        if self.__loader.virtualMemory.kernel == "common":
            self.__func = self.__addElementsCommon

        self.__ctrl = False
        self.__middle = False
        self.__draw = 0


        self.__window = SubMenu(self.__loader, "playfieldEditor", self.__screenSize[0] / 1.65,
                                self.__screenSize[1]/1.10  - 45,
                                None, self.__func)

        self.dead = True




    def __addElementsCommon(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()

        self.__piff = 0.85
        self.__puff = 0.65
        self.__Y = 42

        self.__playfieldFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"))
        self.__playfieldFrame.config(height=round(self.__topLevel.getTopLevelDimensions()[1]/self.__Y*self.__piff)*self.__Y)
        self.__playfieldFrame.pack_propagate(False)
        self.__playfieldFrame.pack(side=TOP, anchor=N, fill=X)

        self.__theField = Frame(self.__playfieldFrame, bg=self.__loader.colorPalettes.getColor("window"))

        self.__theField.config(width=round(self.__topLevel.getTopLevelDimensions()[0]/40*self.__puff)*40)
        self.__theField.pack_propagate(False)
        self.__theField.pack(side=LEFT, anchor=W, fill=Y)

        self.__topLevelWindow.bind("<KeyPress-Control_L>", self.shiftON)
        self.__topLevelWindow.bind("<KeyRelease-Control_L>", self.shiftOff)
        self.__topLevelWindow.bind("<KeyPress-Control_R>", self.shiftON)
        self.__topLevelWindow.bind("<KeyRelease-Control_R>", self.shiftOff)
        self.__topLevelWindow.bind("<Button-2>", self.drawMode)


        self.__table = []
        row = []
        self.__logicalX=[
            [4,35], [5,34], [6,33],
            [7,32], [8,31], [9,30],
            [10,29], [11,28], [12,27],
            [13,26], [14,25], [15,24],
            [16,23], [17,22], [18,21],
            [19,20]
            ]

        #print(self.__logicalX)
        from copy import deepcopy

        for num in range(0,40):
            row.append(0)

        for num in range(0,256):
            self.__table.append(deepcopy(row))

        e = Thread(target=self.generateTableCommon)
        e.daemon=True
        e.start()

    def shiftON(self, event):
        self.__ctrl = True

    def shiftOff(self, event):
        self.__ctrl = False

    def drawMode(self, event):
        if self.__draw == 1:
            self.__draw = 0
        else:
            self.__draw = 1


    def generateTableCommon(self):
        w = round(self.__topLevel.getTopLevelDimensions()[0]/40*self.__puff)
        h = round(self.__topLevel.getTopLevelDimensions()[1]/self.__Y*self.__piff)
        self.__frames = {}
        self.__buttons = {}

        for Y in range(0,self.__Y):
            for X in range(0,40):
                f = Frame(self.__theField, width=w, height=h, bg=self.__colors.getColor("boxBackNormal"))
                f.pack_propagate(False)
                f.place(x=w*X, y=h*Y)
                self.__motion = False

                b = Button(f, name=(str(X) +","+str(Y)), bg=self.__colors.getColor("boxBackNormal"),
                           relief=GROOVE, activebackground=self.__colors.getColor("highLight"))
                b.bind("<Button-1>", self.clickedCommon)
                b.bind("<Button-3>", self.clickedCommon)

                b.bind("<Enter>", self.enterCommon)


                b.pack_propagate(False)
                b.pack(fill=BOTH)

                self.__frames[str(X)+","+str(Y)] = f
                self.__buttons[str(X)+","+str(Y)] = b


    def enterCommon(self, event):
        if self.__draw:
            self.clickedCommon(event)

    def clickedCommon(self, event):
        button = 0

        try:
            button = int(str(event).split(" ")[3].split("=")[1])
        except:
            if self.__ctrl:
                button = 3
            else:
                button = 1

        if self.__ctrl==False and button == 3:
            return

        name = str(event.widget).split(".")[-1]
        X = int(name.split(",")[0])
        Y = int(name.split(",")[1])

        self.changeColor(X,Y, button)

        if (X>3 and X<36):
            for pair in self.__logicalX:
                from copy import deepcopy
                if (X in pair):
                    pairCopy = deepcopy(pair)
                    pairCopy.remove(X)
                    self.changeColor(pairCopy[0], Y, button)

    def changeColor(self, X, Y, button):
        color = ""

        if self.__ctrl:
            if button == 1:
                self.__table[Y][X] = 1
                color = self.__colors.getColor("boxFontNormal")
            else:
                self.__table[Y][X] = 0
                color = self.__colors.getColor("boxBackNormal")
        else:
            if (self.__table[Y][X] == 0):
                self.__table[Y][X] = 1
                color = self.__colors.getColor("boxFontNormal")
            else:
                self.__table[Y][X] = 0
                color = self.__colors.getColor("boxBackNormal")

        self.__buttons[str(X)+","+str(Y)].config(bg=color)

    def focusIn(self, event):
        self.focused = event.widget

    def focusOut(self, event):
        self.focused = None