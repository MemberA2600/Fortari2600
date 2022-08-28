from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from time import sleep

class ScreenTopFrame:

    def __init__(self, loader, caller, bank):

        self.__loader = loader
        self.__mainWindow = self.__loader.mainWindow
        self.dead = False
        self.__caller = caller

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
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize * 0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize * 0.65), False, False, False)
        self.__bigFont = self.__fontManager.getFont(int(self.__fontSize * 1.15), False, False, False)
        self.__bigFont2 = self.__fontManager.getFont(int(self.__fontSize * 1.5), False, False, False)

        self.__bank         = bank

        self.__sizes = [self.__screenSize[0] // 3.75, self.__screenSize[1] // 3.15 - 55]
        self.__window = SubMenu(self.__loader, "screenItem", self.__sizes[0], self.__sizes[1], None, self.__addElements,
                                2)
        self.dead = True


    def __closeWindow(self):
        self.dead = True
        self.__topLevelWindow.destroy()
        self.__loader.topLevels.remove(self.__topLevelWindow)

    def __addElements(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()
        self.__topLevelWindow.protocol('WM_DELETE_WINDOW', self.__closeWindow)

        self.__frame1 = Frame(  self.__topLevelWindow, width=self.__sizes[0],
                        bg = self.__loader.colorPalettes.getColor("window"),
                        height = self.__sizes[1]*0.90)
        self.__frame1.pack_propagate(False)
        self.__frame1.pack(side=TOP, anchor=N, fill=X)

        self.__frame2 = Frame(  self.__topLevelWindow, width=self.__sizes[0],
                        bg = self.__loader.colorPalettes.getColor("window"),
                        height = self.__sizes[1]*0.10)
        self.__frame2.pack_propagate(False)
        self.__frame2.pack(side=TOP, anchor=N, fill=BOTH)

        self.__listBoxLabel = Label(self.__frame1,
                                   text=self.__dictionaries.getWordFromCurrentLanguage("availableScreenElements")+":",
                                   font=self.__normalFont, fg=self.__colors.getColor("font"),
                                   bg=self.__colors.getColor("window"), justify=CENTER
                                   )

        self.__listBoxLabel.pack_propagate(False)
        self.__listBoxLabel.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__frame3 = Frame(  self.__frame1, width=self.__sizes[0],
                        bg = self.__loader.colorPalettes.getColor("window"),
                        height = self.__sizes[1]*0.90)
        self.__frame3.pack_propagate(False)
        self.__frame3.pack(side=TOP, anchor=N, fill=BOTH)

        self.__itemListScrollBar = Scrollbar(self.__frame3)
        self.__itemListBox = Listbox(   self.__frame3, width=100000,
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

        self.__frame4 = Frame(  self.__frame2, width=self.__sizes[0]*0.5,
                        bg = self.__loader.colorPalettes.getColor("window"),
                        height = self.__sizes[1])
        self.__frame4.pack_propagate(False)
        self.__frame4.pack(side=LEFT, anchor=E, fill=Y)

        self.__frame5 = Frame(  self.__frame2, width=self.__sizes[0]*0.5,
                        bg = self.__loader.colorPalettes.getColor("window"),
                        height = self.__sizes[1])
        self.__frame5.pack_propagate(False)
        self.__frame5.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__button1 = Button(self.__frame4, bg=self.__loader.colorPalettes.getColor("window"),
                                   text = self.__dictionaries.getWordFromCurrentLanguage("ok"),
                                   width= self.__frame4.winfo_width(), height = self.__frame4.winfo_height(),
                                   font = self.__normalFont,
                                   fg = self.__loader.colorPalettes.getColor("font"),
                                   command=self.__OK)

        self.__button1.pack_propagate(False)
        self.__button1.pack(fill=BOTH, side = TOP, anchor = N)

        self.__button2 = Button(self.__frame5, bg=self.__loader.colorPalettes.getColor("window"),
                                   text = self.__dictionaries.getWordFromCurrentLanguage("cancel"),
                                   width= self.__frame4.winfo_width(), height = self.__frame4.winfo_height(),
                                   font = self.__normalFont,
                                   fg = self.__loader.colorPalettes.getColor("font"),
                                   command=self.__cancel)

        self.__button2.pack_propagate(False)
        self.__button2.pack(fill=BOTH, side = TOP, anchor = N)

        self.__listBoxItems = []
        import os

        for root, dirs, files in os.walk("src/View/ScreenElements"):
            for file in files:
                if root == "src/View/ScreenElements" and ".py" in file:
                   if file == "JukeBox.py":
                      if self.getIfThereIsAlreadyAJukeBoxAdded() == True: continue

                   self.__listBoxItems.append(file.replace(".py", ""))
                   self.__itemListBox.insert(END, file.replace(".py", ""))

        self.__itemListBox.select_set(0)

    def __OK(self):
        self.__caller.answer = self.__listBoxItems[self.__itemListBox.curselection()[0]]
        self.__closeWindow()

    def __cancel(self):
        self.__closeWindow()

    def getIfThereIsAlreadyAJukeBoxAdded(self):
        __codeData = self.__caller.returnCodeData()

        for screenPart in __codeData.keys():
            for item in __codeData[screenPart][int(self.__bank[-1])-2][2]:
                item = item.split(" ")
                if item[1] == "JukeBox": return True

        return False