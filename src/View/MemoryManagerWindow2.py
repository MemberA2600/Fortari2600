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
        self.__validName = False

        self.__window = SubMenu(self.__loader, "memoryManager", self.__sizes["common"][0],
                                self.__sizes["common"][1], None, self.__addElements, 1)

        self.dead = True

    def __closeWindow(self):
        if self.unsaved == True:
           answer = self.__fileDialogs.askYesOrNo("unsaved", "unsavedText")
           if answer == "Yes":
              self.saveAllBank()

        self.dead = True
        self.__topLevelWindow.destroy()
        self.__loader.topLevels.remove(self.__topLevelWindow)

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
                                     command = self.__insertNew
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
                                     command = self.__insertNew
                                     )
        self.__deleteButton.pack_propagate(False)
        self.__deleteButton.pack(fill=BOTH)

        self.changeForReal("global")
        self.__loader.threadLooper.addToThreading(self, self.loop, [], 1)

    def __setBit(self, num, state, sound):
        self.__bitsSetters[num]["state"] = state

        if state:
           self.__bitsSetters[num]["switchLabel"].config(image = self.__swOnImg)
           self.__bitsSetters[num]["numberLabel"].config(fg  = self.__loader.colorPalettes.getColor("font"))
        else:
           self.__bitsSetters[num]["switchLabel"].config(image = self.__swOff)
           self.__bitsSetters[num]["numberLabel"].config(fg  = self.__loader.colorPalettes.getColor("fontDisabled"))

        if sound and self.__config.getValueByKey("soundOn") == "True":
           sounds = {False: "switchOff", True: "switchOn"}

           self.__loader.soundPlayer.playSound(sounds[state])

    def loop(self):
        try:
            if self.__validName:
               self.__createModifyButton.config(state = NORMAL)

            else:
               self.__createModifyButton.config(state = DISABLED)

        except:
            pass

    def checkIfNameIsOK(self, event):
        entry = event.widget
        name  = str(entry).split(".")[-1]

        theValue = {
            "newVarEntry" : [self.__newVarName.get(), "var", [self.__addNewButton]],
            "varNameEntry": [self.__varNameVar.get(), "var", []]
        }

        error = self.checkName(theValue[name])
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
        writable, readOnly, \
        all     , nonSystem = self.__virtualMemory.returnVariablesForBank(name)

        self.__varList = []
        self.__variableListBox.delete(0, END)

        nonSystem.sort()

        for v in nonSystem:
            var = self.__virtualMemory.getVariableByName2(v)
            if var != False:
               if var.validity == name:
                  self.__varList.append(v)
                  self.__variableListBox.insert(END, v)

        if len(self.__varList) > 0:
           self.__variableListBox.select_set(0)

           self.__selectButton.config(state = NORMAL)
        else:
           self.__selectButton.config(state=DISABLED)

        self.__mode = "create"
        self.__initStuff()

    def __initStuff(self):
        self.__createModifyVar.set(self.__dictionaries.getWordFromCurrentLanguage(self.__mode))
        self.unsaved = False

        success = False

        if self.__mode == "create" or len(self.__varList) == 0:
           self.__deleteButton.config(state = DISABLED)
           self.__selectedVar = None
           self.__varAddressEntry.config(state = DISABLED)
           self.__allocTypeHolder.deSelect()
           self.__allocTypeHolder.select(self.__dictionaries.getWordFromCurrentLanguage("dynamicAllocation"), True)

           done = False
           for varTyp in self.__virtualMemory.types:
               neededBits = self.__virtualMemory.types[varTyp]
               for address in self.__virtualMemory.memory.keys():
                   bits = self.__virtualMemory.getIfThereAreAvaiableBitNearAndInARow(self.__virtualMemory.memory[address].freeBits[self.__selectedBank],
                                                                                     neededBits)
                   if bits == False:
                      continue
                   else:
                      self.__varAddressVar.set(address)
                      done = True
                      for num in range(0, 8):
                          if num in bits:
                             self.__setBit(num, True, False)
                          else:
                             self.__setBit(num, True, False)

                      break
               if done == True: break


        else:
           self.__deleteButton.config(state = NORMAL)
           name = self.__varList[self.__variableListBox.curselection()[0]]
           self.__selectedVar = self.__loader.virtualMemory.getVariableByName(name, self.__selectedBank)

    def displayError(self, word, d):
        if word != "":
           txt = self.__dictionaries.getWordFromCurrentLanguage(word)
           for key in d:
               txt = txt.replace(key, key[d])

           self.__errorLabelVal.set(txt)
           self.__errorLabel.config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                                     fg=self.__loader.colorPalettes.getColor("boxFontUnSaved"))
        else:
           self.__errorLabelVal.set("")
           self.__errorLabel.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                    fg=self.__loader.colorPalettes.getColor("boxFontNormal"))

    def createModifyPressed(self):
        pass

    def deletePressed(self):
        pass

    def saveAllBank(self):
        pass

    def __insertNew(self):
        if self.__addNewButton.cget("state") == DISABLED: return

        self.__mode = "create"
        self.__variableListBox.select_clear(0, END)
        self.__varNameVar.set(self.__newVarName.get())

        self.__initStuff()

    def __insertSelected(self):
        if self.__selectButton.cget("state") == DISABLED: return
        self.__mode = "modify"

        self.__initStuff()

    def selectedTypeChanged(self, event):
        pass

    def selectedAllocTypeChanged(self, event):
        pass

    def addressChanged(self, event):
        if self.__allocTypeHolder.getSelected() == self.__dictionaries.getWordFromCurrentLanguage("dynamicAllocation"): return

    def switchClicked(self, event):
        if self.__allocTypeHolder.getSelected() == self.__dictionaries.getWordFromCurrentLanguage("dynamicAllocation"): return

        num = int(str(event.widget).split(".")[-1])
        self.__setBit(num, 1 - self.__bitsSetters[num]["state"], True)