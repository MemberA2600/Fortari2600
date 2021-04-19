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

        self.editor.deiconify()
        self.editor.overrideredirect(False)
        self.editor.resizable(True, True)
        self.editor.minsize(750,550)
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
        self.__selectedItem = ["bank1", "global_variables"]

        self.__soundPlayer.playSound("Start")
        align = Thread(target=self.__scales)
        align.daemon = True
        align.start()



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

    def __createMenuFrame(self):
        self.__buttonMenu = FrameContent(self.__loader, "buttonMenu",
                                         self.getWindowSize()[0]/3*2, self.getWindowSize()[1]/10, 5, 5,
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
                                          self.__closeProjectButtonFunction, "projectPath",
                                            False, None)
        self.__pasteButton = self.__buttonMaker.createButton("paste", 6.5,
                                          self.__closeProjectButtonFunction, "projectPath",
                                            False, None)
        self.__undoButton = self.__buttonMaker.createButton("undo", 7.5,
                                          self.__closeProjectButtonFunction, "projectPath",
                                            False, self.__undoButtonHandler)
        self.__redoButton = self.__buttonMaker.createButton("redo", 8.5,
                                          self.__closeProjectButtonFunction, "projectPath",
                                            False, self.__redoButtonHandler)

        self.__spriteButton = self.__buttonMaker.createButton("spriteEditor", 10,
                                          self.__closeProjectButtonFunction, "projectPath",
                                            False, self.__redoButtonHandler)

        self.__pfButton = self.__buttonMaker.createButton("playfieldEditor", 11,
                                          self.__closeProjectButtonFunction, "projectPath",
                                            False, self.__redoButtonHandler)

        self.__menuLabel = MenuLabel(self.__loader, self.__buttonMenu, "", 0, self.__fontManager)

    def __createSelectorFrame(self):
        self.__selectMenu = FrameContent(self.__loader, "selectMenu",
                                         self.getWindowSize()[0]/3*2, self.getWindowSize()[1]/5, 5, self.getWindowSize()[1]/10+10,
                                         99999, 150, 400, 60)


    def __createLabel(self, event):
        try:
            name = str(event.widget).split(".")[-1]
            button = self.__loader.menuButtons[name].getButton()
            if button.cget("state") == DISABLED:
                self.__menuLabel.changeColor("gray")
            else:
                self.__menuLabel.changeColor("black")

            self.__menuLabel.setText(self.__dictionaries.getWordFromCurrentLanguage(name))
            if name in ["new", "open", "save", "saveAll", "closeProject"]:
                self.__menuLabel.changePlace(0)
            elif name in ["copy", "paste", "undo", "redo"]:
                self.__menuLabel.changePlace(5.5)
            elif name in ["spriteEditor", "playfieldEditor"]:
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
        if self.projectPath!="" and self.__getIfThereIsUnsavedItem() == True:
            return(self.__fileDialogs.askYesOrNo("unsaved","unsavedText"))
        else:
            return("No")

    def __getIfThereIsUnsavedItem(self):
        for bank in self.__loader.virtualMemory.codes.keys():
            for item in self.__loader.virtualMemory.codes[bank].keys():
                if self.__loader.virtualMemory.codes[bank][item].changed == True:
                    return True
        return False

    def openProject(self, path):
        try:
            projectPath=path.replace("\\", "/")
            from re import sub
            projectPath = sub("/+", "/", projectPath)
            self.__setProjectPath(projectPath)
            #file = open(self.projectPath+os.sep+name+".project2600", "w")
            #file.write(self.projectPath)
            #file.close()
            self.__setVirtualMemoryItem("bank1", "bank_configurations")
            self.__setVirtualMemoryItem("bank1", "global_variables")
            for num in range(2,9):
                bank = "bank"+str(num)
                self.__setVirtualMemoryItem(bank, "enter")
                self.__setVirtualMemoryItem(bank, "leave")
                self.__setVirtualMemoryItem(bank, "local_variables")
                self.__setVirtualMemoryItem(bank, "overscan")
                self.__setVirtualMemoryItem(bank, "screen_elements")
                self.__setVirtualMemoryItem(bank, "special_read_only")
                self.__setVirtualMemoryItem(bank, "subroutines_and_functions")
                self.__setVirtualMemoryItem(bank, "vblank")

            self.__soundPlayer.playSound("Success")

        except Exception as e:
            self.__fileDialogs.displayError("projectOpenError", "projectOpenErrorText",
                                            {
                                                "name": self.projectPath.split("/")[-2]
                                            },
                                            str(e)
                                            )
            self.__closeProject()

    def __setVirtualMemoryItem(self, bank, variable):
        item = self.__loader.virtualMemory.codes[bank][variable]
        item.code = \
            self.__loader.io.loadWholeText(
                str(self.projectPath+bank+os.sep+variable+".a26")
            )
        item.changed = False
        item.archived = []
        item.cursor = 0


    def __saveOnlyOne(self, bank, variable):
        try:
            path = self.projectPath+bank+os.sep+variable+".a26"
            file = open(path, "w", encoding="latin-1")
            file.write(self.__loader.virtualMemory.codes[bank][variable].code)
            file.close()
            item = self.__loader.virtualMemory.codes[bank][variable]
            item.changed = False
            item.archived = []
            item.cursor = 0
        except Exception as e:
            self.__fileDialogs.displayError("projectOpenError", "projectOpenErrorText",
                                            {
                                                "name": variable,
                                                "bank": bank
                                            },
                                            str(e)
                                            )

    def __saveProject(self):
        self.__saveOnlyOne("bank1", "bank_configurations")
        self.__saveOnlyOne("bank1", "global_variables")
        for num in range(2, 9):
            bank = "bank" + str(num)
            self.__saveOnlyOne(bank, "enter")
            self.__saveOnlyOne(bank, "leave")
            self.__saveOnlyOne(bank, "local_variables")
            self.__saveOnlyOne(bank, "overscan")
            self.__saveOnlyOne(bank, "screen_elements")
            self.__saveOnlyOne(bank, "special_read_only")
            self.__saveOnlyOne(bank, "subroutines_and_functions")
            self.__saveOnlyOne(bank, "vblank")

        self.__soundPlayer.playSound("Success")

    def closeProject(self):
        self.__soundPlayer.playSound("Close")
        self.__setProjectPath(None)

    def __openButtonFunction(self):
        if self.projectOpenedWantToSave()=="Yes":
            self.saveProject()

        projectPath = "/".join(self.__fileDialogs.askForFileName("openProjectIndex", False,
                        ["project2600", "*"], "projects/").replace("\\", "/").split("/")[0:-1])+"/"

        self.openProject(projectPath)


    def __saveButtonFunction(self):
        self.__saveOnlyOne(self.__selectedItem[0], self.__selectedItem[1])

    def __saveAllButtonFunction(self):
        self.__saveProject()

    def __closeProjectButtonFunction(self):
        if self.projectOpenedWantToSave()=="Yes":
            self.saveProject()
        self.closeProject()

    def __copyButtonFunction(self):
        print("DONE!!!")

    def __pasteButtonFunction(self):
        print("DONE!!!")

    def __undoButtonFunction(self):
        print("DONE!!!")

    def __redoButtonFunction(self):
        print("DONE!!!")

    def __undoButtonHandler(self, button):
        from time import sleep
        while True:
            #button.preventRun = True
            #button.getButton().config(state = NORMAL)

            sleep(1)

    def __redoButtonHandler(self, button):
        from time import sleep
        while True:
            #button.preventRun = True
            #button.getButton().config(state = NORMAL)

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