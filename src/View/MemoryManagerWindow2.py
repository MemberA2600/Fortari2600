from tkinter import *
from SubMenu import SubMenu
from time import sleep
from PIL import ImageTk, Image as IMAGE
class MemoryManagerWindow:

    def __init__(self, loader):
        self.__loader = loader

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
        self.__virtualMemory = self.__loader.virtualMemory

        self.__focused = None
        self.__screenSize = self.__loader.screenSize

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize*0.65), False, False, False)
        self.__tinyFont = self.__fontManager.getFont(int(self.__fontSize*0.45), False, False, False)
        self.__halfFont = self.__fontManager.getFont(int(self.__fontSize*0.57), False, False, False)

        self.__sizes = {
            "common": [round(self.__screenSize[0] / 1.2), round(self.__screenSize[1]/1.25  - 25)]
        }
        self.unsaved = False
        self.modifyButtonState = False
        self.__nameToDelete    = None

        self.__validName = False

        self.__numBitsOK = False
        self.__errorList = []
        self.__originalVar = []
        self.__archieveCounter = 0

        self.__window = SubMenu(self.__loader, "memoryManager", self.__sizes["common"][0],
                                self.__sizes["common"][1], None, self.__addElements, 1)

        self.dead = True

    def __closeWindow(self):
        if self.unsaved == True:
           answer = self.__fileDialogs.askYesOrNo("unsaved", "unsavedText")
           if answer == "Yes":
              self.saveAllBankNoClose()
           else:
              self.deleteArchieves()

        self.dead = True
        self.__topLevelWindow.destroy()
        self.__loader.topLevels.remove(self.__topLevelWindow)

    def deleteArchieves(self):
        for r in range(0, self.__archieveCounter):
            self.__virtualMemory.getArcPrev()
            self.__virtualMemory.archieved.pop(-1)

        self.__archieveCounter = 0

    def __addElements(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()
        self.__topLevelWindow.protocol('WM_DELETE_WINDOW', self.__closeWindow)

        self.__bankFrame = Frame(self.__topLevelWindow,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__topLevelWindow.winfo_width(),
                                 height=self.__topLevelWindow.winfo_height() // 20)
        self.__bankFrame.pack_propagate(False)
        self.__bankFrame.pack(side=TOP, anchor=E, fill=X)

        self.__hauntedFrame = Frame(self.__topLevelWindow, bg="black",
                                    width=self.__topLevelWindow.winfo_width(),
                                    height=self.__topLevelWindow.winfo_height() // 20 * 3)
        self.__hauntedFrame.pack_propagate(False)
        self.__hauntedFrame.pack(side=TOP, anchor=E, fill=X)

        from threading import Thread
        t = Thread(target = self.haunted)
        t.daemon = True
        t.start()

        self.__bankButtons  = {}
        self.__bankFrames   = []

        while self.__bankFrame.winfo_width() < 2: sleep(0.000001)

        for bankNum in range(1, 9):
            if  bankNum == 1:
                bankName = "global"
            else:
                bankName = "bank" + str(bankNum)

            f = Frame(self.__bankFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                        width= self.__bankFrame.winfo_width()  // 8,
                                        height=self.__bankFrame.winfo_height())
            f.pack_propagate(False)
            f.pack(side=LEFT, anchor=E, fill=Y)

            self.__bankFrames.append(f)

            b = Button(f, name = bankName, bg=self.__loader.colorPalettes.getColor("window"),
                        text = bankName, font = self.__smallFont, width=999999999)
            b.pack_propagate(False)
            b.pack(fill=BOTH)

            self.__loader.threadLooper.bindingMaster.addBinding(self, b, "<Button-1>", self.changeSelectedBank, 1)
            self.__bankButtons[bankName] = b

        self.__errorFrame = Frame(self.__topLevelWindow,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__topLevelWindow.winfo_width(),
                                 height=self.__topLevelWindow.winfo_height() //  40)
        self.__errorFrame.pack_propagate(False)
        self.__errorFrame.pack(side=TOP, anchor=N, fill=X)

        self.__errorLabelVal = StringVar()
        self.__errorLabel    = Label(self.__errorFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 fg=self.__loader.colorPalettes.getColor("font"),
                                 font = self.__smallFont, justify = CENTER,
                                 textvariable = self.__errorLabelVal,
                                 width=self.__topLevelWindow.winfo_width(),
                                 height=self.__topLevelWindow.winfo_height() //  40)
        self.__errorLabel.pack_propagate(False)
        self.__errorLabel.pack(side=TOP, anchor=CENTER, fill=BOTH)

        self.__underFrame = Frame(self.__topLevelWindow,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__topLevelWindow.winfo_width(),
                                 height=self.__topLevelWindow.winfo_height())
        self.__underFrame.pack_propagate(False)
        self.__underFrame.pack(side=TOP, anchor=N, fill=BOTH)

        while self.__underFrame.winfo_width() < 2: sleep(0.0000001)

        self.__varListFrame = Frame(self.__underFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__topLevelWindow.winfo_width() // 6,
                                 height=self.__topLevelWindow.winfo_height())
        self.__varListFrame.pack_propagate(False)
        self.__varListFrame.pack(side=LEFT, anchor=E, fill=Y)

        while self.__varListFrame.winfo_width() < 2: sleep(0.0000001)

        self.__varListTitleFrame = Frame(self.__varListFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__varListFrame.winfo_width(),
                                 height=self.__varListFrame.winfo_height() // 20)
        self.__varListTitleFrame.pack_propagate(False)
        self.__varListTitleFrame.pack(side=TOP, anchor=N, fill=X)

        self.__varListTitleLabel = Label(self.__varListTitleFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 fg=self.__loader.colorPalettes.getColor("font"),
                                 text = self.__dictionaries.getWordFromCurrentLanguage("variables"),
                                 font = self.__normalFont,
                                 width=self.__varListTitleFrame.winfo_width(),
                                 height=self.__varListTitleFrame.winfo_height())
        self.__varListTitleLabel.pack_propagate(False)
        self.__varListTitleLabel.pack(side=TOP, anchor=N, fill=BOTH)

        self.__addNewButtonFrame = Frame(self.__varListFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__varListFrame.winfo_width(),
                                 height=self.__varListFrame.winfo_height() // 20)
        self.__addNewButtonFrame.pack_propagate(False)
        self.__addNewButtonFrame.pack(side=BOTTOM, anchor=S, fill=X)

        self.__newNameFrame = Frame(self.__varListFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__varListFrame.winfo_width(),
                                 height=self.__varListFrame.winfo_height() // 20)
        self.__newNameFrame.pack_propagate(False)
        self.__newNameFrame.pack(side=BOTTOM, anchor=S, fill=X)

        self.__selectListButtonFrame = Frame(self.__varListFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__varListFrame.winfo_width(),
                                 height=self.__varListFrame.winfo_height() // 20)
        self.__selectListButtonFrame.pack_propagate(False)
        self.__selectListButtonFrame.pack(side=BOTTOM, anchor=S, fill=X)

        self.__listBoxFrame = Frame(self.__varListFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__varListFrame.winfo_width(),
                                 height=self.__varListFrame.winfo_height())
        self.__listBoxFrame.pack_propagate(False)
        self.__listBoxFrame.pack(side=BOTTOM, anchor=S, fill=BOTH)

        self.__addNewButton = Button(self.__addNewButtonFrame, name="addNew",
                                     bg=self.__loader.colorPalettes.getColor("window"),
                                     text=self.__dictionaries.getWordFromCurrentLanguage("insertVar"),
                                     font=self.__smallFont, width=999999999, state = DISABLED,
                                     command = self.__insertNew
                                     )
        self.__addNewButton.pack_propagate(False)
        self.__addNewButton.pack(fill=BOTH)

        self.__selectButton = Button(self.__selectListButtonFrame, name="addNew",
                                     bg=self.__loader.colorPalettes.getColor("window"),
                                     text=self.__dictionaries.getWordFromCurrentLanguage("selectVar"),
                                     font=self.__smallFont, width=999999999,
                                     command = self.__insertSelected
                                     )
        self.__selectButton.pack_propagate(False)
        self.__selectButton.pack(fill=BOTH)

        self.__newVarName   = StringVar()
        self.__newVameEntry =  Entry(self.__newNameFrame, name="newVarEntry",
                               bg=self.__colors.getColor("boxBackNormal"),
                               fg=self.__colors.getColor("boxFontNormal"),
                               width=30,
                               textvariable=self.__newVarName,
                               font=self.__smallFont)

        self.__newVameEntry.pack_propagate(False)
        self.__newVameEntry.pack(side=LEFT, anchor=E, fill=Y)

        self.__listBoxScrollBar = Scrollbar(self.__listBoxFrame)
        self.__variableListBox = Listbox(self.__listBoxFrame, width=100000,
                                         height=1000, name = "varListBox",
                                         yscrollcommand=self.__listBoxScrollBar.set,
                                         selectmode=BROWSE,
                                         exportselection=False,
                                         font=self.__smallFont
                                         )
        self.__variableListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__variableListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__variableListBox.pack_propagate(False)

        self.__listBoxScrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__variableListBox.pack(side=LEFT, anchor=W, fill=BOTH)
        self.__listBoxScrollBar.config(command=self.__variableListBox.yview)

        self.__justALine = Frame(self.__underFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__underFrame.winfo_width() // 100,
                                 height=self.__underFrame.winfo_height())
        self.__justALine.pack_propagate(False)
        self.__justALine.pack(side=LEFT, anchor=E, fill=Y)

        self.__justALine2 = Frame(self.__underFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__underFrame.winfo_width() // 100,
                                 height=self.__underFrame.winfo_height())
        self.__justALine2.pack_propagate(False)
        self.__justALine2.pack(side=RIGHT, anchor=W, fill=Y)

        self.__bigFrame = Frame(self.__underFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__underFrame.winfo_width(),
                                 height=self.__underFrame.winfo_height())
        self.__bigFrame.pack_propagate(False)
        self.__bigFrame.pack(side=LEFT, anchor=E, fill=Y)

        while self.__bigFrame.winfo_width() < 2: sleep(0.000001)

        self.__nameOfVar      = StringVar()
        self.__nameLabelFrame = Frame(self.__bigFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__bigFrame.winfo_width(),
                                 height=self.__bigFrame.winfo_height() // 15)
        self.__nameLabelFrame.pack_propagate(False)
        self.__nameLabelFrame.pack(side=TOP, anchor=N, fill=X)

        self.__nameLabelStaticFrame = Frame(self.__nameLabelFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__bigFrame.winfo_width() // 4,
                                 height=self.__bigFrame.winfo_height() // 15)
        self.__nameLabelStaticFrame.pack_propagate(False)
        self.__nameLabelStaticFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__nameLabelStaticLabel = Label(self.__nameLabelStaticFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 fg=self.__loader.colorPalettes.getColor("font"),
                                 text=self.__dictionaries.getWordFromCurrentLanguage("varName"),
                                 font=self.__normalFont, justify = LEFT, anchor = W,
                                 width=99999999,
                                 height=1)
        self.__nameLabelStaticLabel.pack_propagate(False)
        self.__nameLabelStaticLabel.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__varNameVar   =  StringVar()
        self.__varNameEntry =  Entry(self.__nameLabelFrame, name="varNameEntry",
                               bg=self.__colors.getColor("boxBackNormal"),
                               fg=self.__colors.getColor("boxFontNormal"),
                               width=99,
                               textvariable=self.__varNameVar,
                               font=self.__normalFont)

        self.__varNameEntry.pack_propagate(False)
        self.__varNameEntry.pack(side=LEFT, anchor=E, fill=Y)

        self.__varTypeFrame = Frame(self.__bigFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__bigFrame.winfo_width(),
                                 height=self.__bigFrame.winfo_height() // 15)
        self.__varTypeFrame.pack_propagate(False)
        self.__varTypeFrame.pack(side=TOP, anchor=N, fill=X)

        self.__varTypeStaticFrame = Frame(self.__varTypeFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__bigFrame.winfo_width() // 4,
                                 height=self.__bigFrame.winfo_height() // 15)
        self.__varTypeStaticFrame.pack_propagate(False)
        self.__varTypeStaticFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__varTypeStaticLabel = Label(self.__varTypeStaticFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 fg=self.__loader.colorPalettes.getColor("font"),
                                 text=self.__dictionaries.getWordFromCurrentLanguage("varType"),
                                 font=self.__normalFont, justify = LEFT, anchor = W,
                                 width=99999999,
                                 height=1)
        self.__varTypeStaticLabel.pack_propagate(False)
        self.__varTypeStaticLabel.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__varTypeSetterFrame = Frame(self.__varTypeFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__bigFrame.winfo_width() // 4,
                                 height=self.__bigFrame.winfo_height() // 15)
        self.__varTypeSetterFrame.pack_propagate(False)
        self.__varTypeSetterFrame.pack(side=LEFT, anchor=E, fill=Y)

        from FortariMB import FortariMB

        self.__varTypeHolderFrame = Frame(self.__varTypeSetterFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__bigFrame.winfo_width() // 4,
                                 height=self.__bigFrame.winfo_height() // 15)
        self.__varTypeHolderFrame.pack_propagate(False)
        self.__varTypeHolderFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__varTypeHolder      = FortariMB(self.__loader, self.__varTypeHolderFrame, NORMAL, self.__normalFont, ["byte"],
                                              list(self.__loader.virtualMemory.types.keys()), False, False, self.selectedTypeChanged, ["byte"])

        self.__allocationTypeStaticFrame = Frame(self.__varTypeFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__bigFrame.winfo_width() // 4,
                                 height=self.__bigFrame.winfo_height() // 15)
        self.__allocationTypeStaticFrame.pack_propagate(False)
        self.__allocationTypeStaticFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__allocationTypeStaticLabel = Label(self.__allocationTypeStaticFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 fg=self.__loader.colorPalettes.getColor("font"),
                                 text=(" " * 2) + self.__dictionaries.getWordFromCurrentLanguage("allocType"),
                                 font=self.__normalFont, justify = LEFT, anchor = W,
                                 width=99999999,
                                 height=1)
        self.__allocationTypeStaticLabel.pack_propagate(False)
        self.__allocationTypeStaticLabel.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__allocationSetterFrame = Frame(self.__varTypeFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__bigFrame.winfo_width() // 4,
                                 height=self.__bigFrame.winfo_height() // 15)
        self.__allocationSetterFrame.pack_propagate(False)
        self.__allocationSetterFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__varAddressFrame = Frame(self.__bigFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__bigFrame.winfo_width(),
                                 height=self.__bigFrame.winfo_height() // 15)
        self.__varAddressFrame.pack_propagate(False)
        self.__varAddressFrame.pack(side=TOP, anchor=N, fill=X)

        self.__varAddressStaticFrame = Frame(self.__varAddressFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__bigFrame.winfo_width() // 4,
                                 height=self.__bigFrame.winfo_height() // 15)
        self.__varAddressStaticFrame.pack_propagate(False)
        self.__varAddressStaticFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__varAddressStaticLabel = Label(self.__varAddressStaticFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 fg=self.__loader.colorPalettes.getColor("font"),
                                 text=self.__dictionaries.getWordFromCurrentLanguage("varAddress"),
                                 font=self.__normalFont, justify = LEFT, anchor = W,
                                 width=99999999,
                                 height=1)
        self.__varAddressStaticLabel.pack_propagate(False)
        self.__varAddressStaticLabel.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__varAddressSetterFrame = Frame(self.__varAddressFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__bigFrame.winfo_width() // 8,
                                 height=self.__bigFrame.winfo_height() // 15)
        self.__varAddressSetterFrame.pack_propagate(False)
        self.__varAddressSetterFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__varAddressVar   =  StringVar()
        self.__varAddressEntry =  Entry(self.__varAddressSetterFrame, name="varAddressEntry",
                               bg=self.__colors.getColor("boxBackNormal"),
                               fg=self.__colors.getColor("boxFontNormal"),
                               width=7, state = DISABLED, justify = CENTER,
                               textvariable=self.__varAddressVar,
                               font=self.__normalFont)

        self.__varAddressEntry.pack_propagate(False)
        self.__varAddressEntry.pack(side=LEFT, anchor=E, fill=Y)

        self.__varAddressVar.set("$80")

        self.__allocTypes = {"staticAdressing"  : self.__dictionaries.getWordFromCurrentLanguage("staticAdressing")
                           , "dynamicAllocation": self.__dictionaries.getWordFromCurrentLanguage("dynamicAllocation")}

        self.__allocTypeHolder = FortariMB(self.__loader, self.__allocationSetterFrame, NORMAL, self.__normalFont, [list(self.__allocTypes.values())[1]],
                                list(self.__allocTypes.values()), False, False, self.selectedAllocTypeChanged, [list(self.__allocTypes.values())[1]])

        if self.__loader.config.getValueByKey("advanced") != "True":
           self.__allocTypeHolder.changeState(DISABLED)

        self.__varBitsStaticFrame = Frame(self.__varAddressFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__bigFrame.winfo_width() // 6,
                                 height=self.__bigFrame.winfo_height() // 15)
        self.__varBitsStaticFrame.pack_propagate(False)
        self.__varBitsStaticFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__varBitsStaticLabel = Label(self.__varBitsStaticFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 fg=self.__loader.colorPalettes.getColor("font"),
                                 text=self.__dictionaries.getWordFromCurrentLanguage("usedBits"),
                                 font=self.__normalFont, justify = LEFT, anchor = W,
                                 width=99999999,
                                 height=1)
        self.__varBitsStaticLabel.pack_propagate(False)
        self.__varBitsStaticLabel.pack(side=LEFT, anchor=W, fill=BOTH)

        remaining = self.__bigFrame.winfo_width() \
                  - (self.__bigFrame.winfo_width() // 4
                  +  self.__bigFrame.winfo_width() // 8
                  +  self.__bigFrame.winfo_width() // 6)

        self.__varBitsMainFrame = Frame(self.__varAddressFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=remaining,
                                 height=self.__bigFrame.winfo_height() // 15)
        self.__varBitsMainFrame.pack_propagate(False)
        self.__varBitsMainFrame.pack(side=LEFT, anchor=E, fill=BOTH)

        while self.__varBitsMainFrame.winfo_width() < 2: sleep(0.000001)
        """
        self.__varBitsSwitchesFrame = Frame(self.__varBitsMainFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__varBitsMainFrame.winfo_width(),
                                 height=self.__bigFrame.winfo_height() // 30)
        self.__varBitsSwitchesFrame.pack_propagate(False)
        self.__varBitsSwitchesFrame.pack(side=TOP, anchor=N, fill=X)

        self.__varBitsNumbersFrame = Frame(self.__varBitsMainFrame,
                                            bg=self.__loader.colorPalettes.getColor("window"),
                                            width=self.__varBitsMainFrame.winfo_width(),
                                            height=self.__bigFrame.winfo_height() // 30)
        self.__varBitsNumbersFrame.pack_propagate(False)
        self.__varBitsNumbersFrame.pack(side=TOP, anchor=N, fill=X)
        """
        self.__bitsSetters = []

        self.__swOn = IMAGE.open("others/img/switchOn.png").resize(
            (remaining // 16,
             self.__bigFrame.winfo_height() // 15
             ), IMAGE.ANTIALIAS)

        self.__swOnImg = ImageTk.PhotoImage(self.__swOn)

        self.__swOff = IMAGE.open("others/img/switchOff.png").resize(
            (remaining // 16,
             self.__bigFrame.winfo_height() // 15
             ), IMAGE.ANTIALIAS)

        self.__swOffImg = ImageTk.PhotoImage(self.__swOff)

        for num in range(0, 8):
            bitDict = {}
            bitDict["numberFrame"] = Frame(self.__varBitsMainFrame,
                                            bg=self.__loader.colorPalettes.getColor("window"),
                                            width=remaining // 16,
                                            height=self.__bigFrame.winfo_height() // 15)
            bitDict["numberFrame"].pack_propagate(False)
            bitDict["numberFrame"].pack(side=RIGHT, anchor=W, fill=Y)

            bitDict["switchFrame"] = Frame(self.__varBitsMainFrame,
                                            bg=self.__loader.colorPalettes.getColor("window"),
                                            width=remaining // 16,
                                            height=self.__bigFrame.winfo_height() // 15)
            bitDict["switchFrame"].pack_propagate(False)
            bitDict["switchFrame"].pack(side=RIGHT, anchor=W, fill=Y)

            bitDict["numberLabel"] = Label(bitDict["numberFrame"],
                                              bg=self.__loader.colorPalettes.getColor("window"),
                                              fg=self.__loader.colorPalettes.getColor("fontDisabled"),
                                              text=str(num),
                                              font=self.__normalFont, justify=CENTER, anchor=CENTER,
                                              width=99999999,
                                              height=1)
            bitDict["numberLabel"].pack_propagate(False)
            bitDict["numberLabel"].pack(side=LEFT, anchor=CENTER, fill=BOTH)

            bitDict["state"]       = False
            bitDict["switchLabel"] = Label(bitDict["switchFrame"],
                                              bg=self.__loader.colorPalettes.getColor("window"),
                                              image = self.__swOffImg, name = "switch" + str(num),
                                              width=remaining // 16,
                                              height=self.__bigFrame.winfo_height() // 15)
            bitDict["switchLabel"].pack_propagate(False)
            bitDict["switchLabel"].pack(side=LEFT, anchor=CENTER, fill=BOTH)

            self.__loader.threadLooper.bindingMaster.addBinding(self, bitDict["switchLabel"], "<Button-1>",
                                                                self.switchClicked, 1)

            self.__bitsSetters.append(bitDict)

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__varAddressEntry, "<FocusOut>", self.addressChanged, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__varAddressEntry, "<KeyRelease>", self.addressChanged, 1)

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__newVameEntry, "<FocusOut>", self.checkIfNameIsOK, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__newVameEntry, "<KeyRelease>", self.checkIfNameIsOK, 1)

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__varNameEntry, "<FocusOut>", self.checkIfNameIsOK, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__varNameEntry, "<KeyRelease>", self.checkIfNameIsOK, 1)

        self.__fillerBeforeButtons = Frame(self.__bigFrame,
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       width=self.__bigFrame.winfo_width(),
                                       height=self.__bigFrame.winfo_height() // 75)
        self.__fillerBeforeButtons.pack_propagate(False)
        self.__fillerBeforeButtons.pack(side=TOP, anchor=N, fill=X)

        self.__otherThingsFrame = Frame(self.__bigFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__bigFrame.winfo_width(),
                                 height=self.__bigFrame.winfo_height() // 15)
        self.__otherThingsFrame.pack_propagate(False)
        self.__otherThingsFrame.pack(side=TOP, anchor=N, fill=X)

        self.__bcdLabelFrame = Frame(self.__otherThingsFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__bigFrame.winfo_width() // 4,
                                 height=self.__bigFrame.winfo_height() // 15)
        self.__bcdLabelFrame.pack_propagate(False)
        self.__bcdLabelFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__bcdLabel = Label(self.__bcdLabelFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 fg=self.__loader.colorPalettes.getColor("font"),
                                 text=self.__dictionaries.getWordFromCurrentLanguage("binaryEncoding")+":",
                                 font=self.__normalFont, justify = LEFT, anchor = W,
                                 width=99999999,
                                 height=1)
        self.__bcdLabel.pack_propagate(False)
        self.__bcdLabel.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__bcdSelectorFrame = Frame(self.__otherThingsFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__bigFrame.winfo_width() // 4,
                                 height=self.__bigFrame.winfo_height() // 15)
        self.__bcdSelectorFrame.pack_propagate(False)
        self.__bcdSelectorFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__encodingTypes = {"bcd"  : self.__dictionaries.getWordFromCurrentLanguage("bcd")
                              , "binary": self.__dictionaries.getWordFromCurrentLanguage("binary")}

        self.__encodingTypeHolder = FortariMB(self.__loader, self.__bcdSelectorFrame, NORMAL, self.__normalFont, [list(self.__encodingTypes.values())[1]],
                                list(self.__encodingTypes.values()), False, False, self.selectedEcondingChanged, [list(self.__encodingTypes.values())[1]])

        self.__colorLabelFrame = Frame(self.__otherThingsFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__bigFrame.winfo_width() // 4,
                                 height=self.__bigFrame.winfo_height() // 15)
        self.__colorLabelFrame.pack_propagate(False)
        self.__colorLabelFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__colorLabel = Label(self.__colorLabelFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 fg=self.__loader.colorPalettes.getColor("font"),
                                 text=(" " * 2 ) + self.__dictionaries.getWordFromCurrentLanguage("storedValue")+":",
                                 font=self.__normalFont, justify = LEFT, anchor = W,
                                 width=99999999,
                                 height=1)
        self.__colorLabel.pack_propagate(False)
        self.__colorLabel.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__contentSelectorFrame = Frame(self.__otherThingsFrame,
                                 bg=self.__loader.colorPalettes.getColor("window"),
                                 width=self.__bigFrame.winfo_width() // 4,
                                 height=self.__bigFrame.winfo_height() // 15)
        self.__contentSelectorFrame.pack_propagate(False)
        self.__contentSelectorFrame.pack(side=LEFT, anchor=E, fill=Y)


        self.__contentTypes = {"bcd"  : self.__dictionaries.getWordFromCurrentLanguage("common")
                              , "binary": self.__dictionaries.getWordFromCurrentLanguage("colorVar")}

        self.__contentHolder = FortariMB(self.__loader, self.__contentSelectorFrame, NORMAL, self.__normalFont, [list(self.__contentTypes.values())[0]],
                                list(self.__contentTypes.values()), False, False, self.selectedContentChanged, [list(self.__contentTypes.values())[0]])

        self.__importantButtonsFrame = Frame(self.__bigFrame,
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       width=self.__bigFrame.winfo_width(),
                                       height=self.__bigFrame.winfo_height() // 15)
        self.__importantButtonsFrame.pack_propagate(False)
        self.__importantButtonsFrame.pack(side=TOP, anchor=N, fill=X)

        self.__createModifyButtonFrame = Frame(self.__importantButtonsFrame,
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       width=self.__bigFrame.winfo_width() // 6,
                                       height=self.__bigFrame.winfo_height() // 15)
        self.__createModifyButtonFrame.pack_propagate(False)
        self.__createModifyButtonFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__createModifyVar = StringVar()
        self.__createModifyVar.set(self.__dictionaries.getWordFromCurrentLanguage("create"))

        self.__createModifyButton = Button(self.__createModifyButtonFrame, name="createModify",
                                     bg=self.__loader.colorPalettes.getColor("window"),
                                     textvariable = self.__createModifyVar,
                                     font=self.__smallFont, width=999999999, state = NORMAL,
                                     command = self.createModifyPressed
                                     )
        self.__createModifyButton.pack_propagate(False)
        self.__createModifyButton.pack(fill=BOTH)

        self.__fillerFrame = Frame(self.__importantButtonsFrame,
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       width=self.__bigFrame.winfo_width() // 100,
                                       height=self.__bigFrame.winfo_height() // 15)
        self.__fillerFrame.pack_propagate(False)
        self.__fillerFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__deleteButtonFrame = Frame(self.__importantButtonsFrame,
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       width=self.__bigFrame.winfo_width() // 6,
                                       height=self.__bigFrame.winfo_height() // 15)
        self.__deleteButtonFrame.pack_propagate(False)
        self.__deleteButtonFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__deleteButton = Button(self.__deleteButtonFrame, name="delete",
                                     bg=self.__loader.colorPalettes.getColor("window"),
                                     text=self.__dictionaries.getWordFromCurrentLanguage("delete"),
                                     font=self.__smallFont, width=999999999, state = DISABLED,
                                     command = self.deletePressed
                                     )
        self.__deleteButton.pack_propagate(False)
        self.__deleteButton.pack(fill=BOTH)

        self.__fillerFrame2 = Frame(self.__importantButtonsFrame,
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       width=self.__bigFrame.winfo_width() // 100,
                                       height=self.__bigFrame.winfo_height() // 15)
        self.__fillerFrame2.pack_propagate(False)
        self.__fillerFrame2.pack(side=LEFT, anchor=E, fill=Y)

        remaining = (self.__bigFrame.winfo_width() - (
                    (self.__bigFrame.winfo_width() // 6 + self.__bigFrame.winfo_width() // 100) * 2 +
                    self.__bigFrame.winfo_width() // 100
                     ))

        self.__basicRAMFrame = Frame(self.__importantButtonsFrame,
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       width=remaining // 2,
                                       height=self.__bigFrame.winfo_height() // 15)
        self.__basicRAMFrame.pack_propagate(False)
        self.__basicRAMFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__fillerFrame3 = Frame(self.__importantButtonsFrame,
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       width=self.__bigFrame.winfo_width() // 100,
                                       height=self.__bigFrame.winfo_height() // 15)
        self.__fillerFrame3.pack_propagate(False)
        self.__fillerFrame3.pack(side=LEFT, anchor=E, fill=Y)

        self.__saraRAMFrame = Frame(self.__importantButtonsFrame,
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       width=remaining // 2,
                                       height=self.__bigFrame.winfo_height() // 15)
        self.__saraRAMFrame.pack_propagate(False)
        self.__saraRAMFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__basicRAMLabelFrame = Frame(self.__basicRAMFrame,
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       width=remaining // 4,
                                       height=self.__bigFrame.winfo_height() // 15)
        self.__basicRAMLabelFrame.pack_propagate(False)
        self.__basicRAMLabelFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__saraRAMLabelFrame = Frame(self.__saraRAMFrame,
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       width=remaining // 4,
                                       height=self.__bigFrame.winfo_height() // 15)
        self.__saraRAMLabelFrame.pack_propagate(False)
        self.__saraRAMLabelFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__basicRamLabel     = Label(self.__basicRAMLabelFrame,
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       fg=self.__loader.colorPalettes.getColor("font"),
                                       width=remaining // 4,
                                       height=self.__bigFrame.winfo_height() // 15,
                                       text = self.__dictionaries.getWordFromCurrentLanguage("freeBasicRam"),
                                       font=self.__miniFont
                                         )
        self.__basicRamLabel.pack_propagate(False)
        self.__basicRamLabel.pack(side=LEFT, anchor=E, fill=Y)

        self.__saraRAMLabel    = Label(self.__saraRAMLabelFrame,
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       fg=self.__loader.colorPalettes.getColor("font"),
                                       width=remaining // 4,
                                       height=self.__bigFrame.winfo_height() // 15,
                                       text = self.__dictionaries.getWordFromCurrentLanguage("freeSaraRam"),
                                       font=self.__miniFont
                                         )
        self.__saraRAMLabel.pack_propagate(False)
        self.__saraRAMLabel.pack(side=LEFT, anchor=E, fill=Y)

        self.__basicRAM = StringVar()
        self.__saraRAM  = StringVar()

        self.__basicRAMEntryFrame = Frame(self.__basicRAMFrame,
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       width=remaining // 4,
                                       height=self.__bigFrame.winfo_height() // 15)
        self.__basicRAMEntryFrame.pack_propagate(False)
        self.__basicRAMEntryFrame.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__basicRAMEntry = Entry(self.__basicRAMEntryFrame,
                                       bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                       fg=self.__loader.colorPalettes.getColor("font"),
                                       width=9999, state = DISABLED,
                                       textvariable = self.__basicRAM,
                                       font=self.__normalFont, justify = CENTER
                                         )
        self.__basicRAMEntry.pack_propagate(False)
        self.__basicRAMEntry.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__saraRAMEntryFrame = Frame(self.__saraRAMFrame,
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       width=remaining // 4,
                                       height=self.__bigFrame.winfo_height() // 15)
        self.__saraRAMEntryFrame.pack_propagate(False)
        self.__saraRAMEntryFrame.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__saraRAMEntry = Entry(self.__saraRAMEntryFrame,
                                       bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                       fg=self.__loader.colorPalettes.getColor("font"),
                                       width=9999, state = DISABLED,
                                       textvariable = self.__saraRAM,
                                       font=self.__normalFont, justify = CENTER
                                         )
        self.__saraRAMEntry.pack_propagate(False)
        self.__saraRAMEntry.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__bottomFrame = Frame(self.__bigFrame,
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       width=self.__bigFrame.winfo_width(),
                                       height=self.__bigFrame.winfo_height() // 15)
        self.__bottomFrame.pack_propagate(False)
        self.__bottomFrame.pack(side=BOTTOM, anchor=S, fill=X)

        self.__middleFrame = Frame(self.__bigFrame,
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       width=self.__bigFrame.winfo_width(),
                                       height=self.__bigFrame.winfo_height())
        self.__middleFrame.pack_propagate(False)
        self.__middleFrame.pack(side=BOTTOM, anchor=S, fill=Y)

        while self.__middleFrame.winfo_width() < 2: sleep(0.0000000001)

        self.__overLapFrame = Frame(self.__middleFrame,
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       width=self.__middleFrame.winfo_width() // 3,
                                       height=self.__middleFrame.winfo_height())
        self.__overLapFrame.pack_propagate(False)
        self.__overLapFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__arrayFrame = Frame(self.__middleFrame,
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       width=self.__middleFrame.winfo_width() // 3 ,
                                       height=self.__middleFrame.winfo_height())
        self.__arrayFrame.pack_propagate(False)
        self.__arrayFrame.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__arrayVarFrame = Frame(self.__middleFrame,
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       width=self.__middleFrame.winfo_width() // 3 ,
                                       height=self.__middleFrame.winfo_height())
        self.__arrayVarFrame.pack_propagate(False)
        self.__arrayVarFrame.pack(side=LEFT, anchor=E, fill=BOTH)


        self.__overLapLabelFrame = Frame(self.__overLapFrame,
                                         bg=self.__loader.colorPalettes.getColor("window"),
                                         width=self.__middleFrame.winfo_width() // 3,
                                         height=self.__middleFrame.winfo_height()// 10)
        self.__overLapLabelFrame.pack_propagate(False)
        self.__overLapLabelFrame.pack(side=TOP, anchor=N, fill=X)

        self.__overLapLabel      = Label(self.__overLapLabelFrame,
                                         bg=self.__loader.colorPalettes.getColor("window"),
                                         fg=self.__loader.colorPalettes.getColor("font"),
                                         font = self.__smallFont,
                                         text = self.__dictionaries.getWordFromCurrentLanguage("memoryOverlaps"),
                                         width=self.__middleFrame.winfo_width() // 3,
                                         height=1)
        self.__overLapLabel.pack_propagate(False)
        self.__overLapLabel.pack(side=TOP, anchor=N, fill=BOTH)

        self.__overLapBox = Frame(self.__overLapFrame,
                                         bg=self.__loader.colorPalettes.getColor("window"),
                                         width=self.__middleFrame.winfo_width() // 3,
                                         height=self.__middleFrame.winfo_height()// 10 * 9)
        self.__overLapBox.pack_propagate(False)
        self.__overLapBox.pack(side=TOP, anchor=N, fill=BOTH)

        from tkinter import scrolledtext

        self.__overLapBox    = scrolledtext.ScrolledText(self.__overLapBox, width=999999, height=self.__middleFrame.winfo_height()// 10 * 9, wrap=WORD)
        self.__overLapBox.pack(fill=BOTH, side=BOTTOM, anchor=S)

        self.__overLapBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                fg=self.__loader.colorPalettes.getColor("boxFontNormal"))

        self.__getFont()
        self.__overLapBox.bind("<Key>", lambda e: "break")

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__variableListBox, "<Double-1>", self.__doubleClickedListBox, 1)

        self.__loader.threadLooper.addToThreading(self, self.loop, [], 1)

        self.__arrayLabelFrame = Frame(self.__arrayFrame,
                                         bg=self.__loader.colorPalettes.getColor("window"),
                                         width=self.__middleFrame.winfo_width() // 3,
                                         height=self.__middleFrame.winfo_height()// 10)
        self.__arrayLabelFrame.pack_propagate(False)
        self.__arrayLabelFrame.pack(side=TOP, anchor=N, fill=X)

        self.__arrayLabel      = Label(self.__arrayLabelFrame,
                                         bg=self.__loader.colorPalettes.getColor("window"),
                                         fg=self.__loader.colorPalettes.getColor("font"),
                                         font = self.__smallFont,
                                         text = self.__dictionaries.getWordFromCurrentLanguage("arrays"),
                                         width=self.__middleFrame.winfo_width() // 3,
                                         height=1)
        self.__arrayLabel.pack_propagate(False)
        self.__arrayLabel.pack(side=TOP, anchor=N, fill=BOTH)

        self.__arrayListLabelFrame = Frame(self.__arrayVarFrame,
                                         bg=self.__loader.colorPalettes.getColor("window"),
                                         width=self.__middleFrame.winfo_width() // 3,
                                         height=self.__middleFrame.winfo_height()// 10)
        self.__arrayListLabelFrame.pack_propagate(False)
        self.__arrayListLabelFrame.pack(side=TOP, anchor=N, fill=X)

        self.__arrayListLabel      = Label(self.__arrayListLabelFrame,
                                         bg=self.__loader.colorPalettes.getColor("window"),
                                         fg=self.__loader.colorPalettes.getColor("font"),
                                         font = self.__smallFont,
                                         text = self.__dictionaries.getWordFromCurrentLanguage("listOfVariables"),
                                         width=self.__middleFrame.winfo_width() // 3,
                                         height=1)
        self.__arrayListLabel.pack_propagate(False)
        self.__arrayListLabel.pack(side=TOP, anchor=N, fill=BOTH)

        self.__arrayButtonsFrame = Frame(self.__arrayFrame,
                                         bg=self.__loader.colorPalettes.getColor("window"),
                                         width=self.__middleFrame.winfo_width() // 3,
                                         height=self.__middleFrame.winfo_height()// 10 * 3)
        self.__arrayButtonsFrame.pack_propagate(False)
        self.__arrayButtonsFrame.pack(side=BOTTOM, anchor=S, fill=X)

        self.__arrayVarListButtonsFrame = Frame(self.__arrayVarFrame,
                                         bg=self.__loader.colorPalettes.getColor("window"),
                                         width=self.__middleFrame.winfo_width() // 3,
                                         height=self.__middleFrame.winfo_height()// 10 * 3)
        self.__arrayVarListButtonsFrame.pack_propagate(False)
        self.__arrayVarListButtonsFrame.pack(side=BOTTOM, anchor=S, fill=X)

        self.__arrayListBoxFrame = Frame(self.__arrayFrame,
                                         bg=self.__loader.colorPalettes.getColor("window"),
                                         width=self.__middleFrame.winfo_width() // 3,
                                         height=self.__middleFrame.winfo_height())
        self.__arrayListBoxFrame.pack_propagate(False)
        self.__arrayListBoxFrame.pack(side=BOTTOM, anchor=S, fill=BOTH)

        self.__arrayVarListBoxFrame = Frame(self.__arrayVarFrame,
                                         bg=self.__loader.colorPalettes.getColor("window"),
                                         width=self.__middleFrame.winfo_width() // 3,
                                         height=self.__middleFrame.winfo_height())
        self.__arrayVarListBoxFrame.pack_propagate(False)
        self.__arrayVarListBoxFrame.pack(side=BOTTOM, anchor=S, fill=BOTH)


        self.__arrayBoxScrollBaer = Scrollbar(self.__arrayListBoxFrame)
        self.__arrayListBox = Listbox(self.__arrayListBoxFrame, width=100000,
                                         height=1000, name = "arrayListBox",
                                         yscrollcommand=self.__arrayBoxScrollBaer.set,
                                         selectmode=BROWSE,
                                         exportselection=False,
                                         font=self.__smallFont
                                         )
        self.__arrayListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__arrayListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__arrayListBox.pack_propagate(False)

        self.__arrayBoxScrollBaer.pack(side=RIGHT, anchor=W, fill=Y)
        self.__arrayListBox.pack(side=LEFT, anchor=W, fill=BOTH)
        self.__arrayBoxScrollBaer.config(command=self.__arrayListBox.yview)

        self.__arrayListBoxScrollBaer = Scrollbar(self.__arrayVarListBoxFrame)
        self.__arrayListListBox = Listbox(self.__arrayVarListBoxFrame, width=100000,
                                         height=1000, name = "arrayListBox",
                                         yscrollcommand=self.__arrayListBoxScrollBaer.set,
                                         selectmode=BROWSE,
                                         exportselection=False,
                                         font=self.__smallFont
                                         )
        self.__arrayListListBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__arrayListListBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__arrayListListBox.pack_propagate(False)

        self.__arrayListBoxScrollBaer.pack(side=RIGHT, anchor=W, fill=Y)
        self.__arrayListListBox.pack(side=LEFT, anchor=W, fill=BOTH)
        self.__arrayListBoxScrollBaer.config(command=self.__arrayListListBox.yview)

        self.__arrayEntryFrame = Frame(self.__arrayButtonsFrame,
                                         bg=self.__loader.colorPalettes.getColor("window"),
                                         width=self.__middleFrame.winfo_width() // 3,
                                         height=self.__middleFrame.winfo_height()// 10)
        self.__arrayEntryFrame.pack_propagate(False)
        self.__arrayEntryFrame.pack(side=TOP, anchor=N, fill=X)

        self.__arrayButtonFrame1 = Frame(self.__arrayButtonsFrame,
                                         bg=self.__loader.colorPalettes.getColor("window"),
                                         width=self.__middleFrame.winfo_width() // 3,
                                         height=self.__middleFrame.winfo_height()// 10)
        self.__arrayButtonFrame1.pack_propagate(False)
        self.__arrayButtonFrame1.pack(side=TOP, anchor=N, fill=X)

        self.__arrayButtonFrame2 = Frame(self.__arrayButtonsFrame,
                                         bg=self.__loader.colorPalettes.getColor("window"),
                                         width=self.__middleFrame.winfo_width() // 3,
                                         height=self.__middleFrame.winfo_height()// 10)
        self.__arrayButtonFrame2.pack_propagate(False)
        self.__arrayButtonFrame2.pack(side=TOP, anchor=N, fill=X)

        self.__arrayButtonFrame4 = Frame(self.__arrayVarListButtonsFrame,
                                         bg=self.__loader.colorPalettes.getColor("window"),
                                         width=self.__middleFrame.winfo_width() // 3,
                                         height=self.__middleFrame.winfo_height()// 10)
        self.__arrayButtonFrame4.pack_propagate(False)
        self.__arrayButtonFrame4.pack(side=BOTTOM, anchor=S, fill=X)

        self.__arrayButtonFrame3 = Frame(self.__arrayVarListButtonsFrame,
                                         bg=self.__loader.colorPalettes.getColor("window"),
                                         width=self.__middleFrame.winfo_width() // 3,
                                         height=self.__middleFrame.winfo_height()// 10)
        self.__arrayButtonFrame3.pack_propagate(False)
        self.__arrayButtonFrame3.pack(side=BOTTOM, anchor=S, fill=X)

        self.__arrayButtonFrame5 = Frame(self.__arrayVarListButtonsFrame,
                                         bg=self.__loader.colorPalettes.getColor("window"),
                                         width=self.__middleFrame.winfo_width() // 3,
                                         height=self.__middleFrame.winfo_height()// 10)
        self.__arrayButtonFrame5.pack_propagate(False)
        self.__arrayButtonFrame5.pack(side=TOP, anchor=N, fill=X)

        self.__newArrayNameVar = StringVar()
        self.__newArrayName =  Entry(self.__arrayEntryFrame, name="newArrayEntry",
                               bg=self.__colors.getColor("boxBackNormal"),
                               fg=self.__colors.getColor("boxFontNormal"),
                               width=50,
                               textvariable=self.__newArrayNameVar,
                               font=self.__smallFont)

        self.__newArrayName.pack_propagate(False)
        self.__newArrayName.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__addNewArrayButton = Button(self.__arrayButtonFrame1, name="addNewArray",
                                     bg=self.__loader.colorPalettes.getColor("window"),
                                     text=self.__dictionaries.getWordFromCurrentLanguage("addVartoNew"),
                                     font=self.__smallFont, width=999999999, state = DISABLED,
                                     command = self.__insertToNewArray
                                     )
        self.__addNewArrayButton.pack_propagate(False)
        self.__addNewArrayButton.pack(fill=BOTH)

        self.__addToSelectedArrayButton = Button(self.__arrayButtonFrame2, name="addVarToSelectedArray",
                                     bg=self.__loader.colorPalettes.getColor("window"),
                                     text=self.__dictionaries.getWordFromCurrentLanguage("addVarToSelectedArray"),
                                     font=self.__smallFont, width=999999999, state = DISABLED,
                                     command = self.__addToSelectedArray
                                     )
        self.__addToSelectedArrayButton.pack_propagate(False)
        self.__addToSelectedArrayButton.pack(fill=BOTH)

        self.__deleteVarFromArrayButton = Button(self.__arrayButtonFrame3, name="deleteVar",
                                     bg=self.__loader.colorPalettes.getColor("window"),
                                     text=self.__dictionaries.getWordFromCurrentLanguage("deleteVar"),
                                     font=self.__smallFont, width=999999999, state = DISABLED,
                                     command = self.__deleteFromArray
                                     )
        self.__deleteVarFromArrayButton.pack_propagate(False)
        self.__deleteVarFromArrayButton.pack(fill=BOTH)

        self.__deleteArrayButton = Button(self.__arrayButtonFrame4, name="deleteArray",
                                     bg=self.__loader.colorPalettes.getColor("window"),
                                     text=self.__dictionaries.getWordFromCurrentLanguage("deleteArray"),
                                     font=self.__smallFont, width=999999999, state = DISABLED,
                                     command = self.__deleteArray
                                     )
        self.__deleteArrayButton.pack_propagate(False)
        self.__deleteArrayButton.pack(fill=BOTH)

        self.__selectArrayButton = Button(self.__arrayButtonFrame5, name="selectArray",
                                     bg=self.__loader.colorPalettes.getColor("window"),
                                     text=self.__dictionaries.getWordFromCurrentLanguage("selectArray"),
                                     font=self.__smallFont, width=999999999, state = DISABLED,
                                     command = self.selectArray
                                     )
        self.__selectArrayButton.pack_propagate(False)
        self.__selectArrayButton.pack(fill=BOTH)

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__newArrayName, "<FocusOut>"  , self.checkIfNameIsOK, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__newArrayName, "<KeyRelease>", self.checkIfNameIsOK, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__arrayListBox, "<Double-1>", self.changeArrayVarList, 1)

        while(self.__bottomFrame.winfo_width() < 2): sleep(0.00000001)

        self.__okButtonFrame = Frame(self.__bottomFrame,
                                     bg     = self.__loader.colorPalettes.getColor("window"),
                                     width  = self.__bottomFrame.winfo_width() // 6,
                                     height = self.__bottomFrame.winfo_height())
        self.__okButtonFrame.pack_propagate(False)
        self.__okButtonFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__fillerFrame4 = Frame(self.__bottomFrame,
                                     bg     = self.__loader.colorPalettes.getColor("window"),
                                     width  = self.__bottomFrame.winfo_width() // 100,
                                     height = self.__bottomFrame.winfo_height())
        self.__fillerFrame4.pack_propagate(False)
        self.__fillerFrame4.pack(side=LEFT, anchor=E, fill=Y)

        self.__saveButtonFrame =   Frame(self.__bottomFrame,
                                     bg     = self.__loader.colorPalettes.getColor("window"),
                                     width  = self.__bottomFrame.winfo_width() // 6,
                                     height = self.__bottomFrame.winfo_height())
        self.__saveButtonFrame.pack_propagate(False)
        self.__saveButtonFrame.pack(side=LEFT, anchor=E, fill=Y)


        self.__fillerFrame5 = Frame(self.__bottomFrame,
                                     bg     = self.__loader.colorPalettes.getColor("window"),
                                     width  = self.__bottomFrame.winfo_width() // 100,
                                     height = self.__bottomFrame.winfo_height())
        self.__fillerFrame4.pack_propagate(False)
        self.__fillerFrame4.pack(side=LEFT, anchor=E, fill=Y)

        self.__cancelButtonFrame =   Frame(self.__bottomFrame,
                                     bg     = self.__loader.colorPalettes.getColor("window"),
                                     width  = self.__bottomFrame.winfo_width() // 6,
                                     height = self.__bottomFrame.winfo_height())
        self.__cancelButtonFrame.pack_propagate(False)
        self.__cancelButtonFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.__okButton = Button(self.__okButtonFrame, name="ok",
                                     bg=self.__loader.colorPalettes.getColor("window"),
                                     text=self.__dictionaries.getWordFromCurrentLanguage("ok"),
                                     font=self.__smallFont, width=999999999,
                                     command = self.saveAllBank
                                     )
        self.__okButton.pack_propagate(False)
        self.__okButton.pack(fill=BOTH)

        self.__saveButton = Button(self.__saveButtonFrame, name="save",
                                     bg=self.__loader.colorPalettes.getColor("window"),
                                     text=self.__dictionaries.getWordFromCurrentLanguage("saveOnly"),
                                     font=self.__smallFont, width=999999999, state = DISABLED,
                                     command = self.saveAllBankNoClose
                                     )
        self.__saveButton.pack_propagate(False)
        self.__saveButton.pack(fill=BOTH)

        self.__cancelButton = Button(self.__cancelButtonFrame, name="cancel",
                                     bg=self.__loader.colorPalettes.getColor("window"),
                                     text=self.__dictionaries.getWordFromCurrentLanguage("cancel"),
                                     font=self.__smallFont, width=999999999,
                                     command = self.__closeWindow
                                     )
        self.__cancelButton.pack_propagate(False)
        self.__cancelButton.pack(fill=BOTH)

        self.changeForReal("global")
        # readonly.bind("<Key>", lambda e: "break")

    def changeArrayVarList(self, event):
        self.selectArray()

    def selectArray(self):
        if len(self.__arrayList) == 0 or self.__selectArrayButton.cget("state") == DISABLED: return

        self.__fillArrayVarListBox(self.__selectedBank,
                                   self.__arrayList[self.__arrayListBox.curselection()[0]],
                                   True
                                   )

    def __insertToNewArray(self):
        if self.__addNewArrayButton.cget("state") == DISABLED: return
        self.__virtualMemory.archieve()
        self.__archieveCounter += 1

        self.__virtualMemory.addArray(self.__newArrayNameVar.get())
        self.__virtualMemory.addItemsToArray(
            self.__newArrayNameVar.get(),
            self.__originalVar[0], self.__originalVar[1]
        )

        self.doTheArrayChange(self.__selectedBank)
        self.__arrayListBox.select_clear(0, END)

        try:
            self.__arrayListBox.select_set(self.__arrayList.index(self.__newArrayNameVar.get()))
        except Exception as e:
            #print(e)
            self.__arrayListBox.select_set(0)

        """
        for num in range(0, len(self.__arrayList)):
            if self.__newArrayNameVar.get() == self.__arrayList[num]:
               self.__arrayListBox.select_set(num)
               break
        """

        self.__newArrayNameVar.set("")
        self.__fillArrayVarListBox(self.__selectedBank,
                                   self.__arrayList[self.__arrayListBox.curselection()[0]],
                                   True)


    def __addToSelectedArray(self):
        if self.__addToSelectedArrayButton.cget("state") == DISABLED or len(self.__arrayList) == 0: return
        self.__virtualMemory.archieve()
        self.__archieveCounter += 1

        self.__virtualMemory.addItemsToArray(
            self.__arrayList[self.__arrayListBox.curselection()[0]],
            self.__originalVar[0],
            self.__originalVar[1]
        )

        self.__fillArrayVarListBox(self.__selectedBank,
                                   self.__arrayList[self.__arrayListBox.curselection()[0]],
                                   True)

        self.__arrayListListBox.select_clear(0, END)
        try:
            self.__arrayListListBox.select_set(self.__arrayVarList.index(self.__originalVar[0]))
        except:
            self.__arrayListListBox.select_set(0)

        self.__addToSelectedArrayButton.config(state = DISABLED)

    def changeAddButtonOnExisting(self):
        values = {
            True: DISABLED, False: NORMAL
        }

        self.__addToSelectedArrayButton.config(
            state = values[self.checkIfVarIsAlreadyInArray()]
        )

    def checkIfVarIsAlreadyInArray(self):
        for name in self.__arrayVarList:
            if len(self.__originalVar) == 0 : return  False
            if self.__originalVar[0] == name: return True
        return False

    def __deleteArray(self):
        if self.__deleteArrayButton.cget("state") == DISABLED or len(self.__arrayList) == 0: return
        self.__virtualMemory.archieve()
        self.__archieveCounter += 1

        name  = self.__arrayList[self.__arrayListBox.curselection()[0]]

        self.__arrayListBox    .select_clear(0, END)
        self.__arrayListListBox.select_clear(0, END)

        #self.__arrayListBox    .delete(0, END)
        self.__arrayListListBox.delete(0, END)

        index = self.__arrayList.index(name)
        self.__arrayList.remove(name)
        self.__arrayListBox.delete(index)
        self.__virtualMemory.removeArray(name)

        self.doTheArrayChange(self.__selectedBank)

        try:
            self.__arrayListBox.select_set(index)
        except:
            self.__arrayListBox.select_set(0)


    def __deleteFromArray(self):
        if self.__deleteVarFromArrayButton.cget("state") == DISABLED or len(self.__arrayVarList) == 0: return
        self.__virtualMemory.archieve()
        self.__archieveCounter += 1

        name  = self.__arrayVarList[self.__arrayListListBox.curselection()[0]]

        self.__arrayListListBox.select_clear(0, END)
        #self.__arrayListListBox.delete(0, END)

        index = self.__arrayVarList.index(name)

        self.__arrayVarList.remove(name)
        self.__arrayListListBox.delete(index)
        self.__virtualMemory.removeItemFromArray(self.__arrayList[self.__arrayListBox.curselection()[0]], name)

        self.__fillArrayVarListBox(name, self.__arrayList[self.__arrayListBox.curselection()], False)

        try:
            self.__arrayListListBox.select_set(index)
        except:
            self.__arrayListListBox.select_set(0)

    #def __deleteThat(self):
    #    var     = self.__selectedVar
    #    varName = self.__varNameVar.get()

    def addTag(self, Y, X1, X2, tag):
        self.__overLapBox.tag_add(tag, str(Y) + "." + str(X1) , str(Y) + "." + str(X2))

    def __getFont(self):
        baseSize = int(self.__config.getValueByKey("codeBoxFont"))
        w = self.__loader.mainWindow.getWindowSize()[0] / 1600
        h = self.__loader.mainWindow.getWindowSize()[1] / 1200

        self.__fontSize = round((baseSize * w * h) * 1.5)
        self.__normalFont = self.__loader.fontManager.getFont(round(self.__fontSize), False, False, False)
        self.__boldFont = self.__loader.fontManager.getFont(round(self.__fontSize), True, False, False)
        self.__italicFont = self.__loader.fontManager.getFont(round(self.__fontSize), False, True, False)
        self.__undelinedFont = self.__loader.fontManager.getFont(round(self.__fontSize), False, False, True)
        self.__boldItalicFont = self.__loader.fontManager.getFont(round(self.__fontSize), True, True, False)
        self.__boldUnderlinedFont = self.__loader.fontManager.getFont(round(self.__fontSize), True, False, True)
        self.__boldItalicUnderLinedFont = self.__loader.fontManager.getFont(round(self.__fontSize), True, True, True)

        self.__tagSettings = {
            "comment": {
                "foreground": self.__loader.colorPalettes.getColor("comment"),
                "font": self.__italicFont
            },
            "warning": {
                "background": self.__loader.colorPalettes.getColor("highLight"),
                "font": self.__normalFont
            },
            "variable": {
                "foreground": self.__loader.colorPalettes.getColor("variable"),
                "font": self.__boldUnderlinedFont
            },
            "error": {
                "foreground": self.__loader.colorPalettes.getColor("boxFontUnSaved"),
                "background": self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                "font": self.__boldFont
           }
        }

        for key in self.__tagSettings:
            if "background" not in self.__tagSettings[key]:
                self.__overLapBox.tag_config(key,
                                          foreground = self.__tagSettings[key]["foreground"],
                                          font = self.__tagSettings[key]["font"])
            elif "foreground" not in self.__tagSettings[key]:
                self.__overLapBox.tag_config(key,
                                          background = self.__tagSettings[key]["background"],
                                          font = self.__tagSettings[key]["font"])
            else:
                self.__overLapBox.tag_config(key,
                                              foreground=self.__tagSettings[key]["foreground"],
                                              background=self.__tagSettings[key]["background"],
                                              font=self.__tagSettings[key]["font"])

        self.__overLapBox.config(font=self.__normalFont)
        self.__overLapBox.tag_raise("sel")

    def __setBit(self, num, state, sound):
        self.__bitsSetters[num]["state"] = state

        if state:
           self.__bitsSetters[num]["switchLabel"].config(image = self.__swOnImg)
           self.__bitsSetters[num]["numberLabel"].config(fg  = self.__loader.colorPalettes.getColor("font"))
        else:
           self.__bitsSetters[num]["switchLabel"].config(image = self.__swOffImg)
           self.__bitsSetters[num]["numberLabel"].config(fg  = self.__loader.colorPalettes.getColor("fontDisabled"))

        if sound and self.__config.getValueByKey("soundOn") == "True":
           sounds = {False: "switchOff", True: "switchOn"}

           self.__loader.soundPlayer.playSound(sounds[state])

    def loop(self):
        try:
            if self.__validName and self.__numBitsOK and len(self.__errorList) == 0:
               self.__createModifyButton.config(state = NORMAL)

            else:
               self.__createModifyButton.config(state = DISABLED)

            if self.unsaved == True:
               #self.__okButton.config(state=NORMAL)
               self.__saveButton.config(state=NORMAL)

            else:
               #self.__okButton.config(state=DISABLED)
               self.__saveButton.config(state=DISABLED)

        except:
            pass

    def checkIfNameIsOK(self, event):
        entry = event.widget
        name  = str(entry).split(".")[-1]

        theValue = {
            "newVarEntry" :  [self.__newVarName.get()     , "var", [self.__addNewButton]],
            "varNameEntry":  [self.__varNameVar.get()     , "var", []],
            "newArrayEntry": [self.__newArrayNameVar.get(), "arr", [self.__addNewArrayButton]]
        }

        error = self.checkName(theValue[name])

        if name == "varNameEntry" and self.__mode == "modify":
           if error == "alreadyVar" and theValue[name][0] == self.__originalVar[0]:
              error = None

        if error == None or theValue[name][0] == "":
           self.__errorLabelVal.set("")
           self.__errorLabel.config(bg=self.__loader.colorPalettes.getColor("window"),
                                    fg=self.__loader.colorPalettes.getColor("font"))
           entry.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                    fg=self.__loader.colorPalettes.getColor("boxFontNormal"))

           if theValue[name][0] != "":
              for item in theValue[name][2]:
                  item.config(state = NORMAL)
           else:
              for item in theValue[name][2]:
                  item.config(state = DISABLED)

        else:
           self.__errorLabelVal.set(self.__dictionaries.getWordFromCurrentLanguage(error))
           self.__errorLabel.config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                                    fg=self.__loader.colorPalettes.getColor("boxFontUnSaved"))
           entry.config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                                      fg=self.__loader.colorPalettes.getColor("boxFontUnSaved"))

           for item in theValue[name][2]:
               item.config(state = DISABLED)

        if name == "varNameEntry":
           if error == None and theValue[name][0] != "":
               self.__validName = True
           else:
               self.__validName = False

    def checkName(self, theThings):
        value    = theThings[0]
        errStart = theThings[1]

        if len(value) < 4:
             return errStart + "NameTooShort"

        if value.startswith("bank"):
           try:
               teszt = int(value[4])
               return "startWithBank"
           except:
               pass

        delimiterList = (self.__loader.config.getValueByKey("validObjDelimiters").replace("\r", "")
                      + " "
                      + self.__loader.config.getValueByKey("validLineDelimiters").replace("\r", "")).split(" ")

        for d in delimiterList:
            if d in value: return "delimiterInName"

        import re

        if len(re.findall(r'^[a-zA-Z][a-zA-Z0-9_-]+$', value)) == 0: return errStart + "NameNotValid"

        for address in self.__loader.virtualMemory.memory.keys():
            if value in self.__memory[address].variables.keys():
               return "alreadyVar"

        if value in self.__loader.virtualMemory.arrays.keys():
           return "alreadyArr"

        kernelText = self.__loader.io.loadKernelElement(self.__loader.virtualMemory.kernel, "main_kernel").split("\n")
        for line in kernelText:
            if " = " in line:
                if line.split(" = ")[0] == value: return "systemVar"

        return None

    def calculateFreeRAM(self):
        basic = 0
        sara = 0
        basicLocal = 0
        saraLocal = 0
        slot = self.__selectedBank

        for address in self.__memory.keys():
            if len(address) == 3:
                basic+=len(self.__memory[address].freeBits["global"])
                if slot != "global":
                    basicLocal += len(self.__memory[address].freeBits[slot])
            else:
                sara+=len(self.__memory[address].freeBits["global"])
                if slot != "global":
                    saraLocal += len(self.__memory[address].freeBits[slot])

        if slot           != "global":
           sara            = saraLocal
           basic           = basicLocal

        self.__saraRAM.set(self.bitNumToFreeRamText(sara))
        self.__basicRAM.set(self.bitNumToFreeRamText(basic))

        #return(basic, basicLocal, sara, saraLocal)

    def bitNumToFreeRamText(self, num):
        txt = ""

        bytes = num // 8
        bits  = num  % 8

        if bytes != 0:
           txt = str(bytes) + "B"

        if bytes != 0 and bits != 0:
           txt += " + "

        if bits !=0:
           txt += str(bits) + "b"

        return txt


    def haunted(self):
        from Haunted import Haunted

        self.__haunted = Haunted(self.__loader, self.__hauntedFrame, self.__topLevelWindow, self)

    def changeSelectedBank(self, event):
        self.changeForReal(str(event.widget).split(".")[-1])

    def changeForReal(self, name):
        if self.unsaved:
           answer = self.__fileDialogs.askYesNoCancel("unSavedChanges", "unSavedChangesText")
           if   answer == "Yes":
                self.createModifyPressed()
           elif answer == "Cancel":
                return

        self.__selectedBank = name

        for key in self.__bankButtons:
            if key == name:
               self.__bankButtons[key].config(
                   fg=self.__loader.colorPalettes.getColor("window"),
                   bg=self.__loader.colorPalettes.getColor("font")
               )
            else:
                self.__bankButtons[key].config(
                    bg=self.__loader.colorPalettes.getColor("window"),
                    fg=self.__loader.colorPalettes.getColor("font")
                )

        self.__variableListBox.select_clear(0, END)
        self.doListBox(name, None)

        self.doTheArrayChange(name)

        if len(self.__varList) == 0:
           self.__mode = "create"
        else:
           self.__mode = "modify"
           self.__varNameVar.set(
               self.__varList[0]
           )

        self.__initStuff()

    def doTheArrayChange(self, name):

        self.__arrayListBox    .select_clear(0, END)
        self.__arrayListListBox.select_clear(0, END)

        self.__arrayListBox    .delete(0, END)
        self.__arrayListListBox.delete(0, END)

        self.__arrayList = []

        for arrayName in self.__virtualMemory.arrays:
            validity = self.__virtualMemory.getArrayValidity(arrayName)

            if validity == "global" or validity == name:
               self.__arrayList.append(arrayName)

        if len(self.__arrayList) > 0:
           self.__arrayList.sort()

           for arrayName in self.__arrayList:
               self.__arrayListBox.insert(END, arrayName)

           self.__arrayListBox.select_set(0)
           self.__deleteArrayButton.config(state = NORMAL)
           self.__selectArrayButton.config(state = NORMAL)
           self.__fillArrayVarListBox(name, self.__arrayList[0], False)
        else:
           self.__deleteArrayButton.config(state = DISABLED)
           self.__selectArrayButton.config(state = DISABLED)

    def __fillArrayVarListBox(self, bank, arrayName, clear):
        self.__arrayVarList = []

        if clear:
           self.__arrayListListBox.select_clear(0, END)
           self.__arrayListListBox.delete(0, END)

        for varName in self.__virtualMemory.arrays[arrayName]:
            self.__arrayVarList.append(varName)

        if len(self.__arrayVarList) > 0:
           self.__arrayVarList.sort()
           self.__deleteVarFromArrayButton.config(state = NORMAL)

           for varName in self.__arrayVarList:
               self.__arrayListListBox.insert(END, varName)

           self.__arrayListListBox.select_set(0)
        else:
           self.__deleteVarFromArrayButton.config(state = DISABLED)


    def doListBox(self, validity, selected):
        writable, readOnly, \
        all, nonSystem = self.__virtualMemory.returnVariablesForBank(validity)

        self.__varList = []
        self.__variableListBox.delete(0, END)

        nonSystem.sort()

        for v in nonSystem:
            var = self.__virtualMemory.getVariableByName2(v)
            if var != False:
                if var.validity == validity:
                    self.__varList.append(v)
                    self.__variableListBox.insert(END, v)

        if len(self.__varList) > 0:
            if selected == None:
               self.__variableListBox.select_set(0)
            else:
               for index in range(0, len(self.__varList)):
                   if self.__varList[index] == selected:
                      self.__variableListBox.select_set(index)
                      break
            self.__selectButton.config(state=NORMAL)
        else:
            self.__selectButton.config(state=DISABLED)

    def __initStuff(self):
        #print(self.__mode)
        self.__createModifyVar.set(self.__dictionaries.getWordFromCurrentLanguage(self.__mode))
        self.unsaved = False
        self.__contentHolder.deSelect()
        self.__varTypeHolder.deSelect()
        self.__encodingTypeHolder.deSelect()
        self.__numBitsOK = True
        self.__errorLabelVal.set("")
        self.__errorLabel.config(fg=self.__loader.colorPalettes.getColor("font"),
                                 bg=self.__loader.colorPalettes.getColor("window"))
        self.__validName = True

        #success = False

        if self.__mode == "create" or len(self.__varList) == 0:
           self.__deleteButton.config(state = DISABLED)
           self.__selectedVar = None
           self.__varAddressEntry.config(state = DISABLED)
           self.__allocTypeHolder.deSelect()
           self.__allocTypeHolder.select(self.__dictionaries.getWordFromCurrentLanguage("dynamicAllocation"), True)
           self.__varAddressVar.set("")

           self.__contentHolder.select(
               self.__dictionaries.getWordFromCurrentLanguage("common"), True
           )
           self.__encodingTypeHolder.select(
               self.__dictionaries.getWordFromCurrentLanguage("binary"), True
           )

           done = False

           order   = []
           while len(order) < len(self.__virtualMemory.types):
                largestNum = 0
                largestName = ""

                for vartype in self.__virtualMemory.types:
                    if vartype in order: continue

                    if largestNum < self.__virtualMemory.types[vartype]:
                       largestName = vartype
                       largestNum  = self.__virtualMemory.types[vartype]

                order.append(largestName)

           for varTyp in order:
               neededBits = self.__virtualMemory.types[varTyp]
               for address in self.__virtualMemory.memory.keys():
                   #bits = self.__virtualMemory.getIfThereAreAvaiableBitNearAndInARow(self.__virtualMemory.memory[address].freeBits[self.__selectedBank],
                   #                                                                  neededBits)

                   bits = self.__virtualMemory.getTheFirstFreeBitsOnAddessAndBank(self.__selectedBank, neededBits, address)

                   if bits == False:
                      continue
                   else:
                      self.__varAddressVar.set(address)
                      done = True
                      for num in range(0, 8):
                          if num in bits:
                             self.__setBit(num, True, False)
                          else:
                             self.__setBit(num, False, False)
                      break

               if done == True:
                  self.__varTypeHolder.select(varTyp, True)
                  break

           self.__originalVar = []
           self.__addToSelectedArrayButton.config(state = DISABLED)
           self.__newArrayName.config(state = DISABLED)

        else:
           self.__deleteButton.config(state = NORMAL)
           name                = self.__varList[self.__variableListBox.curselection()[0]]
           self.__nameToDelete = name
           self.__selectedVar = self.__loader.virtualMemory.getVariableByName(name, self.__selectedBank)

           self.__allocTypeHolder.deSelect()
           if self.__selectedVar.fixedAlloc:
              self.__allocTypeHolder.select(self.__dictionaries.getWordFromCurrentLanguage("staticAdressing")  , True)
           else:
              self.__allocTypeHolder.select(self.__dictionaries.getWordFromCurrentLanguage("dynamicAllocation"), True)

           self.__varTypeHolder.select(self.__selectedVar.type, True)
           for address in self.__virtualMemory.memory.keys():
               if name in self.__virtualMemory.memory[address].variables.keys():
                  self.__varAddressVar.set(address)
                  break

           for num in range(0, 8):
               if num in self.__selectedVar.usedBits:
                  self.__setBit(num, True, False)
               else:
                  self.__setBit(num, False, False)

           if self.__selectedVar.bcd:
              self.__encodingTypeHolder.select(
                  self.__dictionaries.getWordFromCurrentLanguage("bcd"), True
              )
           else:
              self.__encodingTypeHolder.select(
                  self.__dictionaries.getWordFromCurrentLanguage("binary"), True
              )

           if self.__selectedVar.color:
               self.__contentHolder.select(
                   self.__dictionaries.getWordFromCurrentLanguage("colorVar"), True
               )
           else:
               self.__contentHolder.select(
                   self.__dictionaries.getWordFromCurrentLanguage("common"), True
               )

           #self.__addNewArrayButton.config(state = NORMAL)

           try:
               sel = self.__variableListBox.curselection()[0]
           except:
               sel = 0

           self.__originalVar = [
                self.__varList[sel], self.__virtualMemory.getVariableByName2(self.__varList[sel])
           ]

           if len(self.__arrayList) == 0:
              self.__addToSelectedArrayButton.config(state = DISABLED)
           else:
              #self.__addToSelectedArrayButton.config(state = NORMAL)
              self.changeAddButtonOnExisting()

        self.checkBitsOnType(None)
        self.calculateFreeRAM()

        self.checkForOverlaps()

    def displayError(self, word, d, delete):
        if delete == False:
           txt = self.__dictionaries.getWordFromCurrentLanguage(word)
           for key in d:
               txt = txt.replace(key, d[key])

           self.__errorLabelVal.set(txt)
           self.__errorLabel.config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                                     fg=self.__loader.colorPalettes.getColor("boxFontUnSaved"))

           self.__errorList.append([word, txt])

        else:
           self.__errorLabelVal.set("")
           self.__errorLabel.config(bg=self.__loader.colorPalettes.getColor("window"),
                                    fg=self.__loader.colorPalettes.getColor("font"))

           stop = False
           while(stop == False):
               foundOne    = False
               for itemNum in range(0, len(self.__errorList)):
                   if len(self.__errorList) == 0:
                       stop = True
                       break

                   for w in word:
                       if len(self.__errorList) == 0:
                          stop = True
                          break

                       if self.__errorList[itemNum][0] == w:
                          self.__errorList.pop(itemNum)
                          foundOne = True
                          break

                   if stop or foundOne: break

               if foundOne == False:
                  stop = True
                  break

           if len(self.__errorList) > 0:
               self.__errorLabelVal.set(self.__errorList[-1][1])
               self.__errorLabel.config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                                        fg=self.__loader.colorPalettes.getColor("boxFontUnSaved"))

        self.checkForOverlaps()

    def createModifyPressed(self):
        if self.__createModifyButton.cget("state") == DISABLED: return

        changed = False
        if self.__mode == "modify":
           if self.__varNameVar.get() != self.__originalVar[0]:
              changed       = True
              nameWas       = self.__originalVar[0]
              arraysWithVar = []

              for arrName in self.__virtualMemory.arrays:
                  if nameWas in self.__virtualMemory.arrays[arrName]:
                     arraysWithVar.append(arrName)

           self.__virtualMemory.removeVariable(self.__nameToDelete, self.__selectedBank)

        self.__virtualMemory.archieve()
        self.__archieveCounter += 1

        if self.__contentHolder.getSelected() == self.__dictionaries.getWordFromCurrentLanguage("common"):
           color = False
        else:
           color = True

        if self.__encodingTypeHolder.getSelected() == self.__dictionaries.getWordFromCurrentLanguage("bcd"):
           bcd = True
        else:
           bcd = False

        if self.__allocTypeHolder.getSelected() == self.__dictionaries.getWordFromCurrentLanguage("dynamicAllocation"):
           allocType = False
        else:
           allocType = True

        bitsSelected = []

        for num in range(0, 8):
            if self.__bitsSetters[num]["state"]:
               bitsSelected.append(num)

        success = self.__virtualMemory.addVariable(self.__varNameVar.get(), self.__varTypeHolder.getSelected(),
                                  self.__selectedBank, color, bcd, allocType, self.__varAddressVar.get(), bitsSelected
                                  )

        if success == True:
           self.unsaved = True
           self.__mode = "modify"

           self.__variableListBox.select_clear(0, END)
           self.doListBox(self.__selectedBank, self.__varNameVar.get())

           self.__initStuff()

        else:
           self.__virtualMemory.getArcPrev()
           self.__virtualMemory.archieved.pop(-1)
           self.__archieveCounter -= 1

        self.__originalVar = [self.__varNameVar.get(), self.__virtualMemory.getVariableByName2(self.__varNameVar.get())]
        self.changeAddButtonOnExisting()

        self.unsaved = True
        if changed:
           if len(arraysWithVar) > 0:
              for arrName in arraysWithVar:
                  index = self.__virtualMemory.arrays[arrName].index(nameWas)
                  self.__virtualMemory.arrays[arrName][index] = self.__originalVar[0]

           if nameWas in self.__arrayVarList:
              index    = self.__arrayVarList.index(nameWas)
              selected = self.__arrayListListBox.curselection()[0]
              self.__arrayListListBox.select_clear(0, END)

              self.__arrayListListBox.delete(index)
              self.__arrayListListBox.insert(index, self.__originalVar[0])
              self.__arrayListListBox.select_set(selected)

    def deletePressed(self):
        if self.__deleteButton.cget("state") == DISABLED: return

        self.__virtualMemory.archieve()
        self.__archieveCounter += 1

        self.__virtualMemory.removeVariable(self.__nameToDelete, self.__selectedBank)
        self.unsaved = True

        self.__mode = "create"
        self.__variableListBox.select_clear(0, END)
        self.__varNameVar.set("")

        self.__initStuff()

    def saveAllBank(self):
        if self.unsaved: self.saveAllBankNoClose()
        self.__closeWindow()

    def saveAllBankNoClose(self):
        for num in range(1,9):
            self.__virtualMemory.moveVariablesToMemory("bank"+str(num))

        self.__virtualMemory.archieve()
        self.__archieveCounter = 0
        self.unsaved           = False

    def __insertNew(self):
        if self.__addNewButton.cget("state") == DISABLED: return

        self.__mode = "create"
        self.__variableListBox.select_clear(0, END)
        self.__varNameVar.set(self.__newVarName.get())

        self.__initStuff()
        self.__originalVar = []
        self.__addToSelectedArrayButton.config(state = DISABLED)
        self.__newVarName.set("")

    def __doubleClickedListBox(self, event):
        self.__insertSelected()

    def __insertSelected(self):
        if self.__selectButton.cget("state") == DISABLED: return

        self.__varNameVar.set(
            self.__varList[self.__variableListBox.curselection()[0]]
        )
        self.__mode = "modify"
        self.__originalVar = [self.__varNameVar.get(), self.__virtualMemory.getVariableByName2(self.__varNameVar.get())]

        self.__initStuff()

    def checkBitsOnType(self, data):
        self.__numBitsOK = True

        if data == None:
           bitsNeeded   = self.__loader.virtualMemory.types[self.__varTypeHolder.getSelected()]
           bitsSelected = []

           for num in range(0, 8):
               if self.__bitsSetters[num]["state"]:
                  bitsSelected.append(num)
        else:
            bitsNeeded   = data[0]
            bitsSelected = data[1]

        if len(bitsSelected) < bitsNeeded:
           self.displayError("notEnoughBitsSelected", {
               "#TYPE#": self.__varTypeHolder.getSelected(),
               "#NUM#" : str(self.__loader.virtualMemory.types[self.__varTypeHolder.getSelected()]),
           }, False)

           self.__numBitsOK = False
           return

        if bitsNeeded > 1:
           for bitNum in range(0, len(bitsSelected) - 1):
               num1 = bitsSelected[bitNum]
               num2 = bitsSelected[bitNum + 1]

               if abs(num2 - num1) != 1:
                  strList = []
                  for num in bitsSelected:
                      strList.append(str(num))

                  self.__numBitsOK = False
                  self.displayError("bitsAreNotAligned", {"#BITS#": "-".join(strList)}, False)
                  return

        self.displayError(["notEnoughBitsSelected", "bitsAreNotAligned"], {}, True)

    def selectedTypeChanged(self):
        if self.__allocTypeHolder.getSelected() == self.__dictionaries.getWordFromCurrentLanguage("dynamicAllocation"):
           self.selectedAllocTypeChanged()
        else:
            bitsNeeded   = self.__loader.virtualMemory.types[self.__varTypeHolder.getSelected()]
            bitsSelected = []

            for num in range(0, 8):
                if self.__bitsSetters[num]["state"]:
                   bitsSelected.append(num)

            okList = []
            if len(bitsSelected) > bitsNeeded:
               for bitNum in bitsSelected:
                   if len(okList) == 0:
                      okList.append(bitNum)
                   else:
                      if abs(bitNum - okList[-1]) == 1:
                         okList.append(bitNum)
                      else:
                         okList = [bitNum]

                   if len(okList) == bitsNeeded: break

               if okList != bitsSelected:
                  for num in range(0, 8):
                      for num in range(0, 8):
                          if num in okList:
                             self.__setBit(num, True, False)
                          else:
                             self.__setBit(num, False, False)

               bitsSelected = okList

            self.checkBitsOnType([bitsNeeded, bitsSelected])

    def selectedAllocTypeChanged(self):
        if self.__allocTypeHolder.getSelected() == self.__dictionaries.getWordFromCurrentLanguage("dynamicAllocation"):
            self.displayError(["notEnoughBitsSelected", "bitsAreNotAligned"], {}, True)

            self.__varAddressEntry.config(bg = self.__colors.getColor("boxBackNormal"),
                                          fg = self.__colors.getColor("boxFontNormal"))

            done = False
            neededBits = self.__virtualMemory.types[self.__varTypeHolder.getSelected()]
            for address in self.__virtualMemory.memory.keys():
                #bits = self.__virtualMemory.getIfThereAreAvaiableBitNearAndInARow(
                #    self.__virtualMemory.memory[address].freeBits[self.__selectedBank],
                #    neededBits)

                bits = self.__virtualMemory.getTheFirstFreeBitsOnAddessAndBank(self.__selectedBank, neededBits, address)

                if bits == False:
                    continue
                else:
                    #print(neededBits, bits)

                    self.__varAddressVar.set(address)
                    done = True
                    for num in range(0, 8):
                        if num in bits:
                            self.__setBit(num, True, False)
                        else:
                            self.__setBit(num, False, False)
                    break

            if done == False:
                self.displayError("insufficientFreeMemory", {
                    "#TYPE#": self.__varTypeHolder.getSelected(),
                    "#NUM#": str(self.__loader.virtualMemory.types[self.__varTypeHolder.getSelected()])
                }, False)
            else:
                self.displayError(["insufficientFreeMemory"], {}, True)

            self.__varAddressEntry.config(state = DISABLED)
        else:
            self.__varAddressEntry.config(state = NORMAL)

        self.checkForOverlaps()

    def selectedEcondingChanged(self):
        pass

    def selectedContentChanged(self):
        pass

    def addressChanged(self, event):
        if self.__allocTypeHolder.getSelected() == self.__dictionaries.getWordFromCurrentLanguage("dynamicAllocation"):
            self.__varAddressEntry.config(bg=self.__colors.getColor("boxBackNormal"),
                                          fg=self.__colors.getColor("boxFontNormal"))
            return

        val = self.__varAddressVar.get()
        if (len(val) not in (3,5)):
            self.__varAddressEntry.config(bg=self.__colors.getColor("boxBackUnSaved"),
                                          fg=self.__colors.getColor("boxFontUnSaved"))

            self.displayError("invalidMemoryAddress", {}, False)
            return
        else:
            self.__varAddressEntry.config(bg=self.__colors.getColor("boxBackNormal"),
                                          fg=self.__colors.getColor("boxFontNormal"))
            self.displayError(["invalidMemoryAddress"], {}, True)

        for charNum in range(1, len(val)):
            try:
                teszt = int("0x" + val[charNum], 16)
            except:
                self.__varAddressEntry.config(bg=self.__colors.getColor("boxBackUnSaved"),
                                              fg=self.__colors.getColor("boxFontUnSaved"))

                self.displayError("invalidMemoryAddress", {}, False)
                return

        if len(val) == 3:
           firstValid = self.__virtualMemory.lastAddress
           lastValid  = self.__virtualMemory.stactStart  - 1

           valValue   = int(val.replace("$", "0x"), 16)

           if (valValue < firstValid or valValue > lastValid):
               A1 = format(firstValid, "02x").upper()
               A2 = format(lastValid , "02x").upper()

               self.__varAddressEntry.config(bg=self.__colors.getColor("boxBackUnSaved"),
                                             fg=self.__colors.getColor("boxFontUnSaved"))

               self.displayError("invalidBaseMemoryAddress", {"#A1#": A1, "#A2#": A2}, False)
               return
           else:
               self.displayError(["invalidBaseMemoryAddress"], {}, True)

        else:
            firstByte   = val[1:3]
            lastByte    = val[3:5]

            lastByteVal = int("0x" + lastByte, 16)

            if firstByte.upper() != "F0" or (lastByte > 127):
               self.displayError("invalidSaraMemoryAddress", {}, False)
               return

            else:
               self.displayError(["invalidSaraMemoryAddress"], {}, True)

        foundSystem = False
        varName     = ""

        for varName in self.__loader.virtualMemory.memory[val.lower()].variables.keys():
            if self.__loader.virtualMemory.memory[val.lower()].variables[varName].system:
               foundSystem = True
               break

        if foundSystem:
            self.__varAddressEntry.config(bg = self.__colors.getColor("boxBackUnSaved"),
                                          fg = self.__colors.getColor("boxFontUnSaved"))

            self.displayError("systemFound", {"#VAR#": varName, "#ADDRESS#": val}, False)
            return
        else:
            self.__varAddressEntry.config(bg = self.__colors.getColor("boxBackNormal"),
                                          fg = self.__colors.getColor("boxFontNormal"))
            self.displayError(["systemFound"], {}, True)


    def switchClicked(self, event):
        if self.__allocTypeHolder.getSelected() == self.__dictionaries.getWordFromCurrentLanguage("dynamicAllocation"): return

        bitsSelected = []

        for num in range(0, 8):
            if self.__bitsSetters[num]["state"]:
               bitsSelected.append(num)

        num = int(str(event.widget).split(".")[-1][-1])

        if  len(bitsSelected) >= self.__loader.virtualMemory.types[self.__varTypeHolder.getSelected()] \
        and self.__bitsSetters[num]["state"] == False: return

        self.__setBit(num, 1 - self.__bitsSetters[num]["state"], True)

        if num in bitsSelected:
           bitsSelected.remove(num)
        else:
           bitsSelected.append(num)
           bitsSelected.sort()

        self.checkBitsOnType([self.__loader.virtualMemory.types[self.__varTypeHolder.getSelected()], bitsSelected])


    def checkForOverlaps(self):
        address = self.__varAddressVar.get()

        lineNum = 0

        if address in self.__virtualMemory.memory.keys():
           self.__overLapBox.delete("0.0", END)

           for tag in self.__overLapBox.tag_names():
               if tag == "sel": continue
               self.__overLapBox.tag_remove(tag, "0.0", END)

           bitsSelected = []

           for num in range(0, 8):
               if self.__bitsSetters[num]["state"]:
                   bitsSelected.append(num)

           for varName in self.__virtualMemory.memory[address].variables:
               if len(self.__originalVar) > 0:
                  if varName == self.__originalVar[0]: continue

               var = self.__virtualMemory.memory[address].variables[varName]
               bitsbits = [
                   "-","-","-","-","-","-","-","-"
               ]

               wasAny = False

               for bit in var.usedBits:
                   if bit in bitsSelected:
                      bitsbits[7 - bit] = str(bit)
                      wasAny = True

               if wasAny:
                   if   var.system == True:
                        wholeTag = "error"
                   elif self.__selectedBank == var.validity:
                        wholeTag = "warning"
                   else:
                        wholeTag = ""

                   text = var.validity + "\t" + "".join(bitsbits) + "\t" + varName + "\n"
                   self.__overLapBox.insert(END, text)
                   lineNum += 1
                   startPoz = len(var.validity + "\t" + "".join(bitsbits) + "\t")

                   self.addTag(lineNum, startPoz, len(text) + 1, "variable")

                   if wholeTag != "":
                      self.addTag(lineNum, 0, len(text) + 1, wholeTag)
