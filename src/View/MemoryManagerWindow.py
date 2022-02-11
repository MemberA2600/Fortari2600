from tkinter import *
from SubMenu import SubMenu

class MemoryManagerWindow:

    def __init__(self, loader):
        self.__loader = loader
        self.firstLoad = True
        self.__loader.stopThreads.append(self)
        self.dead = False

        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs
        self.__fontManager = self.__loader.fontManager
        self.__fontSize = int(self.__screenSize[0]/1300 * self.__screenSize[1]/1050*14)
        self.__colors = self.__loader.colorPalettes
        self.__colorDict = self.__loader.colorDict
        self.__memory = self.__loader.virtualMemory.memory
        self.__arrays = self.__loader.virtualMemory.arrays

        self.__focused = None
        self.__screenSize = self.__loader.screenSize

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize*0.65), False, False, False)
        self.__tinyFont = self.__fontManager.getFont(int(self.__fontSize*0.45), False, False, False)
        self.__halfFont = self.__fontManager.getFont(int(self.__fontSize*0.57), False, False, False)


        self.__sizes = {
            "common": [round(self.__screenSize[0] / 1.3), round(self.__screenSize[1]/2  - 25)]
        }


        self.__window = SubMenu(self.__loader, "memoryManager", self.__sizes["common"][0],
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

        self.__bankChangerFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"),
                                 height= self.__topLevel.getTopLevelDimensions()[1]//19)
        self.__bankChangerFrame.pack_propagate(False)
        self.__bankChangerFrame.pack(side=TOP, anchor=N, fill=X)

        self.__bankButtons = {}

        for num in range(1, 9):

            f = Frame(self.__bankChangerFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                            width= self.__topLevel.getTopLevelDimensions()[0] // 11,
                                            height=self.__topLevel.getTopLevelDimensions()[1] // 19)
            f.pack_propagate(False)
            f.pack(side=LEFT, anchor=E, fill=Y)

            name = str(num)
            if name == "1":
               name = "global"
            else:
               name = "bank" + name

            b = Button(f, name = name, bg=self.__loader.colorPalettes.getColor("window"),
                        text = name, font = self.__smallFont, width=999999999)
            b.pack_propagate(False)
            b.pack(fill=BOTH)
            b.bind("<Button-1>", self.getNameAndChange)
            self.__bankButtons[num] = [f, b]

        self.__variableHeader = Label(self.__bankChangerFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                      fg=self.__loader.colorPalettes.getColor("font"),
                                 text = self.__dictionaries.getWordFromCurrentLanguage("variables"),
                                 font = self.__normalFont, justify = CENTER
                                      )
        self.__variableHeader.pack_propagate(False)
        self.__variableHeader.pack(side=TOP, anchor=N, fill=BOTH)


        self.__bigFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"),
                                width=self.__topLevel.getTopLevelDimensions()[0],
                                height=self.__topLevel.getTopLevelDimensions()[1] // 19 * 18)

        self.__bigFrame.pack_propagate(False)
        self.__bigFrame.pack(side=TOP, anchor=N, fill=BOTH)

        self.__listBoxesFrame = Frame(self.__bigFrame, bg=self.__loader.colorPalettes.getColor("window"),
                            width = self.__variableHeader.winfo_width())
        self.__listBoxesFrame.pack_propagate(False)
        self.__listBoxesFrame.pack(side=RIGHT, anchor=W, fill=Y)

        self.__variableListBoxFrame = Frame(self.__listBoxesFrame, bg=self.__loader.colorPalettes.getColor("window"),
                            width = self.__variableHeader.winfo_width(),
                            height=round(self.__topLevel.getTopLevelDimensions()[1] // 5 * 2.5) - (self.__topLevel.getTopLevelDimensions()[1] // 19 )
                                      )
        self.__variableListBoxFrame.pack_propagate(False)
        self.__variableListBoxFrame.pack(side=TOP, anchor=N, fill=X)

        self.__listBoxScrollBar = Scrollbar(self.__variableListBoxFrame)
        self.__variableListBox = Listbox(   self.__variableListBoxFrame, width=100000,
                                    height=1000,
                                    yscrollcommand=self.__listBoxScrollBar.set,
                                    selectmode=BROWSE,
                                    exportselection = False,
                                    font = self.__smallFont
                                    )
        self.__variableListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__variableListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__variableListBox.pack_propagate(False)


        self.__listBoxScrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__variableListBox.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__listBoxScrollBar.config(command=self.__variableListBox.yview)

        self.__arrayHeader = Label(self.__listBoxesFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                      fg=self.__loader.colorPalettes.getColor("font"),
                                 text = self.__dictionaries.getWordFromCurrentLanguage("arrays"),
                                 font = self.__normalFont, justify = CENTER
                                      )
        self.__arrayHeader.pack_propagate(False)
        self.__arrayHeader.pack(side=TOP, anchor=N, fill=X)

        self.__arrayListBoxFrame = Frame(self.__listBoxesFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                            width=self.__variableHeader.winfo_width(),
                                            height=round(self.__topLevel.getTopLevelDimensions()[1] // 5 * 2.5) - (
                                                        self.__topLevel.getTopLevelDimensions()[1] // 19)
                                            )
        self.__arrayListBoxFrame.pack_propagate(False)
        self.__arrayListBoxFrame.pack(side=TOP, anchor=N, fill=BOTH)

        self.__arrayListBoxScrollBar = Scrollbar(self.__arrayListBoxFrame)
        self.__arrayListBox = Listbox(self.__arrayListBoxFrame, width=100000,
                                         height=1000,
                                         yscrollcommand=self.__arrayListBoxScrollBar.set,
                                         selectmode=BROWSE,
                                         exportselection=False,
                                         font=self.__smallFont
                                         )
        self.__arrayListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__arrayListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__arrayListBox.pack_propagate(False)

        self.__arrayListBoxScrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__arrayListBox.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__arrayListBoxScrollBar.config(command=self.__variableListBox.yview)

        self.__allTheOthers = Frame(self.__bigFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                            width=self.__topLevel.getTopLevelDimensions()[0] - self.__variableHeader.winfo_width(),
                                            height=self.__topLevel.getTopLevelDimensions()[1] // 19 * 18)

        self.__allTheOthers.pack_propagate(False)
        self.__allTheOthers.pack(side=RIGHT, anchor=W, fill=BOTH)

        self.__freeMemoryFrameNames = Frame(self.__allTheOthers, bg=self.__loader.colorPalettes.getColor("window"),
                                            width=self.__topLevel.getTopLevelDimensions()[0] - self.__variableHeader.winfo_width(),
                                            height=self.__topLevel.getTopLevelDimensions()[1] // 19)

        self.__freeMemoryFrameNames.pack_propagate(False)
        self.__freeMemoryFrameNames.pack(side=TOP, anchor=N, fill=X)

        self.__freeMemoryFrameValues = Frame(self.__allTheOthers, bg=self.__loader.colorPalettes.getColor("window"),
                                            width=self.__topLevel.getTopLevelDimensions()[0] - self.__variableHeader.winfo_width(),
                                            height=self.__topLevel.getTopLevelDimensions()[1] // 19)

        self.__freeMemoryFrameValues.pack_propagate(False)
        self.__freeMemoryFrameValues.pack(side=TOP, anchor=N, fill=X)

        self.__freeMamoryNames = []
        self.__freeMamoryValues = []
        self.__freeMamoryTexts = []
        names = [
            "basicRam", "basicRamLocal", "saraRam", "saraRamLocal"
        ]

        self.__fuckColors = [
            ["window", "font"], ["fontDisabled", "font"]
        ]

        for num in range(0,4):
            F = Frame(self.__freeMemoryFrameNames, bg=self.__loader.colorPalettes.getColor("window"),
                      width=(self.__topLevel.getTopLevelDimensions()[0] - self.__variableHeader.winfo_width()) // 4,
                      height=self.__topLevel.getTopLevelDimensions()[1] // 19)

            F.pack_propagate(False)
            F.pack(side=LEFT, anchor=E, fill=Y)

            L = Label(F, bg=self.__loader.colorPalettes.getColor(self.__fuckColors[num%2][0]),
                         fg=self.__loader.colorPalettes.getColor(self.__fuckColors[num%2][1]), justify = CENTER,
                         width=999999, font = self.__halfFont,
                         text = self.__dictionaries.getWordFromCurrentLanguage(names[num]))

            L.pack_propagate(False)
            L.pack(side=BOTTOM, anchor=S, fill=BOTH)
            self.__freeMamoryNames.append(L)

            textShit = StringVar()

            F = Frame(self.__freeMemoryFrameValues, bg=self.__loader.colorPalettes.getColor("window"),
                      width=(self.__topLevel.getTopLevelDimensions()[0] - self.__variableHeader.winfo_width()) // 4,
                      height=self.__topLevel.getTopLevelDimensions()[1] // 19)

            F.pack_propagate(False)
            F.pack(side=LEFT, anchor=E, fill=Y)

            L = Label(F, bg=self.__loader.colorPalettes.getColor(self.__fuckColors[num%2][0]),
                         fg=self.__loader.colorPalettes.getColor(self.__fuckColors[num%2][1]), justify = CENTER,
                         width=999999, font = self.__smallFont,
                         textvariable = textShit)

            L.pack_propagate(False)
            L.pack(side=BOTTOM, anchor=S, fill=BOTH)
            self.__freeMamoryValues.append(L)
            self.__freeMamoryTexts.append(textShit)

        # From here goes the setings
        self.__bankButtons[1][1].config(
            bg=self.__loader.colorPalettes.getColor("font"),
            fg=self.__loader.colorPalettes.getColor("window")
        )
        self.changeSlot('global')

        from threading import Thread
        t = Thread(target=self.loop)
        t.daemon = True
        t.start()

    def loop(self):
        from time import sleep
        while self.__loader.mainWindow.dead == False and self.dead == False:
            #self.__colorFiller.config(bg = self.__loader.mainWindow.getLoopColor())
            sleep(0.0001)

    def getNameAndChange(self, event):
        name = str(event.widget).split(".")[-1]
        for b in self.__bankButtons.keys():
            self.__bankButtons[b][1].config(
                bg=self.__loader.colorPalettes.getColor("window"),
                fg=self.__loader.colorPalettes.getColor("font")
            )
        event.widget.config(
            bg=self.__loader.colorPalettes.getColor("font"),
            fg=self.__loader.colorPalettes.getColor("window")
        )


        self.changeSlot(name)

    def changeSlot(self, slot):
        self.__selectedSlot = slot
        self.__variableList = self.getAllVariablesOfSlot(slot)
        self.__variableListBox.delete(0, END)
        for item in self.__variableList:
            self.__variableListBox.insert(END, item)
        self.__variableListBox.select_clear(0,END)
        self.__variableListBox.select_set(0)

        self.__arrayLst = self.getAllArraysOfSlot(slot)
        self.__arrayListBox.delete(0, END)
        for item in self.__arrayLst:
            self.__arrayListBox.insert(END, item)
        self.__arrayListBox.select_clear(0,END)
        self.__arrayListBox.select_set(0)

        self.__freeRAM = self.calculateFreeRAM(slot)
        for num in range(0,4):
            if slot == "global" and num%2 == 1 :
                self.__freeMamoryTexts[num].set("- bytes - bits")

            else:

                self.__freeMamoryTexts[num].set(
                    str(self.__freeRAM[num] // 8 ) + " bytes " +
                    str(self.__freeRAM[num] %  8 ) + " bits"
                )

                if self.__freeRAM[num] // 8 == 1:
                    self.__freeMamoryTexts[num].set(self.__freeMamoryTexts[num].get().replace("bytes", "byte"))
                if self.__freeRAM[num] %  8 == 1:
                    self.__freeMamoryTexts[num].set(self.__freeMamoryTexts[num].get().replace("bits", "bit"))

                if self.__freeRAM[num] // 8 == 0 and self.__freeRAM[num] % 8 == 0:
                    self.__freeMamoryValues[num].config(
                        bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                        fg=self.__loader.colorPalettes.getColor("boxFontUnSaved")
                    )
                else:
                    self.__freeMamoryValues[num].config(
                        bg=self.__loader.colorPalettes.getColor(self.__fuckColors[num % 2][0]),
                        fg=self.__loader.colorPalettes.getColor(self.__fuckColors[num % 2][1])
                    )

    def getAllVariablesOfSlot(self, slot):
        variableList = []
        for address in self.__memory:
            for var in self.__memory[address].variables.keys():
                if (self.__memory[address].variables[var].validity == slot
                and self.__memory[address].variables[var].system == False):
                    variableList.append(var+" ("+address+", "+
                                        self.__memory[address].variables[var].type+")")
        variableList.sort()
        return variableList

    def getAllArraysOfSlot(self, slot):
        arrayList = []
        for name in self.__arrays.keys():
            if self.__loader.virtualMemory.getArrayValidity(name) == slot \
                    or self.__loader.virtualMemory.getArrayValidity(name) == "global":
                    arrayList.append(name+" (" +self.__loader.virtualMemory.getArrayValidity(name)+ ")")

        arrayList.sort()
        return arrayList

    def calculateFreeRAM(self, slot):
        basic = 0
        sara = 0
        basicLocal = 0
        saraLocal = 0
        for address in self.__memory.keys():
            if len(address) == 3:
                basic+=len(self.__memory[address].freeBits["global"])
                if slot != "global":
                    basicLocal += len(self.__memory[address].freeBits[slot])
            else:
                sara+=len(self.__memory[address].freeBits["global"])
                if slot != "global":
                    saraLocal += len(self.__memory[address].freeBits[slot])

        return(basic, basicLocal, sara, saraLocal)