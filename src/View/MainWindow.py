#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
import os

from tkinter.filedialog import *
from tkinter import messagebox
from FrameContent import FrameContent

class MainWindow:

    def __init__(self, config, dictionaries, screensize, super, tk, soundplayer, fileDialogs):
        self.__config = config
        self.__dictionaries = dictionaries
        self.__screenSize = screensize
        self.__soundPlayer = soundplayer
        self.__fileDialogs = fileDialogs

        super.mainWindow = self
        self.editor = tk

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
        self.__createFrames()
        self.__soundPlayer.playSound("others/snd/Start.wav")

    def __closeWindow(self):
        self.editor.destroy()

    def getWindowSize(self):
        return (self.editor.winfo_width(), self.editor.winfo_height())

    def __createFrames(self):
         self.__createMenuFrame()

    def __createMenuFrame(self):
        self.__buttonMenu = FrameContent(self, self.editor, self.getWindowSize()[0]/3*2, self.getWindowSize()[1]/5, 5, 5)
