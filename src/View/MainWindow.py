#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
import os

from tkinter.filedialog import *
from tkinter import messagebox
from PIL import ImageTk, Image
from threading import Thread

from FrameContent import FrameContent
from MenuButton import MenuButton
from MenuLabel import MenuLabel
from ButtonMaker import ButtonMaker
from SubMenu import SubMenu

from tkinter.simpledialog import *
from tkinter.filedialog import *
from tkinter import messagebox


class MainWindow:

    def __init__(self, loader):
        self.dead = False
        self.__loader = loader
        self.__loader.mainWindow = self

        self.__loopColor = "#000000"

        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs
        self.__colorDict = self.__loader.colorDict
        self.__colors = self.__loader.colorPalettes

        self.__mainFocus = None
        self.__subMenu = None

        self.__subMenuOpened = False
        self.__setProjectPath(None)

        self.focused = None
        self.clipBoardText = None

        self.__loader.mainWindowHander.mainWindow = self
        self.editor = self.__loader.tk

        self.__scaleX=1
        self.__scaleY=1

        self.editor.protocol('WM_DELETE_WINDOW', self.__closeWindow)
        self.editor.title("Fortari2600 v"+self.__config.getValueByKey("version"))
        __w = self.__loader.screenSize[0]-150
        __h = self.__loader.screenSize[1]-200
        self.editor.geometry("%dx%d+%d+%d" % (__w, __h, (
                self.__loader.screenSize[0] / 2-__w/2), (self.__loader.screenSize[1]/2-__h/2-25)))

        self.editor.config(bg=self.__loader.colorPalettes.getColor("window"))
        #self.editor.attributes('-toolwindow', True)


        self.editor.overrideredirect(False)
        #self.editor.resizable(True, True)
        self.editor.minsize(1000,720)
        self.editor.pack_propagate(False)
        self.editor.grid_propagate(False)
        self.editor.iconbitmap("others/img/icon.ico")

        self.__originalW = self.getWindowSize()[0]
        self.__originalH = self.getWindowSize()[1]
        self.__lastW = self.getWindowSize()[0]
        self.__lastH = self.getWindowSize()[1]

        from FontManager import FontManager
        self.__fontManager = FontManager(self.__loader)

        self.__fontSize = int(self.__screenSize[0]/1300 * self.__screenSize[1]/1050*14)

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize*0.65), False, False, False)
        self.__tinyFont = self.__fontManager.getFont(int(self.__fontSize*0.45), False, False, False)
        self.__halfFont = self.__fontManager.getFont(int(self.__fontSize*0.57), False, False, False)

        self.__createFrames()
        #self.selectedItem = ["bank1", "global_variables"]
        self.bindThings()

        from threading import Thread

        self.__soundPlayer.playSound("Start")
        align = Thread(target=self.__scales)
        align.daemon = True
        align.start()

        self.editor.deiconify()
        self.editor.focus()
        self.__loader.tk.iconify()

        t = Thread(target=self.__loopColorThread)
        t.daemon = True
        t.start()

        self.__loader.tk.deiconify()
        self.__loader.tk.focus()

    def getLoopColor(self):
        return self.__loopColor

    def bindThings(self):
        self.__pressedHome = False
        self.__pressedShiftL = False

        self.editor.bind("<Key>", self.pressed)
        self.editor.bind("<KeyRelease>", self.released)
        t  = Thread(target=self.__checkBinded)
        t.daemon = True
        t.start()

    def __setProjectPath(self, path):
        self.projectPath=path
        self.__loader.bindedVariables["projectPath"] = path

    def __closeWindow(self):
        self.editor.destroy()

    def getWindowSize(self):
        return (self.editor.winfo_width(), self.editor.winfo_height())

    def __scales(self):
        from time import sleep
        while self.dead == False:

            if self.__mainFocus == None:
               self.__mainFocus = self.editor.focus_get()

            if self.editor.focus_get() == self.__mainFocus:
                if self.__loader.subMenuDict == {} and self.__subMenuOpened == True:
                    self.__subMenuOpened = False
                    self.__killRemaining()
                else:
                    self.__subMenuOpened = True

                if (self.__lastW==self.getWindowSize()[0] and self.__lastH==self.getWindowSize()[1]):
                    sleep(0.05)
                    continue
                self.__lastW = self.getWindowSize()[0]
                self.__lastH = self.getWindowSize()[1]
                self.__scaleX = self.__lastW / self.__originalW
                self.__scaleY = self.__lastH / self.__originalH
            sleep(0.005)

    def __killRemaining(self):
        import gc
        self.__subMenu = None
        self.__loader.subMenus = []

        for item in gc.get_objects():
            if "filedialog" in str(type(item)):
                print(str(type(item)))

    def getScales(self):
        return([self.__scaleX, self.__scaleY])

    def __createFrames(self):
         self.__fullEditor = Frame(self.editor, width=self.getWindowSize()[0],
                                   height=self.getWindowSize()[1],
                                   bg=self.__colors.getColor("window"))
         self.__fullEditor.pack_propagate(False)
         self.__fullEditor.pack(side=TOP, anchor = N, fill=BOTH)

         self.__buttonMenu = Frame(self.__fullEditor, width=self.getWindowSize()[0],
                                   height=self.getWindowSize()[1]//11.25,
                                   bg=self.__colors.getColor("window"))
         self.__buttonMenu.pack_propagate(False)
         self.__buttonMenu.pack(side=TOP, anchor = N, fill=X)

         self.__createMenuFrame()

         self.__controllerMenu = Frame(self.__fullEditor, width=self.getWindowSize()[0],
                                   height=self.getWindowSize()[1]//30,
                                   bg=self.__colors.getColor("window"))
         self.__controllerMenu.pack_propagate(False)
         self.__controllerMenu.pack(side=TOP, anchor = N, fill=X)

         self.__changerButtons = []

         for num in range(1,9):
             f = Frame(self.__controllerMenu, width=self.getWindowSize()[0]//8,
                                   height=self.getWindowSize()[1]//30,
                                   bg=self.__colors.getColor("window"))
             f.pack_propagate(False)
             f.pack(side=LEFT, anchor = E, fill=Y)

             if num == 1:
               name = "global"
             else:
               name = 'bank'+str(num)

             b = Button(f, bg=self.__loader.colorPalettes.getColor("window"),
                        text = name, name = name,
                        fg = self.__loader.colorPalettes.getColor("font"),
                        width=99999, font=self.__normalFont,
                        state=DISABLED, command = None)
             b.pack_propagate(False)
             b.pack(side=LEFT, anchor=E, fill=BOTH)

             self.__changerButtons.append(b)

         __keys = list(self.__loader.virtualMemory.codes["bank2"].keys())
         __keys.remove('local_variables')
         __keys.remove('special_read_only')
         __keys.remove('screen_top')
         __keys.remove('screen_bottom')

         self.__controllerMenu2 = Frame(self.__fullEditor, width=self.getWindowSize()[0],
                                   height=self.getWindowSize()[1]//30,
                                   bg=self.__colors.getColor("window"))
         self.__controllerMenu2.pack_propagate(False)
         self.__controllerMenu2.pack(side=TOP, anchor = N, fill=X)

         self.__sectionButtons = []

         for num in range(0, len(__keys)):
             f = Frame(self.__controllerMenu2, width=self.getWindowSize()[0]//len(__keys),
                                   height=self.getWindowSize()[1]//30,
                                   bg=self.__colors.getColor("window"))
             f.pack_propagate(False)
             f.pack(side=LEFT, anchor = E, fill=Y)

             b = Button(f, bg=self.__loader.colorPalettes.getColor("window"),
                        text = __keys[num], name = __keys[num],
                        fg = self.__loader.colorPalettes.getColor("font"),
                        width=99999, font=self.__normalFont,
                        state=DISABLED, command = None)
             b.pack_propagate(False)
             b.pack(side=LEFT, anchor=E, fill=BOTH)

             self.__changerButtons.append(b)

         from EditorBigFrame import EditorBigFrame

         self.__bigFrame = EditorBigFrame(self.__loader, self.__fullEditor)


