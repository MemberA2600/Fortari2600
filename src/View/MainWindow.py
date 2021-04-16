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
        self.__openedProject = False


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

        self.__soundPlayer.playSound("others/snd/Start.wav")
        align = Thread(target=self.__scales)
        align.daemon = True
        align.start()

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

    def __createMenuFrame(self):
        self.__buttonMenu = FrameContent(self.__loader, "buttonMenu",
                                         self.getWindowSize()[0]/3*2, self.getWindowSize()[1]/5, 5, 5,
                                         99999, 150, 400, 60)

        self.__buttonMaker = ButtonMaker(self.__loader, self.__buttonMenu, self.__createLabel, self.__destroyLabel)

        self.__newButton = self.__buttonMaker.createButton("new", 0,
                                      self.__newButtonFunction, self.__openedProject,
                                       True, None)
        self.__openButton = self.__buttonMaker.createButton("open", 1,
                                       self.__openButtonFunction, self.__openedProject,
                                        True, None)
        self.__saveButton = self.__buttonMaker.createButton("save", 2,
                                       self.__saveButtonFunction, self.__openedProject,
                                        False, None)
        self.__saveAllButton = self.__buttonMaker.createButton("saveAll", 3,
                                          self.__saveAllButtonFunction, self.__openedProject,
                                            False, None)
        self.__closeProjectButton = self.__buttonMaker.createButton("closeProject", 4,
                                          self.__closeProjectButtonFunction, self.__openedProject,
                                            False, None)
        self.__copyButton = self.__buttonMaker.createButton("copy", 5.5,
                                          self.__closeProjectButtonFunction, self.__openedProject,
                                            False, None)
        self.__pasteButton = self.__buttonMaker.createButton("paste", 6.5,
                                          self.__closeProjectButtonFunction, self.__openedProject,
                                            False, None)
        self.__undoButton = self.__buttonMaker.createButton("undo", 7.5,
                                          self.__closeProjectButtonFunction, self.__openedProject,
                                            False, self.__undoButtonHandler)
        self.__redoButton = self.__buttonMaker.createButton("redo", 8.5,
                                          self.__closeProjectButtonFunction, self.__openedProject,
                                            False, self.__redoButtonHandler)

        self.__spriteButton = self.__buttonMaker.createButton("spriteEditor", 10,
                                          self.__closeProjectButtonFunction, self.__openedProject,
                                            False, self.__redoButtonHandler)

        self.__pfButton = self.__buttonMaker.createButton("playfieldEditor", 11,
                                          self.__closeProjectButtonFunction, self.__openedProject,
                                            False, self.__redoButtonHandler)

        self.__menuLabel = MenuLabel(self.__loader, self.__buttonMenu, "", 0, self.__fontManager)


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


    def __openButtonFunction(self):
        print("DONE!!!")

    def __saveButtonFunction(self):
        print("DONE!!!")

    def __saveAllButtonFunction(self):
        print("DONE!!!")

    def __closeProjectButtonFunction(self):
        print("DONE!!!")

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