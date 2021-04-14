from SubMenu import SubMenu
from tkinter import *

class NewProjectWindow:

    def __init__(self, loader):

        self.__dead = False
        self.__loader=loader

        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs
        self.__fontManager = self.__loader.fontManager
        self.__fontSize = int(1600/self.__screenSize[0] * 1200/self.__screenSize[1]*18)

        self.__screenSize = self.__loader.screenSize
        self.__window = SubMenu(self.__loader, "new", self.__screenSize[0] / 3, self.__screenSize[1] / 6 - 25,
                           self.__checker, self.__addElements)
        self.__dead = True

    def __addElements(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()
        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.topLabel = Label(self.__topLevelWindow, text = self.__dictionaries.getWordFromCurrentLanguage("projectPath"), font=self.__normalFont)
        self.topLabel.place(x=5, y=5)


    def __checker(self):
        from time import sleep
        while self.__dead == False:

            sleep(1)