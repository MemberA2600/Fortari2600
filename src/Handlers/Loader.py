class Loader:
    def __init__(self):
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

        self.frames = {}
        self.menuButtons = {}