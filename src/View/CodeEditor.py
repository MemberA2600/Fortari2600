from tkinter import *
from MainMenuLabel import MainMenuLabel


class CodeEditor:

    def __init__(self, loader, main, left, right, bank, view):
        self.__loader = loader
        self.__container = main
        self.__left = left
        self.__right = right

        self.forceCheck = False
        self.forceValue = None

        self.__loader.frames["CodeEditor"] = self
        self.changed = False

        self.__fontManager = loader.fontManager

        self.__inside = Frame(self.__container, width=100000000, height=1000000,
                              bg=self.__loader.colorPalettes.getColor("window"))

        self.__inside.pack_propagate(False)
        self.__inside.pack(side=BOTTOM, anchor=S)
        self.originalSizeX = self.__inside.winfo_width()
        self.originalSizeY = self.__inside.winfo_height()

        self.title = MainMenuLabel(self.__inside, self.__loader, "codeEditor", 24, "CodeEditor")

        #from SpaceShip import SpaceShip
        #self.__spacesShip = SpaceShip(self.__loader, self.__left)

        from LeftFrameEditor import LeftFrameEditor
        self.leftFrane = LeftFrameEditor(self.__loader, self.__left, bank, view)

        from RightFrameEditor import RightFrameEditor
        self.rightFrame = RightFrameEditor(self.__loader, self.__right, bank, view)

        from CodeBox import CodeBox
        self.codeBox = CodeBox(self.__loader, self, self.__inside)

    def getScales(self):
        return (
            self.__inside.winfo_width() / self.originalSizeX,
            self.__inside.winfo_height() / self.originalSizeY,
        )

    def getWindowSize(self):
        return (
            self.__inside.winfo_width(),
            self.__inside.winfo_height()
        )





