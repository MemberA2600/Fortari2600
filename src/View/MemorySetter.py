from tkinter import *
from MainMenuLabel import MainMenuLabel


class MemorySetter:

    def __init__(self, loader, main, left, right, memoryLevel):
        self.__loader = loader
        self.__container = main
        self.__left = left
        self.__right = right

        self.__fontManager = loader.fontManager
        self.__memoryLevel = memoryLevel

        self.__title = MainMenuLabel(self.__container, self.__loader, "memoryManager", 18)

        from RightFrame import RightFrame

        self.__rightFrame = RightFrame(self.__loader, self.__right)

