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

        self.__sizes = [self.__screenSize[0] // 1.15, self.__screenSize[1] // 1.25 - 55]
        self.__window = SubMenu(self.__loader, "screenTopBottom", self.__sizes[0], self.__sizes[1], None, self.__addElements,
                                1)
        self.dead = True

    def setArrowButtons(self):
        self.__moveUpButton.config(state   = DISABLED)
        self.__moveDownButton.config(state = DISABLED)

        if len(self.__listBoxItems) > 1:
           if self.__itemListBox.curselection()[0] > 0:
               self.__moveUpButton.config(state=NORMAL)
           if self.__itemListBox.curselection()[0] < len(self.__listBoxItems) - 1:
               self.__moveDownButton.config(state=NORMAL)



    def importData(self):
        codes = self.__loader.virtualMemory.codes
        for num in range(2,9):
            bankNum = "bank"+str(num)
            for key in codes.keys():
                if   key == "screen_top":
                   self.__codeData["Top"][num - 2][0] = codes[bankNum][key]
                   for line in self.__codeData["Top"][num - 2][0].split("\n"):
                       line = line.replace("\r", "")
                       if line.startswith("*") or line.startswith("#"):
                           continue

                       self.__codeData["Top"][num - 2][2].append(line)
                elif key == "screen_bottom":
                    self.__codeData["Bottom"][num - 2][0] = codes[bankNum][key]
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
                self.__saveAll()
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
        self.__allTheFunStuff.pack_propagate(False)
        self.__allTheFunStuff.pack(side=LEFT, anchor=E, fill=BOTH)

        h = round(self.__sizes[1]//20)

        f1 = Frame(self.__listBoxAndManyOtherFrame, width=self.__sizes[0],
                  bg=self.__loader.colorPalettes.getColor("window"),
                  height=h)
        f1.pack_propagate(False)
        f1.pack(side=TOP, anchor=N, fill=X)

        f2 = Frame(self.__listBoxAndManyOtherFrame, width=self.__sizes[0],
                  bg=self.__loader.colorPalettes.getColor("window"),
                  height=h)
        f2.pack_propagate(False)
        f2.pack(side=TOP, anchor=N, fill=X)

        f3 = Frame(self.__listBoxAndManyOtherFrame, width=self.__sizes[0],
                  bg=self.__loader.colorPalettes.getColor("window"),
                  height=h)
        f3.pack_propagate(False)
        f3.pack(side=TOP, anchor=N, fill=X)

        f4 = Frame(self.__listBoxAndManyOtherFrame, width=self.__sizes[0],
                  bg=self.__loader.colorPalettes.getColor("window"),
                  height=h * 11)
        f4.pack_propagate(False)
        f4.pack(side=TOP, anchor=N, fill=X)

        f6 = Frame(self.__listBoxAndManyOtherFrame, width=self.__sizes[0],
                  bg=self.__loader.colorPalettes.getColor("window"),
                  height=h * 4)
        f6.pack_propagate(False)
        f6.pack(side=TOP, anchor=N, fill=X)

        f5 = Frame(self.__listBoxAndManyOtherFrame, width=self.__sizes[0],
                  bg=self.__loader.colorPalettes.getColor("window"),
                  height=self.__sizes[1])
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
        if False not in self.__finishedThem:
           self.setArrowButtons()

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

            if self.__activeMode == "blank":
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
        self.__activeMode = mode

        if   self.__activeMode == "blank":
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
                                       text = self.__dictionaries.getWordFromCurrentLanguage("emptyBank")
                                       .replace("#bank#", self.__activeBank)
                                       .replace("#level#",
                                                self.__dictionaries.getWordFromCurrentLanguage(
                                                    self.__activePart.lower())))

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
                                   command=self.__moveUp)

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


        self.__undoButton = Button(frame1, bg=self.__loader.colorPalettes.getColor("window"),
                                   image=self.__undoImage,
                                   width= frame1.winfo_width(), height = frame1.winfo_height(),
                                   state=DISABLED,
                                   command=self.__undoChanges)

        self.__undoButton.pack_propagate(False)
        self.__undoButton.pack(fill=BOTH, side = TOP, anchor = N)

        self.__redoButton = Button(frame2, bg=self.__loader.colorPalettes.getColor("window"),
                                   image=self.__redoImage,
                                   width= frame1.winfo_width(), height = frame1.winfo_height(),
                                   state=DISABLED,
                                   command=self.__redoChanges)

        self.__redoButton.pack_propagate(False)
        self.__redoButton.pack(fill=BOTH, side = TOP, anchor = N)

        """
        self.__saveButton = Button(frame3, bg=self.__loader.colorPalettes.getColor("window"),
                                   image=self.__saveImage,
                                   width= frame1.winfo_width(), height = frame1.winfo_height(),
                                   state=DISABLED,
                                   command=self.__saveChanges)

        self.__saveButton.pack_propagate(False)
        self.__saveButton.pack(fill=BOTH, side = TOP, anchor = N)

        self.__saveAllButton = Button(frame4, bg=self.__loader.colorPalettes.getColor("window"),
                                   image=self.__saveAllImage,
                                   width= frame1.winfo_width(), height = frame1.winfo_height(),
                                   state=DISABLED,
                                   command=self.__saveAllChanges)

        self.__saveAllButton.pack_propagate(False)
        self.__saveAllButton.pack(fill=BOTH, side = TOP, anchor = N)
        """

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
        pass

    def __redoChanges(self):
        pass

    def __saveAllChanges(self):
        pass

    def __addNew(self):
        from ScreenTopFrame import ScreenTopFrame

        self.answer = None
        self.__subMenu = ScreenTopFrame(self.__loader, self)

        name = self.answer
        if self.answer != None:
            counter = 0
            while name in self.__listBoxItems:
                name = self.answer+"_"+str(counter)

            self.__listBoxItems.append(name)
            self.__itemListBox.insert(END, name)

            self.__itemListBox.select_set(0)

            bank = self.getBankNum()

            if self.answer == "ChangeFrameColor":
               defaultData = name + " " + "ChangeFrameColor $00"
               self.__codeData[self.__activePart][bank][2].append(deepcopy(defaultData))
               self.__codeData[self.__activePart][bank][1] = True

            self.checkForChanges()
            self.setTheSetter(name, self.answer)

    def setTheSetter(self, name, typ):
        if name != self.__listBoxItems[self.__itemListBox.curselection()[0]]:
           self.__itemListBox.select_clear(0, END)
           self.__itemListBox.select_set(self.__listBoxItems.index(name))

        if name != self.__lastSelected:

           self.__lastSelected = name
           bank = self.getBankNum()

           if typ == "ChangeFrameColor":
              from ChangeFrameColor import ChangeFrameColor

              self.__setterFrame = ChangeFrameColor(self.__loader, self.__allTheFunStuff,
                                                    self.__codeData[self.__activePart][bank][2][
                                                    self.__itemListBox.curselection()[0]])

    def checkForChanges(self):
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
                      if screenType == "Top":
                          self.__topButton.config(bg=self.__loader.colorPalettes.getColor("highLight"))
                      else:
                          self.__bottomButton.config(bg=self.__loader.colorPalettes.getColor("highLight"))

        self.setEditorFrame()
        self.setArrowButtons()

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


        self.checkForChanges()
        if len(self.__listBoxItems) > 0:
            item = self.__codeData[self.__activePart][self.getBankNum()][2][selected]
            name = item.split(" ")[0]
            typ  = item.split(" ")[1]

            self.setTheSetter(name, typ)


    def getBankNum(self):
        return int(self.__activeBank[-1]) - 2

    def __moveUp(self):
        pass

    def __moveDown(self):
        pass

    def __testAll(self):
        pass

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
        self.__itemListBox.bind("<Button-1>", self.clickedListBox)


    def __changeSlot(self, event):
        if False in self.__finishedThem:
            return

        if event.widget.cget('state') == DISABLED:
            return

        name = str(str(event.widget)).split(".")[-1]
        self.__activeBank = name[0].upper() + name[1:]
        self.setEditorFrame()

    def __changeScreenPart(self, event):
        if False in self.__finishedThem:
            return

        if event.widget.cget('state') == DISABLED:
            return

        name = str(str(event.widget)).split(".")[-1]
        self.__activePart = name[0].upper() + name[1:]
        self.setEditorFrame()

    def __saveAll(self):
        pass