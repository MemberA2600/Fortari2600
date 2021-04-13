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

class MainWindow:

    def __init__(self, config, dictionaries, screensize, super, tk,
                 soundplayer, fileDialogs):
        self.__config = config
        self.__dictionaries = dictionaries
        self.__screenSize = screensize
        self.__soundPlayer = soundplayer
        self.__fileDialogs = fileDialogs

        super.mainWindow = self
        self.editor = tk

        self.__scaleX=1
        self.__scaleY=1


        self.editor.protocol('WM_DELETE_WINDOW', self.__closeWindow)
        self.editor.title("Fortari2600 v"+self.__config.getValueByKey("version"))
        __w = screensize[0]-150
        __h = screensize[1]-200
        self.editor.geometry("%dx%d+%d+%d" % (__w, __h, (screensize[0] / 2-__w/2), (screensize[1]/2-__h/2-25)))

        self.editor.deiconify()
        self.editor.overrideredirect(False)
        self.editor.resizable(True, True)
        self.editor.minsize(600,400)
        self.editor.pack_propagate(False)
        self.editor.grid_propagate(False)
        self.editor.iconbitmap("others/img/icon.ico")

        self.__originalW = self.getWindowSize()[0]
        self.__originalH = self.getWindowSize()[1]
        self.__lastW = self.getWindowSize()[0]
        self.__lastH = self.getWindowSize()[1]

        from FontManager import FontManager
        self.__fontManager = FontManager(self)

        self.__createFrames()
        self.__soundPlayer.playSound("others/snd/Start.wav")
        align = Thread(target=self.__scales)
        align.start()



    def __closeWindow(self):
        self.editor.destroy()

    def getWindowSize(self):
        return (self.editor.winfo_width(), self.editor.winfo_height())

    def __scales(self):
        from time import sleep
        while True:
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
        self.__buttonMenu = FrameContent(self, self.editor, self.getWindowSize()[0]/3*2, self.getWindowSize()[1]/5, 5, 5, 99999, 150)
        self.__newButton = MenuButton(self, self.editor, self.__buttonMenu, "new", 0, self.__newButtonFunction)
        self.__openButton = MenuButton(self, self.editor, self.__buttonMenu, "open", 1, self.__openButtonFunction)
        self.__saveButton = MenuButton(self, self.editor, self.__buttonMenu, "save", 2, self.__saveButtonFunction)
        self.__saveAllButton = MenuButton(self, self.editor, self.__buttonMenu, "saveAll", 3, self.__saveAllButtonFunction)
        self.__testLabel = MenuLabel(self, self.editor, self.__buttonMenu, "Ez csak egy teszt.", 0, self.__fontManager)

    def __newButtonFunction(self):
        print("DONE!!!")

    def __openButtonFunction(self):
        print("DONE!!!")

    def __saveButtonFunction(self):
        print("DONE!!!")

    def __saveAllButtonFunction(self):
        print("DONE!!!")

