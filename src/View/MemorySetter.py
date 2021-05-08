from tkinter import *
from MainMenuLabel import MainMenuLabel


class MemorySetter:

    def __init__(self, loader, main, left, right, bank, view):
        self.__loader = loader
        self.__container = main
        self.__left = left
        self.__right = right

        validity = bank
        if bank == "bank1":
            validity = "global"


        self.__fontManager = loader.fontManager

        self.__title = MainMenuLabel(self.__container, self.__loader, "memoryManager", 18)

        from RightFrame import RightFrame
        self.rightFrame = RightFrame(self.__loader, self.__right, validity, view)

        from SwitchFrame import SwitchFrame
        self.__switchFrame =  SwitchFrame(self.__container, self.__loader)

        from VariableFrame import VariableFrame
        self.__variableFrame = VariableFrame(self.__container, self.__loader)

        from ArrayFrame import ArrayFrame
        self.__arrayFrame = ArrayFrame(self.__container, self.__loader)

        from SpaceShip import SpaceShip
        self.__spacesShip = SpaceShip(self.__loader, self.__left)

