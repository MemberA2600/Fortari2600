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

class MainWindow:

    def __init__(self, loader):
        self.dead = False
        self.__loader = loader
        self.__loader.mainWindow = self

        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs

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

        self.editor.deiconify()
        self.editor.focus()

        self.editor.overrideredirect(False)
        self.editor.resizable(True, True)
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

        self.__createFrames()
        #self.selectedItem = ["bank1", "global_variables"]
        self.bindThings()

        self.__soundPlayer.playSound("Start")
        align = Thread(target=self.__scales)
        align.daemon = True
        align.start()

        self.editor.deiconify()
        self.editor.focus()


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
        while self.dead==False:
            if (self.__lastW==self.getWindowSize()[0] and self.__lastH==self.getWindowSize()[1]):
                sleep(0.05)
                continue
            self.__lastW = self.getWindowSize()[0]
            self.__lastH = self.getWindowSize()[1]
            self.__scaleX = self.__lastW / self.__originalW
            self.__scaleY = self.__lastH / self.__originalH
            sleep(0.02)

    def getScales(self):
        return([self.__scaleX, self.__scaleY])

    def __createFrames(self):
         self.__createMenuFrame()
         self.__createSelectorFrame()

         from BFG9000 import BFG9000
         self.__BFG9000 = BFG9000(self.__loader, self.editor, self,
                                  self.__buttonMenu.getFrameSize()[1]+self.__selectMenu1.getFrameSize()[1]
                                  )

    def __createMenuFrame(self):
        self.__buttonMenu = FrameContent(self.__loader, "buttonMenu",
                                         self.getWindowSize()[0]/3*2, self.getWindowSize()[1]/11.25, 5, 5,
                                         99999, 150, 400, 60)

        self.__buttonMaker = ButtonMaker(self.__loader, self.__buttonMenu, self.__createLabel, self.__destroyLabel)

        self.__newButton = self.__buttonMaker.createButton("new", 0,
                                      self.__newButtonFunction, "projectPath" ,
                                       True, None)
        self.__openButton = self.__buttonMaker.createButton("open", 1,
                                       self.__openButtonFunction, "projectPath",
                                        True, None)
        self.__saveButton = self.__buttonMaker.createButton("save", 2,
                                       self.__saveButtonFunction, "projectPath",
                                        False, None)
        self.__saveAllButton = self.__buttonMaker.createButton("saveAll", 3,
                                          self.__saveAllButtonFunction, "projectPath",
                                            False, None)
        self.__closeProjectButton = self.__buttonMaker.createButton("closeProject", 4,
                                          self.__closeProjectButtonFunction, "projectPath",
                                            False, None)
        self.__copyButton = self.__buttonMaker.createButton("copy", 5.5,
                                          self.__copyButtonFunction, None,
                                            False, self.setCopyButton)
        self.__pasteButton = self.__buttonMaker.createButton("paste", 6.5,
                                          self.__pasteButtonFunction, None,
                                            False, self.setPasteButton)
        self.__undoButton = self.__buttonMaker.createButton("undo", 7.5,
                                          self.__undoButtonFunction, None,
                                            False, self.__undoButtonHandler)
        self.__redoButton = self.__buttonMaker.createButton("redo", 8.5,
                                          self.__redoButtonFunction, None,
                                            False, self.__redoButtonHandler)

        self.__spriteButton = self.__buttonMaker.createButton("spriteEditor", 10,
                                          self.__openSpriteEditor, "projectPath",
                                            False, None)

        self.__pfButton = self.__buttonMaker.createButton("playfieldEditor", 11,
                                          self.__openPFEditor, "projectPath",
                                            False, self.__pfButtonHander)

        self.__musicButton = self.__buttonMaker.createButton("music", 12,
                                          self.__openMusicComposer, "projectPath",
                                            False, None)

        self.__64pxPictureButton = self.__buttonMaker.createButton("64pxPicture", 13,
                                          self.__openPictureConverter, "projectPath",
                                            False, None)

        self.__menuLabel = MenuLabel(self.__loader, self.__buttonMenu, "", 0, self.__fontManager)


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


    def __createLabel(self, event):
        try:
            name = str(event.widget).split(".")[-1]
            button = self.__loader.menuButtons[name].getButton()
            if button.cget("state") == DISABLED:
                self.__menuLabel.changeColor(self.__loader.colorPalettes.getColor("fontDisabled"))
            else:
                self.__menuLabel.changeColor(self.__loader.colorPalettes.getColor("font"))

            self.__menuLabel.setText(self.__dictionaries.getWordFromCurrentLanguage(name))
            if name in ["new", "open", "save", "saveAll", "closeProject"]:
                self.__menuLabel.changePlace(0)
            elif name in ["copy", "paste", "undo", "redo"]:
                self.__menuLabel.changePlace(5.5)
            elif name in ["spriteEditor", "playfieldEditor", "colorPalette"]:
                self.__menuLabel.changePlace(10)
        except:
            self.__menuLabel = MenuLabel(self.__loader, self.__buttonMenu, "", 0, self.__fontManager)

    def __destroyLabel(self, event):
        try:
            self.__menuLabel.setText("")
        except:
            self.__menuLabel = MenuLabel(self.__loader, self.__buttonMenu, "", 0, self.__fontManager)

    def __newButtonFunction(self):
        from NewProjectWindow import NewProjectWindow
        w = NewProjectWindow(self.__loader)


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
            sleep(0.1)

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

        open = OpenProjectWindow(self.__loader, self, self.openProject)


    def __openMusicComposer(self):
        from MusicComposer import MusicComposer

        Music = MusicComposer(self.__loader, self, None)

    def __openPictureConverter(self):
        from PictureToCode import PictureToCode

        pictureToCode = PictureToCode(self.__loader, "common", "64pxPicture" , None, None)


    def __openPFEditor(self):
        from PlayfieldEditor import PlayfieldEditor

        PF = PlayfieldEditor(self.__loader, self)

    def __openSpriteEditor(self):
        from SpriteEditor import SpriteEditor

        _7up = SpriteEditor(self.__loader, self)

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
            sleep(1)

    def __pfButtonHander(self, button):
        from time import sleep
        while self.dead==False:
            try:
                # TO DO: write here the pfless kernels!
                if self.__loader.virtualMemory.kernel not in []:
                    self.__undoButton.getButton().config(state=NORMAL)
                else:
                    self.__undoButton.getButton().config(state=DISABLED)
            except:
                pass
            sleep(1)

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
            sleep(1)


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


            sleep(0.4)

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
            sleep(0.4)

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


