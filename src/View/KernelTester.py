from tkinter import *
from SubMenu import SubMenu

class KernelTester:

    def __init__(self, loader):
        self.__loader = loader
        self.__dictionaries = self.__loader.dictionaries

        self.dead = False
        self.__mainWindow = self.__loader.mainWindow

        self.__loader.stopThreads.append(self)

        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs
        self.__fontManager = self.__loader.fontManager
        self.__fontSize = int(self.__screenSize[0]/1300 * self.__screenSize[1]/1050*14)
        self.__colors = self.__loader.colorPalettes
        self.__colorDict = self.__loader.colorDict

        self.__focused = None
        self.__screenSize = self.__loader.screenSize

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize * 0.80), False, False, False)
        self.__smallerFont = self.__fontManager.getFont(int(self.__fontSize * 0.65), False, False, False)


        self.__window = SubMenu(self.__loader, "kernelTester", round(self.__screenSize[0] / 3), round(self.__screenSize[1]/4  - 40), None, self.__addElements, 1)

        self.dead = True

    def __addElements(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()

        self.__title = Label(self.__topLevelWindow, text = self.__dictionaries.getWordFromCurrentLanguage("kernelTester"),
                             bg = self.__loader.colorPalettes.getColor("window"),
                             fg = self.__loader.colorPalettes.getColor("font"),
                             font =  self.__normalFont, justify=CENTER)
        self.__title.pack(side=TOP, anchor = N, fill=X)

        self.__smallTitle = Label(self.__topLevelWindow, text = self.__dictionaries.getWordFromCurrentLanguage("foundOut"),
                             bg = self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                             fg = self.__loader.colorPalettes.getColor("boxFontUnSaved"),
                             font =  self.__smallerFont, justify=CENTER)
        self.__smallTitle.pack(side=TOP, anchor = N, fill=X)

        from KernelTesterLoaderFrame import KernelTesterLoaderFrame

        self.__openKernelFrame = KernelTesterLoaderFrame(self.__loader, self.__topLevelWindow,
                                                         round(self.__topLevel.getTopLevelDimensions()[1]/4.5), self.__smallFont,
                                                         "kernelFile")