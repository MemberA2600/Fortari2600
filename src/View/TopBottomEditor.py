from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from time import sleep


class TopBottomEditor:

    def __init__(self, loader):
        self.__loader = loader
        self.__mainWindow = self.__loader.mainWindow

        self.dead = False
        self.__listBoxItems = []
        self.__lastSelected = None
        self.__lastBank     = None

        self.__activeBank = "Bank2"
        self.__activePart = "Top"
        self.__activeMode = "blank"

        # 0: The code in str format
        # 1: State if it has been changed
        # 2: The code in lines, readable for the editor
        item = ["", False, []]

        self.__codeData = {
            "Top": [
            deepcopy(item), deepcopy(item), deepcopy(item),
            deepcopy(item), deepcopy(item), deepcopy(item),
            deepcopy(item)
            ],
            "Bottom": [
                deepcopy(item), deepcopy(item), deepcopy(item),
                deepcopy(item), deepcopy(item), deepcopy(item),
                deepcopy(item)
            ]
        }

        self.importData()
        self.__loader.stopThreads.append(self)

        self.__topComment = "*** This section contains the screen elements appearing over the main display section (or can be appear standalone if the display\n" +\
                            "*** section is disabled.\n"

        self.__bottomComment = "*** This section contains the screen elements appearing undwer the main display section (or can be appear standalone if the display\n" +\
                               "*** section is disabled.\n"

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
        self.__theyAreDisabled = True

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize*0.65), False, False, False)
        self.__bigFont = self.__fontManager.getFont(int(self.__fontSize*1.15), False, False, False)
        self.__bigFont2 = self.__fontManager.getFont(int(self.__fontSize*1.5), False, False, False)
        self.__poz = 0


        self.__sizes = [self.__screenSize[0] // 1.15, self.__screenSize[1] // 1.25 - 55]
        self.__window = SubMenu(self.__loader, "screenTopBottom", self.__sizes[0], self.__sizes[1], None, self.__addElements,
                                1)
        self.dead = True

    def setArrowButtons(self):

        if len(self.__listBoxItems) > 1:
           if self.__itemListBox.curselection()[0] > 0:
               self.__moveUpButton.config(state=NORMAL)
           else:
               self.__moveUpButton.config(state=DISABLED)

           if self.__itemListBox.curselection()[0] < len(self.__listBoxItems) - 1:
               self.__moveDownButton.config(state=NORMAL)
           else:
               self.__moveDownButton.config(state=DISABLED)
        else:
            self.__moveUpButton.config(state=DISABLED)
            self.__moveDownButton.config(state=DISABLED)

    def importData(self):
        codes = self.__loader.virtualMemory.codes
        for num in range(2,9):
            bankNum = "bank"+str(num)
            for key in codes[bankNum].keys():
                if key == "screen_top":
                   self.__codeData["Top"][num - 2][0] = codes[bankNum][key].code
                   for line in self.__codeData["Top"][num - 2][0].split("\n"):
                       line = line.replace("\r", "")
                       if line.startswith("*") or line.startswith("#"):
                           continue

                       self.__codeData["Top"][num - 2][2].append(line)
                elif key == "screen_bottom":
                    self.__codeData["Bottom"][num - 2][0] = codes[bankNum][key].code
                    for line in self.__codeData["Bottom"][num - 2][0].split("\n"):
                        line = line.replace("\r", "")
                        if line.startswith("*") or line.startswith("#"):
                            continue

                        self.__codeData["Bottom"][num - 2][2].append(line)

    def __closeWindow(self):
        isThereChange = False

        for screen in self.__codeData.keys():
            for item in self.__codeData[screen]:
                if item[1] == True:
                    isThereChange = True
                    break

        if isThereChange == True:
            answer = self.__fileDialogs.askYesNoCancel("notSavedFile", "notSavedFileMessage")
            if answer == "Yes":
                self.__closeMode = True
                self.__saveAllChanges()
                if self.__saved == True:
                   self.__closeMode = False


            elif answer == "Cancel":
                self.__topLevelWindow.deiconify()
                self.__topLevelWindow.focus()
                return

        self.dead = True
        self.__topLevelWindow.destroy()
        self.__loader.topLevels.remove(self.__topLevelWindow)

    def __addElements(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()
        self.__topLevelWindow.protocol('WM_DELETE_WINDOW', self.__closeWindow)

        self.__finishedThem = [False, False, False, False]

        h = round(self.__sizes[1]//20)

        self.__bankFrame = Frame(self.__topLevelWindow, width=self.__sizes[0],
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = h)
        self.__bankFrame.pack_propagate(False)
        self.__bankFrame.pack(side=TOP, anchor=N, fill=X)

        self.__allOtherFrame = Frame(self.__topLevelWindow, width=self.__sizes[0],
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = self.__sizes[1])
        self.__allOtherFrame.pack_propagate(False)
        self.__allOtherFrame.pack(side=TOP, anchor=N, fill=BOTH)

        self.__listBoxAndManyOtherFrame = Frame(self.__allOtherFrame, width=self.__sizes[0]//7,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = self.__sizes[1])
        self.__listBoxAndManyOtherFrame.pack_propagate(False)
        self.__listBoxAndManyOtherFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__allTheFunStuff = Frame(self.__allOtherFrame, width=self.__sizes[0],
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = self.__sizes[1])
        while self.__allTheFunStuff.winfo_width() < 2 or self.__allTheFunStuff.winfo_height() < 2:
            self.__allTheFunStuff.pack_propagate(False)
            self.__allTheFunStuff.pack(side=LEFT, anchor=E, fill=BOTH)
        
        self.__uW, self.__uH = self.__allTheFunStuff.winfo_width(), self.__allTheFunStuff.winfo_height()

        h = round(self.__sizes[1]//20)

        f1 = Frame(self.__listBoxAndManyOtherFrame, width=self.__sizes[0],
                  bg=self.__loader.colorPalettes.getColor("window"),
                  height=h)
        while f1.winfo_width() < 2:
            f1.pack_propagate(False)
            f1.pack(side=TOP, anchor=N, fill=X)

        f2 = Frame(self.__listBoxAndManyOtherFrame, width=self.__sizes[0],
                  bg=self.__loader.colorPalettes.getColor("window"),
                  height=h)
        while f2.winfo_width() < 2:
            f2.pack_propagate(False)
            f2.pack(side=TOP, anchor=N, fill=X)

        f3 = Frame(self.__listBoxAndManyOtherFrame, width=self.__sizes[0],
                  bg=self.__loader.colorPalettes.getColor("window"),
                  height=h)
        while f3.winfo_width() < 2:
            f3.pack_propagate(False)
            f3.pack(side=TOP, anchor=N, fill=X)

        f4 = Frame(self.__listBoxAndManyOtherFrame, width=self.__sizes[0],
                  bg=self.__loader.colorPalettes.getColor("window"),
                  height=h * 11)
        while f4.winfo_width() < 2:
            f4.pack_propagate(False)
            f4.pack(side=TOP, anchor=N, fill=X)

        f6 = Frame(self.__listBoxAndManyOtherFrame, width=self.__sizes[0],
                  bg=self.__loader.colorPalettes.getColor("window"),
                  height=h * 4)
        while f6.winfo_width() < 2:
            f6.pack_propagate(False)
            f6.pack(side=TOP, anchor=N, fill=X)

        f5 = Frame(self.__listBoxAndManyOtherFrame, width=self.__sizes[0],
                  bg=self.__loader.colorPalettes.getColor("window"),
                  height=self.__sizes[1])
        while f5.winfo_width() < 2:
            f5.pack_propagate(False)
            f5.pack(side=TOP, anchor=N, fill=BOTH)

        t1 = Thread(target=self.__createBankButtons, args=(f1, f2, h))
        t1.daemon = True
        t1.start()

        t2 = Thread(target=self.__createListBox, args=(f3, f4))
        t2.daemon = True
        t2.start()

        self.__fuckThis = f5
        self.__fuckThis2 = f6

        t6 = Thread(target=self.__createAddButtons)
        t6.daemon = True
        t6.start()

        t3 = Thread(target=self.__createBottomButtons)
        t3.daemon = True
        t3.start()

        loop = Thread(target=self.loop)
        loop.daemon = True
        loop.start()

    def clickedListBox(self, event):
        try:
            name, typ = self.getItemAndType()
            self.setTheSetter(name, typ)
        except:
            pass

    def getItemAndType(self):
        item = self.__codeData[self.__activePart][self.getBankNum()][2][self.__itemListBox.curselection()[0]]

        name = item.split(" ")[0]
        typ = item.split(" ")[1]

        return name, typ

    def loop(self):
        num  = 0
        num2 = 0

        while self.dead == False and self.__mainWindow.dead == False:
            if False not in self.__finishedThem:
               if self.__theyAreDisabled == True:
                  for button in self.__bankButtons:
                      button.config(state = NORMAL)

                  self.__topButton.config(state = NORMAL)
                  self.__bottomButton.config(state = NORMAL)

                  self.setEditorFrame()
                  self.__theyAreDisabled = False
                  if self.__activeMode != "common":
                     self.__views.append(self.__activeBank + "|" + self.__activePart + "|" + self.__activeMode)
                  else:
                     self.__addView()


            try:
                if self.__theyAreDisabled == False:
                    self.setArrowButtons()
            except Exception as e:
                pass

            if self.__activeMode in ("blank", "missing"):
               try:
                   num2 += 1
                   if num2 == len(self.__loader.rainbowFrames) * 2: num2 = 0
                   self.__onlyLabel.config(image = self.__loader.rainbowFrames[num2 // 2])
                   self.__lockedLabel.config(
                       fg = self.__mainWindow.getLoopColor()
                   )
               except:
                   pass
            elif self.__activeMode == "locked":
                try:
                    num += 1
                    if num == len(self.__loader.lockedFramesTopLevel)*10: num = 0
                    self.__onlyLabel.config(image=self.__loader.lockedFramesTopLevel[num//10])
                    self.__lockedLabel.config(
                        fg=self.__mainWindow.getLoopColor()
                    )
                except:
                    pass

            else:
                num = 0

            sleep(0.025)

    def __addView(self):
        if len(self.__listBoxItems) > 0:
            self.__views.append(
                self.__activeBank + "|" + self.__activePart + "|" + self.__activeMode + "|" +
                self.__codeData[self.__activePart][self.getBankNum()][2][self.__itemListBox.curselection()[0]]
            )
        else:
            self.__views.append(self.__activeBank + "|" + self.__activePart + "|" + "blank")

    def setEditorFrame(self):

        for item in self.__allTheFunStuff.pack_slaves():
            item.destroy()

        locked = False
        if self.__loader.virtualMemory.locks[self.__activeBank.lower()] != None:
           locked = True

        bankNum = self.getBankNum()
        self.__topButton.config(state=NORMAL)
        self.__bottomButton.config(state=NORMAL)
        self.__addNewButton.config(state=NORMAL)
        self.__deleteButton.config(state=DISABLED)
        self.__moveUpButton.config(state=DISABLED)
        self.__moveDownButton.config(state=DISABLED)
        self.__testAllButton.config(state=DISABLED)

        if locked == True:
           self.blankAnimation("locked")
           self.__topButton.config(state = DISABLED)
           self.__bottomButton.config(state = DISABLED)
           self.__addNewButton.config(state = DISABLED)

        elif len(self.__codeData[self.__activePart][bankNum][2]) == 0:
           self.blankAnimation("blank")

        else:
            self.__activeMode = "common"
            self.__allTheFunStuff.config(bg = self.__loader.colorPalettes.getColor("window"))
            if self.__lastBank != self.getBankNum():
               self.__lastBank = self.getBankNum()
               self.fillListBox()

            if len(self.__codeData[self.__activePart][self.getBankNum()][2]) > 0:
                self.__deleteButton.config(state=NORMAL)
                self.__testAllButton.config(state=NORMAL)

                if len(self.__codeData[self.__activePart][self.getBankNum()][2]) > 1:
                    self.__moveUpButton.config(state=NORMAL)
                    self.__moveDownButton.config(state=NORMAL)

                data = self.__codeData[self.__activePart][self.getBankNum()][2][0].split(" ")
                self.setTheSetter(data[0], data[1])


    def fillListBox(self):
        self.__listBoxItems = []

        bank = self.getBankNum()

        for item in self.__codeData[self.__activePart][bank][2]:
            name = item.split(" ")[0]
            self.__listBoxItems.append(name)

        self.__itemListBox.select_clear(0, END)
        self.__itemListBox.delete(0, END)

        for item in self.__listBoxItems:
            self.__itemListBox.insert(END, item)

        if len(self.__listBoxItems) > 0:
            self.__itemListBox.select_set(0)
            item = self.__codeData[self.__activePart][bank][2][0]

            self.setTheSetter(item.split(" ")[0], item.split(" ")[1])

    def blankAnimation(self, mode):
        self.__allTheFunStuff.config(bg="black")
        items = {}

        if type(mode) != str:
            self.__activeMode = mode[0]
            items = mode[1]

        else:
            self.__activeMode = mode

        if   self.__activeMode in ("blank", "missing"):

            txt = ""
            if   self.__activeMode == "blank":
                txt = self.__dictionaries.getWordFromCurrentLanguage("emptyBank").replace("#bank#", self.__activeBank)\
                      .replace("#level#", self.__dictionaries.getWordFromCurrentLanguage(self.__activePart.lower()))

            elif self.__activeMode == "missing":
                txt = self.__dictionaries.getWordFromCurrentLanguage("missingItems")
                for key in items.keys():
                    txt = txt.replace("#"+key+"#", items[key])

            self.__pictureFrame = Frame(self.__allTheFunStuff, bd=0, bg="black",
                                        height = round(self.__allTheFunStuff.winfo_height()*0.90)
                                        )

            self.__pictureFrame.pack_propagate(False)
            self.__pictureFrame.pack(padx=0, pady=0, fill=X, side = TOP, anchor = N)
            self.__onlyLabel = Label(self.__pictureFrame, bd=0, bg="black")
            self.__onlyLabel.pack(padx=0, pady=0, fill=BOTH)

            self.__lockedLabel = Label(self.__allTheFunStuff, bd=0, bg="black",
                                       fg = "orangered",
                                       height = 10, font = self.__bigFont,
                                       text = txt
                                       )

            self.__lockedLabel.pack(padx=0, pady=0, fill=BOTH, side=BOTTOM)


        elif self.__activeMode == "locked":
            self.__pictureFrame = Frame(self.__allTheFunStuff, bd=0, bg="black",
                                        height = round(self.__allTheFunStuff.winfo_height()*0.90)
                                        )

            self.__pictureFrame.pack_propagate(False)
            self.__pictureFrame.pack(padx=0, pady=0, fill=X, side = TOP, anchor = N)
            self.__onlyLabel = Label(self.__pictureFrame, bd=0, bg="black")
            self.__onlyLabel.pack(padx=0, pady=0, fill=BOTH)

            self.__lockedLabel = Label(self.__allTheFunStuff, bd=0, bg="black",
                                       fg = "orangered",
                                       height = 10, font = self.__bigFont,
                                       text = self.__dictionaries.getWordFromCurrentLanguage("lockNChase")
                                       .replace("#bank#", self.__activeBank)
                                       .replace("#lockname#",
                                                self.__loader.virtualMemory.locks[self.__activeBank.lower()].name + " (" +
                                                self.__loader.virtualMemory.locks[self.__activeBank.lower()].type + ")" )
                                       )
            self.__lockedLabel.pack(padx=0, pady=0, fill=BOTH, side=BOTTOM)

    def __createAddButtons(self):

        f6 = self.__fuckThis2

        while f6.winfo_width() < 2:
            f6.config(width = self.__sizes[0], height = self.__sizes[1] // 20 * 3)
            f6.pack_propagate(False)
            f6.pack(side=TOP, anchor=N, fill=X)

        frame1 = Frame( f6, width = f6.winfo_width(),
                        bg = self.__loader.colorPalettes.getColor("window"),
                        height = f6.winfo_height() // 4)
        frame1.pack_propagate(False)
        frame1.pack(side=TOP, anchor=N, fill=X)

        frame2 = Frame( f6, width = f6.winfo_width(),
                        bg = self.__loader.colorPalettes.getColor("window"),
                        height = f6.winfo_height() // 4)
        frame2.pack_propagate(False)
        frame2.pack(side=TOP, anchor=N, fill=X)

        frame3 = Frame( f6, width = f6.winfo_width(),
                        bg = self.__loader.colorPalettes.getColor("window"),
                        height = f6.winfo_height() // 4)
        frame3.pack_propagate(False)
        frame3.pack(side=TOP, anchor=N, fill=X)

        frame2_1 = Frame( frame2, width = f6.winfo_width() // 2,
                        bg = self.__loader.colorPalettes.getColor("window"),
                        height = f6.winfo_height() // 4)
        frame2_1.pack_propagate(False)
        frame2_1.pack(side=LEFT, anchor=E, fill=Y)

        frame2_2 = Frame( frame2, width = f6.winfo_width() // 2,
                        bg = self.__loader.colorPalettes.getColor("window"),
                        height = f6.winfo_height() // 4)
        frame2_2.pack_propagate(False)
        frame2_2.pack(side=LEFT, anchor=E, fill=Y)

        frame4 = Frame( f6, width = f6.winfo_width(),
                        bg = self.__loader.colorPalettes.getColor("window"),
                        height = f6.winfo_height() // 4)
        frame4.pack_propagate(False)
        frame4.pack(side=TOP, anchor=N, fill=X)

        self.__upImage    = self.__loader.io.getImg("arrowUp", None)
        self.__downImage    = self.__loader.io.getImg("arrowDown", None)

        self.__addNewButton = Button(frame1, bg=self.__loader.colorPalettes.getColor("window"),
                                   text = self.__dictionaries.getWordFromCurrentLanguage("addNew"),
                                   width= frame1.winfo_width(), height = frame1.winfo_height(),
                                   state=DISABLED, font = self.__normalFont,
                                   fg = self.__loader.colorPalettes.getColor("font"),
                                   command=self.__addNew)

        self.__addNewButton.pack_propagate(False)
        self.__addNewButton.pack(fill=BOTH, side = TOP, anchor = N)

        self.__deleteButton = Button(frame3, bg=self.__loader.colorPalettes.getColor("window"),
                                   text = self.__dictionaries.getWordFromCurrentLanguage("delete"),
                                   width= frame1.winfo_width(), height = frame1.winfo_height(),
                                   state=DISABLED, font=self.__normalFont,
                                   fg=self.__loader.colorPalettes.getColor("font"),
                                   command=self.__delete)

        self.__deleteButton.pack_propagate(False)
        self.__deleteButton.pack(fill=BOTH, side = TOP, anchor = N)

        self.__moveUpButton = Button(frame2_1, bg=self.__loader.colorPalettes.getColor("window"),
                                   image=self.__upImage,
                                   width= frame1.winfo_width(), height = frame1.winfo_height(),
                                   state=DISABLED,
                                   command=self.__moveUp)

        self.__moveUpButton.pack_propagate(False)
        self.__moveUpButton.pack(fill=BOTH, side = TOP, anchor = N)

        self.__moveDownButton = Button(frame2_2, bg=self.__loader.colorPalettes.getColor("window"),
                                   image=self.__downImage,
                                   width= frame1.winfo_width(), height = frame1.winfo_height(),
                                   state=DISABLED,
                                   command=self.__moveDown)

        self.__moveDownButton.pack_propagate(False)
        self.__moveDownButton.pack(fill=BOTH, side = TOP, anchor = N)

        self.__testAllButton = Button(frame4, bg=self.__loader.colorPalettes.getColor("window"),
                                   text = self.__dictionaries.getWordFromCurrentLanguage("testScreen"),
                                   width= frame1.winfo_width(), height = frame1.winfo_height(),
                                   state=DISABLED, font=self.__normalFont,
                                   fg=self.__loader.colorPalettes.getColor("font"),
                                   command=self.__testAll)

        self.__testAllButton.pack_propagate(False)
        self.__testAllButton.pack(fill=BOTH, side = TOP, anchor = N)

        self.__finishedThem[3] = True

    def __createBottomButtons(self):
        f5 = self.__fuckThis

        while f5.winfo_width() < 2:
            f5.config(width = self.__sizes[0], height = self.__sizes[1])
            f5.pack_propagate(False)
            f5.pack(side=TOP, anchor=N, fill=BOTH)

        w = f5.winfo_width() // 4

        frame1 = Frame( f5, width = w,
                        bg=self.__loader.colorPalettes.getColor("window"),
                        height=self.__sizes[1])
        frame1.pack_propagate(False)
        frame1.pack(side=LEFT, anchor=E, fill=Y)

        frame3 = Frame( f5, width = w*2,
                        bg=self.__loader.colorPalettes.getColor("window"),
                        height=self.__sizes[1])
        frame3.pack_propagate(False)
        frame3.pack(side=LEFT, anchor=E, fill=Y)

        frame2 = Frame( f5, width = w,
                        bg=self.__loader.colorPalettes.getColor("window"),
                        height=self.__sizes[1])
        frame2.pack_propagate(False)
        frame2.pack(side=LEFT, anchor=E, fill=Y)


        #self.__saveImage    = self.__loader.io.getImg("save", None)
        #self.__saveAllImage = self.__loader.io.getImg("saveAll", None)
        self.__undoImage    = self.__loader.io.getImg("undo", None)
        self.__redoImage    = self.__loader.io.getImg("redo", None)

        self.__buffer = [deepcopy(self.__codeData)]
        self.__views  = []

        self.__undoButton = Button(frame1, bg=self.__loader.colorPalettes.getColor("window"),
                                   image=self.__undoImage,
                                   width= 9999999999, height = 9999999999999,
                                   state=DISABLED,
                                   command=self.__undoChanges)

        self.__undoButton.pack_propagate(False)
        self.__undoButton.pack(fill=BOTH, side = RIGHT, anchor = W)

        self.__redoButton = Button(frame2, bg=self.__loader.colorPalettes.getColor("window"),
                                   image=self.__redoImage,
                                   width= 9999999999, height = 99999999999999,
                                   state=DISABLED,
                                   command=self.__redoChanges)

        self.__redoButton.pack_propagate(False)
        self.__redoButton.pack(fill=BOTH, side = LEFT, anchor = E)

        self.__closeMode = False
        self.__okButton = Button(   frame3, bg=self.__loader.colorPalettes.getColor("window"),
                                    fg=self.__loader.colorPalettes.getColor("font"),
                                    text=self.__dictionaries.getWordFromCurrentLanguage("ok"),
                                    width= frame1.winfo_width(), height = frame1.winfo_height(),
                                    state=DISABLED, font = self.__normalFont,
                                    command=self.__saveAllChanges)

        self.__okButton.pack_propagate(False)
        self.__okButton.pack(fill=BOTH, side = TOP, anchor = N)

        self.__finishedThem[2] = True

    def __undoChanges(self):
        self.changePoz(0, -1, self.__undoButton)
        self.__redoButton.config(state = NORMAL)
        self.__setView()

    def __redoChanges(self):
        self.changePoz(len(self.__buffer)-1, 1, self.__redoButton)
        self.__undoButton.config(state = NORMAL)
        self.__setView()

    def changePoz(self, border, add, button):
        if len(self.__buffer) == 0 or self.__poz == border:
            button.config(state=DISABLED)
            return

        self.__poz += add
        self.__codeData = deepcopy(self.__buffer[self.__poz])
        if self.__poz == border: button.config(state = DISABLED)

    def __setView(self):
        viewData = self.__views[self.__poz].split("|")
        if len(viewData) == 3:
           self.__activeBank = viewData[0]
           self.__activePart = viewData[1]
           self.__activeMode = viewData[2]
           self.__lastBank = None
           self.__lastSelected = None

           self.setEditorFrame()
        else:
           self.__activeBank = viewData[0]
           self.__activePart = viewData[1]
           self.__activeMode = viewData[2]
           self.__lastBank = None
           self.__lastSelected = None

           self.setEditorFrame()
           data = viewData[3].split(" ")

           items = self.__codeData[self.__activePart][self.getBankNum()][2]
           itemNum = 0
           for itemNum in range(len(items)):
               if items[itemNum][0] == data[0]:
                  self.__itemListBox.select_clear(0, END)
                  self.__itemListBox.select_set(itemNum)
                  break

           self.setTheSetter(data[0], data[1])

    def __saveAllChanges(self):
        self.__saved = False
        if self.__checkIncomplete() == True: return

        screenPartsInMemory = ["screen_top", "screen_bottom"]
        screenPartsInEditor = ["Top", "Bottom"]

        wasSaved = False

        from datetime import datetime

        for num in range(0,7):
            bankNum = "bank" + str(num+2)
            for num2 in range(0,2):
                inMemory = screenPartsInMemory[num2]
                inEditor = screenPartsInEditor[num2]

                section = self.__codeData[inEditor][num]
                if section[1] == True:
                    wasSaved = True
                    newCode = ["*** Date modified on: " + str(datetime.now())]

                    section[1] = False
                    for item in section[2]:
                        newCode.append(item)

                    section[0] = "\n".join(newCode)
                    self.__loader.virtualMemory.codes[bankNum][inMemory].code = section[0]
                    self.__loader.virtualMemory.codes[bankNum][inMemory].changed = True

        if wasSaved: self.__soundPlayer.playSound("Success")

        self.__saved = True
        if self.__closeMode == False:
            self.dead = True
            self.__topLevelWindow.destroy()
            self.__loader.topLevels.remove(self.__topLevelWindow)


    def __addNew(self):
        from ScreenTopFrame import ScreenTopFrame

        self.answer = None
        self.__subMenu = ScreenTopFrame(self.__loader, self, self.__activeBank)

        name = self.answer
        if self.answer != None:
            counter = 0
            while name in self.__listBoxItems:
                name = self.answer+"_"+str(counter)
                counter += 1

            self.__listBoxItems.append(name)
            self.__itemListBox.insert(END, name)

            self.__itemListBox.select_set(0)

            bank = self.getBankNum()

            defaultDatas = {
                "ChangeFrameColor"  : name + " " + "ChangeFrameColor $00 1",
                "EmptyLines"        : name + " " + "EmptyLines 1",
                "Picture64px"       : name + " " + "Picture64px # 0 0 0",
                "Indicator"         : name + " " + "Indicator $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $",
                "BigSprite"         : name + " " + "BigSprite # # # # # # #",
                "DynamicText"       : name + " " + "DynamicText # # # # # # # # # # # # $16 $00",
                "Menu"              : name + " " + "Menu # # # # #",
                "JukeBox"           : name + " " + "JukeBox # temp16 temp17 temp18 temp19",
                "SpecialEffect"     : name + " " + "SpecialEffect $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $",
                "Reseter"           : name + " " + "Reseter 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1",
                "Wall"              : name + " " + "Wall # # # # # # $20 *None* 8 #",
                "MiniMap"           : name + " " + "MiniMap # # # # # # # #"
            }

            self.__codeData[self.__activePart][bank][2].append(deepcopy(defaultDatas[self.answer]))
            self.__codeData[self.__activePart][bank][1] = True

            self.checkForChanges()
            self.setTheSetter(name, self.answer)
        self.__topLevelWindow.deiconify()
        self.__topLevelWindow.focus()

    def setTheSetter(self, name, typ):
        #print(name, self.__lastSelected)

        try:
            if name != self.__listBoxItems[self.__itemListBox.curselection()[0]]:
                self.__itemListBox.select_clear(0, END)
                self.__itemListBox.select_set(self.__listBoxItems.index(name))
        except:
            try:
                self.__itemListBox.select_clear(0, END)
                self.__itemListBox.select_set(len(self.__listBoxItems)-1)
            except:
                self.__activeMode = "blank"
                for item in self.__allTheFunStuff.pack_slaves():
                    item.destroy()
                self.__lastBank = None
                self.__lastSelected = None
                self.setEditorFrame()

        if name != self.__lastSelected:
           self.__lastSelected = name
           bank = self.getBankNum()

           for item in self.__allTheFunStuff.pack_slaves():
               item.destroy()

           from ChangeFrameColor    import ChangeFrameColor
           from EmptyLines          import EmptyLines
           from Picture64px         import Picture64px
           from Indicator           import Indicator
           from BigSprite           import BigSprite
           from DynamicText         import DynamicText
           from Menu                import Menu
           from JukeBox             import JukeBox
           from SpecialEffect       import SpecialEffect
           from Reseter             import Reseter
           from Wall                import Wall
           from MiniMap             import MiniMap

           typs = {
               "ChangeFrameColor"   : ChangeFrameColor,
               "EmptyLines"         : EmptyLines,
               "Picture64px"        : Picture64px,
               "Indicator"          : Indicator,
               "BigSprite"          : BigSprite,
               "DynamicText"        : DynamicText,
               "Menu"               : Menu,
               "JukeBox"            : JukeBox,
               "SpecialEffect"      : Indicator,
               "Reseter"            : Reseter,
               "Wall"               : Wall,
               "MiniMap"            : MiniMap
           }

           self.__listOfNames = []

           for screenPart in self.__codeData.keys():
               for bankNum in range(0, len(self.__codeData[screenPart])):
                   for item in self.__codeData[screenPart][bankNum][2]:
                       self.__listOfNames.append(item.split(" ")[0])

           self.__setterFrame = typs[typ](  self.__loader, self.__allTheFunStuff,
                                            self.__codeData[self.__activePart][bank][2][
                                            self.__itemListBox.curselection()[0]],
                                            self.__changeName, self.__changeData, self.__uW, self.__uH,
                                            self.__activeBank.lower(), self.blankAnimation, self.__topLevelWindow, self.__listOfNames
                                            )

    def returnCodeData(self):
        return self.__codeData

    def __changeData(self, data):
        if "#" in data: return

        section = self.__codeData[self.__activePart][self.getBankNum()]
        section[1] = True

        itemNum = 0
        for itemNum in range(0, len(section[2])):
            item = section[2][itemNum].split(" ")

            if item[0] == data[0]:
               if  section[2][itemNum] != " ".join(data):
                   section[2][itemNum] = " ".join(data)
                   self.__saveBuffer()
                   self.__addView()
                   print(data)

               break

        #self.checkForChanges()

    def __changeName(self, old, new):
        section = self.__codeData[self.__activePart][self.getBankNum()]
        section[1] = True

        itemNum = 0
        for itemNum in range(0, len(section[2])):
            item = section[2][itemNum].split(" ")

            if item[0] == old:
               item[0] = new
               section[2][itemNum] = " ".join(item)
               break

        self.__listBoxItems[itemNum] = new
        self.__itemListBox.select_clear(0, END)
        self.__itemListBox.delete(itemNum)
        self.__itemListBox.insert(itemNum, new)
        self.__itemListBox.select_set(itemNum)

        self.checkForChanges()

    def __saveBuffer(self):

        while len(self.__buffer) > self.__poz+1:
           self.__buffer.pop(-1)

        if len(self.__buffer) > int(self.__config.getValueByKey("maxUndo")):
           self.__buffer.pop(0)

        self.__buffer.append(
            deepcopy(self.__codeData)
        )
        self.__poz = len(self.__buffer)-1
        self.__undoButton.config(state = NORMAL)

    def checkForChanges(self):
        wasChange = False

        for button in self.__bankButtons:
            button.config(bg = self.__loader.colorPalettes.getColor("window"))

        self.__topButton.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__bottomButton.config(bg=self.__loader.colorPalettes.getColor("window"))

        for screenType in ("Top", "Bottom"):
            for num in range(2, 9):
                bankNum = "Bank"+str(num)
                if self.__codeData[screenType][num-2][1] == True:
                   self.__bankButtons[num-2].config(bg=self.__loader.colorPalettes.getColor("highLight"))
                   if self.__activePart == screenType and self.__activeBank == bankNum:
                      wasChange = True
                      if screenType == "Top":
                          self.__topButton.config(bg=self.__loader.colorPalettes.getColor("highLight"))
                      else:
                          self.__bottomButton.config(bg=self.__loader.colorPalettes.getColor("highLight"))

        if len(self.__listBoxItems) > 0:
            self.setEditorFrame()

        if wasChange == True:
           self.__okButton.config(state = NORMAL)
           self.__saveBuffer()
           self.__addView()

        #self.setArrowButtons()

    def __delete(self):
        selected = self.__itemListBox.curselection()[0]
        self.__itemListBox.select_clear(0, END)
        self.__itemListBox.delete(selected)
        self.__listBoxItems.pop(selected)


        while True:
            try:
                if len(self.__listBoxItems) > 0:
                    self.__itemListBox.select_set(selected)
                break

            except:
                selected-=1

        bank = self.getBankNum()
        self.__codeData[self.__activePart][bank][1] = True
        self.__codeData[self.__activePart][bank][2].pop(selected)

        self.checkForChanges()
        if len(self.__listBoxItems) > 0:
            name, typ = self.getItemAndType()
            self.setTheSetter(name, typ)
        else:
            self.__activeMode = "blank"
            for item in self.__allTheFunStuff.pack_slaves():
                item.destroy()
            self.__lastBank = None
            self.__lastSelected = None
            self.setEditorFrame()

    def getBankNum(self):
        return int(self.__activeBank[-1]) - 2

    def __moveUp(self):
        self.move(-1)

    def __moveDown(self):
        self.move(1)

    def move(self, poz):

        selected = self.__itemListBox.curselection()[0]
        dataPlace = self.__codeData[self.__activePart][self.getBankNum()][2]

        item = deepcopy(dataPlace[selected])

        self.__itemListBox.select_clear(0, END)
        self.__itemListBox.delete(selected)
        self.__listBoxItems.pop(selected)
        dataPlace.pop(selected)

        newPoz = selected + poz

        dataPlace.insert(newPoz, deepcopy(item))
        name = item.split(" ")[0]
        typ  = item.split(" ")[1]

        self.__listBoxItems.insert(newPoz, name)
        self.__itemListBox.insert(newPoz, name)
        self.__itemListBox.select_set(newPoz)

        self.setTheSetter(name, typ)

    def __testAll(self):
        from ScreenTopTester import ScreenTopTester

        self.initCode = ""
        self.overScanCode = ""
        self.answer   = ""
        self.__subMenu = ScreenTopTester(self.__loader, self, self.__codeData)
        if self.answer == "NOPE":
            return

        if self.__checkIncomplete() == False:

            t = Thread(target=self.__testAllThread)
            t.daemon = True
            t.start()

    def __checkIncomplete(self):
        locks = self.__loader.virtualMemory.returnBankLocks()

        for screenPart in self.__codeData.keys():
            for bankNum in range(0, len(self.__codeData[screenPart])):
                for item in self.__codeData[screenPart][bankNum][2]:
                    item = item.split(" ")

                    for setter in item:
                        if setter == "#":
                           self.__loader.fileDialogs.displayError("incompleteItem",
                                                                  "incompleteItemError",
                                                                  {
                                                                      "item": item[0],
                                                                      "bank": "bank" + str(bankNum) + "|" + screenPart
                                                                  }, None

                                                                  )
                           self.__topLevelWindow.deiconify()
                           self.__topLevelWindow.focus()
                           return True

                    if (item[1]) == "JukeBox":
                        files = item[2].split("|")
                        for file in files:
                            locksNeeded = 1
                            testPath = self.__loader.mainWindow.projectPath + "/musics/" + file + "_bank1_double.asm"
                            try:
                                f = open(testPath, "r")
                                t = f.read()
                                f.close()
                                locksNeeded = 2

                            except:
                                pass

                            locksFound = 0
                            for key in locks.keys():
                                lock = locks[key]
                                if lock.name == file:
                                   locksFound += 1

                                   if locksFound == locksNeeded: break

                            if locksFound < locksNeeded:
                                self.__loader.fileDialogs.displayError("missingLock",
                                                                       "missingLockError",
                                                                       {
                                                                           "item": item[0],
                                                                           "bank": "bank" + str(
                                                                               bankNum) + "|" + screenPart
                                                                       }, None

                                                                       )
                                self.__topLevelWindow.deiconify()
                                self.__topLevelWindow.focus()
                                return True

        return False

    def __testAllThread(self):
        from Compiler import Compiler

        Compiler(self.__loader, self.__loader.virtualMemory.kernel,
                 "testScreenElements", [self.__codeData[self.__activePart][self.getBankNum()][2],
                                        "NTSC", self.__activeBank, self.initCode, self.overScanCode
                                        ]
                 )


    def __createBankButtons(self, f1, f2, h):

        self.__bankButtons = []
        for num in range(0, 7):
            bankNum = "Bank" + str(num + 2)
            f = Frame(  self.__bankFrame, width=self.__sizes[0]//7,
                        bg = self.__loader.colorPalettes.getColor("window"),
                        height = h)
            f.pack_propagate(False)
            f.pack(side=LEFT, anchor=E, fill=Y)

            b = Button( f, height=9999, width=9999,
                        bg=self.__loader.colorPalettes.getColor("window"),
                        fg=self.__loader.colorPalettes.getColor("font"),
                        text = bankNum, font = self.__normalFont,
                        state=DISABLED, name = bankNum.lower()
                        )
            b.pack_propagate(False)
            b.pack(side=LEFT, anchor=E, fill=BOTH)

            b.bind("<Button-1>", self.__changeSlot)
            self.__bankButtons.append(b)

        self.__topButton = Button(f1, height=9999, width=9999,
                   bg=self.__loader.colorPalettes.getColor("window"),
                   text=self.__dictionaries.getWordFromCurrentLanguage("screenTop"), font=self.__normalFont,
                   state=DISABLED, name = "top"
                   )
        self.__topButton.pack_propagate(False)
        self.__topButton.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__bottomButton = Button(f2, height=9999, width=9999,
                   bg=self.__loader.colorPalettes.getColor("window"),
                   text=self.__dictionaries.getWordFromCurrentLanguage("screenBottom"), font=self.__normalFont,
                   state=DISABLED, name = "bottom"
                   )
        self.__bottomButton.pack_propagate(False)
        self.__bottomButton.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__topButton.bind("<Button-1>", self.__changeScreenPart)
        self.__bottomButton.bind("<Button-1>", self.__changeScreenPart)

        self.__finishedThem[0] = True

    def __createListBox(self, f3, f4):

        self.__listBoxLabel = Label(f3,
                                   text=self.__dictionaries.getWordFromCurrentLanguage("screenItems"),
                                   font=self.__normalFont, fg=self.__colors.getColor("font"),
                                   bg=self.__colors.getColor("window"), justify=CENTER
                                   )

        self.__listBoxLabel.pack_propagate(False)
        self.__listBoxLabel.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__itemListScrollBar = Scrollbar(f4)
        self.__itemListBox = Listbox(   f4, width=100000,
                                        height=1000,
                                        yscrollcommand=self.__itemListScrollBar.set,
                                        selectmode=BROWSE,
                                        exportselection = False,
                                        font = self.__miniFont,
                                        justify = CENTER
                                    )

        self.__itemListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__itemListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__itemListBox.pack_propagate(False)

        self.__itemListScrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__itemListBox.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__itemListScrollBar.config(command=self.__itemListBox.yview)

        self.__finishedThem[1] = True
        self.__itemListBox.bind("<ButtonRelease-1>", self.clickedListBox)
        self.__itemListBox.bind("<KeyRelease-Up>", self.clickedListBox)
        self.__itemListBox.bind("<KeyRelease-Down>", self.clickedListBox)


    def __changeSlot(self, event):
        if False in self.__finishedThem:
            return

        if event.widget.cget('state') == DISABLED:
            return

        name = str(str(event.widget)).split(".")[-1]
        self.__activeBank = name[0].upper() + name[1:]
        self.__lastBank = None
        self.__lastSelected = None
        self.setEditorFrame()


    def __changeScreenPart(self, event):
        if False in self.__finishedThem:
            return

        if event.widget.cget('state') == DISABLED:
            return

        name = str(str(event.widget)).split(".")[-1]
        self.__activePart = name[0].upper() + name[1:]
        self.__lastBank = None
        self.__lastSelected = None
        self.setEditorFrame()
