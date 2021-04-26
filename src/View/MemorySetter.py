from tkinter import *
from SubMenuLabel import SubMenuLabel

class MemorySetter:

    def __init__(self, loader, main, left, right, memoryLevel):
        self.__loader = loader
        self.__container = main
        self.__left = left
        self.__right = right

        self.__fontManager = loader.fontManager
        self.__memoryLevel = memoryLevel

        self.__normalFont = self.__fontManager.getFont("normal", False, False, False)
        self.__smallItalicFont = self.__fontManager.getFont("small", False, True, False)

        self.__title = SubMenuLabel(self.__container, self.__loader, "memoryManager", self.__normalFont)
        #self.__title = SubMenuLabel(self.__container, self.__loader, self.__memoryLevel, self.__smallItalicFont)
