from tkinter import *

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
        self.colorDict = None
        self.tiaTone = None
        self.piaNotes = None
        self.executor = None

        self.frames = {}
        self.menuButtons = {}
        self.bindedVariables = {}
        self.listBoxes = {}

        self.destroyable = []
        self.subMenus = []
        self.stopThreads = []

        self.sections = []
        self.currentEditor = None