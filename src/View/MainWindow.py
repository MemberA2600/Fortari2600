#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
import os

from tkinter.filedialog import *
from tkinter import messagebox

class MainWindow:

    def __init__(self, config, dictionaries, screensize, super, LSH, tk, soundplayer):
        self.__config = config
        self.__dictionaries = dictionaries
        self.__screenSize = screensize
        self.__soundPlayer = soundplayer

        super.mainWindow = self
        self.editor = tk

        self.__lSH = LSH

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
        self.editor.iconbitmap("others/img/icon.ico")
        self.__soundPlayer.playSound("others/snd/Start.wav")
        self.editor.after(1000, self.__destroyLoader)

    def __closeWindow(self):
        self.editor.destroy()

    def __destroyLoader(self):
        try:
            self.__lSH.destroyScreen()
        except:
            self.editor.after(100, self.__destroyLoader)