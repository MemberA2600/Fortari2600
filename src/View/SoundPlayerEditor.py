from SubMenu import SubMenu
from SubMenuLabel import SubMenuLabel
from SubMenuFrame import SubMenuFrame
from tkinter import *
import re
from time import sleep
from threading import Thread

class SoundPlayerEditor:

    def __init__(self, loader, mainWindow):
        self.__loader = loader
        self.__mainWindow = mainWindow

        self.firstLoad = True
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

        self.__sizes = {
            "common": [self.__screenSize[0] / 6, self.__screenSize[1]/5  - 25]
        }


        self.__window = SubMenu(self.__loader, "soundPlayer", self.__sizes["common"][0],
                                self.__sizes["common"][1], None, self.__addElements, 1)

        self.dead = True

    def __closeWindow(self):
        self.dead = True
        self.__topLevelWindow.destroy()
        self.__loader.topLevels.remove(self.__topLevelWindow)

    def __addElements(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()
        self.__topLevelWindow.protocol('WM_DELETE_WINDOW', self.__closeWindow)

        self.__labelText = StringVar()

        self.__topLabel = Label(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("font"),
                                fg=self.__loader.colorPalettes.getColor("window"), font = self.__smallFont,
                                width = 9999999,
                                textvariable = self.__labelText)
        self.__topLabel.pack_propagate(False)
        self.__topLabel.pack(side=TOP, anchor=N, fill=X)

        self.__topFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"),
                                 height= self.__topLevel.getTopLevelDimensions()[1]//5)
        self.__topFrame.pack_propagate(False)
        self.__topFrame.pack(side=TOP, anchor=N, fill=X)

        self.__buttonFrame1 = Frame(self.__topFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 width=  self.__topLevel.getTopLevelDimensions()[0]//3,
                                 height= self.__topLevel.getTopLevelDimensions()[1]//5)
        self.__buttonFrame1.pack_propagate(False)
        self.__buttonFrame1.pack(side=LEFT, anchor=E, fill=Y)

        self.__buttonFrame2 = Frame(self.__topFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 width=  self.__topLevel.getTopLevelDimensions()[0]//3,
                                 height= self.__topLevel.getTopLevelDimensions()[1]//5)
        self.__buttonFrame2.pack_propagate(False)
        self.__buttonFrame2.pack(side=LEFT, anchor=E, fill=Y)

        self.__buttonFrame3 = Frame(self.__topFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 width=  self.__topLevel.getTopLevelDimensions()[0]//3,
                                 height= self.__topLevel.getTopLevelDimensions()[1]//5)
        self.__buttonFrame3.pack_propagate(False)
        self.__buttonFrame3.pack(side=LEFT, anchor=E, fill=Y)

        self.__openImage = self.__loader.io.getImg("open", None)
        self.__recordImage = self.__loader.io.getImg("record", None)
        self.__robotImage = self.__loader.io.getImg("robot", None)


        self.__openButton = Button(self.__buttonFrame1, bg=self.__loader.colorPalettes.getColor("window"),
                                   name="openSound",
                                   image=self.__openImage, width=999999999, command=None)
        self.__openButton.pack_propagate(False)
        self.__openButton.pack(fill=BOTH)

        self.__recordButton = Button(self.__buttonFrame2, bg=self.__loader.colorPalettes.getColor("window"),
                                     name="recordSound",
                                   image=self.__recordImage, width=999999999, command=None)
        self.__recordButton.pack_propagate(False)
        self.__recordButton.pack(fill=BOTH)

        self.__robotButton = Button(self.__buttonFrame3, bg=self.__loader.colorPalettes.getColor("window"),
                                    name="generateSpeech",
                                   image=self.__robotImage, width=999999999, command=None)
        self.__robotButton.pack_propagate(False)
        self.__robotButton.pack(fill=BOTH)

        self.__mouseHover     = False
        self.__mouseHoverSave = False

        self.__openButton.bind("<Enter>", self.__mouseEnter)
        self.__recordButton.bind("<Enter>", self.__mouseEnter)
        self.__robotButton.bind("<Enter>", self.__mouseEnter)

        self.__openButton.bind("<Leave>", self.__mouseLeave)
        self.__recordButton.bind("<Leave>", self.__mouseLeave)
        self.__robotButton.bind("<Leave>", self.__mouseLeave)

        from threading import Thread
        t = Thread(target=self.checker)
        t.daemon = True
        t.start()

    def checker(self):
        from time import sleep
        while(self.dead==False and self.__loader.mainWindow.dead == False):
            if self.__mouseHover != self.__mouseHoverSave:
               self.__mouseHoverSave = self.__mouseHover

            sleep(0.00005)

    def __mouseLeave(self, event):
        self.__labelText.set("")

    def __mouseEnter(self, event):
        name = str(event.widget).split(".")[-1]
        self.__labelText.set(self.__dictionaries.getWordFromCurrentLanguage(name))
