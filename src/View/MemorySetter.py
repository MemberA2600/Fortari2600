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

        self.__loader.frames["MemorySetter"] = self

        self.__fontManager = loader.fontManager



        self.__inside = Frame(self.__container, width=100000000, height=1000000,
                                 bg = self.__loader.colorPalettes.getColor("window"))

        self.__inside.pack_propagate(False)
        self.__inside.pack(side=BOTTOM, anchor=S)
        self.originalSizeX=self.__inside.winfo_width()
        self.originalSizeY=self.__inside.winfo_height()

        self.title = MainMenuLabel(self.__inside, self.__loader, "memoryManager", 24, "MemorySetter")

        from SpaceShip import SpaceShip
        self.__spacesShip = SpaceShip(self.__loader, self.__left)

        from RightFrame import RightFrame
        self.rightFrame = RightFrame(self.__loader, self.__right, validity, view)


 
        from SwitchFrame import SwitchFrame
        self.__switchFrame =  SwitchFrame(self.__inside, self.__loader)

        from VariableFrame import VariableFrame
        self.__variableFrame = VariableFrame(self.__inside, self.__loader)

        from ArrayFrame import ArrayFrame
        self.__arrayFrame = ArrayFrame(self.__inside, self.__loader)

    def getScales(self):
        return(
            self.__inside.winfo_width() / self.originalSizeX,
            self.__inside.winfo_height() / self.originalSizeY,
        )

    def getWindowSize(self):
        try:
            return(
                self.__inside.winfo_width(),
                self.__inside.winfo_height()
            )
        except Exception as e:
            self.__loader.logger.errorLog(e)





