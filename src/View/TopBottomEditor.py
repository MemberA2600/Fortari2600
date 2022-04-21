from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy

class TopBottomEditor:

    def __init__(self, loader):
        self.__loader = loader
        self.__mainWindow = self.__loader.mainWindow

        self.dead = False

        self.__activeBank = "Bank2"
        self.__activePart = "Top"


        # 0: The cose in str format
        # 1: State if it has been changed
        # 2: The code in lines, readable for the editor
        item = ["", False, []]

        self.__codeDataTop = [
            deepcopy(item), deepcopy(item), deepcopy(item),
            deepcopy(item), deepcopy(item), deepcopy(item),
            deepcopy(item)
        ]

        self.__codeDataBottom = [
            deepcopy(item), deepcopy(item), deepcopy(item),
            deepcopy(item), deepcopy(item), deepcopy(item),
            deepcopy(item)
        ]

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

    def importData(self):
        for num in range(2,9):
            f = open(self.__mainWindow.projectPath+"bank"+str(num)+"/screen_top.a26", "r")
            self.__codeDataTop[num-2][0] = f.read()
            f.close()

            f = open(self.__mainWindow.projectPath+"bank"+str(num)+"/screen_bottom.a26", "r")
            self.__codeDataBottom[num-2][0] = f.read()
            f.close()

    def __closeWindow(self):
        isThereChange = False

        for item in self.__codeDataTop:
            if item[1] == True:
                isThereChange = True
                break

        if isThereChange == False:
            for item in self.__codeDataBottom:
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

        """
        self.__topBottomFrame = Frame(self.__topLevelWindow, width=self.__sizes[0],
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   height = h)
        self.__topBottomFrame.pack_propagate(False)
        self.__topBottomFrame.pack(side=TOP, anchor=N, fill=X)
        """

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

        frame2 = Frame( f5, width = w,
                        bg=self.__loader.colorPalettes.getColor("window"),
                        height=self.__sizes[1])
        frame2.pack_propagate(False)
        frame2.pack(side=LEFT, anchor=E, fill=Y)

        frame3 = Frame( f5, width = w,
                        bg=self.__loader.colorPalettes.getColor("window"),
                        height=self.__sizes[1])
        frame3.pack_propagate(False)
        frame3.pack(side=LEFT, anchor=E, fill=Y)

        frame4 = Frame( f5, width = w,
                        bg=self.__loader.colorPalettes.getColor("window"),
                        height=self.__sizes[1])
        frame4.pack_propagate(False)
        frame4.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__saveImage    = self.__loader.io.getImg("save", None)
        self.__saveAllImage = self.__loader.io.getImg("saveAll", None)
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

        self.__finishedThem[2] = True

    def __undoChanges(self):
        pass

    def __redoChanges(self):
        pass

    def __saveChanges(self):
        pass

    def __saveAllChanges(self):
        pass

    def __addNew(self):
        pass

    def __delete(self):
        pass

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
                                        font = self.__smallFont
                                    )

        self.__itemListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__itemListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__itemListBox.pack_propagate(False)

        self.__itemListScrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__itemListBox.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__itemListScrollBar.config(command=self.__itemListBox.yview)

        self.__finishedThem[1] = True


    def __changeSlot(self, event):
        if False in self.__finishedThem:
            return

        if event.widget.cget('state') == DISABLED:
            return

        name = str(str(event.widget)).split(".")[-1]

    def __changeScreenPart(self, event):
        if False in self.__finishedThem:
            return

        if event.widget.cget('state') == DISABLED:
            return

        name = str(str(event.widget)).split(".")[-1]

    def __saveAll(self):
        pass