from tkinter import *
from threading import Thread
from PIL import Image, ImageTk
from SubMenu import SubMenu

class LockManagerWindow:

    def __init__(self, loader):
        self.dead = False
        self.__loader=loader
        self.OK = False

        #self.__loader.virtualMemory.locks["bank3"] = "music1"
        #self.__loader.virtualMemory.locks["bank5"] = "waveform1"
        #self.__loader.virtualMemory.locks["bank6"] = "waveform1"

        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs
        self.__fontManager = self.__loader.fontManager
        self.__fontSize = int(self.__screenSize[0]/1300 * self.__screenSize[1]/1050*18)

        self.__screenSize = self.__loader.screenSize

        self.__window = SubMenu(self.__loader, "lockManager", self.__screenSize[0] / 2, self.__screenSize[1] / 5 - 15,
                           None, self.__addElements)
        self.__soundPlayer.playSound("Bounce")
        self.dead = True

    def __addElements(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()

        from Switch import Switch
        self.__banks = []
        for num in range(2,9):
            testbank = Switch(self.__loader, self.__topLevel, self.__topLevelWindow, num, self.__banks)
            self.__banks.append(testbank)