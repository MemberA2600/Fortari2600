from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from time import sleep
from PIL import Image as IMAGE, ImageTk



from ScreenSetterFrameBase import ScreenSetterFrameBase

class JukeBox:

    def __init__(self, loader, baseFrame, data, changeName, changeData, w, h, currentBank, blankAnimation, topLevelWindow, itemNames):

        self.__loader = loader
        self.__baseFrame = baseFrame
        self.__data = data.split(" ")
        self.__w = w
        self.__h = h
        self.__currentBank = currentBank

        self.__changeData = changeData

        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs
        self.__fontManager = self.__loader.fontManager
        self.__fontSize = int(self.__screenSize[0]/1300 * self.__screenSize[1]/1050*14)
        self.__colors = self.__loader.colorPalettes
        self.__colorDict = self.__loader.colorDict

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize*0.65), False, False, False)
        self.__bigFont = self.__fontManager.getFont(int(self.__fontSize*1.15), False, False, False)
        self.__bigFont2 = self.__fontManager.getFont(int(self.__fontSize*1.5), False, False, False)

        self.__name         = StringVar()
        self.__name.set(self.__data[0])
        self.dead = [False]

        self.__loadMusicData()

        if len(list(self.__musicData.keys())) != 0:

            self.__loadPictures()

            itWasHash = False

            if self.__data[2] == "#":
                itWasHash = True

            self.__setterBase = ScreenSetterFrameBase(loader, baseFrame, data, self.__name, changeName, self.dead, itemNames)
            self.__addElements()

            if itWasHash == True:
                self.__changeData(self.__data)

        else:
            blankAnimation(["missing", {
                               "item": "music", "folder": self.__loader.mainWindow.projectPath.split("/")[-2]+"/musics"
                           }])

    def __loadMusicData(self):
        self.__musicData = {}
        import os

        locks = self.__loader.virtualMemory.returnBankLocks()

        for root, dir, files in os.walk(self.__loader.mainWindow.projectPath + "/musics/"):
            for file in files:
                if file.endswith(".a26"):
                   name = ".".join(file.split(".")[:-1])
                   asmPairs = []

                   for root, dir, files in os.walk(self.__loader.mainWindow.projectPath + "/musics/"):
                       for file in files:
                           if (name in file) and ("overflow" not in file.split("_")[-1]) and (file.endswith(".asm")):
                               asmPairs.append(file)

                   if len(asmPairs) == 0: continue

                   self.__musicData[name] = []
                   if len(asmPairs) == 2: self.__musicData[name].append("double")
                   else:  self.__musicData[name].append("simple")


    def __loadPictures(self):

        self.__jukeBoxPix = []

        self.__loader.io.loadAnimationFrames("jukebox", 4, self.__jukeBoxPix, "png", (self.__w, round((self.__w / 1260) * 198), 1))

    def __addElements(self):
        self.__uniqueFrame = Frame(self.__baseFrame, width=self.__w,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h)

        self.__uniqueFrame.pack_propagate(False)
        self.__uniqueFrame.pack(side=TOP, anchor=N, fill=X)

        self.__jukeFrame = Label(self.__uniqueFrame, width=self.__w,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=round((self.__w / 1260) * 198),
                                   image = self.__jukeBoxPix[0]
                                 )

        self.__jukeFrame.pack_propagate(False)
        self.__jukeFrame.pack(side=TOP, anchor=N, fill=X)

        self.__errorText = StringVar()

        self.__errorLine = Label(self.__uniqueFrame, width=self.__w,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   fg=self.__loader.colorPalettes.getColor("font"),
                                   height=1,
                                   font = self.__miniFont,
                                   textvariable = self.__errorText
                                 )

        self.__errorLine.pack_propagate(False)
        self.__errorLine.pack(side=TOP, anchor=N, fill=X)

        # If others are needed, put it before this comment

        self.__boxFrame = Label(self.__uniqueFrame, width=self.__w,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=9999999
                                 )

        self.__boxFrame.pack_propagate(False)
        self.__boxFrame.pack(side=TOP, anchor=N, fill=BOTH)

        divider = 5

        self.__availableFrame = Frame(self.__boxFrame, width=self.__w // divider,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=9999999
                                 )

        self.__availableFrame.pack_propagate(False)
        self.__availableFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__availableLabel = Label(self.__availableFrame,
                                   text=self.__dictionaries.getWordFromCurrentLanguage("availableMusic")+":",
                                   font=self.__smallFont, fg=self.__colors.getColor("font"),
                                   bg=self.__colors.getColor("window"), justify=CENTER
                                   )

        self.__availableLabel.pack_propagate(False)
        self.__availableLabel.pack(side=TOP, anchor=CENTER, fill=X)

        self.__availableScrollBar = Scrollbar(self.__availableFrame)
        self.__availableListBox = Listbox(   self.__availableFrame, width=100000, name = "availableList",
                                        height=1000,
                                        yscrollcommand=self.__availableScrollBar.set,
                                        selectmode=BROWSE,
                                        exportselection = False,
                                        font = self.__miniFont,
                                        justify = LEFT
                                    )

        self.__availableListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__availableListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__availableListBox.pack_propagate(False)

        self.__availableScrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__availableListBox.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__availableScrollBar.config(command=self.__availableListBox.yview)

        self.__availableListBox.bind("<ButtonRelease-1>", self.aListBoxChanged)
        self.__availableListBox.bind("<KeyRelease-Up>", self.aListBoxChanged)
        self.__availableListBox.bind("<KeyRelease-Down>", self.aListBoxChanged)

        listOfMusic = self.__data[2]
        if    listOfMusic == "#": listOfMusic = []
        else: listOfMusic = listOfMusic.split("|")

        self.__availableListBoxItems    = []
        self.__addedListBoxItems        = []

        for key in self.__musicData.keys():
            if key not in listOfMusic:
                self.__availableListBox.insert(END, key)
                self.__availableListBoxItems.append(key)

        self.__buttonsFrame = Frame(self.__boxFrame, width=self.__w // divider // 2,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=9999999
                                 )

        self.__buttonsFrame.pack_propagate(False)
        self.__buttonsFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__removeButton = Button(self.__buttonsFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                   text = "<<", font = self.__bigFont,
                                   width= 99999, height = 1,
                                   state=DISABLED,
                                   fg = self.__loader.colorPalettes.getColor("font"),
                                   command=self.__removeSelected)

        self.__removeButton.pack_propagate(False)
        self.__removeButton.pack(fill=X, side = BOTTOM, anchor = S)

        self.__addButton = Button(self.__buttonsFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                   text = ">>", font = self.__bigFont,
                                   width= 99999, height = 1,
                                   state=DISABLED,
                                   fg = self.__loader.colorPalettes.getColor("font"),
                                   command=self.__addNew)

        self.__addButton.pack_propagate(False)
        self.__addButton.pack(fill=X, side = BOTTOM, anchor = S)

        self.__addedFrame = Frame(self.__boxFrame, width=self.__w // divider,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=9999999
                                 )

        self.__addedFrame.pack_propagate(False)
        self.__addedFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__addedLabel = Label(self.__addedFrame,
                                   text=self.__dictionaries.getWordFromCurrentLanguage("addedMusic")+":",
                                   font=self.__smallFont, fg=self.__colors.getColor("font"),
                                   bg=self.__colors.getColor("window"), justify=CENTER
                                   )

        self.__addedLabel.pack_propagate(False)
        self.__addedLabel.pack(side=TOP, anchor=CENTER, fill=X)

        self.__addedScrollBar = Scrollbar(self.__addedFrame)
        self.__addedListBox = Listbox(   self.__addedFrame, width=100000, name = "addedList",
                                        height=1000,
                                        yscrollcommand=self.__addedScrollBar.set,
                                        selectmode=BROWSE,
                                        exportselection = False,
                                        font = self.__miniFont,
                                        justify = LEFT
                                    )

        self.__addedListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__addedListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__addedListBox.pack_propagate(False)

        self.__addedScrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__addedListBox.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__addedScrollBar.config(command=self.__addedListBox.yview)

        for item in listOfMusic:
            self.__addedListBox.insert(END, item)
            self.__addedListBoxItems.append(item)

        self.__addedListBox.bind("<ButtonRelease-1>", self.aListBoxChanged)
        self.__addedListBox.bind("<KeyRelease-Up>", self.aListBoxChanged)
        self.__addedListBox.bind("<KeyRelease-Down>", self.aListBoxChanged)

        self.__selecteds = {"availableList": "",
                            "addedList": ""}
        self.__setButtonsAndErros()

        t = Thread(target=self.jukeAnimation)
        t.daemon = True
        t.start()

    def aListBoxChanged(self, event):
        name = str(event.widget).split(".")[-1]
        listBox = event.widget
        lists = {"availableList": self.__availableListBoxItems,
                 "addedList"    : self.__addedListBoxItems}

        self.__selecteds[name] = lists[name][listBox.curselection()[0]]
        self.__setButtonsAndErros()


    def __setButtonsAndErros(self):
        if len(self.__addedListBoxItems) > 0:
           self.__removeButton.config(state = NORMAL)
        else:
           self.__removeButton.config(state = DISABLED)

        try:
            teszt = self.__addedListBox[self.__availableListBox.curselection()[0]]
        except:
            self.__removeButton.config(state=DISABLED)

        bNeeded = {"simple": 1, "double": 2}

        freeBanks     = self.__loader.virtualMemory.getBanksAvailableForLocking()
        try:
            selectedItem  = self.__availableListBoxItems[self.__availableListBox.curselection()[0]]

            neededBanks   = bNeeded[self.__musicData[selectedItem][0]]
            if neededBanks < len(freeBanks):
                self.__addButton.config(state=DISABLED)
            else:
                self.__addButton.config(state=NORMAL)
        except:
            self.__addButton.config(state=DISABLED)

    def __addNew(self):
        pass

    def __removeSelected(self):
        pass

    def jukeAnimation(self):
        from time import sleep

        num = -1

        while self.dead[0] == False and self.__loader.mainWindow.dead == False:
            num += 1
            if num > 2: num = 0
            try:
                self.__jukeFrame.config(image = self.__jukeBoxPix[num])
            except:
                break
            sleep(0.1)