#self.__createSelectorFrame()

         #from BFG9000 import BFG9000
         #self.__BFG9000 = BFG9000(self.__loader, self.editor, self,
         #                         self.__buttonMenu.getFrameSize()[1]+self.__selectMenu1.getFrameSize()[1]
         #                         )

    def __createMenuFrame(self):
        #self.__buttonMenu = FrameContent(self.__loader, "buttonMenu",
        #                                 self.getWindowSize()[0]/3*2, self.getWindowSize()[1]/11.25, 5, 5,
        #                                 99999, 150, 400, 60)

        self.__places = {}

        self.__buttonMaker = ButtonMaker(self.__loader, self.__buttonMenu, self.__createLabel, self.__destroyLabel)

        self.__newButton = self.__buttonMaker.createButton("new", 0,
                                      self.__newButtonFunction, "projectPath" ,
                                       True, None, self.__places, 0)
        self.__openButton = self.__buttonMaker.createButton("open", 1,
                                       self.__openButtonFunction, "projectPath",
                                        True, None, self.__places, 0)
        self.__saveButton = self.__buttonMaker.createButton("save", 2,
                                       self.__saveButtonFunction, "projectPath",
                                        False, None, self.__places, 0)
        self.__saveAllButton = self.__buttonMaker.createButton("saveAll", 3,
                                          self.__saveAllButtonFunction, "projectPath",
                                            False, None, self.__places, 0)
        self.__closeProjectButton = self.__buttonMaker.createButton("closeProject", 4,
                                          self.__closeProjectButtonFunction, "projectPath",
                                            False, None, self.__places, 0)
        self.__copyButton = self.__buttonMaker.createButton("copy", 5.5,
                                          self.__copyButtonFunction, None,
                                            False, self.setCopyButton, self.__places, 5.5)
        self.__pasteButton = self.__buttonMaker.createButton("paste", 6.5,
                                          self.__pasteButtonFunction, None,
                                            False, self.setPasteButton, self.__places, 5.5)
        self.__undoButton = self.__buttonMaker.createButton("undo", 7.5,
                                          self.__undoButtonFunction, None,
                                            False, self.__undoButtonHandler, self.__places, 5.5)
        self.__redoButton = self.__buttonMaker.createButton("redo", 8.5,
                                          self.__redoButtonFunction, None,
                                            False, self.__redoButtonHandler, self.__places, 5.5)

        self.__spriteButton = self.__buttonMaker.createButton("spriteEditor", 10,
                                          self.__openSpriteEditor, "projectPath",
                                            False, None, self.__places, 10)

        self.__pfButton = self.__buttonMaker.createButton("playfieldEditor", 11,
                                          self.__openPFEditor, "projectPath",
                                            False, None, self.__places, 10)

        self.__musicButton = self.__buttonMaker.createButton("music", 12,
                                          self.__openMusicComposer, "projectPath",
                                            False, None, self.__places, 10)

        self.__64pxPictureButton = self.__buttonMaker.createButton("64pxPicture", 13,
                                          self.__openPictureConverter, "projectPath",
                                            False, None, self.__places, 10)

        self.__soundPlayerButton = self.__buttonMaker.createButton("soundPlayer", 14,
                                          self.__openSoundPlayer, "projectPath",
                                            False, None, self.__places, 10)

        self.__lockManagerButton = self.__buttonMaker.createButton("lockManager", 15.5,
                                          self.__openLockManager, "projectPath",
                                            False, None, self.__places, 15.5)

        self.__lockManagerButton = self.__buttonMaker.createButton("memoryManager", 16.5,
                                          self.openMemoryManager, "projectPath",
                                            False, None, self.__places, 15.5)

        self.__menuLabel = MenuLabel(self.__loader, self.__buttonMenu, "", 0, self.__fontManager)

    """
    def __createSelectorFrame(self):
        self.__selectMenu1 = FrameContent(self.__loader, "bankMenu",
                                         self.getWindowSize()[0] / 7, self.getWindowSize()[1] / 5, 5,
                                         self.__buttonMenu.getFrameSize()[1]+10,
                                         99999, 550, 80, 100)

        from SelectLabel import SelectLabel
        from NewListBoxInFrame import NewListBoxInFrame


        self.__bankLabel = SelectLabel(self.__loader, self.__selectMenu1,
                                       self.__dictionaries.getWordFromCurrentLanguage("selectedBank"),
                                        self.__fontManager
                                       )
        listBoxItems = []
        for num in range(1,9):
            listBoxItems.append("bank"+str(num))

        self.__bankBox = NewListBoxInFrame("bankBox", self.__loader,
                            self.__selectMenu1, listBoxItems, self.checkIfBankChanged, LEFT)


        self.__selectMenu2 = FrameContent(self.__loader, "sectionMenu",
                                         self.getWindowSize()[0] / 6, self.getWindowSize()[1] / 5,
                                         self.__selectMenu1.getFrameSize()[0]+10 ,
                                         self.__buttonMenu.getFrameSize()[1]+10,
                                         99999, 550, 80, 100)

        self.__sectionLabel = SelectLabel(self.__loader, self.__selectMenu2,
                                       self.__dictionaries.getWordFromCurrentLanguage("selectedSection"),
                                        self.__fontManager
                                       )

        self.__tempList = []
        for item in self.__loader.sections:
            if item != "special_read_only":
                self.__tempList.append(item)

        self.__sectionBox = NewListBoxInFrame("sectionBox", self.__loader,
                            self.__selectMenu2, self.__tempList, self.checkIfSectionChanged, LEFT)


        self.__lockMenu = FrameContent(self.__loader, "lockMenu",
                                         self.getWindowSize()[0] / 8, self.getWindowSize()[1] / 5,
                                       (self.__selectMenu1.getFrameSize()[0]+10)*2.25 ,
                                         self.__buttonMenu.getFrameSize()[1]+10,
                                         99999, 550, 80, 100)

        from LockFrame import LockFrame
        self.__lockFrame = LockFrame(self.__loader, self, self.__lockMenu, self.__fontManager)



        self.__changedSelection = Thread(target=self.__listBoxChanges)
        self.__changedSelection.daemon = True
        self.__changedSelection.start()
    """


    def __loopColorThread(self):
        from time import sleep
        colorNum = 0
        while self.__loader.mainWindow.dead == False and self.dead == False:
            colorNum += 1
            if colorNum == 256: colorNum = 0
            hexaNum = hex(colorNum-colorNum%2).replace("0x", "$")
            if len(hexaNum) == 2: hexaNum = "$0"+hexaNum[1]
            self.__loopColor = self.__colorDict.getHEXValueFromTIA(hexaNum)
            sleep(0.025)


    def __createLabel(self, event):
        try:
            name = str(event.widget).split(".")[-1]
            button = self.__loader.menuButtons[name].getButton()
            if button.cget("state") == DISABLED:
                self.__menuLabel.changeColor(self.__loader.colorPalettes.getColor("fontDisabled"))
            else:
                self.__menuLabel.changeColor(self.__loader.colorPalettes.getColor("font"))

            self.__menuLabel.setText(self.__dictionaries.getWordFromCurrentLanguage(name))
            self.__menuLabel.changePlace(self.__places[name])

        except:
            self.__menuLabel = MenuLabel(self.__loader, self.__buttonMenu, "", 0, self.__fontManager)

    def __destroyLabel(self, event):
        try:
            self.__menuLabel.setText("")
        except:
            self.__menuLabel = MenuLabel(self.__loader, self.__buttonMenu, "", 0, self.__fontManager)

    def __newButtonFunction(self):
        from NewProjectWindow import NewProjectWindow
        self.__subMenu = NewProjectWindow(self.__loader)


    def projectOpenedWantToSave(self):
        if self.projectPath!=None and self.__getIfThereIsUnsavedItem() == True:
            return(self.__fileDialogs.askYesOrNo("unsaved","unsavedText"))
        else:
            return("No")

    def __getIfThereIsUnsavedItem(self):
        for bank in self.__loader.virtualMemory.codes.keys():
            for item in self.__loader.virtualMemory.codes[bank].keys():
                if self.__loader.virtualMemory.codes[bank][item].changed == True:
                    return True
        return False

    def checkIfBankChanged(self, listBox):
        if self.projectPath == None:
            self.__loader.listBoxes["bankBox"].getListBoxAndScrollBar()[0].config(state=DISABLED)
        else:
            self.__loader.listBoxes["bankBox"].getListBoxAndScrollBar()[0].config(state=NORMAL)
        num = 0
        for bank in self.__loader.virtualMemory.codes.keys():
            num += 1
            color1 = self.__loader.colorPalettes.getColor("boxBackNormal")
            color2 = self.__loader.colorPalettes.getColor("boxFontNormal")

            for item in self.__loader.virtualMemory.codes[bank].keys():
                if self.__loader.virtualMemory.codes[bank][item].changed == True:
                    color1=self.__loader.colorPalettes.getColor("boxBackUnSaved")
                    color2=self.__loader.colorPalettes.getColor("boxFontUnSaved")
                    break
            listBox.itemconfig(num-1, {"bg": color1})
            listBox.itemconfig(num-1, {"fg": color2})

    def checkIfSectionChanged(self, listBox):
        if (self.__loader.listBoxes["bankBox"].getSelectedName() == "bank1" or
            self.projectPath == None or
                self.__loader.virtualMemory.locks[self.__loader.listBoxes["bankBox"].getSelectedName()]!=None):
            self.__loader.listBoxes["sectionBox"].getListBoxAndScrollBar()[0].config(state=DISABLED)
        else:
            self.__loader.listBoxes["sectionBox"].getListBoxAndScrollBar()[0].config(state=NORMAL)

            num=0
            bank =self.__loader.listBoxes["bankBox"].getSelectedName()
            for item in self.__loader.virtualMemory.codes[bank].keys():
                if item == "special_read_only":
                    continue
                num += 1
                if self.__loader.virtualMemory.codes[bank][item].changed == True:
                    color1 = self.__loader.colorPalettes.getColor("boxBackUnSaved")
                    color2 = self.__loader.colorPalettes.getColor("boxFontUnSaved")
                else:
                    color1 = self.__loader.colorPalettes.getColor("boxBackNormal")
                    color2 = self.__loader.colorPalettes.getColor("boxFontNormal")

                listBox.itemconfig(num-1, {"bg": color1})
                listBox.itemconfig(num-1, {"fg": color2})

    def __listBoxChanges(self):
        bankBox = self.__loader.listBoxes["bankBox"]
        sectionBox = self.__loader.listBoxes["sectionBox"]
        self.__bankSelected = bankBox.getSelectedName()
        self.__sectionSelected = sectionBox.getSelectedName()

        while self.dead == False:
            from time import sleep
            if self.__bankSelected != bankBox.getSelectedName() or self.__sectionSelected != sectionBox.getSelectedName():

                self.__bankSelected = bankBox.getSelectedName()
                try:
                    self.__sectionSelected = sectionBox.getSelectedName()
                except:
                    continue
            sleep(0.005)

    def changeAliasInCodes(self):
        for bank in self.__loader.virtualMemory.codes.keys():
            for section in self.__loader.virtualMemory.codes[bank].keys():
                for command in self.__loader.syntaxList.keys():
                    self.__loader.virtualMemory.codes[bank][section].code = (
                    self.__loader.syntaxList[command].changeAliasToName(
                        command, self.__loader.virtualMemory.codes[bank][section].code
                    ))


    def openProject(self, path):
        try:
            projectPath=path.replace("\\", "/")
            from re import sub
            projectPath = sub("/+", "/", projectPath)
            self.__setProjectPath(projectPath)
            #file = open(self.projectPath+os.sep+name+".project2600", "w")
            #file.write(self.projectPath)
            #file.close()
            self.__loader.config.addProjectPath(projectPath)

            self.__setVirtualMemoryItem("bank1", "bank_configurations")
            self.__setVirtualMemoryItem("bank1", "global_variables")
            for num in range(2,9):
                bank = "bank"+str(num)
                for section in self.__loader.sections:
                    self.__setVirtualMemoryItem(bank, section)

            self.__loader.virtualMemory.setLocksAfterLoading()
            self.__loader.virtualMemory.setVariablesFromMemory("all")
            self.__loader.virtualMemory.archieve()
            self.__soundPlayer.playSound("Success")

        except Exception as e:
            self.__fileDialogs.displayError("projectOpenError", "projectOpenErrorText",
                                            {
                                                "name": self.projectPath.split("/")[-2]
                                            },
                                            str(e)
                                            )
            try:
                self.__closeProject()
            except:
                self.projectPath=""


    def __setVirtualMemoryItem(self, bank, variable):
        path = str(self.projectPath+bank+os.sep+variable+".a26")
        item = self.__loader.virtualMemory.codes[bank][variable]
        item.code = self.__loader.io.loadWholeText(path).replace("%DELIMINATOR%", self.__config.getValueByKey("deliminator"))
        if bank=="bank1" and variable =="bank_configurations":
            old = self.__loader.virtualMemory.kernel
            for line in item.code.split(os.linesep):
                if line.startswith("bank1"):
                    new = line.split("=")[1].replace("\n", "").replace("\r", "")
                    if old != new:
                        self.__loader.virtualMemory.changeKernelMemory(old, new)
        item.changed = False


    def __saveOnlyOne(self, bank, variable):
        try:
            if bank == "bank1":
                variable = "global_variables"
            path = self.projectPath+bank+os.sep+variable+".a26"
            file = open(path, "w", encoding="latin-1")
            BFG9000 = self.__loader.BFG9000.saveFrameToMemory(bank, variable)
            if bank == "bank1" or variable == "local_variables":
                self.__loader.virtualMemory.setVariablesFromMemory(bank)
            file.write(self.__changeFirstValidDeliminator(self.__loader.virtualMemory.codes[bank][variable].code, variable))
            file.close()
            self.__loader.virtualMemory.codes[bank][variable].changed = False
            #self.__loader.virtualMemory.emptyArchieved()
            #item.archived = []
            #item.cursor = 0
        except Exception as e:
            self.__fileDialogs.displayError("projectOpenError", "projectOpenErrorText",
                                            {
                                                "name": variable,
                                                "bank": bank
                                            },
                                            str(e)
                                            )

    def __changeFirstValidDeliminator(self, text, section):
        if section not in ["subroutines","vblank", "enter", "leave", "overscan", "screen_bottom"]:
            return (text)
        newText=[]
        delimiter = self.__config.getValueByKey("deliminator")
        for line in text.split("\n"):
            if line.startswith("*") or line.startswith("#"):
                newText.append(line)
            else:
                valid = 0
                for position in range(0, len(line)-len(delimiter)+1):
                    if line[position] == "(":
                        valid+=1
                    elif line[position] == ")":
                        valid-=1
                    elif valid == 0:
                        if line[position:position+len(delimiter)] == delimiter:
                            line = line[:position] + "%DELIMINATOR%" + line[position+len(delimiter):]
                            break
                newText.append(line)



        return(os.linesep.join(newText))

        #return(self.__config.getValueByKey("deliminator"))

    def __saveProject(self):
        self.__saveOnlyOne("bank1", "bank_configurations")
        self.__saveOnlyOne("bank1", "global_variables")
        for num in range(2, 9):
            bank = "bank" + str(num)
            for section in self.__loader.sections:
                self.__saveOnlyOne(bank, section)

        self.__soundPlayer.playSound("Success")

    def closeProject(self):
        self.__soundPlayer.playSound("Close")
        self.__setProjectPath(None)
        self.__loader.virtualMemory.emptyArchieved()
        self.__loader.virtualMemory.resetMemory()
        self.stopThreads()

    def stopThreads(self):
        for item in self.__loader.stopThreads:
            item.stopThread=True
        self.__loader.stopThreads = []

    def __openButtonFunction(self):
        if self.projectOpenedWantToSave()=="Yes":
            self.saveProject()

        from OpenProjectWindow import OpenProjectWindow

        self.__subMenu = OpenProjectWindow(self.__loader, self, self.openProject)


    def __openMusicComposer(self):
        from MusicComposer import MusicComposer

        self.__subMenu = MusicComposer(self.__loader, self, None)

    def __openPictureConverter(self):
        from PictureToCode import PictureToCode

        self.__subMenu = PictureToCode(self.__loader, "common", "64pxPicture" , None, None)

    def __openSoundPlayer(self):
        from SoundPlayerEditor import SoundPlayerEditor

        self.__subMenu = SoundPlayerEditor(self.__loader, self)

    def __openPFEditor(self):
        from PlayfieldEditor import PlayfieldEditor

        self.__subMenu = PlayfieldEditor(self.__loader, self)

    def __openSpriteEditor(self):
        from SpriteEditor import SpriteEditor

        self.__subMenu = SpriteEditor(self.__loader, self)

    def __saveButtonFunction(self):
        #self.__saveOnlyOne(self.selectedItem[0], self.selectedItem[1])
        self.__saveOnlyOne(self.__loader.listBoxes["bankBox"].getSelectedName(),
                           self.__loader.listBoxes["sectionBox"].getSelectedName())

    def __saveAllButtonFunction(self):
        self.__saveProject()

    def __closeProjectButtonFunction(self):
        if self.projectOpenedWantToSave()=="Yes":
            self.saveProject()
        self.closeProject()

    def __copyButtonFunction(self):
        import clipboard
        clipboard.copy(self.focused.selection_get())
        self.clipBoardText = clipboard.paste()

    def __pasteButtonFunction(self):
        self.focused.insert(INSERT, self.clipBoardText)

    def __undoButtonFunction(self):
        self.__loader.virtualMemory.getArcPrev()

    def __redoButtonFunction(self):
        self.__loader.virtualMemory.getArcNext()

    def __undoButtonHandler(self, button):
        from time import sleep
        while self.dead==False:
            try:
                if len(self.__loader.virtualMemory.archieved)>0 and self.__loader.virtualMemory.cursor>0:
                    self.__undoButton.getButton().config(state=NORMAL)

                else:
                    self.__undoButton.getButton().config(state=DISABLED)
            except:
                pass
            sleep(0.0025)


    def __redoButtonHandler(self, button):
        from time import sleep
        while self.dead==False:
            try:
                if self.__loader.virtualMemory.cursor<len(self.__loader.virtualMemory.archieved)-1:
                    self.__redoButton.getButton().config(state=NORMAL)

                else:
                    self.__redoButton.getButton().config(state=DISABLED)
            except:
                pass
            sleep(0.0025)

    def getConstant(self):
        scalerX = self.getWindowSize()[0]/1300
        scalerY = self.getWindowSize()[1]/1150
        num = round(32*scalerX*scalerY)
        if num>32:
            num=32
        elif num<18:
            num=18
        return(num)

    def focusIn(self, event):
        self.focused = event.widget

    def focusOut(self, event):
        self.focused = None

    def setCopyButton(self, button):
        from time import sleep
        sleep(2)
        while self.dead==False:
            if self.focused == None:
                self.__copyButton.getButton().config(state=DISABLED)
            else:
                self.__copyButton.getButton().config(state=NORMAL)

            sleep(0.0025)

    def setPasteButton(self, button):
        from time import sleep
        sleep(2)
        while self.dead==False:
            if self.focused == None:
                self.__pasteButton.getButton().config(state=DISABLED)
            else:
                if self.clipBoardText == None:
                    self.__pasteButton.getButton().config(state=DISABLED)
                else:
                    self.__pasteButton.getButton().config(state=NORMAL)
            sleep(0.0025)

    def pressed(self, event):
        key = event.keysym

        if key == "Home":
            self.__pressedHome = True
        elif key == "Shift_L" or key == "Shift_R":
            self.__pressedShiftL = True
 

    def released(self, event):
        key = event.keysym
        if key == "Home":
            self.__pressedHome = False
        elif key == "Shift_L" or key == "Shift_R":
            self.__pressedShiftL = False

    def __checkBinded(self):
        from time import sleep
        from threading import Thread

    def __openLockManager(self):
        from LockManagerWindow import LockManagerWindow
        self.__subMenu = LockManagerWindow(self.__loader)

    def openMemoryManager(self):
        from MemoryManagerWindow import MemoryManagerWindow

        self.__subMenu = MemoryManagerWindow(self.__loader)
