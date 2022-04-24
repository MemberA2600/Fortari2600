from tkinter import *
from threading import Thread

class Loader:
    def __init__(self):
        self.collector = None
        self.tk = None
        self.dataReader = None
        self.config = None
        self.dictionaries = None
        self.fileDialogs = None
        self.autoSetter = None
        self.soundPlayer = None
        self.screenSize = None
        self.mainWindowHander = None
        self.mainWindow = None
        self.fontManager = None
        self.io = None
        self.virtualMemory = None
        self.colorPalettes = None
        self.codeBox = None
        self.BFG9000 = None
        self.logger = None
        self.syntaxList = {}
        self.atariFrames = []
        self.rocketFrames = []
        self.tapeFrames = []
        self.centipedeFrames = []
        self.lockedFramesTopLevel = []
        self.rainbowFrames = []
        self.colorDict = None
        self.tiaTone = None
        self.piaNotes = None
        self.executor = None
        self.bigFrame = None

        #self.frames = {}
        self.menuButtons = {}
        self.bindedVariables = {}
        #self.listBoxes = {}

        self.topLevels = []
        # self.destroyable = []
        self.subMenus = []
        self.subMenuDict = {}
        self.stopThreads = []

        self.sections = []
        self.currentEditor = None

        #test        = Thread(target=self.__loop)
        #test.daemon = True
        #test.start()

    def __loop(self):

        from time import sleep

        while True:
            try:
                while self.mainWindow.dead == False:
                    print(
                       # f"frames: {self.topLevels}\n",
                        f"menuButtons: {self.menuButtons}\n",
                        f"bindedVariables: {self.bindedVariables}\n",
                       # f"listBoxes: {self.listBoxes}\n",
                        f"topLevels: {self.topLevels}\n",
                       # f"destroyable: {self.destroyable}\n",
                        f"subMenus: {self.subMenus}\n",
                        f"subMenuDict: {self.subMenuDict}\n",
                       # f"stopThreads: {self.stopThreads}\n",
                        f"sections: {self.sections}\n",
                    )
                    sleep(10)

                break

            except:
                sleep(10)